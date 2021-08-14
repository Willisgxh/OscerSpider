import scrapy
from ..items import OscerSpiderItem, OscerSymptomsItem
from selenium import webdriver
from scrapy.http import HtmlResponse


class mayoClinicSpider(scrapy.Spider):
    name = 'mayoclinic'
    allowed_domains = ['www.mayoclinic.org']
    chrome_driver = webdriver.Chrome('chromedriver.exe')

    # start_urls = ['https://www.mayoclinic.org/diseases-conditions/index?letter=0']
    start_urls = ['https://www.mayoclinic.org/symptoms/index?letter=A']
    # for i in range(26):
    #     url = 'https://www.mayoclinic.org/diseases-conditions/index?letter=' + chr(65 + i)
    #     start_urls.append(url)

    def parse(self, response):
        if response.url[27] == 's':
            # Fetch Symptoms
            index = 1
            symptoms_item = OscerSymptomsItem()
            while True:
                symptoms_xpath = '//*[@id="index"]/ol/li[' + str(index) + ']/a/text()'
                current_symptom = response.xpath(symptoms_xpath).get()
                if not current_symptom:
                    break
                print(current_symptom)
                symptoms_item['Symptoms'] = current_symptom
                index += 1
                yield symptoms_item
            if ord(response.url[-1]) < 90:
                url = response.url[:-1] + chr(ord(response.url[-1]) + 1)
                yield scrapy.Request(url, callback=self.parse)
            else:
                url = 'https://www.mayoclinic.org/diseases-conditions/index?letter=0'
                yield scrapy.Request(url, callback=self.parse)
        elif response.url[27] == 'd':
            # Fetch diseases
            index = 1
            while True:
                xpath = '//*[@id="index"]/ol/li[' + str(index) + ']/a/@href'
                selectors = response.xpath(xpath)
                if not selectors:
                    break
                url = 'https://www.mayoclinic.org/' + selectors.get()
                yield scrapy.Request(url, callback=self.parse_diseases_detail)
                index += 1
            if response.url[-1] == '0':
                url = 'https://www.mayoclinic.org/diseases-conditions/index?letter=A'
                yield scrapy.Request(url, callback=self.parse)
            elif ord(response.url[-1]) < 90:
                url = response.url[:-1] + chr(ord(response.url[-1]) + 1)
                yield scrapy.Request(url, callback=self.parse)
        else:
            raise AttributeError('URL Error')

    def parse_diseases_detail(self, response):
        item = OscerSpiderItem()

        # fetch disease name
        diseases_xpath = '//*[@id="mayoform"]/div[6]/header/div/h1/a/text()'
        selectors = response.xpath(diseases_xpath).get()
        item['Diseases'] = selectors

        main_content = response.xpath('//*[@id="main-content"]//text()').extract()
        h2_content = response.xpath('//*[@id="main-content"]//h2//text()').extract()

        # Find the sections introduce Symptoms
        syptoms = self.find_content('Symptoms', main_content, h2_content)

        item['Symptoms'] = syptoms

        # Find the sections introduce Causes
        causes = self.find_content('Causes', main_content, h2_content)

        item['Causes'] = causes

        # Click Diagnosis & treatment to reveal hidden content
        self.chrome_driver.get(response.url)
        button = self.chrome_driver.find_element_by_xpath('//*[@id="et_genericNavigation_diagnosis-treatment"]')
        button.click()
        html = self.chrome_driver.page_source
        selenium_response = HtmlResponse(url=response.url, body=html, encoding='utf-8')

        new_main_content = selenium_response.xpath('//*[@id="main-content"]//text()').extract()
        new_h2_content = selenium_response.xpath('//*[@id="main-content"]//h2//text()').extract()

        # Find the sections introduce Diagnosis
        diagnosis = self.find_content('Diagnosis', new_main_content, new_h2_content)
        item['Diagnosis'] = diagnosis

        # Find the sections introduce Treatment
        treatment = self.find_content('Treatment', new_main_content, new_h2_content)
        item['Treatment'] = treatment
        print(item['Diseases'])

        yield item

    def find_content(self, item, main_content, h2_content):
        try:
            start_index = main_content.index(item)
            h2_index = h2_content.index(item)
            if h2_index == len(h2_content) - 1:
                end_index = main_content.index('By Mayo Clinic Staff')
            else:
                next_title = h2_content[h2_index + 1]
                end_index = main_content.index(next_title)

            content = ''
            for index in range(start_index + 1, end_index):
                content += main_content[index]
        except ValueError:
            content = ''

        return content
