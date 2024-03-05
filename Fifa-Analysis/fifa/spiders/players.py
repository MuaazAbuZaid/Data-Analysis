import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import time

class PlayersSpider(CrawlSpider):
    name = "players"
    allowed_domains = ["sofifa.com"]
    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url= 'https://sofifa.com', headers= {'User-Agent': self.user_agent})

    rules = (
        Rule(LinkExtractor(restrict_xpaths= '//table//tbody//tr/td[2]/a'), callback="parse_item", follow=False),
        Rule(LinkExtractor(restrict_xpaths= '//a[@class="button"]'), process_request= 'set_user_agent'),
        )

    def set_user_agent(self, request, ay7aga):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):

        time.sleep(0.5)
        
        if '/player' in response.url:
            yield {
                'full_name': response.xpath('//div[@class="profile clearfix"]/h1/text()').get(),
                'overall_rating': response.xpath('(//div[@class="grid"]//em)[1]/text()').get(),
                'potential': response.xpath('(//div[@class="grid"]//em)[2]/text()').get(),
                'value': response.xpath('(//div[@class="grid"]//em)[3]/text()').get(),
                'wage': response.xpath('(//div[@class="grid"]//em)[4]/text()').get(),
                'club': response.xpath('normalize-space(((//div[@class="grid attribute"]/div)[3]//a)[1]/text())').get(),
                'league': response.xpath('normalize-space(((//div[@class="grid attribute"]/div)[3]//a)[2]/text())').get(),
                'position': response.xpath('normalize-space((//div[@class="profile clearfix"]/p/span/text())[1])').get(),
                'preferred_foot': response.xpath('normalize-space(((//div[@class="grid attribute"]/div)[1]//p)[1]/text())').get(),
                'skill_moves': response.xpath('normalize-space((((//div[@class="grid attribute"]/div)[1]//p)[2]/text())[1])').get(),
                'week_foot': response.xpath('normalize-space((((//div[@class="grid attribute"]/div)[1]//p)[3]/text())[1])').get(),
                'international_reputation': response.xpath('normalize-space((((//div[@class="grid attribute"]/div)[1]//p)[4]/text())[1])').get(),
                'release_clause': response.xpath('normalize-space((//div[@class="grid attribute"]/div)[1]//p[8]/text())').get(),
                'id': response.xpath('normalize-space((//div[@class="grid attribute"]/div)[1]//p[9]/text())').get(),
                'work_rate': response.xpath('normalize-space((//div[@class="grid attribute"]/div)[1]//p[5]/text())').get(),
                'body_type': response.xpath('normalize-space((//div[@class="grid attribute"]/div)[1]//p[6]/text())').get(),
                'joined': response.xpath('normalize-space(((//div[@class="grid attribute"]/div)[3]//p)[6]/text())').get(),
                'contract_valid_until': response.xpath('normalize-space(((//div[@class="grid attribute"]/div)[3]//p)[7]/text())').get(),
                'birthdate_heigt_weight': response.xpath('normalize-space((//div[@class="profile clearfix"]/p/text())[last()])').get()
            }
        else:
            pass
    
       
