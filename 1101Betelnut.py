import pandas as pd
import jieba
#导入新词词库，完善分词结果（按项目）
userDict = 'G:/inprism_share/nigel/Py/Files/userdict.txt'   # 新词词库路径
jieba.load_userdict(userDict)

#导入停用词，项目通用，并清理空格
stopWordsFile = open('G:/inprism_share/nigel/Py/Files/stop_words.txt',encoding='utf-8')   # 停用词路径
stopWords = list()
for line in stopWordsFile.readlines():
    line = line.strip()
    stopWords.append(line)
#print(stopWords)     #如有必要，可打印查看停用词效果

#导入源数据，并精简字段
dataFile = 'G:/inprism_share/nigel/Py/Data/1027Betelnut.csv'  # 源数据路径
df_read = pd.read_csv(dataFile, header=0, encoding='utf-8')
df = df_read[['分析对象','抓取来源','用户名','文章链接','发表日期','标题','内容','情感','店名']]   # 精简源数据字段
#type(df)    #如有需要，可以确定df的dataframe化

#在源数据后添加分词数量统计列
df.loc[:,'Times'] = 0

#导入项目词库，必须包含Attribute（按项目）
dictPath = 'G:/inprism_share/nigel/Py/Files/BetelnutClass.csv'
dictFile = pd.read_csv(dictPath,header=None,index_col=0,encoding='utf-8')    #读取词库文件时，将Attribute列设置为Index
#print(dictFile.head())

#在源数据后添加线管Attribute列
attriList = list(dictFile.index)    #将项目词库的Index转为List，便于列添加
for attri in attriList:
    df.loc[:,attri] = 0      #在源数据后面添加Attribute列
#print(df.columns)    #如有需要，查看添加后的colNames

#Jieba分词，并且去除停用词、去除长度小于2、大于5的词，并统计各自总词数
lenDf = len(df)     #未合并分词结果的长度
jiebaDict = {}

for num in range(0,lenDf):
    singleContent = str(df.loc[num,'内容'])    #针对‘内容’字段分词，可以换成‘标题’字段
    singleJieba = jieba.lcut(singleContent)
    copyJieba = jieba.lcut(singleContent)    #为了规避remove的问题，另建一个分词结果的copy，用于选词
    for item in copyJieba:
        if item in stopWords:
            singleJieba.remove(item)    #去除停用词
        elif len(item) > 5:
            singleJieba.remove(item)    #去除长度大于5的词
        elif len(item) < 2:
            singleJieba.remove(item)    #去除长度小于2的词
        else:
            continue
    jiebaDict[num] = singleJieba
    df.loc[num,'Times'] = len(jiebaDict[num])    #将每个分词结果的包含词个数添加到源数据的Times Column
#print(jiebaDict)     #可以预览分词结果，Dict对象
#for key,value in jiebaDict.items():
#    print(key,value)

#将分词结果，合并到源数据，用于最后的统计导出
dfJieba = pd.Series(jiebaDict,name='Jieba')    #将最终分词结果Series化，用于和源数据合并
newdf = pd.concat([df,dfJieba],axis=1)    #将分词结果和源数据合并
#print(newdf.head())    #预览合并后的DataFrame效果
#print(newdf.columns)

#jiebaCsv = newdf.Jieba
#jiebaCsv.to_csv('jiebaCsv.csv',encoding='utf-8')

lenNewdf = len(newdf)     #合并分词后的df长度
#每个分词结果的Attribute次数统计
for num in range(0,lenNewdf):
    for attri in dictFile.index:
        for word in newdf.loc[num,'Jieba']:
            for item in dictFile.loc[attri,:]:
                if word == item:
                    newdf.loc[num,attri] = newdf.loc[num,attri] + 1     #统计每条数据的Attribute次数
#forsee = newdf.loc[:,'致癌物':'Jieba'].head(20)
#forsee.to_csv('forsee.csv',encoding='utf-8')

#统计每个维度在每条数据的词频占比，覆盖原次数统计
for num in range(0,lenNewdf):
    for attri in dictFile.index:
        newdf.loc[num,attri] = newdf.loc[num,attri] / newdf.loc[num,'Times']

#forsee = newdf.loc[:,'致癌物':'Jieba'].head(20)
#forsee.to_csv('forsee.csv',encoding='utf-8')

#导出结果为csv文件
newdf.to_csv('G:/inprism_share/nigel/Py/Files/newdf.csv',encoding='utf-8')
