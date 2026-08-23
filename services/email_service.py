import os
import smtplib

from email.message import EmailMessage

from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


class EmailService:

    def __init__(self):

        self.email_address = os.getenv(
            "EMAIL_ADDRESS"
        )

        self.app_password = os.getenv(
            "EMAIL_APP_PASSWORD"
        )

        # Check email
        if not self.email_address:

            raise ValueError(
                "EMAIL_ADDRESS is missing from .env"
            )

        # Check app password
        if not self.app_password:

            raise ValueError(
                "EMAIL_APP_PASSWORD is missing from .env"
            )

    # ==========================================================
    # SEND INVOICE
    # ==========================================================

    def send_invoice(
        self,
        customer_email,
        customer_name,
        sale_id,
        invoice_path
    ):

        # ------------------------------------------------------
        # Validate customer email
        # ------------------------------------------------------

        if not customer_email:

            raise ValueError(
                "Customer email is missing."
            )

        # ------------------------------------------------------
        # Validate PDF
        # ------------------------------------------------------

        if not os.path.exists(invoice_path):

            raise FileNotFoundError(
                "Invoice PDF was not found."
            )

        # ------------------------------------------------------
        # Create email
        # ------------------------------------------------------

        message = EmailMessage()

        message["Subject"] = (
            f"Invoice #{sale_id} - "
            "Inventory & Billing System"
        )

        message["From"] = self.email_address

        message["To"] = customer_email

        message.set_content(
            f"""
Hello {customer_name},

Thank you for your purchase.

Please find your invoice attached.

Invoice Number: #{sale_id}

Thank you for shopping with us.

Regards,
Inventory & Billing System
"""
        )

        # ------------------------------------------------------
        # Attach PDF
        # ------------------------------------------------------

        with open(
            invoice_path,
            "rb"
        ) as file:

            pdf_data = file.read()

        message.add_attachment(
            pdf_data,
            maintype="application",
            subtype="pdf",
            filename=f"invoice_{sale_id}.pdf"
        )

        # ------------------------------------------------------
        # Connect to Gmail
        # ------------------------------------------------------

        try:

            with smtplib.SMTP(
                "smtp.gmail.com",
                587
            ) as server:

                # Secure connection
                server.starttls()

                # Login using App Password
                server.login(
                    self.email_address,
                    self.app_password
                )

                # Send email
                server.send_message(
                    message
                )

            print(
                f"Invoice sent to {customer_email}"
            )

            return True

        except Exception as e:

            print(
                "Email sending error:",
                repr(e)
            )

            return False

if __name__ == "__main__":

    service = EmailService()

    result = service.send_invoice(
        customer_email="parthbhor0225@gmail.com",
        customer_name="Parth",
        sale_id=1,
        invoice_path="invoices/invoice_1.pdf"
    )

    if result:

        print(
            "Email sent successfully!"
        )

    else:

        print(
            "Email failed."
        )