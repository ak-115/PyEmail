import imaplib, smtplib, dns.resolver
from validate_email_address import validate_email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email import message_from_bytes

def actually_read_email(email_id, email, password):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email, password)
        mail.select("INBOX")
        email_info = {}
        data=mail.fetch(email_id,"(RFC822)")
        msg=message_from_bytes(data[0][1])
        # to
        print(msg.get('From'))
    except Exception as e:
        print(f"An error occurred: {str(e)}")
"""
def actually_read_email(email_id, email, password):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email, password)
        mail.select("INBOX")
        email_info = {}

        # to
        _, to_data = mail.fetch(email_id, "(BODY[HEADER.FIELDS (TO)])")
        _, to_header = to_data[0]
        to_header=(str(to_header)).split()
       
        to_val=0
        for l in to_header:
            if '@' in l:
                to_val=l
        try:
            i,j= to_val.index('<'),to_val.index('>')
        except:
            i,j=-1,to_val.index("\\")
    
        to_val=to_val[i+1:j]
        email_info["To"] = to_val 

        # from
        _, from_data = mail.fetch(email_id, "(BODY[HEADER.FIELDS (FROM)])")
        _, from_header = from_data[0]
        from_header=((str(from_header))).split()
        from_val=0
        
        for l in from_header:
            if '@' in l:
                from_val=l
        try:
            i,j= from_val.index('<'),from_val.index('>')
        except:
            i,j=-1,from_val.index("\\")
        from_val=from_val[i+1:j]
        email_info["From"] = from_val 
       
        # subject    
        _, sub_data = mail.fetch(email_id, "(BODY[HEADER.FIELDS (SUBJECT)])")
        _, sub_header = sub_data[0]
        sub_header = sub_header.decode('utf-8')
    
        i= sub_header.find('"')
        j=sub_header.find('"',i+1)
        sub_header=sub_header[i+1:j]
        sub_header=sub_header.replace("Subject: ", "")
        sub_header=sub_header.rstrip()
        email_info["Subject"] = sub_header
        
        # date
        _, date_data = mail.fetch(email_id, "(BODY[HEADER.FIELDS (DATE)])")
        _, date_header = date_data[0]
        date_header=date_header.decode('utf-8')
        
        email_info["Date"] = date_header[6:].rstrip()
        
        print("Email ID:", email_id.decode())
        print("-" * 50)
        for key, value in email_info.items():
            print(f"{key}: {value}")
        print("-" * 50 + "\n")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
"""
def read_emails(email, password):

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email, password)
    mail.select("INBOX")
    _, data = mail.search(None, "ALL")

    if data:
        email_ids = data[0].split()
        num_emails = len(email_ids)
        i=0
        email_id=email_ids[i]
        actually_read_email(email_id, email, password)
        while True:
            choice = input(f"'p' for previous email, 'n' for next email or simply enter the email no. (1 to {num_emails}, 'e' for exit")
            cisnum=False
            try:
                choici = int(choice)-1
                cisnum=True
                if choici not in range(1,num_emails):
                    print("Out of range")
                    cisnum=False
            except:
                pass
            if choice.lower() == 'p':
                i=i-1
            elif choice.lower() == 'n':
                i=i+1
                pass  
            elif cisnum:
                i=choici
            elif choice.lower()=='e':
                break
            else:
                i=i

            email_id=email_ids[i]
            actually_read_email(email_id, email, password)

    else:
        print("No emails found.")
       
    mail.logout()


def validate_email_address(email):
    if validate_email(email):
        return True
    else:
        return False
    
def split_id(email):
    parts = email.split("@")
    username = parts[0]
    domain = parts[1]
    print("username:",username)
    print("domain:", domain)

def validate_dmx(email):
    parts = email.split("@")
    domain = parts[1]
    
    try:
        # Query the MX records for the domain
        answers = dns.resolver.resolve(domain, 'MX')
        if len(answers) > 0:
            return True
        else:
            return False
    except dns.resolver.NoAnswer:
        return False        
    except dns.resolver.NXDOMAIN:
        return False
    except dns.resolver.Timeout:
        return False

def send_email(receiver_email, subject, message, smtp_server, smtp_port, username, password,attachment_path):

    
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html'))

    with open(attachment_path, 'rb') as attachment:
        attachment_part = MIMEApplication(attachment.read())

    attachment_part.add_header('Content-Disposition', 'attachment', filename='asset.png')

    msg.attach(attachment_part)
    
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        
        server.login(username, password)
        server.send_message(msg)
        
    print("Email sent successfully!")

def trylogin(email,password,controller,DoWhatPage,log_var,email_entry,password_entry):

    if validate_email_address(email):        
        if validate_dmx(email):
            parts = email.split("@")
            domain = parts[1]
            mail = imaplib.IMAP4_SSL(f"imap.{domain}")
            mail.login(email, password)
            controller.show_frame(DoWhatPage)
            log_var.set("")
            email_entry.delete(0, 'end')
            password_entry.delete(0, 'end')
            mail.logout()
            
            return True
        else:
            log_var.set("Failed to login")
            return False

    else:
        log_var.set("Failed to login")
        return False
    
def splitandverify(email,nameval,domval,fail):
    if validate_email_address(email):
        if validate_dmx(email):
            parts = email.split("@")
            nameval.configure(text=parts[0])
            domval.configure(text=parts[1])
            fail.configure(text="Sliced successfully")
        else:
            fail.configure(text="Invalid email")
            
    else:
        fail.configure(text="Invalid email")
            