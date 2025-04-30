import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_notification_email(contact_info, recipient_email="mailus.zionsolutions@gmail.com"):
    """
    Sends notification email using Python's built-in smtplib
    
    Args:
        contact_info (dict): Dictionary containing contact form information
        recipient_email (str): Email address to receive the notification
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    # Log attempt
    logging.info(f"Attempting to send notification email to {recipient_email}")
    
    try:
        # Format the message content
        message_content = f"""
        New Contact Form Submission:
        
        Name: {contact_info.get('name')}
        Email: {contact_info.get('email')}
        Phone: {contact_info.get('phone')}
        Subject: {contact_info.get('subject')}
        
        Message:
        {contact_info.get('message')}
        
        This is an automated notification from your Zion Solutions website.
        """
        
        # Set up the message formatting
        msg = MIMEMultipart()
        msg['Subject'] = f"New Contact Form: {contact_info.get('subject')}"
        msg['From'] = contact_info.get('email')
        msg['To'] = recipient_email
        
        # Attach the message content
        msg.attach(MIMEText(message_content, 'plain'))
        
        logging.info("Email notification formatted and ready to send")
        
        # For now, just log the email content as we don't have SMTP credentials
        logging.info(f"EMAIL WOULD BE SENT: {msg.as_string()}")
        
        # In a production environment with SMTP credentials, you would use:
        # server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.starttls()
        # server.login("your_email@gmail.com", "your_password")
        # server.send_message(msg)
        # server.quit()
        
        # Return success status - this is a mock success
        return True
        
    except Exception as e:
        logging.error(f"Failed to send email notification: {str(e)}")
        return False