# HuhuSeg

HuhuSeg是一个基于**MMSEG**[1]的四种消歧规则和最大匹配方式的简单中文分词器，只有数百行代码。    
Simple Chinese segmentor based on the four ambiguity-resolving rules by **MMSEG**[1] and examples.  

同时HuhuSeg实现了一个简单但是非常高效的词图生成方式，由**HanLP**[3]的启发而来。同时核心词典直接使用了**jieba**[2]的词频词典。    
HuhuSeg implemented a simple but graceful words-gram generation enlightened by **HanLP**[3]. And the dictionary(including the words tag and frequency) was included from **jieba**[2].  

## Changelog  
### v0.4.29  
1. Add hotspot words weight computing.
2. Add extraction of topic-phrase for news based on hmm.
3. Fix bugs.

### v0.3.26  
1. Add support of named entity recognition based on 2-gram hmm model
2. Fix bugs.

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

### Named Entity Recognition

通过参考《基于角色标注的中国人名自动识别研究》[7]这篇论文和HanLP的训练数据[8]，输入粗分词结果，基于一阶HMM模型和Viterbi算法得到词语序列标签，然后使用Aho Corasick有限自动状态机进行模式匹配，获得其中匹配的人名标签，进行中文人名识别.      
As referrence to the paper **Automatic Recognition of Chinese personal Name Based on Role Tagging**[7] and HanLP's 2-gram hmm model[8], we build the hidden markov chain with Viterbi Algorithm to compute the max global probabilities. Through the tagged words, we can recognize the person's name by matching the pattern rules based on the AC automata. It receive the first level's tokens, and output token sequences with higher precision. 

```python
from huhu_seg.segmentor import Segmentor

s = Segmentor('李智伟高高兴兴和王晓薇出去玩。', hmm_config = True)
tokens = s.gen_tokens()
for item in tokens:
    print(str(item))
```

And the output is :
```
[frequency 3 | nr | length 3] 李智伟
[frequency 119 | ns | length 4] 高高兴兴
[frequency 555815 | c | length 1] 和
[frequency 3 | nr | length 3] 王晓薇
[frequency 3 | n | length 3] 出去玩
[frequency 0 | wj | length 1] 。

```


### Keywords Extraction
#### TF-IDF Keywords Extraction

HuhuSeg基于**TF-IDF**[4]算法实现了一个关键词提取器，IDF词频模型来源于针对接近100万条的wiki中文词条的分词统计，如下为使用方式：    
Now HuhuSeg supports the keywords extraction based on the **TF-IDF**[4]. Just have a try like :  

```python
from huhu_seg.tfidf import TFIDF

k = TFIDF('程序员(英文Programmer)是从事程序开发、维护的专业人员。一般将程序员分为程序设计人员和程序编码人员，但两者的界限并不非常清楚，特别是在中国。软件从业人员分为初级程序员、高级程序员、系统分析员和项目经理四大类。')
list = k.extract_kw()
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
Hit-Point：对于衍生产品，如果可能的话，我们一定会进行开发。很难想象《猫咪后院》最后拍成了电影，但是游戏的世界观和人物设定是可以以各种方式利用的，所以谁会想到未来会发生什么呢？""", window_width = 3, weight = 0.8)

list = t.extract_kw()
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

### Similarity of Texts
#### SimHash    

**SimHash**[6], proposed by MS Charikar, as a LSH(Locality Sensitive Hash), can be used to detect the similarity of two passages. There is a simple implementation; by the IDF Model we have and the tfidf keywords extraction, we extract those Top-200 feature words and hash them. Summing and normalizing, we get the SimHash fingerprint. All is done, now we just compute the two's Hamming Distance, and the similarity is represented by the distance.

We can have a try :  

```python

from huhu_seg.simhash import SimHash

t1 = SimHash("""
首家无印良品酒店深圳开业：定价950元起，没有门童行李员
1月18日，全球首家无印良品（MUJI）酒店在深圳正式开业。酒店共79间客房，定价从950元至2500元不等，预计将于今年3月和明年春季于北京和日本银座再开两家。
确切地说，此次开业的酒店属于无印良品全球首个“三合一项目”的一部分。这个项目包括了无印良品位于深圳深业上城的店铺、无印良品餐堂（MUJI Diner）和无印良品酒店（MUJI Hotel Shenzhen）。除了酒店是无印良品在全球开出的首家之外，此次新开的餐堂也是无印良品继上海旗舰店之后开出的第二家。
无印良品深圳三合一项目开业
无印良品“三合一项目”选址位于深圳市福田区的深业上城城市综合体。据株式会社良品计画代表取缔役社长松崎晓介绍，无印良品酒店整体理念和客房内的设计由无印良品把控，运营则由深业上城的开发商、深业集团旗下的深圳深业酒店管理有限公司执行，“无印良品的盈利主要来自冠名费”。
谈到开酒店的好处时，松崎晓称，顾客在酒店入住后可以为无印良品的产品、服务提供意见，公司可以根据顾客反馈而做出改进。
无印良品酒店大堂
无印良品深圳酒店共设置了79间客房，面积从26平方米到61平方米不等，价格分为950元、1085元、1300元、1480元和2500元五档。
无印良品酒店定价从950元至2500元不等
尽管无印良品酒店客房的定价不算便宜，但深业置地常务副总经理郝继霖认为，这一收费还是简单合理的，“首先，大家要负担得起，这不是一个奢华的酒店；另外，收费要简单，950元包含了税、早餐，不再收取任何服务费。而且我们每天都是这个价钱，没有浮动，情人节、新年都是一个价。”
深业置地有限公司总经理徐恩利也一再强调，从零售跨界到酒店领域的无印良品运营酒店的独特之处——追求极简，满足基本的需求，而不是过度的服务，因此酒店不安排门童和行李员等，但安排了休闲顾问，可以为住客提供深圳的休闲、游玩建议。
无印良品酒店内部
郝继霖介绍，无印良品酒店目前也没有与任何第三方酒店预订平台合作，订房只能通过无印良品的自有平台完成，价格除了连续订一个月有9折优惠外，价格没有弹性。在谈到背后逻辑时，他称：“因为我们是个小酒店，来住的一般都是粉丝，了解这个文化。”
无印良品酒店秉承了MUJI的一贯风格基因，其大堂没有一般酒店常见的大吊灯，酒店房间内包括床上用品等70%的物品都来自无印良品，房间内的烧水壶、洗浴用品、拖鞋和挂式CD机等都是无印良品的招牌产品。房间内墙上涂有一面硅藻泥，以海洋的硅藻土为主要原料，有吸收甲醛和防止墙壁发霉的作用。
无印良品酒店房间内，有70%的物品都来自无印良品
当被问及无印良品下一步的扩张计划时，松崎晓表示，目前，无印良品在中国有230家店铺，到2020年为止的一个目标是，每年新开20家店，改装30家原有店铺。“我们从来不说要开1000家或5000家店。我们不追求数量，也不追求规模。不会说一定要开多少家店。”
据介绍，目前无印良品80%的店铺集中在一二线城市，但松崎晓称，无印良品开店“不拘泥于开在几线城市，只是开在有无印良品粉丝的地方”。但他也谈到了无印良品大型店铺的开店计划——此前全国范围内仅在上海、成都有2家大型旗舰店，将来要翻3倍，即开到6家。
此次深圳的无印良品酒店开业后，另外两家酒店也将于今年3月和明年春季，先后在北京和日本银座开张。
“但除了这三家之外，目前没有其他的酒店计划。”松崎晓表示。
""") 
t2 = SimHash("""
全球首家MUJI HOTEL今天开业 我们提前去住了一晚
在房间里，有70%的物品都来自无印良品，可以在店内买到。
自从无印良品将要把全球首家MUJI HOTEL开在深圳的深业上城这一消息确定之后，很多人都在好奇酒店做出来最终会是怎样的。1月18日，MUJI HOTEL SHENZHEN正式对外开业。确切地说，开业的是无印良品的“三合一项目”——中国第三大的无印良品店铺、全球第2家MUJI Diner无印良品餐堂以及MUJI HOTEL。
一年前，当MUJI HOTEL还在施工时界面新闻曾经到访，当时已经知道负责设计MUJI HOTEL SHENZHEN的团队，来自无印良品的创始之一杉本贵志所拥有的工作室Super Potato。一年过去了，Super Potato对MUJI HOTEL SHENZHEN提及的一些设想已经实现，比如，切割废旧木材并贴在墙上以作装饰；购买一艘旧渔船摆放在酒店区域内，以纪念深圳曾经是座小渔村等等。
但更多未曾公布的细节，需要真正走进去才能一探究竟。
关于MUJI HOTEL的一些数据：
房间内有70％的物品是来自于无印良品，换而言之是可以在店内购买的
一共有79间客房，分布在深业上城的4楼至6楼
3楼设有300平方米的会议室，通过可移动墙面可分隔成三处独立空间，若完全开放，则可作为能容纳200人的小剧场
客房按面积和设施共分为5种房型，26平方米到61平方米不等，房价从950元起
有别于一般酒店前台连着大堂的设计，MUJI HOTEL SHENZHEN的前台和大堂是分开的。由于深业上城依山而建，酒店位于山坡的上方，所以酒店前台在二楼，而大堂则放在了三楼。这两个功能区的面积都不大，也没有酒店常见的大吊灯。但由于层高较高，两个空间并不显得压抑。
前台
大堂，一侧的书墙摆放着650多本书，住客可以带回房间阅读
会议室
MUJI HOTEL SHENZHEN的走廊灯光亮度，和房间内的灯光亮度保持一致。走廊里有缓缓的音乐，和无印良品店铺内播放的音乐也如出一辙。
房间内的烧水壶、洗浴用品、拖鞋等物都是无印良品的招牌产品。房间里还有深泽直人设计的那只著名的挂式CD机，遥控器床头，可以随时开关。
洗漱包内是牙刷、牙膏、浴帽等，没有梳子，所以要记得自备
房间内涂有一面硅藻泥，这种装修材质在南方地区的使用比较常见，以海洋的硅藻土为主要原料，有吸收甲醛和防止墙壁发霉的作用——在回南天漫长深圳，一到冬春之交墙壁能潮湿得淌下水来。
深业上城处在深圳商业最发达的福田区，但由于周围是莲花山和笔架山，夜里十分安静。床垫软硬适中，但比起无印良品在售的床品，酒店的床单和被套却不够柔软。为了测试酒店房间的隔音效果如何，我们想到了晚上在房间里打开“唱吧”唱了陈粒的《虚拟》。飙了几遍之后，并没有人来敲门投诉。
去年， 无印良品曾表示MUJI HOTEL SHENZHEN“不会卖得太贵”，参照对象是同样位于深业上城的五星级酒店文华东方。 MUJI HOTEL SHENZHEN正式价格公布之后，对于深圳消费水平而言，房间价格定得也的确不高，且不随淡旺季而产生价格波动。
“我们认为不应该有个忙季和淡季，360天，24小时都是提供一样的服务。”株式会社良品计划总裁兼执行董事松崎晓对界面新闻说。
“定这个价格是有讲究的，无印良品本身是面向大众的品牌，酒店也要和产品定位匹配，我们毕竟不是豪华酒店，不需要定个很高的价，”深业集团常务副总经理郝继霖对界面新闻说道。郝继霖是深业上城的操盘手，他上一个名声在外的项目是广州太古汇。
按照深业集团的说法，极简的概念不仅用在房间装修上，还有服务的内容，MUJI HOTEL SHENZHEN也没有门童和行李服务员。“无印良品给了两个定价标准：收费要简单，大家要负担得起。这个价格包含了服务费、税费和早餐，每一天都是这个价钱。但也没什么折扣，只有住超过一个月，才有10%的折扣。我们的房间有限，只有粉丝、理解这个品牌的人才会来。”郝继霖补充。
事实上，深业上城并不是唯一一家接触无印良品，希望与其合作开酒店的购物中心，不过郝继霖称，他对MUJI Diner、 MUJI HOTEL都提出了许多设想和建议，最终说服了松崎晓。
关于无印良品为什么要开酒店，是否代表着这个以极简和克制为特征的品牌变得复杂起来。除了开酒店，无印良品几乎覆盖了衣食住行方方面面，即使在服装品类，产品线也越来也多。一年前，我们曾就此询问过松崎晓，他否认了这种说法，称“无论是什么业务，都是在同一个理念下的分支”。
一年后，郝继霖对松崎晓的解释有了进一步的说明。
“MUJI HOTEL楼下就是无印良品的店铺，你去那里看看，可以看到MUJI to GO。无印良品关心旅行，也就自然从旅行用品延伸到旅行中所要住的地方，其实它没有改变。 ”郝继霖对界面新闻说道。MUJI to GO是无印良品为旅行爱好者设立的陈列区，出售牙刷、颈枕、小瓶装洗浴用品等，方便酒店客人入住时补充旅行所需，或为顾客提案出行方式。
除了MUJI to GO，深业上城的无印良品店内还有从全球寻找、发现而来的生活良品“Found MUJI”，出售书籍的MUJI BOOKS，定期邀请艺术家和手工匠人来对话的开放空间Open MUJI等。此外，这家全国第三大的店铺内，在售的还有与无印良品同属于良品计画集团的家居品牌IDÉE。顾客可以前往家具搭配咨询受理台，由无印良品家具搭配顾问提供定制的家居生活设计方案。
在MUJI HOTEL SHENZHEN下榻的住客，一日三餐都可以在MUJI Diner完成，而MUJI Diner内设有的吧台，取代了一般酒店的行政酒廊。不用期待MUJI Diner可以吃到日本料理，因为这家餐堂所提供的选择非常家常——日本伊贺、中国新疆和意大利迪赛奥的“家庭菜肴”。
早餐有日式套餐、洋式套餐及中式套餐三个选项；午餐也是以午市套餐形式提供，有3品、4品、5品套餐、肉酱芝士意大利面和黄油鸡肉咖喱饭套餐；晚餐自由度更高些。可自由选择主厨特选开胃菜拼盘、冷菜色拉、牛排、意面和甜点等。
酒吧区
据悉，MUJI HOTEL SHENZHEN最近一个月内的房间都已经预订完毕。想要来睡一晚的话，需要注意的是，MUJI HOTEL SHENZHEN不在携程、去哪儿等平台上开放销售，所有预订都要在无印良品的自有平台上完成。
""")

t1.similarity(t2)
```

Output like this :

```

0000000001111101010011110000110111011110111011110111010101111010
0000000001111110010011110010110111011010111000110011000001111001
Hamming Distance is  11
Similarity is 0.828125

```

#### Bag-of-Words(BoW) 
Bag-of-Words model builds the simplest connection between passage and words. It ignores the order of the sentences, phrases of course, and words. Because of this, we can simply construct a vector to represent one passage. From the corpura, we get the dictionary(word-index dict). Then in one passage, each element of the vector based on the dictionary is the TF-IDF value. We use this vector as the representation of the passage, the similarity of two passages is avaliable(Consin, Jabcard, etc.).   

We can have a try :  

```python

from huhu_seg.bow import BOW, Corpura
l = [
"""
首家无印良品酒店深圳开业：定价950元起，没有门童行李员
1月18日，全球首家无印良品（MUJI）酒店在深圳正式开业。酒店共79间客房，定价从950元至2500元不等，预计将于今年3月和明年春季于北京和日本银座再开两家。
确切地说，此次开业的酒店属于无印良品全球首个“三合一项目”的一部分。这个项目包括了无印良品位于深圳深业上城的店铺、无印良品餐堂（MUJI Diner）和无印良品酒店（MUJI Hotel Shenzhen）。除了酒店是无印良品在全球开出的首家之外，此次新开的餐堂也是无印良品继上海旗舰店之后开出的第二家。
无印良品深圳三合一项目开业
无印良品“三合一项目”选址位于深圳市福田区的深业上城城市综合体。据株式会社良品计画代表取缔役社长松崎晓介绍，无印良品酒店整体理念和客房内的设计由无印良品把控，运营则由深业上城的开发商、深业集团旗下的深圳深业酒店管理有限公司执行，“无印良品的盈利主要来自冠名费”。
谈到开酒店的好处时，松崎晓称，顾客在酒店入住后可以为无印良品的产品、服务提供意见，公司可以根据顾客反馈而做出改进。
无印良品酒店大堂
无印良品深圳酒店共设置了79间客房，面积从26平方米到61平方米不等，价格分为950元、1085元、1300元、1480元和2500元五档。
无印良品酒店定价从950元至2500元不等
尽管无印良品酒店客房的定价不算便宜，但深业置地常务副总经理郝继霖认为，这一收费还是简单合理的，“首先，大家要负担得起，这不是一个奢华的酒店；另外，收费要简单，950元包含了税、早餐，不再收取任何服务费。而且我们每天都是这个价钱，没有浮动，情人节、新年都是一个价。”
深业置地有限公司总经理徐恩利也一再强调，从零售跨界到酒店领域的无印良品运营酒店的独特之处——追求极简，满足基本的需求，而不是过度的服务，因此酒店不安排门童和行李员等，但安排了休闲顾问，可以为住客提供深圳的休闲、游玩建议。
无印良品酒店内部
郝继霖介绍，无印良品酒店目前也没有与任何第三方酒店预订平台合作，订房只能通过无印良品的自有平台完成，价格除了连续订一个月有9折优惠外，价格没有弹性。在谈到背后逻辑时，他称：“因为我们是个小酒店，来住的一般都是粉丝，了解这个文化。”
无印良品酒店秉承了MUJI的一贯风格基因，其大堂没有一般酒店常见的大吊灯，酒店房间内包括床上用品等70%的物品都来自无印良品，房间内的烧水壶、洗浴用品、拖鞋和挂式CD机等都是无印良品的招牌产品。房间内墙上涂有一面硅藻泥，以海洋的硅藻土为主要原料，有吸收甲醛和防止墙壁发霉的作用。
无印良品酒店房间内，有70%的物品都来自无印良品
当被问及无印良品下一步的扩张计划时，松崎晓表示，目前，无印良品在中国有230家店铺，到2020年为止的一个目标是，每年新开20家店，改装30家原有店铺。“我们从来不说要开1000家或5000家店。我们不追求数量，也不追求规模。不会说一定要开多少家店。”
据介绍，目前无印良品80%的店铺集中在一二线城市，但松崎晓称，无印良品开店“不拘泥于开在几线城市，只是开在有无印良品粉丝的地方”。但他也谈到了无印良品大型店铺的开店计划——此前全国范围内仅在上海、成都有2家大型旗舰店，将来要翻3倍，即开到6家。
此次深圳的无印良品酒店开业后，另外两家酒店也将于今年3月和明年春季，先后在北京和日本银座开张。
“但除了这三家之外，目前没有其他的酒店计划。”松崎晓表示。
""",
"""
全球首家MUJI HOTEL今天开业 我们提前去住了一晚
在房间里，有70%的物品都来自无印良品，可以在店内买到。
自从无印良品将要把全球首家MUJI HOTEL开在深圳的深业上城这一消息确定之后，很多人都在好奇酒店做出来最终会是怎样的。1月18日，MUJI HOTEL SHENZHEN正式对外开业。确切地说，开业的是无印良品的“三合一项目”——中国第三大的无印良品店铺、全球第2家MUJI Diner无印良品餐堂以及MUJI HOTEL。
一年前，当MUJI HOTEL还在施工时界面新闻曾经到访，当时已经知道负责设计MUJI HOTEL SHENZHEN的团队，来自无印良品的创始之一杉本贵志所拥有的工作室Super Potato。一年过去了，Super Potato对MUJI HOTEL SHENZHEN提及的一些设想已经实现，比如，切割废旧木材并贴在墙上以作装饰；购买一艘旧渔船摆放在酒店区域内，以纪念深圳曾经是座小渔村等等。
但更多未曾公布的细节，需要真正走进去才能一探究竟。
关于MUJI HOTEL的一些数据：
房间内有70％的物品是来自于无印良品，换而言之是可以在店内购买的
一共有79间客房，分布在深业上城的4楼至6楼
3楼设有300平方米的会议室，通过可移动墙面可分隔成三处独立空间，若完全开放，则可作为能容纳200人的小剧场
客房按面积和设施共分为5种房型，26平方米到61平方米不等，房价从950元起
有别于一般酒店前台连着大堂的设计，MUJI HOTEL SHENZHEN的前台和大堂是分开的。由于深业上城依山而建，酒店位于山坡的上方，所以酒店前台在二楼，而大堂则放在了三楼。这两个功能区的面积都不大，也没有酒店常见的大吊灯。但由于层高较高，两个空间并不显得压抑。
前台
大堂，一侧的书墙摆放着650多本书，住客可以带回房间阅读
会议室
MUJI HOTEL SHENZHEN的走廊灯光亮度，和房间内的灯光亮度保持一致。走廊里有缓缓的音乐，和无印良品店铺内播放的音乐也如出一辙。
房间内的烧水壶、洗浴用品、拖鞋等物都是无印良品的招牌产品。房间里还有深泽直人设计的那只著名的挂式CD机，遥控器床头，可以随时开关。
洗漱包内是牙刷、牙膏、浴帽等，没有梳子，所以要记得自备
房间内涂有一面硅藻泥，这种装修材质在南方地区的使用比较常见，以海洋的硅藻土为主要原料，有吸收甲醛和防止墙壁发霉的作用——在回南天漫长深圳，一到冬春之交墙壁能潮湿得淌下水来。
深业上城处在深圳商业最发达的福田区，但由于周围是莲花山和笔架山，夜里十分安静。床垫软硬适中，但比起无印良品在售的床品，酒店的床单和被套却不够柔软。为了测试酒店房间的隔音效果如何，我们想到了晚上在房间里打开“唱吧”唱了陈粒的《虚拟》。飙了几遍之后，并没有人来敲门投诉。
去年， 无印良品曾表示MUJI HOTEL SHENZHEN“不会卖得太贵”，参照对象是同样位于深业上城的五星级酒店文华东方。 MUJI HOTEL SHENZHEN正式价格公布之后，对于深圳消费水平而言，房间价格定得也的确不高，且不随淡旺季而产生价格波动。
“我们认为不应该有个忙季和淡季，360天，24小时都是提供一样的服务。”株式会社良品计划总裁兼执行董事松崎晓对界面新闻说。
“定这个价格是有讲究的，无印良品本身是面向大众的品牌，酒店也要和产品定位匹配，我们毕竟不是豪华酒店，不需要定个很高的价，”深业集团常务副总经理郝继霖对界面新闻说道。郝继霖是深业上城的操盘手，他上一个名声在外的项目是广州太古汇。
按照深业集团的说法，极简的概念不仅用在房间装修上，还有服务的内容，MUJI HOTEL SHENZHEN也没有门童和行李服务员。“无印良品给了两个定价标准：收费要简单，大家要负担得起。这个价格包含了服务费、税费和早餐，每一天都是这个价钱。但也没什么折扣，只有住超过一个月，才有10%的折扣。我们的房间有限，只有粉丝、理解这个品牌的人才会来。”郝继霖补充。
事实上，深业上城并不是唯一一家接触无印良品，希望与其合作开酒店的购物中心，不过郝继霖称，他对MUJI Diner、 MUJI HOTEL都提出了许多设想和建议，最终说服了松崎晓。
关于无印良品为什么要开酒店，是否代表着这个以极简和克制为特征的品牌变得复杂起来。除了开酒店，无印良品几乎覆盖了衣食住行方方面面，即使在服装品类，产品线也越来也多。一年前，我们曾就此询问过松崎晓，他否认了这种说法，称“无论是什么业务，都是在同一个理念下的分支”。
一年后，郝继霖对松崎晓的解释有了进一步的说明。
“MUJI HOTEL楼下就是无印良品的店铺，你去那里看看，可以看到MUJI to GO。无印良品关心旅行，也就自然从旅行用品延伸到旅行中所要住的地方，其实它没有改变。 ”郝继霖对界面新闻说道。MUJI to GO是无印良品为旅行爱好者设立的陈列区，出售牙刷、颈枕、小瓶装洗浴用品等，方便酒店客人入住时补充旅行所需，或为顾客提案出行方式。
除了MUJI to GO，深业上城的无印良品店内还有从全球寻找、发现而来的生活良品“Found MUJI”，出售书籍的MUJI BOOKS，定期邀请艺术家和手工匠人来对话的开放空间Open MUJI等。此外，这家全国第三大的店铺内，在售的还有与无印良品同属于良品计画集团的家居品牌IDÉE。顾客可以前往家具搭配咨询受理台，由无印良品家具搭配顾问提供定制的家居生活设计方案。
在MUJI HOTEL SHENZHEN下榻的住客，一日三餐都可以在MUJI Diner完成，而MUJI Diner内设有的吧台，取代了一般酒店的行政酒廊。不用期待MUJI Diner可以吃到日本料理，因为这家餐堂所提供的选择非常家常——日本伊贺、中国新疆和意大利迪赛奥的“家庭菜肴”。
早餐有日式套餐、洋式套餐及中式套餐三个选项；午餐也是以午市套餐形式提供，有3品、4品、5品套餐、肉酱芝士意大利面和黄油鸡肉咖喱饭套餐；晚餐自由度更高些。可自由选择主厨特选开胃菜拼盘、冷菜色拉、牛排、意面和甜点等。
酒吧区
据悉，MUJI HOTEL SHENZHEN最近一个月内的房间都已经预订完毕。想要来睡一晚的话，需要注意的是，MUJI HOTEL SHENZHEN不在携程、去哪儿等平台上开放销售，所有预订都要在无印良品的自有平台上完成。
"""
]
c = Corpura(l)

a = BOW(l[0], c)
b = BOW(l[1], c)
sim = a.similarity(b)

```

the output :

```
Find 471 unique words
Sim is  0.8135632082626852
```

  
## TO-DO List
The TO-DO below shows what I have done and the next-steps :  
- [x] Implementation of MMSEG segmentor
- [ ] Optimization for dictionary indexing
- [x] Named Entity Recognition
- [x] Keywords extraction
- [x] Similarity computing of texts
- [ ] Extraction of topic-phrase for news 

## Referrence
[1] [MMSEG: A Word Identification System for Mandarin Chinese Text Based on Two Variants of the Maximum Matching Algorithm](http://technology.chtsai.org/mmseg/)  
[2] [fxsjy/jieba](https://github.com/fxsjy/jieba)  
[3] [词图的生成](http://www.hankcs.com/nlp/segment/the-word-graph-is-generated.html)   
[4] [News Keyword Extraction for Topic Tracking](http://ieeexplore.ieee.org/document/4624203/)  
[5] [TextRank: Bringing Order into Texts](https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf)  
[6] [Similarity Estimation Techniques from Rounding Algorithms](https://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/CharikarEstim.pdf)  
[7] [基于角色标注的中国人名自动识别研究](http://www.nlp.org.cn/Admin/kindeditor/attached/file/20130508/20130508094537_92322.pdf)  
[8] [实战HMM-Viterbi角色标注中国人名识别](http://www.hankcs.com/nlp/chinese-name-recognition-in-actual-hmm-viterbi-role-labeling.html)  


