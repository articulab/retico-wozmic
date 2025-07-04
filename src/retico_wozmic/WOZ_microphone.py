"""
MicrophonePTTModule
==================

This module provides push-to-talk capabilities to the classic retico MicrophoneModule
which captures audio signal from the microphone and chunks the audio signal into AudioIUs.
"""

import queue
import sys
import keyboard as keyb
import librosa
from pynput import keyboard
import pyaudio
import os

import retico_core
from retico_core.audio import MicrophoneModule


class WOZMicrophoneModule(MicrophoneModule):
    """A modules overrides the MicrophoneModule which captures audio signal from the microphone and chunks the audio signal into AudioIUs.
    The addition of this module is the introduction of the push-to-talk capacity : the microphone's audio signal is captured only while the M key is pressed.
    """

    @staticmethod
    def name():
        return "WozMicrophone Module"

    @staticmethod
    def description():
        return "A producing module that produce audio from wave file."

    def __init__(
        self,
        file: str = "audios/hello16k.wav",
        frame_length: float = 0.02,
        hotkey_library: str = "pynput",
        **kwargs,
    ):
        super().__init__(**kwargs)

        # Check OS to set rate
        computer_os = sys.platform
        self.terminal_logger.debug(f"OS : {computer_os}", cl="trace")
        if sys.platform.startswith("linux"):
            self.terminal_logger.debug(f"OS is LINUX, forcing to use 48k audio rate", cl="trace")
            file = "audios/hello48k.wav"
            self.rate = 48000

        # Convert relative to absolute path
        if not os.path.isabs(file):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file = os.path.join(base_dir, file)

        self.file = file
        self.frame_length = frame_length
        self._run_thread_active = False
        self.args = None
        self.list_ius = []
        self.silence_ius = []
        self.cpt = 0
        self.play_audio = False
        self.hotkey_library = hotkey_library

    def setup(self, **kwargs):
        super().setup(**kwargs)
        # load data
        audio_data, metadata = retico_core.audio.load_audiofile_PCM16(self.file)
        frame_rate = metadata["rate"]
        n_channels = metadata["n_channels"]
        sample_width = metadata["sampwidth"]

        # convert to mono and resample audio if required and possible
        if self.rate > frame_rate:
            raise NotImplementedError(
                f"your audio file has a smaller sample rate ({frame_rate}) than your target sample rate ({self.rate}), not possible to upsample audio."
            )
        else:
            audio_data_float, sr = librosa.load(self.file, sr=self.rate, mono=True)
            audio_data = retico_core.audio.convert_audio_float32_to_PCM16(audio_data_float)
            n_channels = 1
            # sf.write("audios/test.wav", audio_data_float, self.rate)

        # calculate IUs
        chunk_size = round(self.rate * n_channels * self.frame_length)
        max_cpt = int(len(audio_data) / (chunk_size * sample_width))
        total_time = len(audio_data) / (self.rate * n_channels * sample_width)
        self.terminal_logger.debug(
            "load sound",
            rate_audio_file=frame_rate,
            rate_module=self.rate,
            n_channels=n_channels,
            sample_width=sample_width,
            chunk_size=chunk_size,
            total_time=total_time,
            cl="trace",
        )
        self.list_ius = []
        read_cpt = 0
        while read_cpt < max_cpt:
            sample = audio_data[(chunk_size * sample_width) * read_cpt : (chunk_size * sample_width) * (read_cpt + 1)]
            read_cpt += 1
            output_iu = self.create_iu(
                audio=sample, raw_audio=sample, nframes=chunk_size, rate=self.rate, sample_width=sample_width
            )
            self.list_ius.append((output_iu, retico_core.UpdateType.ADD))

        # init "m" key listener
        if self.hotkey_library == "pynput":
            self.m_listener = keyboard.Listener(on_press=self.on_press)
            self.m_listener.start()

    def on_press(self, key):
        try:
            if key.char == "m":
                self.play_audio = True
        except AttributeError:
            pass

    def callback(self, in_data, frame_count, time_info, status):
        """The callback function that gets called by pyaudio. Stores silence
        audio bytes in audio_buffer, unless the M key is pressed, which then
        makes the function put in the audio_buffer all audio IUs corresponding
        to the woz audio file (IUs one by one, until the end of audio, then
        switch back to silence IUs).

        Args:
            in_data (bytes[]): The raw audio that is coming in from the
                microphone
            frame_count (int): The number of frames that are stored in in_data
        """
        if self.hotkey_library == "keyboard" and keyb.is_pressed("m"):
            self.play_audio = True
        if self.play_audio is True:
            in_data = self.list_ius[self.cpt][0].raw_audio
            if self.cpt == len(self.list_ius) - 1:
                self.cpt = 0
                self.play_audio = False
            else:
                self.cpt += 1
            self.audio_buffer.put(in_data)
        else:
            self.audio_buffer.put(b"\x00" * self.sample_width * self.chunk_size)
        return (in_data, pyaudio.paContinue)

    def process_update(self, _):
        """overrides MicrophoneModule : https://github.com/retico-team/retico-core/blob/main/retico_core/audio.py#202

        Returns:
            UpdateMessage: list of AudioIUs produced from the microphone's audio signal.
        """
        if not self.audio_buffer:
            return None
        try:
            sample = self.audio_buffer.get(timeout=1.0)
        except queue.Empty:
            return None
        output_iu = self.create_iu(
            raw_audio=sample,
            nframes=self.chunk_size,
            rate=self.rate,
            sample_width=self.sample_width,
        )
        return retico_core.UpdateMessage.from_iu(output_iu, retico_core.UpdateType.ADD)

    def shutdown(self):
        """Close the audio stream."""
        if self.stream:
            self.stream.close()
            self.stream = None
        self.audio_buffer = queue.Queue()
        if self.hotkey_library == "pynput":
            self.m_listener.stop()
