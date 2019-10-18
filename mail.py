#!/usr/bin/python3

import smtplib
import mysql.connector

smtpUser = 'Email_ID'
smtpPass = 'Yourpassword'

mydb = mysql.connector.connect(host = "localhost", user= "thebjm", passwd = "password", database = "homeSecurity")

mycursor = mydb.cursor()
mycursor.execute('select email_id from logins')

result = mycursor.fetchall()
type(result)
#print (type(result))

#for i in range(len(result)):
#	print(result[i])
	#toAdd = str(result[i])
	#print(toAdd)
	
#toAdd = result
toAdd = 'bhaskarmudoi.bjm@gmail.com'
fromAdd = smtpUser

subject = 'Smart Door Alert !!!!!! '
body = ' There is some unauthorize Access to your Home ! '
header = 'T0: ' + toAdd + '\n' + 'From: ' + fromAdd +'\n' +'Subject: ' + subject


print (header +'\n'+body )

s = smtplib.SMTP('smtp.gmail.com',587)

s.ehlo()
s.starttls()
s.ehlo()

s.login(smtpUser, smtpPass)
s.sendmail(fromAdd, toAdd, header + '\n\n' + body )

s.quit()
