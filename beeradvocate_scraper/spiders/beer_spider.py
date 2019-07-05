from scrapy import Spider, Request
from recommendabeer.items import BeerItem, ReviewItem
import re
import math

i = 0
j = 0


class BeerSpider(Spider):
	name = 'beer_spider'
	allowed_urls = ['https://www.beeradvocate.com/']
	start_urls = ['https://www.beeradvocate.com/beer/styles/']
	domain = 'https://www.beeradvocate.com'

	def parse(self, response):
		# Find each 'family'' of beer
		families = response.xpath('//div[@class="stylebreak"]')
		for family in families[:]:
			# find urls to each child in family			
			children = family.xpath('./ul/li/a')

			for child in children[:]:
				child_url = child.xpath('./@href').extract_first()
						
				yield Request(url='https://www.beeradvocate.com' + child_url, 
					callback=self.parse_first_product_list)

	def parse_first_product_list(self, response):
			
		# Get general description for beer.
		#style_desc = response.xpath("//div[@id='ba-content']/div/text()").extract_first()		

		# Find the total number of beers in category
		num_reviews = response.xpath('//span[@style="color: #FFFFFF"]/b/text()').extract_first()
		num_reviews = num_reviews[num_reviews.find("(out of ")+8:num_reviews.find(")")]
		num_reviews = int(''.join(num_reviews.split(',')))
		num_pages = num_reviews // 50 + 1 #50 beers per page

		# Generate each page of product lists from formula
		pages_of_beers = [response.url + '?sort=revsD&start={}'.format(x*50) for x in range(num_pages)]

		# Go to each page of product lists 
		for beer_page in pages_of_beers[:]:
			yield Request(url = beer_page, 
				callback=self.parse_each_product_list)

	def parse_each_product_list(self, response):
		# Carry through values
		#style_desc = response.meta['style_desc']
			
		# Find the url to each product on product list page
		num_beers = len(response.xpath('//table//tr').extract())-4
		beer_rows = [response.xpath('//table//tr[{}]'.format(x)) for x in range(4,num_beers+4)]

		for beer in beer_rows[:]:
			num_ratings = int(''.join(beer.xpath('.//text()').extract()[3].split(',')))
			if num_ratings < 100:
				break
			beer_url = beer.xpath('.//a/@href').extract_first()

			yield Request(url = 'https://www.beeradvocate.com' + beer_url, callback = self.parse_product_overview)
		
	def parse_product_overview(self, response):
		# Get name of beer
		beer_name = response.xpath("//div[@class='titleBar']/h1/text()").extract_first()
		brewery = response.xpath("//div[@id='info_box']/a/b/text()").extract_first()
		BAscore = response.xpath("//span[@class='BAscore_big']/span/text()").extract_first()
		abv = re.search('\d+\.\d+%',''.join(response.xpath('//*[@id="info_box"]/text()').extract()))[0].replace('%','')		
		num_reviews = int(''.join(response.xpath('//span[@class="ba-reviews"]/text()').extract_first().split(',')))
		ranking = ''.join(response.xpath('//div[@id="item_stats"]//dd/text()').extract_first().replace('#','').split(','))
		beer_img = response.xpath('//div[@style="position:relative;"]/img/@src').extract_first()
		desc = ''.join(list(filter(lambda x: len(x) > 12, response.xpath('//div[@id="info_box"]/text()').extract()))).replace('\n','')
		beer_style = response.xpath('//div[@id="info_box"]/a/b/text()').extract()[1]
		
		global i
		i = i + 1

		print('*-'*45,'\n\t\t\t\t',i, "-", beer_name, "PROCESSED\n",'*-'*45)
		
		item = BeerItem()
		item['beer_id'] = i
		item['beer_name'] = beer_name
		item['brewery'] = brewery
		item['BAscore'] = BAscore
		item['abv'] = abv
		item['num_reviews'] = num_reviews
		item['ranking'] = ranking
		item['beer_img'] = beer_img
		item['desc'] = desc
		item['beer_style'] = beer_style
		#item['style_desc'] = response.meta['style_desc']
		
		# Send beer product to writer.
		yield item

		# Process reviews for this beer.
		# Find the number of reviews for this produt
		num_reviews = response.xpath('//div[@style="font-size:1em; padding:4px; margin:0px 0px 10px 0px;"]//text()').extract()[1]
		num_reviews = int(''.join(re.search(':\s(.+)',num_reviews)[1].split(',')))

		review_pages = num_reviews // 25 + 1 #25 reviews per page
		
		base_url = response.url
		reviews_urls = ['?view=beer&sort=top&start={}'.format(x*25) for x in range(review_pages)]
		for review_page in reviews_urls[:]:
			yield Request(url = base_url + review_page, callback = self.parse_review_page,
				meta={'id':i})

	def parse_review_page(self, response):
		reviews_on_page = response.xpath('//div[@id="rating_fullview_container"]') 
		global j
		for review in reviews_on_page:
			j = j + 1
			username, posted = review.xpath('./div/div/span/a/text()').extract()
			text = ''.join(review.xpath('./div/text()').extract()[1:-1])
			ratings = review.xpath('./div/span[@class="muted"]/text()').extract_first()
			score = review.xpath('./div/span[@class="BAscore_norm"]/text()').extract_first()

			item = ReviewItem()
			item['review_id'] = j
			item['beer_id'] = response.meta['id']
			item['username'] = username
			item['posted'] = posted
			item['text'] = text
			item['ratings'] = ratings
			item['score'] = score
			
			yield item
			


