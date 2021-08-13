# OscerSpider

Software Engineer - Web Scraping
Author: Xiaohan Gu

## Intro 
This project is used to crawl diseases data, their associated symptoms, treatment, causes and diagnosis which form a knowledge graph using the graph database neo4j.
The final graph should reveal the realationship between different diseases, symptoms, treatment, causes, diagnosis and you will be able to see their connections.

## Tech Stack
1. Python. The whole project is written in Python.
2. Scrapy framework. Scrapy is the most popular web scraping framewok in the industry. This project applies Scrapy to make schedule, dispatch spiders to their works,
   store in scrapy Items and use the scrapy pipeline to store the final data into local database.
   To install Scrapy:
   - pip install scrapy
   - There might be other prerequisites (install based on your env):
      - pip install wheel
      - pip install Twisted
      - pip install pywin32
3. Selenium. Selenium is applied in this project to simulate some user actions like clicking. With the help of Selenium, our spiders can fetch some hidden content
   from the website.
   To Install Selenium:
   - pip install selenium
