from datetime import datetime, timedelta
import traceback

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
	def _update_feed(self, config, feed_name, mode=None, start_date=None, end_date=None):
		print("UPDATE_CALL feed: %s mode:%s start:%s end:%s" %(feed_name,mode,start_date,end_date))
		#If not mode override was passed in, use the one in config
		if mode == None:
			mode = config['mode']
		if mode == None:
			mode = 'latest'

		if not self.is_valid_update_mode(mode):
			raise Exception("Invalid update mode '%s'" % mode)
		
		granularity_delta = self.granularity_to_timedelta(config.get('granularity',''))
		delay = timedelta(seconds=config.get('delay',0))

		if mode == 'latest':
			end_date = datetime.now() - delay
			start_date = end_date - granularity_delta
		elif mode == 'next':
			#Treat the case when the interval is too large (cap it) then try latest and leave gat - do backfilling when appropriate
			start_date = self.datasync.get_last_timestamp(feed_name, self.translator.get_user())
			end_date = datetime.now() - delay
			print("Last record of %s in database is from %s" % (feed_name,start_date))
			if end_date < start_date:
				print("Database contains the latest data within configured delay");
				return

		print("Updating feed %s mode:%s - from datetime: %s to datetime: %s" % (feed_name, mode,start_date,end_date))
		data = self.datasource.query(feed_name, start_date, end_date)
		
		if data != None:
			translated = self.translator.translate(data, feed_name)
			self.datasync.write(translated)
		else:
			print("Failed to fetch %s data for %s" % (feed_name, start_date))
			raise Exception("Failed to fetch data")

	def update_feed(self, feed_name, mode=None, start_date=None, end_date=None):
		config = self.feeds[feed_name]
		fallback_mode = config.get('fallback_mode', None)

		try:
			self._update_feed(config, feed_name, mode, start_date, end_date)
		except Exception as e:
			print("Update feed failed.")
			traceback.print_exc(file=sys.stdout)
			if fallback_mode == None:
				raise e
			else:
				print("Attempting fallback")
				self._update_feed(config, feed_name, fallback_mode, start_date, end_date)			

	#update feeds with their default modes
	def update(self, feeds=[]):	
		if feeds == None or len(feeds) == 0:
			feeds = self.feeds.keys()
		
		for feed in feeds:
			try:
				self.update_feed(feed, mode)
			except Exception as e:
				print("Failed to update feed %s" % feed)
				print(e)