import pandas as pd
import jieba

#停用词文件
stopWordsFile = open('G:/inprism_share/nigel/Py/Files/stop_words.txt',encoding='utf-8')
stopWords = list()
for line in stopWordsFile.readlines():
    line = line.strip()
    stopWords.append(line)
stopWordsFile.close()

#源数据文件
dataPath = 'G:/inprism_share/nigel/Py/Data/1124senviv.csv'
df = pd.read_csv(dataPath,header=0,engine='python',encoding='utf-8')

#精简源文件字段
simplefields = ['分析对象','抓取来源','用户名','文章链接','发表日期','标题','内容','情感','店名']
df = df.loc[:,simplefields]

#自定义词典
userDict = 'G:/inprism_share/nigel/Py/Files/userdict.txt'
jieba.load_userdict(userDict)

#项目词库
dictPath = 'G:/inprism_share/nigel/Py/Files/SenvivClass.csv'
dictFile = pd.read_csv(dictPath,header=None,index_col=0,encoding='utf-8')
attriList = list(dictFile.index)
for attri in attriList:
    df.loc[:,attri] = 0

#新增词数统计列“Times”
df.loc[:,'Times'] = 0

def jiebaHandle(content):
    singleContent = str(content)
    singleJieba = jieba.lcut(singleContent)
    copyJieba = jieba.lcut(singleContent)
    for item in copyJieba:
        if item in stopWords:
            singleJieba.remove(item)
        elif len(item) > 5:
            singleJieba.remove(item)
        elif len(item) < 2:
            singleJieba.remove(item)
        else:
            continue
    return singleJieba

sepCha = '|'
for num in range(0,len(df)):
    for attri in dictFile.index:
        content = df.loc[num,'内容']
        for word in jiebaHandle(content):
            for item in dictFile.loc[attri,:]:
                if word == item:
                    df.loc[num,attri] += 1
    df.loc[num,'Jieba'] = sepCha.join(jiebaHandle(content))
    df.loc[num,'Times'] = len(jiebaHandle(content))


for num in range(0,len(df)):
    for attri in list(dictFile.index):
        if df.loc[num,'Times'] != 0:
            df.loc[num,attri] = df.loc[num,attri] / df.loc[num,'Times']

outputPath = 'G:/inprism_share/nigel/Py/Files/1127senviv.csv'
df.to_csv(outputPath,encoding='utf-8')
