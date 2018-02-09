#!/usr/bin/env python3

from huhu_seg.simhash import SimHash

t1 = SimHash("""
SpaceX的“猎鹰重型”成为地表最强大的火箭。（图源：CNN）
微信图片_20180207094359.gif
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

