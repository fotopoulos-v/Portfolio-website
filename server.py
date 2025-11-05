import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template, url_for, request, redirect, send_file, send_from_directory, Response
import datetime
import csv
import os

app = Flask(__name__)


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
        server = smtplib.SMTP('smtp.office365.com', 587)  # Hotmail SMTP server
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



@app.route('/sitemap.xml')
def sitemap():
    # Absolute path to sitemap.xml (same folder as server.py)
    sitemap_path = os.path.join(os.path.dirname(__file__), 'sitemap.xml')
    try:
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            xml_data = f.read()
        return Response(xml_data, mimetype='application/xml')
    except Exception as e:
        return f"Error reading sitemap.xml: {e}", 500

@app.route('/robots.txt')
def robots():
    return send_from_directory(os.path.dirname(__file__), 'robots.txt', mimetype='text/plain')


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
    

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(
        directory='static/assets/downloads',
        path=filename,
        as_attachment=True,
        download_name="requirements.txt"  # this sets the downloaded filename
    )


    
if __name__ == '__main__':
    app.run(debug=True)
