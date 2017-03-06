import re
import os

from parser import MetaParser

# Access Paths of the files.
def get_file_paths(dirname):

	paths = []
	not_allowed_paths = set(['.git'])

	for d in os.listdir(dirname):
		# print(d)
		if os.path.isdir(dirname+d) and d not in not_allowed_paths:
			temp = dirname + d
			for c_d in os.listdir(temp):
				# print(c_d)
				c_d = temp + '/' + c_d
				if os.path.isdir(c_d):
					for g_d in os.listdir(c_d):
						g_d = c_d + '/'+g_d
						if not os.path.isdir(g_d):
							# print(g_d)
							paths.append(g_d)
	return paths


def test_parser_get_meta():

	# tw-judgements-2010-4 have html files
	text_files = get_file_paths('tw-judgements-2010-4/')
	target_html_number = len(text_files)
	meta_parser = MetaParser()
	count = 0
	unsuccessful_text = []
	results = []
	for text_file in text_files:
		text_file = open(text_file, 'r').read()
		result = meta_parser.get_meta(text_file)
		if result != {}:
			count += 1
			results.append(result)
			if 'prosecutor' not in result:
				print('============ Check Prosecutor =====================')
				# print(result['prosecutor'])
				print(text_file)
				print('===================================================')
				# print(text_file)
		else:
			unsuccessful_text.append(text_file)

	# Assure every verdict's meta is stored.
	if count != target_html_number:
		for text in unsuccessful_text:
			print('==========')
			print(text)

	# else:
	# 	for r in results:
	# 		if 'prosecutor' in r:
	# 			print('==========')
	# 			print(r)



	# tw-judgements-2010-4 have text files
	# text_files = get_file_paths('tw-judgements-2010-4/')


if __name__ == '__main__':
 	
 	test_parser_get_meta()