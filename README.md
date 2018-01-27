# HuhuSeg
Simple Chinese segmentor based on the four ambiguity-resolving rules by **MMSEG**[1] and examples.  

HuhuSeg implemented a simple but graceful words-gram generation enlightened by **HanLP**[3]. And the dictionary(including the words tag and frequency) was included from **jieba**[2]. 

## How to use 
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
  
## TO-DO List
The TO-DO below shows what I have done and the next-steps :  
- [x] Implementation of MMSEG segmentor
- [ ] Optimization for dictionary indexing
- [ ] Named Entity Recognition
- [ ] Keywords extraction
- [ ] Extraction of topic-phrase for news 

## Referrence
[1] [MMSEG: A Word Identification System for Mandarin Chinese Text Based on Two Variants of the Maximum Matching Algorithm](http://technology.chtsai.org/mmseg/)  
[2] [fxsjy/jieba](https://github.com/fxsjy/jieba)  
[3] [词图的生成](http://www.hankcs.com/nlp/segment/the-word-graph-is-generated.html)
