import matplotlib.pyplot as plt
import psycopg2

conn = psycopg2.connect("dbname=datawarehouse user=ricamigu password=password1234")

sql = "select newTab2.age_range, AVG(newTab2.swimTimeMiliseconds) as avg_Time, gender, newTab2.meetid \
    from (select fact.meetid, fact.athleteid, (EXTRACT(epoch FROM swimtime::time)*100) as swimTimeMiliseconds, gender, \
    case when newTable.age between 25 and 29 then 'A' when newTable.age between 30 and 34 then 'B' \
    when newTable.age between 35 and 39 then 'C' when newTable.age between 40 and 44 then 'D' \
    when newTable.age between 45 and 49 then 'E' when newTable.age between 50 and 54 then 'F' \
    when newTable.age between 55 and 59 then 'G' when newTable.age between 60 and 64 then 'H' \
    when newTable.age between 65 and 69 then 'I' when newTable.age between 70 and 74 then 'J' \
    when newTable.age between 75 and 79 then 'K' when newTable.age between 80 and 84 then 'L' \
    when newTable.age between 85 and 89 then 'M' when newTable.age between 90 and 94 then 'N' \
    when newTable.age between 95 and 99 then 'O'  END as age_range, newTable.age \
        from (select fact.meetid, gender, fact.athleteid, EXTRACT(year FROM age(current_date,birthdate::timestamp)) :: int as age \
            from athlete, fact, meet where fact.athleteid = athlete.athleteid and fact.meetid = meet.meetid)newTable, \
            fact where newTable.athleteId = fact.athleteId and swimtime != '00:00:00' and newTable.meetid = fact.meetid \
        order by age)newTab2 group by rollup (newTab2.age_range, gender, newTab2.meetid) \
        order by newTab2.age_range, gender"

default_meetid = 41231234

cursor_psql = conn.cursor()

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

data_male_1 = {}
data_male_2 = {}
data_female_1 = {}
data_female_2 = {}

for row in results:
    print(row)
    if(row[2] == 'M'): 
        if( row[3] != None):
            if(int(row[3]) == default_meetid): data_male_1[row[0]] = int(row[1])
            else: 
                data_male_2[row[0]] = int(row[1])

    elif(row[2] == 'F'): 
        if(row[3] != None):
            if(int(row[3]) == default_meetid): data_female_1[row[0]] = int(row[1])
            else: 
                data_female_2[row[0]] = int(row[1])


categories = list(data_male_1.keys())

values_male_1 = list(data_male_1.values())
values_male_2 = list(data_male_2.values())
values_female_1 = list(data_female_1.values())
values_female_2 = list(data_female_2.values())

plt.title("Average times by category, gender and meet")
plt.xlabel("Categories")
plt.ylabel("Times")
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12], categories)
plt.plot(values_male_1, label="Men from meet " + str(default_meetid), color='royalblue')
plt.plot(values_male_2, label="Men from meet " + str(default_meetid+1), color='darkturquoise', linestyle="--")
plt.plot(values_female_1, label="Women from meet " + str(default_meetid), color='pink')
plt.plot(values_female_2, label="Women from meet " + str(default_meetid+1), color='mediumvioletred',  linestyle="--")
plt.legend()
plt.show()