# Gather from Mining Cart and Tree Stump
# Target ground for stop script

hatchet = 0x41DB0B09 # Default Hatchet, if not exists request for a target

while True:
    itm = Items.FindBySerial(Target.PromptTarget())
    if itm is None:
        break
    Journal.Clear()
    i = 1
    while not Journal.Search("There are no more"):
        if Journal.Search("Your backpack is full"):
            break
        Items.Message(itm,33,str(i))
        Items.UseItem(itm)
        Misc.Pause(700)
        i = i + 1
    
    Misc.SendMessage("Looking for logs")
    while True:
        logs = Items.FindByID(0x1BDD, -1, Player.Backpack.Serial)
        if logs is None:
            Misc.SendMessage("No logs in backpack")
            break
        if (hatchet == 0):
            Player.HeadMessage(33, "Target an Hatchet")
            hatchet = Items.FindBySerial(Target.PromptTarget())
        Items.UseItem(hatchet)
        Target.WaitForTarget(15000)
        Target.TargetExecute(logs)
        Misc.Pause(700)
        
    