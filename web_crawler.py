import html.parser
import urllib.request
import sys

# Crawler has a state, it keeps tabs on previously found and crawled urls.
# url_extractor and html_provider should be stateless
class Crawler():
	def __init__(self, url_extractor, html_provider):
		self.url_extractor = url_extractor
		self.html_provider = html_provider

		# The unique urls that were visited on depth > 0
		self.crawled_urls = set()
		# The unique urls that were visited on any depth
		self.found_urls = set()

	def crawl(self, url, max_depth):
		if url in self.crawled_urls:
			return
		self.found_urls.add(url)

		if max_depth == 0:
			return
		max_depth -= 1
		self.crawled_urls.add(url)
			
		html = self.html_provider.fetch_html(url)
		urls_in_html = self.url_extractor.extract_urls(html)
		for i in urls_in_html:
			self.crawl(i, max_depth)

class WebHtmlProvider():
	def fetch_html(self, url):
		fp = urllib.request.urlopen(url)
		byte_content = fp.read()
		content = ""
		try:
			content = byte_content.decode("utf8")
		except Exception as e:
			print(e)
		return content	
			
class UrlExtractor():
	class CustomHTMLParser(html.parser.HTMLParser):
		def __init__(self):
			super().__init__()
			self.urls = []

		def handle_starttag(self, tag, attrs):
			if tag != 'a':
				return

			for k,v in attrs:
				if k == "href" and v.startswith("http"):
					no_args_url = v.split('?')[0]
					self.urls.append(no_args_url)
					break

	# delegating finding urls to the composed inner class to make UrlExtractor stateless
	def extract_urls(self, html):
		parser = UrlExtractor.CustomHTMLParser()
		parser.feed(html)
		return parser.urls

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Correct usage:\n\t./{} url max_depth".format(sys.argv[0]))
		exit(1)
	starting_url = sys.argv[1]
	max_depth = int(sys.argv[2])
	
	url_extractor = UrlExtractor()
	html_provider = WebHtmlProvider()
	crawler = Crawler(url_extractor, html_provider)
	crawler.crawl(starting_url, max_depth)
	
	for i in crawler.found_urls:
		print(i)
	print("total: {}".format(len(crawler.found_urls)))

