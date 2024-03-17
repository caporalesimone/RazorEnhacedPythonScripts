pause = 10 # N * 1 second

while True:
    Player.UseSkill("Detect Hidden")
    Target.WaitForTarget(10000, False)
    Target.TargetExecuteRelative(Player.Serial, 1)
    for x in reversed(range(pause)):
        Player.HeadMessage(22,x)
        Misc.Pause(1000)
        
