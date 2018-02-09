=======
HuhuSeg
=======

HuhuSeg是一个基于 **MMSEG** [1]_ 的四种消歧规则和最大匹配方式的简单中文分词器，只有数百行代码。  

Simple Chinese segmentor based on the four ambiguity-resolving rules by **MMSEG** [1]_ and examples.

同时HuhuSeg实现了一个简单但是非常高效的词图生成方式，由 **HanLP** [3]_ 的启发而来。同时核心词典直接使用了**jieba** [2]_ 的词频词典。  

HuhuSeg implemented a simple but graceful words-gram generation enlightened by **HanLP** [3]_. And the dictionary(including the words tag and frequency) was included from **jieba** [2]_.  

How-to use
----------

Installation
~~~~~~~~~~~~

::

    pip3 install HuhuSeg

Segmentation
~~~~~~~~~~~~

如下代码为分词器的使用方式：

We can just try to segment the Chinese texts like this :  

.. code:: python

    from huhu_seg.segmentor import Segmentor

    s = Segmentor('为人民办公益')
    tokens = s.gen_tokens()
    for item in tokens:
        print(str(item))

And the output is :

::

    [frequency 295952 | p | length 1] 为
    [frequency 43719 | n | length 2] 人民
    [frequency 10314 | v | length 1] 办
    [frequency 404 | n | length 2] 公益

Keywords Extraction
~~~~~~~~~~~~~~~~~~~

TF-IDF Keywords Extraction
^^^^^^^^^^^^^^^^^^^^^^^^^^

HuhuSeg基于 **TF-IDF** [4]_ 算法实现了一个关键词提取器，IDF词频模型来源于针对接近100万条的wiki中文词条的分词统计，如下为使用方式： 

Now HuhuSeg supports the keywords extraction based on the **TF-IDF** [4]_ . Just have a try like :  

.. code:: python

    from huhu_seg.tfidf import TFIDF

    k = TFIDF('程序员(英文Programmer)是从事程序开发、维护的专业人员。一般将程序员分为程序设计人员和程序编码人员，但两者的界限并不非常清楚，特别是在中国。软件从业人员分为初级程序员、高级程序员、系统分析员和项目经理四大类。')
    list = k.extract_kw()
    for word, freq in list :
        print('[%s %f]' % (word, freq))

Output is :

::

    [程序员 0.735660]
    [人员 0.305123]
    [系统分析员 0.300264]
    [程序开发 0.232286]
    [项目经理 0.231476]

TextRank Keywords Extraction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在TF-IDF实现的关键词提取之外，这里还实现了基于 **TextRank** [5]_ 的提取算法，不依赖于庞大的IDF模型，而是试图在文本中词语的共现关系图里找到被Rank最高的词语。当然，除此之外，这里的代码实现的关键词提取还使用了一个小trick，在通过TextRank提取完关键词之后，会再次扫描文本，找到top关键词中是否有邻接词可以组成短语，如下面的提取“旅行青蛙”和“开发游戏”即是通过这种方式提取出来的。

By **TextRank** [5]_ , we can escape those huge and overwhelming IDF dictionaries, and try to find the relationship of words between the co-occuring gragh. As you can see in this output, we have a little trick to extract the better keywords with meaningful semantics: the extractor may scan the whole text to find if there are top keywords could construct the phrase. If it is true, we select them and build new keywords table. In the test, it seems to have the effective and better results.  

.. code:: python

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

We can see the output :

::

    [旅行青蛙 19.167803]
    [开发游戏 14.831004]
    [玩家 4.801199]
    [中国 3.508624]
    [用户 3.118792]

Similarity of Texts
~~~~~~~~~~~~~~~~~~~

SimHash
^^^^^^^

**SimHash** [6]_ , proposed by MS Charikar, as a LSH(Locality Sensitive Hash), can be used to detect the similarity of two passages. There is a simple implementation; by the IDF Model we have and the tfidf keywords extraction, we extract those Top-200 feature words and hash them. Summing and normalizing, we get the SimHash fingerprint. All is done, now we just compute the two's Hamming Distance, and the similarity is represented by the distance.

We can have a try :  

.. code:: python

    from huhu_seg.simhash import SimHash

    t1 = SimHash("""
    SpaceX的“猎鹰重型”成为地表最强大的火箭。（图源：CNN）
    助推火箭同时垂直着陆。（图源：网络）
    海外网2月7日电 被誉为世界最强大现役运载火箭的重型猎鹰火箭，当地时间周二（6日）下午3点45分左右在美国佛罗里达州肯尼迪航天中心发射成功。
    据美国有线电视新闻网（CNN）报道，约300万人收看了SpaceX的现场直播，为之欢呼。伊隆·马斯克周一（5日）在接受美国有线电视新闻网采访时说：“来自世界各地的人们将会看到这场伟大的火箭发射，同时也会是他们见过的最棒的烟火表演。”
    SpaceX的重型猎鹰火箭不仅将SpaceX首席执行官伊隆·马斯克安排的特斯拉跑车送入了太空，而且被成功回收了两枚一级助推火箭。发射成功后，伊隆·马斯克对记者说：“我还在试图消化这个成果，真像做梦一样。”SpaceX在2017年年初表示，有两位“太空游客”已经为乘重型猎鹰火箭进行环月旅行而付了一大笔定金。SpaceX当时表示，环月之旅2018年可能会实现，不过SpaceX后来没再给出新动向。
    据美国有线电视新闻网报道，早在2017年9月，伊隆·马斯克表示要在2020年在火星降落两艘货船，并计划建造“巨型猎鹰火箭”（BFR），如果火箭回收的部分可以“重复利用”，“人类探索火星的成本可以大大减少”。
    从科幻到现实并不是一蹴而就。从2008年9月28日猎鹰1号火箭首次成功发射，到如今的重型猎鹰火箭的成功发射背后，有着SpaceX付出的巨大努力。重型猎鹰火箭的成功发射，标志着SpaceX用其开创性技术撼动火箭行业的设想向前迈进了一步，而如今人类移民火星的梦想也前进了一步。
    """) 
    t2 = SimHash("""
    阿波罗时代的太空已斗转星移。
    　　美国当地时间2月6日，科技大亨伊隆·马斯克（Elon Musk）旗下SpaceX公司的新型火箭“猎鹰重型”（Falcon Heavy）在佛罗里达州的肯尼迪航天中心成功升空。
    　　这标志着人类航空史上的一个新的里程碑。50年前，曾在同样的发射平台上，土星5号运载火箭首次把人类带向月球，开启了“阿波罗”时代。

    　　运力堪比土星5号
    　　猎鹰重型发射成功后，美国总统特朗普发表Twitter称：“祝贺马斯克，祝贺SpaceX。这一胜利和NASA商业以及国际合作伙伴一起，继续展现美国最好的天才智慧。”
    　　马斯克也在猎鹰重型发射成功后通过Twitter表示：“从SpaceX发射的控制画面来看，毫无疑问一辆汽车已经进入了地球轨道。”
    　　SpaceX的竞争对手蓝色起源（Blue Origin）的创始人、亚马逊总裁贝佐斯也发表Twitter祝贺马斯克，不过只有非常简单的一个词：“Woohoo!”
    　　据美国有线电视新闻网CNN报道，有约300万人收看了SpaceX的现场直播。马斯克在接受CNN采访时说：“来自世界各地的人们将会看到这场伟大的火箭发射，同时也会是他们见过的最棒的烟火表演。”
    　　自大如马斯克，在新火箭发射前也有担忧。他此前曾表示，研发该新火箭遇上挑战，首次试射的成功率只有一半。 “我脑海曾经出现过一些画面，比如在发射平台上出现爆炸，或者有轮胎脱落滚开。” 他说。
    　　但幸运的是，上述种种都没有发生。
    　　“这就像一部科幻片终于走向了事实。”前NASA官员、麻省理工学院（MIT）阿波罗宇航教授Dava Newman表示：“他们做到了！太了不起了。”
    　　此次发射成功意味着“猎鹰重型”成为现役火箭中载荷量最重的一枚。在这次充满不确定性的试射中，马斯克为“猎鹰重型”选择了少而有趣的搭载物：价值10万美元的樱桃红特斯拉Roadster敞篷跑车，司机位坐着一个宇航服人偶，中控面板上显示着“不要慌张”（Don’t Panic）的字样，车上大卫·鲍伊（David Bowie）经典的歌声《Space Oddity》中反复唱道：“火星上的生活？”（Life on Mars?）。
    　　不过，此次发射也有美中不足的地方。 “猎鹰重型”由三枚SpaceX“猎鹰九号”火箭绑定在一起。与此前的SpaceX发射一样，最理想的状态是在发射后，这三枚火箭底部的推进器回到大气层降落地面，实现回收。但实际上，其中两个推进器成功在肯尼迪航天中心以南的划定范围内降落，而且两者的着陆架几乎是同时着地。第三个推进器由于推进剂不足，最终未能在目标地点降落，以每小时300英里的速度在水面坠毁。
    　　送跑车上太空
    　　“马斯克发送一辆特斯拉汽车到太空中，目的不是为了给车打广告或者玩科技情怀。” 中科院量子信息与量子科技创新研究员副研究院张文卓在接受第一财经记者采访时表示，“而是为了说明他的火箭有能力把几吨重的物品运送到远地轨道。这意味着美国未来或许要依靠SpaceX的火箭载人重返月球或者登陆火星。”
    　　“猎鹰重型”的设计目标是要载荷64吨进入近地轨道（距地球表面数百公里），相当于将五辆双层巴士送上太空。这样的载荷能力，是此前全球最强火箭“三角洲四号”（Delta IV Heavy）的两倍；但马斯克称，“猎鹰重型”的成本仅为“三角洲四号”的三分之一。
    　　“猎鹰重型”的成本预计在9000万美元左右，这一成本是美国航空航天局NASA正在建造的“太空发射系统”（Space Launch System，简称SLS）火箭的不到十分之一。SLS的目标是在2019年底前将宇航员以及货物运往深空甚至火星。
    　　不过马斯克的梦想前进了一大步，他的目标是要在火星上建一个城市。马斯克曾在2017年9月表示，将于2020年在火星降落两艘货船，并计划建造“巨型猎鹰火箭”（BFR）。他当时说：“如果火箭回收的部分可以重复利用，人类探索火星的成本可以大大减少。”
    　　不过在“猎鹰重型”上的投资加大令SpaceX不得不暂时搁置火星计划。公司总裁Gwynne Shotwell（肖特韦尔）曾表示：“公司已经将火星计划推迟到2020年启动，而不是2018年，因为我们觉得需要投入更多的资源在我们的载人航天项目和猎鹰重型计划。”
    　　随着火箭运力的不断增加，未来更大的卫星或者望远镜将能够被送上太空，目前可用的卫星均受制于搭载火箭的负荷能力。此外，人们可以把体积更大、功能更齐全的机械人送上火星表面，甚至更远的木星、土星或者冥王星。
    　　从科幻到现实并不是一蹴而就。从2008年9月28日猎鹰1号火箭首次成功发射，到2016年4月执行的CRS-8任务首次让第一节火箭在海上成功着陆，SpaceX创造了火箭回收的奇迹。不过，2016年9月，SpaceX开发的梅林火箭引擎（merlin rocket engine）在测试场发生爆炸，损坏了公司的两个试验区，公司的火箭发射任务也一度被迫中止。
    　　一直到去年2月，SpaceX启用了阿波罗登月时代的发射平台进行首次私人航天发射任务，将“龙”飞船送往国际空间站（ISS），被视作极具历史传承意义的航空领域的里程碑事件。
    　　如今，“猎鹰重型”的发射又开启了一个新的时代。这些计划包括在月球上建立起一个新的空间站，发射新的通信卫星和情报卫星，并将人类运往更深的太空目的地。去年2月，SpaceX曾表示，有两位“太空游客”已经为乘坐“猎鹰重型”火箭进行环月旅行预付了一大笔定金，环月之旅将于2018年实现。
    　　中美航空竞赛升级
    　　马斯克预估，SpaceX在“猎鹰重型”上的投资目前已经超过5亿美元，他还表示，这些资金完全来源于SpaceX内部，未使用纳税人的钱。
    　　马斯克最初使用他自己的1亿美元投资了SpaceX。在与波音公司和洛克希德·马丁公司进行了激烈的竞争之后，SpaceX累计已经获得了NASA超过65亿美元的货物运输合同，并且最终将承担把美国的宇航员运往国际空间站的任务。SpaceX还与一些私人公司签署协议，帮助其将卫星发送至轨道。此外，SpaceX还有望在2020年前得到美国国防部数十亿美元的合同。
    　　以马斯克为代表，美国航空航天局在PPP（私营公共合作）方面的步子迈得很大。以波音为代表的NASA传统合同商和以SpaceX为代表的“新航空”两大阵营的格局已经发生了根本的变化，也助推了美国航空业重返阿波罗时代的荣耀。
    　　值得注意的是，尽管中美在航空领域的差距依然明显，但中国也在迎头赶上。2003年起，中国就启动了载人航天任务，神州十一号将两名航天员发射升空。现在中国提出新的目标：在2022年前建造自己的空间站，在月球黑暗面登陆，并向火星发送探测车。
    　　美国国会议员不由提出一个问题：“在这场航天竞赛中我们是否输给了中国？”美中经济与安全审查委员会主席丹尼斯·谢伊（Dennis Shea）认为，中国采取了更深思熟虑、更全面的方法，太空计划将为中国创造机会，从经济、政治和外交等方面获得重要利益。
    　　华盛顿战略与国际问题研究中心（Center for Strategic and International Studies）资深副主席詹姆斯·刘易斯（James Lewis）也表示，尽管美国航空航天局已经成功登陆月球，但美国高度关注的2030年火星载人飞行计划一旦失败，中国便可以迎头赶上。
    """)
    t1.similarity(t2)


Output like this :

::

    0000000011100011111000010010110000110110101111001010100010001100
    0000000010100011111100000010110000110111101010001001100010001100
    Hamming Distance is  8
    Similarity is 0.875000


TO-DO List
----------

The TO-DO below shows what I have done and the next-steps :  

- Implementation of MMSEG segmentor [x] 

- Optimization for dictionary indexing [ ]

- Named Entity Recognition [ ] 

- Keywords extraction [x] 

- Similarity computing of texts [x] 

- Extraction of topic-phrase for news [ ] 

Referrence
----------

.. [1] [MMSEG: A Word Identification System for Mandarin Chinese Text Based on Two Variants of the Maximum Matching Algorithm](http://technology.chtsai.org/mmseg/)
.. [2] [fxsjy/jieba](https://github.com/fxsjy/jieba)
.. [3] [词图的生成](http://www.hankcs.com/nlp/segment/the-word-graph-is-generated.html). 
.. [4] [News Keyword Extraction for Topic Tracking](http://ieeexplore.ieee.org/document/4624203/)  
.. [5] [TextRank: Bringing Order into Texts](https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf)
.. [6] [Similarity Estimation Techniques from Rounding Algorithms](https://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/CharikarEstim.pdf)

