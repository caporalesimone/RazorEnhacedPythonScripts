target = Target.PromptTarget("target something")
while True:
    Player.UseSkill("Forensics")
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(target)
    Misc.Pause(1000)