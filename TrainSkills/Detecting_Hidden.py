pause = 10 # N * 1 second

while True:
    Player.UseSkill("Detect Hidden")
    Target.WaitForTarget(10000, False)
    Target.TargetExecute(Player.Position.X+1,Player.Position.Y+1,Player.Position.Z)
    for x in reversed(range(pause)):
        Player.HeadMessage(22,x)
        Misc.Pause(1000)
        
