target = Target.PromptTarget("Target a mobile")

while True:
    Player.UseSkill("Anatomy")
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(target)
    Misc.Pause(1000)