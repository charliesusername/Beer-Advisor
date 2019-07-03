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
			family_style = family.xpath('./b/text()').extract_first()
			
			children = family.xpath('./ul/li/a')

			for child in children[:]:
				child_url = child.xpath('./@href').extract_first()
						
				yield Request(url='https://www.beeradvocate.com' + child_url, 
					callback=self.parse_first_product_list,
					meta = {'family_style':family_style})

	def parse_first_product_list(self, response):
		# Carry through values
		family_style = response.meta['family_style']
		 		
		# Get general description for beer.
		style_desc = response.xpath("//div[@id='ba-content']/div/text()").extract_first()
		

		# Find the total number of beers in category
		num_reviews = response.xpath('//span[@style="color: #FFFFFF"]/b/text()').extract_first()
		num_reviews = num_reviews[num_reviews.find("(out of ")+8:num_reviews.find(")")]
		num_reviews = int(''.join(num_reviews.split(',')))
		num_pages = num_reviews // 50 + 1 #50 beers per page

		# Generate each page of product lists from formula
		pages_of_beers = [response.url + '?sort=revsD&start={}'.format(x*50) for x in range(num_pages)]

		# Go to each page of product lists 
		for beer_page in pages_of_beers:
			yield Request(url = beer_page, callback=self.parse_each_product_list,
				meta = {'family_style':family_style,'style_desc':style_desc})

	def parse_each_product_list(self, response):
		# Carry through values
		family_style = response.meta['family_style']
		style_desc = response.meta['style_desc']
			
		# Find the url to each product on product list page
		beer_urls = response.xpath('//table//td[@class="hr_bottom_light"]/a/@href').extract()[::2]
		for beer in beer_urls[:]:
			yield Request(url = 'https://www.beeradvocate.com' + beer, callback = self.parse_product_overview,
				meta = {'family_style':family_style,'style_desc':style_desc})
		
	def parse_product_overview(self, response):
		# Get name of beer
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

		item['family_style'] = response.meta['family_style']
		item['style_desc'] = response.meta['style_desc']
		item['beer_name'] = beer_name
		item['brewery'] = brewery
		item['BAscore'] = BAscore
		item['beer_img'] = beer_img
		item['abv'] = abv
		item['num_reviews'] = num_reviews
		item['ranking'] = ranking
		item['desc'] = desc

		yield item