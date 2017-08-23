# NOTE
# excel sheet 1=review,2=photo_info_in_review
from browser.scrap import *
from excel.excelutil import *
from browser.crawlcontrol import *
from time import sleep
import pandas as pd
from random import uniform
import sys
from threading import Thread
from datetime import datetime
import hashlib
import uuid
class UserProfile:
    css_real_photo=".review-list .review-sidebar img"
    css_name=".review-sidebar .user-name"
    css_real_address=".review-sidebar .user-location b"
    css_passport=".review-sidebar .user-passport-stats"
    css_friend_count=".friend-count b"
    css_review_count=".review-count b"
    css_photo_count=".photo-count b"
    def __init__(self,selector):
        self.selector=selector
        self.get_real_photo()
        self.get_name()
        self.get_passport_stat()
        self.get_real_address()
        self.get_friend_count()
        self.get_review_count()
        self.get_photo_count()
    def get_passport_stat(self):
        selector=self.selector
        self.stats=selector.select(UserProfile.css_passport)
    def get_real_photo(self):
        selector=self.selector
        real_photo=selector.css_attr(UserProfile.css_real_photo,"src")
        #if len(real_photo) == 21:
        real_photo=real_photo[1:]
        self.real_photo=real_photo
    def get_name(self):
        selector=self.selector
        name=selector.css_text(UserProfile.css_name)
        self.name=name
    def get_real_address(self):
        selector=self.selector
        address=selector.css_text(UserProfile.css_real_address)
        self.address=address
    def get_friend_count(self):
        selector=self.selector
        rv=[]
        for s in self.stats:
            friend_count=selector.css_text(UserProfile.css_friend_count)
            if len(friend_count) > 0:
                rv.append(friend_count[0])
            else:
                rv.append('0')
        self.friend_count=rv
    def get_review_count(self):
        selector=self.selector
        rv=[]
        for s in self.stats:
            review_count=selector.css_text(UserProfile.css_review_count)
            if len(review_count) > 0:
                rv.append(review_count[0])
            else:
                rv.append('0')
        self.review_count=rv
    def get_photo_count(self):
        selector=self.selector
        rv=[]
        for s in self.stats:
            photo_count=selector.css_text(UserProfile.css_photo_count)
            if len(photo_count) > 0:
                rv.append(photo_count[0])
            else:
                rv.append('0')
        self.photo_count=rv
class Review:
    css_rating=".review-content .biz-rating .i-stars"
    css_qualified_date=".review-content span.rating-qualifier"
    css_review_content=".review-content"
    css_review_photo=".review-content .photo-box a"
    def __init__(self,selector):
        self.selector=selector
        self.review_id=[]
        self.get_rating()
        self.get_qualified_date()
        self.get_review_content()
        self.get_review_photo()
    def gen_review_id(self):
        self.review_id=[str(uuid.uuid4()) for _ in range(self.num)]
    def get_rating(self):
        selector=self.selector
        rating=selector.css_attr(Review.css_rating,"title",regexp=r"(^[0-9.]+)")
        self.rating=rating
    def get_qualified_date(self):
        selector=self.selector
        qualified_date=selector.css_text(Review.css_qualified_date,regexp=r"(^[0-9]+/[0-9]+/[0-9]+)")
        self.qualified_date=qualified_date
    def get_review_content(self):
        selector=self.selector
        review_contents=selector.select(Review.css_review_content)
        review_content=[]
        for rc in review_contents:
            content=" ".join([item.text for item in rc.select('p')])
            review_content.append(content)
        self.num=len(review_content)
        self.gen_review_id()
        self.review_content=review_content
    def get_review_photo(self):
        selector=self.selector
        photo_cnt=[]
        photo_urls=[]
        photo_urls_str=[]
        for review in selector.select(".review-content"):
            review_photo=review.select(".photo-box a")
            photo_url=["https://www.yelp.com"+i['href'] for i in review_photo]
            photo_cnt.append(len(review_photo))
            photo_urls.append(photo_url)
            photo_urls_str.append(str(photo_url))
        self.photo_cnt=photo_cnt
        self.photo_urls=photo_urls
        self.photo_urls_str=photo_urls_str
class PhotoInReview:
    css_helpful=".voting-stat [rel='helpful'] .count"
    css_not_helpful=".voting-stat [rel='not_helpful'] .count"
    css_photo_url=".main-content-wrap .media .photo-box-img"
    css_photo_caption=".selected-photo-caption"
    def __init__(self,selector,rid):
        self.selector=selector
        self.rid=rid
        self.get_helpful()
        self.get_not_helpful()
        self.get_photo_url()
        self.get_photo_caption()
    def get_helpful(self):
        selector=self.selector
        helpful=selector.css_text(PhotoInReview.css_helpful)
        if len(helpful)==0:
            self.helpful=0
            return
        self.helpful=helpful[0]
    def get_not_helpful(self):
        selector=self.selector
        not_helpful=selector.css_text(PhotoInReview.css_not_helpful)
        if len(not_helpful)==0:
            self.not_helpful=0
            return
        self.not_helpful=not_helpful[0]
    def get_photo_url(self):
        selector=self.selector
        photo_url=selector.css_attr(PhotoInReview.css_photo_url,"src")
        if len(photo_url)==0:
            self.photo_url="NA"
            return
        self.photo_url=photo_url[0]
    def get_photo_caption(self):
        selector=self.selector
        photo_caption=selector.css_text(PhotoInReview.css_photo_caption)
        if len(photo_caption)==0:
            self.photo_caption="NA"
            return
        if photo_caption[0].strip()=="":
            self.photo_caption="NA"
            return
        self.photo_caption=photo_caption[0]
class Scraper:
    def __init__(self):
        pass
# class RequestScraper(Scraper):
    # def __init__(self):
        # Scraper.__init__(self)
    # @classmethod
    # def factory(cls,url):
        # req=BrowserPlan().requests(url)
        # if req.status_code != requests.codes.ok:
            # return None
        # return Selector(req)
class ChromeScraper(Scraper):
    def __init__(self):
        Scraper.__init__(self)
    @classmethod
    def factory(cls,chrome,url,politeness=5):
        chrome.visit(url,politeness=politeness)
        content=chrome.page_source
        return Selector(content)
class Control:
    @classmethod
    def measure_page_length(cls,selector):
        css=".pagination-block .page-of-pages"
        c=re.compile(r"of ([0-9,]+)$")
        page_items=selector.css_text(css)
        if len(page_items) > 0:
            pages=c.findall(page_items[0].strip())
            if len(pages) > 0:
                page=int(pages[0].replace(",",""))
            else:
                page=0
        else:
            page=0
        return page-1
    @classmethod
    def pagination(cls,chrome,target_page):
        current_url=chrome.current_url
        if target_page==0:
            return None
        c=re.compile(r"start=([0-9]+)$")
        try:
            current_page=int(c.findall(current_url)[0])
            cursor=int(current_page/20)
            url=current_url[:current_url.index("?")]
        except:
            cursor=0
            url=current_url
        if cursor == target_page:
            return None
        new_page = cursor+1
        params={"start":new_page*20}
        new_url=url+"?start="+new_page*20
        return new_url
    @classmethod
    def get_hex_code(cls,text):
        m=hashlib.md5()
        m.update(text.encode("utf-8"))
        return m.hexdigest()
def extract_yp(s,chrome,verbose=True,politeness=10):
    user=UserProfile(s)
    review=Review(s)
    i=len(review.photo_cnt)
    photo_frame=[]
    for j in range(i):
        photo_cnt=review.photo_cnt[j]
        rid=review.review_id[j]
        photo_result=[]
        if photo_cnt > 0:
            for purl in review.photo_urls[j]:
                if verbose:
                    sys.stdout.write(".")
                r0=ChromeScraper.factory(chrome,purl,politeness)
                p=PhotoInReview(r0,rid)
                photo_result.append(p)
        photo_frame.append(photo_result)
    if verbose:
        sys.stdout.write("!\n")
    return (user,review,photo_frame)        
def write_output(dir,outfilename,user,review,photo_frame):
    fname=dir+"/"+outfilename+'.xls'
    names=['reivew','photo']
    df_review=pd.DataFrame()
    df_review['user_realPhoto']=user.real_photo
    df_review['user_name']=user.name
    df_review['user_address']=user.address
    df_review['user_friendCount']=user.friend_count
    df_review['user_reviewCount']=user.review_count
    df_review['user_photoCount']=user.photo_count
    df_review['review_Id']=review.review_id
    df_review['review_rating']=review.rating
    df_review['review_qualifiedDate']=review.qualified_date
    df_review['review_reviewContent']=review.review_content
    df_review['review_photoCount']=review.photo_cnt
    df_review['review_photoUrls']=review.photo_urls_str
    df_photo=pd.DataFrame()
    p_review_id=[]
    photo_helpful=[]
    photo_notHelpful=[]
    photo_url=[]
    photo_caption=[]
    for pf in photo_frame:
        p_review_id.extend([p.rid for p in pf])
        photo_helpful.extend([p.helpful for p in pf])
        photo_notHelpful.extend([p.not_helpful for p in pf])
        photo_url.extend([p.photo_url for p in pf])
        photo_caption.extend([p.photo_caption for p in pf])
    df_photo['review_Id']=p_review_id
    df_photo['photo_helpful']=photo_helpful
    df_photo['photo_notHelpful']=photo_notHelpful
    df_photo['photo_url']=photo_url
    df_photo['photo_caption']=photo_caption
    ExcelOutput.export(fname,names,[df_review,df_photo])
def go(dir_name,code_name,url,verbose=True,start=1,end=-1,politeness=10):
    chrome=MyChrome()
    s=ChromeScraper.factory(chrome,url,politeness)
    target=Control.measure_page_length(s)
    i=start
    if verbose:
        print("End page = {}".format(target+1))
    while True:
        fname="{}_{:03d}".format(code_name,i)
        user,review,photo_frame=extract_yp(s,chrome,verbose=verbose,politeness=politeness)
        write_output(dir_name,fname,user,review,photo_frame)
        if verbose:
            print("[{}] page_{:04d}".format(str(datetime.now()),i))
        #pagination
        new_url=Control.pagination(s,chrome,target)
        if new_url == None:
            break
        s=ChromeScraper.factory(chrome,new_url,politeness)
        #control
        if end > 0 and i==end:
            break
        i+=1
    chrome.close()
    print("done")