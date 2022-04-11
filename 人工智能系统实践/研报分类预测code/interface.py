import jieba
import multiprocessing
import os
import numpy as np
from keras.preprocessing import sequence
import datetime

class Interface_base(object):
    
    def __init__(self):
        self.filedir_train = "./spider_report/"     # 训练数据集
        self.filedir_test = "./test_report/"        # 测试数据集（用于预测）

        # word2vec训练时的参数设置
        self.vocab_dim = 300                              # 每个词向量的维度
        self.n_exposures = 0                              # 词频大于0的都会被向量化
        self.window_size = 7                              # 窗口大小
        self.cpu_count = multiprocessing.cpu_count()      #多进程模块，统计cpu核数
        self.n_iterations = 1 
        self.w2v_file_path='./spider_report/'                # 用于训练词向量的文本
        self.wordsList='./word2vec_model/wordsList.npy'      # 词典
        self.wordVectors='./word2vec_model/wordVectors.npy'  # 词向量
        self.Word2vec_model='./word2vec_model/Word2vec_model.pkl'  # word2vec模型保存
        self.word_index='./word2vec_model/word_index.npz'    # {词：索引}
        self.word_vec='./word2vec_model/word_vec.npz'        # {词：词向量}
        
        # lstm的参数设置
        self.batch_size = 2      # 每次batch大小
        self.n_epoch = 5        # 训练轮数
        self.input_length = 550  # 每篇文本的长度固定时，这个值和self.maxlen相等     
        self.maxlen = 550        # 设定每篇文档的最大长度
        self.test_size=0.2       # 测试文本的比例
        self.pos_path='./lstm_train_data/pos/'      #积极训练集
        self.neg_path='./lstm_train_data2/neg/'      #消极训练集
        self.neu_path='./lstm_train_data2/neu/'      #中性训练集
        self.lstm_model='./lstm_model/lstm.yml'     #lstm模型保存
        self.lstm_weight='./lstm_model/lstm.h5'
        
        self.time=datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d%H%M_')

    # 对句子分词并去掉空格
    def tokenizer(self,text):
        # 注意这里必须把generator转换为list
        text = [list(jieba.cut(document.replace(' ', ''))) for document in text]
        return text

    # 加载训练文件    
    def load_w2v_file(self,w2v_file_path):        
        file_w2v=np.array([])       
        files= os.listdir(w2v_file_path) # 文件夹spider_report的文件路径
        for file in files:
            file_raw = os.path.join(w2v_file_path, file)
            text_dealed=self.text_proce(file_raw)
            file_w2v=np.append(file_w2v,text_dealed)
        return file_w2v

    # 对文本进行处理
    def text_proce(self,text_raw):
        str_tmp=''
        with open(text_raw, "r", encoding='utf-8') as f:
            yy=f.readlines()
            if len(yy)==1:  # 这里判断是为了避免 str_tmp=str_tmp+line+','的逗号一直添加
                str_tmp=yy[0]
            else:                      
                for line in yy:                    
                    line=line.strip()
                    if not line.startswith('<'):
                        str_tmp=str_tmp+line+'&'
                    else:
                        str_tmp=str_tmp+line[3:len(line)-4] # 这里是为了去除<p>,</p>字符
                str_tmp.replace(' ', '') # 去除空格                           
        with open(text_raw, "w", encoding='utf-8') as f: # 把处理过的文本重新写入 
            f.write(str_tmp)
        return str_tmp

    # 测试文本的向量化
    def file_test_vec(self,w2indx,file_reshape):
        #print('file_reshape:',file_reshape)
        data=[]
        for sentence in file_reshape:
            #print('sentence:',sentence)
            word_vec = []
            for word in sentence:
                try:
                    word_vec.append(w2indx[word])
                except:
                    word_vec.append(0)
            data.append(word_vec)
        # 每个句子所含词语对应的索引，后端截断和填0补充
        data= sequence.pad_sequences(data, maxlen=self.maxlen,padding='post',truncating='post')
        return data

        
        
        
        
        
        
        
        
    