import paramiko
'''
port=22
username=["root"]
password=["!2ntsj","123456"]
a="!2ntsj"
ip=["172.23.13.34"]
test=[]
try:
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip[0],port,username[0], password[0])
	stdin, stdout, stderr = ssh.exec_command('echo %s | passwd --stdin root'%(a))
	if stderr.read()=="":
		print ("%s 密码修改成功." %(ip[0]))
except TimeoutError:
	print ("连接超时")
except paramiko.ssh_exception.AuthenticationException:
	print ("原始密码错误")
except ConnectionRefusedError:
        print ("非linux主机")
finally:
        ssh.close()
        print ("xixihaha")
'''

d=[]
f=[]
file = open(r"C:\Users\Administrator\Desktop\pvg.txt")
for line in file:
        line=line.strip('\n')
        line=line.strip()
        d.append(line)
file.close()


def ceshi(ip,port,username,password):
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ip,port,username, password)
		stdin, stdout, stderr = ssh.exec_command('rpm -e --nodeps `rpm -qa | grep samba`')
		if stderr.read()=="":
			return ("%s \t samba删除成功." %(ip))
		else:
						return ("%s \t 不包含samba"%(ip))
	except TimeoutError:
	       return ("%s \t 连接超时"%(ip))
	except paramiko.ssh_exception.AuthenticationException:
	       return ("%s \t 原始密码错误"%(ip))
	except ConnectionRefusedError:
	       return ("%s \t 非linux主机"%(ip))
	finally:
		ssh.close()
port=22
username=["root"]
password=["!2ntsj"]


for i in d:
        v=ceshi(i,port,username[0],password[0])
        print (v)
        f.append(v)


output = open(r"C:\Users\Administrator\Desktop\result.txt", 'wt')
for i in f:
        output.write(i+'\n')

output.close()
