import tkinter as tk
from tkinter import messagebox

from gui.suppliers import SupplierWindow
from gui.customers import CustomerWindow
from gui.products import ProductWindow
from gui.billing import BillingWindow
from gui.sales_history import SalesHistoryWindow


# ==================================================================
# THEME
# ==================================================================

BACKGROUND = "#F7F8FD"
FOREGROUND = "#111111"
PRIMARY = "#5E60F5"
PRIMARY_FOREGROUND = "#FFFFFF"
SECONDARY = "#E1E3FC"
SECONDARY_FOREGROUND = "#111111"
TERTIARY = "#A3ADEA"
MUTED_FOREGROUND = "#6B7280"
ACCENT = "#CBCEFA"
CARD = "#FFFFFF"
BORDER = "#E1E3FC"
DESTRUCTIVE = "#DC2626"


FONT_HEADING = ("Segoe UI", 26, "bold")
FONT_SUBHEADING = ("Segoe UI", 13, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_NAV = ("Segoe UI", 11)
FONT_STAT_VALUE = ("Segoe UI", 18, "bold")


class Dashboard:

    def __init__(
        self,
        root,
        user_id=None,
        username=None,
        role=None
    ):

        self.root = root

        self.userid = user_id
        self.username = username or "admin"
        self.role = role

        # Currently selected sidebar item
        self.active_nav = "Dashboard"

        self.root.title(
            "Inventory & Billing System"
        )

        self.root.geometry(
            "1200x750"
        )

        self.root.configure(
            bg=BACKGROUND
        )

        self.create_widgets()

    # ==========================================================
    # CREATE DASHBOARD
    # ==========================================================

    def create_widgets(self):

        self._build_header()

        body = tk.Frame(
            self.root,
            bg=BACKGROUND
        )

        body.pack(
            fill="both",
            expand=True
        )

        # Sidebar
        self._build_sidebar(body)

        # Main content
        main = tk.Frame(
            body,
            bg=BACKGROUND
        )

        main.pack(
            side=tk.LEFT,
            fill="both",
            expand=True,
            padx=40,
            pady=30
        )

        self._build_welcome(main)
        self._build_cards(main)
        self._build_stats(main)
        self._build_footer(main)

    # ==========================================================
    # HEADER
    # ==========================================================

    def _build_header(self):

        header = tk.Frame(
            self.root,
            bg=CARD,
            height=64,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        header.pack(
            fill="x",
            side=tk.TOP
        )

        header.pack_propagate(False)

        # ------------------------------------------------------
        # LEFT HEADER
        # ------------------------------------------------------

        left = tk.Frame(
            header,
            bg=CARD
        )

        left.pack(
            side=tk.LEFT,
            padx=20
        )

        logo_box = tk.Label(
            left,
            text="🏪",
            font=("Segoe UI", 14),
            bg=SECONDARY,
            fg=PRIMARY,
            width=3,
            height=1
        )

        logo_box.pack(
            side=tk.LEFT
        )

        tk.Label(
            left,
            text="Inventory & Billing System",
            font=FONT_SUBHEADING,
            bg=CARD,
            fg=FOREGROUND
        ).pack(
            side=tk.LEFT,
            padx=12
        )

        # ------------------------------------------------------
        # RIGHT HEADER
        # ------------------------------------------------------

        right = tk.Frame(
            header,
            bg=CARD
        )

        right.pack(
            side=tk.RIGHT,
            padx=20
        )

        # Avatar

        avatar = tk.Label(
            right,
            text=self.username[:1].upper(),
            font=("Segoe UI", 12, "bold"),
            bg=SECONDARY,
            fg=PRIMARY,
            width=3,
            height=1
        )

        avatar.pack(
            side=tk.RIGHT,
            padx=(10, 0)
        )

        # Notification

        bell = tk.Label(
            right,
            text="🔔",
            font=("Segoe UI", 12),
            bg=CARD,
            fg=MUTED_FOREGROUND,
            width=3,
            height=1,
            relief="solid",
            bd=1,
            cursor="hand2"
        )

        bell.pack(
            side=tk.RIGHT,
            padx=10
        )

    # ==========================================================
    # SIDEBAR
    # ==========================================================

    def _build_sidebar(self, parent):

        self.sidebar = tk.Frame(
            parent,
            bg=CARD,
            width=220,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        self.sidebar.pack(
            side=tk.LEFT,
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # ------------------------------------------------------
        # TOP SECTION
        # ------------------------------------------------------

        top = tk.Frame(
            self.sidebar,
            bg=CARD
        )

        top.pack(
            fill="x",
            padx=15,
            pady=20
        )

        # Home icon

        home_icon = tk.Label(
            top,
            text="🏠",
            font=("Segoe UI", 18),
            bg=PRIMARY,
            fg=PRIMARY_FOREGROUND,
            width=3,
            height=1,
            cursor="hand2"
        )

        home_icon.pack(
            anchor="w",
            pady=(0, 20)
        )

        home_icon.bind(
            "<Button-1>",
            lambda event: self.handle_navigation(
                self.show_dashboard,
                "Dashboard"
            )
        )

        # ------------------------------------------------------
        # NAVIGATION ITEMS
        # ------------------------------------------------------

        nav_items = [
            (
                "📊",
                "Dashboard",
                self.show_dashboard
            ),
            (
                "📦",
                "Products",
                self.open_products
            ),
            (
                "🛒",
                "Sales",
                self.open_sales_history
            ),
            (
                "📈",
                "Reports",
                self.open_reports
            ),
            (
                "⚙",
                "Settings",
                self.open_settings
            )
        ]

        self.nav_widgets = {}

        for icon, text, command in nav_items:

            is_active = (
                text == self.active_nav
            )

            background = (
                SECONDARY
                if is_active
                else CARD
            )

            foreground = (
                PRIMARY
                if is_active
                else MUTED_FOREGROUND
            )

            # Navigation frame

            item = tk.Frame(
                top,
                bg=background,
                cursor="hand2"
            )

            item.pack(
                fill="x",
                pady=3
            )

            # Navigation label

            label = tk.Label(
                item,
                text=f"  {icon}   {text}",
                font=FONT_NAV,
                bg=background,
                fg=foreground,
                anchor="w",
                padx=10,
                pady=10,
                cursor="hand2"
            )

            label.pack(
                fill="x"
            )

            # Store references

            self.nav_widgets[text] = (
                item,
                label
            )

            # --------------------------------------------------
            # CLICK
            # --------------------------------------------------

            item.bind(
                "<Button-1>",
                lambda event,
                       cmd=command,
                       name=text:
                self.handle_navigation(
                    cmd,
                    name
                )
            )

            label.bind(
                "<Button-1>",
                lambda event,
                       cmd=command,
                       name=text:
                self.handle_navigation(
                    cmd,
                    name
                )
            )

            # --------------------------------------------------
            # HOVER
            # --------------------------------------------------

            item.bind(
                "<Enter>",
                lambda event,
                       name=text:
                self.nav_hover(
                    name,
                    True
                )
            )

            item.bind(
                "<Leave>",
                lambda event,
                       name=text:
                self.nav_hover(
                    name,
                    False
                )
            )

            label.bind(
                "<Enter>",
                lambda event,
                       name=text:
                self.nav_hover(
                    name,
                    True
                )
            )

            label.bind(
                "<Leave>",
                lambda event,
                       name=text:
                self.nav_hover(
                    name,
                    False
                )
            )
        # ------------------------------------------------------
        # LOGOUT
        # ------------------------------------------------------

        logout = tk.Label(
            self.sidebar,
            text="  ↪   Logout",
            font=FONT_NAV,
            bg=CARD,
            fg=MUTED_FOREGROUND,
            anchor="w",
            padx=10,
            pady=10,
            cursor="hand2"
        )

        logout.pack(
            side=tk.BOTTOM,
            fill="x",
            padx=15,
            pady=20
        )

        logout.bind(
            "<Button-1>",
            lambda event: self.logout()
        )

        logout.bind(
            "<Enter>",
            lambda event: logout.config(
                bg=SECONDARY,
                fg=PRIMARY
            )
        )

        logout.bind(
            "<Leave>",
            lambda event: logout.config(
                bg=CARD,
                fg=MUTED_FOREGROUND
            )
        )

    # ==========================================================
    # NAVIGATION HANDLER
    # ==========================================================

    def handle_navigation(
        self,
        command,
        name
    ):

        self.set_active_nav(
            name
        )

        command()

    # ==========================================================
    # SET ACTIVE NAVIGATION
    # ==========================================================

    def set_active_nav(
        self,
        active_name
    ):

        self.active_nav = active_name

        for name, widgets in self.nav_widgets.items():

            item, label = widgets

            if name == active_name:

                item.config(
                    bg=SECONDARY
                )

                label.config(
                    bg=SECONDARY,
                    fg=PRIMARY
                )

            else:

                item.config(
                    bg=CARD
                )

                label.config(
                    bg=CARD,
                    fg=MUTED_FOREGROUND
                )

    # ==========================================================
    # NAVIGATION HOVER
    # ==========================================================

    def nav_hover(
        self,
        name,
        entering
    ):

        if name == self.active_nav:

            return

        item, label = (
            self.nav_widgets[name]
        )

        if entering:

            item.config(
                bg="#F0F1FF"
            )

            label.config(
                bg="#F0F1FF",
                fg=PRIMARY
            )

        else:

            item.config(
                bg=CARD
            )

            label.config(
                bg=CARD,
                fg=MUTED_FOREGROUND
            )

    # ==========================================================
    # SHOW DASHBOARD
    # ==========================================================

    def show_dashboard(self):

        self.set_active_nav(
            "Dashboard"
        )

    # ==========================================================
    # WELCOME / TITLE
    # ==========================================================

    def _build_welcome(self, parent):

        tk.Label(
            parent,
            text=f"Welcome back, {self.username} 👋",
            font=FONT_BODY,
            bg=BACKGROUND,
            fg=MUTED_FOREGROUND
        ).pack(
            anchor="w"
        )

        tk.Label(
            parent,
            text="Inventory & Billing System",
            font=FONT_HEADING,
            bg=BACKGROUND,
            fg=FOREGROUND
        ).pack(
            anchor="w",
            pady=(10, 5)
        )

        tk.Frame(
            parent,
            bg=SECONDARY,
            width=48,
            height=4
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        tk.Label(
            parent,
            text=(
                "Manage your inventory, sales and "
                "business operations efficiently."
            ),
            font=FONT_BODY,
            bg=BACKGROUND,
            fg=MUTED_FOREGROUND
        ).pack(
            anchor="w",
            pady=(0, 20)
        )

    # ==========================================================
    # ACTION CARDS
    # ==========================================================

    def _build_cards(self, parent):

        cards_frame = tk.Frame(
            parent,
            bg=BACKGROUND
        )

        cards_frame.pack(
            fill="x",
            pady=10
        )

        for col in range(3):

            cards_frame.grid_columnconfigure(
                col,
                weight=1,
                uniform="cards"
            )

        cards = [

            (
                "📄",
                "Create Bill",
                "Generate new bills for customers",
                self.open_billing,
                SECONDARY,
                PRIMARY
            ),

            (
                "🧾",
                "Sales History",
                "View and search past sales",
                self.open_sales_history,
                ACCENT,
                TERTIARY
            ),

            (
                "📦",
                "Products",
                "Manage your product inventory",
                self.open_products,
                SECONDARY,
                PRIMARY
            ),

            (
                "👥",
                "Customers",
                "View and manage customer details",
                self.open_customers,
                ACCENT,
                PRIMARY
            ),

            (
                "🚚",
                "Suppliers",
                "Manage supplier information",
                self.open_suppliers,
                SECONDARY,
                TERTIARY
            ),

            (
                "📊",
                "Reports",
                "View business reports & insights",
                self.open_reports,
                ACCENT,
                DESTRUCTIVE
            )
        ]

        for index, (
            icon,
            title_text,
            desc,
            command,
            icon_bg,
            icon_fg
        ) in enumerate(cards):

            row = index // 3
            col = index % 3

            self._create_card(
                cards_frame,
                row,
                col,
                icon,
                title_text,
                desc,
                command,
                icon_bg,
                icon_fg
            )

    # ==========================================================
    # CREATE CARD
    # ==========================================================

    def _create_card(
        self,
        parent,
        row,
        col,
        icon,
        title_text,
        desc,
        command,
        icon_bg,
        icon_fg
    ):

        card = tk.Frame(
            parent,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
            cursor="hand2"
        )

        card.grid(
            row=row,
            column=col,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        inner = tk.Frame(
            card,
            bg=CARD,
            padx=18,
            pady=18
        )

        inner.pack(
            fill="both",
            expand=True
        )

        # Icon

        icon_label = tk.Label(
            inner,
            text=icon,
            font=("Segoe UI", 20),
            bg=icon_bg,
            fg=icon_fg,
            width=3,
            height=1,
            cursor="hand2"
        )

        icon_label.pack(
            side=tk.LEFT,
            padx=(0, 15)
        )

        # Text

        text_frame = tk.Frame(
            inner,
            bg=CARD
        )

        text_frame.pack(
            side=tk.LEFT,
            fill="both",
            expand=True
        )

        title_label = tk.Label(
            text_frame,
            text=title_text,
            font=FONT_SUBHEADING,
            bg=CARD,
            fg=FOREGROUND,
            anchor="w",
            cursor="hand2"
        )

        title_label.pack(
            fill="x"
        )

        desc_label = tk.Label(
            text_frame,
            text=desc,
            font=FONT_SMALL,
            bg=CARD,
            fg=MUTED_FOREGROUND,
            anchor="w",
            wraplength=220,
            justify="left",
            cursor="hand2"
        )

        desc_label.pack(
            fill="x",
            pady=(4, 0)
        )

        # Arrow

        arrow = tk.Label(
            inner,
            text="›",
            font=("Segoe UI", 16, "bold"),
            bg=CARD,
            fg=MUTED_FOREGROUND,
            cursor="hand2"
        )

        arrow.pack(
            side=tk.RIGHT
        )

        # ------------------------------------------------------
        # CARD CLICK
        # ------------------------------------------------------

        clickable_widgets = [
            card,
            inner,
            icon_label,
            text_frame,
            title_label,
            desc_label,
            arrow
        ]

        def on_click(event):

            command()

        def on_enter(event):

            card.config(
                highlightbackground=PRIMARY
            )

        def on_leave(event):

            card.config(
                highlightbackground=BORDER
            )

        for widget in clickable_widgets:

            widget.bind(
                "<Button-1>",
                on_click
            )

            widget.bind(
                "<Enter>",
                on_enter
            )

            widget.bind(
                "<Leave>",
                on_leave
            )

    # ==========================================================
    # STATS
    # ==========================================================

    def _build_stats(self, parent):

        stats_card = tk.Frame(
            parent,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        stats_card.pack(
            fill="x",
            pady=15
        )

        stats_inner = tk.Frame(
            stats_card,
            bg=CARD,
            padx=20,
            pady=20
        )

        stats_inner.pack(
            fill="x"
        )

        for col in range(4):

            stats_inner.grid_columnconfigure(
                col,
                weight=1,
                uniform="stats"
            )

        stats = [

            (
                "🛍",
                "Total Products",
                "128",
                "In inventory",
                SECONDARY,
                PRIMARY,
                PRIMARY
            ),

            (
                "🛒",
                "Today's Sales",
                "₹18,540",
                "6 bills",
                ACCENT,
                TERTIARY,
                TERTIARY
            ),

            (
                "👥",
                "Total Customers",
                "356",
                "Registered",
                SECONDARY,
                PRIMARY,
                PRIMARY
            ),

            (
                "📦",
                "Low Stock Items",
                "12",
                "Reorder soon",
                ACCENT,
                DESTRUCTIVE,
                DESTRUCTIVE
            )
        ]

        for col, (
            icon,
            label,
            value,
            note,
            icon_bg,
            icon_fg,
            note_fg
        ) in enumerate(stats):

            stat_frame = tk.Frame(
                stats_inner,
                bg=CARD
            )

            stat_frame.grid(
                row=0,
                column=col,
                sticky="w",
                padx=10
            )

            tk.Label(
                stat_frame,
                text=icon,
                font=("Segoe UI", 16),
                bg=icon_bg,
                fg=icon_fg,
                width=3,
                height=1
            ).pack(
                side=tk.LEFT,
                padx=(0, 10)
            )

            text_col = tk.Frame(
                stat_frame,
                bg=CARD
            )

            text_col.pack(
                side=tk.LEFT
            )

            tk.Label(
                text_col,
                text=label,
                font=FONT_SMALL,
                bg=CARD,
                fg=MUTED_FOREGROUND,
                anchor="w"
            ).pack(
                fill="x"
            )

            tk.Label(
                text_col,
                text=value,
                font=FONT_STAT_VALUE,
                bg=CARD,
                fg=FOREGROUND,
                anchor="w"
            ).pack(
                fill="x"
            )

            tk.Label(
                text_col,
                text=note,
                font=FONT_SMALL,
                bg=CARD,
                fg=note_fg,
                anchor="w"
            ).pack(
                fill="x"
            )

    # ==========================================================
    # FOOTER
    # ==========================================================

    def _build_footer(self, parent):

        tk.Label(
            parent,
            text="© 2026 Inventory & Billing System. All rights reserved.",
            font=FONT_SMALL,
            bg=BACKGROUND,
            fg=MUTED_FOREGROUND
        ).pack(
            pady=15
        )

    # ==========================================================
    # OPEN BILLING
    # ==========================================================

    def open_billing(self):

        window = tk.Toplevel(
            self.root
        )

        BillingWindow(window)

    # ==========================================================
    # OPEN SALES HISTORY
    # ==========================================================

    def open_sales_history(self):

        window = tk.Toplevel(
            self.root
        )

        SalesHistoryWindow(window)

    # ==========================================================
    # OPEN PRODUCTS
    # ==========================================================

    def open_products(self):

        window = tk.Toplevel(
            self.root
        )

        ProductWindow(window)

    # ==========================================================
    # OPEN CUSTOMERS
    # ==========================================================

    def open_customers(self):

        window = tk.Toplevel(
            self.root
        )

        CustomerWindow(window)

    # ==========================================================
    # OPEN SUPPLIERS
    # ==========================================================

    def open_suppliers(self):

        window = tk.Toplevel(
            self.root
        )

        SupplierWindow(window)

    # ==========================================================
    # REPORTS
    # ==========================================================

    def open_reports(self):

        messagebox.showinfo(
            "Reports",
            "Reports module will be connected here."
        )

    # ==========================================================
    # SETTINGS
    # ==========================================================

    def open_settings(self):

        messagebox.showinfo(
            "Settings",
            "Settings module will be connected here."
        )

    # ==========================================================
    # LOGOUT
    # ==========================================================

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if not answer:

            return

        # Destroy dashboard

        self.root.destroy()

        # Reopen login

        login_root = tk.Tk()

        from gui.login import LoginWindow

        LoginWindow(
            login_root
        )

        login_root.mainloop()


# ==============================================================
# TEST
# ==============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = Dashboard(
        root,
        username="admin",
        role="admin"
    )

    root.mainloop()