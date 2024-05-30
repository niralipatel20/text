from flask import Flask, request, jsonify,render_template,redirect,url_for
import nltk
import numpy
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from collections import Counter
import re
import string
stop_words = set(stopwords.words('english'))
punctuation = string.punctuation
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import spacy
from spacy import displacy
import json
from string import punctuation, digits
from nltk.corpus import stopwords
stopwords = stopwords.words('english')

app = Flask(__name__)

@app.route('/preprocess',methods=['POST'])
def preprocess():
    text = request.form['text_input']
    Re_pattern = request.form['re_input']
    emojipattern=request.form['emoji_pattern']
    preprocessed_data={}

    #tokenization
    if ("tokenize" in request.form)==True:
            tokenize_text = word_tokenize(text)
            preprocessed_data["tokenize_text"]=tokenize_text

    #lemmatization
    if ("lemmatization" in request.form)==True:
            lemmatizer = WordNetLemmatizer()
            words = word_tokenize(text)
            lemmas = [lemmatizer.lemmatize(word) for word in words]
            Lemmatization_text = " ".join(lemmas)
            preprocessed_data["Lemmatization_text"]=Lemmatization_text

    #RE pattern
    if ("pattern" in request.form)==True:
            def preprocessedre(text,Re_pattern):
                Re_pattern=''.join(list(Re_pattern))
                try:
                    if "," in Re_pattern:
                        pattern_parts = Re_pattern.split(",")  # Split the pattern by comma
                        processed_text = text
                        for part in pattern_parts:
                            processed_text = re.sub(part, '', processed_text)
                    else:
                        processed_text = re.sub(Re_pattern, '', text)
                    return processed_text
                except re.error as e:
                    error_message = f"Invalid regex pattern: {str(e)}"
                    return error_message            
            RE_text = preprocessedre(text,Re_pattern)
            preprocessed_data["RE_text"] = RE_text

    #Upper
    if ("upper" in request.form)==True:
            upper_text=text.upper()
            preprocessed_data["upper_text"]=upper_text

    #lower
    if ("lower" in request.form)==True:
            lower_text=text.lower()       
            preprocessed_data["lower_text"]=lower_text

    #capitalization 
    if ("capitalization" in request.form)==True:
            def capitalization(text):
                text = text.lower()
                text = text.title()
                return text
            capitalization_text = capitalization(text)
            preprocessed_data["capitalization_text"]=capitalization_text

    #whiteapce removal
    if ("whitespace" in request.form)==True:
            whitespace_text = " ".join(text.split())
            preprocessed_data["whitespace_text"]=whitespace_text


    #emoji removal word
    if ("emoji" in request.form)==True:
            def remove_emoji(text,emojipattern):
                print("nooo:",emojipattern)
                emojipattern=''.join(list(emojipattern))
                try:
                    if "," in emojipattern:
                        pattern_parts = emojipattern.split(",")  # Split the pattern by comma
                        processed_text = text
                        for part in pattern_parts:
                            print(part)
                            emoji_pattern = re.compile(part,'', flags=re.UNICODE)
                            print(emojipattern)
                            processed_text = emoji_pattern.sub(r'', string)
                    else:
                        processed_text = re.sub(emojipattern, '', text)
                    return processed_text
                except re.error as e:
                    error_message = f"Invalid regex pattern: {str(e)}"
                    return error_message
            
            emoji_text = remove_emoji(text,emojipattern)
            preprocessed_data["emoji_text"]=emoji_text

    #frequent Word
    if ("frequency" in request.form)==True:
            def frequency(text):
                cnt = Counter()
                for word in text.split():
                    cnt[word] += 1
                text=cnt.most_common(10)
                return text
            frequency_text = frequency(text)
            preprocessed_data["frequency_text"]=frequency_text
        
    #Rare Option
    if ("rare" in request.form)==True:
            def rare(text):
                cnt = Counter()
                for word in text.split():
                    cnt[word] += 1
                n_rare_words = 10
                text = set([w for (w, wc) in cnt.most_common()[:-n_rare_words-1:-1]])
                text=list(text)
                return text
            rare_text = rare(text)
            preprocessed_data["rare_text"]=rare_text
            print(preprocessed_data["rare_text"])

    #POS Option
    if ("POS" in request.form)==True:
            def POS(text):
                pos_tags = pos_tag(word_tokenize(text))
                cnt = {tag: {
                    "count" : len(list(filter(lambda x: x[1] == tag, pos_tags))),
                    "Words": [word for word, tag_ in pos_tags if tag_ == tag]
                }for tag in ["CD", "NNS", "NN", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NNP", "NNPS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB"]}
                return cnt
            POS_text = POS(text)
            preprocessed_data["POS_text"]=POS_text


    #NER Option
    if "NER" in request.form:
        def NER(text):
                NER = spacy.load("en_core_web_md")
                ner_text = NER(text)
                named_entities = []
                for word in ner_text.ents:
                    named_entities.append((word.text, word.label_))
                return named_entities

        NER_text = NER(text)
        preprocessed_data["NER_text"] = NER_text
    
    #json convert the data
    print("preprocessed_data",preprocessed_data)
    details = json.dumps(preprocessed_data)
    return render_template('output.html',preprocessed_data=details,real_text=text)


@app.route('/')
def index():
    return render_template('index.html')


if __name__== '__main__':
    app.run(debug=True)