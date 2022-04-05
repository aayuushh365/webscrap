import requests  # for http requests
from bs4 import BeautifulSoup  # for web scraping
import smtplib  # for sending the mail
from email.mime.multipart import MIMEMultipart  # for email body
from email.mime.text import MIMEText  # for email body
import datetime  # for system date and time manipulation

now = datetime.datetime.now()

content = ''  # email content placeholder


# extracting hacker news stories

def extract_news(url):  # creating a function to extract news
    print('Extracting Hacker news Stories...')  # to keep user updated printing this message
    cnt = ''  # creating temporary placeholder. this holder is used to assign value to content(line 12)
    cnt += ('<b> CN top Stories: </b>\n' + '<br>' + '-' * 50 + '<br>')    # <b>- for bolding the statement <br>- break
    response = requests.get(url)   # using get function of the request package to get the content of the url and then store it in the response object
    # The content once we get from the get function is actually in  response body HTTP response, which will contain content the actual content that is required for  us which is the content of the webpage.
    content = response.content # here content is the scope in extract_news. so content in line 12 is different from content in line 23
    soup = BeautifulSoup(content,'html.parser')         # here html.parser is used to extract the soup out of content in line 23 from where we got the response

    for i,tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        cnt += ((str(i+1)+' :: '+tag.text + "\n" + '<br>') if tag.text!='More' else '')
    return cnt
cnt = extract_news('https://https://news.ycombinator.com/')
content = content+cnt
content = content + ('<br>------------</br>')                # putting br at the end of the content
content = content + ('<br></br>End of Message!')


# sending the email

print('Composing Email...')

# updating your email details
SERVER = 'smtp.gmail.com'   # your smtp server
PORT = 587 # your port number i.e gmail port no is 587
FROM = ''    # from where you need to send the email
TO = ''     # your email address #can be a python list
PASS = ''  # your email id password

# creating a message body
msg = MIMEMultipart()
#creating email subject line
msg['Subject'] = 'Top News Stories from HN [Automated Email]' + '' + str(now.day) + '-' + str(now.year)
msg['From']  = FROM
msg['To'] = TO
msg.attach(MIMEText(content,'html'))

print('Initialising Server...')
server = smtplib.SMTP(SERVER,PORT)  # here server = smtplib.SMTP SSL('smtp.gmail.com, 465)
server.set_debuglevel(1)   # if there's a problem in connecting to the server, do you want to see the error message 0-no , 1-yes
server.ehlo()  # initiate the server with ehlo
server.starttls()  # start a tls connection which is a secured connection
server.login(FROM,PASS)
server.sendmail(FROM,TO,msg.as_string())

print('Email Sent...')

server.quit()

