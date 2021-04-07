import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import CctbiItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class CctbiSpider(scrapy.Spider):
	name = 'ctbi'
	start_urls = ['https://www.ctbi.com/news/community-trust-news']

	def parse(self, response):
		post_links = response.xpath('//a[@target="_self"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//div[@class="content"]/div//em[last()]//text()[not (ancestor::span[@class="small"])]').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="content"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=CctbiItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
