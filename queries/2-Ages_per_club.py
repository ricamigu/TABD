import matplotlib.pyplot as plt
import psycopg2

conn = psycopg2.connect("dbname=datawarehouse user=ricamigu password=password1234")

sql = "select code, MIN( EXTRACT(year FROM age(current_date,birthdate::timestamp)) :: int) as minAge, Max( EXTRACT(year FROM age(current_date,birthdate::timestamp)) :: int) as maxAge, AVG( EXTRACT(year FROM age(current_date,birthdate::timestamp)) :: int) as avgAge from club, athlete, fact where club.clubid=fact.clubid and fact.athleteid = athlete.athleteid group by rollup (code) order by avgage"

cursor_psql = conn.cursor()

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

data_min = {}
data_avg = {}
data_max = {}

for row in results:
    if row[0] != None:
        data_min[row[0]] = int(row[1])
        data_max[row[0]] = int(row[2])
        data_avg[row[0]] = int(row[3])

minList = data_min.items()
xmin, ymin = zip(*minList)
plt.plot(xmin, ymin, label="Min", linewidth=0.5, color="blue")

avgList = data_avg.items()
xavg, yavg = zip(*avgList)
plt.plot(xavg, yavg, label="Average", linewidth=2, linestyle="--", color="orange")

maxList = data_max.items()
xmax, ymax = zip(*maxList)
plt.plot(xmax, ymax, label="Max", linewidth=0.5, color="red")

plt.title("Average age per club")
plt.xlabel("Clubs (Code)")
plt.ylabel("Ages")
plt.legend()
plt.xticks(rotation=90)
plt.fill_between(xavg, yavg, ymax, color='red', alpha=.2)
plt.fill_between(xavg, yavg, ymin, color='blue', alpha=.2)
plt.show()