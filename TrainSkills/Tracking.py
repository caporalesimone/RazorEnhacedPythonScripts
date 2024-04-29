trackButton = 1

while True:
    Player.UseSkill("Tracking")
    while not Gumps.HasGump():
        Misc.Pause(1)
    gump = Gumps.CurrentGump()
    Gumps.SendAction(gump, trackButton) # Select Animals
    
    
    safeExit = 3000
    while not Gumps.HasGump() and safeExit > 0:
        safeExit = safeExit - 1
        Misc.Pause(1)
    
    sleep = 7
    if Gumps.HasGump():
        gump = Gumps.CurrentGump()
        Gumps.SendAction(gump, 1)
        sleep = 10
    
    for i in range(sleep)[::-1]:
        Player.HeadMessage(33,i)
        Misc.Pause(1000)
    
    