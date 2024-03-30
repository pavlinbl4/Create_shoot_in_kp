import tkinter as tk
from tkinter import Text, WORD


def get_input_data():
    # function inserts the clipboard content into the Text widget:
    def paste():
        input_field.insert('insert', input_window.clipboard_get())

    # Create a new Tkinter window
    input_window = tk.Tk()

    # Set the title of the window
    input_window.title("Shoot caption")
    input_window.resizable(False, False)

    # Добавляем логику чтобы окно было по центру экрана
    window_height = 200
    window_width = 400
    screen_width = input_window.winfo_screenwidth()
    screen_height = input_window.winfo_screenheight()
    x = int(screen_width / 4 - window_width / 2)
    y = int(screen_height / 2 - window_height / 2)
    input_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a label for the input field
    input_label = tk.Label(input_window, text="Enter the shoot caption:")
    input_label.pack()

    # Create an entry field for the input data
    # input_text = tk.StringVar()

    # old version
    tk.Entry(input_window, width=50)
    input_field = Text(wrap=WORD, font=("Arial", 20), background="#abdbe3")  # #abdbe3     #f4dca8
    input_field.pack(padx=50, pady=50)
    input_field.place(x=10, y=30, width=380, height=130)


    # Create a button to submit the data
    submit_button = tk.Button(input_window, text="Submit", command=input_window.quit, height=1, width=10)
    submit_button.pack(side='bottom', pady=10, anchor='center')
    submit_button.pack()

    # Start the main event loop for the window
    input_window.mainloop()

    input_field.bind('<Control-v>', paste)

    # Bind paste keyboard shortcut
    input_field.bind('<Control-v>', lambda e: input_field.event_generate('<<Paste>>'))

    # Get the entered data from the input field
    input_text = input_field.get("1.0", 'end-1c')

    # Destroy the window after it has been submitted
    input_window.destroy()

    # Return the entered data
    # return input_data
    return input_text


if __name__ == '__main__':
    print(get_input_data())
