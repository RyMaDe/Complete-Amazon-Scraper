import scrapy
from ..items import BestSellersItem

class BestsellersSpider(scrapy.Spider):
    name = 'bestsellers'
    allowed_domains = ['amazon.com','amazon.co.uk']

    def __init__(self, q, dom=None, cat_url=None, subcat=None):
        self.q = q
        self.dom = dom
        self.cat_url = cat_url
        self.subcat = subcat
        self.start_requests()

    def start_requests(self):
        if self.cat_url != None: #To filter by category the user should enter the filtered url
            if self.subcat == True:
                yield scrapy.Request(url = self.cat_url, callback = self.parse_subcat)
            else:
                yield scrapy.Request(url = self.cat_url, callback = self.parse_cat)
        elif self.dom == "uk":
            url = 'https://www.amazon.co.uk/Best-Sellers/zgbs/'
            yield scrapy.Request(url=url, callback = self.parse)
        else:
            url = 'https://www.amazon.com/Best-Sellers/zgbs/'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.css("div ul ul li a::attr(href)").extract()
        if self.dom != "uk":
            links.append("https://www.amazon.com/Best-Sellers-MP3-Downloads/zgbs/dmusic/digital-music-album/")
        #Need to append the music link as it must be accessed differently
        for link in links:
            if self.subcat == True:
                #Selecting between whether we are scraping only the department best sellers (parse.cat)
                #or the sub department best sellers also (parse_subcat).
                yield scrapy.Request(link, callback=self.parse_subcat)
            else:
                yield scrapy.Request(link, callback=self.parse_cat)

    def parse_subcat(self,response): 
        #parsing the sub categories and passing the response to be scraped
        links = response.css("div.a-fixed-left-grid-col ul ul ul li a::attr(href)").extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_cat)

    def parse_cat(self,response):
        item = BestSellersItem()

        page = response.css("div.a-fixed-left-grid-col")
        item["Category"] = page.css("h1.a-size-large span.category::text").extract_first()
        if item["Category"] == "": #Certain sub categories may not show with the above selector
            item["Category"] = page.css("ul ul ul li span::text").extract_first()

        if self.subcat == True:
            item["Parent_Cat"] = page.css("ul ul li a::text").extract_first()

        products = page.css("ol.a-ordered-list li.zg-item-immersion")
        for product in products:
            item["Position"] = product.css("span span.zg-badge-text::text").extract_first()
            try:
                #some items are no longer be available whilch will cause an error here
                item["Product"] = product.css("a.a-link-normal div.p13n-sc-truncate::text").extract_first().strip()
            except:
                item["Product"] = None
            item["Price"] = product.css("span.p13n-sc-price::text").extract()
            item["ImageUrl"] = product.css("img::attr(src)").extract()
            item["URL"] = product.css("span a.a-link-normal::attr(href)").extract_first()
            item["Ratings"] = product.css("i.a-icon-star span.a-icon-alt::text").extract_first()
            item["No_of_Ratings"] = product.css("a.a-size-small.a-link-normal::text").extract_first()

            if item["Price"] == []:
                item["Price"] = ["0"]

            if item["Position"] !="":
                item["Position"] = int(item["Position"][1:])

            yield item

        next_page = response.css("ul.a-pagination li.a-last a::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse_cat)