# Trains Necromancy to GM
# Wearing a good suit will greatly improve training.  
# The most important property will be 100% Lower Reagent Cost forgo using reagents. 
# Other desirable properties include: 40% Lower Mana Cost, 2 Faster Casting, 6 Faster Cast Recovery, and as much Mana Regeneration as possible.
# 
# 
# ------------------------------------
self = Player.Serial
#Necro Reag
Batwing = 0x0F78
DaemonBlood = 0x0F7D
PigIron = 0x0F8A
GraveDust = 0x0F8F
NoxCrystal = 0x0F8E



def trainNecromancy():
    #Healing 
    while Player.Hits < 45:
        Misc.Pause(100)
    
    if Player.GetRealSkillValue('Necromancy') < 35:
        Misc.SendMessage('Go buy Necro skill!!')
        Stop
    elif Player.GetRealSkillValue('Necromancy') < 50:
        Spells.CastNecro('Pain Spike')
        Target.WaitForTarget(2500)
        Target.TargetExecute(self)
        Misc.Pause(2000)
    elif Player.GetRealSkillValue('Necromancy') < 70:
        Spells.CastNecro('Horrific Beast')
        Misc.Pause(4000)
    elif Player.GetRealSkillValue('Necromancy') < 85:# 90 On UOGuide.com
        Spells.CastNecro("Wither")
        Misc.Pause(4000)
    elif Player.GetRealSkillValue('Necromancy') < 100:
        Spells.CastNecro("Lich Form")
        Misc.Pause(400)
    elif Player.GetRealSkillValue('Necromancy') < 120:
        Spells.CastNecro("Vampiric Embrace")
        Misc.Pause(4000)
    #Meditating
    if Player.Mana < 40:
        Player.UseSkill('Meditation')
        while Player.Mana < Player.ManaMax:
            if (not Player.BuffsExist('Meditation') and not Timer.Check('skillTimer')):
                Player.UseSkill('Meditation')
                Timer.Create('skilltimer', 11000)
            Misc.Pause(100)
            
#Main Loop
Journal.Clear()
while Player.GetRealSkillValue('Necromancy')  < 100:
    trainNecromancy()
    
Player.ChatSay(33, 'GM Necromancy')