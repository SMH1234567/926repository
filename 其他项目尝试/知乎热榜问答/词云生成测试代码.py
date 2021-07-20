# 导入模块
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import jieba
# 准备文本数据
path_txt = 'E:/词云/headline.txt'
f = open(path_txt, 'r', encoding='UTF-8').read()
# 结巴分词，生成字符串，wordcloud无法直接生成正确的中文词云
cut_text = " ".join(jieba.cut(f))
# 加载一张图片，转换为numpy中的数组
mask = np.array(Image.open('E:/词云/图片.png'))
# 创建词云对象
wordcloud = WordCloud(
    width=500,  # 设置宽度为500px
    height=300,  # 设置高度为300px
    background_color='white',  # 设置背景为白色
    # 设置字体，不然会出现口字乱码，文字的路径是电脑的字体一般路径，可以换成别的
    font_path="C:/Windows/Fonts/simfang.ttf",
    stopwords={"p", "P"},  # 设置禁用词
    max_font_size=100,  # 设置最大字体大小
    min_font_size=10,  # 设置最小字体大小
    collocations=False,  # 去除重复
    mask=mask
)
# 根据文本生成词云
wordcloud.generate(cut_text)
# 绘图
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()