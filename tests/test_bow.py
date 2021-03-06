#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from huhu_seg.bow import BOW, Corpura

start = time.time()
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
duration = time.time() - start
print('Runs %.2f s' % duration)

