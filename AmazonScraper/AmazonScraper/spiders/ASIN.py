import scrapy
from ..items import AsinItem

class AsinSpider(scrapy.Spider):
    name = 'asin'
    allowed_domains = ['Amazon.com','Amazon.co.uk']

    def __init__(self, q, url_term="",dom=None):
        if dom=="uk":
            self.start_urls = ['http://Amazon.co.uk/dp/'+url_term]
        else:
            self.start_urls = ['http://Amazon.com/dp/'+url_term]
        self.q = q

    def parse(self, response):
        items = AsinItem()
        result = response.css("div div.a-container")

        try:
            items["Title"] = result.css("h1.a-size-large span.product-title-word-break::text").extract_first().strip("\n")
        except:#books may not show:
            items["Title"] = result.css("h1.a-spacing-none span.a-size-extra-large::text").extract_first().strip("\n")
        try:
            items["Brand"] = result.css("div.centerColAlign div.a-section.a-spacing-none a.a-link-normal::text").extract_first()
            if items["Brand"]!=None:
                items["Brand"]=items["Brand"].replace("Visit the ","").replace(" Store","").replace("Brand: ","")
            else: #Trying an alternative css selector:
                items["Brand"] = result.css("div.a-section.a-spacing-none a.a-link-normal::text").extract_first().replace("Visit the ","").replace(" Store","").replace("Brand: ","")
        except:
            pass
        items["Rating"] = result.css("a.a-popover-trigger i.a-icon-star span.a-icon-alt::text").extract_first()
        items["No_of_Ratings"] = result.css("span.a-declarative a.a-link-normal span.a-size-base::text").extract_first()
        items["Price"] = result.css("td.a-span12 span.a-color-price::text").extract()
        try:
            items["Description"] = result.css("div.a-row.feature div.a-section.a-spacing-small p::text").extract_first().strip("\n")
        except:
            items["Description"] = "N/A"
        items["ASIN"] = result.css("div.centerColAlign div::attr(data-asin)").extract()
        if items["ASIN"]==[]:
            items["ASIN"] = [response.url[-10:]]
        items["Colour"] = result.css("ul.imageSwatches img.imgSwatch::attr(alt)").extract()

        try: #Scraping the product info to get the weight and dimensions
            ProdInfo = result.css("div.a-section div.a-spacing-top-base tr .prodDetSectionEntry::text").extract()
            i = ProdInfo.index("\nItem Weight\n")
            items["Weight"] = result.css("div.a-row.a-spacing-base .prodDetAttrValue::text").extract()[i].strip("\n")
            i = ProdInfo.index("\nProduct Dimensions\n")
            items["Dimensions"] = result.css("div.a-row.a-spacing-base .prodDetAttrValue::text").extract()[i].strip("\n")
        except:
            pass

        #cleaning the data/data validation
        if items["Price"] == []:
            items["Price"] = [0.00]
        else:
            try:
                items["Price"] = list(map(lambda t: float(t[1:].replace(",","")),items["Price"]))
            except:
                pass
        try:
            items["No_of_Ratings"] = int(items["No_of_Ratings"].split(" ")[0].replace(",",""))
        except:
            items["No_of_Ratings"] = 0
        
        items["Colour"]=",".join(items["Colour"]) #Colours will be a list, we need it be a string for sqlite
        
        yield items