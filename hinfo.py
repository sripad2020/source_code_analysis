from googlesearch import search
import re,requests,heapq,nltk
from bs4 import BeautifulSoup
from transformers import pipeline
fopen=open('hotel.py','r')
read=fopen.readlines()
print(f'The file contains {len(read)} lines...')
minus=len(read)-1
print(f'The line starting from 0 to {minus}')
print('-------------------------------------------')
er='error'
for i in range(len(read)):
    text=re.sub('\n','',read[i])
    print(i,":",text)
while True:
    print('---------------------------------------')
    print('=======================================')
    para=[]
    output=[]
    inp=int(input('enter the line number: '))
    srch=search(read[inp])
    for i in srch:
        data=requests.get(i).text
        try:
            text=BeautifulSoup(data,'html.parser')
            for parag in text.find_all('p'):
                text=parag.get_text()
                token = nltk.tokenize.sent_tokenize(text)
                para.append(token)
        except requests.exceptions.MissingSchema as er:
            print(er)
    def r(para):
        for s in para:
            if type(s) == list:
                r(s)
            else:
                output.append(s)
    r(para)
    stri = ' '.join(map(str, output))
    text = stri.lower()
    clean = re.sub('[^a-zA-Z]', ' ', text)
    clean2 = re.sub('\s +', ' ', clean)
    sentence_list = nltk.sent_tokenize(text)
    stopwords = nltk.corpus.stopwords.words('english')
    word_frequencies = {}
    for word in nltk.word_tokenize(clean2):
        if word not in stopwords:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] = word_frequencies[word] / maximum_frequency
    sentence_scores = {}
    for sentence in sentence_list:
        for word in nltk.word_tokenize(sentence):
            if word in word_frequencies and len(sentence.split(' ')) < 30:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]
    summary = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)
    sentence = ''.join(summary)
    pr = re.sub('\n+', ' ', sentence)
    text_cleaned = re.sub('{*?}', '', pr)
    sd = re.sub("{.*?}", '', text_cleaned)
    cleaned = re.sub('\*?', '', sd)
    summarizer = pipeline('summarization')
    for i in summarizer(cleaned, min_length=10, max_length=95):
        print(i['summary_text'])