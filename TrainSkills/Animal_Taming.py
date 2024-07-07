
def RenamePet(animal):
    Misc.PetRename(animal, "Pasquale")

def ReleasePet(animal):
    Misc.WaitForContext(animal,1000,False)
    Misc.Pause(1000)
    Misc.UseContextMenu(animal,"release",1000)
    while not Gumps.HasGump():
        Misc.Pause(10)
    gump = Gumps.CurrentGump()
    Misc.Pause(1000)
    Gumps.SendAction(gump, 2) # Select Animals
    Misc.Pause(500)
    Mobiles.Message(animal, 33, "Bye Bye my friend!")
    #Player.ChatSay("All kill")
    #Target.WaitForTarget(1000,True)
    #Target.TargetExecute(animal)
    

def Tame(animal):
    while True:
        Journal.Clear()
        CUO.FollowMobile(animal)
        Mobiles.Message(animal, 33, "It's me")
        Player.UseSkill("Animal Taming")
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(animal)
        
        safeExit = 13
        while safeExit > 0:
            safeExit = safeExit - 1
            Misc.Pause(1000)
            if Journal.Search("It seems to accept you"):
                Player.HeadMessage(33, "Tame done, bye bye pet")
                RenamePet(animal)
                #ReleasePet(animal)
                CUO.FollowOff()
                return
            if Journal.Search("You have no chance of taming"):
                Player.HeadMessage(33, "Unable to tame it")
                return
            if Journal.Search("You fail to tame the creature"):
                break
            

target = Target.PromptTarget("Target an animal")
Tame(target)
            