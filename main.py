import tkinter as tk
from tkinter import ttk
import re
import xml.dom.minidom
import json
import os
import sys


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

        dropdown_list = ["SQL Agent log", "Format XML", "Format JSON"]
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
            processed_text = self.clean_sql_log(input_text)
        elif choice == "Format XML":
            processed_text = self.format_xml(input_text)
        elif choice == "Format JSON":
            processed_text = self.format_json(input_text)

        return processed_text

    def clean_sql_log(self, content):
        try:
            cleaned = content
            regex_match = re.search(r"(?im)^\s*Message\s*$", cleaned)
            if regex_match:
                cleaned = cleaned[regex_match.end():].strip()
            else:
                cleaned = cleaned.strip()

            cleaned = re.sub("Executed.*?\\d+-\\d+\\s\\d+:\\d+:\\d+\\.\\d+\\s+", "", cleaned).strip()
            cleaned = re.sub("Code:\\s\\dx.*?\\s+", "", cleaned).strip()
            cleaned = re.sub("\\sEnd\\sError\\s", "", cleaned).strip()
            cleaned = re.sub("Error:.*?\\.\\d\\d\\s\\s", "", cleaned).strip()
            cleaned = re.sub("\\s\\s", "\r\n\r\n", cleaned).strip()

            cleaned_lines = ""
            # loop over each line from the input
            for line in cleaned.splitlines():
                if cleaned_lines.find(line.strip()) == -1:  # remove duplicates
                    # trim extra whitspace and add two line breaks back to the end of each line
                    cleaned_lines += line.strip() + "\r\n\r\n"
            return cleaned_lines.strip()
        except Exception as e:
            return f"Error parsing SQL Agent log: {e}"

    def format_xml(self, xml_string):
        try:
            # Parse the XML string and pretty print it
            dom = xml.dom.minidom.parseString(xml_string)
            pretty_xml_as_string = dom.toprettyxml(indent="   ")
            return pretty_xml_as_string.strip()
        except Exception as e:
            return f"Error formatting XML: {e}"

    def format_json(self, json_string):
        try:
            # Parse the JSON string and pretty print it
            parsed_json = json.loads(json_string)
            pretty_json_as_string = json.dumps(parsed_json, indent=3)
            return pretty_json_as_string.strip()
        except Exception as e:
            return f"Error formatting JSON: {e}"

    def run(self):
        self.root.mainloop()


# --- Entry Point ---
if __name__ == "__main__":
    # Ensure clipboard formats are registered before starting
    app = TextRecasterApp()
    app.run()
