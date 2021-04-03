import scrapy
from ..items import DealsItem

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

class DealsSpider(scrapy.Spider):
    name = 'deals'
    allowed_domains = ['amazon.com', 'amazon.co.uk']
    #To enable there to be a limit of how many pages to crawl we need to keep a count
    count = 1

    def __init__(self, q, dom=None, pages = None,dep=None):
        self.q = q #Loading the multiprocessing list
        self.pages = pages #Page crawl limit
        self.dom=dom
        self.dep = dep #dep should be the same as the text used for each category on the site

        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

        #Deciding which function to use in start_requests() below.
        #If a department was selected it will go to dep_parse(), otherwise it will go to parse().
        if self.dep != None:
            self.noDep = self.dep_parse
        else:
            self.noDep = self.parse

    def start_requests(self):
        if self.dom == "uk":
            url = "https://www.amazon.co.uk/gp/goldbox/"
        else:
            #usa url will be the default
            url = 'https://www.amazon.com/international-sales-offers/b/?ie=UTF8&node=15529609011'

        self.driver.get(url)
        yield scrapy.Request(url=url, callback=self.noDep)

    def dep_parse(self,response):
        time.sleep(3)
        #Below we are loading the names of all the categories
        if self.dom == "uk":
            depts = self.driver.find_elements_by_css_selector("span.a-declarative [class='a-checkbox checkbox a-spacing-micro']")
        else:#USA
            #Need to expand list of all departments on US site
            self.driver.find_element_by_css_selector("div.a-expander-inline-container span.a-expander-prompt").click()
            time.sleep(1)
            depts = self.driver.find_elements_by_css_selector("div.a-expander-inline-container span.a-declarative")

        for dept in depts:
            department = dept.find_element_by_css_selector("label span.a-checkbox-label").text

            #Click the checkbox of the department specified by the user,
            #then go to the parse function to scrape.
            if self.dep == department:
                dept.find_element_by_css_selector("label input").click()
                link=self.driver.current_url

                yield scrapy.Request(link, callback=self.parse, dont_filter=True)
                break

    def parse(self, response):
        time.sleep(10) #Makes sure all the results will show
        results = self.driver.find_elements_by_css_selector("div.a-row div.a-spacing-none.tallCellView")
        #A list that contains all of the sections with a product

        items = DealsItem()
        for result in results:
            try:
                items["Product"] = result.find_element_by_css_selector("a.singleCellTitle span.a-declarative").text
            except:
                items["Product"] = "N/A"
            try:
                items["Price"] = result.find_element_by_css_selector("span.dealPriceText").text
            except:
                items["Price"] = "N/A"
            try:
                items["Pre_Price"] = result.find_element_by_css_selector("span.a-text-strike").text
            except:
                items["Pre_Price"] = "N/A"
            try:
                items["Rating"] = result.find_element_by_css_selector("div.reviewStars a.touchAnchor").get_attribute("aria-label").split(",")[0]
            except:
                items["Rating"] = "N/A"
            try:
                items["No_of_Ratings"] = int(result.find_element_by_css_selector("span.a-declarative span.a-size-small").text)
            except:
                items["No_of_Ratings"] = "N/A"
            try:
                items["Timer"] = result.find_element_by_css_selector("span[role='timer']").text
            except:
                items["Timer"] = "N/A"
            try:
                items["Claimed"] = result.find_element_by_css_selector("div.a-span5 span.a-size-mini").text
            except:
                items["Claimed"] = "N/A"
            try:
                items["URL"] = result.find_element_by_css_selector("a.a-link-normal[href]").get_attribute("href")
            except:
                items["URL"] = "N/A"
            try:
                items["IMG_URL"] = result.find_element_by_css_selector("img[src]").get_attribute("src")
            except:
                items["IMG_URL"] = "N/A"

            yield items

        try:#To go to the last page
            NEXT_PAGE_SELECTOR = "[class='a-text-center'] ul.a-pagination li.a-last a[href]"
            next_page = self.driver.find_element_by_css_selector(NEXT_PAGE_SELECTOR)
            next_link = next_page.get_attribute("href")
            next_page.click()
        except:
            next_page = None

        #This will make sure to continue looping through all pages if a page limit is not set.
        #If a limit is set, it makes sure to stay within the limit.
        if next_page!=None and (self.pages==None or self.count<self.pages):
            self.count+=1
            yield scrapy.Request(response.urljoin(next_link), callback=self.parse, dont_filter=True)
        else:
            self.driver.quit()