import sqlite3
import json

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

def sentiment_score(s, negation_words, conn_cursor):
    score = 0
    count = 0
    possible_negations = []
    for word in s.split():
	possible_negations.append(word)
        count += 1
        if count > 3:
           possible_negations.pop(0)
        multiplier = 1
        temp_score = 0
        for word_score in conn_cursor.execute("SELECT weight FROM KEYWORD WHERE word='{0}'".format(word.lower().replace("'", "''"))):
            temp_score = word_score[0]
            print "this is the word: " + word
        if temp_score != 0:
            score += temp_score * is_negation(possible_negations, negation_words)
    return score

conn = sqlite3.connect(':memory:')
c = conn.cursor()

creation_sql = ['''CREATE TABLE IF NOT EXISTS APP (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, developer text,
        release_date DATE, added_date DATE, updated_date DATE, version text)''',
  ''' CREATE TABLE IF NOT EXISTS KEYWORD (id INTEGER PRIMARY KEY AUTOINCREMENT, word text, weight DECIMAL) '''

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


def get_column_names (cursor, table_name):
    c2 = cursor.execute("select * from " + table_name)
    return [d[0] for d in c2.description]

with open('query.json') as data_file:
  data = json.load(data_file)



print "Adding words:"

conn.commit()

with open('vader_sentiment_lexicon.txt') as word_file:
    for line in word_file:
        word_weight = line.split()
        if is_number(word_weight[1]):
            c.execute("INSERT INTO KEYWORD(word, weight) VALUES (?,?)", 
                     (word_weight[0].decode('utf8'), float(word_weight[1])))

print "Adding reviews:"
columns = get_column_names(c, "review")
with open ('allTextraReviews.json') as word_file:
    for line in json.load(word_file):
        c.execute("INSERT INTO REVIEW(id, product, original_review, date, author, stars, version) VALUES (?,?,?,?,?,?,?)", (line['id'], line['product'], line['original_review'], line['date'], line['author'], line['stars'], line['version']))
conn.commit()

# gets a review and assigns score based on KEYWORD table
negation_words = open('negationWords.txt').read().splitlines()
for row in c.execute("SELECT original_review FROM REVIEW ORDER BY RANDOM() LIMIT 1"):
    print "this is a review: " + row[0]
    print "this is the review's score: " + str(sentiment_score(row[0], negation_words, c))

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
