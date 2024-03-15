pause = 1 # N * 1 second
target = Target.PromptTarget("Target an item",20)

while True:
    Player.UseSkill("Item ID")
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(target)
    for x in reversed(range(pause)):
        #Player.HeadMessage(20, x)
        Misc.Pause(1000)
        
        
        

