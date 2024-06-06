#Creating an automail sender of process automation log file through email
import psutil
import os
import time
import urllib.request as urllib2
import smtplib
import schedule
from sys import *
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import pandas as pd

def Is_connected():
    try:
        urllib2.urlopen('https://www.google.com',timeout=1)
        return True
    except urllib2.URLError as e:
        return False
    

def Mailsender(filename,time,to):
    try:
        fromaddr="suyashpatil1817@gmail.com"
        toaddr="%s"%to
        msg=MIMEMultipart()
        msg['from']=fromaddr
        msg['to']=toaddr
        body="""
        Hello %s.
        Please find the  attached document which conatin
        log of running process.
        Log file is created at: %s

        This is auto Generated Mail.

        Thanks & Regards,
        Suyash Patil
        """%(toaddr,time)

        Subject="""Process log generated at :%s"""%(time)
        msg['Subject']=Subject
        msg.attach(MIMEText(body,'plain'))
        attachment=open(filename,'rb')
        p=MIMEBase('application','octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition',"attachment ; Filename : %s "%filename)
        msg.attach(p)
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login(fromaddr,"oqss trtc zlqg mlbl")
        text=msg.as_string()
        s.sendmail(fromaddr,toaddr,text)
        s.quit()
        print("Log File Successfuly send !!")



    except Exception as e:
        print("Mail not send",e)

def process_log(logdir="Process_file"):
    listprocess=[]

    if not os.path.exists(logdir):
        try:
            os.mkdir(logdir)
        except:
            pass

    seperator="-"*80
    logpath=os.path.join(logdir,"LOgfile.log")
    f=open(logpath,'w')
    f.write(seperator+"\n")
    f.write("Process Loger : "+ time.ctime()+"\n")
    f.write(seperator+"\n")
    


    
    for proc in psutil.process_iter():
        try:
            pinfo=proc.as_dict(attrs=['pid','name','username'])
            vms=proc.memory_info().vms/(1024*1024)
            pinfo['vms']=vms
            listprocess.append(pinfo)
        
        except(psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
            pass
        
    for elem in listprocess:
        f.write("%s\n"%elem)

    print("Logfile is created successfuly")

    connected=Is_connected()

    if connected:
        starttime=time.time()
        o=pd.read_csv('Contactsp - Sheet1.csv')
        for i in range (len(o)):
            row=o.iloc[i]
            print(row['Email'])
            Mailsender(logpath,time.ctime(),row['Email'])
        endtime=time.time()
        print("Took %s seconds to send mail "%(endtime-starttime))
    else:
        print("There is no internet connection ")

def main():
    print("Application Name :",argv[0])

    if(len(argv)!=2):
        print("Invalid Input ")

    if(argv[1]=="-h" or argv[1]=="-H"):
        print("This Script is used to log record of running process")
        exit()

    if(argv[1]=="-u"or argv[1]=="-U"):
        print("Usage : ApplicationName Absolutepath_directory")
        exit()

    try:
        schedule.every(int(argv[1])).minutes.do(process_log)
        while(True):
            schedule.run_pending()
            time.sleep(1)

    except ValueError:
        print("Error : Invalid Data type of input")

    except Exception as E:
        print("Error:Invalid Input ",E)

if __name__=="__main__":
    main()
