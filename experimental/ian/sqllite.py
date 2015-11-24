import sqlite3
import json

__author__ = 'Ian'

conn = sqlite3.connect(':memory:')
c = conn.cursor()

creation_sql = ['''CREATE TABLE IF NOT EXISTS APP (id INTEGER PRIMARY KEY, name text, developer text,
        release_date DATE, added_date DATE, updated_date DATE, version text)''',
  ''' CREATE TABLE IF NOT EXISTS KEYWORD (id INTEGER PRIMARY KEY AUTOINCREMENT, word text, weight DECIMAL) '''

]
# Create table

map(c.execute, creation_sql)

#creates tables needing FKs
c.execute( '''CREATE TABLE IF NOT EXISTS REVIEW (id text PRIMARY KEY, product_id INTEGER date date, author text,stars DECIMAL, version DECIMAL,
                FOREIGN KEY (product_id) REFERENCES  APP(ID))'''
           )
c.execute('''CREATE TABLE IF NOT EXISTS REVIEWXKEYWORD
          (REVIEW_ID INTEGER,
          KEYWORD_ID,
          FOREIGN KEY(REVIEW_ID) REFERENCES REVIEW(ID),
          FOREIGN KEY(KEYWORD_ID) REFERENCES KEYWORD(ID))''')




def get_column_names (cursor, table_name):
    c2 = cursor.execute("select * from " + table_name)
    return [d[0] for d in c2.description]


print "Adding words:"

conn.commit()

apps = [['14831371782', 'Textra SMS']]

for app in apps:
    c.execute("INSERT INTO APP(id, name) VALUES(?,?)", app)
with open('words.json') as word_file:
    for line in json.load(word_file):
        c.execute("INSERT INTO KEYWORD(word, weight) VALUES (?,?)",
                  (line['word'], line['weight']))

print "Adding reviews:"
columns = get_column_names(c, "review")
with open('allTextraReviews.json') as word_file:
    for line in json.load(word_file):
        c.execute("INSERT INTO REVIEW(id, product_id, author, stars, version) VALUES (?,?,?,?,?)",
              (line['id'], line['product'], line['author'], line['stars'], line['version']))
conn.commit()

# Gets column names
#c = c.execute("select * from app")
#names = [d[0] for d in c.description]
#for x in data:
#  for col in names:
#    print x[col]

for col_name in get_column_names(c, "app"):
    print col_name
# Insert a row of data
#c.execute("INSERT INTO app VALUES (1,'2006-01-05','BUY')")

#print [str(v) +"_extra" for v in c.execute("select *from app").fetchmany(100)]
# Save (commit) the changes



# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
