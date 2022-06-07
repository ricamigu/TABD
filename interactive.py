from calendar import c
import matplotlib.pyplot as plt
import numpy as np
import psycopg2


# ranking of athletes
def ranking_athlete(conn, license):

    sql =  "SELECT license, completeName, sum(points) AS SUM, AVG(points) AS AVG, min(points) AS MIN, MAX(points) AS MAX, code FROM fact, athlete, club \
        WHERE points IS NOT NULL AND fact.athleteid = athlete.athleteid AND fact.clubid = club.clubid \
        GROUP BY athlete.license, code, license, completeName \
        ORDER BY SUM DESC" 
    
    """
    sql = "select newTab.* from (select license, completeName, sum(points) as sum, code from fact, athlete, club where points is not NULL \
    and fact.athleteid = athlete.athleteid and fact.clubid = club.clubid group by athlete.license, code, license, completeName)newTab order by sum desc"
    """

    cursor_psql = conn.cursor()

    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()

    data = {}

    i = 0
    for row in results:
        i = i + 1
        if(str(row[0])==str(license)):
            print("The athlete with license", str(license), "in team", str(row[6]) ,"is in position", i, "with", str(row[2]) ,"total points.\n" \
                  "MIN POINTS:",str(row[5]), "\nAVG POINTS:", str(row[3]), "\nMAX POINTS:",  str(row[4]) )
            return

    print("License not found!")


def top_5_from_club(conn, code):

    sql =  "select newTab.completeName, newTab.min as minimum, newTab.avg as average, newTab.max as maximum, newTab.license \
            from (select DISTINCT fact.athleteid, license, completeName, MIN(points) as min, AVG(points) as avg, MAX(points) as max from fact, athlete, \
            club where points is not NULL and fact.athleteid = athlete.athleteid and fact.clubid = club.clubid group by fact.athleteid, code, license, completeName)newTab, club, fact \
            where newTab.athleteid = fact.athleteid and club.clubid = fact.clubid and club.code = '" + code + "' \
            group by (newTab.max, newTab.avg,newTab.min, newTab.completeName,code, license) \
            order by max desc \
            limit 5" 

    cursor_psql = conn.cursor()

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
        
    plt.xlabel("Athletes")
    plt.ylabel("Points")
    plt.boxplot(total_data)
    plt.xticks([1,2,3,4,5], names)
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

    plt.pie(values, labels=['Female', 'Male'], colors=['Pink','royalblue'], autopct='%1.1f%%')
    plt.title("Male vs Female athletes")
    plt.show()


if __name__ == '__main__':

    conn = psycopg2.connect("dbname=datawarehouse user=ricamigu password=password1234")

    print("This program will search for an athlete based on his/her license and return the ranking position of the athlete")
    val = input("\nEnter the athlete's license: ")

    ranking_athlete(conn, val)

    ## -------------------------------------------------------------------------------------------------------------------------
    print("Select an option: ")
    print("1 - Gender distribution per gender")
    print("2 - Boxplot of the best 5 athletes")
    #print("\nThis program will return a boxplot of the top 5 athletes from a club.")
    option = input("> ")

    club = input("Enter the club code:")

    if(int(option) == 1): circular_plot(conn, club)
    else: top_5_from_club(conn, club)
