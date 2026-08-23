import tkinter as tk
from tkinter import ttk, messagebox

from database.db_connection import get_connection


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
MUTED_FOREGROUND = "#6B7280"
ACCENT = "#CBCEFA"
CARD = "#FFFFFF"
BORDER = "#E1E3FC"
DESTRUCTIVE = "#DC2626"

FONT_HEADING = ("Segoe UI", 20, "bold")
FONT_SUBHEADING = ("Segoe UI", 11, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_LABEL = ("Segoe UI", 10, "bold")


class CustomerWindow:

    def __init__(self, root):

        self.root = root
        self.root.title("Customer Management")
        self.root.geometry("1200x850")
        self.root.minsize(950, 600)
        self.root.configure(bg=BACKGROUND)

        self.selected_customer_id = None

        self._setup_styles()
        self.create_widgets()
        self.load_customers()

    # ==========================================================
    # STYLES (ttk theming to match the HTML design palette)
    # ==========================================================

    def _setup_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background=CARD,
            fieldbackground=CARD,
            foreground=FOREGROUND,
            rowheight=34,
            bordercolor=BORDER,
            borderwidth=0,
            font=FONT_BODY
        )

        style.configure(
            "Treeview.Heading",
            background=SECONDARY,
            foreground=SECONDARY_FOREGROUND,
            font=FONT_SUBHEADING,
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[("selected", SECONDARY)],
            foreground=[("selected", FOREGROUND)]
        )

    # ==========================================================
    # SMALL WIDGET HELPERS
    # ==========================================================

    def _card(self, parent):

        return tk.Frame(
            parent,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

    def _primary_button(self, parent, text, command):

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=PRIMARY,
            fg=PRIMARY_FOREGROUND,
            activebackground=PRIMARY,
            activeforeground=PRIMARY_FOREGROUND,
            font=FONT_LABEL,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=14,
            pady=10
        )

    def _outline_button(self, parent, text, command, fg=PRIMARY):

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=CARD,
            fg=fg,
            activebackground=CARD,
            activeforeground=fg,
            font=FONT_LABEL,
            relief="flat",
            bd=1,
            highlightbackground=fg,
            highlightthickness=1,
            cursor="hand2",
            padx=14,
            pady=10
        )

    def _labeled_entry(self, parent, icon, label_text, width=25):

        wrap = tk.Frame(parent, bg=CARD)

        icon_label = tk.Label(
            wrap,
            text=icon,
            font=("Segoe UI", 14),
            bg=SECONDARY,
            fg=PRIMARY,
            width=3,
            height=1
        )

        icon_label.pack(side=tk.LEFT, anchor="n", padx=(0, 12))

        text_col = tk.Frame(wrap, bg=CARD)
        text_col.pack(side=tk.LEFT, fill="x", expand=True)

        tk.Label(
            text_col,
            text=label_text,
            font=FONT_LABEL,
            bg=CARD,
            fg=FOREGROUND
        ).pack(anchor="w", pady=(0, 6))

        entry = tk.Entry(
            text_col,
            width=width,
            font=FONT_BODY,
            bg=BACKGROUND,
            fg=FOREGROUND,
            relief="flat",
            highlightbackground=BORDER,
            highlightthickness=1,
            insertbackground=FOREGROUND
        )

        entry.pack(fill="x", ipady=6)

        return wrap, entry

    # ==========================================================
    # GUI
    # ==========================================================

    def create_widgets(self):

        self._build_header()

        body = tk.Frame(self.root, bg=BACKGROUND)
        body.pack(fill="both", expand=True)

        # ------------------------------------------------------
        # Scrollable content area so nothing is ever pushed off
        # screen and unreachable, regardless of window size.
        # ------------------------------------------------------

        canvas = tk.Canvas(body, bg=BACKGROUND, highlightthickness=0)
        scrollbar = tk.Scrollbar(body, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        main = tk.Frame(canvas, bg=BACKGROUND)
        main_window = canvas.create_window((0, 0), window=main, anchor="nw")

        def on_main_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_canvas_configure(event):
            canvas.itemconfig(main_window, width=event.width)

        main.bind("<Configure>", on_main_configure)
        canvas.bind("<Configure>", on_canvas_configure)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        content = tk.Frame(main, bg=BACKGROUND)
        content.pack(fill="both", expand=True, padx=30, pady=25)

        self._build_title_row(content)
        self._build_form_section(content)
        self._build_search_section(content)
        self._build_table_section(content)

        self.customer_table.bind(
            "<ButtonRelease-1>",
            self.select_customer
        )

    # ----------------------------------------------------------
    # HEADER
    # ----------------------------------------------------------

    def _build_header(self):

        header = tk.Frame(
            self.root,
            bg=CARD,
            height=60,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        header.pack(fill="x", side=tk.TOP)
        header.pack_propagate(False)

        left = tk.Frame(header, bg=CARD)
        left.pack(side=tk.LEFT, padx=20)

        tk.Label(
            left,
            text="\U0001F4E6",
            font=("Segoe UI", 13),
            bg=SECONDARY,
            fg=PRIMARY,
            width=3
        ).pack(side=tk.LEFT)

        tk.Label(
            left,
            text="Inventory & Billing System",
            font=FONT_SUBHEADING,
            bg=CARD,
            fg=FOREGROUND
        ).pack(side=tk.LEFT, padx=12)

        right = tk.Frame(header, bg=CARD)
        right.pack(side=tk.RIGHT, padx=20)

        tk.Label(
            right,
            text="AR",
            font=("Segoe UI", 11, "bold"),
            bg=SECONDARY,
            fg=SECONDARY_FOREGROUND,
            width=3,
            height=1
        ).pack(side=tk.RIGHT, padx=(10, 0))

        tk.Label(
            right,
            text="\U0001F514",
            font=("Segoe UI", 12),
            bg=CARD,
            fg=MUTED_FOREGROUND,
            width=3,
            relief="solid",
            bd=1
        ).pack(side=tk.RIGHT, padx=10)

    # ----------------------------------------------------------
    # TITLE ROW
    # ----------------------------------------------------------

    def _build_title_row(self, parent):

        row = tk.Frame(parent, bg=BACKGROUND)
        row.pack(fill="x")

        back_btn = tk.Label(
            row,
            text="\u2190",
            font=("Segoe UI", 16, "bold"),
            bg=CARD,
            fg=PRIMARY,
            width=3,
            height=1,
            highlightbackground=BORDER,
            highlightthickness=1,
            cursor="hand2"
        )

        back_btn.pack(side=tk.LEFT, padx=(0, 15))

        text_col = tk.Frame(row, bg=BACKGROUND)
        text_col.pack(side=tk.LEFT)

        tk.Label(
            text_col,
            text="Customer Management",
            font=FONT_HEADING,
            bg=BACKGROUND,
            fg=FOREGROUND
        ).pack(anchor="w")

        tk.Label(
            text_col,
            text="Manage your customers and their details",
            font=FONT_BODY,
            bg=BACKGROUND,
            fg=MUTED_FOREGROUND
        ).pack(anchor="w")

    # ----------------------------------------------------------
    # CUSTOMER FORM
    # ----------------------------------------------------------

    def _build_form_section(self, parent):

        section = self._card(parent)
        section.pack(fill="x", pady=(20, 0))

        inner = tk.Frame(section, bg=CARD, padx=25, pady=25)
        inner.pack(fill="x")

        grid = tk.Frame(inner, bg=CARD)
        grid.pack(fill="x")

        grid.grid_columnconfigure(0, weight=1, uniform="form")
        grid.grid_columnconfigure(1, weight=1, uniform="form")

        name_wrap, self.name_entry = self._labeled_entry(
            grid, "\U0001F464", "Name"
        )
        name_wrap.grid(row=0, column=0, sticky="ew", padx=(0, 20), pady=10)

        phone_wrap, self.phone_entry = self._labeled_entry(
            grid, "\U0001F4DE", "Phone"
        )
        phone_wrap.grid(row=0, column=1, sticky="ew", padx=(20, 0), pady=10)

        email_wrap, self.email_entry = self._labeled_entry(
            grid, "\U0001F4E7", "Email"
        )
        email_wrap.grid(row=1, column=0, sticky="ew", padx=(0, 20), pady=10)

        address_wrap, self.address_entry = self._labeled_entry(
            grid, "\U0001F4CD", "Address"
        )
        address_wrap.grid(row=1, column=1, sticky="ew", padx=(20, 0), pady=10)

        # ------------------------------------------------------
        # ACTION BUTTONS
        # ------------------------------------------------------

        button_row = tk.Frame(inner, bg=CARD)
        button_row.pack(fill="x", pady=(20, 0))

        button_row.grid_columnconfigure(0, weight=1, uniform="actions")
        button_row.grid_columnconfigure(1, weight=1, uniform="actions")
        button_row.grid_columnconfigure(2, weight=1, uniform="actions")
        button_row.grid_columnconfigure(3, weight=1, uniform="actions")

        self._primary_button(
            button_row,
            "\u2795  Add Customer",
            self.add_customer
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self._outline_button(
            button_row,
            "\u270F  Update",
            self.update_customer
        ).grid(row=0, column=1, sticky="ew", padx=8)

        self._outline_button(
            button_row,
            "\U0001F5D1  Delete",
            self.delete_customer,
            fg=DESTRUCTIVE
        ).grid(row=0, column=2, sticky="ew", padx=8)

        self._outline_button(
            button_row,
            "\U0001F504  Clear",
            self.clear_form,
            fg=MUTED_FOREGROUND
        ).grid(row=0, column=3, sticky="ew", padx=(8, 0))

    # ----------------------------------------------------------
    # SEARCH
    # ----------------------------------------------------------

    def _build_search_section(self, parent):

        section = self._card(parent)
        section.pack(fill="x", pady=(20, 0))

        inner = tk.Frame(section, bg=CARD, padx=20, pady=18)
        inner.pack(fill="x")

        search_wrap = tk.Frame(
            inner,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        search_wrap.pack(side=tk.LEFT, fill="x", expand=True)

        tk.Label(
            search_wrap,
            text="\U0001F50D",
            font=("Segoe UI", 11),
            bg=CARD,
            fg=MUTED_FOREGROUND,
            padx=10
        ).pack(side=tk.LEFT)

        self.search_entry = tk.Entry(
            search_wrap,
            font=FONT_BODY,
            bg=CARD,
            fg=FOREGROUND,
            relief="flat",
            insertbackground=FOREGROUND
        )

        self.search_entry.pack(
            side=tk.LEFT,
            fill="x",
            expand=True,
            ipady=8,
            padx=(0, 10)
        )

        self.search_entry.bind(
            "<Return>",
            lambda event: self.search_customers()
        )

        button_row = tk.Frame(inner, bg=CARD)
        button_row.pack(side=tk.LEFT, padx=(15, 0))

        self._primary_button(
            button_row,
            "\U0001F50D  Search",
            self.search_customers
        ).pack(side=tk.LEFT, padx=(0, 10))

        self._outline_button(
            button_row,
            "\U0001F501  Show All",
            self.load_customers
        ).pack(side=tk.LEFT)

    # ----------------------------------------------------------
    # CUSTOMER TABLE
    # ----------------------------------------------------------

    def _build_table_section(self, parent):

        section = self._card(parent)
        section.pack(fill="both", expand=True, pady=(20, 0))

        table_frame = tk.Frame(section, bg=CARD, padx=10, pady=10)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = (
            "id",
            "name",
            "phone",
            "email",
            "address"
        )

        self.customer_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=14
        )

        self.customer_table.heading(
            "id",
            text="ID"
        )

        self.customer_table.heading(
            "name",
            text="Name"
        )

        self.customer_table.heading(
            "phone",
            text="Phone"
        )

        self.customer_table.heading(
            "email",
            text="Email"
        )

        self.customer_table.heading(
            "address",
            text="Address"
        )

        self.customer_table.column(
            "id",
            width=60,
            anchor="center"
        )

        self.customer_table.column(
            "name",
            width=180
        )

        self.customer_table.column(
            "phone",
            width=140
        )

        self.customer_table.column(
            "email",
            width=220
        )

        self.customer_table.column(
            "address",
            width=220
        )

        scrollbar_y = tk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.customer_table.yview
        )

        self.customer_table.configure(
            yscrollcommand=scrollbar_y.set
        )

        self.customer_table.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        scrollbar_y.pack(side=tk.LEFT, fill="y")

        self.customer_count_label = tk.Label(
            parent,
            text="Showing 0 customers",
            font=FONT_SMALL,
            bg=BACKGROUND,
            fg=MUTED_FOREGROUND
        )

        self.customer_count_label.pack(anchor="w", pady=(10, 0))

    # ==========================================================
    # LOAD CUSTOMERS
    # ==========================================================

    def load_customers(self):

        self.search_entry.delete(
            0,
            tk.END
        )

        self.fetch_customers()

    # ==========================================================
    # FETCH CUSTOMERS
    # ==========================================================

    def fetch_customers(
        self,
        search_text=None
    ):

        for row in self.customer_table.get_children():
            self.customer_table.delete(row)

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            if search_text:

                cursor.execute("""
                    SELECT
                        customer_id,
                        name,
                        phone,
                        email,
                        address
                    FROM customers
                    WHERE name LIKE ?
                    OR phone LIKE ?
                    OR email LIKE ?
                    ORDER BY customer_id DESC
                """, (
                    f"%{search_text}%",
                    f"%{search_text}%",
                    f"%{search_text}%"
                ))

            else:

                cursor.execute("""
                    SELECT
                        customer_id,
                        name,
                        phone,
                        email,
                        address
                    FROM customers
                    ORDER BY customer_id DESC
                """)

            customers = cursor.fetchall()

            for customer in customers:

                self.customer_table.insert(
                    "",
                    tk.END,
                    values=(
                        customer[0],
                        customer[1],
                        customer[2],
                        customer[3],
                        customer[4]
                    )
                )

            # Purely visual count refresh -- does not affect the
            # table data or any of the search/fetch logic above.

            if hasattr(self, "customer_count_label"):

                self.customer_count_label.config(
                    text=f"Showing {len(customers)} customer"
                    f"{'s' if len(customers) != 1 else ''}"
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not load customers.\n\n{e}"
            )

        finally:

            if connection:
                connection.close()

    # ==========================================================
    # SEARCH
    # ==========================================================

    def search_customers(self):

        search_text = (
            self.search_entry.get().strip()
        )

        if not search_text:

            self.load_customers()
            return

        self.fetch_customers(
            search_text
        )

    # ==========================================================
    # SELECT CUSTOMER
    # ==========================================================

    def select_customer(self, event):

        selected = self.customer_table.selection()

        if not selected:
            return

        values = self.customer_table.item(
            selected[0],
            "values"
        )

        self.selected_customer_id = int(
            values[0]
        )

        self.name_entry.delete(
            0,
            tk.END
        )
        self.name_entry.insert(
            0,
            values[1]
        )

        self.phone_entry.delete(
            0,
            tk.END
        )
        self.phone_entry.insert(
            0,
            values[2]
        )

        self.email_entry.delete(
            0,
            tk.END
        )
        self.email_entry.insert(
            0,
            values[3]
        )

        self.address_entry.delete(
            0,
            tk.END
        )
        self.address_entry.insert(
            0,
            values[4]
        )

    # ==========================================================
    # VALIDATE FORM
    # ==========================================================

    def validate_form(self):

        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if not name:

            messagebox.showwarning(
                "Invalid Customer",
                "Customer name is required."
            )
            return None

        if not phone:

            messagebox.showwarning(
                "Invalid Customer",
                "Phone number is required."
            )
            return None

        if not phone.isdigit() or len(phone) != 10:

            messagebox.showerror(
                "Invalid Phone",
                "Phone number must contain exactly 10 digits."
            )
            return None

        if not email:

            messagebox.showwarning(
                "Invalid Customer",
                "Email is required because it is used "
                "for sending invoices."
            )
            return None

        # Basic email validation
        if "@" not in email or "." not in email.split("@")[-1]:

            messagebox.showerror(
                "Invalid Email",
                "Please enter a valid email address."
            )
            return None

        if not address:

            messagebox.showwarning(
                "Invalid Customer",
                "Address is required."
            )
            return None

        return (
            name,
            phone,
            email,
            address
        )

    # ==========================================================
    # ADD CUSTOMER
    # ==========================================================

    def add_customer(self):

        data = self.validate_form()

        if data is None:
            return

        name, phone, email, address = data

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO customers
                (name, phone, email, address)
                VALUES (?, ?, ?, ?)
            """, (
                name,
                phone,
                email,
                address
            ))

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Customer added successfully."
            )

            self.clear_form()
            self.fetch_customers()

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Could not add customer.\n\n{e}"
            )

        finally:

            if connection:
                connection.close()

    # ==========================================================
    # UPDATE CUSTOMER
    # ==========================================================

    def update_customer(self):

        if self.selected_customer_id is None:

            messagebox.showwarning(
                "No Selection",
                "Please select a customer first."
            )
            return

        data = self.validate_form()

        if data is None:
            return

        name, phone, email, address = data

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE customers
                SET
                    name = ?,
                    phone = ?,
                    email = ?,
                    address = ?
                WHERE customer_id = ?
            """, (
                name,
                phone,
                email,
                address,
                self.selected_customer_id
            ))

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Customer updated successfully."
            )

            self.clear_form()
            self.fetch_customers()

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Could not update customer.\n\n{e}"
            )

        finally:

            if connection:
                connection.close()

    # ==========================================================
    # DELETE CUSTOMER
    # ==========================================================

    def delete_customer(self):

        if self.selected_customer_id is None:

            messagebox.showwarning(
                "No Selection",
                "Please select a customer first."
            )
            return

        confirmation = messagebox.askyesno(
            "Delete Customer",
            "Are you sure you want to delete this customer?"
        )

        if not confirmation:
            return

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM customers
                WHERE customer_id = ?
            """, (
                self.selected_customer_id,
            ))

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Customer deleted successfully."
            )

            self.clear_form()
            self.fetch_customers()

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Could not delete customer.\n\n"
                f"The customer may already have sales.\n\n{e}"
            )

        finally:

            if connection:
                connection.close()

    # ==========================================================
    # CLEAR FORM
    # ==========================================================

    def clear_form(self):

        self.selected_customer_id = None

        self.name_entry.delete(
            0,
            tk.END
        )

        self.phone_entry.delete(
            0,
            tk.END
        )

        self.email_entry.delete(
            0,
            tk.END
        )

        self.address_entry.delete(
            0,
            tk.END
        )

        selected = self.customer_table.selection()

        if selected:

            self.customer_table.selection_remove(
                selected
            )


# ==============================================================
# TEST
# ==============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CustomerWindow(root)

    root.mainloop()