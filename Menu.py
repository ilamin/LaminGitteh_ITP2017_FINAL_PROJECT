import time
clock = time.sleep(1)

def load():
    print(15 * "-", "WELCOME TO MY BANKING SIMULATION", 15 * "-", )
    # List of available services
    services = ["Run Banking", "Manage Teller", "Exit Application"]
    while True:
        for i in range(0, len(services)):
            print("\t\t\t\t\t\t", i + 1, services[i])
        try:
            print(64 * "-")
            select = int(input(
                "\t\t\t\t\t\tSELECT SERVICE TO START\n----------------------------------------------------------------\n:"))
            if select == 1:
                clock = time.sleep(1)
                import Simulation
            elif select == 2:
                clock = time.sleep(1)
                import Operators
            elif select == 3:
                print("GOODBYE")
                raise SystemExit
            else:
                print("INVALID OPTION")
        except ValueError:
            print("OOPS!  INVALID INPUT.. TRY AGAIN")
load()

