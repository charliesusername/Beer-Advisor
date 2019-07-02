from scrapy import Spider, Request
from recommendabeer.items import RecommendabeerItem
import re
import math

class BeerSpider(Spider):
	name = 'beer_spider'
	allowed_urls = ['https://www.beeradvocate.com/']
	start_urls = ['https://www.beeradvocate.com/beer/styles/']
	domain = 'https://www.beeradvocate.com'

	def parse(self, response):
		# Find each 'family'' of beer
		families = response.xpath('//div[@class="stylebreak"]')
		for family in families:
			# find urls to each child in family
			family_name = family.xpath('./b/text()').extract()
			children = family.xpath('./ul/li/a')

			for child in children[:]:
				child_url = child.xpath('./@href').extract_first()
				
				yield Request(url='https://www.beeradvocate.com' + child_url, 
					meta ={'family':family_name}, callback=self.parse_siblings_page)

	def parse_siblings_page(self, response):
		print("PARSING PAGE - O - BEERS")	
		family_name = response.meta['family']
		# Get general description for beer.
		desc = response.xpath("//div[@id='ba-content']/div/text()").extract_first()

		# Find the total number of beers in category
		num_reviews = response.xpath('//span[@style="color: #FFFFFF"]/b/text()').extract_first()
		num_reviews = num_reviews[num_reviews.find("(out of ")+8:num_reviews.find(")")]
		num_reviews = int(''.join(num_reviews.split(',')))
		num_pages = num_reviews // 50 + 1 #50 beers per page

		# find each beer url on the page
		response.xpath('//table//td[@class="hr_bottom_light"]/a/b/text()').extract()
		beer_urls = response.xpath('//table//td[@class="hr_bottom_light"]/a/@href').extract()[::2]

		for beer in beer_urls[:]:
			yield Request(url = 'https://www.beeradvocate.com' + beer, callback = self.parse_beer_overview)

	def parse_beer_overview(self, response):
		# Get name of beer
		print("PARSING NEW BEER")
		beer_name = response.xpath("//div[@class='titleBar']/h1/text()").extract_first()
		brewery = response.xpath("//div[@id='info_box']/a/b/text()").extract_first()
		BAscore = response.xpath("//span[@class='BAscore_big']/span/text()").extract_first()
		beer_img = response.xpath("//div[@id='main_pic_norm']/div/img/@src").extract_first()
		abv = re.search('\d+\.\d+%',''.join(response.xpath('//*[@id="info_box"]/text()').extract()))[0].replace('%','')
		num_reviews = int(''.join(response.xpath('//span[@class="ba-reviews"]/text()').extract_first().split(',')))
		ranking = ''.join(response.xpath('//div[@id="item_stats"]//dd/text()').extract_first().replace('#','').split(','))
		desc = ''.join(list(filter(lambda x: len(x) > 12, response.xpath('//div[@id="info_box"]/text()').extract()))).replace('\n','')
		print(beer_name, "PROCESSED")

		item = RecommendabeerItem()
		
		item['beer_name'] = beer_name
		item['brewery'] = brewery
		item['BAscore'] = BAscore
		item['beer_img'] = beer_img
		item['abv'] = abv
		item['num_reviews'] = num_reviews
		item['ranking'] = ranking
		item['desc'] = desc

		yield item