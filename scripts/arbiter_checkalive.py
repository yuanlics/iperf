import smtplib
from email.mime.text import MIMEText
from email.header import Header

from tcping import Ping

import pathlib
import os
from os.path import join as opj
from dotenv import load_dotenv


load_dotenv('/home/nus/iperf/scripts/.env')
smtp_sender = os.getenv('SMTP_SENDER')
smtp_recver = os.getenv('SMTP_RECVER')
smtp_pwd = os.getenv('SMTP_PWD')


def ping_check(addr, port):
    ping = Ping(host=addr, port=port, timeout=5)
    ping.ping(count=2)


def send_alart(addr, port):
    mail_host = "smtp.126.com"
    mail_user = smtp_sender
    mail_pass = smtp_pwd

    sender = smtp_sender
    receiver = smtp_recver

    message = MIMEText(f'Unresponsive node: {addr}:{port}', 'html', 'utf-8')
    subject = 'ONL trace collection alert - unresponsive node'
    message['Subject'] = Header(subject, 'utf-8')
    message['from'] = smtp_sender
    message['to'] = smtp_recver

    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)  # SMTP port 25
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receiver, message.as_string())
        print("Sent node-fail alart")
    except smtplib.SMTPException as e:
        print("Error: unable to send email", e)


cwd = pathlib.Path(__file__).parent.resolve()
with open(opj(cwd, 'addr_servers.txt')) as f1, open(opj(cwd, 'addr_clients.txt')) as f2:
    nodes = f1.readlines() + f2.readlines()
    nodes = [n.strip().split(':') for n in nodes]
    for addr, ssh_port, iperf_server_port, nodename in nodes:
        if nodename == 'NUS1':
            continue
        try:
            ping_check(addr, ssh_port)
        except Exception as e:
            print('Connection failed:', e)
            send_alart(addr, ssh_port)
