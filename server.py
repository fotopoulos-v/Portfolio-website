from flask import Flask, render_template, url_for, request, redirect
import datetime
import csv

app = Flask(__name__)

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
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting = csv.QUOTE_MINIMAL)
        csv_writer.writerow([datetime.datetime.now().strftime('Date: %d/%m/%Y, Time: %H:%M:%S'),email,subject,message])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/form_submitted.html')
        except:
            return 'did not save to database'
    else:
        return "something went wrong"
    
    
if __name__ == '__main__':
    app.run(debug=True)