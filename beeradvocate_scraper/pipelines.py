# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter
from recommendabeer.items import BeerItem, ReviewItem

class WriteItemsPipeline(object):
	def open_spider(self, spider):
		self.csvfile1 = open('beer_info.csv', 'wb')
		self.exporter1 = CsvItemExporter(self.csvfile1)
		self.exporter1.start_exporting()

		self.csvfile2 = open('beer_reviews.csv', 'wb')
		self.exporter2 = CsvItemExporter(self.csvfile2)
		self.exporter2.start_exporting()


	def process_item(self, item, spider):
		if isinstance(item,BeerItem):
			self.exporter1.export_item(item)
		elif isinstance(item, ReviewItem):
			self.exporter2.export_item(item)
		return item

	def close_spider(self, spider):
		self.exporter1.finish_exporting()
		self.csvfile1.close()
	
		self.exporter2.finish_exporting()
		self.csvfile2.close()
	








class WriteItemsToPipeline(object):
	def __init__(self):
		self.filename = 'beer_info.csv'

	def open_spider(self, spider):
		self.csvfile = open(self.filename, 'wb')
		self.exporter = CsvItemExporter(self.csvfile)
		self.exporter.start_exporting()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item	
		
	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.csvfile.close()

class WriteReviewItemPipeline(object):
	def __init__(self):
		self.filename = 'beer_reviews.csv'

	def open_spider(self, spider):
		self.csvfile = open(self.filename, 'wb')
		self.exporter = CsvItemExporter(self.csvfile)
		self.exporter.start_exporting()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		if isinstance(item, BeerItem):    		
			return item
		else:
			raise DropItem()

	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.csvfile.close()
