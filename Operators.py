import sqlite3
from datetime import datetime


#DECLARE SQLLITE DATABASE POINTING TO BANK.DB
connection = sqlite3.connect('Bank.db')
cursor = connection.cursor()


class AllTellers(object):
    #CREATING A TABLE IF NOT EXISTS WITH 2 COLUMNS
    cursor.execute("CREATE TABLE IF NOT EXISTS operators(tellerid TEXT, password TEXT,PRIMARY KEY(tellerid))")
    cursor.execute("SELECT * FROM operators")
    tellerdatabase = cursor.fetchall()

    #FUNCTION TO REGISTER NEW TELLER
    def register(self):
            try:
                self.newteller = input("Enter teller ID\n:")
                self.findaccount = ('SELECT * FROM operators WHERE tellerid = ?')
                for row in cursor.execute(self.findaccount,[(self.newteller)]): #CHECK IF self.newteller value is IN THE DATABASE IF NOT IN THE DATABASE THEN JUMP TO THE ELSE
                    print("\t\t\t\tTeller",self.newteller,"alreadt exists ")
                    print(64*"-")
                    self.comfirm = input("RETURN TO SUB MENU?\t\t\t\tYES - Y | EXIT APPLICATION - E\n----------------------------------------------------------------\n:").lower()
                    if self.comfirm == 'y':
                        starter()
                    elif self.comfirm == 'e':
                        print("GOODBYE")
                        raise SystemExit
                    else:
                        print("INVALID OPTION")
                        starter()
                else:
                    self.newtellerpass = input("Enter password\n:")
                    #INSERT NEW VALUE IN THE operators table.
                    cursor.execute("INSERT INTO operators VALUES ('%s','%s')" % (self.newteller, self.newtellerpass))
                    connection.commit()
                    print("\t\t\t\tTeller",self.newteller,"successfully registered ")
                    print(64*"-")
                    self.comfirm = input("RETURN TO SUB MENU?\t\t\t\tYES - Y | EXIT APPLICATION - E\n----------------------------------------------------------------\n:").lower()
                    if self.comfirm == 'y':
                        starter()
                    elif self.comfirm == 'e':
                        print("GOODBYE")
                        raise SystemExit
                    else:
                        print("INVALID OPTION")
                        starter()
            except ValueError:
                print("OOPS!  INVALID INPUT.. TRY AGAIN") #INVALID INPUT ERROR HANDLER
            except sqlite3.OperationalError:
                print("Error! Connecting to the database") #HANDLE DATABASE BLOCK ERROR

    #FUNCTION TO REMOVE TELLER
    def remove(self):
        while True:
            try:
                self.tellername = input("Enter teller ID to delete\n:")
                self.findaccount = ('SELECT * FROM operators WHERE tellerid = ?')
                for row in cursor.execute(self.findaccount,[(self.tellername)]):
                    find_user = 'DELETE FROM operators WHERE tellerid =?'
                    cursor.execute(find_user, (self.tellername,))
                    connection.commit()
                    print("\t\t\t\tTeller",self.tellername,"successfully deleted ")
                    print(64*"-")
                    self.comfirm = input("RETURN TO SUB MENU?\t\t\t\tYES - Y | EXIT APPLICATION - E\n----------------------------------------------------------------\n:").lower()
                    if self.comfirm == 'y':
                        starter()
                    elif self.comfirm == 'e':
                        print("GOODBYE")
                        raise SystemExit
                    else:
                        print("INVALID OPTION")
                        starter()
                else:
                    print("----------------[ Teller ID",self.tellername.upper(),"not found ]-------------------")
                    break

            except ValueError:
                print ("OOPS!  INVALID INPUT.. TRY AGAIN")
            except sqlite3.OperationalError:
                print("Error! Connecting to the database")

    #VIEW LIST OF TELLERS in the tellerid TABLE
    def viewtellers(self):
        while True:
            try:
                cursorforrow = connection.cursor()
                findaccount = ('SELECT tellerid FROM operators')
                getrow = "SELECT count(*) FROM operators"
                cursor.execute(findaccount)
                cursorforrow.execute(getrow)
                rowcount = cursorforrow.fetchall()
                connection.commit()
                getall = cursor.fetchall()
                num = int(rowcount[0][0])
                for i in range (0,num):
                    tellers = sorted([x[0] for x in getall]).pop(i) #Convert the tuple to list and pop the value to tellers.
                    print("\t\t\t\t", i + 1,"\t",tellers)
                print(64 * "-")
                comfirm = input("RETURN TO SUB MENU?\t\t\t\tYES - Y | EXIT APPLICATION - E\n----------------------------------------------------------------\n:").lower()
                if comfirm == 'y':
                    starter()
                elif comfirm == 'e':
                    print("GOODBYE")
                    raise SystemExit
                else:
                    print("INVALID OPTION")
                    starter()
            except ValueError:
                print("OOPS!  INVALID INPUT.. TRY AGAIN")
            except sqlite3.OperationalError:
                print("Error! Connecting to the database")

    #FUNCTION TO CHANGE TELLER PASS
    def change(self):
        while True:
            try:
                connection = sqlite3.connect('Bank.db')
                cursor = connection.cursor()
                print(14*"-"," ENTER YOUR TELLER ID AND PASSWORD",14*"-")
                telleraccount = input("Enter teller ID:\n")
                findaccount = ('SELECT * FROM operators WHERE tellerid = ?')
                for tellercheck in cursor.execute(findaccount,[(telleraccount)]):
                    break
                else:
                    print("-------------[ NO ACCOUNT FOUND FOR :",telleraccount.upper(),"]----------------")
                    starter()
                tellerspass = str(input("Enter teller password:\n"))
                findpassword = 'SELECT * FROM operators WHERE tellerid = ?'
                cursor.execute(findpassword, (telleraccount,))
                foundteller = cursor.fetchall()
                theteller = foundteller[0][1]
                if tellerspass == theteller:  # Comparing password
                    pass1 = str(input("Enter new password:\n"))
                    pass2 = str(input("Confirm new password:\n"))
                    if pass1 == pass2:
                        updating = '''UPDATE operators SET password = ? WHERE tellerid = ?'''
                        cursor.execute(updating,(pass1,telleraccount))
                        connection.commit()
                        print("\t\t\t\tCongrats", telleraccount, " password successfully changed")
                        print(64 * "-")
                        cp_comfirm = input(
                            "RETURN TO SUB MENU?\t\t\t\tYES - Y | EXIT APPLICATION - E\n----------------------------------------------------------------\n:").lower()
                        if cp_comfirm == 'y':
                            starter()
                        elif cp_comfirm == 'e':
                            print("GOODBYE")
                            raise SystemExit
                        else:
                            print("INVALID OPTION")
                            starter()
                    else:
                        print("PASSWORD DOES NOT MATCH - TRY AGAIN")
                        break
                else:
                    print("WRONG PASSWORD")
                    starter()

            except ValueError:
                print ("OOPS!  INVALID INPUT.. TRY AGAIN")
            except sqlite3.OperationalError:
                print("Error! Connecting to the database")

print(8*"-"," WELCOME TO MY BANKING REGISTRATION SIMULATION",8*"-",)
print(64*"-")

menu = ["Add new teller","View tellers","Change Teller Password","Remove teller","Main Menu","Exit Application"]
def starter():
    while True:
        try:
            for i in range(0,len(menu)):
                print(i+1,"",menu[i])
            print(64*"-")
            select = int(input("\t\t\t\t\t\tSELECT SERVICE TO START\n----------------------------------------------------------------\n:"))
            if select == 1:
                run = AllTellers().register()
            elif select == 2:
                run = AllTellers().viewtellers()
            elif select == 3:
                run = AllTellers().change()
            elif select == 4:
                run = AllTellers().remove()
            elif select == 5:
                import Menu

            elif select == 6:
                print("GOODBYE")
                raise SystemExit

            else:
                print("CHOOSE A VALID OPTION")

        except ValueError:
            print ("OOPS!  INVALID INPUT.. TRY AGAIN")
starter()
