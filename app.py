import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.middleware.proxy_fix import ProxyFix
from email_service import send_notification_email
from sms_service import send_sms_notification

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-key-for-testing")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/admin')
def admin():
    contacts = []  # Placeholder: no database used
    return render_template('admin.html', contacts=contacts)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')

        contact_info = {
            'name': name,
            'email': email,
            'phone': phone,
            'subject': subject,
            'message': message
        }

        try:
            logging.info(f"Contact form from {name} received")

            # Send email
            email_sent = send_notification_email(contact_info)
            if email_sent:
                logging.info(f"Email sent for {name}")
            else:
                logging.warning(f"Email sending failed for {name}")

            # Send SMS
            sms_sent = send_sms_notification(contact_info)
            if sms_sent:
                logging.info(f"SMS sent for {name}")
            else:
                logging.warning(f"SMS sending failed for {name}")

            flash(f'Thank you {name}! Your message has been received. We will contact you shortly at {phone} or {email}.', 'success')
        except Exception as e:
            logging.error(f"Error handling contact form: {str(e)}")
            flash('There was an error processing your request. Please try again later.', 'danger')

        return redirect(url_for('contact'))

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
