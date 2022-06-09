import matplotlib.pyplot as plt
import numpy as np
import psycopg2

fig = plt.figure(figsize=(5, 5))
grid = plt.GridSpec(2, 3, hspace=0.2, wspace=0.2)
main_x = fig.add_subplot(grid[0, :2])
pie = fig.add_subplot(grid[0, 2])
box = fig.add_subplot(grid[1,0])
times = fig.add_subplot(grid[1,1:])

conn = psycopg2.connect("dbname=datawarehouse user=ricamigu password=password1234")

print("This program will search for an athlete based on his/her license and return some graphics")
license = input("\nEnter the athlete's license: ")

cursor_psql = conn.cursor()

athlete = "select * from athlete where license = '"+ license +"'"

cursor_psql.execute(athlete)
results = cursor_psql.fetchall()

athlete_id = int(results[0][0])
name = str(results[0][1])


sql = "select stroke, license, count(stroke) as N \
        from fact, swimstyle, athlete \
        where fact.swimstyleid = swimstyle.swimstyleid \
        and athlete.athleteid = fact.athleteid and athlete.athleteid = "+ str(athlete_id) +" \
        group by (license, stroke)"

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

data_stroke = {}

i = 0
for row in results:
    i = i + 1
    data_stroke[str(row[0])] = int(row[2])


    
strokes = list(data_stroke.keys())
values = list(data_stroke.values())

pie.pie(values, labels=strokes, autopct='%1.1f%%')
pie.set_title("Stroke distribution")


sql_distance = "select distance, athleteId, count(distance) as N \
                from fact, swimstyle \
                where fact.swimstyleid = swimstyle.swimstyleid \
                and athleteId= '"+ str(athlete_id) +"' \
                group by (athleteId, distance)"

cursor_psql.execute(sql_distance)
results = cursor_psql.fetchall()

data_distance = {}

for row in results:
    data_distance[str(row[0])] = int(row[2])

distances = list(data_distance.keys())
values = list(data_distance.values())

main_x.bar(range(len(data_distance)), values, tick_label=distances, color="palegreen")
main_x.set_title("Distance distribution")
main_x.set_ylabel("N")
main_x.set_xlabel("distances")

query_boxplot = "select newTab.completeName, newTab.min as minimum, newTab.avg as average, newTab.max as maximum, newTab.license  \
        from (select DISTINCT fact.athleteid, license, completeName, MIN(points) as min, AVG(points) as avg, MAX(points) as max from fact, athlete, \
        club where points is not NULL and fact.athleteid = athlete.athleteid and fact.clubid = club.clubid group by fact.athleteid, code, license, completeName)newTab, club, fact \
        where newTab.athleteid = fact.athleteid and club.clubid = fact.clubid and newTab.athleteid = "+ str(athlete_id) +" \
        group by (newTab.max, newTab.avg,newTab.min, newTab.completeName,code, license)"

cursor_psql.execute(query_boxplot)
results = cursor_psql.fetchall()

d_min = int(results[0][1])
d_avg = int(results[0][2])
d_max = int(results[0][3])
data_points = [d_min, d_avg, d_max]

box.boxplot(data_points)
box.set_xlabel("Athlete")
box.set_ylabel("Points")
box.set_title("Points distribution")


query_times = "select stroke, AVG(EXTRACT(epoch FROM swimtime::time)*100) as average, athlete.athleteid \
                from swimstyle, fact,athlete where swimstyle.swimstyleid = fact.swimstyleid and fact.athleteid = athlete.athleteid \
                and athlete.athleteid = "+ str(athlete_id)+" group by stroke, gender, athlete.athleteid order by stroke, gender" 

cursor_psql.execute(query_times)
results = cursor_psql.fetchall()

data_time = {}

for row in results:
    data_time[str(row[0])] = int(row[1])

strokes = list(data_time.keys())
values = list(data_time.values())

X_axis = np.arange(len(strokes))
times.set_xticks(X_axis, strokes)

times.bar(X_axis, values, color="skyblue")
times.set_xlabel("Strokes")
times.set_ylabel("Average time in miliseconds")


sql =  "SELECT license, completeName, sum(points) AS SUM, AVG(points) AS AVG, min(points) AS MIN, MAX(points) AS MAX, code FROM fact, athlete, club \
        WHERE points IS NOT NULL AND fact.athleteid = athlete.athleteid AND fact.clubid = club.clubid \
        GROUP BY athlete.license, code, license, completeName \
        ORDER BY SUM DESC" 
    
cursor_psql = conn.cursor()

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

data = {}

i = 0
for row in results:
    i = i + 1
    if(str(row[0])==str(license)): break

fig.suptitle('Analysis for player ' + name + ' in position #' + str(i) + ' on the global ranking')

plt.show()
