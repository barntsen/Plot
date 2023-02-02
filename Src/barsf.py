
import sys
import re
import struct
import numpy as np

class rsf :
    def __init__(self,fname) :
        """Create rsf file object and parse rsf header file"""
        characters = self.rsfopen(fname)
        parselist = rsfparse(characters)
        self.n1=0
        self.d1=0
        self.o1=0
        self.n2=0
        self.d2=0
        self.o2=0

        for item in parselist :
            if item[0] == 'n1' :
                self.n1=int(item[1])
            if item[0] == 'n2' :
                self.n2=int(item[1])
            if item[0] == 'd1' :
                self.d1=float(item[1])
            if item[0] == 'd2' :
                self.d2=float(item[1])
            if item[0] == 'o1' :
                self.o1=float(item[1])
            if item[0] == 'o2' :
                self.o2=float(item[1])
            if item[0] == 'in' :
                self.fname=item[1]

        if self.fname != 'stdin' :
           self.file=open(self.fname)
        
        if self.n2 <= 1 :
            self.shape = (self.n1,)
        else :
            self.shape = (self.n2,self.n1)
             
    def rsfopen(self,fname) :
       """Open and read the rsf header file"""
       self.file = open(fname)
       characters=' '
       while True:
            c=self.file.read(1) 
            if c == "" :
               return characters
            elif c == '\014' :
               d = self.file.read(2)
               if (d[0] == '\014' ) & (d[1] == '\004') :
                   return characters
            else  :
               characters=characters+c 

       return characters 

    def read(self) :
        """Read  the rsf binary data"""
        dim=self.shape
        n=product(dim)
        string=self.file.read(4*n) #Read trace data as a string
        fmt=str(n)+'f'
        tmp=struct.unpack(fmt,string) #Convert to floats
        data=np.resize(np.array(tmp,dtype='f',order='c'),dim)        #Copy data to numpy array
        #Return a numpy data array
        self.file.close()
        return data 

def product(tuple1):
    """Calculates the product of a tuple"""
    prod = 1
    for x in tuple1:
        prod = prod * x
    return prod


def lex(characters, token_exprs):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match:
            pos=pos+1
        else:
            pos = match.end(0)
    return tokens


RESERVED = 'RESERVED'
INT      = 'INT'
FLOAT    = 'FLOAT'
ID       = 'ID'
STRING   = 'STRING'

token_exprs = [
    (r'[ \n\t]+',              None),
    (r'#[^\n]*',               None),
    (r'\:=',                   RESERVED),
    (r'\(',                    RESERVED),
    (r'\)',                    RESERVED),
    (r';',                     RESERVED),
    (r'\+',                    RESERVED),
    (r'-',                     RESERVED),
    (r'\*',                    RESERVED),
    (r'/',                     RESERVED),
    (r'<=',                    RESERVED),
    (r'<',                     RESERVED),
    (r'>=',                    RESERVED),
    (r'>',                     RESERVED),
    (r'=',                     RESERVED),
    (r'!=',                    RESERVED),
    (r'and',                   RESERVED),
    (r'or',                    RESERVED),
    (r'not',                   RESERVED),
    (r'if',                    RESERVED),
    (r'then',                  RESERVED),
    (r'else',                  RESERVED),
    (r'while',                 RESERVED),
    (r'do',                    RESERVED),
    (r'end',                   RESERVED),
    (r'n1',                   RESERVED),
    (r'n2',                   RESERVED),
    (r'n3',                   RESERVED),
    (r'n4',                   RESERVED),
    (r'd1',                   RESERVED),
    (r'd2',                   RESERVED),
    (r'd3',                   RESERVED),
    (r'd4',                   RESERVED),
    (r'\"(\\.|[^"])*\"',      STRING),
    (r'(?<![-.])\b[0-9]+\b(?!\.[0-9])',                INT),
    (r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?', FLOAT),
    (r'[A-Za-z][A-Za-z0-9_]*', ID),
]
def rsflex(characters) :
    return lex(characters, token_exprs)

def rsfparse(characters) :
    tokens=rsflex(characters)
    parselist=[('Parselist','START')]
    pos=0
    while pos < (len(tokens)-3) : 
        item=rsfasign(pos,tokens)
        if item != None :
           parselist.append(item)
           pos=pos+3
        else :
           pos=pos+1

    item=rsfasign(pos,tokens)
    if item != None :
       parselist.append(item)

    return parselist    

def rsfasign(pos,tokens) :
    parselist=None
    token=tokens[pos]

    if token[0]=='in':
       token=tokens[pos+1]
       if token[0] == '=' :  
           token=tokens[pos+2]
           if token[1] == STRING :
                 parselist=('in',token[0][1:len(token[0])-1])

    if token[0]=='n1':
       token=tokens[pos+1]
       if token[0] == '=' :  
           token=tokens[pos+2]
           if token[1] == INT :
                 parselist=('n1',token[0])

    if token[0]=='n2':
       token=tokens[pos+1]
       if token[0] == '=' :  
           token=tokens[pos+2]
           if token[1] == INT :
                 parselist=('n2',token[0])

    if token[0]=='d1':
       token=tokens[pos+1]
       if token[0] == '=' :  
           token=tokens[pos+2]
           if token[1] == INT :
                 parselist=('d1',token[0])
           if token[1] ==  FLOAT :
                 parselist=('d1',token[0])

    if token[0]=='d2':
       token=tokens[pos+1]
       if token[0] == '=' :  
           token=tokens[pos+2]
           if token[1] == INT :
                 parselist=('d2',token[0])
           if token[1] ==  FLOAT :
                 parselist=('d2',token[0])

    if token[0]=='o1':
       token=tokens[pos+1]
       if token[0] == '=' :  
           token=tokens[pos+2]
           if token[1] == INT :
                 parselist=('o1',token[0])
           if token[1] ==  FLOAT :
                 parselist=('o1',token[0])

    if token[0]=='o2':
       token=tokens[pos+1]
       if token[0] == '=' :  
           token=tokens[pos+2]
           if token[1] == INT :
                 parselist=('o2',token[0])
           if token[1] ==  FLOAT :
                 parselist=('o2',token[0])

    return parselist
