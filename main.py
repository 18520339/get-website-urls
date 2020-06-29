# -*- coding: utf-8 -*-
import threading
import multiprocessing
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'alphabooks'
HOMEPAGE = 'https://alphabooks.vn/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)

QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
OTHERS_FILE = PROJECT_NAME + '/others.txt' 

NUMBER_OF_THREADS = multiprocessing.cpu_count() * 2

queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

# Tạo các luồng thực hiện
def create_workers():
	for _ in range(NUMBER_OF_THREADS):
		t = threading.Thread(target = work)
		t.daemon = True
		t.start()

def work():
	while True:
		url = queue.get()
		Spider.crawl_page(threading.current_thread().name, url)
		queue.task_done()


# Mỗi link trong hàng đợi là 1 luồng mới
def create_jobs():
	for link in file_to_set(QUEUE_FILE):		
		queue.put(link)
	queue.join()
	crawl()

# Kiểm tra có phần từ nào trong hàng đợi ko, nếu có thì crawl
def crawl():
	queued_links = file_to_set(QUEUE_FILE)
	if len(queued_links) > 0:
		print(str(len(queued_links)) + ' links trong hàng đợi')
		create_jobs()
	else:
	 	os.remove(QUEUE_FILE)

create_workers()
crawl()