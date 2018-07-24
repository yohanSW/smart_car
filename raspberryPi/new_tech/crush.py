def crush():
    #set var

    while True :
        while True :

            Accident = 0 

            if fire == 1 :
                print("Fire Fire Fire")
                Accident = 1

            if heartpulse >= 130 and heartpulse <=40 :
                print("Driver is under heart attack")
                #if heart attack has been happend, Auto driving must be started!!
                Accident = 1

            if impact == 1 and sona <= 40 :
                print("Car crush has been happened")
                Accident = 1
        
        
            if Accident == 1 :
                gpsx, gpsy = gps()

                break


def sensing():
