import subprocess

def renew_connection():
    popen=subprocess.Popen("ipconfig /release",stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    (a,b)=popen.communicate()
    popen=subprocess.Popen("ipconfig /renew",stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    (a,b)=popen.communicate()
