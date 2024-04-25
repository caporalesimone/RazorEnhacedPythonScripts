def update_status_bar():

    rb = 25 * "█"
    hp = int(Player.Hits/Player.HitsMax * 25) * "█"
    mp = int(Player.Mana/Player.ManaMax * 25) * "█"
    sp = int(Player.Stam/Player.StamMax * 25) * "█"

    gd = Gumps.CreateGump()
    Gumps.AddPage(gd, 0)
    Gumps.AddBackground(gd, 0, 0, 545, 78, 1755)

    Gumps.AddLabel(gd, 12, 10, 54,"H:")
    Gumps.AddLabel(gd, 10, 30, 54,"M:")
    Gumps.AddLabel(gd, 12, 50, 54,"S:")

    Gumps.AddLabel(gd, 30, 10, 37, rb)
    Gumps.AddLabel(gd, 30, 30, 37, rb)
    Gumps.AddLabel(gd, 30, 50, 37, rb)

    if Player.Poisoned:     hp_hue = 72
    elif Player.YellowHits: hp_hue = 53
    else:                   hp_hue = 97

    Gumps.AddLabel(gd, 30, 10, hp_hue, hp)
    Gumps.AddLabel(gd, 30, 30, 97, mp)
    Gumps.AddLabel(gd, 30, 50, 97, sp)

    Gumps.AddLabel(gd, 460, 10, 54, str(Player.Hits))
    Gumps.AddLabel(gd, 460, 30, 54, str(Player.Mana))
    Gumps.AddLabel(gd, 460, 50, 54, str(Player.Stam))

    Gumps.AddLabel(gd, 490, 10, 54, "/")
    Gumps.AddLabel(gd, 490, 30, 54, "/")
    Gumps.AddLabel(gd, 490, 50, 54, "/")

    Gumps.AddLabel(gd, 510, 10, 54, str(Player.HitsMax))
    Gumps.AddLabel(gd, 510, 30, 54, str(Player.ManaMax))
    Gumps.AddLabel(gd, 510, 50, 54, str(Player.StamMax))

    Gumps.CloseGump(123456)
    Gumps.SendGump(123456, Player.Serial, 120, 120, gd.gumpDefinition, gd.gumpStrings)

def position_status_bar():
    update_status_bar()
    Player.HeadMessage(68, "You have 5 seconds")
    Player.HeadMessage(68, "to move the status")
    Player.HeadMessage(68, "bar to final position")
    Misc.Pause(5000)

def main():

    position_status_bar()

    while True:

        update_status_bar()
        Misc.Pause(50)

main()