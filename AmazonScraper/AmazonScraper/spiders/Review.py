import scrapy
from ..items import ReviewsItem

class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    allowed_domains = ['Amazon.com','Amazon.co.uk']
    #To enable there to be a limit of how many pages to crawl we need to keep a count
    count = 1

    def __init__(self,q, ASIN, dom = None, pages = None):
        if dom =="uk":
            self.start_urls = ['http://amazon.co.uk/product-reviews/'+ASIN]
        else:
            self.start_urls = ['http://amazon.com/product-reviews/'+ASIN]
        self.q = q
        self.pages = pages #Page crawl limit

    def parse(self, response):
        items = ReviewsItem()

        reviews = response.css("div.a-section.review.aok-relative")

        for review in reviews:
            items["Reviewer"] = review.css("span.a-profile-name::text").extract_first()
            items["Rating"] = review.css("span.a-icon-alt::text").extract_first()
            items["Title"] = review.css("a.review-title-content span::text").extract_first()
            items["Date"] = review.css("span.review-date::text").extract_first()
            items["Verified"] = review.css("div.review-data span.a-size-mini::text").extract_first()
            items["Review"] = review.css("span.review-text span::text").extract_first()
            items["Helpful"] = review.css("div.review-comments span.cr-vote-text::text").extract_first()

            yield items

        #Continue crawling to the last page or to the specified limit.
        if self.pages==None or self.count<self.pages:
            self.count+=1
            next_page = response.css("ul.a-pagination li.a-last a::attr(href)").extract_first()
            if next_page:
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse, dont_filter = True)