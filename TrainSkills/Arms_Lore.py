pause = 1 # N * 1 second
target = Target.PromptTarget("Target a weapon",20)

while True:
    Player.UseSkill("Arms Lore")
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(target)
    for x in reversed(range(pause)):
        #Player.HeadMessage(20, x)
        Misc.Pause(1000)

