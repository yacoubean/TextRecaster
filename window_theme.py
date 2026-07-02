import tkinter as tk
import sys

if sys.platform == "win32":
    import ctypes


class WindowTheme:
    def create_title_bar(self):
        self.title_bar = tk.Frame(self.window_frame, height=self.TITLE_BAR_HEIGHT, bd=0)
        self.title_bar.grid(row=0, column=0, sticky="ew")
        self.title_bar.grid_propagate(False)
        self.title_bar.columnconfigure(0, weight=1)

        self.title_label = tk.Label(
            self.title_bar,
            text="Text Recaster",
            anchor="w",
            padx=10,
        )
        self.title_label.grid(row=0, column=0, sticky="nsew")

        self.minimize_button = tk.Button(
            self.title_bar,
            text="—",
            command=self.minimize_window,
            width=4,
        )
        self.minimize_button.grid(row=0, column=1, sticky="nsew")

        self.maximize_button = tk.Button(
            self.title_bar,
            text="□",
            command=self.toggle_maximize,
            width=4,
        )
        self.maximize_button.grid(row=0, column=2, sticky="nsew")

        self.close_button = tk.Button(
            self.title_bar,
            text="✕",
            command=self.root.destroy,
            width=4,
        )
        self.close_button.grid(row=0, column=3, sticky="nsew")

        for widget in (self.title_bar, self.title_label):
            widget.bind("<ButtonPress-1>", self.start_window_drag)
            widget.bind("<B1-Motion>", self.drag_window)
            widget.bind("<Double-Button-1>", lambda event: self.toggle_maximize())

    def create_resize_handles(self):
        """Create thin invisible-ish handles around the window for resizing."""
        self.resize_handles = {}

        handle_specs = {
            "n": {"cursor": "sb_v_double_arrow", "relx": 0, "rely": 0, "relwidth": 1, "height": self.RESIZE_BORDER_WIDTH, "anchor": "nw"},
            "s": {"cursor": "sb_v_double_arrow", "relx": 0, "rely": 1, "relwidth": 1, "height": self.RESIZE_BORDER_WIDTH, "anchor": "sw"},
            "w": {"cursor": "sb_h_double_arrow", "relx": 0, "rely": 0, "width": self.RESIZE_BORDER_WIDTH, "relheight": 1, "anchor": "nw"},
            "e": {"cursor": "sb_h_double_arrow", "relx": 1, "rely": 0, "width": self.RESIZE_BORDER_WIDTH, "relheight": 1, "anchor": "ne"},
            "nw": {"cursor": "top_left_corner", "relx": 0, "rely": 0, "width": self.RESIZE_BORDER_WIDTH * 2, "height": self.RESIZE_BORDER_WIDTH * 2, "anchor": "nw"},
            "ne": {"cursor": "top_right_corner", "relx": 1, "rely": 0, "width": self.RESIZE_BORDER_WIDTH * 2, "height": self.RESIZE_BORDER_WIDTH * 2, "anchor": "ne"},
            "sw": {"cursor": "bottom_left_corner", "relx": 0, "rely": 1, "width": self.RESIZE_BORDER_WIDTH * 2, "height": self.RESIZE_BORDER_WIDTH * 2, "anchor": "sw"},
            "se": {"cursor": "bottom_right_corner", "relx": 1, "rely": 1, "width": self.RESIZE_BORDER_WIDTH * 2, "height": self.RESIZE_BORDER_WIDTH * 2, "anchor": "se"},
        }

        for direction, options in handle_specs.items():
            cursor = options.pop("cursor")
            handle = tk.Frame(self.root, cursor=cursor, bd=0, highlightthickness=0)
            handle.place(**options)
            handle.bind("<ButtonPress-1>", lambda event, d=direction: self.start_resize(event, d))
            handle.bind("<B1-Motion>", self.resize_window)
            self.resize_handles[direction] = handle

    def apply_theme(self):
        """Apply the current app theme to all Tk and ttk widgets.

        This is intentionally centralized so a light/dark toggle and config-file
        preference can be added later without hunting through the UI code.
        """
        theme = self.theme

        self.root.configure(bg=theme["window_border"])
        self.window_frame.configure(bg=theme["window_bg"], highlightbackground=theme["window_border"])
        self.title_bar.configure(bg=theme["chrome_bg"])
        self.title_label.configure(
            bg=theme["chrome_bg"],
            fg=theme["chrome_fg"],
            font=("Segoe UI", 10),
        )
        self.content_frame.configure(bg=theme["window_bg"])

        for handle in self.resize_handles.values():
            handle.configure(bg=theme["window_border"])

        self.apply_title_button_style(self.minimize_button)
        self.apply_title_button_style(self.maximize_button)
        self.apply_title_button_style(self.close_button, is_close=True)

        self.apply_ttk_styles()

        self.text_box.configure(
            bg=theme["text_bg"],
            fg=theme["text_fg"],
            insertbackground=theme["text_insert"],
            selectbackground=theme["text_select_bg"],
            selectforeground=theme["text_select_fg"],
            relief="flat",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=theme["text_border"],
            padx=10,
            pady=10,
            undo=True,
        )

        self.button.configure(
            bg=theme["button_bg"],
            fg=theme["button_fg"],
            activebackground=theme["button_active_bg"],
            activeforeground=theme["button_active_fg"],
            disabledforeground="#777777",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            padx=12,
            pady=6,
            cursor="hand2",
        )

    def apply_title_button_style(self, button, is_close=False):
        theme = self.theme
        hover_bg = theme["chrome_close_hover_bg"] if is_close else theme["chrome_hover_bg"]

        button.configure(
            bg=theme["chrome_bg"],
            fg=theme["chrome_fg"],
            activebackground=hover_bg,
            activeforeground="#ffffff",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            font=("Segoe UI", 10),
            cursor="hand2",
        )
        button.bind("<Enter>", lambda event: button.configure(bg=hover_bg, fg="#ffffff"))
        button.bind("<Leave>", lambda event: button.configure(bg=theme["chrome_bg"], fg=theme["chrome_fg"]))

    def apply_ttk_styles(self):
        """Configure ttk widget styles used by the app."""
        theme = self.theme

        self.app_style.configure(
            "TextRecaster.TCombobox",
            background=theme["combo_bg"],
            foreground=theme["combo_fg"],
            fieldbackground=theme["combo_field_bg"],
            selectbackground=theme["combo_select_bg"],
            selectforeground=theme["combo_select_fg"],
            bordercolor=theme["combo_border"],
            lightcolor=theme["combo_border"],
            darkcolor=theme["combo_border"],
            arrowcolor=theme["combo_fg"],
            padding=4,
        )

        self.app_style.map(
            "TextRecaster.TCombobox",
            background=[
                ("readonly", theme["combo_bg"]),
                ("active", theme["combo_bg"]),
            ],
            fieldbackground=[
                ("readonly", theme["combo_field_bg"]),
                ("active", theme["combo_field_bg"]),
            ],
            foreground=[
                ("readonly", theme["combo_fg"]),
                ("active", theme["combo_fg"]),
            ],
            selectbackground=[
                ("readonly", theme["combo_select_bg"]),
            ],
            selectforeground=[
                ("readonly", theme["combo_select_fg"]),
            ],
            arrowcolor=[
                ("readonly", theme["combo_fg"]),
                ("active", theme["combo_fg"]),
            ],
        )

        # The drop-down list portion of ttk.Combobox is backed by Tk's option database.
        self.root.option_add("*TCombobox*Listbox.background", theme["combo_field_bg"])
        self.root.option_add("*TCombobox*Listbox.foreground", theme["combo_fg"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", theme["combo_select_bg"])
        self.root.option_add("*TCombobox*Listbox.selectForeground", theme["combo_select_fg"])

    def set_windows_taskbar_icon(self):
        """Make the borderless window appear as a normal app window on Windows."""
        if sys.platform != "win32":
            return

        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080

        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

        # Hide/show refreshes the style change without a visible flicker in most cases.
        self.root.withdraw()
        self.root.after(10, self.root.deiconify)

    def on_window_mapped(self, event):
        if event.widget == self.root and self.root.state() == "normal":
            self.root.after(10, lambda: self.root.overrideredirect(True))

    def minimize_window(self):
        self.root.overrideredirect(False)
        self.root.iconify()

    def start_window_drag(self, event):
        if self.is_maximized:
            return

        self.drag_start_x = event.x_root - self.root.winfo_x()
        self.drag_start_y = event.y_root - self.root.winfo_y()

    def drag_window(self, event):
        if self.is_maximized:
            return

        x = event.x_root - self.drag_start_x
        y = event.y_root - self.drag_start_y
        self.root.geometry(f"+{x}+{y}")

    def toggle_maximize(self):
        if self.is_maximized:
            self.restore_window()
        else:
            self.maximize_window()

    def maximize_window(self):
        if self.is_maximized:
            return

        self.normal_geometry = self.root.geometry()
        self.is_maximized = True
        self.maximize_button.configure(text="❐")

        # This fills the screen. Avoiding the taskbar exactly requires OS-specific APIs,
        # so we can refine this later if desired.
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

    def restore_window(self):
        if not self.is_maximized:
            return

        self.is_maximized = False
        self.maximize_button.configure(text="□")
        self.root.geometry(self.normal_geometry)

    def restore_if_maximized(self, event=None):
        if self.is_maximized:
            self.restore_window()

    def start_resize(self, event, direction):
        if self.is_maximized:
            return

        self.resize_direction = direction
        self.resize_start_x = event.x_root
        self.resize_start_y = event.y_root
        self.resize_start_width = self.root.winfo_width()
        self.resize_start_height = self.root.winfo_height()
        self.resize_start_root_x = self.root.winfo_x()
        self.resize_start_root_y = self.root.winfo_y()

    def resize_window(self, event):
        if self.is_maximized or not self.resize_direction:
            return

        dx = event.x_root - self.resize_start_x
        dy = event.y_root - self.resize_start_y

        new_width = self.resize_start_width
        new_height = self.resize_start_height
        new_x = self.resize_start_root_x
        new_y = self.resize_start_root_y

        if "e" in self.resize_direction:
            new_width = max(self.MIN_WIDTH, self.resize_start_width + dx)

        if "s" in self.resize_direction:
            new_height = max(self.MIN_HEIGHT, self.resize_start_height + dy)

        if "w" in self.resize_direction:
            proposed_width = self.resize_start_width - dx
            if proposed_width >= self.MIN_WIDTH:
                new_width = proposed_width
                new_x = self.resize_start_root_x + dx

        if "n" in self.resize_direction:
            proposed_height = self.resize_start_height - dy
            if proposed_height >= self.MIN_HEIGHT:
                new_height = proposed_height
                new_y = self.resize_start_root_y + dy

        self.root.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}")
