from email.mime.text import MIMEText
import json
import smtplib as SMTP
import credentials as creds

def build_message(arr):
	arr.sort()
	
	message = ''' Gizmo has downloaded the following items to be read.
Please enjoy them at your leisure
-----------------------------------
	 '''
	
	for i in arr:
		message = message + i + ''',
'''
	
	message = message + '''	-----------------------------------
	
	Until next time.'''
	
	return message
		
def alert_of_downloads(message):
	msg = MIMEText(message, 'plain')
	msg['Subject'] = "Manga Downloads"
	me =creds.login['email']
	msg['To'] = 'j.nagelxz@gmail.com'
	recipients = [me]
	try:
		conn = SMTP.SMTP('smtp.mailgun.org', 587)
		conn.ehlo()
		conn.starttls()
		conn.ehlo()
		conn.login(creds.login['email'], creds.login['password'])
		try:
			conn.sendmail(me, recipients, msg.as_string())
		finally:
			conn.close()

	except:
		print ('failed to send')
