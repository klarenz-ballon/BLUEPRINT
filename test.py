from apps import dbconnect as db
sql_query = """ SELECT * FROM alumni"""
values = []
# number of column names must match the attributes for table genres
columns = ['alumni_id','specialization','valid_id']

df = db.querydatafromdatabase(sql_query, values, columns)
print(df)