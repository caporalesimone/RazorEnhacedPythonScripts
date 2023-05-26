def doLock(box):
    Player.HeadMessage(33, "Locking the box")
    Misc.Pause(1000)
    Items.UseItem(0x4109A387)
    Target.WaitForTarget(11000, False)
    Target.TargetExecute(box)
    Misc.Pause(1000)
    Player.HeadMessage(33, "Box locked")


def ManageEvent(box):
    
    txt1 = "does not appear to be locked"
    txt2 = "The lock quickly yields to your skill."
    txt3 = "You don't see how that lock can be manipulated."
    txt4 = "You broke the lockpick"
    txt5 = "You are unable to pick the lock"
    
    while not Journal.Search(txt1) and not Journal.Search(txt2) and not Journal.Search(txt3) and not Journal.Search(txt4) and not Journal.Search(txt5): 
        Misc.Pause(100)
        
    if Journal.Search(txt1):
        Player.HeadMessage(33, "Box was open")
        doLock(box)
        
    if Journal.Search(txt2):
        doLock(box)
        
    if Journal.Search(txt3):
        Player.HeadMessage(33, "Too much difficoult, change box")
        
    if Journal.Search(txt4):
        Player.HeadMessage(33, "Broke Lockpick")
        
    Misc.Pause(1000)
    return

            
box = Target.PromptTarget("Box to be unlocked")
while True:
    Journal.Clear()
    Player.HeadMessage(33, "Lockpicking: " + str(Player.GetSkillValue("Lockpicking")))
    Items.UseItemByID(0x14FC, 0)
    Target.WaitForTarget(11000, False)
    Target.TargetExecute(box)
    ManageEvent(box)
    
