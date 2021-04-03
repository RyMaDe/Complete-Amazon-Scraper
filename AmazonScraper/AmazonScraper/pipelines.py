# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class AmazonscraperPipeline: #Product Search

    def __init__(self):
        self.conn = sqlite3.connect("Scraper.db")
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Search (
            id integer PRIMARY KEY,
            Product text,
            Price float,
            Rating float,
            No_of_Ratings int,
            ASIN text,
            URL text,
            ImageURL text
        )""")

    def add_items(self,item):
        self.cur.execute("""INSERT INTO Search(Product,Price,Ratings,No_of_Ratings,ASIN,URL, ImageURL) VALUES (?,?,?,?,?,?,?)""", ( 
            item["Product"][0],
            item["Price"][0],
            item["Rating"][0],
            item["No_of_Ratings"],
            item["ASIN"][0],
            item["URL"],
            item["ImageURL"][0]
        ))
        self.conn.commit()

    def process_item(self, item, spider):
        self.add_items(item)
        return item

class ASINPipeline: #ASIN description
    def __init__(self):
        self.conn = sqlite3.connect("Scraper.db")
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Description (
            id integer PRIMARY KEY,
            Title text,
            Brand text,
            Description text,
            Price float,
            Rating text,
            No_of_Ratings int,
            ASIN text,
            Colour text,
            Weight text,
            Dimensions text
        )""")

    def add_items(self,item):
        self.cur.execute("""INSERT INTO Description(Title,Brand,Description,Price,Ratings,No_of_Ratings,ASIN,Colour, Weight, Dimensions) VALUES (?,?,?,?,?,?,?,?,?,?)""", (
            item["Title"],
            item["Brand"],
            item["Description"],
            item["Price"][0],
            item["Rating"],
            item["No_of_Ratings"],
            item["ASIN"][0],
            item["Colour"],
            item["Weight"],
            item["Dimensions"]
        ))
        self.conn.commit()

    def process_item(self,item,spider):
        self.add_items(item)
        return item

class ReviewPipeline: # Reviews
    def __init__(self):
        self.conn = sqlite3.connect("Scraper.db")
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Reviews (
            id integer PRIMARY KEY,
            Reviewer text,
            Rating text,
            Title text,
            Date text,
            Verified text,
            Review text,
            Helpful text
        )""")

    def add_items(self,item):
        self.cur.execute("""INSERT INTO Reviews (Reviewer,Rating,Title,Date,Verified,Review,Helpful) VALUES (?,?,?,?,?,?,?)""", (
            item["Reviewer"],
            item["Rating"],
            item["Title"],
            item["Date"],
            item["Verified"],
            item["Review"],
            item["Helpful"]
        ))
        self.conn.commit()

    def process_item(self,item,spider):
        self.add_items(item)
        return item

class BestSellersPipeline: #Best Sellers
    def __init__(self):
        self.conn = sqlite3.connect("Scraper.db")
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS BestSellers (
            id integer PRIMARY KEY,
            Category text,
            Parent_Cat text,
            Position int,
            Price text,
            Product text,
            Ratings text,
            No_of_Ratings text,
            URL text,
            ImageUrl text
        )""")

    def add_items(self,item):
        self.cur.execute("""INSERT INTO BestSellers (Category,Position,Price,Product,Ratings,No_of_Ratings,URL,ImageUrl, Parent_Cat) VALUES (?,?,?,?,?,?,?,?,?)""", (
            item["Category"],
            item["Parent_Cat"],
            item["Position"],
            item["Price"][0],
            item["Product"],
            item["Ratings"],
            item["No_of_Ratings"],
            item["URL"],
            item["ImageUrl"][0]
        ))
        self.conn.commit()

    def process_item(self,item,spider):
        self.add_items(item)
        return item

class DealsPipeline: #Deals
    def __init__(self):
        self.conn = sqlite3.connect("Scraper.db")
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Deals (
            id integer PRIMARY KEY,
            Product text,
            Price text,
            Pre_Price text,
            Rating text,
            No_of_Ratings int,
            Timer text,
            Claimed text,
            URL text,
            IMG_URL text
        )""")

    def add_items(self,item):
        self.cur.execute("""INSERT INTO Deals (Product,Price,Pre_Price,Rating,No_of_Ratings,Timer,Claimed,URL,IMG_URL) VALUES (?,?,?,?,?,?,?,?,?)""",(
            item["Product"],
            item["Price"],
            item["Pre_Price"],
            item["Rating"],
            item["No_of_Ratings"],
            item["Timer"],
            item["Claimed"],
            item["URL"],
            item["IMG_URL"]
        ))
        self.conn.commit()

    def process_item(self,item,spider):
        self.add_items(item)
        return item

class DataVar: #multiprocessing queue - Receive info in list
    def process_item(self, item, spider):
        spider.q.put(dict(item))
        return item

class DataVarList: #multiprocessing list - Receive info in list
    def process_item(self, item, spider):
        spider.q.append(dict(item))
        return item