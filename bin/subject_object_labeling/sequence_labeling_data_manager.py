import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../bert")))
import tokenization
import data
import bilstm__cnn_crf.bilstm__cnn_crf
import jieba

print("if not have raw data, please dowload data from http://lic2019.ccf.org.cn/kg !")

class Model_data_preparation(object):

    def __init__(self, DATA_INPUT_DIR="raw_data", DATA_OUTPUT_DIR="SKE_2019_tokened_labeling",
                 vocab_file_path="vocab.txt", do_lower_case=True):
        # BERT 自带WordPiece分词工具，对于中文都是分成单字
        self.bert_tokenizer = tokenization.FullTokenizer(vocab_file=self.get_vocab_file_path(vocab_file_path),
                                                         do_lower_case=do_lower_case)  # 初始化 bert_token 工具
        self.DATA_INPUT_DIR = self.get_data_input_dir(DATA_INPUT_DIR)
        self.DATA_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), DATA_OUTPUT_DIR)
        print("数据输入路径：", self.DATA_INPUT_DIR)
        print("数据输出路径：", self.DATA_OUTPUT_DIR)

    def get_data_input_dir(self, DATA_INPUT_DIR):
        DATA_INPUT_DIR = os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")), DATA_INPUT_DIR)
        return DATA_INPUT_DIR

    def get_vocab_file_path(self, vocab_file_path):
        vocab_file_path = os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../../pretrained_model/chinese_L-12_H-768_A-12")), vocab_file_path)
        return vocab_file_path

    #序列标注对齐：由原始数据文件生成标注好的序列文件
    def subject_object_labeling(self, spo_list, text , model , lexicon , max_len ):
        #以关系为 key 分组spo_list
        def _spo_list_to_spo_predicate_dict(spo_list):
            spo_predicate_dict = dict()
#            print( spo_list )
            for spo_item in spo_list:
                predicate = spo_item[1]
                subject = spo_item[2]
                object = spo_item[0]
                spo_predicate_dict.setdefault(predicate, []).append((subject, object))
            return spo_predicate_dict

        def boo( a , b , l , n , c ):
#            for i in range( len( b ) - l ) :
#                if b[ l + i ] == a[ n ]:
#                    c.append( l + i )
#                    if l == len( b ) - 1:
#                        if n == len( a ) - 1 :
#                            return c
#                        else:
#                            return False
#                    else:
#                        if n == len( a ) - 1 :
#                            return c
#                        else:
#                            r = boo( a , b , l + i + 1 , n + 1 , c )
#                            if r:
#                                return r
#                else:
#                    continue
#            return False
            text_tokened = b
            so_tokened = a
            r = []
            def s( z , c ):
                for n in range( z , len( text_tokened ) ):
                    if c == text_tokened[ n ]:
                        c = n
                        return True , c
                return False , c
            
            for m in range( 0 , len( so_tokened ) ):
                if( len( r ) >= 1 ):
                    b , l = s( r[ len( r ) - 1 ] + 1 , so_tokened[ m ] )
                else:
                    b , l = s( 0 , so_tokened[ m ] )
                if b:
                    r.append( l )
                else:
                    b , c = s( 0 , so_tokened[ m ] )
                    if b:
                        r.append( c )
            if len( r ) == len( so_tokened ):
                return r
            else:
                return False
            
        def connect( so_tokened ):

            r = []
            set = -1
            for k in range( 0 , len( so_tokened ) ):
                if not so_tokened[ k ].isdigit():
                    if set != -1:
                        s = ''
                        for m in range( set , k ):
                            s += so_tokened[ m ]
                        r.append( s )
                        r.append( so_tokened[ k ] )
                    else:
                        r.append( so_tokened[ k ] )
                    set = -1
                else:
                    if k == len( so_tokened ) - 1:
                        if set != -1:
                            s = ''
                            for m in range( set , k + 1 ):
                                s += so_tokened[ m ]
                            r.append( s )
                        else:
                            r.append( so_tokened[ k ] )
                    if set == -1:
                        set = k

        
        # 在列表 k 中确定列表 q 的位置
        def _index_q_list_in_k_list(q_list, k_list):
            """Known q_list in k_list, find index(first time) of q_list in k_list"""
            q_list_length = len(q_list)
            k_list_length = len(k_list)
#            print( q_list )
#            print( k_list )
            r = boo( q_list , k_list , 0 , 0 , [] )
#            for idx in range(k_list_length - q_list_length + 1):
#                t = [q == k for q, k in zip(q_list, k_list[idx: idx + q_list_length])]
                # print(idx, t)
#            if r:#all(t):
                # print(idx)
            idx_start = r#idx
            return idx_start

        # 给主体和客体表上BIO分割式类型标签
        def _labeling_type(subject_object, so_type , to ):
            tokener_error_flag = False
            
#            text = subject_object
#            splitText,predLabel=bilstm__cnn_crf.bilstm__cnn_crf.word_seg_by_sentences(to.replace('\n', '').replace('\r', '').replace(' ', ''),model,lexicon,max_len)
#            print( to )
#            so_tokened = to.split( ' ' )
            so_tokened = list( to.replace( '\xa0' , '=' ).replace( ' ' , '@' ).lower() )#self.bert_tokenizer.tokenize( to.replace( ' ' , '@' ) )
#            print( so_tokened )
            

            
            so_tokened = so_tokened
            so_tokened_length = len(so_tokened)
            idx_start = _index_q_list_in_k_list(q_list=so_tokened, k_list=text_tokened)
            if idx_start == False :#is None:
                tokener_error_flag = True
                '''
                实体: "1981年"  原句: "●1981年2月27日，中国人口学会成立"
                so_tokened ['1981', '年']  text_tokened ['●', '##19', '##81', '年', '2', '月', '27', '日', '，', '中', '国', '人', '口', '学', '会', '成', '立']
                so_tokened 无法在 text_tokened 找到！原因是bert_tokenizer.tokenize 分词增添 “##” 所致！
                '''
                #            text_tokened = b
                r = []
                def s( z , c ):
                    for n in range( z , len( text_tokened ) ):
                        if c == text_tokened[ n ]:
                            c = n
                            return True , c
                    return False , c
                
                for m in range( 0 , len( so_tokened ) ):
                    if( len( r ) >= 1 ):
                        b , l = s( r[ len( r ) - 1 ] + 1 , so_tokened[ m ] )
                    else:
                        b , l = s( 0 , so_tokened[ m ] )
                    if b:
                        r.append( l )
                    else:
                        b , c = s( 0 , so_tokened[ m ] )
                        if b:
                            r.append( c )
                if len( r ) == len( so_tokened ):
                    tokener_error_flag = False
                    idx_start = r
                    labeling_list[idx_start[0]] = "B-" + so_type
    #                print( labeling_list )
                    if so_tokened_length == 2:
                        labeling_list[idx_start[1]] = "I-" + so_type
                    elif so_tokened_length >= 3:
    #                    print( idx_start )
                        for k in range( 1 , len( idx_start ) ):
                            labeling_list[idx_start[k] ] = "I-" + so_type
    #                        labeling_list[idx_start[k]: idx_start[1 + so_tokened_length] ] = ["I-" + so_type] * (so_tokened_length - 1)
                else:
                    tokener_error_flag = True
                    
                    
                    
                self.bert_tokener_error_log_f.write(subject_object + " @@ " + text + "\n")
                self.bert_tokener_error_log_f.write(str(so_tokened) + " @@ " + str(text_tokened) + "\n")
            else: #给实体开始处标 B 其它位置标 I
                labeling_list[idx_start[0]] = "B-" + so_type
#                print( labeling_list )
                if so_tokened_length == 2:
                    labeling_list[idx_start[1]] = "I-" + so_type
                elif so_tokened_length >= 3:
#                    print( idx_start )
                    for k in range( 1 , len( idx_start ) ):
                        labeling_list[idx_start[k] ] = "I-" + so_type
#                        labeling_list[idx_start[k]: idx_start[1 + so_tokened_length] ] = ["I-" + so_type] * (so_tokened_length - 1)
            print( labeling_list )      
            return tokener_error_flag

        t = text.replace('\n', '').replace('\r', '').replace(' ', '=')
        text = t
        splitText = ' '.join( jieba.cut( text , cut_all = False ) )
#        splitText,predLabel=bilstm__cnn_crf.bilstm__cnn_crf.word_seg_by_sentences(text,model,lexicon,max_len)
        tt = splitText.replace( '\xa0' , '=' ).replace( ' ' , '@' )
        text_tokened = list( tt.lower() )#self.bert_tokenizer.tokenize(tt)
#        print( text_tokened )
        
        text_tokened_not_UNK = text_tokened
        
#        text_tokened = self.bert_tokenizer.tokenize(text)
#        text_tokened_not_UNK = self.bert_tokenizer.tokenize_not_UNK(text)

        spo_predicate_dict = _spo_list_to_spo_predicate_dict(spo_list)
        for predicate, spo_list_form in spo_predicate_dict.items():
            tokener_error_flag = False
            labeling_list = ["O"] * len(text_tokened)
            for (spo_subject, spo_object) in spo_list_form:
                
                b1 = boo( spo_subject.replace(' ', '=') , splitText , 0 , 0 , [] )
                if b1 == False or b1 == []:
                    s1 = self.bert_tokenizer.tokenize(spo_subject.replace(' ', '='))
                    s1 = str( s1 )
                else:
                    s1 = tt[ b1[ 0 ] ]
                    for k in range( 1 , len( b1 ) ):
                            if b1[ k ] - 1 == b1[ k - 1 ]:
                                s1 = s1 +  tt[ b1[ k ] ]
                            else:
                                s1 = s1 + ' ' + tt[ b1[k] ]
                b2 = boo( spo_object.replace(' ', '=') , splitText , 0 , 0 , [] )
                if b2 == False:
                    s2 = self.bert_tokenizer.tokenize(spo_subject.replace(' ', '='))
                    s2 = str( s2 )
                else:
                    s2 = tt[ b2[ 0 ] ]
                    for k in range( 1 , len( b2 ) ):
                            if b2[ k ] - 1 == b2[ k - 1 ]:
                                s2 = s2 +  tt[ b2[ k ] ]
                            else:
                                s2 = s2 + ' ' + tt[ b2[k] ]
                
                spo_s = s1.lower()
                spo_o = s2.lower()
#                print( b1 )
#                print( b2 )
                flag_A = _labeling_type(spo_subject.replace(' ', '='), "SUB" , spo_s )
                flag_B = _labeling_type(spo_object.replace(' ', '='), "OBJ" , spo_o )
                if flag_A or flag_B:
                    tokener_error_flag = True

            #给被bert_tokenizer.tokenize 拆分的词语打上特殊标签[##WordPiece]
            for idx, token in enumerate(text_tokened):
                """标注被 bert_tokenizer.tokenize 拆分的词语"""
                if token.startswith("##"):
#                    print( idx )
#                    print( token )
                    labeling_list[idx] = "[##WordPiece]"
            if not tokener_error_flag:
                self.token_label_and_one_prdicate_out_f.write(" ".join(labeling_list)+"\t"+predicate+"\n")
                self.text_f.write(text + "\n")
                self.token_in_f.write(" ".join(text_tokened)+"\t"+predicate+"\n")
                self.token_in_not_UNK_f.write(" ".join(text_tokened_not_UNK) + "\n")



    #处理原始数据
    def separate_raw_data_and_token_labeling(self):
        if not os.path.exists(self.DATA_OUTPUT_DIR):
            os.makedirs(os.path.join(self.DATA_OUTPUT_DIR, "train"))
            os.makedirs(os.path.join(self.DATA_OUTPUT_DIR, "valid"))
            os.makedirs(os.path.join(self.DATA_OUTPUT_DIR, "test"))

        for file_set_type in ["train", "valid"]:
            print(os.path.join(os.path.join(self.DATA_OUTPUT_DIR, file_set_type)))
            self.token_label_and_one_prdicate_out_f = open(os.path.join(os.path.join(self.DATA_OUTPUT_DIR, file_set_type), "token_label_and_one_prdicate_out.txt"), "w", encoding='utf-8-sig')
            self.bert_tokener_error_log_f = open(os.path.join(os.path.join(self.DATA_OUTPUT_DIR, file_set_type), "bert_tokener_error_log.txt"), "w", encoding='utf-8-sig')

            self.text_f = open(os.path.join(os.path.join(self.DATA_OUTPUT_DIR, file_set_type), "text.txt"), "w", encoding='utf-8-sig')
            self.token_in_f = open(os.path.join(os.path.join(self.DATA_OUTPUT_DIR, file_set_type), "token_in.txt"), "w", encoding='utf-8-sig')
            self.token_in_not_UNK_f = open(os.path.join(os.path.join(self.DATA_OUTPUT_DIR, file_set_type), "token_in_not_UNK.txt"), "w", encoding='utf-8-sig')

            if file_set_type == "train":
                path_to_raw_data_file = "train.csv"
            elif file_set_type == "valid":
                path_to_raw_data_file = "dev.csv"
            else:
                pass
            texts , spo_lists = data.csv_( os.path.join(self.DATA_INPUT_DIR, path_to_raw_data_file) ) 
            c = 0
            
            model , lexicon , max_len = bilstm__cnn_crf.bilstm__cnn_crf.tokenizer()

            while c in range( len( texts ) ):
                spo_list = spo_lists[ c ]
                text = texts[ c ]
                self.subject_object_labeling(spo_list=spo_list, text=text , model = model , lexicon = lexicon , max_len = max_len )
                c += 1
                print ( c )
            count_numbers = c
            print("all numbers", count_numbers)
            self.text_f.close()
            self.token_in_f.close()
            self.token_in_not_UNK_f.close()
            self.token_label_and_one_prdicate_out_f.close()
            self.bert_tokener_error_log_f.close()

if __name__=="__main__":
    DATA_INPUT_DIR = "raw_data"
    DATA_OUTPUT_DIR = "sequence_labeling_data"
    model_data = Model_data_preparation(DATA_INPUT_DIR=DATA_INPUT_DIR, DATA_OUTPUT_DIR=DATA_OUTPUT_DIR)
    model_data.separate_raw_data_and_token_labeling()

