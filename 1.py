import matplotlib.pyplot as plt
from datetime import datetime
import pymysql.cursors
from dateutil.relativedelta import relativedelta


host_name="localhost"
db_user="ricardo"
db_password="password1234"
db_name="db_annp"

connection = pymysql.connect(host=host_name,
                             user=db_user,
                             password=db_password,
                             database=db_name,
                             cursorclass=pymysql.cursors.DictCursor)

cur = connection.cursor()

query = "select avg(year(from_days(to_days(now())-to_days(birthdate)))) as age, b.code from athlete a, club b where a.clubid = b.clubid group by b.clubid"

cur.execute(query)

#today = datetime.today()

age_dict = {}

rows = cur.fetchall()

age_list = []
club_list = []

for row in rows:
    age_list.append( int(row['age']) )
    club_list.append( row['code'] )

fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(club_list, age_list, color ='lightsalmon', width = 0.5)
plt.plot(age_list, marker='.', color='black', ms=2)
plt.xticks(rotation=90)
plt.xlabel("Clubs")
plt.ylabel("Average")
plt.title("Age averages for each club")
plt.show()

import seaborn as sns
from numpy import median

sns.set_theme(style="whitegrid")
ax = sns.barplot(x=club_list, y=age_list)
plt.show()
"""
ages = list(age_dict.keys())
values = list(age_dict.values())
x = list(age_dict.keys())
   
num_bins = 10
   
n, bins, patches = plt.hist(x, num_bins, 
                            density = 1, 
                            color ='green',
                            alpha = 0.7)
   
y = values
  
plt.plot(bins, y, '--', color ='black')
  
plt.xlabel('X-Axis')
plt.ylabel('Y-Axis')
  
plt.title('matplotlib.pyplot.hist() function Example\n\n',
          fontweight ="bold")
  
plt.show()

"""