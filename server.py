import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template, url_for, request, redirect
import datetime
import csv
import os

app = Flask(__name__)

@app.route('/test_email')
def test_email():
    send_email('Test Subject', 'This is a test email body.')
    return 'Email Sent'

# Function to send email notification
def send_email(subject, body):
    # Load your email and password from environment variables
    email_user = os.getenv('EMAIL_USER')  # Example: "youremail@hotmail.com"
    email_password = os.getenv('EMAIL_PASSWORD')  # Example: "yourpassword"
    to_email = "fotopoulos.v2@gmail.com"  # Your email address where you want to receive notifications

    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = to_email
    msg['Subject'] = subject

    # Add body to email
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Hotmail's SMTP server and send the email
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)  # Hotmail SMTP server
        server.starttls()  # Secure the connection
        server.login(email_user, email_password)  # Login using your credentials
        server.sendmail(email_user, to_email, msg.as_string())  # Send the email
        server.quit()  # Close the connection
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.route("/")
def my_home():
    return render_template('index.html')

@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f"\n{datetime.datetime.now().strftime('Date: %d/%m/%Y, Time: %H:%M:%S')} \n{email} \n{subject} \n{message}\n\n")

def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([datetime.datetime.now().strftime('Date: %d/%m/%Y, Time: %H:%M:%S'), email, subject, message])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()  # Get form data
            write_to_csv(data)  # Write to CSV file
            # Send an email notification
            subject = f"New Message from {data['email']}"
            body = f"Subject: {data['subject']}\n\nMessage:\n{data['message']}"
            send_email(subject, body)  # Send email notification
            return redirect('/form_submitted.html')  # Redirect after form submission
        except Exception as e:
            return f"An error occurred: {e}"
    else:
        return "Something went wrong"

if __name__ == '__main__':
    app.run(debug=True)
