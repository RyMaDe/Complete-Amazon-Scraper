from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from AmazonScraper.AmazonScraper.spiders import Search
from AmazonScraper.AmazonScraper.spiders import ASIN
from AmazonScraper.AmazonScraper.spiders import Review
from AmazonScraper.AmazonScraper.spiders import BestSellers
from AmazonScraper.AmazonScraper.spiders import Deals
from multiprocessing import Process, Queue, Manager
import os

#Making sure we change the settings path so that we can use the settings file.
#It also allows us to access this code from outside of the AmazonScraper path.
#Changes were made in the settings file too regarding the paths.
settings_file_path = "AmazonScraper.AmazonScraper.settings"
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

settings = get_project_settings()
process = CrawlerProcess(settings)

def Search_Pro(term, dom=None, feed = None):
    term = term.replace(" ","+")
    if feed == "csv":
        settings.update({'FEED_FORMAT' : 'csv', 'FEED_URI' : 'result.csv'})
    elif feed == "json":
        settings.update({'FEED_FORMAT' : 'json', 'FEED_URI' : 'result.json'})
    elif feed == "xml":
        settings.update({'FEED_FORMAT' : 'xml', 'FEED_URI' : 'result.xml'})
    elif feed == "sqlite":
        settings.update({'ITEM_PIPELINES' : {'AmazonScraper.AmazonScraper.pipelines.AmazonscraperPipeline': 300}})
    elif feed == "data":
        settings.update({'ITEM_PIPELINES' : {'AmazonScraper.AmazonScraper.pipelines.DataVarList': 300}})

    def execute_crawling(q):
        process.crawl(Search.SearchSpider, q, url_term = term, dom=dom)
        process.start()

    q = Manager().list()
    p = Process(target=execute_crawling, args=(q,))
    p.start()
    p.join()
    results = list(q)
    return results
    #Here data will be a variable list of dicts which can store all of the items so
    #that the user can access them in a variable.

def Search_Asin(asin,dom=None, feed=None):
    if feed == "csv":
        settings.update({'FEED_FORMAT' : 'csv', 'FEED_URI' : 'product.csv'})
    elif feed == "json":
        settings.update({'FEED_FORMAT' : 'json', 'FEED_URI' : 'product.json'})
    elif feed == "xml":
        settings.update({'FEED_FORMAT' : 'xml', 'FEED_URI' : 'product.xml'})
    elif feed == "sqlite":
        settings.update({'ITEM_PIPELINES' : {'AmazonScraper.AmazonScraper.pipelines.ASINPipeline': 300}})
    elif feed == "data":
        settings.update({'ITEM_PIPELINES' : {'AmazonScraper.AmazonScraper.pipelines.DataVar': 300}})

    def execute_crawling(q):
        process.crawl(ASIN.AsinSpider, q, url_term = asin, dom=dom)
        process.start()

    q = Queue()
    p = Process(target=execute_crawling, args=(q,))
    p.start()
    p.join()
    results = [q.get() for i in range(q.qsize())]
    return results

def Reviews(asin, dom=None, pages = None, feed = None):
    if feed == "csv":
        settings.update({'FEED_FORMAT' : 'csv', 'FEED_URI' : 'reviews.csv'})
    elif feed == "json":
        settings.update({'FEED_FORMAT' : 'json', 'FEED_URI' : 'reviews.json'})
    elif feed == "xml":
        settings.update({'FEED_FORMAT' : 'xml', 'FEED_URI' : 'reviews.xml'})
    elif feed == "sqlite":
        settings.update({'ITEM_PIPELINES' : {'AmazonScraper.AmazonScraper.pipelines.ReviewPipeline': 300}})
    elif feed == "data":
        settings.update({'ITEM_PIPELINES' : {'AmazonScraper.AmazonScraper.pipelines.DataVarList': 300}})

    def execute_crawling(q):
        process.crawl(Review.ReviewsSpider, q, ASIN=asin, dom=dom, pages=pages)
        process.start()

    q = Manager().list()
    p = Process(target=execute_crawling, args=(q,))
    p.start()
    p.join()
    results = list(q)
    return results

def Best_Sellers(dom = None, url=None, feed = None, subcat=None):
    if feed == "csv":
        settings.update({'FEED_FORMAT' : 'csv', 'FEED_URI' : 'bestsellers.csv'})
    elif feed == "json":
        settings.update({'FEED_FORMAT' : 'json', 'FEED_URI' : 'bestsellers.json'})
    elif feed == "xml":
        settings.update({'FEED_FORMAT' : 'xml', 'FEED_URI' : 'bestsellers.xml'})
    elif feed == "sqlite":
        settings.update({'ITEM_PIPELINES' : {'AmazonScraper.AmazonScraper.pipelines.BestSellersPipeline': 300}})
    elif feed == "data":
        settings.update({'ITEM_PIPELINES' : {'AmazonScraper.AmazonScraper.pipelines.DataVarList': 300}})

    def execute_crawling(q):
        process.crawl(BestSellers.BestsellersSpider, q, dom=dom, cat_url = url, subcat=subcat)
        process.start()

    q = Manager().list()
    p = Process(target=execute_crawling, args=(q,))
    p.start()
    p.join()
    results = list(q)
    return results

def Deals_List(dom = None, feed = None, pages = None, dep=None):
    if feed == "csv":
        settings.update({'FEED_FORMAT' : 'csv', 'FEED_URI' : 'deals.csv'})
    elif feed == "json":
        settings.update({'FEED_FORMAT' : 'json', 'FEED_URI' : 'deals.json'})
    elif feed == "xml":
        settings.update({'FEED_FORMAT' : 'xml', 'FEED_URI' : 'deals.xml'})
    elif feed == "sqlite":
        settings.update({'ITEM_PIPELINES' : {'AmazonScraper.AmazonScraper.pipelines.DealsPipeline': 300}})
    elif feed == "data":
        settings.update({'ITEM_PIPELINES' : {'AmazonScraper.AmazonScraper.pipelines.DataVarList': 300}})

    def execute_crawling(q):
        process.crawl(Deals.DealsSpider, q, dom=dom, pages = pages, dep=dep)
        process.start()

    q = Manager().list()
    p = Process(target=execute_crawling, args=(q,))
    p.start()
    p.join()
    results = list(q)
    return results