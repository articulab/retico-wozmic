import tkinter as tk

def on_key_press(event):
    if event.char.lower() == 'm':
        print("M was pressed!")
    elif event.keysym == 'Escape':
        root.destroy()

root = tk.Tk()
root.title("Key Test")
root.geometry("200x100")

label = tk.Label(root, text="Press 'M' or ESC", font=("Arial", 14))
label.pack(expand=True)

root.bind("<Key>", on_key_press)
root.mainloop()