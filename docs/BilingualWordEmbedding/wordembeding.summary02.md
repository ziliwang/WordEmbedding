theme: Bilingual Word embedding
reporter: zili
date: 2017-04-14
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
### TESTED MODELS
  - [x] BiSkip
  - [x] BiCVM
  - [x] BiCCA
  - [ ] BiVCD
### TESTED TASKS
  - [x] Word Similarity
  - [x] QVEC
  - [x] Cross-lingual Dictionary Induction
  - [ ] Cross-lingual Document Classification
  - [ ] Cross-lingual Dependency Parsing
### RESULT
##### Word Similarity
pair|Mono|BiSkip|BiCVM|BiCCA|BiVCD
---|---|---|---|---|---
en-de|0.265| **0.313** |0.225|0.264|-
en-fr|0.254| **0.277** |0.266|0.253|-
en-sv|0.248| **0.316** |0.241|0.249|-
en-zh|0.202| **0.289** |0.238|0.197|-
##### QVEC
pair|Mono|BiSkip|BiCVM|BiCCA|BiVCD
---|---|---|---|---|---
en-de| **0.375** | **0.375** |0.286| **0.375** |-
en-fr| **0.377** |0.367|0.300| **0.377** |-
en-sv|0.373|0.365|0.298| **0.377** |-
en-zh| **0.351** |0.343|0.276|0.301|-
##### Cross-lingual Dictionary Induction
pair|BiSkip|BiCVM|BiCCA|BiVCD
---|---|---|---|---
en-de| **0.771** |0.676|0.651|-
en-fr| **0.745** |0.712|0.486|-
en-sv| **0.786** |0.758|0.467|-
en-zh| **0.595** |0.524|0.452|-
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
1. 采不采用预处理（停用词，去非单词符号）对不同model在不同任务上性能的影响有差别。测试结果表明，不采用预处理有如下表现：

model|word similarity|QVEC|translation
---|---|---|---
word2vec| + | + | +
BiSkip| - | + | +
BiCVM| - | + | ?
+：提高，-：降低，?：在不同语言上的情况不一样

### STATE
##### doing
##### to do
##### abandon
  - BiVCD model. (无法获取开源代码，原文献描述不清)
  - task: Cross-lingual Document Classification
  - task: Cross-lingual Dependency Parsing
##### finished
  - recode BiCCA model.
  - model: word2vec
  - test: model performance with only tokenize
