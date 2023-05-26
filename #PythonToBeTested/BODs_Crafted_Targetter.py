itemid = 0x13EE
color = 0


found = Items.FindByID(itemid, color, Player.Backpack.Serial, False)
while True:
    if found is not None:
        Target.TargetExecute(found)
    Misc.Pause(300)
    found = Items.FindByID(itemid, color, Player.Backpack.Serial, False)
    Misc.Pause(300)
