import os


# Mỗi website crawl đc là 1 folder
def create_website_folder(project_name):
	if not os.path.exists(project_name):
		print('Đang tạo folder ' + project_name)
		os.makedirs(project_name)


# Tạo hàng đợi và các file đc crawl
def create_data_files(project_name, base_url):
	queue = os.path.join(project_name , 'queue.txt')
	crawled = os.path.join(project_name,'crawled.txt')
	others = os.path.join(project_name,'others.txt')

	if not os.path.isfile(queue):
		write_file(queue, base_url)

	if not os.path.isfile(crawled):
		write_file(crawled, '')

	if not os.path.isfile(others):
		write_file(others, '')


def write_file(path, data):
	with open(path, 'w', encoding="utf-8") as file:
		file.write(data)


def append_to_file(path, data):
	with open(path, 'a', encoding="utf-8") as file: # a = append
		file.write(data + '\n')


def delete_file_contents(path):
	# with open(path, 'w', encoding="utf-8") as file:
	# 	pass
	open(path, 'w').close()


''' Tăng tốc độ crawl '''

# Đọc file và convert mỗi dòng thành các phần tử set
def file_to_set(file_name):
	results = set()

	with open(file_name, 'rt', encoding="utf-8") as file: # rt = read text file
		for line in file:
			results.add(line.replace('\n', ''))

	return results


# Lặp quanh 1 set, mỗi phần tử sẽ là 1 dòng mới trong file
def set_to_file(links, file_name):
	# delete_file_contents(file_name)
	# for link in sorted(links):
	# 	append_to_file(file_name, link)

	with open(file_name, 'w', encoding="utf-8") as file:
		for link in sorted(links):
			file.write(link + '\n')