from calendar import c
import matplotlib.pyplot as plt
import numpy as np
import psycopg2

# average points my stroke and gender
def average_stroke_gender(conn):

    sql = "select stroke, AVG(fact.points) as average, gender from swimstyle, fact,athlete where swimstyle.swimstyleid = fact.swimstyleid and fact.athleteid = athlete.athleteid group by rollup (stroke, gender) order by stroke, gender"

    cursor_psql = conn.cursor()

    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()
 
    data_female = {}
    data_male = {}

    for row in results:
        stroke = row[0]
        avg = row[1]
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
    plt.ylabel("Average points")
    plt.title("Average points by stroke type and gender")
    plt.legend()
    plt.show()

# average time by stroke and gender
def average_stroke_time(conn):
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


# Number of athletes per club
def count_club(conn):
    
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
    plt.ylabel("N")
    plt.xticks(rotation=90)
    plt.bar(range(len(data)), values, tick_label=codes)
    plt.show()


def top_10_clubs(conn):

    sql = "select code, MAX(points) as max from club, fact \
            where club.clubid=fact.clubid and points is not null \
            group by code  \
            order by max desc limit 10"

    cursor_psql = conn.cursor()

    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()

    data = {}

    for row in results:
       data[str(row[0])] = int(row[1]) 

    codes = list(data.keys())
    values = list(data.values())

    plt.title("Top 10 clubs by points")
    plt.xlabel("Clubs (Code)")
    plt.ylabel("Points")
    plt.xticks(rotation=45)
    plt.bar(range(len(data)), values, tick_label=codes)
    plt.show()



# min, avg and max age by club
def ages_by_club(conn):

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


def category_by_gender(conn):

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

    for row in results:
        if(row[2] == 'M'): data_male[row[0]] = int(row[1])
        elif(row[2] == 'F'): data_female[row[0]] = int(row[1])
        else: 
            if(row[0] != None): data_avg[row[0]] = int(row[1])

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
    plt.legend()
    plt.show()


if __name__ == '__main__':

    conn = psycopg2.connect("dbname=datawarehouse user=ricamigu password=password1234")
    
    average_stroke_gender(conn)
    average_stroke_time(conn)
    ages_by_club(conn)
    count_club(conn)
    top_10_clubs(conn)
    category_by_gender(conn)