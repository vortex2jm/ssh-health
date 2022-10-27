import os
import time
import email
import smtplib
import schedule
from dotenv import load_dotenv
from paramiko import SSHClient, AutoAddPolicy

load_dotenv()

# SSH Client
IP = os.getenv("IP")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Email service
SENDER = os.getenv("SENDER")
RECEIVER = os.getenv("RECEIVER") 
APP_PASSWORD = os.getenv("APP_PASSWORD")
SUBJECT = "PET Virtual Machine"
BODY = "<h3>VM fora do ar</h3>!"

def send_email():
    msg = email.message.Message()
    msg['Subject'] = SUBJECT
    msg['From'] = SENDER
    msg['To'] = RECEIVER
    password = APP_PASSWORD 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(BODY)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print(f'Email enviado para {RECEIVER}')

def main():
  client = SSHClient()
  client.load_system_host_keys()
  client.set_missing_host_key_policy(AutoAddPolicy())

  for i in range(3):
    try:
      client.connect(hostname=IP, username=USERNAME, password=PASSWORD)
      
    except Exception as error:
      if i == 2:
        print("Connection failure!")
        print(error)

        try:
          send_email()
        except Exception as error:
          print("Failure trying to send email")
          print(error)

      else:
        print("Trying again!")
        time.sleep(3)
    else:
      print("Connected Sucefully!")
      break
    finally:
      client.close()
      print("Client closed!")


if __name__ == "__main__":
  schedule.every(1).minutes.do(main)
  while True:
    schedule.run_pending()
    time.sleep(1)
