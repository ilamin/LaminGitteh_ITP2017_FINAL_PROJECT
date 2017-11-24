import matplotlib.pyplot as plt
import sqlite3

def plotgraph():
#ESTABLISHING CONNECTION BETWEEN THE PROGROM AND SQL 'Bank.db' DATABASE
    connection = sqlite3.connect('Bank.db')
    cursor = connection.cursor()
    cursorforrow = connection.cursor()

#EMPTY LIST TO HOLD VALUES FROM THE DATABASE TABLE
    days = []
    data = []
    getrow = "SELECT count(*) FROM salesrecords"
    getdata = "SELECT dayincome FROM salesrecords"


    cursor.execute(getdata) #GET VALUE FROM THE dayincome column IN THE salesrecords table.
    cursorforrow.execute(getrow) #GET NUMBER OF ROWS IN THE salesrecords table.

    incomedata = cursor.fetchall() #RETRIEVE THE dayincome values.
    rowcount = cursorforrow.fetchall() #RETRIEVE THE length of the row.
    num = int(rowcount[0][0])
    for i in range(0, num):
        days.append("Day "+str(i+1))
        data.append(incomedata[i])
    day = [x for x in range(len(days))]
    plt.plot(data, linewidth = 5)
    plt.title("S-B STATISTICS", fontsize = 24)
    plt.xlabel("Records recorded", fontsize = 14)
    plt.xticks(day, days)
    plt.ylabel("Total daily income", fontsize = 14)
    plt.tick_params(axis = "Both", labelsize = 14)
    plt.show()
    plt.close('all')

plotgraph()