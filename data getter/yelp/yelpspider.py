import scrapy

class MyprojectItem(scrapy.Item):
    date = scrapy.Field()
    rating = scrapy.Field()
    comment = scrapy.Field()


start_url="https://www.yelp.com/biz/amys-baking-company-scottsdale?sort_by=date_desc"
END_PAGE = 74
class YelpSpider(scrapy.Spider):
    name = 'yelp'
    start_urls = []
    
    current_idx = 0
    
    def __init__(self, start_url, *args, **kwargs):
        super(YelpSpider, self).__init__(*args, **kwargs)
        YelpSpider.start_urls = [start_url]
        
    
    def parse(self, response):
        # Extracting the content using css selectors
        for entry in response.xpath('//*[@id="reviews"]/section/div[2]/ul/li'): # comment item
            item = MyprojectItem()
            item['date'] = entry.xpath('./div/div[2]//text()').get()
            item['rating'] = entry.xpath('./div/div[2]/div/div/span/div/@aria-label').get()
            item['comment'] = '\n'.join(entry.xpath('./div/div[3]//text()').getall())
            yield item

        # Handling pagination
        YelpSpider.current_idx += 1
        next_page_url = start_url + f'&start={YelpSpider.current_idx}0'
        if YelpSpider.current_idx < END_PAGE:
            yield scrapy.Request(response.urljoin(next_page_url))
