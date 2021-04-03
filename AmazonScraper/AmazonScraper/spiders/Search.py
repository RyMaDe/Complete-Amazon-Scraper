import scrapy
from ..items import AmazonscraperItem

class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['amazon.com', 'amazon.co.uk']

    def __init__(self, q, url_term = "", dom=None):
        if dom == "uk":
            self.start_urls = ["https://www.amazon.co.uk/s?k="+url_term]
        else:
            self.start_urls = ["https://www.amazon.com/s?k="+url_term]

        self.q = q

    def parse(self, response):
        items = AmazonscraperItem()

        results = response.css("div.s-main-slot .s-result-item.s-asin.sg-col-0-of-12")
        if results.css(".a-size-medium::text").extract_first() == None: #checking if the product name shows in listview
            results = response.css("div.s-main-slot .s-result-item.s-asin.sg-col-4-of-12") #Check the gridview if it doesn't

        for result in results:
            items["Product"] = result.css(".a-size-medium::text").extract()
            if items["Product"] == []: 
                items["Product"] = result.css(".a-size-base-plus::text").extract()
            items["Price"] = result.css(".a-offscreen::text").extract()
            items["Rating"] = result.css(".a-icon-alt::text").extract()
            items["No_of_Ratings"] = result.css("a.a-link-normal span.a-size-base::text").extract_first()
            items["ASIN"] = result.css("div::attr(data-asin)").extract()
            items["URL"] = result.css("h2.a-size-mini.a-spacing-none a.a-link-normal.a-text-normal ::attr(href)").extract_first()
            items["ImageURL"] = result.css("img.s-image ::attr(src)").extract()

            #cleaning the data/data validation
            if items["Price"] == []:
                items["Price"] = [0.00]
            else:
                items["Price"] = list(map(lambda t: float(t[1:].replace(",","")),items["Price"]))

            if items["Rating"] == []:
                items["Rating"] = ["N/A"]
            try:
                items["No_of_Ratings"] = int(items["No_of_Ratings"].replace(",",""))
            except:
                items["No_of_Ratings"] = 0

            yield items

        NEXT_PAGE_SELECTOR = 'ul.a-pagination li.a-last a::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()

        if next_page:
            #print("++++++++++++++++++++++++++++++++++Testing++++++++++++++++++++++++++++++")
            #print(response.urljoin(next_page))
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)