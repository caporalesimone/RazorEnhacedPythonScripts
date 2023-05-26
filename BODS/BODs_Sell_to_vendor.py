import math

PLAYER_HEAD_COLOR_MSG = 55
DEF_BUTTON_ID_RUNEBOOK = 31  # Banca Delucia Sacred Journey
DEF_GUMP_ID_NEW_BOD = 2611865322

def distance(x1, y1, x2, y2):
    return math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )


def moveToVendor(vendor):
    if vendor != None:
        if Player.Position == vendor.Position:
            return
        while distance(Player.Position.X, Player.Position.Y, vendor.Position.X, vendor.Position.Y) > 1:
            Player.PathFindTo(vendor.Position.X, vendor.Position.Y, vendor.Position.Z)
            Misc.Pause(1000)
            

        
def requestBod(tailor, bookSerial):
    Misc.WaitForContext(tailor.Serial, 15000)
    Misc.ContextReply(tailor.Serial, 1)
    Gumps.WaitForGump(DEF_GUMP_ID_NEW_BOD, 15000)
    Gumps.SendAction(DEF_GUMP_ID_NEW_BOD, 1)
    Misc.Pause(1000)
    bod = Items.FindByID(0x2258, 0x0483, Player.Backpack.Serial, False)  # Green BOD
    Items.Move(bod.Serial, bookSerial, 1)
    Gumps.WaitForGump(0, 20000)
    gump = Gumps.CurrentGump()
    Gumps.CloseGump(gump)
    Misc.Pause(500)

    
def giveBod(tailor, filledBodsSerial):
    # Get bod out from filled book
    Items.UseItem(filledBodsSerial)
    Misc.Pause(500)
    Gumps.WaitForGump(0, 20000)
    gump = Gumps.CurrentGump()
    Gumps.SendAction(gump, 5)
    Gumps.WaitForGump(gump, 3000)
    Gumps.CloseGump(gump)
    Misc.Pause(500)
    # Give bod to vendor
    bod = Items.FindByID(0x2258, 0x0483, Player.Backpack.Serial, False)  # Green BOD
    Items.Move(bod.Serial, tailor.Serial, 0)
    Misc.Pause(1000)    
    return True

######################################################################

homeRuneBookSerial = 0x4688A53D      

bookNewBodsSerial = Target.PromptTarget("Book of EMPTY BODs")
filledBodsSerial = Target.PromptTarget("Book of FILLED BODs")
        
tailorSerial = 0x0007FFAA #  Delucia Armstrong The Tailor
tailor = Mobiles.FindBySerial(tailorSerial)

Player.HeadMessage(PLAYER_HEAD_COLOR_MSG, "Hello, " + tailor.Name)
Player.HeadMessage(PLAYER_HEAD_COLOR_MSG, "I have something for you.")


while True:
    
    if Player.Weight > Player.MaxWeight - 50:
        Player.HeadMessage(PLAYER_HEAD_COLOR_MSG, "Too Heavy")
        Items.UseItem(homeRuneBookSerial)
        Gumps.WaitForGump(0, 10000)
        Gumps.SendAction(Gumps.CurrentGump(), DEF_BUTTON_ID_RUNEBOOK) # ButtonID of rune for home
        break
    
    moveToVendor(tailor)
    gaveBod = giveBod(tailor, filledBodsSerial)
    if gaveBod == False:
        Player.HeadMessage(PLAYER_HEAD_COLOR_MSG, "Book of filled bod is empty")
        break
        
    requestBod(tailor, bookNewBodsSerial)
    Player.HeadMessage(PLAYER_HEAD_COLOR_MSG, "Waiting for vendor to be ready")
    Misc.Pause(6000)
    
    
    
    
    

