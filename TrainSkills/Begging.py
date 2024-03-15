pause = 13 # 11 * 1 second
target = Target.PromptTarget("Target a NPC",20)


while True:
    Player.UseSkill("Begging")
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(target)
    for x in reversed(range(pause)):
        Player.HeadMessage(20, x)
        Misc.Pause(1000)


