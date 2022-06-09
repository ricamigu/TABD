import matplotlib.pyplot as plt
import numpy as np
import psycopg2

conn = psycopg2.connect("dbname=datawarehouse user=ricamigu password=password1234")


sql = "select newTab2.age_range, AVG(newTab2.points) as avg_points, gender from (select fact.athleteid, points, gender, case when newTable.age between 25 and 29 then 'A' when newTable.age between 30 and 34 then 'B' \
        when newTable.age between 35 and 39 then 'C' when newTable.age between 40 and 44 then 'D' when newTable.age between 45 and 49 then 'E' when newTable.age between 50 and 54 then 'F' \
        when newTable.age between 55 and 59 then 'G' when newTable.age between 60 and 64 then 'H' when newTable.age between 65 and 69 then 'I' when newTable.age between 70 and 74 then 'J' \
        when newTable.age between 75 and 79 then 'K' when newTable.age between 80 and 84 then 'L' when newTable.age between 85 and 89 then 'M' when newTable.age between 90 and 94 then 'N' \
        when newTable.age between 95 and 99 then 'O' END as age_range, newTable.age from (select gender, fact.athleteid, EXTRACT(year FROM age(current_date,birthdate::timestamp)) :: int as age \
        from athlete, fact where fact.athleteid = athlete.athleteid)newTable, fact where newTable.athleteId = fact.athleteId and points is not null \
        order by age)newTab2 group by rollup(newTab2.age_range, gender) order by newTab2.age_range"

cursor_psql = conn.cursor()

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

data_male = {}
data_avg = {}
data_female = {}
vertical = 0

for row in results:
    if(row[2] == 'M'): data_male[row[0]] = int(row[1])
    elif(row[2] == 'F'): data_female[row[0]] = int(row[1])
    else: 
        if(row[0] != None): data_avg[row[0]] = int(row[1])
    if(row[0] == None and row[2] == None): vertical = row[1]

categories = list(data_avg.keys())
values_male = list(data_male.values())
values_female = list(data_female.values())
values_avg = list(data_avg.values())

plt.title("Points by category and gender")
plt.xlabel("Categories")
plt.ylabel("Points")
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11], categories)
plt.plot(values_male, label="Males", color='royalblue')
plt.plot(values_female, label="Females", color='pink')
plt.plot(values_avg, label="Average", color='orange', linestyle="--", linewidth=0.5)
plt.axhline(y = vertical, color = 'red', linestyle = '--', linewidth=0.4)
plt.legend()
plt.show()