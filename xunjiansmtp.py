#coding=gbk
import cx_Oracle
import time
import sys
import smtplib
import string
from email.mime.text  import MIMEText
from email.mime.multipart import MIMEMultipart


#sys.stdout=outputfile
file1=open("D:\\schema\\123.txt", "w")
sys.stdout = file1

conn=cx_Oracle.connect('username/password@ip/orcl')
c=conn.cursor()
cc=c.execute('select count(*) from camera where substr(pvgname,-20,6) like \'320602\'').fetchall()	
gz=c.execute('select count(*) from camera where substr(pvgname,-20,6) like \'320611\'').fetchall()
kfq=c.execute('select count(*) from camera where substr(pvgname,-20,6) like \'320691\'').fetchall()
qd=c.execute('select count(*) from camera where substr(pvgname,-20,6) like \'320681\'').fetchall()
rd=c.execute('select count(*) from camera where substr(pvgname,-20,6) like \'320623\'').fetchall()
ha=c.execute('select count(*) from camera where substr(pvgname,-20,6) like \'320621\'').fetchall()
hm=c.execute('select count(*) from camera where substr(pvgname,-20,6) like \'320684\'').fetchall()
rg=c.execute('select count(*) from camera where substr(pvgname,-20,6) like \'320682\'').fetchall()
tz=c.execute('select count(*) from camera where substr(pvgname,-20,6) like \'320683\'').fetchall()
c.close()
conn.close()
total=cc[0][0]+gz[0][0]+kfq[0][0]+qd[0][0]+rd[0][0]+ha[0][0]+hm[0][0]+tz[0][0]+rg[0][0]
print ("总点位数：*************************%d********************"   %total)
print ("1:崇川[%d] \t \t2:港闸[%d] \t \t3:开发区[%d] \t\t" %(cc[0][0],gz[0][0],kfq[0][0]))
print ("4:启东[%d] \t \t5:如东[%d] \t \t6:海安[%d] \t\t"%(qd[0][0],rd[0][0],ha[0][0]))
print ("7:海门[%d] \t \t8:通州[%d] \t \t9:如皋[%d] \t\t"%(hm[0][0],tz[0][0],rg[0][0]))

print ("======================================================")
f=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
conn=cx_Oracle.connect('username/password@ip/orcl')
c=conn.cursor()
x1=c.execute('select sysdate-1/24,sysdate from dual ')
a=x1.fetchall()
print ("时间从 %s 到%s " % (a[0][0],a[0][1]))

j={320602:"崇川",320611:"港闸",320691:"开发区",320681:"启东",320623:"如东",320621:"海安",320684:"海门",320682:"如皋",320683:"通州"}
ff=0
for  g in j.keys():
    x1=c.execute('select count(*) from camera where substr(pvgname,-20,6) like \'%d\'' %g) #获取到点位数
    a=x1.fetchall()[0][0]
    x2=c.execute('select count(*) from cameraanalyse where cameraid in (select id from camera where substr(pvgname,-20,6) like \'%d\') and to_char(cameraanalyse.diagtime, \'yyyy-mm-dd HH24:MI:SS\') >to_char(sysdate - 1 / 24, \'yyyy-mm-dd HH24:MI:SS\') and to_char(cameraanalyse.diagtime, \'yyyy-mm-dd HH24:MI:SS\') <to_char(sysdate, \'yyyy-mm-dd HH24:MI:SS\')'  %g ) #已经巡检次数
    b=x2.fetchall()[0][0]
    x3=c.execute('select count(distinct cameraid) from cameraanalyse where cameraid in (select id from camera where substr(pvgname,-20,6) like \'%d\') and to_char(cameraanalyse.diagtime, \'yyyy-mm-dd HH24:MI:SS\') >to_char(sysdate - 1 / 24, \'yyyy-mm-dd HH24:MI:SS\') and to_char(cameraanalyse.diagtime, \'yyyy-mm-dd HH24:MI:SS\') <to_char(sysdate, \'yyyy-mm-dd HH24:MI:SS\')'  %g )#获取已经巡检的点位数
    d=x3.fetchall()[0][0]
    x4=c.execute('select count(distinct cameraid) from cameraanalyse where cameraid in (select id from camera where substr(pvgname,-20,6) like \'%d\') and to_char(cameraanalyse.diagtime, \'yyyy-mm-dd HH24:MI:SS\') >to_char(sysdate - 1 / 24, \'yyyy-mm-dd HH24:MI:SS\') and to_char(cameraanalyse.diagtime, \'yyyy-mm-dd HH24:MI:SS\') <to_char(sysdate, \'yyyy-mm-dd HH24:MI:SS\') and cameraanalyse.diaggeneravalue > \'0\' ' %g)#获取畅通的点位数
    e=float(x4.fetchall()[0][0])
    print ("======================================================")
    if d==0:
        print ("%s还没跑/n" % (j[g]))
        continue
    print("%s: 总次数: %d  已巡检: %d  畅通：%d  不通: %d  未巡检:%d  畅通率 %.2f%% " %(j[g],b,d,e,d-e,a-d,float(e/d*100)))
    print ("======================================================")
    ff=ff+(d-e)
		
c.close()
conn.close()
			
print("不通点位%d" %(ff))

file1.close()

HOST="smtp.126.com"
SUBJECT="畅通率"
TO="xxxxxxxxxxxxxx"
FROM="xxxxxxxxxxxx"
text="Python rules them all"
BODY=string.join((
	"FROM: %s"% FROM,
	"TO:   %s" % TO,
	"Subject: %s" % SUBJECT,
	"",
	text
	),"\r\n")

msg=MIMEMultipart('related')
attach=MIMEText(open("D:\\schema\\123.txt","r").read())
#attach["Content-Type"]="application/octet-sream"
attach["Content-Disposition"]="attachment;filename=\"report.txt\""

msg.attach(attach)

msg['Subject']=SUBJECT
msg['From']=FROM
msg['TO']=TO

server=smtplib.SMTP()
server.connect(HOST,"25")
#servr.starttls()
server.login("email","password")
server.sendmail(FROM, TO ,msg.as_string())
server.quit()

