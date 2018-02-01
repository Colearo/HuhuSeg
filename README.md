# HuhuSeg

HuhuSeg是一个基于**MMSEG**[1]的四种消歧规则和最大匹配方式的简单中文分词器，只有数百行代码。    
Simple Chinese segmentor based on the four ambiguity-resolving rules by **MMSEG**[1] and examples.  

同时HuhuSeg实现了一个简单但是非常高效的词图生成方式，由**HanLP**[3]的启发而来。同时核心词典直接使用了**jieba**[2]的词频词典。    
HuhuSeg implemented a simple but graceful words-gram generation enlightened by **HanLP**[3]. And the dictionary(including the words tag and frequency) was included from **jieba**[2].  

## How-to use 
### Installation  

```
pip3 install HuhuSeg
```

### Segmentation  

如下代码为分词器的使用方式：    
We can just try to segment the Chinese texts like this :  

```python
from huhu_seg.segmentor import Segmentor

s = Segmentor('为人民办公益')
tokens = s.gen_tokens()
for item in tokens:
    print(str(item))
```

And the output is :
```
[frequency 295952 | p | length 1] 为
[frequency 43719 | n | length 2] 人民
[frequency 10314 | v | length 1] 办
[frequency 404 | n | length 2] 公益
```

### Keywords Extraction
#### TF-IDF Keywords Extraction

HuhuSeg基于**TF-IDF**[4]算法实现了一个关键词提取器，IDF词频模型来源于针对接近100万条的wiki中文词条的分词统计，如下为使用方式：    
Now HuhuSeg supports the keywords extraction based on the **TF-IDF**[4]. Just have a try like :  

```python
from huhu_seg.tfidf import KeywordsEx

k = KeywordsEx('程序员(英文Programmer)是从事程序开发、维护的专业人员。一般将程序员分为程序设计人员和程序编码人员，但两者的界限并不非常清楚，特别是在中国。软件从业人员分为初级程序员、高级程序员、系统分析员和项目经理四大类。')
list = k.extract()
for word, freq in list :
    print('[%s %f]' % (word, freq))
```

Output is :
```
[程序员 0.735660]
[人员 0.305123]
[系统分析员 0.300264]
[程序开发 0.232286]
[项目经理 0.231476]
```

#### TextRank Keywords Extraction

在TF-IDF实现的关键词提取之外，这里还实现了基于**TextRank**[5]的提取算法，不依赖于庞大的IDF模型，而是试图在文本中词语的共现关系图里找到被Rank最高的词语。当然，除此之外，这里的代码实现的关键词提取还使用了一个小trick，在通过TextRank提取完关键词之后，会再次扫描文本，找到top关键词中是否有邻接词可以组成短语，如下面的提取“旅行青蛙”和“开发游戏”即是通过这种方式提取出来的。   
By **TextRank**[5], we can escape those huge and overwhelming IDF dictionaries, and try to find the relationship of words between the co-occuring gragh. As you can see in this output, we have a little trick to extract the better keywords with meaningful semantics: the extractor may scan the whole text to find if there are top keywords could construct the phrase. If it is true, we select them and build new keywords table. In the test, it seems to have the effective and better results.  

```python
from huhu_seg.textrank import TextRank

t = TextRank("""《旅行青蛙》目前仍是App Store中国区免费游戏下载榜榜首。
一款放置类休闲手游，在没有汉化版的情况下，打败一众试图将玩家拽入沉迷的“肝系游戏”，达成了一个不大不小的奇迹。
《旅行青蛙》的玩法极其简单，玩家只需采集庭院里的四叶草为青蛙购置旅行使用的便当、道具、护身符三样物品，为旅行蛙做好出门旅行的准备就可以了。游戏里的等待多过操作，也有人把它当成当下最火的“佛系”说法里的“佛系游戏”。
对《旅行青蛙》的制方Hit-Point来说，走进舞台中央，曝光在聚光灯下，却是一种无来由的慌乱。“太意外”是他们向外界陈述感受时，最常提到的一个词语。
创立于2007年的Hit-Point，主要从事休闲手机游戏开发，例如他们的《猫咪后院》，这款游戏让玩家在庭院里摆放各种道具来吸引各式各样的猫咪。在十年中，Hit-Point共开发了约30款游戏。
尽管《旅行青蛙》是Hit-Point的最新游戏，但实际上，开发者没有为这款游戏赋予太多意义，按照Hit-Point的说法，在开发游戏时，他们仅简单设置了一个“10岁到30岁的女性”的目标客户范围。
而现在，《旅行青蛙》覆盖玩家群体已经大大超出Hit-Point设定目标，在中国更是获得了爆发性增长。Hit-Point告诉界面新闻记者，截至1月26日，《旅行青蛙》下载总量已达到1100万，目前这个数字仍在迅速增长。根据日本媒体报道，在App Store的下载总量中，中国占95%，日本仅有2%。
“我们一直在努力设计和开发游戏，并期望它们能被世界范围内的玩家所接受，但《旅行青蛙》在中国获得如此大范围的流行，还是超过了我们想象。”一位Hit-Point负责人告诉界面新闻记者，他们没有进行任何游戏推广。
“也许是游戏非常简单，人们会想为什么不下载试试呢？而且通过社交媒体和口头传播，这种连锁反应一下子吸引了很多玩家。”Hit-Point相关负责人猜测游戏成功的原因时说道。
设计为免费游戏的《旅行青蛙》，主要通过广告和游戏内购买盈利，玩家可以选择使用真实货币购买四叶草。就盈利模式而言，《旅行青蛙》极为克制，其内置广告是否观看被设定为用户选择，而游戏最大的内购金额也仅为25元人民币。
即使如此，玩家为《旅行青蛙》付费的意愿也超过Hit-Point预料。根据App Annie统计，《旅行青蛙》在中国区App Store畅销排名第21，超过《阴阳师》、《荒野行动》等手游。
“《旅行青蛙》被设定为一款可以基本免费玩的游戏，但似乎比我们想象中有更多用户使用了游戏的内购，”Hit-Point负责人告诉界面记者，“根据我们统计，在游戏的日活跃用户中，约有3%-8%选择了内购。”
实际上，伴随游戏的火爆，各种山寨版《旅行青蛙》已经在应用市场泛滥。正版《旅行青蛙》在App Store里显示的名字为《旅かえる》，制作公司为Hit-Point Co,.Ltd，在App Store里评分4.3。而此前，玩家若在App Store搜索中文“旅行青蛙”，则会出现一款收费30元，名为“旅行青蛙.”的仿制版游戏，游戏玩法类似微信小游戏“跳一跳”，但该应用开发者显示“Song Yang”。目前，该游戏已经被苹果下架。
对于频繁出现的山寨版游戏，以及非授权提供的盗版《旅行青蛙》，Hit-Point更多的是一种无奈，“盗版存在对我们来说是一个很难过的问题，当用户因为盗版受到任何损失时，我们会更加难过，对此我们认为有必要采取一些对策。不过首先，我们希望创造一个向用户传递正确信息的环境。”
Hit-Point向界面记者透露，对于将《旅行青蛙》正式引入中国的问题，他们已经收到一些中国公司的合作提议并积极考虑中，但还没有达到谈论细节的阶段。关于《旅行青蛙》的中国文化，这家公司表示可能会和《旅行青蛙》的代理合作公司一同讨论。
对于《旅行青蛙》未来的更新，Hit-Point表示，它们首先将增加青蛙可参观地点的数量，这样，青蛙将会发回更多的旅行照片。“玩家给我们的反馈非常积极，比如多语言支持和更多的旅行照片。我们会在不断更新游戏的同时一起处理玩家的请求。”
随着《旅行青蛙》大火，Hit-Point也拥有了《猫咪后院》外又一个知名IP，而对于后者，Hit-Point也进行了相当深入的IP开发，比如周边《猫咪后院食谱》以及衍生电影。
“我们最初根本无法想象《猫咪后院》会被拍成电影。但从人物设定和世界观来看，《旅行青蛙》是可以通过各种方式展现的，但谁又知道它会如何发展呢？”在《旅行青蛙》衍生品开发方面，Hit-Point表示，如有机会，一定会进行相关研究。
据Hit-Point负责人介绍，Hit-Point内部有多个小组，负责开发不同的游戏。“从这方面看，我不能确定公司的发展方向，但简单的游戏玩法确实是我们吸引广泛玩家群体的重要理念。在思考未来的游戏制作方向时，这会是我们的重要考虑点。”上述负责人表示。
以下为采访摘要：
界面：《青蛙旅行》何时会提供中文化的版本？有没有一些中国公司接洽代理？
Hit-Point：我们已经收到建议并积极思考，但目前我们还没有达到谈论细节的阶段。中文化方面，我们确实有在考虑将游戏本地化，并且我们会与代理合作公司一起讨论。
界面：目前《青蛙旅行》在中国地区的用户规模和营收比例如何？大概有多少用户为游戏付费了？
Hit-Point：由于玩家基数仍在增长，我们不能给出一个确切数字，不过截至1月26日，游戏的总下载量已经达到了1100万。在游戏内购上数字也在迅速变化，我们统计到在日活跃用户中，有3%-8%的玩家使用了内购购买了三叶草。《青蛙旅行》是一款基本上可以免费玩的游戏，但似乎有比我们想象中更多的用户进行了内购。
界面：《青蛙旅行》应该是Hit-Point在中国最成功的一款游戏，您如何看待这种成功和在意外流行？有没有想过相关原因？
Hit-Point：我们一直在设计开发能被世界各地人们接受的游戏，但《青蛙旅行》在中国如此受欢迎还是超过了我们的预想，我们没有对游戏进行任何推广。人们喜欢这款游戏可能的原因是，《青蛙旅行》设计非常简单，所以人们非常愿意尝试这款游戏。另外，基于社交媒体和人们口头传播，让它产生了传播上的连锁反应。
界面：在中国的安卓市场，有一些未经过授权的非官方盗版游戏，在iOS上也有了一些山寨抄袭旅行《青蛙旅行》的游戏，您如何看待这点，是否会考虑采取维权行动？
Hit-Point：盗版的存在是一个令我们难过的问题。如果用户因此而遭受任何损失，我们会感到更加难过。因此我们认为有必要提供一些对策，但首先，我们希望创造一个能够向用户传达正确信息的环境。
界面：对于游戏未来的更新，有没有相关计划和打算，下一步更新的方向会是怎样的？比如是否会加入更多景点，在游戏玩法上更加丰富一些？
Hit-Point：在未来的更新中，我们将首先增加青蛙将参观的地方的数量，这样青蛙就可以发回更多照片。玩家给了我们许多反馈，例如多语言支持等，我们会在不断更新的同时也一并处理这些反馈。
界面：之前的作品《猫咪后院》已经有了丰富的周边衍生品开发，比如电影等，《青蛙旅行》会不会有相关考虑？
Hit-Point：对于衍生产品，如果可能的话，我们一定会进行开发。很难想象《猫咪后院》最后拍成了电影，但是游戏的世界观和人物设定是可以以各种方式利用的，所以谁会想到未来会发生什么呢？""")

list = t.extract()
for word, rank in list :
    print('[%s %f]' % (word, rank))
```

We can see the output :
```
[旅行青蛙 19.167803]
[开发游戏 14.831004]
[玩家 4.801199]
[中国 3.508624]
[用户 3.118792]
```

  
## TO-DO List
The TO-DO below shows what I have done and the next-steps :  
- [x] Implementation of MMSEG segmentor
- [ ] Optimization for dictionary indexing
- [ ] Named Entity Recognition
- [x] Keywords extraction
- [ ] Extraction of topic-phrase for news 

## Referrence
[1] [MMSEG: A Word Identification System for Mandarin Chinese Text Based on Two Variants of the Maximum Matching Algorithm](http://technology.chtsai.org/mmseg/)  
[2] [fxsjy/jieba](https://github.com/fxsjy/jieba)  
[3] [词图的生成](http://www.hankcs.com/nlp/segment/the-word-graph-is-generated.html)   
[4] [News Keyword Extraction for Topic Tracking](http://ieeexplore.ieee.org/document/4624203/)  
[5] [TextRank: Bringing Order into Texts](https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf)  

