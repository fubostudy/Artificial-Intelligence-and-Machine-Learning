from interface import Interface_base
from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary
import numpy as np
import jieba
import os,sys
np.random.seed(1337)  
sys.setrecursionlimit(1000000)

class Word2vec(Interface_base):
   
    def __init__(self):
        Interface_base.__init__(self)
        
    # 创建词语字典，并返回每个词语的索引，词向量，以及每个句子所对应的词语索引
    def create_dictionaries(self,model=None,combined=None): 
        if (combined is not None) and (model is not None):           
            gensim_dict = Dictionary() # 空字典
            gensim_dict.doc2bow(model.wv.vocab.keys(),allow_update=True)          
            # 词:索引 ，这里的v:k+1和v:k的区别是下标从0还是1开始
            w2indx = {v: k+1 for k, v in gensim_dict.items()}                
            # 词:词向量，所有频数超过0的词语的词向量
            w2vec = {word: model[word] for word in w2indx.keys()}
            wordsList=[word for word in w2indx.keys()]     
            wordVectors=[model[word] for word in w2indx.keys()]
            np.save(self.wordsList,wordsList)            
            np.save(self.wordVectors,wordVectors)   
            np.savez(self.word_index,dic=w2indx)
            np.savez(self.word_vec,dic=w2vec)
            return w2indx, w2vec           
        else:
            print ('No data provided...')
    
    # 创建词语字典，并返回每个词语的索引，词向量，以及每个句子所对应的词语索引
    def word2vec_train(self,combined):
        # word2vec网络参数设置
        model = Word2Vec(     size=self.vocab_dim,
                         min_count=self.n_exposures,
                            window=self.window_size,
                           workers=self.cpu_count,
                              iter=self.n_iterations)
        
        model.build_vocab(combined) # 建立词典        
        model.train(combined,total_examples =model.corpus_count,epochs = model.iter) # 训练模型       
        model.save(self.Word2vec_model) # 保存word2vec网络模型

        # 创建词语字典，并返回每个词语的索引，词向量，以及每个句子所对应的词语索引
        index_dict, word_vectors = self.create_dictionaries(model=model,combined=combined)
        return   index_dict, word_vectors

    def train(self):    
        print ('Loading report Data...')
        file_w2v=self.load_w2v_file(self.filedir_train)        
        print ('Tokenising...')
        file_token = self.tokenizer(file_w2v)
        print ('Training a Word2vec model...')
        index_dict, word_vectors=self.word2vec_train(file_token)

   # 测试     
    def test(self):            
        w2indx=np.load(self.word_index)              #加载word_index.npz文件：{词：索引}，
        print('w2indx:',w2indx)                      #打印词文件的格式
        w2indx=w2indx['dic'][()]                     #注意必须这种形式读取保存的字典
        print('历史 词索引:',w2indx['历史'])           #打印"历史"这个词在字典的索引
        w2vec=np.load(self.word_vec)                 #加载word_vec.npz文件：{词：词向量}
        print('历史 词向量:',w2vec['dic'][()]['历史']) #读取字典，并打印"历史"这个词的词向量
        wl=np.load(self.wordsList)                   #加载wordsList.npy文件：整个词典
        wl = wl.tolist()                             #也可以以list方式进行读取
        print('词典长度:',len(wl))                     #打印词典list的长度
        #wl = [word.decode('UTF-8')  for word in wl]
        print('期货 词索引:',wl.index('期货'))          #打印期货这个词的索引
        vec=np.load(self.wordVectors)                #加载wordVectors.npy文件：词向量
        print('词向量长度:',len(vec))                  #打印词向量的长度
        print('第52个词向量:',vec[52])                 #打印第52个词向量

# w2=Word2vec()
# w2.train()
# w2.test()

    
    
    