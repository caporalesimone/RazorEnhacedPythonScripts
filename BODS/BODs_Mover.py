toEmpty = Target.PromptTarget('BOD to be emptied')
toFill = Target.PromptTarget('BOD to be filled')

if toEmpty == 0 or toFill == 0:
    Crash()

while True:
    Journal.Clear()
    Items.UseItem(toEmpty)
    for i in range(10):
        Gumps.WaitForGump(0,1000)
        if Journal.Search("The book is empty"):
            break
        gump = Gumps.CurrentGump()
        Gumps.SendAction(gump, 5)
        Gumps.WaitForGump(gump,1000)
        Misc.Pause(10)
        

    Gumps.CloseGump(gump)
    Misc.Pause(500)
    bod = None
    while True:
        bod = Items.FindByID(0x2258, -1, Player.Backpack.Serial, False)
        if bod is None:
            break
        Items.Move(bod.Serial, toFill, 1)
        Gumps.WaitForGump(0,15000)
        gump = Gumps.CurrentGump()
        Gumps.CloseGump(gump)
        Misc.Pause(400)
    Misc.Pause(5)
