theme: Bilingual Word embedding
reporter: zili
date: 2017-04-07
-----
### CORPUS
pairs|source|note
---|---|----
en-de|[European Parliament Proceedings Parallel Corpus v7](http://www.statmt.org/europarl/v7/)|
en-sv|[European Parliament Proceedings Parallel Corpus v7](http://www.statmt.org/europarl/v7/)|
en-fr|[European Parliament Proceedings Parallel Corpus v7/v8](http://www.statmt.org/wmt15/translation-task.html)|文章中使用的是Europarl v7/v8和News Commentary， 但原始News Commentary并未句对齐， 所以只用了Europarl v7/v8
en-zh|[FBIS parallel corpus](https://github.com/s-matthew-english/trst/tree/master/bilingual-ce-part1-LDC2003E14-FBIS-MultilanguageTexts)|不完全
### PREPROCESS
  - [x] tokenize(nltk.tokenize used in en,fr,sv,de; stanford word segmenter used in zh).
  - [x] remove stopwords(stopwords of en,fr,sv,de from nltk.stopwords, zh from ITNLP LAB OF HIT)
  - [x] remove punctuation marks.
  - [x] lower case
### TESTED MODELS
  - [x] BiSkip
  - [x] BiCVM
  - [ ] BiCCA
  - [ ] BiVCD
### TESTED TASKS
  - [x] Word Similarity
  - [x] QVEC
  - [x] Cross-lingual Dictionary Induction
  - [ ] Cross-lingual Document Classification
  - [ ] Cross-lingual Dependency Parsing
### RESULT
##### Word Similarity
pair|BiSkip|BiCVM|BiCCA|BiVCD
---|---|---|---|---
en-de|0.3253|0.3189|||
en-fr|0.3187|0.3071|||
en-sv|0.3234|0.2962|||
en-zh|0.3028|0.2204|||
##### QVEC
pair|BiSkip|BiCVM|BiCCA|BiVCD
---|---|---|---|---
en-de|0.359426|0.290998|||
en-fr|0.358955|0.299896|||
en-sv|0.364019|0.297837|||
en-zh|0.336311|0.273235|||
##### Cross-lingual Dictionary Induction
pair|BiSkip|BiCVM|BiCCA|BiVCD
---|---|---|---|---
en-de|0.7621052631578947|0.7452631578947368
en-fr|0.7443708609271523|0.7158940397350994
en-sv|0.7568359375|0.7529296875
en-zh|0.5950310559006211|0.5335403726708075
### REFERENCE
##### Word Similarity
pair|BiSkip|BiCVM|BiCCA|BiVCD
---|---|---|---|---
en-de|0.34|0.37|0.30|0.32
en-fr|0.35|0.39|0.31|0.36
en-sv|0.32|0.34|0.27|0.32
en-zh|0.34|0.39|0.30|0.31
##### QVEC
pair|BiSkip|BiCVM|BiCCA|BiVCD
---|---|---|---|---
en-de|0.40|0.31|0.33|0.37|
en-fr|0.40|0.31|0.33|0.38|
en-sv|0.39|0.31|0.32|0.37|
en-zh|0.40|0.32|0.33|0.38|
##### Cross-lingual Dictionary Induction
pair|BiSkip|BiCVM|BiCCA|BiVCD
---|---|---|---|---
en-de|79.7|74.5|72.4|62.5
en-fr|78.9|72.9|70.1|68.8
en-sv|77.1|76.7|74.2|56.9
en-zh|69.4|66.0|59.6|53.2
### CONCLUSION
1. 相对于文章作者，本次试验对语料库进行了前处理，而相应的任务性能下，相对于作者较低。这反应过多的预处理可能word embedding有影响。
2. BiSkip模型训练慢，需要对平行语料库做词对齐，性能强。BiCVM模型训练相对快，无需词对齐。在QVEC任务下，没有发现文章中的BiCVM $\gt$ BiSkip规律。造成的原因有两个：1、预处理。2、参数。
### STATE
##### doing
  - recode BiCCA model. (开源代码需要matlib)
##### to do
  - task: Cross-lingual Document Classification
  - task: Cross-lingual Dependency Parsing
##### stuck
  - BiVCD model. (无法获取开源代码，原文献描述不清)
##### finished
  - model: BiSkip
  - model: BiCVM
  - task: Word Similarity (modify)
  - task: QVEC (modify)
  - task: Cross-lingual Dictionary Induction (override)
#### unexpected
  - 模型训练时间比预期长
  - 部分算法需要重写
  - 刚开始自以为是非root用户，花了很长时间在编译上。
  - 开始处理语料库的时候走了些弯路，导致后续很多无意义计算。
  - 语料库下载耗时比预期长，en-fr语料库下载错了几次。
