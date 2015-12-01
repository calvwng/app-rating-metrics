import sqlite3
import json
import sentiment_scoring
import spelling_scoring

__author__ = 'Ian'

conn = sqlite3.connect(':memory:')
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

print "Adding reviews:"
with open ('snapchatReviews.json') as word_file:
    for line in json.load(word_file):
        c.execute("INSERT INTO REVIEW(id, product, original_review, date, author, stars, version) VALUES (?,?,?,?,?,?,?)", (line['id'], line['product'], line['original_review'], line['date'], line['author'], line['stars'], line['version']))
conn.commit()

# gets reviews and assigns scores
for row in c.execute("SELECT original_review FROM REVIEW"):
    print
    print "this is a review: " + row[0]
    print "this is the sentiment score from range -5 to 5: " + str(sentiment_scoring.sentiment_score(row[0]))
    print "this is the spelling score from range 0 to 5: " + str(spelling_scoring.spelling_score(row[0]))

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
