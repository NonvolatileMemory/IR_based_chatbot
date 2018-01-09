# -*_ coding: utf-8 -*-
#
from lucene import *
import lucene
text = ["a b c d" , "c d e e"]
texts = ["Python 是 一个 很有 吸引力 的 语言",
"C++ 语言 也 很 有 吸引力 ， 长久 不衰",
"我们 希望 Python 和 C++ 高手加入",
"我们 的 技术 巨牛 ，人人 都是 高手"]

initVM()
INDEX_DIR = '/root/weibo_corpus/post_index'
directory = lucene.SimpleFSDirectory(lucene.File(INDEX_DIR))
analyzer = SimpleAnalyzer()


def read(filename):
    text = []
    with open(filename,'r') as f:
        count = 0
        for line in f:
            text.append(line.strip())
            count = count + 1
            if(count%10000==1):
                print(count)
    return text




def search(searcher,qtext):
    parser = QueryParser(lucene.Version.LUCENE_CURRENT,'post', analyzer)
    query = parser.parse(qtext)

    #query1 = TermQuery(Term("content", qtext))
    #query2 = TermQuery(Term("content", qtext2))
    #bquery = BooleanQuery()
    #bquery.add(Term("content", qtext))
    #bquery.add(query2)
    hits = searcher.search(query,None,10)
    print "----------------------------------------------"
    a = hits.totalHits
    print(a)
    print "Query:'%s', %d Found" % (qtext,hits.totalHits)
    for doc in hits.scoreDocs:
        print(doc.score)
        doc = searcher.doc(doc.doc)

        print "\t",doc["resp"]

def dump(reader):
    for i in range(reader.maxDoc()):
        print "-----------------------------------------------"
        tv = reader.getTermFreqVector(i, "content")
        for tk in tv.getTerms():
            print tk


def index(post,resp):


    writer = IndexWriter(directory, analyzer,True,lucene.IndexWriter.MaxFieldLength.UNLIMITED)
    count = 0
    for text in post:
        doc = Document()
        doc.add(Field("post", text, Field.Store.YES, Field.Index.ANALYZED,
            Field.TermVector.YES))
        doc.add(Field("resp", resp[count], Field.Store.YES, Field.Index.ANALYZED,
            Field.TermVector.YES))
        writer.addDocument(doc)
        count = count + 1
    writer.optimize()
    writer.close()

def create():
    post = read('weibo_pair.post')
    resp = read('weibo_pair.resp')
    index(post,resp)
reader = IndexReader.open(directory)
searcher = IndexSearcher(directory)
search(searcher, "你 觉得 山东 如何")
