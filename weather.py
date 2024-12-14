from datetime import datetime
import tkinter as tk
import re
import pyfiglet
import requests.exceptions
from termcolor import colored
from requests_html import HTMLSession
from email.message import EmailMessage
import ssl
import smtplib


# These are all the packages we used in running the program
class weather:
    def __init__(self, url, temp, query, unit, desc, formatted_datetime, body, em):
        self.url = url
        self.temp = temp
        self.query = query
        self.unit = unit
        self.desc = desc
        self.formatted_datetime = formatted_datetime
        self.body = body
        self.em = em

        # a class that holds instance of the url,temp,unit,and decription,basically allows

    def current(self):
        while True:
            try:
                s = HTMLSession()
                while True:
                    self.query = input(" Enter City :")
                    if re.match("^[a-zA-Z]+$", self.query):
                        self.url = url = f'https://www.google.com/search?q=weather+{self.query}'
                        r = s.get(url, headers={
                            'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'})
                        self.temp = r.html.find('span#wob_tm', first=True).text
                        self.unit = (r.html.find('div.vk_bk.wob-unit span.wob_t', first=True).text)
                        self.desc = r.html.find('div.VQF4g', first=True).find('span#wob_dc', first=True).text
                        return True

                    else:
                        print("please input cities only")
                        continue

            except AttributeError:
                print("please enter a valid city")
                continue
            except requests.exceptions.RequestException:
                print("connect to the internet !")
                continue

    # This is responsible for retrieving the current weather details using google

    def send_mail(self):
        email_sender = 'techdave683@gmail.com'
        current = datetime.now().strftime("%H:%M")
        email_password = 'dhuo wrps dxui tqgd'
        try:
            while True:
                email_reciever = input("Enter Email Address !")
                if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$',
                            email_reciever):  # we used regular expression here to make sure only appropraie email address are entered
                    subject = "weather report"
                    self.body = f"{self.query, self.temp, self.unit} with {self.desc}, current time is, {current}"
                    self.em = EmailMessage()
                    self.em['From'] = email_sender
                    self.em['To'] = email_reciever
                    self.em['Subject'] = subject
                    self.em.set_content(self.body)
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.sendmail(email_sender, email_reciever, self.em.as_string())
                        print(f"Succesfully sent weather report to {email_reciever}")
                        break

                else:
                    print("Enter an Email address in the right format")
                    continue
        except smtplib.SMTPException:
            return "Email address does not exist !!"

        #This function is responsible for sending an email in this instance we are sending the weather details to the email as the message

    def send_to_phone(self):
        try:
            while True:
                phone_number = input("enter phone number: ")
                if re.match(r"^[0-9]{10}$", phone_number):
                    self.resp = requests.post('https://textbelt.com/text', {
                        'phone': phone_number,
                        'message': self.body,
                        'key': 'textbelt', })
                    break
                else:
                    print("enter a valid number of 10 digits and of numbers only")
                    continue
        except Exception:
            print("TEXTBELT IS DOWN TRY AGAIN")


def final_run():
    header = pyfiglet.figlet_format("WELCOME TO WEATHER CLOUD", font="small")
    header = colored(header, color="magenta")
    print(header)
    donecheck = weather1.current()
    if donecheck:
        print("Do you want to get the weather information to your email address or to your phone number !")
        while True:
            ques = input("enter 1 to send to your phone number and 2 for to your email address: ")
            if re.match(r"^[12]$", ques):
                if ques == "1":
                    weather1.send_to_phone()
                    break
                else:
                    weather1.send_mail()
                    break
            else:
                print("enter 1 or 2!  ")
                continue


# This is the final function, and it is responsible for calling the other functions


weather1 = weather("url", "temp", "query", "unit", "desc", "datetime", "body", "em")
final_run()
