from browser.scrap import *
class UserProfile:
    css_real_photo=".review-list .review-sidebar img"
    css_name=".review-sidebar .user-name"
    css_real_address=".review-sidebar .user-location b"
    css_friend_count=".review-sidebar .user-passport-stats .friend-count b"
    css_review_count=".review-sidebar .user-passport-stats .review-count b"
    css_photo_count=".review-sidebar .user-passport-stats .photo-count b"
    def __init__(self,selector):
        self.selector=selector
    def get_real_photo(self):
        selector=self.selector
        real_photo=selector.css_attr(UserProfile.css_real_photo,"src")
        if len(real_photo) == 21:
            real_photo=real_photo[1:]
        return real_photo
    def get_name(self):
        selector=self.selector
        name=selector.css_text(UserProfile.css_name)
        return name
    def get_real_address(self):
        selector=self.selector
        address=selector.css_text(UserProfile.css_real_address)
        return address
    def get_friend_count(self):
        selector=self.selector
        friend_count=selector.css_text(UserProfile.css_friend_count)
        return friend_count
    def get_review_count(self):
        selector=self.selector
        review_count=selector.css_text(UserProfile.css_review_count)
        return review_count
    def get_photo_count(self):
        selector=self.selector
        photo_count=selector.css_text(UserProfile.css_photo_count)
        return photo_count
class Review:
    css_rating=".review-content .biz-rating .i-stars"
    css_qualified_date=".review-content span.rating-qualifier"
    css_review_content=".review-content"
    css_review_photo=".review-content .photo-box a"
    def __init__(self,selector):
        self.selector=selector
    def get_rating(self):
        selector=self.selector
        rating=selector.css_attr(Review.css_rating,"title",regexp=r"(^[0-9.]+)")
        return rating
    def get_qualified_date(self):
        selector=self.selector
        qualified_data=selector.css_text(Review.css_qualified_date,regexp=r"(^[0-9]+/[0-9]+/[0-9]+)")
        return qualified_data
    def get_review_content(self):
        selector=self.selector
        review_contents=selector.select(Review.css_review_content)
        results=[]
        for rc in review_contents:
            content=" ".join([item.text for item in rc.select('p')])
            results.append(content)
        return results
    def get_review_photo(self):
        selector=self.selector
        photo_cnt=[]
        photo_urls=[]
        for review in selector.select(".review-content"):
            review_photo=review.select(".photo-box a")
            photo_url=["https://www.yelp.com"+i['href'] for i in review_photo]
            photo_cnt.append(len(review_photo))
            photo_urls.append(photo_url)
        return (photo_cnt,str(photo_urls),)
class PhotoInReview:
    css_helpful=".voting-stat [rel='helpful'] .count"
    css_not_helpful=".voting-stat [rel='not_helpful'] .count"
    css_photo_url=".main-content-wrap .media .photo-box-img"
    css_photo_caption=".selected-photo-caption"
    def __init__(self,selector):
        self.selector=selector
    def get_helpful(self):
        selector=self.selector
        helpful=selector.css_text(PhotoInReview.css_helpful)
        if len(helpful)==0:
            return 0
        return helpful[0]
    def get_not_helpful(self):
        selector=self.selector
        not_helpful=selector.css_text(PhotoInReview.css_not_helpful)
        if len(not_helpful)==0:
            return 0
        return not_helpful[0]
    def get_photo_url(self):
        selector=self.selector
        photo_url=selector.css_attr(PhotoInReview.css_photo_url,"src")
        if len(photo_url)==0:
            return "NA"
        return photo_url[0]
    def get_photo_caption(self):
        selector=self.selector
        photo_caption=selector.css_text(PhotoInReview.css_photo_caption)
        if len(photo_caption)==0:
            return "NA"
        if photo_caption[0].strip()=="":
            return "NA"
        return photo_caption[0]
class Scraper:
    def __init__(self):
        pass
class RequestScraper(Scraper):
    def __init__(self):
        Scraper.__init__(self)
    def factory(cls,url):
        req=BrowserPlan().requests(url)
        if req.status_code != requests.codes.ok:
            return None
        return Selector(req)
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
    def pagination(cls,selector,target_page):
        req=selector.req
        current_url=req.url
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
        return BrowserPlan.requests(url,params=params)
def test():
    ur1="https://www.yelp.com/biz/shaking-crab-new-york-4"
    s=RequestScraper().factory(url1)
    u=UserProfile(s)
    review=Review(s)
    url2="https://www.yelp.com/biz_photos/shaking-crab-new-york-4?select=pbe8R3mrdtVsNGQKVN7EJQ"
    r=RequestScraper().factory(url2)
    p=PhotoInReview(r)
    url3="https://www.yelp.com/biz_photos/shaking-crab-new-york-4?select=5tDdn5SLyazzbjQnWMR13Q"
def test2():
    #pagination
    url='https://www.yelp.com/biz/babbo-new-york'
    r0=BrowserPlan.requests(url)
    s0=Selector(r0)
    target=Control.measure_page_length(s0)
    while True:
        r0=Control.pagination(s0,target)
        if r0 == None:
            break
        s0=Selector(r0)
        print(r0.url)
    print("done")