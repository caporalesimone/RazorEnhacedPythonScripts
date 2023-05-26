

while(True):
    if (Player.GetSkillValue("Healing") >= 100):
        Player.HeadMessage(33,"Head done")
        break

    Misc.SendMessage("Wait for damage")
    healed = Mobiles.FindBySerial(0x4500D)      
    while (healed.Hits == healed.HitsMax):
        Misc.Pause(100)
    
    Misc.SendMessage("Healing")
    serial = Items.FindByID(0x0E21, -1, Player.Backpack.Serial)
    Items.UseItem(serial)
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(0x4500D)
    Misc.Pause(6500)