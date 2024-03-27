skill = Player.GetSkillValue("lockpicking")
Player.HeadMessage(33, "Lockpicking: {:.1f}".format(skill))
box = Target.PromptTarget("Select box")
Misc.Pause(500)
count = 0
while True:
    if (count == 0):
        count = 30
        Items.UseItem(box)
        Misc.Pause(800)
    count = count - 1
    lockpick = Items.FindByID(0x14FC, -1, Player.Backpack.Serial)
    Items.UseItem(lockpick)
    Target.WaitForTarget(2000)
    Target.TargetExecute(box)
    Misc.Pause(150)
    new_skill = Player.GetSkillValue("lockpicking")
    if (new_skill > skill):
        skill = new_skill
        Player.HeadMessage(33, "Lockpicking: {:.1f}".format(skill))
        if (skill >= 100):
            break

