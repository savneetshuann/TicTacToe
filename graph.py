import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import sqlite3

fig = plt.figure()
ax = fig.add_subplot(111)

dat = sqlite3.connect('player_info.db')
g = dat.cursor()
g.execute(
        'SELECT * FROM(SELECT user_name,points, RANK() OVER (ORDER BY points DESC) PRANK FROM players) WHERE '
        'PRANK <=3')

engine = create_engine('mssql+pymssql://**:****@127.0.0.1:1433/AffectV_Test')
connection = engine.connect()
result = connection.execute('SELECT Campaign_id, SUM(Count) AS Total_Count FROM Impressions GROUP BY Campaign_id')


## the data

data = []
xTickMarks = []

for row in result:
   data.append(int(row[1]))
   xTickMarks.append(str(row[0]))

connection.close()


## necessary variables
ind = np.arange(len(data))                # the x locations for the groups
width = 0.35                      # the width of the bars

## the bars
rects1 = ax.bar(ind, data, width,
                color='black',
                error_kw=dict(elinewidth=2,ecolor='red'))


# axes and labels
ax.set_xlim(-width,len(ind)+width)
ax.set_ylim(0,45)


ax.set_ylabel('Y LABEL')
ax.set_xlabel('X LABEL')
ax.set_title('TITLE_HERE')

ax.set_xticks(ind+width)
xtickNames = ax.set_xticklabels(xTickMarks)
plt.setp(xtickNames, rotation=45, fontsize=10)


plt.show()