import requests # http requests

from bs4 import BeautifulSoup # web scraping
import smtplib # send email

#email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#system date and time manipulation
import datetime

#global objects
now = datetime.datetime.now()
content = ''

def extract_news(url):
    print('Extracting Hacker News Stories...')
    cnt = ''
    cnt +=('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    for i,tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        cnt += ((str(i+1)+' :: '+tag.text+"\n"+"<br>" if tag.text != "More" else ""))
    return(cnt)

cnt = extract_news('http://news.ycombinator.com/')
content += cnt
content += '<br>-------<br>'
content += '<br><br>End of Message'

#print(content)

print ('Composing Email...')

SERVER = 'smtp-mail.outlook.com'
PORT = 587
FROM = 'kwon741@hotmail.com'
TO = 'krnjin94@gmail.com'
PASS = '********' #pw changed

msg = MIMEMultipart()

msg['Subject'] = "Top News Stories HN [Automated EMail]" + str(now.day) + '-' + str(now.year) + '--' + str(now.strftime('%H:%M:%S'))
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

print('Initiating Server...')

server = smtplib.SMTP(SERVER, PORT)

server.set_debuglevel(1) # 1 - see debug messages; 0 - do not see error messages
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()
