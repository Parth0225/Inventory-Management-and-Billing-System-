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


class ProductWindow:

    def __init__(self, root):

        self.root = root
        self.root.title("Product Management")
        self.root.geometry("1150x850")
        self.root.minsize(900, 600)
        self.root.configure(bg=BACKGROUND)

        self.selected_product_id = None

        self._setup_styles()
        self.create_widgets()
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

        # ------------------------------------------------------
        # Scrollable content area so nothing is ever pushed off
        # screen and unreachable, regardless of window size.
        # ------------------------------------------------------

        outer = tk.Frame(self.root, bg=BACKGROUND)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=BACKGROUND, highlightthickness=0)
        scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
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

        # Click a row (kept exactly as in the original)
        self.product_table.bind(
            "<ButtonRelease-1>",
            self.select_product
        )

    # ----------------------------------------------------------
    # HEADER
    # ----------------------------------------------------------

    def _build_header(self):

        header = tk.Frame(
            self.root,
            bg=CARD,
            height=56,
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
            text="Product Management",
            font=FONT_HEADING,
            bg=BACKGROUND,
            fg=FOREGROUND
        ).pack(anchor="w")

        tk.Label(
            text_col,
            text="Manage your products, stock and categories",
            font=FONT_BODY,
            bg=BACKGROUND,
            fg=MUTED_FOREGROUND
        ).pack(anchor="w")

    # ----------------------------------------------------------
    # PRODUCT FORM
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
            grid, "\U0001F3F7", "Product Name"
        )
        name_wrap.grid(row=0, column=0, sticky="ew", padx=(0, 20), pady=10)

        price_wrap, self.price_entry = self._labeled_entry(
            grid, "\u20B9", "Price (\u20B9)"
        )
        price_wrap.grid(row=0, column=1, sticky="ew", padx=(20, 0), pady=10)

        quantity_wrap, self.quantity_entry = self._labeled_entry(
            grid, "\U0001F4E6", "Quantity"
        )
        quantity_wrap.grid(row=1, column=0, sticky="ew", padx=(0, 20), pady=10)

        category_wrap, self.category_entry = self._labeled_entry(
            grid, "\U0001F4CB", "Category"
        )
        category_wrap.grid(row=1, column=1, sticky="ew", padx=(20, 0), pady=10)

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
            "\u2795  Add Product",
            self.add_product
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self._outline_button(
            button_row,
            "\u270F  Update",
            self.update_product
        ).grid(row=0, column=1, sticky="ew", padx=8)

        self._outline_button(
            button_row,
            "\U0001F5D1  Delete",
            self.delete_product,
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
            lambda event: self.search_products()
        )

        button_row = tk.Frame(inner, bg=CARD)
        button_row.pack(side=tk.LEFT, padx=(15, 0))

        self._primary_button(
            button_row,
            "\U0001F50D  Search",
            self.search_products
        ).pack(side=tk.LEFT, padx=(0, 10))

        self._outline_button(
            button_row,
            "\U0001F501  Show All",
            self.load_products
        ).pack(side=tk.LEFT)

    # ----------------------------------------------------------
    # PRODUCT TABLE
    # ----------------------------------------------------------

    def _build_table_section(self, parent):

        section = self._card(parent)
        section.pack(fill="both", expand=True, pady=(20, 0))

        table_frame = tk.Frame(section, bg=CARD, padx=10, pady=10)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = (
            "id",
            "name",
            "category",
            "price",
            "quantity"
        )

        self.product_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=14
        )

        self.product_table.heading(
            "id",
            text="ID"
        )

        self.product_table.heading(
            "name",
            text="Product Name"
        )

        self.product_table.heading(
            "category",
            text="Category"
        )

        self.product_table.heading(
            "price",
            text="Price"
        )

        self.product_table.heading(
            "quantity",
            text="Quantity"
        )

        self.product_table.column(
            "id",
            width=70,
            anchor="center"
        )

        self.product_table.column(
            "name",
            width=280
        )

        self.product_table.column(
            "category",
            width=180
        )

        self.product_table.column(
            "price",
            width=140,
            anchor="e"
        )

        self.product_table.column(
            "quantity",
            width=120,
            anchor="center"
        )

        # Purely visual stock-level tinting -- does not affect the
        # values stored/read from the table in any way.

        self.product_table.tag_configure("stock_out", background="#FCE7E7")
        self.product_table.tag_configure("stock_low", background="#F1F2FE")
        self.product_table.tag_configure("stock_ok", background=CARD)

        scrollbar_y = tk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.product_table.yview
        )

        self.product_table.configure(
            yscrollcommand=scrollbar_y.set
        )

        self.product_table.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        scrollbar_y.pack(side=tk.LEFT, fill="y")

        self.product_count_label = tk.Label(
            parent,
            text="Showing 0 products",
            font=FONT_SMALL,
            bg=BACKGROUND,
            fg=MUTED_FOREGROUND
        )

        self.product_count_label.pack(anchor="w", pady=(10, 0))

    # ==========================================================
    # LOAD PRODUCTS
    # ==========================================================

    def load_products(self):

        self.search_entry.delete(
            0,
            tk.END
        )

        self.fetch_products()

    # ==========================================================
    # FETCH PRODUCTS
    # ==========================================================

    def fetch_products(
        self,
        search_text=None
    ):

        # Clear table

        for row in self.product_table.get_children():
            self.product_table.delete(row)

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            if search_text:

                cursor.execute("""
                    SELECT
                        product_id,
                        name,
                        category,
                        price,
                        quantity
                    FROM products
                    WHERE name LIKE ?
                    OR category LIKE ?
                    ORDER BY product_id DESC
                """, (
                    f"%{search_text}%",
                    f"%{search_text}%"
                ))

            else:

                cursor.execute("""
                    SELECT
                        product_id,
                        name,
                        category,
                        price,
                        quantity
                    FROM products
                    ORDER BY product_id DESC
                """)

            products = cursor.fetchall()

            for product in products:

                quantity = product[4]

                if quantity == 0:
                    tag = "stock_out"
                elif quantity < 5:
                    tag = "stock_low"
                else:
                    tag = "stock_ok"

                self.product_table.insert(
                    "",
                    tk.END,
                    values=(
                        product[0],
                        product[1],
                        product[2],
                        f"₹{product[3]:.2f}",
                        product[4]
                    ),
                    tags=(tag,)
                )

            # Purely visual count refresh -- does not affect the
            # table data or any of the search/fetch logic above.

            if hasattr(self, "product_count_label"):

                self.product_count_label.config(
                    text=f"Showing {len(products)} product"
                    f"{'s' if len(products) != 1 else ''}"
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not load products.\n\n{e}"
            )

        finally:

            if connection:
                connection.close()

    # ==========================================================
    # SEARCH
    # ==========================================================

    def search_products(self):

        search_text = (
            self.search_entry.get().strip()
        )

        if not search_text:

            self.load_products()
            return

        self.fetch_products(
            search_text
        )

    # ==========================================================
    # SELECT PRODUCT
    # ==========================================================

    def select_product(self, event):

        selected = self.product_table.selection()

        if not selected:
            return

        values = self.product_table.item(
            selected[0],
            "values"
        )

        self.selected_product_id = int(
            values[0]
        )

        # Fill form

        self.name_entry.delete(
            0,
            tk.END
        )
        self.name_entry.insert(
            0,
            values[1]
        )

        self.category_entry.delete(
            0,
            tk.END
        )
        self.category_entry.insert(
            0,
            values[2]
        )

        self.price_entry.delete(
            0,
            tk.END
        )
        self.price_entry.insert(
            0,
            values[3].replace("₹", "")
        )

        self.quantity_entry.delete(
            0,
            tk.END
        )
        self.quantity_entry.insert(
            0,
            values[4]
        )

    # ==========================================================
    # ADD PRODUCT
    # ==========================================================

    def add_product(self):

        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        price_text = self.price_entry.get().strip()
        quantity_text = self.quantity_entry.get().strip()

        # Validate name

        if not name:

            messagebox.showwarning(
                "Invalid Product",
                "Product name is required."
            )
            return

        # Validate category

        if not category:

            messagebox.showwarning(
                "Invalid Product",
                "Category is required."
            )
            return

        # Validate price

        try:

            price = float(price_text)

            if price <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Price",
                "Price must be a positive number."
            )
            return

        # Validate quantity

        try:

            quantity = int(quantity_text)

            if quantity < 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be a non-negative whole number."
            )
            return

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO products
                (name, category, price, quantity)
                VALUES (?, ?, ?, ?)
            """, (
                name,
                category,
                price,
                quantity
            ))

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Product added successfully."
            )

            self.clear_form()
            self.fetch_products()

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Could not add product.\n\n{e}"
            )

        finally:

            if connection:
                connection.close()

    # ==========================================================
    # UPDATE PRODUCT
    # ==========================================================

    def update_product(self):

        if self.selected_product_id is None:

            messagebox.showwarning(
                "No Selection",
                "Please select a product first."
            )

            return

        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        price_text = self.price_entry.get().strip()
        quantity_text = self.quantity_entry.get().strip()

        if not name or not category:

            messagebox.showwarning(
                "Invalid Product",
                "Name and category are required."
            )

            return

        try:

            price = float(price_text)

            if price <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Price",
                "Price must be a positive number."
            )

            return

        try:

            quantity = int(quantity_text)

            if quantity < 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be a non-negative whole number."
            )

            return

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE products
                SET
                    name = ?,
                    category = ?,
                    price = ?,
                    quantity = ?
                WHERE product_id = ?
            """, (
                name,
                category,
                price,
                quantity,
                self.selected_product_id
            ))

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Product updated successfully."
            )

            self.clear_form()
            self.fetch_products()

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Could not update product.\n\n{e}"
            )

        finally:

            if connection:
                connection.close()

    # ==========================================================
    # DELETE PRODUCT
    # ==========================================================

    def delete_product(self):

        if self.selected_product_id is None:

            messagebox.showwarning(
                "No Selection",
                "Please select a product first."
            )

            return

        confirmation = messagebox.askyesno(
            "Delete Product",
            "Are you sure you want to delete this product?"
        )

        if not confirmation:
            return

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM products
                WHERE product_id = ?
            """, (
                self.selected_product_id,
            ))

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Product deleted successfully."
            )

            self.clear_form()
            self.fetch_products()

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Could not delete product.\n\n{e}"
            )

        finally:

            if connection:
                connection.close()

    # ==========================================================
    # CLEAR FORM
    # ==========================================================

    def clear_form(self):

        self.selected_product_id = None

        self.name_entry.delete(
            0,
            tk.END
        )

        self.category_entry.delete(
            0,
            tk.END
        )

        self.price_entry.delete(
            0,
            tk.END
        )

        self.quantity_entry.delete(
            0,
            tk.END
        )

        self.product_table.selection_remove(
            self.product_table.selection()
        )


# ==============================================================
# TEST
# ==============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = ProductWindow(root)

    root.mainloop()