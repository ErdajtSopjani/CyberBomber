import smtplib
import getpass
import os
import mimetypes
import threading
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def print_colored_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    start_color = "\033[38;5;93m"
    end_color = "\033[38;5;104m"
    reset_color = "\033[0m"

    ascii_art = f"""
    {start_color}
╔═╗┬ ┬┌┐ ┌─┐┬─┐╔╗ ┌─┐┌┬┐┌┐ ┌─┐┬─┐
║  └┬┘├┴┐├┤ ├┬┘╠╩╗│ ││││├┴┐├┤ ├┬┘
╚═╝ ┴ └─┘└─┘┴└─╚═╝└─┘┴ ┴└─┘└─┘┴└─
    {end_color}{reset_color}
    """
    print(ascii_art)
print_colored_banner()
def send_email(email, password, recipient_email, subject, msg, attachment_path):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(email, password)
        message = MIMEMultipart()
        message['From'] = email
        message['To'] = recipient_email
        message['Subject'] = subject

        message.attach(MIMEText(msg, 'plain'))

        if attachment_path:
            attachment_name = os.path.basename(attachment_path)
            mime_type, _ = mimetypes.guess_type(attachment_path)
            if mime_type:
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(open(attachment_path, 'rb').read())
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', f'attachment; filename={attachment_name}')
                message.attach(attachment)

        text = message.as_string()
        server.sendmail(email, recipient_email, text)
        print(f"Email sent to {recipient_email} successfully!")

    except smtplib.SMTPAuthenticationError as e:
        print("Authentication Error:", e)
    finally:
        server.quit()

def send_emails(email, password):
    wordlist_path = input("(e.g C:\\Path\\to\\wordlist.txt) \nPlease enter the path to a wordlist with emails: ")
    print_colored_banner()

    with open(wordlist_path, 'r') as file:
        email_list = file.readlines()

    subject = input("Enter the Subject: ")
    print_colored_banner()

    num_threads = int(input("How many times do you want to send this email: "))

    msg = ""
    option_msg = input("Do you want to send a message from a .txt file or write a message yourself?\n1) From .txt file\n2) Write it myself\n")

    while option_msg != "1" and option_msg != "2":
        option_msg = input("Do you want to send a message from a .txt file or write a message yourself?\n1) From .txt file\n2) Write it myself\n")

    if option_msg == "1":
        message_path = input("(e.g C:\\Path\\to\\email.txt) \nEnter the path to the message .txt file: ")
        print_colored_banner()
        with open(message_path, 'r') as message_file:
            msg = message_file.read()
    elif option_msg == "2":
        msg = input("Enter Your Message:\n")
        print_colored_banner()

    attachment_path = input("Enter the path to the attachment (e.g C:\\Path\\to\\file.pdf): ")
    print_colored_banner()

    def send_emails_thread(recipient_email):
        for _ in range(num_threads):
            send_email(email, password, recipient_email, subject, msg, attachment_path)

    threads = []
    for recipient_email in email_list:
        recipient_email = recipient_email.strip()
        thread = threading.Thread(target=send_emails_thread, args=(recipient_email,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def main():
    email = input("Enter Your Email (gmail only): ")

    password = getpass.getpass("Enter your App Password: ")

    print("Attempting login...")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    try:
        server.login(email, password)
        print("Successfully Signed in")
        time.sleep(1)
        print_colored_banner()

        while not email or not password:
            print("You must provide both email and password.\n")
            email = input("Enter Your Email (gmail only): ")
            password = getpass.getpass("Enter your App Password: ")
            print_colored_banner()

        send_emails(email, password)

    finally:
        server.quit()

if __name__ == "__main__":
    main()

