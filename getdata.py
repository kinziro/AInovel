# -*- coding: utf-8 -*-

import json
from urllib.request import urlopen
import gzip

def get_header(lim=20, minlen=10000 ):
    """
    小説家になろうから小説情報の概要を取得します.

    :param int lim: 情報の取得件数
    :rtype: list
    :return: 取得した情報概要
    """

    # APIのURL
    #url='http://api.syosetu.com/novelapi/api/?out=json&lim=100&gzip=5'
    url='http://api.syosetu.com/novelapi/api/?out=json' \
           + '&lim=' + str(lim) \
            + '&minlen=' + str(minlen) \
            + '&gzip=5'
    
    # APIを取得
    response = urlopen(url)
    
    # 解凍する
    with gzip.open(response, "rt", encoding="utf-8") as f:
        j_raw = f.read()
    
    # JSONデコード
    jObj = json.loads(j_raw)
    
    # jObj0番目はallcountなので1番目から処理
    for a_novel in jObj[1:]:
        # titleの表示
        title = a_novel['title']
        print("title:", title)
    
        # あらすじの表示
        story = a_novel['story']
        print("story:", story)
    
        # 小説へのリンク作成
        ncode = a_novel['ncode']
        link = "http://ncode.syosetu.com/{}/".format(ncode.lower())
        print("ncode:", ncode)
        print("link:", link)

    # JSON形式で概要を戻す
    return jObj


def get_all_noveltext(ncode, general_all_no):
    '''
    指定したncodeの小説本文全てを取得します

    :param string ncode: 小説のncode
    :param string general_all_no: 小説のページ数
    :rtype: string
    :return: 小説本文
    '''

    # 小説のページ数文まとめて取得する
    text = ""
    for no in range(1,int(general_all_no) + 1):
        url = "http://ncode.syosetu.com/{}/".format(ncode.lower()) + str(no) + "/"      # 小説本文のurl
        text += get_noveltext(url)

    # 本文を戻す
    return text


import requests
from bs4 import BeautifulSoup
def get_noveltext(url):
    '''
    指定したURLから小説本文を取得します

    :param string url: 小説本文のあるURL
    :rtype: string
    :return: 小説本文
    '''
    print("url:", url)
    
    reqinfo = requests.get(url)       # 小説本文のhtmlを取得 
    reqinfo.encoding = 'UTF-8'
    soup = BeautifulSoup(reqinfo.text, "html.parser")
    noveltext = soup.find('div', id='novel_honbun').text

    # 本文を戻す
    return noveltext 


from janome.tokenizer import Tokenizer
def split_word(text):
    '''
    指定したURLから小説本文を取得します

    :param string text: 文章
    :rtype: string
    :return: 単語ごとに改行した文章
    '''
    t = Tokenizer()
    out_text = ""
    for token in t.tokenize(text):
        word = token.surface.replace('\n',"") 
        if word != "" and word != "　" and not(word.isspace()):
            out_text += word
            out_text += "\n"

    return out_text


# 小説家になろうのAPIから小説をダウンロード
jIndex = get_header(2)
ncode = jIndex[1]['ncode']
title = jIndex[1]['title']
length = jIndex[1]['length']
general_all_no = jIndex[1]['general_all_no'] 
#general_all_no = "1"
text = get_all_noveltext(ncode, general_all_no)
words = split_word(text)
with open('./Data/contents.txt', 'a') as fout:
    fout.write(title + "," + str(length))
with open('./Data/' + title + '.txt', 'wt') as fout:
    fout.write(words)
