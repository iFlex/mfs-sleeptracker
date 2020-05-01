from datetime import datetime, timedelta

class FeedManager:

	def __init__(self, config, datasource, datasync, translator):
		self.feeds = {}
		self.update_modes = ['latest','next','custom']
		self.update_config(config)
		self.datasource = datasource
		self.datasync = datasync
		self.translator = translator

	def update_config(self, config):
		self.feeds = config


	def has_feed(self, feed):
		return feed in self.feeds


	def is_valid_update_mode(self, mode):
		return mode in self.update_modes


	def granularity_to_timedelta(self, granularity):
		if granularity == 'day':
			return timedelta(days=1)
		if granularity == 'hour':
			return timedelta(hours=1)
		return timedelta(hours=0)


	'''
	This updates a feed in 3 ways (mode):
	1. latest - the latest data available / data for now with granularity considered
	2. next - the next block of data following what was last written in the datasync for this feed
	3. custom - custom datetime provided by user
	'''
	def update_feed(self, feed_name, mode=None, start_date=None, end_date=None):
		config = self.feeds[feed_name]

		if 'mode' in config and mode == None:
			mode = config['mode']
		elif mode == None:
			mode = 'latest'

		if not self.is_valid_update_mode(mode):
			raise Exception("Invalid update mode '%s'" % mode)
		
		
		granularity = config['granularity']
		granularity_delta = self.granularity_to_timedelta(granularity)
		delay = timedelta(seconds=0)
		if 'delay' in config
			delay = timedelta(seconds=config['delay'])

		if mode == 'latest':
			end_date = datetime.now() - delay
			start_date = end_date - granularity_delta
		elif mode == 'next':
			start_date = self.datasync.get_last_timestamp(feed_name, self.translator.get_user())
			end_date = datetime.now() - delay
			print("Last record of %s in database is from %s" % (feed_name,start_date))
			if end_date < start_date:
				print("Database contains the latest data within configured delay");
				return

		print("Updating feed %s mode:%s - for datetime: %s to datetime: %s" % (feed_name, mode,start_date,end_date))
		data = self.datasource.query(feed_name, start_date, end_date)
		
		if data != None:
			translated = self.translator.translate(data, feed_name)
			self.datasync.write(translated)
		else:
			print("Failed to fetch %s data for %s" % (feed_name, start_date))


	def update(self, feeds=[], mode='latest'):	
		if feeds == None or len(feeds) == 0:
			feeds = self.feeds.keys()
		
		for feed in feeds:
			try:
				self.update_feed(feed, mode)
			except Exception as e:
				print("Failed to update feed %s" % feed)
				print(e)