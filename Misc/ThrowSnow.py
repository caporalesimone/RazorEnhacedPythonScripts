import random
from System.Collections.Generic import List
from System import Byte


TROW_TIMEOUT = 10000 # Throw every 10 seconds

snowID = 0x0913

snowSerial = Items.FindByID(snowID, -1, Player.Backpack.Serial, 0, False)
if snowSerial is None:
    Player.HeadMessage(33, "You don't have the snow in your main backpack")
else:
    mobileFilter = Mobiles.Filter()
    mobileFilter.Enabled = True
    mobileFilter.RangeMin = 0
    mobileFilter.RangeMax = 5
    mobileFilter.CheckLineOfSight = True
    mobileFilter.IsGhost = False  
    mobileFilter.Notorieties = List[Byte](bytes([1,2])) 
    #Notorieties:
    #   1: blue, innocent
    #   2: green, friend
    #   3: gray, neutral
    #   4: gray, criminal
    #   5: orange, enemy
    #   6: red, hostile 
    #   7: yellow, invulnerable    
    while True:
        people = Mobiles.ApplyFilter(mobileFilter)
        randomPerson = random.choice(people)
        Player.HeadMessage(33, "Trowing to " + randomPerson.Name)
        Mobiles.Message(randomPerson.Serial,33,"Got Me",True)
        Items.UseItem(snowSerial)
        Target.WaitForTarget(2000)
        Target.TargetExecute(randomPerson)
        Misc.Pause(TROW_TIMEOUT)

        
