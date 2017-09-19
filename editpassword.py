import paramiko
import threading
from time import sleep, ctime 

ip_list=[]
file = open(r"C:\Users\Administrator\Desktop\pvg.txt")
for line in file:
        line=line.strip('\n')
        line=line.strip()
        ip_list.append(line)
file.close()
v=[]
def ceshi(ip,port,username,password):
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ip,port,username, password)
		stdin, stdout, stderr = ssh.exec_command('echo %s | passwd --stdin root'%(a))
		if stderr.read()=="":
			print ("%s \t 密码修改成功." %(ip))
			v.append("%s \t 密码修改成功." %(ip))
	#except TimeoutError:
	       #print ("%s \t 连接超时"%(ip))
	except paramiko.ssh_exception.AuthenticationException:
	       print ("%s \t 原始密码错误"%(ip))
	       v.append("%s \t 原始密码错误"%(ip))
	except ConnectionRefusedError:
	       print ("%s \t 非linux主机"%(ip))
	       v.append("%s \t 非linux主机"%(ip))
	finally:
		ssh.close()
port=22
username=["root"]
password=["!2ntsj"]
a="!2ntsj"
length=range(len(ip_list))
threads=[]
for i in length:
        t = threading.Thread(target=ceshi,args=(ip_list[i],port,username[0],password[0]))
        threads.append(t)
if __name__ == '__main__':
        for i in length:
                threads[i].start()
        for i in length:
                threads[i].join()
        print "======================================="
        for i in v:
                print i
        
