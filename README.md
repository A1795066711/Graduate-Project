# Graduate-Project

## Intro
  
  It's a project aiming to solve some not high accuracy problems in NLP area particularly in Entity-Relation Extraction.
  
  For each data set for learning and prediction, processes will be:
  
  1. Text Segmentation
  
     The Training: The training data set would be added to one BiLSTM layer and one CNN layer in the same time, output of both would be the input for the CRF layer.
     
     The Prediction: Segmentation of the text.
     
     Comparation with some other models:
     
                                                        MODEL           P         R           F1 
                                                        CRF             0.898    0.891        0.894 
                                                        LSTM            0.893    0.887        0.889 
                                                        BiLSTM          0.912    0.897        0.904 
                                                        BiLSTM-CNN-CRF  0.929    0.921        0.924 
     
  2. Text Classification
     
     The training data was collected by web crawler program from the Internet.
     
     Data would be like: { "some text" , its label } with 10 labels for all.
     
     CNN and RNN models are applied to this task.
     
     Comparation to other base models:                  
                                                        Methods       Precision Recall  F1 
                                                        ( Base models ) 
                                                        LR            0.87      0.87    0. 87 
                                                        MultinomialNB 0.91      0.86    0.88 
                                                        SVM           0.89      0.76    0.81 
                                                        ( Applied models ) 
                                                        CNN           0.96      0.96    0.96 
                                                        RNN           0.94      0.94    0.94 
                                                    
   3.Entity Relation Extraction:
   
     Google's BERT MODEL is applied in this part, with the improving of its segmentation codes by the BiLSTM-CNN-CRF model mentioned.
     
     Some of the results:
     
                                                        Relationship          Precision   Recall    F1 
                                                        Time of the event     93.37%      87.71%    81.19% 
                                                        Area of the event     86.94%      86.11%    89.11% 
                                                        Center of the event   89.11%      95.02%    86.19% 
                                                        Duration of the event 88.16%      81.91%    78.69% 
                                                        Cause of the event    87.69%      81.11%    87.71% 
                                                        Lessons of the event  91.78%      61.11%    81.66% 
                                                        Damage of the event   71.17%      71.88%    87.11% 
                                                        
            
## Some details of the data

The data set is composed of plenty of pieces of text about the electricity outage or blackout. 

Data preprocessing is about signing the texts with the relevant relationship, entities and labels for classification.  
