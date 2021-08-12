from scrapy import cmdline

cmdline.execute('scrapy crawl mayoclinic -o result.json -t json'.split())