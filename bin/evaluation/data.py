# coding=utf-8
import csv
def csv_( p ):
    i = 0
    print( 'csv' )
    csvFile = open( p , "r" , encoding = 'utf-8-sig' )
    dict_reader = csv.DictReader(csvFile)
    result = []
    text = []
    for item in dict_reader:
        t = item[ "原始句子" ]
        if text.__contains__( t ):
            continue
        print( t )
        text.append( t )
    for t in text:
        d = [t]
        spo = []
        csvFile = open( p , "r" , encoding = 'utf-8-sig' )
        dict_reader = csv.DictReader(csvFile)
        for item in dict_reader:
            if d.__contains__( item[ "原始句子" ] ):
                r = []
                r.append( item[ "实体1" ] )
                r.append( item[ "关系" ] )
                r.append( item[ "实体2" ] )
                spo.append( r )
        print( spo )
        i = i + 1
        print( i )
        result.append( spo )
    return text , result

