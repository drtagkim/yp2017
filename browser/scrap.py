from selenium import webdriver as wd
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities as DC
import requests
import re
from bs4 import BeautifulSoup as BS
dcap = dict(DC.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
    "(KHTML, like Gecko) Chrome/15.0.87"
)
class MyPhantomJS(wd.PhantomJS):
    def __init__(self,**args):
        wd.PhantomJS.__init__(self,desired_capabilities=dcap,**args)
        self.set_window_size(1024,768)
class BrowserPlan():
    @classmethod
    def requests(cls,url,params=None):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                    'Connection':'close'}
        if params==None:
            return requests.get(url,headers=headers)
        else:
            return requests.get(url,headers=headers,params=params)
class Selector(BS):
    def __init__(self,req):
        BS.__init__(self,req.content,"lxml")
        self.req=req
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

    