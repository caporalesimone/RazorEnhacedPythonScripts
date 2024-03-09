pause = 11 # 11 * 1 second

while True:
    Player.UseSkill("Hiding")
    for x in reversed(range(pause)):
        Player.HeadMessage(20, x)
        Misc.Pause(1000)
