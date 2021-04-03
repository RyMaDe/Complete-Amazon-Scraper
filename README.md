# Complete-Amazon-Scraper
Used to scrape search results, product pages, reviews, best sellers and today's deals.

This programme can be plugged into other program via import and the results will be received as a json, csv, xml or sqlite file, or as a variable list of dictionaries which can then be utilised directly in your program.

Notes:

- The below functions should work for the UK and US site.

- When importing this program, it will allow you to perform multiple scrapes through multiprocessing.

- Currently the slowest export method is sqlite, the others are much faster. When using the "data" feed you will receive the results as a list of dictionaries which you can store in a variable.

- The Amazon sites are ever changing and I suspect that this project will need regular updating.

### Requirements
You will only be able to use this program from the command line. You must import this program into your program and then execute your program from the command line.

You will need to install the following for this to work:
- python3 (3.8.5)
- Scrapy (2.3)
- Scrapy-UserAgents (0.0.1)
- Selenium (3.141)

The specific versions mentioned above are not needed but are listed just in case those currently available create errors.

Note Selenium will only be needed when scraping the deals page, in which case you will also need to download the following:
- geckodriver - Store this in the usr/bin folder (or venv/bin folder if using a virtual environment)
- firefox

The program makes use of user agent rotation in the settings file. You may need to add more user agents to this list or update them over time.

## Functions
All of the below functions should work for the US and UK site.
#### Search Products
- This will return a list of products and their details (name, price, no. reviews, avg rating, asin code, url, image url).
- Filters: To add filters to your search results you need to provide the full url of the filtered search results page or the partial url after the .com/.
- This has been made to work with grid and list views of search results

#### Product's Page
- This will provide the details of a product specified by its ASIN code.
- It should provide the title, rating, no of ratings, price, description, colours, weight and dimensions

#### Product's Reviews
- This will provide all of the reviews of a product specified by its ASIN
- Filters: to add filters then you just need to provide the url from the asin onwards once the filters have been applied.
- Limits: A page limit can also be provided if you only want the first few pages.

#### Best Sellers
- This will provide the current best sellers.
- Category: If you want the best sellers for a specific category then you will need to provide the whole url for the category.
- Sub-Category: You can get the best sellers for all sub categories also instead of just the top level category.
 
#### Today's Deals
- This will provide the results from the Today's Deals page.
- Limit: You can specify a page limit here if you only want the results for the first few pages.
- Category: If you would like to only see the deals for a specific category then you just need specify the category as listed on the website (no url needed).
- Uses Selenium - see the requirements above to make the deals page work

### Examples:
#### **Setup**
First you must store your file (the file you will be importing into) in the same directory as the top level AmazonScraper folder found when you download this repo (first folder in the Complete-Amazon-Scraper folder).

        from AmazonScraper import main

#### **Search Products**
        main.Search_Pro("Python textbook", feed = "csv")

The default domain is the US, by specifying the uk you will access the uk site.
    
        main.Search_Pro("Python textbook", feed = "xml", dom = "uk")

For a link:
    
        main.Search_Pro("Enter URL Here in quotes", feed = "data")

#### **Search Single Product**
        main.Search_Asin("Enter ASIN", feed = "sqlite")

Optionally add the below args:

- dom = "uk" - for uk results

#### **Search Reviews**
        main.Reviews("Enter ASIN", feed = "json")

Optionally you can add the below args:
- dom = "uk"	- for uk results
- pages = 3	- This will limit results to the first three pages
- "URL from and including the ASIN onwards"	- This will allow you to add filters to the reviews

#### **Best Sellers**
        main.Best_Sellers(feed = "csv")

Optionally you can add the below args:
- dom = "uk"	- for uk results
- url = "enter full URL"	- This will allow you scrape only a specific category.
- subcat = True	- Thill will include the best sellers of all sub categories in your results rather than just the best sellers for the overall category.

#### **Today's Deals**
        main.Deals_List(feed = "csv")

Optionally you can add the below args:
- dom = "uk"	- for uk results
- pages = 5	- This will the limit the number of scraped pages
- dep = "Musical Instruments"	- This will make sure to scrape only that category rather than all categories.
