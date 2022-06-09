from calendar import c
import matplotlib.pyplot as plt
import numpy as np
import psycopg2

fig = plt.figure(figsize=(5, 5))
grid = plt.GridSpec(1, 3, hspace=0.2, wspace=0.2)
main_x = fig.add_subplot(grid[0, :2])
pie = fig.add_subplot(grid[0, 2])

print("This program will search for a club based on its code and return some graphics")

code = input("Enter the club code: ")

conn = psycopg2.connect("dbname=datawarehouse user=ricamigu password=password1234")

sql = "select count (fact.athleteid) as count, gender from athlete, club, fact  \
        where fact.athleteid = athlete.athleteid and fact.clubid = club.clubid and club.code = '" + code + "' group by rollup (gender) order by gender"

cursor_psql = conn.cursor()

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

values = []

for row in results: 
    if(row[1]!=None):
        values.append(int(row[0]))

pie.pie(values, labels=['Female', 'Male'], colors=['Pink','royalblue'], autopct='%1.1f%%')
pie.set_title("Male vs Female athletes in " + code)
#plt.pie(values, labels=['Female', 'Male'], colors=['Pink','royalblue'], autopct='%1.1f%%')
#plt.title("Male vs Female athletes in " + code)
#plt.show()

sql =  "select newTab.completeName, newTab.min as minimum, newTab.avg as average, newTab.max as maximum, newTab.license \
        from (select DISTINCT fact.athleteid, license, completeName, MIN(points) as min, AVG(points) as avg, MAX(points) as max from fact, athlete, \
        club where points is not NULL and fact.athleteid = athlete.athleteid and fact.clubid = club.clubid group by fact.athleteid, code, license, completeName)newTab, club, fact \
        where newTab.athleteid = fact.athleteid and club.clubid = fact.clubid and club.code = '" + code + "' \
        group by (newTab.max, newTab.avg,newTab.min, newTab.completeName,code, license) \
        order by max desc \
        limit 5" 

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

data = []
names = []
total_data = []
for row in results:
    data = []
    names.append(row[0])
    data.append(int(row[1]))
    data.append(int(row[2]))
    data.append(int(row[3]))
    total_data.append(data)

"""
plt.xlabel("Athletes")
plt.ylabel("Points")
plt.boxplot(total_data)
plt.xticks([1,2,3,4,5], names)
plt.title("Top 5 athletes from " + code)
plt.show()
"""

main_x.boxplot(total_data)
main_x.set_xlabel("Athletes") 
main_x.set_ylabel("Points") 
main_x.set_xticks([1,2,3,4,5])
main_x.set_xticklabels(names)
main_x.set_title("Top 5 athletes from " + str(code))

plt.show()