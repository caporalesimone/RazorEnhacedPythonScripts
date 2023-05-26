from System.Collections.Generic import List

#serial = 0x414172CA
serial = 0x408DD7C7

stop = False

while not stop:
    Journal.Clear()
    Spells.Cast("Gate Travel")
    Target.WaitForTarget(2000)
    Target.TargetExecute(serial)
    Misc.Pause(500)
    
    if Journal.Search("The spell fizzles"):
        Player.HeadMessage(33, "Damn!")
    else:
        Player.ChatSay(33,"All come")
        #Misc.Pause(100)
        filter = Items.Filter()
        filter.Enabled = True
        filter.RangeMax = 2
        filter.Graphics = List[int]([0x0F6C])

        gate = Items.ApplyFilter( filter )
        Items.UseItem(gate[0])
        stop = True
        
    Misc.Pause(2000)