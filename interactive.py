from calendar import c
import matplotlib.pyplot as plt
import numpy as np
import psycopg2


# ranking of athletes
def ranking_athlete(conn, license):
    
    sql = "select newTab.* from (select license, completeName, sum(points) as sum, code from fact, athlete, club where points is not NULL \
    and fact.athleteid = athlete.athleteid and fact.clubid = club.clubid group by athlete.license, code, license, completeName)newTab order by sum desc"

    cursor_psql = conn.cursor()

    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()

    data = {}

    i = 0
    for row in results:
        i = i + 1
        if(str(row[0])==str(license)):
            print("The athlete with license", str(license), "in team", str(row[3]) ,"is in position", i, "with", str(row[2]) ,"points")
            return

    print("License not found!")


# not working
def top_5_from_club(conn, club):

    sql =  "select newTab.completeName, newTab.min as minimum, newTab.avg as average, newTab.max as maximum, code \
            from (select DISTINCT fact.athleteid, license, completeName, MIN(points) as min, AVG(points) as avg, MAX(points) as max from fact, athlete, \
            club where points is not NULL and fact.athleteid = athlete.athleteid and fact.clubid = club.clubid group by fact.athleteid, code, license, completeName)newTab, club, fact \
            where newTab.athleteid = fact.athleteid and club.clubid = fact.clubid and club.code = '" + club + "' \
            group by (newTab.max, newTab.avg,newTab.min, newTab.completeName,code) \
            order by max desc \
            limit 5" 

    cursor_psql = conn.cursor()

    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()

    data_min = {}
    data_avg = {}
    data_max = {}

    for row in results:
        data_min[row[0]] = int(row[1])
        data_avg[row[0]] = int(row[2])
        data_max[row[0]] = int(row[3])


    names = list(data_avg.keys())

    values_min = np.asarray(list(data_min.values()))
    values_avg = np.asarray(list(data_avg.values()))
    values_max = np.asarray(list(data_max.values()))

    plt.xlabel(names)
    plt.boxplot(values_min, values_avg, values_max)
    plt.show()


def circular_plot(conn, code):

    # Female
    sql_f = "select COUNT(fact.athleteid) as F \
            from athlete, club, fact  \
            where gender='F' and code = '" + code + "' and fact.athleteid = athlete.athleteid and fact.clubid = club.clubid"

    # Male

    sql_m = "select COUNT(fact.athleteid) as M \
            from athlete, club, fact \
            where gender='M' and code = '" + code + "' and fact.athleteid = athlete.athleteid and fact.clubid = club.clubid"

    cursor_psql = conn.cursor()

    cursor_psql.execute(sql_f)
    results_f = cursor_psql.fetchall()

    cursor_psql.execute(sql_m)
    results_m = cursor_psql.fetchall()

    values = []

    for row in results_f:
        values.append(int(row[0]))

    for row in results_m:
        values.append(int(row[0]))

    plt.pie(values, labels=['Female', 'Male'], shadow=True, autopct='%1.1f%%')
    plt.title("Male vs Female athletes")
    plt.show()

if __name__ == '__main__':

    conn = psycopg2.connect("dbname=datawarehouse user=ricamigu password=password1234")

    print("This program will search for an athlete based on his/her license and return the ranking position of the athlete")

    #val = input("\nEnter the athlete's license: ")

    #ranking_athlete(conn, val)
    circular_plot(conn, "SCP")
