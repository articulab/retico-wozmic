import retico_wozmic as wozmic
import retico_core


def main(frame_length, rate, audio_file):

    terminal_logger, _ = retico_core.log_utils.configurate_logger()

    mic = wozmic.WOZMicrophoneModule3(frame_length=frame_length, rate=rate, file=audio_file)
    spk = retico_core.audio.SpeakerModule(rate=rate)
    mic.subscribe(spk)

    # running system
    try:
        retico_core.network.run(mic)
        terminal_logger.info("Dialog system running until ENTER key is pressed")
        input()
        retico_core.network.stop(mic)
    except Exception:
        terminal_logger.exception("exception in main")
        retico_core.network.stop(mic)


if __name__ == "__main__":

    frame_length = 0.02
    rate = 48000
    audio_file = "audios/hello48k.wav"
    main(frame_length=frame_length, rate=rate, audio_file=audio_file)
