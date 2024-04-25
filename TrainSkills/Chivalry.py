#0 - 15  Close Wounds
#15 - 25 Consacrate Weapon
#25 - 35 Divine Fury
#35 - 45 Dispel Evil
#45 - 55 Enemy of One
#55 - 120    Holy Light

while True:
    if Player.Mana < 15:
        Misc.Pause(10000)
    
    skill = Player.GetRealSkillValue("Chivalry")
    if skill >= 100:
        Player.HeadMessage(33, "Done!")
        break
    if skill > 35 and skill <= 45:
        Spells.CastChivalry("Dispel Evil")
        Misc.Pause(3000)
    if skill > 45  and skill <= 55:
        Spells.CastChivalry("Enemy Of One")
        Misc.Pause(3000)
    if skill > 55:
        Spells.CastChivalry("Holy Light")
        Misc.Pause(3000)