pet = Target.PromptTarget("Target an animal",33)
while True:
    Player.UseSkill("Animal Lore")
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(pet)
    while not Gumps.HasGump():
        Misc.Pause(1)
    gump = Gumps.CurrentGump()
    Gumps.SendAction(gump, 0)
    Misc.Pause(50)