import matplotlib.pyplot as plt
import numpy as np
import psycopg2

def top_10_clubs(conn):

    sql = "select distinct code, SUM(points) as sum, fact.meetid from club, fact, meet \
            where club.clubid=fact.clubid and points is not null \
            and meet.meetid = fact.meetid \
            group by rollup (code, fact.meetid, code) \
            order by sum desc, meetid"

    cursor_psql = conn.cursor()

    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()

    data_m1 = {}
    data_m2 = {}

    default_meet = 41231234

    m1 = 0
    m2 = 0

    m1_name = "XXII Campeonato Nacional Masters de Verão - OPEN"
    m2_name = "Troféu Pescada - José Carlos Freitas e Troféu Master ANNP"

    for row in results:
        if(m1 >= 10 and m2 >= 10): break

        if(row[0] != None and row[2] != None and (m1 < 10 or m2 < 10)): 
            if(int(row[2]) == default_meet and m1 < 10):
                data_m1[str(row[0])] = int(row[1]) 
                m1 += 1
            elif (m2 < 10): 
                data_m2[str(row[0])] = int(row[1]) 
                m2 += 1

    
    fig, axes = plt.subplots(2)

    codes = list(data_m1.keys())
    values = list(data_m1.values())

    ax = axes[0]
    ax.bar(range(len(data_m1)), values, tick_label=codes)
    ax.set_title("Top 10 clubs by points in meet " + m1_name)
    ax.set_ylabel("Points")
    ax.set_xlabel("Clubs")
    codes = list(data_m2.keys())
    values = list(data_m2.values())

    ax = axes[1]
    ax.bar(range(len(data_m2)), values, tick_label=codes)
    ax.set_title("Top 10 clubs by points in meet " + m2_name)
    ax.set_ylabel("Points")
    ax.set_xlabel("Clubs")
    fig.suptitle('Top 10 clubs by meet')
    fig.tight_layout()
    plt.show()

conn = psycopg2.connect("dbname=datawarehouse user=ricamigu password=password1234")

top_10_clubs(conn)