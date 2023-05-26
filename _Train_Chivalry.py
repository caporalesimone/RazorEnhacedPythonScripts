while True:
    #Spells.CastChivalry("Holy light")
    Spells.CastChivalry("Noble Sacrifice")
    Misc.Pause(800)
    if Player.Mana <= 19:
        Player.HeadMessage(33, "Ohmmm")
        Misc.Pause(500)
        Player.UseSkill("Meditation")
        while Player.Mana < Player.ManaMax:
            Misc.Pause(500)
    else:
        Misc.Pause(800)