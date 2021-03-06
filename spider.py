from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *


class Spider:

	project_name = ''
	base_url = ''
	domain_name = ''

	queue_file = ''
	crawled_file = ''
	others_file = ''

	queue = set()
	crawled = set()
	others = set()


	def __init__(self, project_name, base_url, domain_name):
		Spider.project_name = project_name
		Spider.base_url = base_url
		Spider.domain_name = domain_name

		Spider.queue_file = Spider.project_name + '/queue.txt'
		Spider.crawled_file = Spider.project_name + '/crawled.txt'
		Spider.others_file = Spider.project_name + '/others.txt'

		self.launch()
		self.crawl_page('First Spider', Spider.base_url)


	@staticmethod
	def launch():
		create_website_folder(Spider.project_name)
		create_data_files(Spider.project_name, Spider.base_url)

		Spider.queue = file_to_set(Spider.queue_file)
		Spider.crawled = file_to_set(Spider.crawled_file)
		Spider.others = file_to_set(Spider.others_file)


	@staticmethod
	def crawl_page(thread_name, page_url):
		if page_url not in Spider.crawled:
			print(thread_name + ' đang crawl trang ' + page_url)
			print('Số link trong hàng đợi: ' + str(len(Spider.queue)) + ' | Số trang đã crawl: ' + str(len(Spider.crawled)))
			
			Spider.add_links_to_queue(Spider.gather_links(page_url))
			Spider.queue.remove(page_url)
			Spider.crawled.add(page_url)
			Spider.update_files()


	@staticmethod
	def gather_links(page_url):
		html_string = ''

		try:
			response = urlopen(page_url)
			# if response.getheader('Content-Type') == 'text/html':

			if 'text/html' in response.getheader('Content-Type'):
				html_bytes = response.read()
				html_string = html_bytes.decode('UTF-8')

			finder = LinkFinder(Spider.base_url, page_url)
			finder.feed(html_string)

		except Exception as error:
			print(str(error))
			return set()

		return finder.page_links()


	@staticmethod
	def add_links_to_queue(links):
		for link in links:
			if (link in Spider.queue) or (link in Spider.crawled):
				continue

			if Spider.domain_name != get_domain_name(link):
				Spider.others.add(link)
				continue

			Spider.queue.add(link)


	@staticmethod
	def update_files():
		set_to_file(Spider.queue, Spider.queue_file)
		set_to_file(Spider.crawled, Spider.crawled_file)
		set_to_file(Spider.others, Spider.others_file)