tgt = Target.PromptTarget("Select NPG")
while True:
    Player.UseSkill("Eval Int")
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(tgt)
    Misc.Pause(1000)