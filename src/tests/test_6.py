import time
from pynput import keyboard

CPT = 0
def on_press(key):
    global CPT
    try:
        # if key.char == 'q':
            
        if key.char == 'm':
            print("M was pressed!")
            CPT += 1
    except AttributeError:
        pass


if __name__ == "__main__":
    
    listener = keyboard.Listener(
        on_press=on_press)
    listener.start()
    
    # running system
    try:
        print("Dialog system running until ENTER key is pressed")
        input()
        listener.stop()
    except Exception as e:
        print("exception in main", e)
        
    print(CPT)