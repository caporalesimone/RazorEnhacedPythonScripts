# https://www.uoguide.com/Spellweaving#Training

immolate_weapon_serial = 0x41969F29

while True:
    
    if Player.GetSkillValue("spellweaving") < 25:
        Spells.CastSpellweaving("Arcane Circle")
        Player.HeadMessage(33, "Arcane Circle")
        Misc.Pause(2000)
        if Player.Mana < 22:
            while Player.Mana < Player.ManaMax:
                Player.HeadMessage(33, "Ohmmmm")
                Misc.Pause(5000)
    elif Player.GetSkillValue("spellweaving") < 40:
        Spells.CastSpellweaving("Immolate Weapon")
        Player.HeadMessage(33, "Immolate Weapon")
        Target.WaitForTarget(5000)
        Target.TargetExecute(immolate_weapon_serial)
        Misc.Pause(2000)
        if Player.Mana < 30:
            while Player.Mana < Player.ManaMax:
                Player.HeadMessage(33, "Ohmmmm")
                Misc.Pause(5000)
    elif Player.GetSkillValue("spellweaving") < 58:
        Spells.CastSpellweaving("Reaper Form")
        Player.HeadMessage(33, "Reaper Form")
        Misc.Pause(4000)
        if Player.Mana < 31:
            while Player.Mana < Player.ManaMax:
                Player.HeadMessage(33, "Ohmmmm")
                Misc.Pause(5000)
    elif Player.GetSkillValue("spellweaving") < 80:
        Spells.CastSpellweaving("Essence of wind")
        Player.HeadMessage(33, "Essence of wind")
        Misc.Pause(4000)
        if Player.Mana < 37:
            while Player.Mana < Player.ManaMax:
                Player.HeadMessage(33, "Ohmmmm")
                Misc.Pause(5000)        
    elif Player.GetSkillValue("spellweaving") < 100:
        Spells.CastSpellweaving("Wildfire")
        Player.HeadMessage(33, "Wildfire")
        Target.WaitForTarget(5000)
        Target.TargetExecute(Player.Serial)
        Misc.Pause(4000)
        if Player.Mana < 37:
            while Player.Mana < Player.ManaMax:
                Player.HeadMessage(33, "Ohmmmm")
                Misc.Pause(5000)                    
                
    Misc.Pause(100)
            
        
        