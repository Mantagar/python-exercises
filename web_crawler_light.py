# NOTE: A lightweight approach using regex, inspired by web_crawler.sh
import urllib.request
import re
import sys

class WebHtmlProvider():
  def fetch_html(self, url):
    content = ""
    try:
      fp = urllib.request.urlopen(url)
      byte_content = fp.read()
      content = byte_content.decode("utf8")
    except Exception as e:
      pass
    return content  

class Crawler:
  LINK_PATTERN = re.compile("https?://[\\w\\-/.]+")
  
  def __init__(self, html_provider):
    self.html_provider = html_provider
    self.found_urls = set()
  
  def crawl(self, url, depth):
    if url in self.found_urls:
      return
    self.found_urls.add(url)

    print("-"*depth + url)

    if depth == 0:
      return
    depth -= 1

    html = self.html_provider.fetch_html(url)
    extracted_urls = Crawler.LINK_PATTERN.findall(html)

    for i in extracted_urls:
      self.crawl(i, depth)


if __name__ == "__main__":
  if len(sys.argv) != 3:
    print("Correct usage:\n\t./{} url max_depth".format(sys.argv[0]))
    exit(1)
  starting_url = sys.argv[1]
  max_depth = int(sys.argv[2])
  
  html_provider = WebHtmlProvider()
  crawler = Crawler(html_provider) 
  crawler.crawl(starting_url, max_depth)

