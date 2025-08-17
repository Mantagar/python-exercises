from web_crawler import Crawler, UrlExtractor
import pytest

class MockHtmlProvider():
  LINK_TEMPLATE = '<a href="{}">link</a>'
  def __init__(self, url_map):
    self.url_to_html_map = {url:self.build_html(url_map[url]) for url in url_map}

  def fetch_html(self, url):
    return self.url_to_html_map[url]

  def build_html(self, hrefs):
    html = ""
    for i in hrefs:
      html += MockHtmlProvider.LINK_TEMPLATE.format(i)  
    return html

test_url_1 = "http://test.url"
test_url_2 = "http://test.url/sth"
test_url_3 = "https://another-test.url/sth"
test_url_4 = "https://depth-test.url"
url_test_mapping = {
  test_url_1: (test_url_2,),
  test_url_2: (test_url_3,),
  test_url_3: (),
  test_url_4: (test_url_1, test_url_2)
}

# mock downloading pages
html_provider = MockHtmlProvider(url_test_mapping)
url_extractor = UrlExtractor()

"""
Crawler has a state - it remembers previously found urls.
Therefore I used fixtures to get a fresh instance every time.
"""
@pytest.fixture
def crawler():
  return Crawler(url_extractor, html_provider)

"""
This test is for a fringe scenario when an url was first
seen at depth 0 (not crawled) and the seen again with
higher depth. Such an url is expected not to be skipped.
"""
def test_seen_urls_on_depth_0(crawler):
  max_depth = 2
  crawler.crawl(test_url_4, max_depth)
  assert len(crawler.found_urls) == 4
  assert test_url_3 in crawler.found_urls

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

"""
NOTE: this test is great, it made me realize there was a severe bug
where UrlExtractor remembered previously seen urls. In effect urls accumulated
with every recursive call made by crawl method. In summary instead of crawling only
the urls extracted from the html at hand, all previously seen urls were crawled again.
Adding another test just to handle such a case: test_stateless_aggregate
"""
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
