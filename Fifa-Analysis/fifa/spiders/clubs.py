from typing import Iterable
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
import time


class clubsSpider(scrapy.Spider):
    name = "clubs"
    allowed_domains = ["sofifa.com"]

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    
    def start_requests(self):
        yield scrapy.Request(url= 'https://sofifa.com/players', headers= {'User-Agent': self.user_agent})

    def parse(self, response):
        players = response.xpath('//table//tbody//tr/td[2]/a')
        for player in players:
            name = player.xpath('./text()').get()
            player_url = 'https://sofifa.com' + player.xpath('./@href').get()
            request = scrapy.Request(url= player_url,\
                                      headers= {'User-Agent': self.user_agent},\
                                         callback= self.parse_player, meta= {'name': name})
            yield request

        next_page = response.xpath('//a[@class="button"]/@href').get()

        if next_page:
            next_page = 'https://sofifa.com' + response.xpath('//a[@class="button"]/@href').get()
            yield scrapy.Request(url=next_page, callback=self.parse, headers={
                'User-Agent': self.user_agent
            })

    def parse_player(self, response):

        time.sleep(1)
        name = response.meta['name']
        yield {
            'name': name,
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