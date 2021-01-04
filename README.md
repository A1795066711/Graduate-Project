# Graduation-Project

## Documents

### graph.svg
   The ***final graph*** formed in NEO4J based on the data set

### Relation Entity Extraction.pdf
   The architecture of the Relation & Entity Extraction model

### BiLSTM-CNN-CRF.pdf
   The structure of the segmentation model
    
## Project Intro
  
  It's a project aiming to solve some not high accuracy problems in NLP area particularly in Entity-Relation Extraction.
  
  For each data set for learning and prediction, processes will be:
  
  1. Text Segmentation
  
     The Training: The training data set would be added to one BiLSTM layer and one CNN layer in the same time, output of both would be the input for the CRF layer.
     
     The Prediction: Segmentation of the text.
     
     Comparation with some other models:（ cited from the [paper](http://www.cnki.com.cn/Article/CJFDTotal-DQXX201908002.htm) and the [project](https://github.com/FanhuaandLuomu/BiLstm_CNN_CRF_CWS) ）

                                                        MODEL           P           R            F1 
                                                        CRF             0.904       0.898        0.901 
                                                        LSTM            0.893       0.887        0.890 
                                                        BiLSTM          0.912       0.907        0.909 
                                                        BiLSTM-CNN-CRF  0.919644    0.906250     0.912898 
     
  2. Text Classification
     
     The training data is collected by the web crawler program from the Internet.
     
     Data would be like: { "some text" , its label } with 10 labels for all.
     
     CNN and RNN models are applied to this task.
     
     Comparation to other base models: （ cited from the [paper](http://cdmd.cnki.com.cn/Article/CDMD-83801-1018130739.htm) and the [project](https://github.com/gaussic/text-classification-cnn-rnn)）                 

                                                        Method        Precision Recall   F1 
                                                        ( Base models ) 
                                                        LR            0.8001    0.7752   0.7357 
                                                        MultinomialNB 0.9136    0.8527   0.8745 
                                                        SVM           0.8997    0.8527   0.8489 
                                                        ( Applied models ) 
                                                        CNN           0.96      0.96     0.96 
                                                        RNN           0.94      0.94     0.94 
                                                    
   3.Entity Relation Extraction:
   
   Google's BERT MODEL ( BERT-Base, Chinese: Chinese Simplified and Traditional, 12-layer, 768-hidden, 12-heads, 110M parameters ) 
   is applied in this part, ***with the improving of its segmentation codes by the BiLSTM-CNN-CRF model mentioned***.
     
   Results ( about the accuracy of relationships and relevant entities extracted ):
     
                                                        Schema：
                                                        Relationship          Subject     Object
                                                        Time of the event     Event       Time    
                                                        Area of the event     Event       Area       
                                                        Duration of the event Event       Duration    
                                                        Cause of the event    Event       Cause    
                                                        Lessons of the event  Event       Lessons    
                                                        Damage of the event   Event       Damage    
                                                        
                                                        Results：
                                                        Precision             Recall      F1 
                                                        0.6496                0.7917      0.7136
            
## Some details of the data

The data set is composed of plenty of pieces of texts about the electricity outage or blackout. 

Data preprocessing is about signing the texts with the relevant relationship, entities and labels for classification.  

## Some configurations
                                                        Harware:
                                                        
                                                        CPU                   Intel Core i7 
                                                        GPU                   GTX 
                                                        
                                                        Software:
                                                        
                                                        OS                     Windows 10 
                                                        Programming Language   Python     ( Version: 3.6 ) 
                                                        Framework              Tensorflow ( Version：2 )
                                                        IDE                    Spyder     ( Version: 3 ) 
                                                        RAM                    16G 
                                                        
                                                        
                                                        Packages ( Python ):
                                                        
                                                        Package   Version
                                                        Torch     1.2.0 ( CPU ) 
                                                        Numpy     1.14.6 
                                                        Jieba     0.36.2 
                                                        Scipy     1.1.0 
                                                        Sklearn   0.21.3 
                                                        Genism    3.6.0 
