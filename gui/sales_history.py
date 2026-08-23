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
FONT_STAT_VALUE = ("Segoe UI", 16, "bold")


class SalesHistoryWindow:

    def __init__(self, root):

        self.root = root
        self.root.title("Sales History")
        self.root.geometry("1250x800")
        self.root.minsize(950, 600)
        self.root.configure(bg=BACKGROUND)

        self._setup_styles()
        self.create_widgets()
        self.load_sales()

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
            rowheight=32,
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
            pady=8
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
            pady=8
        )

    # ==========================================================
    # CREATE GUI
    # ==========================================================

    def create_widgets(self):

        self._build_header()

        # ------------------------------------------------------
        # Scrollable content area so nothing is ever pushed off
        # screen and unreachable, regardless of window size.
        # ------------------------------------------------------

        outer = tk.Frame(self.root, bg=BACKGROUND)
        outer.pack(fill="both", expand=True)

        body = tk.Frame(outer, bg=BACKGROUND)
        body.pack(fill="both", expand=True)

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
        self._build_search_section(content)
        self._build_table_section(content)
        self._build_stats_section(content)

    # ----------------------------------------------------------
    # HEADER
    # ----------------------------------------------------------

    def _build_header(self):

        header = tk.Frame(
            self.root,
            bg=CARD,
            height=48,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        header.pack(fill="x", side=tk.TOP)
        header.pack_propagate(False)

        left = tk.Frame(header, bg=CARD)
        left.pack(side=tk.LEFT, padx=20)

        tk.Label(
            left,
            text="\U0001FAB6",
            font=("Segoe UI", 12),
            bg=CARD,
            fg=PRIMARY
        ).pack(side=tk.LEFT)

        tk.Label(
            left,
            text="Inventory & Billing System",
            font=FONT_SUBHEADING,
            bg=CARD,
            fg=FOREGROUND
        ).pack(side=tk.LEFT, padx=10)

    # ----------------------------------------------------------
    # PAGE TITLE ROW
    # ----------------------------------------------------------

    def _build_title_row(self, parent):

        row = tk.Frame(parent, bg=BACKGROUND)
        row.pack(fill="x")

        left = tk.Frame(row, bg=BACKGROUND)
        left.pack(side=tk.LEFT)

        tk.Label(
            left,
            text="\U0001F4C8",
            font=("Segoe UI", 22),
            bg=SECONDARY,
            fg=PRIMARY,
            width=3,
            height=1
        ).pack(side=tk.LEFT, padx=(0, 15))

        text_col = tk.Frame(left, bg=BACKGROUND)
        text_col.pack(side=tk.LEFT)

        tk.Label(
            text_col,
            text="Sales History",
            font=FONT_HEADING,
            bg=BACKGROUND,
            fg=FOREGROUND
        ).pack(anchor="w")

        tk.Label(
            text_col,
            text="View and track all sales transactions",
            font=FONT_BODY,
            bg=BACKGROUND,
            fg=MUTED_FOREGROUND
        ).pack(anchor="w")

        right = tk.Frame(row, bg=BACKGROUND)
        right.pack(side=tk.RIGHT)

        self._outline_button(
            right,
            "\U0001F5D1  Refresh",
            self.load_sales
        ).pack(side=tk.LEFT, padx=(10, 0))

        self._outline_button(
            right,
            "\U0001F4C4  View Bill",
            self.view_bill
        ).pack(side=tk.LEFT)

    # ----------------------------------------------------------
    # SEARCH / FILTER CARD
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
            fg=PRIMARY,
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
            lambda event: self.search_sales()
        )

        button_row = tk.Frame(inner, bg=CARD)
        button_row.pack(side=tk.LEFT, padx=(15, 0))

        self._primary_button(
            button_row,
            "\U0001F50D  Search",
            self.search_sales
        ).pack(side=tk.LEFT, padx=(0, 10))

        self._outline_button(
            button_row,
            "\U0001F504  Show All",
            self.load_sales
        ).pack(side=tk.LEFT)

    # ----------------------------------------------------------
    # SALES TABLE
    # ----------------------------------------------------------

    def _build_table_section(self, parent):

        section = self._card(parent)
        section.pack(fill="both", expand=True, pady=(20, 0))

        table_frame = tk.Frame(section, bg=CARD, padx=10, pady=10)

        table_frame.pack(
            fill=tk.BOTH,
            expand=True
        )

        columns = (
            "sale_id",
            "date",
            "customer",
            "subtotal",
            "discount",
            "gst",
            "total",
            "payment"
        )

        self.sales_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        headings = {
            "sale_id": "Bill ID",
            "date": "Date",
            "customer": "Customer",
            "subtotal": "Subtotal",
            "discount": "Discount",
            "gst": "GST",
            "total": "Total",
            "payment": "Payment"
        }

        for column, heading in headings.items():

            self.sales_table.heading(
                column,
                text=heading
            )

        self.sales_table.column("sale_id", width=70, anchor="center")
        self.sales_table.column("date", width=160)
        self.sales_table.column("customer", width=160)
        self.sales_table.column("subtotal", width=100, anchor="e")
        self.sales_table.column("discount", width=100, anchor="e")
        self.sales_table.column("gst", width=100, anchor="e")
        self.sales_table.column("total", width=110, anchor="e")
        self.sales_table.column("payment", width=90, anchor="center")

        # Purely visual row tinting by payment method -- does not
        # affect the values stored/read from the table in any way.

        self.sales_table.tag_configure("pay_cash", background="#EEF0FE")
        self.sales_table.tag_configure("pay_upi", background="#F1F2FE")
        self.sales_table.tag_configure("pay_card", background="#FFFFFF")

        scrollbar_y = tk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.sales_table.yview
        )

        self.sales_table.configure(
            yscrollcommand=scrollbar_y.set
        )

        self.sales_table.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        scrollbar_y.pack(side=tk.LEFT, fill="y")

    # ----------------------------------------------------------
    # STATS ROW (decorative summary, matches design only)
    # ----------------------------------------------------------

    def _build_stats_section(self, parent):

        stats_card = tk.Frame(
            parent,
            bg=SECONDARY
        )

        stats_card.pack(pady=(20, 10))

        stats = [
            ("\U0001FA99", "Total Sales", "sales_total_value"),
            ("\U0001F4C4", "Total Bills", "sales_count_value"),
            ("\U0001F465", "Customers", "customer_count_value"),
        ]

        self._stat_labels = {}

        for icon, label, key in stats:

            box = tk.Frame(stats_card, bg=SECONDARY, padx=20, pady=14)
            box.pack(side=tk.LEFT)

            tk.Label(
                box,
                text=icon,
                font=("Segoe UI", 18),
                bg=SECONDARY,
                fg=PRIMARY
            ).pack(side=tk.LEFT, padx=(0, 10))

            text_col = tk.Frame(box, bg=SECONDARY)
            text_col.pack(side=tk.LEFT)

            tk.Label(
                text_col,
                text=label,
                font=FONT_SMALL,
                bg=SECONDARY,
                fg=SECONDARY_FOREGROUND
            ).pack(anchor="w")

            value_label = tk.Label(
                text_col,
                text="--",
                font=FONT_STAT_VALUE,
                bg=SECONDARY,
                fg=FOREGROUND
            )

            value_label.pack(anchor="w")

            self._stat_labels[key] = value_label

    def _update_stats(self, sales):

        total_sales = sum(
            sale[6] for sale in sales
        )

        total_bills = len(sales)

        unique_customers = len(
            {sale[2] for sale in sales}
        )

        if "sales_total_value" in self._stat_labels:

            self._stat_labels["sales_total_value"].config(
                text=f"₹{total_sales:,.2f}"
            )

        if "sales_count_value" in self._stat_labels:

            self._stat_labels["sales_count_value"].config(
                text=str(total_bills)
            )

        if "customer_count_value" in self._stat_labels:

            self._stat_labels["customer_count_value"].config(
                text=str(unique_customers)
            )

    # ==========================================================
    # LOAD SALES
    # ==========================================================

    def load_sales(self):

        self.search_entry.delete(
            0,
            tk.END
        )

        self.fetch_sales()

    # ==========================================================
    # SEARCH SALES
    # ==========================================================

    def search_sales(self):

        search_text = (
            self.search_entry.get().strip()
        )

        if not search_text:

            self.load_sales()
            return

        self.fetch_sales(
            search_text
        )

    # ==========================================================
    # FETCH SALES FROM DATABASE
    # ==========================================================

    def fetch_sales(
        self,
        search_text=None
    ):

        # Clear table

        for item in self.sales_table.get_children():

            self.sales_table.delete(item)

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            if search_text:

                cursor.execute("""
                    SELECT
                        s.sale_id,
                        s.sale_date,
                        c.name,
                        s.subtotal,
                        s.discount,
                        s.gst,
                        s.total,
                        s.payment_method
                    FROM sales s
                    JOIN customers c
                    ON s.customer_id = c.customer_id
                    WHERE c.name LIKE ?
                    ORDER BY s.sale_id DESC
                """, (
                    f"%{search_text}%",
                ))

            else:

                cursor.execute("""
                    SELECT
                        s.sale_id,
                        s.sale_date,
                        c.name,
                        s.subtotal,
                        s.discount,
                        s.gst,
                        s.total,
                        s.payment_method
                    FROM sales s
                    JOIN customers c
                    ON s.customer_id = c.customer_id
                    ORDER BY s.sale_id DESC
                """)

            sales = cursor.fetchall()

            # Insert into table

            for sale in sales:

                payment_method = (sale[7] or "").strip().lower()

                if payment_method == "cash":
                    tag = "pay_cash"
                elif payment_method == "upi":
                    tag = "pay_upi"
                else:
                    tag = "pay_card"

                self.sales_table.insert(
                    "",
                    tk.END,
                    values=(
                        sale[0],
                        sale[1],
                        sale[2],
                        f"₹{sale[3]:.2f}",
                        f"₹{sale[4]:.2f}",
                        f"₹{sale[5]:.2f}",
                        f"₹{sale[6]:.2f}",
                        sale[7]
                    ),
                    tags=(tag,)
                )

            # Purely visual summary refresh -- does not affect the
            # table data or any of the search/fetch logic above.

            self._update_stats(sales)

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not load sales.\n\n{e}"
            )

        finally:

            if connection:
                connection.close()

    # ==========================================================
    # VIEW BILL
    # ==========================================================

    def view_bill(self):

        selected = self.sales_table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a bill first."
            )

            return

        values = self.sales_table.item(
            selected[0],
            "values"
        )

        sale_id = values[0]

        self.show_bill_details(
            sale_id
        )

    # ==========================================================
    # BILL DETAILS
    # ==========================================================

    def show_bill_details(
        self,
        sale_id
    ):

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            # Get sale information

            cursor.execute("""
                SELECT
                    s.sale_id,
                    s.sale_date,
                    c.name,
                    c.phone,
                    c.email,
                    c.address,
                    s.subtotal,
                    s.discount,
                    s.gst,
                    s.total,
                    s.payment_method
                FROM sales s
                JOIN customers c
                ON s.customer_id = c.customer_id
                WHERE s.sale_id = ?
            """, (
                sale_id,
            ))

            sale = cursor.fetchone()

            if sale is None:

                messagebox.showerror(
                    "Error",
                    "Bill not found."
                )

                return

            # Get products in bill

            cursor.execute("""
                SELECT
                    p.name,
                    si.quantity,
                    si.price,
                    si.total
                FROM sale_items si
                JOIN products p
                ON si.product_id = p.product_id
                WHERE si.sale_id = ?
            """, (
                sale_id,
            ))

            items = cursor.fetchall()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not load bill.\n\n{e}"
            )

            return

        finally:

            if connection:
                connection.close()

        # ======================================================
        # BILL WINDOW
        # ======================================================
        #
        # Wrapped in a scrollable canvas (same fix used on the
        # other windows) so the full invoice -- including the
        # item table's "Total" column and the Subtotal/Total
        # summary lines -- is always reachable, no matter how
        # many items are on the bill or how small the window is.

        bill_window = tk.Toplevel(
            self.root
        )

        bill_window.title(
            f"Bill #{sale_id}"
        )

        bill_window.geometry(
            "700x750"
        )

        bill_window.minsize(600, 400)

        bill_window.configure(bg=BACKGROUND)

        bw_canvas = tk.Canvas(
            bill_window,
            bg=BACKGROUND,
            highlightthickness=0
        )

        bw_scrollbar = tk.Scrollbar(
            bill_window,
            orient="vertical",
            command=bw_canvas.yview
        )

        bw_canvas.configure(yscrollcommand=bw_scrollbar.set)

        bw_canvas.pack(side=tk.LEFT, fill="both", expand=True)
        bw_scrollbar.pack(side=tk.RIGHT, fill="y")

        bw_content = tk.Frame(bw_canvas, bg=BACKGROUND)

        bw_window = bw_canvas.create_window(
            (0, 0),
            window=bw_content,
            anchor="nw"
        )

        def on_bw_configure(event):
            bw_canvas.configure(scrollregion=bw_canvas.bbox("all"))

        def on_bw_canvas_configure(event):
            bw_canvas.itemconfig(bw_window, width=event.width)

        bw_content.bind("<Configure>", on_bw_configure)
        bw_canvas.bind("<Configure>", on_bw_canvas_configure)

        def on_bw_mousewheel(event):
            bw_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        bw_canvas.bind("<Enter>", lambda e: bw_canvas.bind_all("<MouseWheel>", on_bw_mousewheel))
        bw_canvas.bind("<Leave>", lambda e: bw_canvas.unbind_all("<MouseWheel>"))

        tk.Label(
            bw_content,
            text="INVOICE",
            font=("Segoe UI", 22, "bold"),
            bg=BACKGROUND,
            fg=FOREGROUND
        ).pack(pady=15)

        # Customer information

        customer_text = (
            f"Customer: {sale[2]}\n"
            f"Phone: {sale[3]}\n"
            f"Email: {sale[4]}\n"
            f"Address: {sale[5]}\n\n"
            f"Bill ID: {sale[0]}\n"
            f"Date: {sale[1]}\n"
            f"Payment: {sale[10]}"
        )

        tk.Label(
            bw_content,
            text=customer_text,
            justify=tk.LEFT,
            anchor="w",
            bg=BACKGROUND,
            fg=FOREGROUND,
            font=FONT_BODY
        ).pack(
            padx=30,
            anchor="w"
        )

        # Items

        columns = (
            "product",
            "quantity",
            "price",
            "total"
        )

        item_table = ttk.Treeview(
            bw_content,
            columns=columns,
            show="headings",
            height=min(len(items), 10) or 1
        )

        item_table.heading(
            "product",
            text="Product"
        )

        item_table.heading(
            "quantity",
            text="Qty"
        )

        item_table.heading(
            "price",
            text="Price"
        )

        item_table.heading(
            "total",
            text="Total"
        )

        # Explicit widths so every column -- including "Total" --
        # fits inside the window instead of being cut off.

        item_table.column("product", width=260, anchor="w")
        item_table.column("quantity", width=80, anchor="center")
        item_table.column("price", width=140, anchor="e")
        item_table.column("total", width=140, anchor="e")

        item_table.pack(
            fill=tk.X,
            padx=20,
            pady=20
        )

        for item in items:

            item_table.insert(
                "",
                tk.END,
                values=(
                    item[0],
                    item[1],
                    f"₹{item[2]:.2f}",
                    f"₹{item[3]:.2f}"
                )
            )

        # Summary

        summary = (
            f"Subtotal: ₹{sale[6]:.2f}\n"
            f"Discount: ₹{sale[7]:.2f}\n"
            f"GST: ₹{sale[8]:.2f}\n"
            f"TOTAL: ₹{sale[9]:.2f}"
        )

        tk.Label(
            bw_content,
            text=summary,
            font=("Segoe UI", 13, "bold"),
            justify=tk.RIGHT,
            bg=BACKGROUND,
            fg=PRIMARY
        ).pack(
            padx=30,
            pady=(0, 25),
            anchor="e"
        )


# ==============================================================
# TEST
# ==============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SalesHistoryWindow(root)

    root.mainloop()