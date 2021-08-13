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
4. neo4j. The graph database neo4j is applied in this project since I want to reveal the relatinship of the diseases data I fetched. To enable the connection of
   neo4j database and scrapy framework, the py2neo library is used here. All the settings like host, username and password are all stored in the settings.py file.
   Feel free to modify them based on your own local env.
   To install neo4j:
   - Download and install neo4j graph database. Source: https://neo4j.com/try-neo4j/
   - pip install py2neo





