import sqlite3
import json

__author__ = 'Ian'

conn = sqlite3.connect(':memory:')
c = conn.cursor()


creation_sql = ['''CREATE TABLE IF NOT EXISTS app (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, developer text,
        release_date DATE, added_date DATE, updated_date DATE, version text)''',
  '''CREATE TABLE IF NOT EXISTS review (id INTEGER PRIMARY KEY AUTOINCREMENT, date date, user text,rating DECIMAL )'''

]
# Create table

map(c.execute, creation_sql)



with open('query.json') as data_file:
  data = json.load(data_file)

print(data)

# Gets column names
c = c.execute("select * from app")
names = [d[0] for d in c.description]
for x in data:
  for col in names:
    print x[col]


# Insert a row of data
#c.execute("INSERT INTO app VALUES (1,'2006-01-05','BUY')")

#print [str(v) +"_extra" for v in c.execute("select *from app").fetchmany(100)]
# Save (commit) the changes
conn.commit()


# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
