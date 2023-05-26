from System.Collections.Generic import List

MAXRUNE = 5
START_FROM_RUNE = 1
MAXRADIUS = 35
REST_DURATION_SECONDS = 150

runebookSerial = 0x414D517D
containerSerial = 0x417BE7A9

PLANTS = [
            0x0C51, 0x0C52, 0x0C53, 0x0C54, # Cotton
            0x1A99, 0x1A9A, 0x1A9B, # Flax
            # Veggies
            0x0C62, 0x0C63, # Turnip
            # 0x0C5E,0x0C5F,  # Vines but this plant does not change graphics so this script remains blocked
            0x0C6F,         # Onions
            0x0C76,         # Carrots
            
            # 0x0C56, 0x0C57, 0x0C58, # Wheat
         ]
RESOURCES = [
            0x0DF9, # Bale of cotton
            0x1A9C, 0x1A9D, # Flax bundle
            # Veggies
            0x0D39, 0x0D3A, # Turnip
            0x0C6B,         # Pumpkin from vines
            0x0C6D, 0x0C6E, # Onion
            0x0C77, 0x0C78, # Carrots
            # Wheat
            0x1EBD, 
            ]

            
###########################################################
            

def findBale():
    baleFilter = Items.Filter()
    baleFilter.Enabled = True
    baleFilter.RangeMax = 2
    baleFilter.OnGround = True
    baleFilter.Graphics = List[int] (RESOURCES)  # Items to gather. Eg. Cotton, Linen 
    plants = Items.ApplyFilter(baleFilter)
    if plants != None or len(plants) > 0:
        return plants
    return None

    
def findPlants(range):
    platsFilter = Items.Filter()
    platsFilter.Enabled = True
    platsFilter.RangeMax = range
    platsFilter.Graphics = List[int](PLANTS)  # Plants from gather
    seenPlants = Items.ApplyFilter(platsFilter)
    if seenPlants != None or len(seenPlants) > 0:
        return seenPlants
    return None    

    
def gather(plant):
    Player.HeadMessage(33, "Esamino la pianta")
    Items.UseItem(plant)
    Misc.Pause(500)
    bales = findBale()
    if bales != None:
        Player.HeadMessage(33, "Raccolgo")
        for bale in bales:
            Misc.Pause(500)
            Items.Move(bale, Player.Backpack, 4) #Should be -1?

    Misc.Pause(500)
        

def areStillFar(player, plant):
    
    distX = abs(player.X - plant.X)
    distY = abs(player.Y - plant.Y)
    distZ = abs(player.Z - plant.Z)
    
    #Misc.SendMessage('{} - {} - {}'.format(distX, distY, distZ))
    
    if (distX > 1): return True
    if (distY > 1): return True
    if (distZ > 1): return True
    
    return False
        
    
def movetoplant(plant):
    if plant != None:
        if Player.Position == plant.Position: # This happen if 2 plants are in the same tile (Server bug?)
            return
        
        Player.PathFindTo(plant.Position.X, plant.Position.Y, plant.Position.Z)
        
        maxsafeexit = 200
        safeexit = 0
        
        while areStillFar(Player.Position, plant.Position) and safeexit < maxsafeexit:
            safeexit += 1
            Misc.Pause(50)
            
        if safeexit >= maxsafeexit:
            Misc.SendMessage("Safe exit on movetoplant")

            
#First rune = 0    
def recall(runebookSerial, runenum):
    Items.UseItem(runebookSerial)
    Gumps.WaitForGump(0, 20000)
    gump = Gumps.CurrentGump()
    Misc.Pause( 50 )
    Gumps.SendAction( gump, 5 + runenum * 6 )
    Misc.Pause(3500)

    
def unloadresources(containerSerial):
    Player.HeadMessage(33, "Dumping resources")
    for resource in RESOURCES:
        item = Items.FindByID(resource, 0, Player.Backpack.Serial)
        if item != None:
            Items.Move(item,containerSerial,item.Amount)
            Misc.Pause(500)
    Misc.Pause(1000)

    
def gobackhome(runebookSerial, containerSerial, waitnextturn = False):
    recall(runebookSerial, 0)
    unloadresources(containerSerial)
    if Player.Mana < 20:
        while Player.Mana < Player.ManaMax:
            Misc.Pause(1000)
    if waitnextturn:
        Player.HeadMessage(33, "I take a rest")
        for i in reversed(range(REST_DURATION_SECONDS)):
            Player.HeadMessage(33, str(i))
            Misc.Pause(1000)
            
#############################################################################    

radius = 1
rune = START_FROM_RUNE # La runa 0 è casa
recall(runebookSerial, rune)
while True:
        
    if Player.Weight > Player.MaxWeight - 20:
        gobackhome(runebookSerial, containerSerial)
        recall(runebookSerial, rune)
        radius = 1
        
    if Player.Mana < 20:
        gobackhome(runebookSerial, containerSerial)
        recall(runebookSerial, rune)
        radius = 1
    
    Player.HeadMessage(33, "Radius: " + str(radius))
    if radius >= MAXRADIUS:
        radius = 1
        rune = rune + 1
        if rune > MAXRUNE:
            gobackhome(runebookSerial, containerSerial, waitnextturn = True)
            rune = 1
        recall(runebookSerial, rune)
        
    plants = findPlants(radius)
    if plants != None and len(plants) > 0:
        for plant in plants:
            movetoplant(plant)
            gather(plant)
            break   # I run the radius check again for be sure to find the closest
        radius = 1
    else:
        radius = radius + 1
    
    Misc.Pause(10)

    
