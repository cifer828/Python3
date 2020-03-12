#encoding:utf-8
from collections import defaultdict
# import sys
# import importlib
# importlib.reload(sys)
# sys.setdefaultencoding('utf8')

class LBTrie:  
    '''
    实现词频统计的字典树
    '''
    def __init__(self):  
        self.trie = {}  
        self.size = 0  
         
    #添加单词   
    def add(self, word):  
        p = self.trie 
        dicnum = 0 
        word = word.strip()  
        for c in word:  
            if not c in p:  
                p[c] = {}
            dicnum+=1  
            p = p[c] 
        if word != '':  
            #在单词末尾处添加键值''作为标记，即只要某个字符的字典中含有''键即为单词结尾  
            p[''] = ''   
        if dicnum == len(word):
            return True 
        else:
            return False
    #查询单词        
    def search(self, word):  
        p = self.trie  
        word = word.lstrip()  
        for c in word:  
            if not c in p:  
                return False  
            p = p[c]  
        #判断单词结束标记''  
        if '' in p:  
            return True  
        return False            
      
    #打印Trie树的接口  
    def output(self):  
        #print '{'  
        self.__print_item(self.trie)      
        #print '}'  
        return  self.__print_item(self.trie)
      
    #实现Trie树打印的私有递归函数 
    def __print_item(self, p, indent=0):       
        if p:  
            ind = '' + '\t' * indent  
            for key in list(p.keys()):  
                label = "'%s' : " % key  
                #print ind + label + '{'  
                self.__print_item(p[key], indent+1)
  
