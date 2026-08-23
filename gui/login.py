import tkinter as tk
from tkinter import messagebox

from database.db_connection import get_connection
from gui.dashboard import Dashboard


# ==================================================================
# THEME (colors / fonts lifted from the HTML design)
# ==================================================================

BACKGROUND = "#F7F8FD"
FOREGROUND = "#111111"
PRIMARY = "#5E60F5"
PRIMARY_FOREGROUND = "#FFFFFF"
SECONDARY = "#E1E3FC"
SECONDARY_FOREGROUND = "#111111"
TERTIARY = "#A3ADEA"
MUTED = "#F7F8FD"
MUTED_FOREGROUND = "#6B7280"
CARD = "#FFFFFF"
BORDER = "#E1E3FC"

FONT_HEADING = ("Segoe UI", 20, "bold")
FONT_SUBTITLE = ("Segoe UI", 11)
FONT_LABEL = ("Segoe UI", 11)
FONT_BUTTON = ("Segoe UI", 12, "bold")
FONT_SMALL = ("Segoe UI", 9)


class LoginWindow:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Inventory Management Login"
        )

        self.root.geometry(
            "900x640"
        )

        self.root.resizable(
            False,
            False
        )

        self.root.configure(
            bg=BACKGROUND
        )

        self.create_widgets()

    # ==========================================================
    # CREATE LOGIN GUI
    # ==========================================================

    def create_widgets(self):

        # ------------------------------------------------------
        # HEADER
        # ------------------------------------------------------

        header = tk.Frame(
            self.root,
            bg=BACKGROUND
        )

        header.pack(
            fill="x",
            padx=30,
            pady=20
        )

        header_icon = tk.Label(
            header,
            text="\U0001F4E6",
            font=("Segoe UI", 14),
            bg=SECONDARY,
            fg=PRIMARY,
            width=2,
            height=1
        )

        header_icon.pack(
            side=tk.LEFT
        )

        header_title = tk.Label(
            header,
            text="Inventory Management Login",
            font=("Segoe UI", 13, "bold"),
            bg=BACKGROUND,
            fg=FOREGROUND
        )

        header_title.pack(
            side=tk.LEFT,
            padx=10
        )

        # ------------------------------------------------------
        # MAIN AREA (centers the card)
        # ------------------------------------------------------

        main_area = tk.Frame(
            self.root,
            bg=BACKGROUND
        )

        main_area.pack(
            fill="both",
            expand=True
        )

        # Card container with a thin border to fake the shadow/card look

        card_border = tk.Frame(
            main_area,
            bg=BORDER
        )

        card_border.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        card = tk.Frame(
            card_border,
            bg=CARD,
            padx=50,
            pady=40
        )

        card.pack(
            padx=1,
            pady=1
        )

        # ------------------------------------------------------
        # LOCK ICON
        # ------------------------------------------------------

        icon_canvas = tk.Canvas(
            card,
            width=80,
            height=80,
            bg=CARD,
            highlightthickness=0
        )

        icon_canvas.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(0, 15)
        )

        icon_canvas.create_oval(
            0, 0, 80, 80,
            fill=SECONDARY,
            outline=""
        )

        icon_canvas.create_text(
            40, 40,
            text="\U0001F512",
            font=("Segoe UI", 26)
        )

        # ------------------------------------------------------
        # TITLE / SUBTITLE
        # ------------------------------------------------------

        title = tk.Label(
            card,
            text="Inventory Management Login",
            font=FONT_HEADING,
            bg=CARD,
            fg=FOREGROUND
        )

        title.grid(
            row=1,
            column=0,
            columnspan=2,
            pady=(0, 6)
        )

        subtitle = tk.Label(
            card,
            text="Welcome back! Please login to continue.",
            font=FONT_SUBTITLE,
            bg=CARD,
            fg=MUTED_FOREGROUND
        )

        subtitle.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=(0, 25)
        )

        # ------------------------------------------------------
        # USERNAME
        # ------------------------------------------------------

        username_wrap = tk.Frame(
            card,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        username_wrap.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=8
        )

        username_icon = tk.Label(
            username_wrap,
            text="\U0001F464",
            font=("Segoe UI", 12),
            bg=SECONDARY,
            fg=PRIMARY,
            width=3
        )

        username_icon.pack(
            side=tk.LEFT,
            padx=8,
            pady=8
        )

        self.username_entry = tk.Entry(
            username_wrap,
            font=FONT_LABEL,
            bg=CARD,
            fg=FOREGROUND,
            relief="flat",
            insertbackground=FOREGROUND
        )

        self.username_entry.insert(0, "")
        self.username_entry.pack(
            side=tk.LEFT,
            fill="x",
            expand=True,
            ipady=10,
            padx=(0, 10)
        )

        self._add_placeholder(
            self.username_entry,
            "Username"
        )

        # ------------------------------------------------------
        # PASSWORD
        # ------------------------------------------------------

        password_wrap = tk.Frame(
            card,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        password_wrap.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=8
        )

        password_icon = tk.Label(
            password_wrap,
            text="\U0001F512",
            font=("Segoe UI", 12),
            bg=SECONDARY,
            fg=PRIMARY,
            width=3
        )

        password_icon.pack(
            side=tk.LEFT,
            padx=8,
            pady=8
        )

        self.password_entry = tk.Entry(
            password_wrap,
            font=FONT_LABEL,
            bg=CARD,
            fg=FOREGROUND,
            relief="flat",
            show="*",
            insertbackground=FOREGROUND
        )

        self.password_entry.pack(
            side=tk.LEFT,
            fill="x",
            expand=True,
            ipady=10,
            padx=(0, 10)
        )

        # ------------------------------------------------------
        # REMEMBER ME / FORGOT PASSWORD (decorative, no logic change)
        # ------------------------------------------------------

        options_row = tk.Frame(
            card,
            bg=CARD
        )

        options_row.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(8, 20)
        )

        remember_var = tk.IntVar()

        remember_check = tk.Checkbutton(
            options_row,
            text="Remember me",
            variable=remember_var,
            font=FONT_SMALL,
            bg=CARD,
            fg=MUTED_FOREGROUND,
            activebackground=CARD,
            selectcolor=CARD
        )

        remember_check.pack(
            side=tk.LEFT
        )

        forgot_label = tk.Label(
            options_row,
            text="Forgot Password?",
            font=FONT_SMALL,
            bg=CARD,
            fg=PRIMARY,
            cursor="hand2"
        )

        forgot_label.pack(
            side=tk.RIGHT
        )

        # ------------------------------------------------------
        # LOGIN BUTTON
        # ------------------------------------------------------

        login_button = tk.Button(
            card,
            text="Login  \u2192",
            font=FONT_BUTTON,
            bg=PRIMARY,
            fg=PRIMARY_FOREGROUND,
            activebackground=PRIMARY,
            activeforeground=PRIMARY_FOREGROUND,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.login
        )

        login_button.grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="ew",
            ipady=12
        )

        # ------------------------------------------------------
        # DIVIDER
        # ------------------------------------------------------

        divider_row = tk.Frame(
            card,
            bg=CARD
        )

        divider_row.grid(
            row=7,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=25
        )

        divider_row.columnconfigure(0, weight=1)
        divider_row.columnconfigure(2, weight=1)

        tk.Frame(
            divider_row,
            bg=BORDER,
            height=1
        ).grid(row=0, column=0, sticky="ew")

        tk.Label(
            divider_row,
            text="or",
            font=FONT_SMALL,
            bg=CARD,
            fg=MUTED_FOREGROUND
        ).grid(row=0, column=1, padx=10)

        tk.Frame(
            divider_row,
            bg=BORDER,
            height=1
        ).grid(row=0, column=2, sticky="ew")

        # ------------------------------------------------------
        # LOGIN AS ADMIN (decorative, matches design only)
        # ------------------------------------------------------

        admin_button = tk.Button(
            card,
            text="\U0001F6E1  Login as Admin",
            font=("Segoe UI", 11, "bold"),
            bg=CARD,
            fg=PRIMARY,
            activebackground=CARD,
            activeforeground=PRIMARY,
            relief="flat",
            bd=1,
            highlightbackground=BORDER,
            highlightthickness=1,
            cursor="hand2"
        )

        admin_button.grid(
            row=8,
            column=0,
            columnspan=2,
            sticky="ew",
            ipady=10
        )

        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=1)

        # ------------------------------------------------------
        # FOOTER
        # ------------------------------------------------------

        footer = tk.Label(
            self.root,
            text="\u00A9 2025 Inventory Management System. All rights reserved.",
            font=FONT_SMALL,
            bg=BACKGROUND,
            fg=MUTED_FOREGROUND
        )

        footer.pack(
            side=tk.BOTTOM,
            pady=15
        )

        # Press Enter to login

        self.root.bind(
            "<Return>",
            lambda event: self.login()
        )

        self.username_entry.focus()

    # ==========================================================
    # PLACEHOLDER HELPER (visual only, no functional change)
    # ==========================================================

    def _add_placeholder(self, entry, placeholder):

        entry.insert(0, placeholder)
        entry.config(fg=MUTED_FOREGROUND)

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=FOREGROUND)

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg=MUTED_FOREGROUND)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    # ==========================================================
    # LOGIN
    # ==========================================================

    def login(self):

        username = (
            self.username_entry
            .get()
            .strip()
        )

        if username == "Username":
            username = ""

        password = (
            self.password_entry
            .get()
        )

        # ------------------------------------------------------
        # Empty fields
        # ------------------------------------------------------

        if not username:

            messagebox.showwarning(
                "Login Error",
                "Please enter your username."
            )

            self.username_entry.focus()

            return

        if not password:

            messagebox.showwarning(
                "Login Error",
                "Please enter your password."
            )

            self.password_entry.focus()

            return

        connection = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    user_id,
                    username,
                    role
                FROM users
                WHERE username = ?
                AND password = ?
            """, (
                username,
                password
            ))

            user = cursor.fetchone()

            if user:

                user_id = user[0]
                username = user[1]
                role = user[2]

                self.open_dashboard(
                    user_id,
                    username,
                    role
                )

            else:

                messagebox.showerror(
                    "Login Failed",
                    "Invalid username or password."
                )

                self.password_entry.delete(
                    0,
                    tk.END
                )

                self.password_entry.focus()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not perform login.\n\n{e}"
            )

        finally:

            if connection:

                connection.close()

    # ==========================================================
    # OPEN DASHBOARD
    # ==========================================================

    def open_dashboard(
        self,
        user_id,
        username,
        role
    ):

        # Hide login window

        self.root.withdraw()

        # Create dashboard window

        dashboard_window = tk.Toplevel(
            self.root
        )

        dashboard_window.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )

        Dashboard(
            dashboard_window,
            user_id=user_id,
            username=username,
            role=role
        )

    # ==========================================================
    # CLOSE APPLICATION
    # ==========================================================

    def close_application(self):

        self.root.destroy()


# ==============================================================
# TEST
# ==============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = LoginWindow(root)

    root.mainloop()