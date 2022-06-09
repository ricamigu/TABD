import matplotlib.pyplot as plt
import numpy as np
import psycopg2

conn = psycopg2.connect("dbname=datawarehouse user=ricamigu password=password1234")

sql = "select stroke, AVG(EXTRACT(epoch FROM swimtime::time)*100) as average, gender from swimstyle, fact,athlete where swimstyle.swimstyleid = fact.swimstyleid and fact.athleteid = athlete.athleteid group by rollup (stroke, gender) order by stroke, gender;"

cursor_psql = conn.cursor()

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

data_female = {}
data_male = {}


for row in results:
    stroke = row[0]
    avg = int(row[1])
    gender = row[2]
    if gender == 'M':
        data_male[stroke] = avg
    elif gender == 'F':
        data_female[stroke] = avg
    
stroke = list(data_male.keys())
values_male = list(data_male.values())
values_female = list(data_female.values())

X_axis = np.arange(len(stroke))
width = 0.4

plt.xticks(X_axis, stroke)

plt.bar(X_axis - 0.2, values_male, color = 'royalblue',
        width = width, edgecolor = 'black',
        label='Male')
plt.bar(X_axis + 0.2, values_female, color = 'pink',
        width = width, edgecolor = 'black',
        label='Female')

plt.xlabel("Strokes")
plt.ylabel("Average time in miliseconds")
plt.title("Average miliseconds by stroke type and gender")
plt.legend()
plt.show()