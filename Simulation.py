from datetime import datetime
import sqlite3

import os

chosenservice = 0
connection = sqlite3.connect('Bank.db')
cursor = connection.cursor()

class MyImports():
    def menu(self):
        import Menu
    def statistic(self):
        import Statistic
        Statistic.plotgraph()
    def tellers(self):
        import Operators

#BANK CLASS
class Bank(MyImports):
        #DICTONARY OF AVAILABLE SERVICES
        services = {1: '\tOpen Account ',
                    2: '\tDeposit',
                    3: '\tWithdraw',
                    4: '\tTransfer',
                    5: '\tUser A/C Status',
                    6: '\tClose Account',
                    7:'\tView All Transaction',
                    8: '\tCurrent Income',
                    9: '\tView Statistic',
                    10: '\tLock Session',
                    11: '\tExit Application\n----------------------------------------------------------------'}
        #TO HOLD INCOME VALUES
        accountstransactions = {}

        #TO HOLD LOGS
        records = []

        #TO HOLD TOTAL INCOME
        income = 0

        #GLOBAL LOGIN DETAILS TO UNLOCK ACCOUNT
        global login
        global logpass

#TRANSACTIONS CLASS INHERITING BANK CLASS
class Transactions(Bank):
    global chosenservice
    def __init__(self,operatorid,password):
        self.start()
    def start(self):
        print(64*"-")
        while True:
            for i in self.services:
                print(i,self.services[i])
            try:
                chosenservice = int(input("\t\t\t\t\tCHOOSE SERVICE TO START\n----------------------------------------------------------------\n:"))
                self.choose(chosenservice)
            except ValueError:
                print ("OOPS!  INVALID INPUT.. TRY AGAIN")

#ACCESS METHODS WITHIN THE CLASS
    def choose(self, chosenoption):
        if chosenoption == 1:
            self.newaccount()
        if chosenoption == 2:
            self.deposit()
        if chosenoption == 3:
            self.withdrawal()
        if chosenoption == 4:
            self.transfer()
        if chosenoption == 5:
            self.useraccount()
        if chosenoption == 6:
            self.remove()
        if chosenoption == 7:
            self.allrecords()
        if chosenoption == 8:
            self.dailyincome()
        if chosenoption == 9:
            self.incomestatistic()
        if chosenoption ==10:
            self.lockscreen()
        if chosenoption ==11:
            self.exitapplication()
        else:
            print("---------SORRY! THE SERVICE YOUR SELECTED IS UNVAILABLE---------")
            choose_comfirm = input("[SELECT FROM AVAILABLE SERVICES? YES - Y | EXIT - E ]\n:").lower()
            if choose_comfirm == 'y':
                pass
            elif choose_comfirm == 'e':
                print("GOOD-BYE")
                raise SystemExit
            else:
                print("GOOD-BYE")
                raise SystemExit


# 1 FUNCTION TO CREATE NEW ACCOUNT
    def newaccount(self):
        print(10 * "-", "STARTING NEW ACCOUNT REGISTRATIONS SERVICE", 10 * "-")
        try:
            connection = sqlite3.connect("Bank.db")
            cursor = connection.cursor()
            #CREATE TABLE customers in Bank.db DATABASE IF NOT EXITS
            cursor.execute("CREATE TABLE IF NOT EXISTS customers (accnumber NUMERIC,accbalance REAL)")
            # GET THE CURRENT ROW COUNT OF custmers table
            cursor.execute("SELECT count(*) FROM customers")
            ua_lastrow = cursor.fetchall()
            ua_getlastrow = ua_lastrow[0][0]
            # ADD 1 TO THE CURRENT ROW LENGTH
            newcustomeraccount = ua_getlastrow + 1
            print('Your A/C No is : ', newcustomeraccount)
            ua_openingbalance = int(input("Opening Balance\n:"))
            #INSERT VALUE INTO customers TABLE
            cursor.execute("INSERT INTO customers VALUES (%d,%d)" % (newcustomeraccount, ua_openingbalance))
            #SAVE THE STATEMENT
            connection.commit()
            #ADD THE NEW ACCOUNT NUMBER AND OPENING BALANCE TO accountstransactions dictionary.
            self.accountstransactions.update({newcustomeraccount: ua_openingbalance})
            #GET THE CURRENT TIME
            ua_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            # ADD THE NEW ACCOUNT NUMBEROPENING BALANCE  AND TIME TO records list.
            self.records.append("%d created account : O/B %d at %s" % (newcustomeraccount, ua_openingbalance, ua_time))
            self.income += ua_openingbalance
            print("[", newcustomeraccount, "] successfully created an A/C with opening balance = [", ua_openingbalance,"]")
            print(64 * "-")
            ua_comfirm = input("RETURN TO SUB MENU?\t\t\t\t\t\t\tYES - Y | EXIT - E \n----------------------------------------------------------------\n:").lower()
            if ua_comfirm == 'y':
                self.start()
            elif ua_comfirm == 'e':
                print("GOOD-BYE")
                raise SystemExit
            else:
                print("INVALID OPTION")
                self.start()

        except ValueError:
            print ("OOPS!  INVALID INPUT.. TRY AGAIN")
        except sqlite3.OperationalError:
            print("Error! Connecting to the database")

# 2 FUNCTION TO CREATE TO DEPOSIT
    def deposit(self):
        while True:
            try:
                connection = sqlite3.connect("Bank.db")
                cursor = connection.cursor()
                print(13 * "-", "STARTING CUSTOMER DEPOSITING SERVICE", 13 * "-")
                customeraccount = int(input("Enter account number to deposit:\n"))
                findaccount = 'SELECT * FROM customers WHERE accnumber = ?'
                for row in cursor.execute(findaccount,(customeraccount,)):
                    break
                else:
                    print("-------------[ NO ACCOUNT FOUND WITH A/C NO :", customeraccount, "]----------------")
                    self.start()
                findaccount = ('SELECT * FROM customers WHERE accnumber = ?')
                cursor.execute(findaccount, [(customeraccount)])
                customerdeposit = int(input("Enter deposit amount:\n"))
                getdepositaccount = cursor.fetchall()
                deposittobalance = getdepositaccount[0][1]
                currentbalance = customerdeposit + deposittobalance
                cursor.execute("UPDATE customers SET accbalance = %d WHERE accnumber = %d" % (currentbalance, customeraccount))
                connection.commit()
                time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                print("--------[ A/C No :", customeraccount, "successfully deposited : Rp",customerdeposit, "]---------")
                self.records.append("%d deposited : %d at %s" % (customeraccount, customerdeposit, time))
                self.accountstransactions.update({customeraccount: customerdeposit})
                self.income += customerdeposit
                print(64 * "-")
                comfirm = input("RETURN TO SUB MENU?\t\t\t\t\t\t\tYES - Y | EXIT - E\n----------------------------------------------------------------\n:").lower()
                if comfirm == 'y':
                    self.start()
                elif comfirm == 'e':
                    print("GOOD-EYE")
                    raise SystemExit
                else:
                    print("INVALID OPTION")
                    self.start()

            except ValueError:
                print("OOPS!  INVALID INPUT.. TRY AGAIN")
            except sqlite3.OperationalError:
                print("Error! Connecting to the database")

#3 FUNCTION TO WITHDRAW
    def withdrawal(self):
        while True:
            try:
                connection = sqlite3.connect("Bank.db")
                cursor = connection.cursor()
                print(13 * "-", "STARTING CUSTOMER WITHDRAWAL SERVICE", 13 * "-")
                customeraccount = int(input("Enter account number to withdraw from:\n"))
                findaccount = ('SELECT * FROM customers WHERE accnumber = ?')
                for row in cursor.execute(findaccount, (customeraccount,)):
                    break
                else:
                    print("-------------[ NO ACCOUNT FOUND WITH A/C NO :", customeraccount, "]----------------")
                    self.start()
                cursor.execute(findaccount, (customeraccount,))
                customerwithdrawal = int(input("Enter withdraw amount:\n"))
                getwithdrawalaccount = cursor.fetchall()
                customersbalance = getwithdrawalaccount[0][1]
                afterwithdrawn = customersbalance - customerwithdrawal
                if customersbalance >= customerwithdrawal:
                    cursor.execute("UPDATE customers SET accbalance = %d WHERE accnumber = %d" % (afterwithdrawn,customeraccount))
                    connection.commit()
                    time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                    print("-------[ A/C No :", customeraccount,"successfully withdrawn : Rp",customerwithdrawal,"]---------")
                    self.records.append("%d withdrawn : %d at %s" % (customeraccount, customerwithdrawal, time))
                    self.income += customerwithdrawal
                    print(64 * "-")
                    comfirm = input("RETURN TO SUB MENU?\t\t\t\t\t\t\tYES - Y | EXIT - E \n----------------------------------------------------------------\n:").lower()
                    if comfirm == 'y':
                        self.start()
                    elif comfirm == 'n':
                        print("GOOD-BYE")
                        raise SystemExit
                    else:
                        print("INVALID OPTION")
                        self.start()
                else:
                    print("YOUR HAVE INSUFFICIENT BALANCE")
                    self.start()
            except ValueError:
                print("OOPS!  INVALID INPUT.. TRY AGAIN")
            except sqlite3.OperationalError:
                print("Error! Connecting to the database")



# 4 FUNCTION TO TRANSFER
    def transfer(self):
        print(12 * "-", "STARTING CUSTOMER TRANSFERRING SERVICE", 12 * "-")
        while True:
            connection = sqlite3.connect("Bank.db")
            cursor = connection.cursor()
            try:
                transferfrom = int(input("Enter account number to transfer from:\n"))
                findaccount = 'SELECT * FROM customers WHERE accnumber = ?'
                for row in cursor.execute(findaccount, (transferfrom,)):
                    break
                else:
                    print("-------------[ NO ACCOUNT FOUND FOR A/C NO :", transferfrom, "]----------------")
                    self.start()
                cursor.execute(findaccount, (transferfrom,))
                results = cursor.fetchall()
                gettransferfromaccount = results[0][0]
                gettransferfrombalance = results[0][1]
                transferto = int(input("Enter account number to transfer to:\n"))
                for row in cursor.execute(findaccount, (transferto,)):
                    break
                else:
                    findaccount = 'SELECT * FROM customers WHERE accnumber = ?'
                    cursor.execute(findaccount, (transferto,))
                    results = cursor.fetchall()
                    print(" -------------[INTERNATIONAL BANKING 5% CHARGES]----------------")
                    transferamount = int(input("Enter transfer amount:\n"))
                    charges = ((transferamount * 5) / 100)
                    totalcharges = transferamount + charges
                    if gettransferfrombalance >= totalcharges:
                        transfromcurrentbalance = gettransferfrombalance - totalcharges
                        cursor.execute("UPDATE customers SET accbalance = %d WHERE accnumber = %d" % (transfromcurrentbalance, transferfrom))
                        connection.commit()
                        time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                        print("-----[A/C No:", transferfrom, "successfully transferred : Rp", transferamount, "to A/C No:",transferto, "]-----")
                        self.records.append("%d transfered %d to account %d: at %s" % (transferfrom, transferamount, transferto, time))
                        print(64 * "-")
                        comfirm = input("RETURN TO SUB MENU?\t\t\t\t\t\t\tYES - Y | EXIT - E\n----------------------------------------------------------------\n:").lower()
                        if comfirm == 'y':
                            self.start()
                        elif comfirm == 'e':
                            print("GOODBYE")
                            raise SystemExit
                        else:
                            print("INVALID OPTION")
                            self.start()
                    else:
                        print("YOU HAVE UNSUFFICIENT BALANCE")
                        self.start()
                cursor.execute(findaccount,(transferto,))
                results = cursor.fetchall()
                gettransfertoaccount = results[0][0]
                gettransfertobalance = results[0][1]
                print("----------------------[DOMESTIC BANKING]------------------------")
                transferamount = int(input("Enter transfer amount:\n"))
                if gettransferfrombalance >= transferamount:
                    transfromcurrentbalance = int(gettransferfrombalance - transferamount)
                    transtocurrentbalance = int(gettransfertobalance + transferamount)
                    cursor.execute("UPDATE customers SET accbalance = %d WHERE accnumber = %d" % (transfromcurrentbalance, transferfrom))
                    cursor.execute("UPDATE customers SET accbalance = %d WHERE accnumber = %d" % (transtocurrentbalance, transferto))
                    connection.commit()
                    time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                    print("--[A/C No:", transferfrom, "successfully transferred : Rp", transferamount,"to A/C No:", transferto, "]--")
                    self.records.append("%d transfered %d to account %d: at %s" % (transferfrom, transferamount, transferto, time))
                    print(64 * "-")
                    comfirm = input("RETURN TO SUB MENU?\t\t\t\t\t\t\tYES - Y | EXIT - E\n----------------------------------------------------------------\n:").lower()
                    if comfirm == 'y':
                        self.start()
                    elif comfirm == 'e':
                        print("GOODBYE")
                        raise SystemExit
                    else:
                        print("INVALID OPTION")
                        self.start()
                else:
                    print("YOU HAVE UNSUFFICIENT BALANCE")
                    self.start()

            except ValueError:
                print("OOPS! INVALID INPUT.. TRY AGAIN")
            except sqlite3.OperationalError:
                print("Error! Connecting to the database")


#5 FUNCTION TO FOR ACCOUNNT INFORMATION
    def useraccount(self):
        try:
            uanumber = int(input("Enter customer's A/C\n:"))
            check = "SELECT accnumber FROM customers WHERE accnumber = ?"
            for accounts in cursor.execute(check,[uanumber]):
                break
            else:
                print("-------------[ NO ACCOUNT FOUND WITH A/C NO :", uanumber, "]----------------")
                self.start()
            check = "SELECT accbalance FROM customers WHERE accnumber = ?"
            cursor.execute(check, [uanumber])
            balanceresult = cursor.fetchall()
            uaresult = balanceresult[0][0]
            print(20 * "-", "A/C:", uanumber, " BALANCE STATUS", 20 * "-")
            print("\t\t\t\t  Current balance is Rp:", uaresult, )
            print(64 * "-")
            comfirm = input("RETURN TO SUB MENU?\t\t\t\t\t\t\tYES - Y | EXIT - E\n----------------------------------------------------------------\n:").lower()
            if comfirm == 'y':
                self.start()
            elif comfirm == 'e':
                print("GOOD-BYE")
                raise SystemExit
            else:
                print("INVALID OPTION")
                self.start()

        except ValueError:
            print("OOPS! INVALID INPUT.. TRY AGAIN")
        except sqlite3.OperationalError:
            print("Error! Connecting to the database")

#6 FUNCTION TO CLOSE ACCOUNT
    def remove(self):
        try:
            connection = sqlite3.connect("Bank.db")
            cursor = connection.cursor()
            ranumber = int(input("Enter customer's A/C\n:"))
            check = "SELECT accnumber FROM customers WHERE accnumber = ?"
            for accounts in cursor.execute(check, [ranumber]):
                break
            else:
                print("-------------[ NO ACCOUNT FOUND WITH A/C NO :", ranumber, "]----------------")
                self.start()
            cursor.execute("DELETE FROM customers WHERE accnumber = ?",(ranumber,))
            connection.commit()
            time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            print("----------[A/C No:", ranumber, "successfully closed account]----------")
            self.records.append("%d closed account: at %s" % (ranumber, time))
            print(64 * "-")
            comfirm = input("RETURN TO SUB MENU?\t\t\t\t\t\t\tYES - Y | EXIT - E\n----------------------------------------------------------------\n:").lower()
            if comfirm == 'y':
                self.start()
            elif comfirm == 'e':
                print("GOOD-BYE")
                raise SystemExit
            else:
                print("INVALID OPTION")
                self.start()

        except ValueError:
            print("OOPS! INVALID INPUT.. TRY AGAIN")
        except sqlite3.OperationalError:
            print("Error! Connecting to the database")


#7  FUNCTION TO PRINT ALL RECORDS
    def allrecords(self):
        print (19*"-","[ LIST ALL TRANSACTIONS ]",19*"-")
        if len(self.records)== 0:
            print("\t\t\t\t\t","  Your record is empty")
            self.start()
        else:
            for i in range (0,len(self.records)):
                print(i+1,"[",self.records[i],"]",)
            print(64*"-")
            try:
                arr_comfirm = input("RETURN TO SUB MENU?\t\t\t\t\t\t\tYES - Y | EXIT - E\n----------------------------------------------------------------\n:").lower()
                if arr_comfirm == 'y':
                    self.start()
                elif arr_comfirm == 'e':
                    print("GOOD-BYE")
                    raise SystemExit
                else:
                    print("INVALID OPTION")
                    self.start()
            except ValueError:
                print("OOPS!  INVALID INPUT.. TRY AGAIN")

#8  FUNCTION TO PRINT DAILY INCOME
    def dailyincome(self):
            #Set the income features unavailable if income is 0
            if self.income != 0:
                print(22 * "-", "PRINT DAILY INCOME", 22 * "-")
                print("\t\t\t\t\tYour daily income is :", self.income)
                try:
                    print(64 * "-")
                    di_comfirm = input("FILTER CURRENT INCOME?  \t\t\t\t\t\tYES - Y | NO - N\n----------------------------------------------------------------\n:").lower()
                    if di_comfirm == 'y':
                        self.incomelist = ['Maximum Transaction', 'Lowest Transaction','Back to Menu']
                        for i in range(0, len(self.incomelist)):
                            print(i + 1, "\t", self.incomelist[i])
                        print(64 * "-")
                        dis_comfirm = int(input("\t\t\t\t\t\tSELECT OPTION?\n————————————————————————————————————————————————————————————————\n:"))
                        if dis_comfirm == 1:
                            print(24 * "-", "MAXMUM TRANSACTION", 24 * "-")
                            maximum = max(self.accountstransactions, key=self.accountstransactions.get)
                            print("\t\t\tYour maximum income is : [", maximum, "]", self.accountstransactions[maximum])
                            print(64 * "-")
                            self.start()
                        elif dis_comfirm == 2:
                            print(23 * "-", "MINUMUM TRANSACTION", 23 * "-")
                            minimum = min(self.accountstransactions, key=self.accountstransactions.get)
                            print("\t\t\t\t\tYour minimum income is : [", minimum, "]", self.accountstransactions[minimum],[minimum])
                            print(64 * "-")
                            self.start()
                        elif dis_comfirm == 3:
                            self.start()
                        else:
                            print("\t\t\t\t\t\tINVALID OPTION")
                            self.start()
                    elif di_comfirm == 'n':
                        self.start()
                    else:
                        print("INVALID OPTION")
                        self.start()

                except ValueError:
                    print("OOPS!  INVALID INPUT.. TRY AGAIN")
            else:
                print("\t\t\t\t\tYour current income is :", self.income)
                self.start()



#9 FUNCTION TO TO VIEW STATISTIC
    def incomestatistic(self):
        try:
            connection = sqlite3.connect("Bank.db")
            cursor = connection.cursor()
            print (19*"-","MONTHLY INCOME STATISTIC",19*"-")
            self.submenu = ["Update Statistic & Run ","View current Statistic","Back to Menu"]
            # view = ""
            for i in range (len(self.submenu)):
                print(i+1,"\t",self.submenu[i])
                # view += " ["+str(i+1)+"] "+submenu[i]+"\t\t\t\t\t"
            print(64*"-")
            #print(view)
            s_comfirm = int(input("\t\t\t\t\t\tSELECT OPTION?\n----------------------------------------------------------------\n:"))
            if s_comfirm == 1:
                cursor.execute("SELECT count(*) FROM salesrecords")
                self.showlastrow = cursor.fetchall()
                self.thelastrow = self.showlastrow [0][0] + 1
                self.counter = "day"+str(self.thelastrow)
                cursor.execute("INSERT INTO salesrecords VALUES ('%s','%d')" % (self.counter, self.income))
                connection.commit()
                print("Income for ",self.counter.upper(),"successfully saved")
                self.statistic()
                self.start()
                print(" ------------------- RECORD SAVED SUCCESSFUL ------------------- ")
                print(64*"-")
                sr_comfirm = input("RETURN TO SUB MENU?\t\t\t\t\t\t\tYES - Y | EXIT - E\n----------------------------------------------------------------\n:").lower()
                if sr_comfirm == 'y':
                    self.start()
                elif sr_comfirm == 'e':
                    print("GOODBYE")
                    raise SystemExit
                else:
                    print("INVALID OPTION")
                    self.start()

            elif s_comfirm == 2:
                self.statistic()
                self.start()
            elif s_comfirm == 3:
                self.start()
            else:
                print("INVALID OPTION")
                self.start()
        except ValueError:
            print("OOPS!  INVALID INPUT.. TRY AGAIN")
        except sqlite3.OperationalError:
            print("Error! Connecting to the database")

#10  FUNCTION TO LOCK USER SESSION
    def lockscreen(self):
        self.process = True
        while self.process:
            try:
                print("ACCOUNT LOCKED..... ENTER PASSWORD TO UNLOCKED")
                self.unlogin = input("Enter ID:\n")
                self.unlocklogpass = input("Enter Password:\n")
                if self.unlogin == login and self.unlocklogpass == logpass:
                        self.start()
                else:
                    print("NO USER | WRONG PASSWORD")

            except ValueError:
                print ("OOPS!  INVALID INPUT.. TRY AGAIN")

#11 FUNCTION TO EXIT THE APPLICATION
    def exitapplication(self):
        try:
            log_comfirm = input("SAVE YOUR INCOME BEFORE LOGOUT?\t\t\t\tYES - Y | NO - N\n----------------------------------------------------------------\n:").lower()
            if log_comfirm == 'y':
                cursor.execute("SELECT count(*) FROM salesrecords")
                self.showlastrow = cursor.fetchall()
                self.thelastrow = self.showlastrow[0][0] + 1
                self.counter = "day" + str(self.thelastrow)
                cursor.execute("INSERT INTO salesrecords VALUES ('%s','%d')" % (self.counter, self.income))
                connection.commit()
                print(64 * "-")
                print("------------- Income for ", self.counter.upper(), " successfully saved ------------")
                print(64 * "-")
                print("GOODBYE")
                raise SystemExit
            elif log_comfirm == 'n':
                print("GOODBYE")
                raise SystemExit
            else:
                print("INVALID OPTION")
                self.start()
        except ValueError:
            print("OOPS!  INVALID INPUT.. TRY AGAIN")
        except sqlite3.OperationalError:
            print("Error! Connecting to the database")

global login
global logpass
while True:
    try:
        print(15*"-","WELCOME TO MY BANKING SIMULATION",15*"-",)
        print(16*"-","ENTER YOUR LOGIN DETAILS BELOW",16*"-",)
        login = input("Enter ID\n:")
        logpass = input("Enter Password\n:")
        with sqlite3.connect("Bank.db") as connection:
            cursor = connection.cursor()
            find_user = ('SELECT * FROM operators WHERE tellerid = ? AND password = ?')
            cursor.execute(find_user,[(login),(logpass)])
            results = cursor.fetchall()
            if results:
                print(64*"-")
                print("\t\t\t\t\t\t","WELCOME",login.upper())
                while True:
                        __user = Transactions(login,logpass)
                        __user.choose()
            else:
                print("\t\t\t\t No Teller account found for",login)
                print(64*"-")
                teller_comfirm = input("TRY AGAIN?  \t\t\t\t\t\t\tYES - Y | NO - N\n----------------------------------------------------------------\n:").lower()
                if teller_comfirm == 'y':
                    pass
                elif teller_comfirm == 'n':
                    print("GOOD-BYE")
                    raise SystemExit
                else:
                    print("GOOD-BYE")
                    raise SystemExit

    except ValueError:
        print ("OOPS!  INVALID INPUT.. TRY AGAIN")
    except sqlite3.OperationalError:
        print("Error! Connecting to the database")




