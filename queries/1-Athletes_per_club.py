import matplotlib.pyplot as plt
import psycopg2

conn = psycopg2.connect("dbname=datawarehouse user=ricamigu password=password1234")

sql = "select code, COUNT(athleteId) as N from club, fact where club.clubid=fact.clubid group by rollup (code) order by N desc"

cursor_psql = conn.cursor()

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

data = {}

i = 0
for row in results:
    if i==0: 
        i = i + 1
        continue
    data[row[0]] = int(row[1])

codes = list(data.keys())
values = list(data.values())

plt.title("Number of athletes per club")
plt.xlabel("Clubs (Code)")
plt.ylabel("Number of athletes")
plt.xticks(rotation=90)
plt.bar(range(len(data)), values, tick_label=codes)
plt.show()