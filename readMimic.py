import csv, time
import pandas as pd
from sqlalchemy import create_engine

t1 = time.time()
filename = "/path/to/mimic/data"

print(pd.read_csv(filename, nrows=5))
#.schema 

csv_database = create_engine('sqlite:///mimic.db')

chunksize = 1000000
i = 0
j = 1

for df in pd.read_csv(filename, chunksize=chunksize, iterator=True):
      df = df.rename(columns={c: c.replace(' ', '') for c in df.columns}) 
      df.index += j
      i+=1
      df.to_sql('mydata', csv_database, if_exists='append')
      j = df.index[-1] + 1


print("Made csv sqlite db: done in %0.3fs." % (time.time() - t1))

df = pd.read_sql_query('select * from mydata limit 5;', csv_database)
print(df)
print(type(df))

