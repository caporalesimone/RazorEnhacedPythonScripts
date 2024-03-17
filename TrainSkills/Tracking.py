
while True:
    Player.UseSkill("Tracking")
    Gumps.WaitForGump(4069740721, 10000)
    Gumps.SendAction(4069740721, 1)
    Gumps.WaitForGump(155295600, 10000)
    Gumps.SendAction(155295600, 1)
    Misc.Pause(10000)