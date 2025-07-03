import keyboard
import threading

THREAD_ACTIVE = False


def run_process():
    while THREAD_ACTIVE:
        # Waits until the user presses the "M" key
        print("Press 'M' to continue...")
        keyboard.wait("m")
        print("You pressed M!")


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
