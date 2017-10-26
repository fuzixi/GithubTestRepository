# -*- coding: utf-8 -*-
import smtplib 
import pdb
import time
from datetime import date
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.application import MIMEApplication
from ftplib import FTP
#######FTP连接
ftp = FTP()
timeout=60
port=21
ftp.connect('10.48.190.5',port,timeout)
ftp.login('broadband','Hlw@2016') #####用户名，密码
print(ftp.getwelcome())
##ftp.cwd('file/test')#####设置FTP路径
name = "ftptest.sh"
path='d:/fzxtemp/专题工作/python script/'+name
f= open(path,'wb')
filename = 'RETR '+name
ftp.retrbinary(filename,f.write) ##保存FTP上的文件
##name = 'pythonEmail测试.txt'
##ftp.storbinary('STOR '+name, open(path,'rb')) ##上传ftp文件
ftp.quit()




########发送下载的文件
_user = "fuzixi09@139.com"
_pwd = "fuzixi0605"
_to  = "fuzixi09@139.com"
   
#如名字所示Multipart就是分多个部分 
msg = MIMEMultipart() 
msg["Subject"] = "zongceftp"
msg["From"]  = _user 
msg["To"]   = _to

   
#---这是文字部分--- 
part = MIMEText("python email send test") 
msg.attach(part) 
   
#---这是附件部分--- 
#xlsx类型附件 
part = MIMEApplication(open(name,'rb').read()) 
part.add_header('Content-Disposition', 'attachment', filename=name) 
msg.attach(part)  
###pdb.set_trace() 
try:   
	s = smtplib.SMTP("smtp.139.com", timeout=30)#连接smtp邮件服务器,端口默认是25 
	s.login(_user, _pwd)#登陆服务器 
	s.sendmail(_user, _to, msg.as_string())#发送邮件 
	s.close()
	print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")

