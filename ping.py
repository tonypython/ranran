#encoding=gbk
import os,sys
import subprocess,cmd
import threading
from time import sleep, ctime
import time
import smtplib
import string
from email.mime.text  import MIMEText
from email.mime.multipart import MIMEMultipart

d=[]
file1 = open(r"C:\Users\Administrator\Desktop\pvg.txt")
for line in file1:
        line=line.strip('\n')
        line=line.strip()
        d.append(line)
file1.close()
v=[]
def ping(ip):
    ipcommand= str('ping -n 4 -w 1000 %s ' %ip)
    result=subprocess.call(ipcommand,stdout=subprocess.PIPE,shell=True)

    if result==1:
        v.append("%s \t不通"%ip)
    else:
        #v.append("%s \t畅通"%ip)
        pass

length=range(len(d))
threads=[]
for i in length:
        t = threading.Thread(target=ping,args=(d[i],))
        threads.append(t)
if __name__ == '__main__':
        for i in length:
                threads[i].start()
        for i in length:
                threads[i].join()

if len(v):    
    file2=open("d:\\schema\\iperror.txt","w")
    
    v.insert(0,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    for i in v:
        file2.write(i)
        file2.write('\n')
    file2.close()
    
    HOST="smtp.126.com"
    SUBJECT="不畅通ip"
    TO="xxxxxxx"
    FROM="xxxxx"
    #text="Python rules them all"
    #BODY=string.join((
    #        "FROM: %s"% FROM,
    #       "TO:   %s" % TO,
    #        "Subject: %s" % SUBJECT,
    #        "",
    #        text
    #       ),"\r\n")

    msg=MIMEMultipart('related')
    attach=MIMEText(open("D:\\schema\\iperror.txt","r").read())
    #attach["Content-Type"]="application/octet-sream"
    attach["Content-Disposition"]="attachment;filename=\"iperror.txt\""

    msg.attach(attach)

    msg['Subject']=SUBJECT
    msg['From']=FROM
    msg['TO']=TO

    server=smtplib.SMTP()
    server.connect(HOST,"25")
    #servr.starttls()
    server.login("username","password")
    server.sendmail(FROM, TO ,msg.as_string())
    server.quit()

else:
    sys.exit(0)
