#-*- encoding: utf-8 -*-
#author : rayment
#CreateDate : 2013-01-24
import imaplib
import email
#设置命令窗口输出使用中文编码
from imp import reload
import sys
reload(sys)
import time
from datetime import date
from ftplib import FTP
##sys.setdefaultencoding('gbk')

def ftpPutfile(filename):
    ###########FTP开始
    ftp = FTP()
    timeout=60
    port=21
    ftp.connect('xxx.xxx.1xx.xx',port,timeout)
    ftp.login('xxxxxxx','xxxxxxxx') #####用户名，密码
    print(ftp.getwelcome())
    ftp.cwd('/zongcedata')#####设置FTP路径
    print(filename)
    f= open(filename,'rb')
    ##filename = 'RETR '+name
    ##ftp.retrbinary(filename,f.write) ##保存FTP上的文件
    ##name = 'pythonEmail测试.txt'
    ftp.storbinary('STOR '+filename, f) ##上传ftp文件
    ftp.quit()
#保存文件方法（都是保存在指定的根目录下）
def savefile(filename, data, path):
    try:
    filepath = path + filename
    print('Saved as ' + filepath)
    f = open(filepath, 'wb')
    f.write(data)
    f.close()
    print("filename to ftp is:"+filepath)
    ftpPutfile(filepath)
    except:
        print('filename error')
        
   
#字符编码转换方法
def my_unicode(s, encoding):
    if encoding:
        return unicode(s, encoding)
    else:
        return unicode(s)

#获得字符编码方法
def get_charset(message, default="ascii"):
    #Get the message charset
    return message.get_charset()
    return default

#解析邮件方法（区分出正文与附件）
def parseEmail(msg, mypath):
    mailContent = None
    contenttype = None
    suffix =None
    for part in msg.walk():
        if not part.is_multipart():
            contenttype = part.get_content_type()   
            filename = part.get_filename()
            ##print("filename: "+filename)
            charset = get_charset(part)
            ##if charset != None:
            ##    print("charset: "+charset)
            #是否有附件
            if filename !=None:
                h = email.header.Header(filename)
                dh = email.header.decode_header(h)
                fname = dh[0][0]
                encodeStr = dh[0][1]
                ##print(encodeStr)
                if encodeStr != None:
                    ##fname = fname.decode(encodeStr)
                    if charset == None:
                        fname = fname.decode('utf-8').encode('gbk').decode('gbk')
                    else:
                        fname = fname.decode(encodeStr, charset)
                data = part.get_payload(decode=True)
                ##print('Attachment : ' + fname)
                #保存附件
                if fname != None or fname != '':
                    savefile(fname, data, mypath)            
            else:
                if contenttype in ['text/plain']:
                    suffix = '.txt'
                if contenttype in ['text/html']:
                    suffix = '.htm'
                if charset == None:
                    mailContent = part.get_payload(decode=True)
                else:
                    mailContent = part.get_payload(decode=True).decode(charset)         
    return  (mailContent, suffix)

#获取邮件方法
def getMail(mailhost, account, password, diskroot, port = 993, ssl = 1):
    mypath = diskroot ##+ ':\\'
    #是否采用ssl
    if ssl == 1:
        imapServer = imaplib.IMAP4_SSL(mailhost, port)
    else:
        imapServer = imaplib.IMAP4(mailhost, port)
    imapServer.login(account, password)
    imapServer.select()
    #邮件状态设置，新邮件为Unseen
    #Message statues = 'All,Unseen,Seen,Recent,Answered, Flagged'
    resp, items = imapServer.search(None, "Recent")
    number = 1
    for i in items[0].split():
       #get information of email
       resp, mailData = imapServer.fetch(i, "(RFC822)")   
       mailText = mailData[0][1]
       msg = email.message_from_bytes(mailText)
       ls = msg["From"].split(' ')
       strfrom = ''
       ##print(ls[0])
       if(len(ls) == 2 ):
           fromname = email.header.decode_header((ls[0]).strip('\"'))
           if(fromname[0][1] != None):
                 strfrom = 'From : ' + fromname[0][0].decode(fromname[0][1]) + ls[1]
           else:
                 strfrom = 'From : ' + fromname[0][0]
       else:
           strfrom = 'From : ' + msg["From"]
       
       datestr=msg["Date"]
       if(datestr != None):
           strdate = 'Date : ' + msg["Date"]
       else:
           strdate = 'Date : '+date.today().strftime("%y/%m/%d %h")
       ##print(strdate)
       subject = email.header.decode_header(msg["Subject"])
       
       if (len(subject)>=1):
           if(subject[0][1] != None):
              strsub=subject[0][0].decode(subject[0][1])
           else:
              strsub=subject[0][0]
       else:
           strsub=subject[0][0]
       strsub1 = strsub
       strsub = 'Subject : ' + strsub
       
       
       if(  strfrom=="From : fuzixi09@139.com" and strsub=="Subject : zongceftp"):    
           mailContent, suffix = parseEmail(msg, mypath)
           #命令窗体输出邮件基本信息
           ##print('\n')
           print( 'No : ' + str(number))
           print(strfrom)
           print(strdate)
           print(strsub)
           number = number + 1
           #保存邮件正文
           ##if (suffix != None and suffix != '') and (mailContent != None and mailContent != ''):
           ##    savefile(strsub1 + suffix, mailContent, mypath)
       else:
            print('\n'+strsub1+" email is not from fuzixi09@139.com")
           
    imapServer.close()
    imapServer.logout()


if __name__ =="__main__":
    #邮件保存在e盘
    mypath ='d:\\fzxtemp\\'
    print('begin to get email...')
    getMail('imap.139.com', 'fuzixi09@139.com', 'pwword', mypath, 143, 0)
    #126邮箱登陆没用ssl
    #getMail('imap.126.com', 'xxxxxxxxx@126.com', 'xxxxxxxxxx', mypath, 143, 0)
    print('the end of get email.')
