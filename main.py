import tkinter as tk
from tkinter import ttk
import re
import xml.dom.minidom
import json
import os
import sys
from window_theme import WindowTheme


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class TextRecasterApp(WindowTheme):
    DARK_THEME = {
        "window_bg": "#1e1e1e",
        "panel_bg": "#1e1e1e",
        "chrome_bg": "#181818",
        "chrome_hover_bg": "#2d2d30",
        "chrome_close_hover_bg": "#c42b1c",
        "chrome_fg": "#c7dfff",
        "window_border": "#3c3c3c",

        "text_bg": "#252526",
        "text_fg": "#c7dfff",
        "text_insert": "#ffffff",
        "text_select_bg": "#264f78",
        "text_select_fg": "#ffffff",
        "text_border": "#3c3c3c",

        "button_bg": "#2d2d30",
        "button_fg": "#c7dfff",
        "button_active_bg": "#3e3e42",
        "button_active_fg": "#ffffff",

        "combo_bg": "#252526",
        "combo_fg": "#c7dfff",
        "combo_field_bg": "#252526",
        "combo_select_bg": "#264f78",
        "combo_select_fg": "#ffffff",
        "combo_border": "#3c3c3c",
    }

    RESIZE_BORDER_WIDTH = 6
    TITLE_BAR_HEIGHT = 34

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Text Recaster")

        try:
            self.root.iconbitmap(resource_path("TextRecaster.ico"))
        except tk.TclError:
            print("Icon file not found. Continuing without icon.")

        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.MIN_WIDTH = 500
        self.MIN_HEIGHT = 350

        self.theme = self.DARK_THEME
        self.app_style = ttk.Style(self.root)

        # "clam" tends to accept custom colors more predictably than native Windows themes.
        self.app_style.theme_use("clam")

        self.winx = self.root.winfo_screenwidth() // 2 - self.WINDOW_WIDTH // 2
        self.winy = self.root.winfo_screenheight() // 2 - self.WINDOW_HEIGHT // 2
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{self.winx}+{self.winy}")
        self.root.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)

        # Remove the native OS title bar/window border so we can draw our own.
        self.root.overrideredirect(True)

        self.is_maximized = False
        self.normal_geometry = self.root.geometry()
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.resize_direction = None
        self.resize_start_x = 0
        self.resize_start_y = 0
        self.resize_start_width = 0
        self.resize_start_height = 0
        self.resize_start_root_x = 0
        self.resize_start_root_y = 0

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.window_frame = tk.Frame(self.root, bd=0, highlightthickness=1)
        self.window_frame.grid(row=0, column=0, sticky="nsew")
        self.window_frame.rowconfigure(0, weight=0)
        self.window_frame.rowconfigure(1, weight=1)
        self.window_frame.columnconfigure(0, weight=1)

        self.create_title_bar()
        self.create_main_content()
        self.create_resize_handles()

        self.apply_theme()

        # Keep borderless window behavior after restoring from the taskbar.
        self.root.bind("<Map>", self.on_window_mapped)
        self.root.bind("<Escape>", self.restore_if_maximized)

        if sys.platform == "win32":
            self.root.after(10, self.set_windows_taskbar_icon)

    def on_button_click(self):
        input_text = self.text_box.get("1.0", tk.END).strip()
        format_choice = self.dropdown.get()

        if input_text:
            if format_choice != "Choose a format":
                processed_text = self.process_text(input_text, format_choice)
                self.text_box.delete("1.0", tk.END)
                self.text_box.insert(tk.END, processed_text)

    def create_main_content(self):
        self.content_frame = tk.Frame(self.window_frame, bd=0)
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.rowconfigure(1, weight=0)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=1)

        self.text_box = tk.Text(self.content_frame, wrap="word")
        self.text_box.grid(column=0, row=0, columnspan=2, sticky="nsew", padx=10, pady=(10, 0))

        dropdown_list = ["SQL Agent log", "Format XML", "Format JSON"]

        self.dropdown = ttk.Combobox(
            self.content_frame,
            values=dropdown_list,
            state="readonly",
            style="TextRecaster.TCombobox"
        )
        self.dropdown.set("Choose a format")
        self.dropdown.grid(column=0, row=1, sticky="e", pady=10)

        # Process text button
        self.button = tk.Button(
            self.content_frame,
            text="Process text",
            command=self.on_button_click
        )
        self.button.grid(column=1, row=1, sticky="w", padx=5, pady=10)

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
            cleaned = re.sub("Executed.*?\\d+-\\d+\\s\\d+:\\d+:\\d+\\.\\d+\\s+", "", cleaned).strip()
            cleaned = re.sub("Code:\\s\\dx.*?\\s+", "", cleaned).strip()
            cleaned = re.sub("\\sEnd\\sError\\s", "", cleaned).strip()
            cleaned = re.sub("Error:.*?\\.\\d\\d\\s\\s", "", cleaned).strip()
            cleaned = re.sub("\\s\\s", "\r\n\r\n", cleaned).strip()
            cleaned_lines = ""

            # loop over each line from the input
            for line in cleaned.splitlines():
                if cleaned_lines.find(line.strip()) == -1:  # remove duplicates
                    # trim extra whitespace and add two line breaks back to the end of each line
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
    app = TextRecasterApp()
    app.run()
