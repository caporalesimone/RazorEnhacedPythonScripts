lootList = [
            0x0EED, # Gold

            #0x0F7A, # Black Pearl
            #0x0F7B, # Blood Moss            
            #0x0F84, # Garlic
            #0x0F85, # Ginseng
            #0x0F86, # Mandrake Root
            #0x0F88, # NightShade
            #0x0F8C, # Sulfurous Ash
            #0x0F8D, # Spiders' Silk
            
            #0x0F78, # Batwing
            #0x0F7D, # Daemon Blood
            #0x0F7E, # Bone
            #0x0F8A, # Pig Iron
            #0x0F8E, # Nox Crystal
            #0x0F8F, # Grave Dust
            
            0x0F10, # Emerald
            0x0F13, # Ruby
            0x0F15, # Citrine
            0x0F16, # Amethyst
            0x0F11, 0x0F19, # Sapphire
            0x0F0F, 0x0F21, # Star sapphire
            0x0F25, # Amber
            0x0F26, # Diamond
            0x0F18, 0x0F2D, # Tourmaline
           ]

###########################################           
            
lootBagSerial = 0x41670969

chestSerial = Target.PromptTarget("Target Chest")
if chestSerial > 0:
    chestItem = Items.FindBySerial(chestSerial)
    Items.UseItem(chestSerial)
    Misc.Pause(1000)

    for loot in chestItem.Contains:
        if loot.ItemID in lootList:
            Player.HeadMessage(33, "Looting: " + loot.Name)
            Items.Move(loot.Serial, lootBagSerial, 0)
            Misc.Pause(800)
