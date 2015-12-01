import sqlite3
import json
import enchant

__author__ = 'Ian'

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_negation(possible_negations, negation_list):
    full_string = " ".join(possible_negations)
    if any(str in full_string for str in negation_list):
        print "negation here: " + full_string
        return -1
    return 1

def sentiment_score(s, negation_words, sent_dict):
    score = 0
    count = 0
    possible_negations = []
    for word in s.split():
	possible_negations.append(word)
        count += 1
        if count > 3:
           possible_negations.pop(0)
        multiplier = 1
        if word in sent_dict:
            temp_score = sent_dict[word]
            score += temp_score * is_negation(possible_negations, negation_words)
    if score > 5:
        score = 5
    if score < -5:
        score = -5
    return score


def spelling_score(s, dict):
    correct = 0
    incorrect = 0
    for word in s.split():
        if dict.check(word):
            correct += 1
        else:
            incorrect += 1
    if incorrect == 0:
        return 5
    else:
        incorr_percent = incorrect / float(correct + incorrect)
        if incorr_percent > 0.3:
            return 0
        elif incorr_percent > 0.2:
            return 1 
        elif incorr_percent > 0.1:
            return 2
        elif incorr_percent > 0.05:
            return 3
        else:
            return 4

dict = enchant.Dict()
conn = sqlite3.connect('snapchat_reviews.db')
c = conn.cursor()

creation_sql = ['''CREATE TABLE IF NOT EXISTS APP (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, developer text,
        release_date DATE, added_date DATE, updated_date DATE, version text)'''
]
# Create table

map(c.execute, creation_sql)

#creates tables needing FKs
c.execute( '''CREATE TABLE IF NOT EXISTS REVIEW (id text PRIMARY KEY, product INTEGER, original_review TEXT, date DATE, author TEXT, stars DECIMAL, version DECIMAL,
                FOREIGN KEY (product) REFERENCES  APP(ID))'''
           )
c.execute('''CREATE TABLE IF NOT EXISTS REVIEWXKEYWORD
          (REVIEW_ID INTEGER,
          KEYWORD_ID,
          FOREIGN KEY(REVIEW_ID) REFERENCES REVIEW(ID),
          FOREIGN KEY(KEYWORD_ID) REFERENCES KEYWORD(ID))''')

conn.commit()

# Populating sentiment analysis dictionary from file

sent_dict = {}
with open('vader_sentiment_lexicon.txt') as word_file:
    for line in word_file:
        word_weight = line.split()
        if is_number(word_weight[1]):
            sent_dict[word_weight[0]] = float(word_weight[1])

print "Adding reviews:"
with open ('snapchatReviews.json') as word_file:
    for line in json.load(word_file):
        c.execute("INSERT INTO REVIEW(id, product, original_review, date, author, stars, version) VALUES (?,?,?,?,?,?,?)", (line['id'], line['product'], line['original_review'], line['date'], line['author'], line['stars'], line['version']))
conn.commit()

# gets reviews and assigns scores
negation_words = open('negationWords.txt').read().splitlines()
for row in c.execute("SELECT original_review FROM REVIEW"):
    print
    print "this is a review: " + row[0]
    print "this is the sentiment score from range -5 to 5: " + str(sentiment_score(row[0], negation_words, sent_dict))
    print "this is the spelling score from range 0 to 5: " + str(spelling_score(row[0], dict))

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
