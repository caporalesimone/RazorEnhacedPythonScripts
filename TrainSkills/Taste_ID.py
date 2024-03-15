pause = 1 # N * 1 second
target = Target.PromptTarget("Target a food",20)

while True:
    Player.UseSkill("Taste ID")
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(target)
    for x in reversed(range(pause)):
        Misc.Pause(1000)
