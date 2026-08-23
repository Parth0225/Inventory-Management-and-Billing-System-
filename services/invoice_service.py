import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from database.db_connection import get_connection


class InvoiceService:

    def __init__(self):

        self.invoice_folder = "invoices"

        # Create invoices folder if it doesn't exist
        os.makedirs(
            self.invoice_folder,
            exist_ok=True
        )

    # ==========================================================
    # GENERATE PDF
    # ==========================================================

    def generate_invoice(self, sale_id):

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            # --------------------------------------------------
            # Get sale + customer information
            # --------------------------------------------------

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
            """, (sale_id,))

            sale = cursor.fetchone()

            if sale is None:

                print("Sale not found.")

                return None

            # --------------------------------------------------
            # Get sale items
            # --------------------------------------------------

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
            """, (sale_id,))

            items = cursor.fetchall()

        except Exception as e:

            print("Database error:", e)

            return None

        finally:

            if connection:
                connection.close()

        # ======================================================
        # PDF PATH
        # ======================================================

        file_path = os.path.join(
            self.invoice_folder,
            f"invoice_{sale_id}.pdf"
        )

        # ======================================================
        # CREATE PDF
        # ======================================================

        try:

            document = SimpleDocTemplate(
                file_path,
                pagesize=A4,
                rightMargin=20 * mm,
                leftMargin=20 * mm,
                topMargin=20 * mm,
                bottomMargin=20 * mm
            )

            styles = getSampleStyleSheet()

            elements = []

            # --------------------------------------------------
            # TITLE
            # --------------------------------------------------

            title = Paragraph(
                "<b>INVENTORY & BILLING SYSTEM</b>",
                styles["Title"]
            )

            elements.append(title)

            elements.append(
                Spacer(1, 10)
            )

            invoice_title = Paragraph(
                f"<b>INVOICE #{sale[0]}</b>",
                styles["Heading2"]
            )

            elements.append(invoice_title)

            elements.append(
                Spacer(1, 10)
            )

            # --------------------------------------------------
            # CUSTOMER DETAILS
            # --------------------------------------------------

            customer_data = [
                ["Customer", sale[2]],
                ["Phone", sale[3]],
                ["Email", sale[4]],
                ["Address", sale[5]],
                ["Date", sale[1]],
                ["Payment", sale[10]]
            ]

            customer_table = Table(
                customer_data,
                colWidths=[
                    35 * mm,
                    120 * mm
                ]
            )

            customer_table.setStyle(
                TableStyle([
                    (
                        "FONTNAME",
                        (0, 0),
                        (0, -1),
                        "Helvetica-Bold"
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),
                    (
                        "PADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    )
                ])
            )

            elements.append(
                customer_table
            )

            elements.append(
                Spacer(1, 15)
            )

            # --------------------------------------------------
            # ITEMS TABLE
            # --------------------------------------------------

            item_data = [
                [
                    "Product",
                    "Quantity",
                    "Price",
                    "Total"
                ]
            ]

            for item in items:

                item_data.append([
                    item[0],
                    str(item[1]),
                    f"₹{item[2]:.2f}",
                    f"₹{item[3]:.2f}"
                ])

            item_table = Table(
                item_data,
                colWidths=[
                    70 * mm,
                    25 * mm,
                    30 * mm,
                    30 * mm
                ]
            )

            item_table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold"
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),
                    (
                        "ALIGN",
                        (1, 1),
                        (-1, -1),
                        "RIGHT"
                    ),
                    (
                        "PADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    )
                ])
            )

            elements.append(
                item_table
            )

            elements.append(
                Spacer(1, 15)
            )

            # --------------------------------------------------
            # BILL SUMMARY
            # --------------------------------------------------

            summary_data = [
                ["Subtotal", f"₹{sale[6]:.2f}"],
                ["Discount", f"₹{sale[7]:.2f}"],
                ["GST", f"₹{sale[8]:.2f}"],
                ["Grand Total", f"₹{sale[9]:.2f}"]
            ]

            summary_table = Table(
                summary_data,
                colWidths=[
                    120 * mm,
                    35 * mm
                ]
            )

            summary_table.setStyle(
                TableStyle([
                    (
                        "ALIGN",
                        (1, 0),
                        (1, -1),
                        "RIGHT"
                    ),
                    (
                        "FONTNAME",
                        (0, -1),
                        (-1, -1),
                        "Helvetica-Bold"
                    ),
                    (
                        "LINEABOVE",
                        (0, -1),
                        (-1, -1),
                        1,
                        colors.black
                    ),
                    (
                        "PADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    )
                ])
            )

            elements.append(
                summary_table
            )

            elements.append(
                Spacer(1, 20)
            )

            # --------------------------------------------------
            # FOOTER
            # --------------------------------------------------

            footer = Paragraph(
                "Thank you for your purchase!",
                styles["Normal"]
            )

            elements.append(
                footer
            )

            # Build PDF

            document.build(elements)

            print(
                f"Invoice generated successfully: {file_path}"
            )

            return file_path

        except Exception as e:

            print(
                "PDF generation error:",
                e
            )

            return None

if __name__ == "__main__":

    service = InvoiceService()

    service.generate_invoice(1)