from web_crawler import Crawler, UrlExtractor
import pytest

class MockHtmlProvider():
	def __init__(self, url_to_html_map):
		self.url_to_html_map = url_to_html_map

	def fetch_html(self, url):
		return self.url_to_html_map[url]

test_url_1 = "http://test.url"
test_url_2 = "http://test.url/sth"
test_url_3 = "https://another-test.url/sth"
url_test_mapping = {
	test_url_1: '<a href="{}">link</a><a href="{}">link</a>'.format(test_url_1, test_url_2),
	test_url_2: '<a href="{}">link</a>'.format(test_url_3),
	test_url_3: '<b>NO LINKS HERE</b>' 
}
# mock downloading pages
html_provider = MockHtmlProvider(url_test_mapping)
url_extractor = UrlExtractor()

# Crawler has state - it remembers previously found urls
# using fixtures to get a fresh instance every time
@pytest.fixture
def crawler():
	return Crawler(url_extractor, html_provider)

def test_depth_0(crawler):
	max_depth = 0
	crawler.crawl(test_url_1, max_depth)
	assert len(crawler.found_urls) == 1
	assert test_url_1 in crawler.found_urls

def test_depth_1(crawler):
	max_depth = 1
	crawler.crawl(test_url_1, max_depth)
	assert len(crawler.found_urls) == 2
	assert test_url_1 in crawler.found_urls
	assert test_url_2 in crawler.found_urls

def test_depth_2(crawler):
	max_depth = 2
	crawler.crawl(test_url_1, max_depth)
	assert len(crawler.found_urls) == 3
	assert test_url_1 in crawler.found_urls
	assert test_url_2 in crawler.found_urls
	assert test_url_3 in crawler.found_urls

# NOTE: this test is great, it made me realize there was a severe bug
# where UrlExtractor remembered previously seen urls. In effect all
# accumulated urls from previous levels were wrongly crawled again
# on every level. Adding another test just to verify it: test_stateless_aggregate
def test_depth_3(crawler):
	max_depth = 3
	crawler.crawl(test_url_3, max_depth)
	assert len(crawler.found_urls) == 1
	assert test_url_3 in crawler.found_urls

def test_stateless_aggregate():
	max_depth = 1
	crawler = Crawler(url_extractor, html_provider)
	crawler.crawl(test_url_1, max_depth)
	assert len(crawler.found_urls) == 2
	crawler = Crawler(url_extractor, html_provider)
	crawler.crawl(test_url_3, max_depth)
	assert len(crawler.found_urls) == 1
