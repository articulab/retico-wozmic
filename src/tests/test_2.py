import threading
import time
import keyboard

THREAD_ACTIVE = False

def on_key_event(e):
    if e.name == 'm':
        print("M was pressed!")
        time.sleep(1)

def run_process():
    while THREAD_ACTIVE:
        keyboard.on_press(on_key_event)

        # # Keep the program running
        # keyboard.wait('esc')  # Press ESC to stop


if __name__ == "__main__":
    
    THREAD_ACTIVE = True
    threading.Thread(target=run_process).start()
    
    # running system
    try:
        print("Dialog system running until ENTER key is pressed")
        input()
        THREAD_ACTIVE = False
    except Exception as e:
        print("exception in main", e)