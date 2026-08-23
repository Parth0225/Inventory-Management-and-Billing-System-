import tkinter as tk
from tkinter import ttk, messagebox

from services.invoice_service import InvoiceService
from services.email_service import EmailService

from database.db_connection import get_connection
from models.sale import Sale
from models.sale_item import SaleItem
from services.billing_service import BillingService


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

FONT_HEADING = ("Segoe UI", 18, "bold")
FONT_SUBHEADING = ("Segoe UI", 11, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_LABEL = ("Segoe UI", 10, "bold")
FONT_TOTAL = ("Segoe UI", 20, "bold")


class BillingWindow:

    def __init__(self, root):

        self.root = root
        self.root.title("Inventory & Billing System")
        self.root.geometry("1150x900")
        self.root.minsize(900, 600)
        self.root.configure(bg=BACKGROUND)

        self.billing_service = BillingService()
        self.invoice_service = InvoiceService()
        self.email_service = EmailService()

        # Stores products currently added to the bill
        self.cart = []

        self._setup_styles()
        self.create_widgets()

        self.load_customers()
        self.load_products()

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
            "TCombobox",
            fieldbackground=CARD,
            background=CARD,
            foreground=FOREGROUND,
            arrowcolor=PRIMARY,
            bordercolor=BORDER,
            lightcolor=CARD,
            darkcolor=CARD,
            padding=6
        )

        style.map(
            "TCombobox",
            fieldbackground=[("readonly", CARD)],
            foreground=[("readonly", FOREGROUND)]
        )

        style.configure(
            "Treeview",
            background=CARD,
            fieldbackground=CARD,
            foreground=FOREGROUND,
            rowheight=30,
            bordercolor=BORDER,
            borderwidth=1,
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

    def _card(self, parent, **kwargs):

        frame = tk.Frame(
            parent,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        return frame

    def _primary_button(self, parent, text, command, **kwargs):

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
            pady=8,
            **kwargs
        )

    def _outline_button(self, parent, text, command, fg=PRIMARY, **kwargs):

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
            pady=8,
            **kwargs
        )

    # ==========================================================
    # CREATE GUI
    # ==========================================================

    def create_widgets(self):

        self._build_header()

        # ------------------------------------------------------
        # Scrollable content area.
        #
        # The window has a fixed default size, but the stacked
        # cards (input row, cart, discount/summary, generate
        # button, footer) can add up to more vertical space than
        # that on smaller screens. Without scrolling, anything
        # past the bottom of the window is simply invisible and
        # unreachable (this is what caused "Generate Bill and
        # everything below it disappeared"). A canvas + scrollbar
        # guarantees every widget stays reachable no matter the
        # window size, while the visual layout is unchanged.
        # ------------------------------------------------------

        outer = tk.Frame(self.root, bg=BACKGROUND)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            outer,
            bg=BACKGROUND,
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            outer,
            orient="vertical",
            command=canvas.yview
        )

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        main = tk.Frame(canvas, bg=BACKGROUND)

        main_window = canvas.create_window(
            (0, 0),
            window=main,
            anchor="nw"
        )

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
        content.pack(fill="both", expand=True, padx=30, pady=20)

        self._build_title(content)
        self._build_input_section(content)
        self._build_cart_section(content)

        bottom_row = tk.Frame(content, bg=BACKGROUND)
        bottom_row.pack(fill="x", pady=(20, 0))
        bottom_row.grid_columnconfigure(0, weight=1, uniform="bottom")
        bottom_row.grid_columnconfigure(1, weight=1, uniform="bottom")

        left_col = tk.Frame(bottom_row, bg=BACKGROUND)
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        right_col = tk.Frame(bottom_row, bg=BACKGROUND)
        right_col.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self._build_discount_payment_section(left_col)
        self._build_summary_section(right_col)

        self._build_generate_button(content)
        self._build_footer(content)

    # ----------------------------------------------------------
    # HEADER
    # ----------------------------------------------------------

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

        left = tk.Frame(header, bg=CARD)
        left.pack(side=tk.LEFT, padx=20)

        tk.Label(
            left,
            text="\U0001F3EA",
            font=("Segoe UI", 14),
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

    # ----------------------------------------------------------
    # TITLE ROW
    # ----------------------------------------------------------

    def _build_title(self, parent):

        title_row = tk.Frame(parent, bg=BACKGROUND)
        title_row.pack(fill="x")

        left = tk.Frame(title_row, bg=BACKGROUND)
        left.pack(side=tk.LEFT)

        back_btn = tk.Label(
            left,
            text="\u2190",
            font=("Segoe UI", 14, "bold"),
            bg=CARD,
            fg=PRIMARY,
            width=3,
            height=1,
            highlightbackground=BORDER,
            highlightthickness=1,
            cursor="hand2"
        )

        back_btn.pack(side=tk.LEFT, padx=(0, 12))

        text_col = tk.Frame(left, bg=BACKGROUND)
        text_col.pack(side=tk.LEFT)

        tk.Label(
            text_col,
            text="Create Bill",
            font=FONT_HEADING,
            bg=BACKGROUND,
            fg=FOREGROUND
        ).pack(anchor="w")

        tk.Label(
            text_col,
            text="Add products to the cart and generate an invoice.",
            font=FONT_BODY,
            bg=BACKGROUND,
            fg=MUTED_FOREGROUND
        ).pack(anchor="w")

        # "New Bill" re-uses the existing reset_after_bill logic,
        # so no new behavior is introduced -- it just gives the
        # existing "clear everything" functionality a second
        # entry point, matching the button shown in the design.

        new_bill_btn = self._outline_button(
            title_row,
            "\u2795  New Bill",
            self.reset_after_bill
        )

        new_bill_btn.pack(side=tk.RIGHT)

    # ----------------------------------------------------------
    # CUSTOMER / PRODUCT / QUANTITY / ADD PRODUCT
    # ----------------------------------------------------------

    def _build_input_section(self, parent):

        section = self._card(parent)
        section.pack(fill="x", pady=(20, 0))

        inner = tk.Frame(section, bg=CARD, padx=20, pady=20)
        inner.pack(fill="x")

        for col in range(4):
            inner.grid_columnconfigure(col, weight=1, uniform="inputs")

        # Customer
        tk.Label(
            inner,
            text="\U0001F464  Customer",
            font=FONT_LABEL,
            bg=CARD,
            fg=FOREGROUND
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.customer_combo = ttk.Combobox(
            inner,
            width=35,
            state="readonly"
        )

        self.customer_combo.grid(row=1, column=0, sticky="ew", padx=(0, 10))

        # Product
        tk.Label(
            inner,
            text="\U0001F4E6  Product",
            font=FONT_LABEL,
            bg=CARD,
            fg=FOREGROUND
        ).grid(row=0, column=1, sticky="w", pady=(0, 6))

        self.product_combo = ttk.Combobox(
            inner,
            width=30,
            state="readonly"
        )

        self.product_combo.grid(row=1, column=1, sticky="ew", padx=(0, 10))

        # Quantity
        tk.Label(
            inner,
            text="\U0001F6D2  Quantity",
            font=FONT_LABEL,
            bg=CARD,
            fg=FOREGROUND
        ).grid(row=0, column=2, sticky="w", pady=(0, 6))

        self.quantity_entry = tk.Entry(
            inner,
            width=10,
            font=FONT_BODY,
            bg=CARD,
            fg=FOREGROUND,
            highlightbackground=BORDER,
            highlightthickness=1,
            relief="flat"
        )

        self.quantity_entry.grid(row=1, column=2, sticky="ew", padx=(0, 10), ipady=4)

        # Add product button
        self._primary_button(
            inner,
            "\u2795  Add Product",
            self.add_product
        ).grid(row=1, column=3, sticky="ew")

    # ----------------------------------------------------------
    # CART TABLE + REMOVE / CLEAR
    # ----------------------------------------------------------

    def _build_cart_section(self, parent):

        section = self._card(parent)
        section.pack(fill="both", expand=True, pady=(20, 0))

        cart_frame = tk.Frame(section, bg=CARD, padx=15, pady=15)
        cart_frame.pack(fill="both", expand=True)

        columns = (
            "product_id",
            "product",
            "quantity",
            "price",
            "total"
        )

        table_wrap = tk.Frame(cart_frame, bg=CARD)
        table_wrap.pack(side=tk.LEFT, fill="both", expand=True)

        # Empty-state placeholder shown over the table area when the
        # cart has no items yet, purely visual -- refresh_cart() below
        # toggles it, it never touches self.cart or the table data.

        self.cart_empty_state = tk.Frame(table_wrap, bg=CARD)

        tk.Label(
            self.cart_empty_state,
            text="\U0001F6D2",
            font=("Segoe UI", 34),
            bg=SECONDARY,
            fg=PRIMARY,
            width=3,
            height=1
        ).pack(pady=(40, 15))

        tk.Label(
            self.cart_empty_state,
            text="Your cart is empty",
            font=FONT_SUBHEADING,
            bg=CARD,
            fg=FOREGROUND
        ).pack()

        tk.Label(
            self.cart_empty_state,
            text="Add products to get started.",
            font=FONT_BODY,
            bg=CARD,
            fg=MUTED_FOREGROUND
        ).pack(pady=(4, 0))

        self.cart_empty_state.pack(fill="both", expand=True)

        self.cart_table = ttk.Treeview(
            table_wrap,
            columns=columns,
            show="headings",
            height=10
        )

        self.cart_table.heading("product_id", text="ID")
        self.cart_table.heading("product", text="Product")
        self.cart_table.heading("quantity", text="Quantity")
        self.cart_table.heading("price", text="Price")
        self.cart_table.heading("total", text="Total")

        self.cart_table.column("product_id", width=70, anchor="center")
        self.cart_table.column("product", width=280)
        self.cart_table.column("quantity", width=100, anchor="center")
        self.cart_table.column("price", width=120, anchor="e")
        self.cart_table.column("total", width=120, anchor="e")

        # Table starts unpacked; the empty-state placeholder is shown
        # instead until refresh_cart() detects items and swaps them.

        cart_button_frame = tk.Frame(cart_frame, bg=CARD)

        cart_button_frame.pack(
            side=tk.LEFT,
            fill="y",
            padx=(15, 0)
        )

        self._outline_button(
            cart_button_frame,
            "\U0001F5D1  Remove Selected",
            self.remove_product,
            fg=DESTRUCTIVE
        ).pack(fill="x", pady=(0, 10))

        self._outline_button(
            cart_button_frame,
            "\U0001F6D2  Clear Cart",
            self.clear_cart,
            fg=PRIMARY
        ).pack(fill="x")

    # ----------------------------------------------------------
    # DISCOUNT + PAYMENT
    # ----------------------------------------------------------

    def _build_discount_payment_section(self, parent):

        section = self._card(parent)
        section.pack(fill="x", pady=(20, 0))

        calculation_frame = tk.Frame(section, bg=CARD, padx=20, pady=20)
        calculation_frame.pack(fill="x")

        tk.Label(
            calculation_frame,
            text="\U0001F4B0  Discount:",
            font=FONT_LABEL,
            bg=CARD,
            fg=FOREGROUND
        ).grid(row=0, column=0, padx=5)

        self.discount_entry = tk.Entry(
            calculation_frame,
            width=10,
            font=FONT_BODY,
            bg=CARD,
            fg=FOREGROUND,
            highlightbackground=BORDER,
            highlightthickness=1,
            relief="flat"
        )

        self.discount_entry.insert(0, "0")

        self.discount_entry.grid(row=0, column=1, padx=5, ipady=4)

        self._primary_button(
            calculation_frame,
            "Calculate",
            self.update_total
        ).grid(row=0, column=2, padx=10)

        tk.Label(
            calculation_frame,
            text="\U0001F4B3  Payment:",
            font=FONT_LABEL,
            bg=CARD,
            fg=FOREGROUND
        ).grid(row=0, column=3, padx=(30, 5))

        self.payment_combo = ttk.Combobox(
            calculation_frame,
            values=["Cash", "UPI", "Card"],
            state="readonly",
            width=12
        )

        self.payment_combo.current(0)

        self.payment_combo.grid(row=0, column=4, padx=5)

    # ----------------------------------------------------------
    # BILL SUMMARY
    # ----------------------------------------------------------

    def _build_summary_section(self, parent):

        section = self._card(parent)
        section.pack(fill="x", pady=(20, 0))

        inner = tk.Frame(section, bg=CARD, padx=25, pady=20)
        inner.pack(fill="x")

        self.subtotal_label = tk.Label(
            inner,
            text="Subtotal: \u20B90.00",
            font=FONT_BODY,
            bg=CARD,
            fg=FOREGROUND,
            anchor="w"
        )

        self.subtotal_label.pack(fill="x", pady=2)

        self.discount_label = tk.Label(
            inner,
            text="Discount: \u20B90.00",
            font=FONT_BODY,
            bg=CARD,
            fg=TERTIARY,
            anchor="w"
        )

        self.discount_label.pack(fill="x", pady=2)

        self.gst_label = tk.Label(
            inner,
            text="GST (18%): \u20B90.00",
            font=FONT_BODY,
            bg=CARD,
            fg=FOREGROUND,
            anchor="w"
        )

        self.gst_label.pack(fill="x", pady=2)

        divider = tk.Frame(inner, bg=BORDER, height=1)
        divider.pack(fill="x", pady=10)

        total_row = tk.Frame(inner, bg=CARD)
        total_row.pack(fill="x")

        tk.Label(
            total_row,
            text="Total Amount",
            font=FONT_SUBHEADING,
            bg=CARD,
            fg=FOREGROUND
        ).pack(side=tk.LEFT)

        self.total_label = tk.Label(
            total_row,
            text="Total: \u20B90.00",
            font=FONT_TOTAL,
            bg=CARD,
            fg=PRIMARY
        )

        self.total_label.pack(side=tk.RIGHT)

    # ----------------------------------------------------------
    # GENERATE BILL
    # ----------------------------------------------------------

    def _build_generate_button(self, parent):

        btn = tk.Button(
            parent,
            text="\U0001F9FE  GENERATE BILL",
            command=self.generate_bill,
            bg=PRIMARY,
            fg=PRIMARY_FOREGROUND,
            activebackground=PRIMARY,
            activeforeground=PRIMARY_FOREGROUND,
            font=("Segoe UI", 13, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        btn.pack(fill="x", pady=20, ipady=10)

    # ----------------------------------------------------------
    # FOOTER
    # ----------------------------------------------------------

    def _build_footer(self, parent):

        tk.Label(
            parent,
            text="\u00A9 2025 Inventory & Billing System. All rights reserved.",
            font=FONT_SMALL,
            bg=BACKGROUND,
            fg=MUTED_FOREGROUND
        ).pack(pady=(0, 10))

    # ==========================================================
    # LOAD CUSTOMERS
    # ==========================================================

    def load_customers(self):

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT customer_id, name, email
                FROM customers
                ORDER BY name
            """)

            customers = cursor.fetchall()

            self.customer_data = customers

            self.customer_combo["values"] = [
                f"{customer[0]} - {customer[1]} - {customer[2]}"
                for customer in customers
            ]

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not load customers.\n\n{e}"
            )

            self.customer_data = []

        finally:

            if connection:
                connection.close()

    # ==========================================================
    # LOAD PRODUCTS
    # ==========================================================

    def load_products(self):

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    product_id,
                    name,
                    price,
                    quantity
                FROM products
                WHERE quantity > 0
                ORDER BY name
            """)

            products = cursor.fetchall()

            self.product_data = products

            self.product_combo["values"] = [
                f"{product[0]} - {product[1]} - ₹{product[2]:.2f}"
                for product in products
            ]

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not load products.\n\n{e}"
            )

            self.product_data = []

        finally:

            if connection:
                connection.close()

    # ==========================================================
    # ADD PRODUCT
    # ==========================================================

    def add_product(self):

        selected = self.product_combo.get()

        if not selected:

            messagebox.showwarning(
                "Product Required",
                "Please select a product."
            )

            return

        quantity_text = (
            self.quantity_entry.get().strip()
        )

        if not quantity_text:

            messagebox.showwarning(
                "Quantity Required",
                "Please enter a quantity."
            )

            return

        try:

            quantity = int(quantity_text)

        except ValueError:

            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be a whole number."
            )

            return

        if quantity <= 0:

            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be greater than 0."
            )

            return

        # Get product ID

        try:

            product_id = int(
                selected.split(" - ")[0]
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Invalid product selected."
            )

            return

        # Find product

        product = None

        for p in self.product_data:

            if p[0] == product_id:

                product = p
                break

        if product is None:

            messagebox.showerror(
                "Error",
                "Product could not be found."
            )

            return

        # Check stock

        available_stock = product[3]

        existing_quantity = 0

        for item in self.cart:

            if item["product_id"] == product_id:

                existing_quantity = item["quantity"]
                break

        total_requested = (
            existing_quantity + quantity
        )

        if total_requested > available_stock:

            messagebox.showerror(
                "Insufficient Stock",
                f"Available stock: {available_stock}\n"
                f"Already in cart: {existing_quantity}\n"
                f"Requested quantity: {quantity}"
            )

            return

        price = float(product[2])

        # If product already exists in cart,
        # increase its quantity

        found = False

        for item in self.cart:

            if item["product_id"] == product_id:

                item["quantity"] += quantity

                item["total"] = (
                    item["quantity"] * item["price"]
                )

                found = True

                break

        # Otherwise add new product

        if not found:

            self.cart.append({
                "product_id": product_id,
                "name": product[1],
                "quantity": quantity,
                "price": price,
                "total": price * quantity
            })

        self.refresh_cart()

        self.quantity_entry.delete(
            0,
            tk.END
        )

    # ==========================================================
    # REFRESH CART
    # ==========================================================

    def refresh_cart(self):

        for item in self.cart_table.get_children():

            self.cart_table.delete(item)

        for item in self.cart:

            self.cart_table.insert(
                "",
                tk.END,
                values=(
                    item["product_id"],
                    item["name"],
                    item["quantity"],
                    f"₹{item['price']:.2f}",
                    f"₹{item['total']:.2f}"
                )
            )

        # Recalculate without showing an error
        self.update_total(
            show_errors=False
        )

        # Purely visual: swap the empty-state placeholder for the
        # table (or back) depending on whether the cart has items.
        # Does not affect self.cart or the table's data in any way.
        self._sync_cart_visibility()

    def _sync_cart_visibility(self):

        if self.cart:

            self.cart_empty_state.pack_forget()

            self.cart_table.pack(
                side=tk.LEFT,
                fill="both",
                expand=True
            )

        else:

            self.cart_table.pack_forget()

            self.cart_empty_state.pack(
                fill="both",
                expand=True
            )

    # ==========================================================
    # REMOVE PRODUCT
    # ==========================================================

    def remove_product(self):

        selected = self.cart_table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a product to remove."
            )

            return

        selected_item = selected[0]

        values = self.cart_table.item(
            selected_item,
            "values"
        )

        product_id = int(values[0])

        self.cart = [
            item
            for item in self.cart
            if item["product_id"] != product_id
        ]

        self.refresh_cart()

    # ==========================================================
    # CLEAR CART
    # ==========================================================

    def clear_cart(self):

        if not self.cart:

            return

        answer = messagebox.askyesno(
            "Clear Cart",
            "Are you sure you want to clear the cart?"
        )

        if not answer:

            return

        self.cart.clear()

        # Reset discount BEFORE recalculating
        self.discount_entry.delete(
            0,
            tk.END
        )

        self.discount_entry.insert(
            0,
            "0"
        )

        # Clear table

        for row in self.cart_table.get_children():

            self.cart_table.delete(row)

        # Reset totals

        self.update_total(
            show_errors=False
        )

    # ==========================================================
    # RESET AFTER SUCCESSFUL BILL
    # ==========================================================

    def reset_after_bill(self):

        # IMPORTANT:
        # Reset discount BEFORE clearing cart.
        #
        # Otherwise:
        #
        # discount = 100
        # subtotal = 0
        #
        # and the application may think
        # discount exceeds subtotal.

        self.discount_entry.delete(
            0,
            tk.END
        )

        self.discount_entry.insert(
            0,
            "0"
        )

        # Clear cart

        self.cart.clear()

        # Clear cart table

        for row in self.cart_table.get_children():

            self.cart_table.delete(row)

        # Reset totals

        self.subtotal_label.config(
            text="Subtotal: ₹0.00"
        )

        self.discount_label.config(
            text="Discount: ₹0.00"
        )

        self.gst_label.config(
            text="GST (18%): ₹0.00"
        )

        self.total_label.config(
            text="Total: ₹0.00"
        )

        # Clear quantity

        self.quantity_entry.delete(
            0,
            tk.END
        )

    # ==========================================================
    # CALCULATE TOTAL
    # ==========================================================

    def update_total(self, show_errors=True):

        # Calculate subtotal

        subtotal = sum(
            item["total"]
            for item in self.cart
        )

        # Empty cart
        #
        # IMPORTANT:
        # Don't validate the discount against
        # zero subtotal when there are no items.

        if subtotal <= 0:

            self.subtotal_label.config(
                text="Subtotal: ₹0.00"
            )

            self.discount_label.config(
                text="Discount: ₹0.00"
            )

            self.gst_label.config(
                text="GST (18%): ₹0.00"
            )

            self.total_label.config(
                text="Total: ₹0.00"
            )

            return (
                0,
                0,
                0,
                0
            )

        # Read discount

        discount_text = (
            self.discount_entry.get().strip()
        )

        if discount_text == "":

            discount = 0

        else:

            try:

                discount = float(
                    discount_text
                )

            except ValueError:

                if show_errors:

                    messagebox.showerror(
                        "Invalid Discount",
                        "Discount must be a number."
                    )

                return None

        # Negative discount

        if discount < 0:

            if show_errors:

                messagebox.showerror(
                    "Invalid Discount",
                    "Discount cannot be negative."
                )

            return None

        # Discount greater than subtotal

        if discount > subtotal:

            if show_errors:

                messagebox.showerror(
                    "Invalid Discount",
                    f"Discount cannot exceed "
                    f"subtotal of ₹{subtotal:.2f}"
                )

            return None

        # Amount after discount

        taxable_amount = (
            subtotal - discount
        )

        # GST

        gst = taxable_amount * 0.18

        # Final total

        total = taxable_amount + gst

        # Update labels

        self.subtotal_label.config(
            text=f"Subtotal: ₹{subtotal:.2f}"
        )

        self.discount_label.config(
            text=f"Discount: ₹{discount:.2f}"
        )

        self.gst_label.config(
            text=f"GST (18%): ₹{gst:.2f}"
        )

        self.total_label.config(
            text=f"Total: ₹{total:.2f}"
        )

        return (
            subtotal,
            discount,
            gst,
            total
        )

    # ==========================================================
    # GENERATE BILL
    # ==========================================================

    def generate_bill(self):

        # -------------------------
        # Check customer
        # -------------------------

        customer = self.customer_combo.get()

        if not customer:

            messagebox.showwarning(
                "Customer Required",
                "Please select a customer."
            )

            return

        # -------------------------
        # Check cart
        # -------------------------

        if not self.cart:

            messagebox.showwarning(
                "Empty Cart",
                "Please add at least one product."
            )

            return

        # -------------------------
        # Calculate total
        # -------------------------

        totals = self.update_total(
            show_errors=True
        )

        if totals is None:

            return

        subtotal, discount, gst, total = totals

        # -------------------------
        # Get customer ID
        # -------------------------

        try:

            customer_id = int(
                customer.split(" - ")[0]
            )
            customer_parts = customer.split(" - ")
            customer_name = customer_parts[1]
            customer_email = customer_parts[2]

        except ValueError:

            messagebox.showerror(
                "Error",
                "Invalid customer selected."
            )

            return

        # -------------------------
        # Payment method
        # -------------------------

        payment_method = (
            self.payment_combo.get()
        )

        if not payment_method:

            messagebox.showwarning(
                "Payment Required",
                "Please select a payment method."
            )

            return

        # -------------------------
        # Create Sale object
        # -------------------------

        sale = Sale(
            customer_id=customer_id,
            subtotal=subtotal,
            discount=discount,
            gst=gst,
            payment_method=payment_method
        )

        # -------------------------
        # Add items
        # -------------------------

        for item in self.cart:

            sale_item = SaleItem(
                product_id=item["product_id"],
                quantity=item["quantity"],
                price=item["price"]
            )

            sale.add_item(
                sale_item
            )

        # -------------------------
        # Confirm
        # -------------------------

        confirmation = messagebox.askyesno(
            "Confirm Bill",
            f"Subtotal: ₹{subtotal:.2f}\n"
            f"Discount: ₹{discount:.2f}\n"
            f"GST: ₹{gst:.2f}\n"
            f"Total: ₹{total:.2f}\n"
            f"Payment: {payment_method}\n\n"
            f"Generate this bill?"
        )

        if not confirmation:

            return

        # -------------------------
        # Save sale
        # -------------------------

        sale_id = (
            self.billing_service.create_sale(
                sale
            )
        )

        if sale_id:

        # ==========================================
        # GENERATE PDF
        # ==========================================

            invoice_path = (
                self.invoice_service.generate_invoice(
                    sale_id
                )
            )

            if not invoice_path:

                messagebox.showwarning(
                    "PDF Error",
                    f"Bill #{sale_id} was saved successfully,\n"
                    "but the PDF could not be generated."
                )

                self.reset_after_bill()
                self.load_products()

                return

            # ==========================================
            # SEND EMAIL
            # ==========================================

            email_sent = False

            try:

                email_sent = (
                    self.email_service.send_invoice(
                        customer_email=customer_email,
                        customer_name=customer_name,
                        sale_id=sale_id,
                        invoice_path=invoice_path
                    )
                )

            except Exception as e:

                print(
                    "Email error:",
                    e
                )

            # ==========================================
            # SHOW RESULT
            # ==========================================

            if email_sent:

                messagebox.showinfo(
                    "Bill Completed",
                    f"Bill generated successfully!\n\n"
                    f"Bill ID: {sale_id}\n"
                    f"Payment: {payment_method}\n"
                    f"Total: ₹{total:.2f}\n\n"
                    f"Invoice PDF generated.\n"
                    f"Receipt sent to:\n"
                    f"{customer_email}"
                )

            else:

                messagebox.showwarning(
                    "Bill Generated",
                    f"Bill #{sale_id} was generated successfully.\n\n"
                    f"PDF invoice was created, but the "
                    f"email could not be sent.\n\n"
                    f"Customer Email:\n{customer_email}"
                )

            # ==========================================
            # RESET BILLING SCREEN
            # ==========================================

            self.reset_after_bill()

            # Reload products because stock changed

            self.load_products()


# ==============================================================
# RUN
# ==============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = BillingWindow(root)

    root.mainloop()