'''
Function:
	数据可视化
'''
import os
import json
import jieba
import pickle
from pyecharts import Bar
from pyecharts import Pie
from pyecharts import Funnel
from wordcloud import WordCloud


'''柱状图(2维)'''
def drawBar(title, data, savepath='./results'):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	bar = Bar(title, title_pos='center')
	bar.use_theme('vintage')
	attrs = [i for i, j in data.items()]
	values = [j for i, j in data.items()]
	bar.add('', attrs, values, xaxis_rotate=15, yaxis_rotate=10)
	bar.render(os.path.join(savepath, '%s.html' % title))


'''饼图'''
def drawPie(title, data, savepath='./results'):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	pie = Pie(title, title_pos='center')
	pie.use_theme('westeros')
	attrs = [i for i, j in data.items()]
	values = [j for i, j in data.items()]
	pie.add('', attrs, values, is_label_show=True, legend_orient="vertical", legend_pos="left", radius=[30, 75], rosetype="area")
	pie.render(os.path.join(savepath, '%s.html' % title))


'''漏斗图'''
def drawFunnel(title, data, savepath='./results'):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	funnel = Funnel(title, title_pos='center')
	funnel.use_theme('chalk')
	attrs = [i for i, j in data.items()]
	values = [j for i, j in data.items()]
	funnel.add("", attrs, values, is_label_show=True, label_pos="inside", label_text_color="#fff", funnel_gap=5, legend_pos="left", legend_orient="vertical")
	funnel.render(os.path.join(savepath, '%s.html' % title))


'''词云'''
def drawWordCloud(words, title, savepath='./results'):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	wc = WordCloud(font_path='data/simkai.ttf', background_color='white', max_words=2000, width=1920, height=1080, margin=5)
	wc.generate_from_frequencies(words)
	wc.to_file(os.path.join(savepath, title+'.png'))


'''统计词频'''
def statistics(texts, stopwords):
	words_dict = {}
	for text in texts:
		temp = jieba.cut(text)
		for t in temp:
			if t in stopwords or t == 'unknow':
				continue
			if t in words_dict.keys():
				words_dict[t] += 1
			else:
				words_dict[t] = 1
	return words_dict


'''run'''
if __name__ == '__main__':
	with open('data.pkl', 'rb') as f:
		all_data = pickle.load(f)
	'''词云'''
	stopwords = open('stopwords.txt', 'r', encoding='utf-8').read().split('\n')[:-1]
	texts = [each[1][0] for each in all_data]
	words_dict = statistics(texts, stopwords)
	drawWordCloud(words_dict, '景点位置词云', savepath='./results')
	'''评分分布'''
	scores = {}
	for key, value in all_data.items():
		if value[3] in scores:
			scores[value[3]] += 1
		else:
			scores[value[3]] = 1
	drawPie('景区评分分布', scores)
	'''评级分布'''
	levels = {}
	print('AAAAA级景区有: ')
	for key, value in all_data.items():
		if not value[1] or value[1] == 'unknow':
			continue
		if 'AAAAA' in value[1]:
			print(key)
		if value[1] in levels:
			levels[value[1]] += 1
		else:
			levels[value[1]] = 1
	drawBar('景区评级分布', levels)
	'''价格分布'''
	prices = {'50元以下': 0, '50-100元': 0, '100-200元': 0, '200元以上': 0}
	for key, value in all_data.items():
		if value[2] == 'unknow' or not value[2]:
			continue
		price = float(value[2])
		if price < 50:
			prices['50元以下'] += 1
		elif price >= 50 and price < 100:
			prices['50-100元'] += 1
		elif price >= 100 and price < 200:
			prices['100-200元'] += 1
		elif price >= 200:
			prices['200元以上'] += 1
	drawFunnel('景区价格分布', prices)
	'''评论量最多的8个景区'''
	comments = {}
	for key, value in all_data.items():
		if value[-1] == '暂无' or not value[-1]:
			continue
		value[-1] = value[-1].replace('条', '')
		if len(comments.keys()) < 8:
			comments[key] = int(value[-1])
			continue
		if int(value[-1]) > min(list(comments.values())):
			comments[key] = int(value[-1])
			abandoned_key = list(comments.keys())[list(comments.values()).index(min(list(comments.values())))]
			del comments[abandoned_key]
	drawBar('评论人数最多的8个景区', comments)

	# # pkl文件先转化为txt文件，再转化为csv文件
	# 似乎网络上有直接将pkl文件转化为csv文件的网站
	# import pickle
	# import pandas as pd
	#
	# f = open('data.pkl', 'rb')
	# data = pickle.load(f)
	# pd.set_option('display.width', None)
	# pd.set_option('display.max_rows', None)
	# pd.set_option('display.max_colwidth', None)
	# print(data)
	# inf = str(data)
	# ft = open('test1.csv', 'w')
	# ft.write(inf)
