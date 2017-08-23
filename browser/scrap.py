from selenium import webdriver as wd
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities as DC
import requests
import re
from bs4 import BeautifulSoup as BS
from random import uniform
from time import sleep
dcap = dict(DC.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
    "(KHTML, like Gecko) Chrome/15.0.87"
)
SLEEP_BUFF=5
class MyPhantomJS(wd.PhantomJS):
    def __init__(self,**args):
        wd.PhantomJS.__init__(self,desired_capabilities=dcap,**args)
        self.set_window_size(1024,768)
class MyChrome(wd.Chrome):
    def __init__(self,**kargs):
        wd.Chrome.__init__(self,**kargs)
    def visit(self,url,politeness=5):
        sleep(politeness+uniform(0,SLEEP_BUFF))
        self.get(url)
class BrowserPlan():
    @classmethod
    def requests(cls,url,params=None,politeness=5):
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                    'Connection':'close'}
        sleep(politeness+uniform(0,SLEEP_BUFF))
        if params==None:
            return requests.get(url,headers=headers)
        else:
            return requests.get(url,headers=headers,params=params)
class Selector(BS):
    def __init__(self,content):
        BS.__init__(self,content,"lxml")
    def css_text(self,css,regexp=None):
        if regexp != None:
            cp=re.compile(regexp)
        results=[]
        try:
            items=self.select(css)
        except:
            return results
        for item in items:
            a=item.text.strip()
            if regexp != None:
                try:
                    a=cp.findall(a)[0]
                except:
                    pass
            results.append(a)
        return results
    def css_attr(self,css,attr,regexp=None):
        if regexp != None:
            cp=re.compile(regexp)
        results=[]
        try:
            items=self.select(css)
        except:
            return results
        for item in items:
            try:
                a=item[attr].strip()
                if regexp != None:
                    try:
                        a=cp.findall(a)[0]
                    except:
                        pass
                results.append(a)
            except:
                results.append("")
        return results

    