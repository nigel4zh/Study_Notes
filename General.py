import pandas as pd
import jieba

#停用词文件
stopWordsFile = open('D:/Nigel/code/Jupyter/stop_words.txt',encoding='utf-8')
stopWords = list()
for line in stopWordsFile.readlines():
    line = line.strip()
    stopWords.append(line)
stopWordsFile.close()

juheColNames = ['活跃度','微博点赞数','作者','双向关注数','出生日期','出生年份',',biz','简介','类别id','城市','城市级别','微博评论数','公司','星座','内容','数据类型','反对数','粉丝数','粉丝级别','收藏数','关注数','性别','id','是否广告','是否精华帖','是否火贴','是否原创','是否推荐','是否机器人水贴','是否置顶','关键词','点赞数','微博mid','微博类型','用户名','分析对象ID','分析对象','省份','发布时间','发表时间','微博转发数','评论数','转发微博id','学校','原创内容','情感','店铺id','店铺','店铺类别','站点id',',站点名称','发布终端','源内容','源微博id','源微博用户id','标题','话题','微博用户uid','url','用户类型','微博用户类型','阅读数','认证类型','微博数','本文作者','微信公众号id','内容_维度','内容_属性','内容_特征词','内容_情感','内容_正负面','内容_特征情感对']

juheColNamesV2 = ['分析对象ID','分析对象','搜索关键词','数据类型','站点名称','新闻来源','发表时间','url','标题','内容','作者','情感','阅读数','评论数','点赞数','微博评论数','粉丝数','关键词','用户名','话题','微博类型','原创内容','源内容','出生年份','性别','省份','城市','城市级别','粉丝级别','认证类型','活跃度','店铺','店铺类别','是否原创','是否广告','是否置顶','是否精华帖','是否火贴','是否推荐','是否水贴','id','类别id','mid','微博用户uid','站点id','源微博id','源微博用户id','转发微博id','微信公众号id','biz','店铺id','星座','用户类型','关注数','双向关注数','反对数','公司','本文作者','内容分词','微博用户类型','收藏数','出生日期','发布时间','微博点赞数','学校','微博数','微博转发数','总互动量','简介']

#筛选词文件
filtterFile = 'D:/Nigel/171130CNICE/FiltterWords.csv'
#filtterWords = pd.read_csv(filtterFile,header=0,encoding='utf-8')

#精简字段
simpleFields = ['数据类型','分析对象','内容','是否广告','发表时间','情感','url','用户名','用户类型','认证类型']

#单条内容分词，去停用词，长度控制
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

#维度统计模块化
#默认使用Mean作为标尺
def attriOutput(attriPoint,outputPath):
    attris = attriPoint.columns
    attriPointdf = pd.DataFrame({'inTimes':0,'inPer':0,'biggerTimes':0,'biggerPer':0,'gap':0},index=attris)
    attriPoint.loc['Row_sum'] = attriPoint.apply(lambda x: x.sum())
    attriPoint.loc['Mean'] = attriPoint.apply(lambda x: x.mean())
    attriPoint.loc['Median'] = attriPoint.apply(lambda x: x.median())
    for attri in attris:
        meanBigger = attriPoint[attri] > attriPoint.loc['Mean',attri]
        medianBigger = attriPoint[attri] > attriPoint.loc['Median',attri]
        lenBuzz = len(attriPoint)
        inBuzz = attriPoint[attri] > 0
        attriPointdf.loc[attri,'inTimes'] = inBuzz.sum()
        attriPointdf.loc[attri,'inPer'] = inBuzz.sum() / lenBuzz
        attriPointdf.loc[attri,'biggerTimes'] = meanBigger.sum()
        attriPointdf.loc[attri,'biggerPer'] = meanBigger.sum() / lenBuzz
        attriPointdf.loc[attri,'gap'] = inBuzz.sum() / lenBuzz - meanBigger.sum() / lenBuzz
    attriPointdf.to_csv(outputPath,encoding='utf-8')


#优化Mean和Median的选择：min优先
def attriOutput(attriPoint,outputPath):
    attris = attriPoint.columns
    attriPointdf = pd.DataFrame({'inTimes':0,'inPer':0,'biggerTimes':0,'biggerPer':0,'gap':0},index=attris)
    attriPoint.loc['Row_sum'] = attriPoint.apply(lambda x: x.sum())
    attriPoint.loc['Mean'] = attriPoint.apply(lambda x: x.mean())
    attriPoint.loc['Median'] = attriPoint.apply(lambda x: x.median())
    for attri in attris:
        meanBigger = attriPoint[attri] > attriPoint.loc['Mean',attri]
        medianBigger = attriPoint[attri] > attriPoint.loc['Median',attri]
        bigger = min(meanBigger.sum(),medianBigger.sum())
        lenBuzz = len(attriPoint)
        inBuzz = attriPoint[attri] > 0
        attriPointdf.loc[attri,'inTimes'] = inBuzz.sum()
        attriPointdf.loc[attri,'inPer'] = inBuzz.sum() / lenBuzz
        attriPointdf.loc[attri,'biggerTimes'] = bigger.sum()
        attriPointdf.loc[attri,'biggerPer'] = bigger.sum() / lenBuzz
        attriPointdf.loc[attri,'gap'] = inBuzz.sum() / lenBuzz - bigger.sum() / lenBuzz
    attriPointdf.to_csv(outputPath,encoding='utf-8')

#批量维度分词导出
def attriWords(attris,attriOutput,outputPath):
    for attri in attris:
        attriPart = attriOutput.loc[attriOutput[attri] > 0,:]
        attriPart = attriPart.reset_index(drop=True)
        attriDict = {}
        for num in range(0,len(attriPart)):
            content = attriPart.loc[num,'内容']
            singleJieba = jiebaHandle(content)
            for word in singleJieba:
                if word in attriDict.keys():
                    attriDict[word] += 1
                else:
                    attriDict[word] = 1
        attriWorddf = pd.DataFrame(columns=['Times'],index=None)
        for word in attriDict.keys():
            attriWorddf.loc[word,'Times'] = attriDict[word]
        outputFile = outputPath+attri+'.csv'
        attriWorddf.to_csv(outputFile,encoding='utf-8')
