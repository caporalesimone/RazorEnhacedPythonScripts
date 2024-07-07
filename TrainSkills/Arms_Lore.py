target = Target.PromptTarget("Target a weapon",20)

while True:
    Player.UseSkill("Arms Lore")
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(target)
    Misc.Pause(1000)
    if Player.GetSkillValue("Arms Lore") >= 100:
        break

