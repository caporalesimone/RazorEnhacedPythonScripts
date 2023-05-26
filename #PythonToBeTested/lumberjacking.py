import time
import math
import sys
#
if not Misc.CurrentScriptDirectory() in sys.path:
    sys.path.append(Misc.CurrentScriptDirectory())
#
import System
import common
common.Gumps = Gumps
common.Items = Items
common.Player = Player
common.Mobiles = Mobiles
#
Current_Map = Player.Map  # Note Faraan and Felucca seem the same
#
square_size=8
eightByEightX = Player.Position.X / square_size
eightByEightY = Player.Position.Y / square_size
areaToClear_X = 6
areaToClear_Y = 37
x_direction = 1
y_direction = 1
#    
from System.Collections.Generic import List
from System import Byte, Int32
#
import clr
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer
#
Lumberjacking_Data_File = "Data/lumberjacking_data.txt"
wood_data_file = open(Lumberjacking_Data_File, "r")
wood_data_json = wood_data_file.read()
locations = JavaScriptSerializer().Deserialize(wood_data_json, list)
wood_data_file.close()

Using_Garg = False
Garg_axe = Items.FindByID(0x0F45, 0x076c, Player.Backpack.Serial)
wood_locations = set()
for loc in locations:
    wood_locations.add( (loc[0], loc[1], loc[2], loc[3]) )

#
def check_wood_locations(x, y):
    global wood_locations    
    for loc in wood_locations:
        if Current_Map == loc[0] and x == loc[1] and y == loc[2]:
            return loc[3]
    return None        
#
def update_wood_locations(x, y, color):
    global wood_locations
    # dont add locations that are already being mined with Garg pick
    global Using_Garg
    if Using_Garg:
        Misc.SendMessage("USING GARG")
        return
    if color.lower() == "regular":
        return    
    locationData = check_wood_locations(x, y)
    if locationData == None or locationData == "regular": 
        wood_locations.add( (Current_Map, x, y, color) )
        Misc.SendMessage("ADDED LOCATION for {}".format(color))
        wood_data_file = open(Lumberjacking_Data_File, "w")
        wood_data_file.write(JavaScriptSerializer().Serialize(wood_locations))
        wood_data_file.close()
#
# 
Garg_Wood_Types = [ 
                 ]
import re
def check_use_garg(x, y):
    global Using_Garg 
    update = False
    journalEntry = None
    if Journal.Search("You put some"):
        journalEntry = Journal.GetLineText("You put some", False)
        groups = re. search('some\s+(.+)\slogs', journalEntry)       
        if groups:               
            update_wood_locations(x, y, groups.group(1))
        else:
            Misc.SendMessage("NO GROUPS!")    
    #
    wood_color = check_wood_locations(x, y)
    if wood_color in Garg_Wood_Types:
        Using_Garg = True
        Player.HeadMessage(9, "Use Garg to upgrade {}".format(wood_color))
        return True
    Using_Garg = False
    return False                
#                                   
#
def FindPackhorse():
    pack_horse = 0
    findPack = Mobiles.Filter()
    findPack.Enabled = True
    findPack.RangeMax = 2
    findPack.Bodies = List[int]((0x0123, 0x0319))
    listPack = Mobiles.ApplyFilter(findPack)
    if len(listPack) > 0:
        for i in listPack:
            pack_horse = listPack[0]
            Misc.SendMessage("Pack is 0x{:x}".format(pack_horse.Serial))
    else:
        Misc.SendMessage("NO PACK HORSE")
        pack_horse = Mobiles.FindBySerial(0x00B0C1E5)
    return pack_horse

PackHorse = FindPackhorse()    
#
def DepositItems():
    BankStorage = 0x4B23F910
    pack_horse = FindPackhorse()
    Mobiles.UseMobile(pack_horse)
    Mobiles.WaitForProps(pack_horse, 10000)
    Misc.Pause(1000)
    Player.ChatSay(52, "bank")
    Misc.Pause(500)
    moveItemList = [0x1BD7, 0x3191, 0x3190, 0x2F5F,  0x318F]
    for item in Player.Backpack.Contains:
        if item.ItemID in moveItemList:
            Items.Move(item, BankStorage, 0)
            Misc.Pause(1000)         
    Mobiles.UseMobile(pack_horse)     
    for pack in pack_horse.Contains:
        Misc.SendMessage("test")
        for item in pack.Contains:
            Misc.SendMessage(str(item))
            Items.Move(item, BankStorage, 0)
            Misc.Pause(1000) 
#
def CheckAndRun():
    # figure this out later
    return
    enemy_filter = Mobiles.Filter()
    enemy_filter.Enabled = True
    enemy_filter.RangeMin = -1
    enemy_filter.RangeMax = 10
    enemy_filter.Notorieties = List[Byte](bytes([4,5,6]))
    enemies = Mobiles.ApplyFilter(enemy_filter)
    
    #if len(enemies) > 0:
        #Spells.CastMagery("Mark")
        #Target.WaitForTarget(2000, True)
        #Target.TargetExecute(SavePlaceRune)
        #Misc.Pause(3000)
        #Spells.CastMagery("Recall")
        #Target.WaitForTarget(2000, True)
        #Target.TargetExecute(StoreWoodRune)
        #sys.exit(0)
        
#

#
def RangeTree( tree ):
    dist = math.sqrt( ((Player.Position.X - tree.X)**2) + ((Player.Position.Y - tree.Y)**2) )
    return dist
#
def NearestCalc(itemList):
    if len(itemList) == 0:
        return None
    min_distance_item = None
    min_distance = 99999
    for i in itemList:
        dist = RangeTree(i)
        #Misc.SendMessage("dist: {}, {} item: 0x{:x}".format(dist, Player.DistanceTo(i), i.Serial), 5)        
        if dist < min_distance:
            min_distance = dist
            min_distance_item = i            
        #Misc.SendMessage("FINAL dist: {} item: 0x{:x}".format(min_distance, min_distance_item.Serial), 5)
    return min_distance_item
#
def FindAxe():
    axe = Items.FindByID(common.hatchetID, 0, Player.Backpack.Serial)
    # if one in pack use it
    if axe:
        return axe
    # Make 2 as long as we are making    
    while Items.BackpackCount(common.hatchetID, 0) < 2:             
        if Items.BackpackCount(common.tinker_kitsID, 0) < 2:
            common.MakeTinkerKits()        
            Misc.Pause(1000)
            if Items.BackpackCount(common.tinker_kitsID, 0) < 2:
                Misc.SendMessage("Could not make tinker kits")
                return        
        common.MakeHatchet()
        Misc.Pause(1000)
    axe = Items.FindByID(common.hatchetID, 0, Player.Backpack.Serial)        
    return axe

WalkToBank = False 
SavePlaceRune = 0x422331D2          
StoreWoodRune = 0x4129A2A8
def StoreWood():
    if WalkToBank:
        save_position = Player.Position
        Player.PathFindTo(2873, 3482, 0)
        DepositItems()
        Player.PathFindTo(save_position.X, save_position.Y, save_position.Z)
        return
    Spells.CastMagery("Mark")
    Target.WaitForTarget(2000, True)
    Target.TargetExecute(SavePlaceRune)
    Misc.Pause(3000)
    Spells.CastMagery("Recall")
    Target.WaitForTarget(2000, True)
    Target.TargetExecute(StoreWoodRune)
    Misc.Pause(3000)
    DepositItems()
    Misc.Pause(1000)
    Spells.CastMagery("Recall")
    Target.WaitForTarget(2000, True)
    Target.TargetExecute(SavePlaceRune)
    Misc.Pause(1000)
#
TreeStaticID = [ 0xc95, 0xc96, 0xc99, 0xc9b, 0xc9c, 0xc9D, 0xc8a, 0xca6, 0xca8, 
0xcaa, 0xcab, 0xcc3, 0xcc4, 0xcc8, 0xcc9, 0xcca, 0xccb, 0xccc, 0xccd, 0xcd3, 0xcd1, 0xcd0, 0xcd6, 0xcd8, 
0xcda, 0xcdd, 0xce0, 0xce3, 0xce6, 0xcf8, 0xcf8, 0xcfe, 0xd01, 0xd25, 0xd27, 0xd35, 0xd37, 0xd38, 
0xd42, 0xd43, 0xd59, 0xd70, 0xd85, 0xd94, 0xd96, 0xd98, 0xd9a, 0xd9c, 0xd9e, 0xda0, 0xda2, 0xda04, 
0xda8, 0x0DAC, 0x0DAD ]
#
tileinfo = List[Statics.TileInfo]
#

class Tree:
    def __init__(self, x, y, z, id):
        self.X = x
        self.Y = y
        self.Z = z
        self.ID = id
        
def ScanStaticTrees(start_x, start_y): 
    Misc.SendMessage("--> Initiating Tile Scan", 77)
    trees = []
    #
    for y in range(start_y, start_y+8+1):
        for x in range(start_x, start_x+8+1):
            tileinfo = Statics.GetStaticsTileInfo(x, y, Player.Map)
            #Misc.SendMessage("X:{} Y:{} tilenum: {} map{}".format( 
            #x, y, tileinfo.Count, Player.Map))
            if tileinfo.Count > 0:
                for tile in tileinfo: 
                    if tile.StaticID in TreeStaticID:
                        #Misc.SendMessage('--> Tree X: %i - Y: %i - Z: %i' % (x, y, tile.StaticZ), 66)
                        tree = Tree(x, y, tile.StaticZ, tile.StaticID)
                        trees.append(tree)
   
    Misc.SendMessage('--> Total Trees: {}'.format(len(trees)), 77) 
    #for tree in trees:
        #Misc.SendMessage("Found tree at X:{} Y:{} Z:{} ID{}".format(tree.X, tree.Y, tree.Z, tree.ID))
    return trees

#
def CheckTreeFinished(tree):
    if Misc.CheckSharedValue("StaticTrees"):
        return Journal.Search("not enough wood here")
    else:    
        check_tree = Items.FindBySerial(tree.Serial)
        if check_tree == None:
            return True
        else:
            return False
#
def ConvertLogsToWood():
    axe = FindAxe()
    if not axe:
        Misc.SendMessage("Unable to Find suitable Axe")
        Stop()
    logID = 0x1BDD
    log = Items.FindByID(logID, -1, Player.Backpack.Serial) 
    prev_log = 0  
    max_tries = 10 
    while log != None:
        #Misc.SendMessage("{} 0x{:x} - 0x{:x}".format(wood.Name, prev_wood, wood.Serial), 5)
        prev_log = log.Serial
        Items.UseItem(axe)
        Target.WaitForTarget(5000, False)
        #Misc.SendMessage("0x{:x}".format(log.Serial), 5)
        Target.TargetExecute(log)
        Misc.Pause(1000)
        log = Items.FindByID(logID, -1, Player.Backpack.Serial)
        #
def StoreInKey(): 
    woodID = 0x1BD7
    allWood = common.findRecursive(Player.Backpack.Serial, [ woodID, 0x318F, 0x2F5F, 0x3190, 0x3191 ] ) 
    if len(allWood) <= 0:
        return
    keyID = 0x176B   
    allKeys = common.findRecursive(Player.Backpack.Serial, [ keyID ] ) 
    woodKey = None
    for key in allKeys:
        if key.Hue == 0x0058:
            woodKey = key
    if woodKey == None:
        Misc.SendMessage("No key for wood storage found")
        return
    woodKeyGumpID = 173511501
    Items.UseItem(woodKey)
    Gumps.WaitForGump(woodKeyGumpID, 2000)
    Gumps.SendAction(woodKeyGumpID, 60023)
    for wood in allWood:
        Target.WaitForTarget(2000, False)
        Target.TargetExecute(wood)
    # 
    Misc.Pause(1000)
    Gumps.WaitForGump(woodKeyGumpID, 2000)
    Gumps.SendAction(woodKeyGumpID, 0)    
    Gumps.CloseGump(woodKeyGumpID)
    Target.Cancel()
        
    #MoveWoodToBOH()    
#    
def MoveWoodToBOH():
    # Move to Packhorse or BagOfHolding       
    woodID = 0x1BD7
    wood = Items.FindByID(woodID, -1, Player.Backpack.Serial) 
    prev_wood = 0  
    max_tries = 10 
    while wood != None:
        #Misc.SendMessage("{} 0x{:x} - 0x{:x}".format(wood.Name, prev_wood, wood.Serial), 5)
        prev_wood = wood.Serial
        Items.Move(wood.Serial, Misc.ReadSharedValue("BagOfHolding"), 0)
        Misc.Pause(1000)
        test = Items.FindBySerial(wood.Serial)
        if test != None:
            Misc.SendMessage("TRYING TO MOVE WOOD", 6)
            #break
        wood = Items.FindByID(woodID, -1, Player.Backpack.Serial)
        max_tries = max_tries - 1
        if max_tries <= 0:
            break

#
def MoveWoodToPack():
    # Move to Packhorse
    if not PackHorse:
        return
    woodID = 0x1BD7
    wood = Items.FindByID(woodID, -1, Player.Backpack.Serial) 
    prev_wood = 0  
    max_tries = 10 
    while wood != None:
        #Misc.SendMessage("{} 0x{:x} - 0x{:x}".format(wood.Name, prev_wood, wood.Serial), 5)
        prev_wood = wood.Serial
        if Player.DistanceTo(PackHorse) > 1:
                Misc.Pause(2000)
        Items.Move(wood.Serial, PackHorse, 0)
        Misc.Pause(1000)
        test = Items.FindBySerial(wood.Serial)
        if test != None:
            Misc.SendMessage("UNABLE TO MOVE WOOD", 6)
            #break
        wood = Items.FindByID(woodID, -1, Player.Backpack.Serial)
        max_tries = max_tries - 1
        if max_tries <= 0:
            break
#           
if areaToClear_X < 0:
    x_direction = -1
if areaToClear_Y < 0:
    y_direction = -1
#
axe = Player.GetItemOnLayer('LeftHand')
if not axe:
    axe = FindAxe()
    if not axe:
        Misc.SendMessage("Unable to Find suitable Axe")
        stop()

for ebe_x in range(eightByEightX, eightByEightX+areaToClear_X, x_direction):
    for ebe_y in range(eightByEightY, eightByEightY+areaToClear_Y, y_direction):
        Misc.SendMessage("NEW 8x8 X: {} Y: {} Z: {}".format(ebe_x*square_size, ebe_y*square_size, 0))
        #Player.PathFindTo(ebe_x*square_size, ebe_y*square_size, 0)
        trees = ScanStaticTrees(ebe_x*square_size, ebe_y*square_size)
        while trees != None and len(trees) > 0:
            # In theory only 1 tree in this 8x8 will have logs
            tree = NearestCalc(trees)
            Dress.ChangeList("lj_regular")
            Dress.DressFStart()
            #Misc.SendMessage("TREE FOUND X:{} Y:{} Z:{}".format(tree.X, tree.Y, tree.Z))
            while (None != tree):
                ConvertLogsToWood()
                if False == Misc.CheckSharedValue("BagOfHolding"):
                    if PackHorse:
                        weight = Mobiles.GetPropValue(PackHorse, "Weight") 
                    else:
                        weight = 1400
                    if weight > 1400:
                        StoreWood()
                #Misc.SendMessage("tree at ( {}, {}, {}".format(tree.Position.X, tree.Position.Y, tree.Position.Z), 5)    
                #Player.PathFindTo(tree.X, tree.Y, tree.Z)
                if Misc.CheckSharedValue("UseKeys"):
                    StoreInKey()
                elif Misc.CheckSharedValue("BagOfHolding"):
                    MoveWoodToBOH()
                else:
                    MoveWoodToPack()
                wait_secs = 0
                #Player.PathFindTo(tree.X, tree.Y, tree.Z)
                route = PathFinding.Route()
                route.X = tree.X - 1
                route.Y = tree.Y - 1
                route.MaxRetry = 5
                PathFinding.Go(route)
                if RangeTree(tree) > 2:
                    Misc.Pause(1000)
                    wait_secs = wait_secs + 1
                    if wait_secs > 20:
                        Misc.SendMessage("SKIPPING Tree Location ( {}, {}, {})".format(tree.Position.X, tree.Position.Y, tree.Position.Z), 5)
                        continue
                wood_to_chop = True
                Journal.Clear()               
                while wood_to_chop:
                    useGargAxe = check_use_garg(tree.X, tree.Y)
                    CheckAndRun()
                    axe = FindAxe()
                    failed_chop_time = time.time() + 6
                    Misc.Pause(1000)
                    Target.Cancel
                    if Garg_axe and useGargAxe:
                        Items.UseItem(garg_axe)
                    else:    
                        Items.UseItem(axe)
                    Target.WaitForTarget(5000, False)
                    #Misc.SendMessage("0x{:x}".format(tree.Serial), 5)
                    #Misc.SendMessage("Chop Tree at X:{} Y:{} Z:{} Tile:{}".format(tree.X, tree.Y, tree.Z, tree.ID))
                    Target.TargetExecute(tree.X, tree.Y, tree.Z, tree.ID)
                    CheckAndRun()
                    Misc.Pause(2700)
                    if CheckTreeFinished(tree):
                        Misc.SendMessage("Stopping due to finished")
                        wood_to_chop = False
                    if Journal.Search("You put") or Journal.Search("You put"):
                        failed_chop_time = time.time() + 6
                    if Journal.Search("no more wood"):
                        Misc.SendMessage("Stopping due to Journal")
                        wood_to_chop = False
                    if Player.Weight > Player.MaxWeight * .95:
                        Misc.SendMessage("Stopping due to Player Weight")
                        wood_to_chop = False
                    if Journal.Search("Can't get there"):
                        Misc.SendMessage("Stopping due to Unreachable")
                        #all comeMisc.CheckIgnoreObject(tree)
                        wood_to_chop = False    
                    if Journal.Search("far away"):
                        Misc.SendMessage("Stopping due to Unreachable")
                        #Misc.IgnoreObject(tree)
                        wood_to_chop = False
                    if Journal.Search("lack the skill"):
                        Misc.SendMessage("Stopping due to lack of skill")
                        #Misc.IgnoreObject(tree)
                        wood_to_chop = False    
                    if Journal.Search("cannot be seen"):
                        Misc.SendMessage("Stopping due to lack of visibility")
                        #Misc.IgnoreObject(tree)
                        wood_to_chop = False  
                    if Journal.Search("can't use an axe"):
                        Misc.SendMessage("Stopping due to invalid target")
                        #Misc.IgnoreObject(tree)
                        wood_to_chop = False                     
                    if Journal.Search("You broke your axe"):
                        axe = FindAxe()
                        if axe:
                            failed_chop_time = time.time() + 6
                            wood_to_chop = True
                        else:
                            Misc.SendMessage("Cannot find a new axe")
                            wood_to_chop = False
                    if failed_chop_time <= time.time():
                        Misc.SendMessage("Stopping due to Time-out")
                        #Misc.IgnoreObject(tree)
                        wood_to_chop = False       
                #trees = FindTrees()
                trees.Remove(tree)
                #Misc.SendMessage(str(len(trees)), 5)
                tree = NearestCalc(trees)
                    
