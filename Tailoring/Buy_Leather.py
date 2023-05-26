def findHides():
    return Items.FindByID(0x1079, 0 ,Player.Backpack.Serial, False) # Hides

    
def findCutLeather():
    return Items.FindByID(0x1081, 0 ,Player.Backpack.Serial, False) # Cut Leather
    
    
def findFurTraders():
    found = []
    filter = Mobiles.Filter()
    mobs = Mobiles.ApplyFilter( filter ) 
    if (mobs.Count > 0):
        for m in mobs:
            if "furtrader" in str(m.Properties[0]):
                found.append(m)
    return found

    
def cutHides():
    Target.Cancel()
    scissors = Items.FindByID(0x0F9F, 0 ,Player.Backpack.Serial, False)# Shissors
    Misc.Pause(500)
    hides = findHides()
    if hides is not None:
        Items.UseItem(scissors)
        Target.WaitForTarget(15000, False)
        Target.TargetExecute(hides.Serial)
        Target.Cancel()
    Misc.Pause(500)
        
#############################################################    


mountSerial = 0x0007DF23 # Player.Mount.Serial

traders = findFurTraders()

Mobiles.UseMobile(Player.Serial)
Misc.Pause(1000)

while True:
    Misc.Pause(500)
    emptyvendors = []
    for trader in traders:
        Misc.WaitForContext(trader,15000)
        Misc.ContextReply(trader,1)
        Misc.Pause(500)
        Journal.Clear()
        Player.HeadMessage(77, "Hello, " + trader.Name)
        maxBuy = int((Player.MaxWeight - Player.Weight) / 5)
        Misc.SendMessage(trader.Serial)
        Vendor.Buy(trader.Serial, 0x1079, maxBuy)
        Misc.Pause(500)
        if findHides() is not None:
            cutHides()
            #if Player.Weight > Player.MaxWeight - 100:
            #Misc.Pause(1000)
            #Mobiles.UseMobile(Player.Serial)
            #Misc.Pause(1000)
            leather = findCutLeather()
            Misc.Pause(700)
            Items.Move(leather, Mobiles.FindBySerial(mountSerial), 0)
            Misc.Pause(700)
            #Mobiles.UseMobile(mountSerial)
            #Misc.Pause(1000)
        else:
            emptyvendors.append(trader)
            break
            
        if Journal.Search("Thou hast bought nothing!"):
            emptyvendors.append(trader)
            break
            
    traders = list(set(traders) - set(emptyvendors))
    if len(traders) == 0:
        break
    
Mobiles.UseMobile(mountSerial)
Misc.Pause(1000)        
Misc.SendMessage("Fine")
    
    
    
    
    
    