import os
import re
import lxml.html

class MetaParser():

	def __init__(self):

		self.verdict_basic_re = re.compile(
			'【裁判字號】\s+(?P<verdict_no>\d+,[\u4e00-\u9fff]+\(*（*[\u4e00-\u9fff]*）*\)*[\u4e00-\u9fff]*,\d+)\s+'
			'【裁判日期】\s+(?P<verdict_date>\d+)\s+' 
			'【裁判案由】\s+(?P<verdict_reason>[\u4e00-\u9fff]*（*[\u4e00-\u9fff]*）*)\s+')

		### Regular expressions to get judges information 
		self.single_judge_re = re.compile('\s+(?P<judge>法\s*官\s+([\u4e00-\u9fff]\s*){2,4})\s+')

		# For 合議庭 3 of the local courts and higher courts.
		self.full_court_3_re = re.compile(
			'(?P<chief_judge>審\s*判\s*長\s*法\s*官\s*([\u4e00-\u9fff]\s*){2,4})'
			'\s+(?P<judge_1>法\s*官\s+([\u4e00-\u9fff]\s*){2,4})'
			'\s+(?P<judge_2>法\s*官\s+([\u4e00-\u9fff]\s*){2,4})\s+'
		)
		# For 合議庭 of the surpreme court.
		self.full_court_5_re = re.compile(
			'(?P<chief_judge>審\s*判\s*長\s*法\s*官\s*([\u4e00-\u9fff]\s*){2,4})'
			'\s+(?P<judge_1>法\s*官\s+([\u4e00-\u9fff]\s*){2,4})'
			'\s+(?P<judge_2>法\s*官\s+([\u4e00-\u9fff]\s*){2,4})'
			'\s+(?P<judge_3>法\s*官\s+([\u4e00-\u9fff]\s*){2,4})'
			'\s+(?P<judge_4>法\s*官\s+([\u4e00-\u9fff]\s*){2,4})\s+'
		)

		### Regular Expression for prosecutor
		self.prosecutor_re = re.compile(
			'(?P<prosecutor>公\s*訴\s*人\s*[\u4e00-\u9fff]+檢\s*察\s*官\s*)+\s+'
		)

		### Regular Expression for lawyers
		self.lawyer_re = re.compile(
			# '((?P<representive_lawyer>訴\s*訟\s*代\s*理\s*人(\s*[\u4e00-\u9fff]+律\s*師\s*){1,}\s+)|'
			# '(?P<appionted_lawyer>指\s*定\s辯s*護\s*人\s*[\u4e00-\u9fff]+律\s*師\s*))'
			'(訴\s*訟\s*代\s*理\s*人\s*|選\s*任\s*辯s*護\s*人\s*|指\s*定\s*辯\s*護\s*人|'
			'自\s*訴\s*代\s*理\s*人\s*|代\s*理\s*人\s*|複\s*代\s*理\s*人\s*|共\s*同\s*理\s*人\s*)'
			'*\s+(?P<lawyers>\s+([\u4e00-\u9fff]\s*){2,5}律\s*師)'
		)


	def get_meta(self, context):

		item = {}

		# Access the basic meta info
		basic_meta_info = self.verdict_basic_re.search(context)
		if basic_meta_info:
			item['verdict_no'] = basic_meta_info.group('verdict_no')
			item['verdict_date'] = basic_meta_info.group('verdict_date')
			item['verdict_reason'] = basic_meta_info.group('verdict_reason')

		# Access the prosecutor information
		prosecutor = self.prosecutor_re.search(context)
		if prosecutor:
			item['prosecutor'] = self._prosecutor_filter(prosecutor.group('prosecutor'))

		# Access the lawyer
		lawyers

		# Access the judges' information
		full_court_5 = self.full_court_5_re.search(context)
		full_court_3 = self.full_court_3_re.search(context)
		if full_court_5:
			item['chief_judge'] = self._judge_filter(full_court_5.group('chief_judge'))
			item['judge_1'] = self._judge_filter(full_court_5.group('judge_1'))
			item['judge_2'] = self._judge_filter(full_court_5.group('judge_2'))
			item['judge_3'] = self._judge_filter(full_court_5.group('judge_3'))
			item['judge_4'] = self._judge_filter(full_court_5.group('judge_4'))
		elif full_court_3:
			item['chief_judge'] = self._judge_filter(full_court_3.group('chief_judge'))
			item['judge_1'] = self._judge_filter(full_court_3.group('judge_1'))
			item['judge_2'] = self._judge_filter(full_court_3.group('judge_2'))

		# For not 合議庭(Full court)'s 判決
		else:
			judge = self.single_judge_re.search(context)
			if judge:
				item['judge'] = self._judge_filter(judge.group('judge'))



		return item


	def _judge_filter(self, string):

		return re.sub('(審|判|長|法|官|\s)', '', string)

	def _prosecutor_filter(self, string):

		return re.sub('(公|訴|人|\s)', '', string)

# def get_context(html_context):

# 	html_doc = lxml.html.fromstring(html_context)

# 	return html_doc.cssselect('pre')[0].text_content


# def get_meta(context):

# 	item = {}

# 	### Basic info of verdict
# 	# verdict_basic_re = re.compile(
# 	# 	'【裁判字號】\s+(?P<verdict_no>\d+,[\u4e00-\u9fff]+\(*[\u4e00-\u9fff]*\)*,\d+)\s+'
# 	# 	'【裁判日期】\s+(?P<verdict_date>\d+)\s+' 
# 	# 	'【裁判案由】\s+(?P<verdict_reason>[\u4e00-\u9fff]*（*[\u4e00-\u9fff]*）*)\s+')

# 	### Regular expressions to get judges information 
# 	# chief_judge_re = re.compile('審\s*判\s*長\s*法\s*官\s*(?P<name>([\u4e00-\u9fff]\s*){2,3})')
# 	judge_1_re = re.compile('\s+(?P<judge_1>法\s*官\s+([\u4e00-\u9fff]\s*){2,4})\s+')

# 	# For 合議庭 3 of the local courts and higher courts.
# 	judge_3_re = re.compile(
# 		'(?P<chief_judge>審\s*判\s*長\s*法\s*官\s*([\u4e00-\u9fff]\s*){2,4})'
# 		'\s+(?P<judge_1>法\s*官\s+([\u4e00-\u9fff]\s*){2,4})'
# 		'\s+(?P<judge_2>法\s*官\s+([\u4e00-\u9fff]\s*){2,4})\s+'
# 	)
# 	# For 合議庭 of the surpreme court.
# 	judge_5_re = re.compile(
# 		'(?P<chief_judge>審\s*判\s*長\s*法\s*官\s*([\u4e00-\u9fff]\s*){2,4})'
# 		'\s+(?P<judge_1>法\s*官\s+([\u4e00-\u9fff]\s*){2,4})'
# 		'\s+(?P<judge_2>法\s*官\s+([\u4e00-\u9fff]\s*){2,4})'
# 		'\s+(?P<judge_3>法\s*官\s+([\u4e00-\u9fff]\s*){2,4})'
# 		'\s+(?P<judge_4>法\s*官\s+([\u4e00-\u9fff]\s*){2,4})\s+'
# 	)

	# Get 法官
	# judge_re = re.compile('法\s*官\s+(?P<name>([\u4e00-\u9fff]\s*){2,4})\s+')


# if __name__ == '__main__':
