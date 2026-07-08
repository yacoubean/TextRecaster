import tkinter as tk
from tkinter import ttk
import os
import sys
from recasters import clean_sql_log, format_xml, format_json, url_decode, url_encode


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class TextRecasterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Text Recaster")
        try:
            self.root.iconbitmap(resource_path("TextRecaster.ico"))
        except tk.TclError:
            print("Icon file not found. Continuing without icon.")
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.BG = '#ffffff'
        self.winx = self.root.winfo_screenwidth() // 2 - self.WINDOW_WIDTH // 2
        self.winy = self.root.winfo_screenheight() // 2 - self.WINDOW_HEIGHT // 2
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{self.winx}+{self.winy}")

        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=0)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.text_box = tk.Text(self.root, wrap="word")
        self.text_box.grid(column=0, row=0, columnspan=2, sticky="nsew", padx=10)

        dropdown_list = ["SQL Agent log", "Format XML", "Format JSON", "URL Decode", "URL Encode"]
        self.dropdown = ttk.Combobox(self.root, values=dropdown_list, state="readonly")
        self.dropdown.set("Choose a format")
        self.dropdown.grid(column=0, row=1, sticky="e", pady=10)

        # Process text button
        self.button = tk.Button(
                        self.root,
                        text="Process text",
                        command=self.on_button_click
                        )
        self.button.grid(column=1, row=1, sticky="w", padx=5, pady=10)

    def on_button_click(self):
        input_text = self.text_box.get("1.0", tk.END).strip()
        format_choice = self.dropdown.get()
        if input_text:
            if format_choice != "Choose a format":
                processed_text = self.process_text(input_text, format_choice)
                self.text_box.delete("1.0", tk.END)
                self.text_box.insert(tk.END, processed_text)

    def process_text(self, input_text, choice):
        processed_text = ""

        if choice == "SQL Agent log":
            processed_text = clean_sql_log(input_text)
        elif choice == "Format XML":
            processed_text = format_xml(input_text)
        elif choice == "Format JSON":
            processed_text = format_json(input_text)
        elif choice == "URL Decode":
            processed_text = url_decode(input_text)
        elif choice == "URL Encode":
            processed_text = url_encode(input_text)

        return processed_text

    def run(self):
        self.root.mainloop()


# --- Entry Point ---
if __name__ == "__main__":
    # Ensure clipboard formats are registered before starting
    app = TextRecasterApp()
    app.run()
