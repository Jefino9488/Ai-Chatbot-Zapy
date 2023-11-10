import ttkbootstrap as tk
from ttkbootstrap import *
from tkinter.ttk import Checkbutton, LabelFrame
import tkinter.filedialog as filedialog
import threading
import os
from res import bot_zapy as functions

bot_name = "Zapy"

zapy = functions.ZapyBot()


def create_chat_window():
    def handle_user_input(event=None):
        user_input = input_entry.get()
        chat_display.insert(tk.END, "You: " + user_input + "\n", "user")
        bot_response_thread = threading.Thread(
            target=get_bot_response, args=(user_input, event)
        )
        bot_response_thread.start()
        input_entry.delete(0, tk.END)

    def get_bot_response(user_input, event=None):
        bot_response = zapy.commands(user_input)

        if bot_response is not None:
            chat_display.insert(tk.END, f"{bot_name}: {bot_response}\n", "zapy")
            zapy.say(bot_response)
        else:
            print("Received None response from Zapy.")

        chat_display.see(tk.END)

    def insert_file():
        file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.txt")])

        if file_path:
            file_name = os.path.basename(file_path)
            dest_path = os.path.join("zapy_data", "data", file_name)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            os.rename(file_path, dest_path)

            chat_display.insert(tk.END, "Importing: " + file_name + "\n", "user")

            with open(dest_path, "r") as new_file:
                new_content = new_file.read()

            data_file_path = os.path.join("zapy_data", "data", "data.txt")
            with open(data_file_path, "a") as data_file:
                data_file.write("\n" + new_content)

            os.remove(dest_path)

            zapy.persist_index(zapy.is_persist_enabled)

            chat_display.insert(
                tk.END, "You inserted a file: " + file_name + "\n", "user"
            )

    root = tk.Tk()
    root.title("Zapy")
    root.geometry("800x600")  # Set an initial size

    def toggle_fullscreen():
        root.attributes("-fullscreen", not root.attributes("-fullscreen"))

    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Escape>", toggle_fullscreen)

    chat_frame = tk.Frame(root)
    chat_frame.pack(fill=tk.BOTH, expand=True)

    chat_display = tk.Text(chat_frame, wrap=tk.WORD, bg="lightgray")
    chat_display.pack(
        side=tk.LEFT,
        expand=True,
        padx=(10, 220),
        pady=10,
    )

    scrollbar = tk.Scrollbar(chat_frame, command=chat_display.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    chat_display.config(yscrollcommand=scrollbar.set)

    input_frame = tk.Frame(root)
    input_frame.pack(fill=tk.X, padx=20, pady=10)

    settings_frame = LabelFrame(root, text="Preference")
    settings_frame.place(relx=0.75, rely=0, relwidth=0.25, relheight=1)

    persist_var = tk.BooleanVar()
    persist_var.set(False)  # Initial value
    persist_checkbox = Checkbutton(
        settings_frame, text="Persistence", variable=persist_var
    )
    persist_checkbox.pack(padx=10, pady=10)

    def update_persist_setting():
        zapy.is_persist_enabled = persist_var.get()
        zapy.index = zapy.persist_index(zapy.is_persist_enabled)

    persist_checkbox.config(command=update_persist_setting)

    input_entry = tk.Entry(input_frame, font=("Arial", 12))
    input_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    input_entry_frame = tk.Frame(input_frame)
    input_entry_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    send_button = tk.Button(
        input_entry_frame, text="Send", command=handle_user_input, font=("Arial", 12)
    )

    insert_button = tk.Button(
        input_entry_frame, text="Insert File", command=insert_file, font=("Arial", 12)
    )

    send_button.pack(side=tk.LEFT, padx=5, pady=10)
    insert_button.pack(side=tk.LEFT, padx=5, pady=10)

    input_entry.bind("<Return>", handle_user_input)
    input_entry.focus()

    chat_display.tag_configure("user", justify="right", foreground="blue")
    chat_display.tag_configure("zapy", justify="left", foreground="green")

    root.mainloop()


if __name__ == "__main__":
    create_chat_window()
