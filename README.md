# HuhuSeg
Simple Chinese segmentor based on the four ambiguity-resolving rules by **MMSEG**[1] and examples.  

HuhuSeg implemented a simple but graceful words-gram generation enlightened by **HanLP**[3]. And the dictionary(including the words tag and frequency) was included from **jieba**[2]. 

## How to use 
### Segmentation

We can just try to segment the Chinese texts like this :
```python
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

Now HuhuSeg supports the keywords extraction. Just have a try like :
```python
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
