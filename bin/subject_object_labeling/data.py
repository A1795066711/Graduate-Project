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
#        print( t )
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
#        print( spo )
        i = i + 1
        print( i )
        result.append( spo )
    return text , result

def boo( a , b , l , n , c ):
    for i in range( len( b ) - l ) :
        print( l )
        if b[ l + i ] == a[ n ]:
            c.append( l + i )
            if l == len( b ) - 1:
                if n == len( a ) - 1 :
                    return c
                else:
                    return False
            else:
                if n == len( a ) - 1 :
                    return c
                else:
                    r = boo( a , b , l + i + 1 , n + 1 , c )
                    if r:
                        return r
        else:
            continue
    return False

a = "11防12备加34强备"

b = "加强电力设备防备"
#r = boo( a , b , 0 , 0 , [] )
text_tokened = b
so_tokened = a
r = []
#def s( z , c ):
#    for n in range( z , len( text_tokened ) ):
#        if lc == text_tokened[ n ]:
#            c = n
#            return True , c
#    return False , c
#
#for m in range( 0 , len( so_tokened ) ):
#    if( len( r ) >= 1 ):
#        b , l = s( r[ len( r ) - 1 ] + 1 , so_tokened[ m ] )
#    else:
#        b , l = s( 0 , so_tokened[ m ] )
#    if b:
#        r.append( l )
#    else:
#        b , c = s( 0 , so_tokened[ m ] )
#        if b:
#            r.append( c )
#r = []
#set = -1
#for k in range( 0 , len( so_tokened ) ):
#    if not so_tokened[ k ].isdigit():
#        if set != -1:
#            s = ''
#            for m in range( set , k ):
#                s += so_tokened[ m ]
#            r.append( s )
#            r.append( so_tokened[ k ] )
#        else:
#            r.append( so_tokened[ k ] )
#        set = -1
#    else:
#        if k == len( so_tokened ):
#            if set != -1:
#                s = ''
#                for m in range( set , k + 1 ):
#                    s += so_tokened[ m ]
#                r.append( s )
#            else:
#                r.append( so_tokened[ k ] )
#        if set == -1:
#            set = k
import jieba
r = b
print( ' '.join( jieba.cut( b , cut_all = False ) ) )