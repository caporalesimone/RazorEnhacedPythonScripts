#Auto Rail Miner 
#based off a script by Crezdba, for mining part
#   -inspect your firebeetle, put its serial below under beetle =
#Have shovels or pickaxes in bag, once out it stops. 
#have a secure you can access, I used a metal chest, but anything should work.
#setup a rail and add the coordinates under railcoords=
#It will check to see if it can mine at each stop, and will look for your secure at each stop.
#so make sure you make a stop next to your secure.
#It currently will attempt to look W,N for ore spots. you can change this if you need to
#lines 108, 119 just change the direction.
#It should run the rail, when close to overweight will smelt all the ore in your pack
#When it gets to your secure, it will drop off all ingots.
#


import time
import sys
import math
#
if not Misc.CurrentScriptDirectory() in sys.path:
    sys.path.append(Misc.CurrentScriptDirectory())
#    
from System.Collections.Generic import List
from System import Byte, Int32
#
import clr
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer
#
railCoords =
Journal.Clear()
def gotoLocation(x1, y1):
    Coords = PathFinding.Route()
    Coords.X = x1
    Coords.Y = y1
    Coords.MaxRetry = 10
    PathFinding.Go(Coords)
    Misc.Pause(600)
    

beetle =             
shovelID = 0x0F39
pickaxeID = 0x0E86
waitForTarget = 5000
waitAfterMining = 2500
waitAfterPickAxe = 4000
pickaxe_spots = List[int] (( 0x136D, 0x1367, 0x136A)) 

def smelt():
    Mobiles.FindBySerial(beetle)
    Player.HeadMessage(3,"found")
    types = [0x19B9,0x19B8,0x19BA,0x19B7]
    
    for t in Items.FindBySerial(Player.Backpack.Serial).Contains:
        if t.ItemID in types:
            Items.UseItem(t)
            Target.WaitForTarget(1000,False)
            Target.TargetExecute(beetle)
            Misc.Pause(1000)
           

def getVeins():
    findVeins = Items.Filter()
    findVeins.Enabled = True
    findVeins.OnGround = 1
    findVeins.Movable = False
    findVeins.RangeMin = -1
    findVeins.RangeMax = 2
    findVeins.Graphics = pickaxe_spots
    findVeins.Hues = List[int]((  ))
    findVeins.CheckIgnoreObject = True
    listVeins = Items.ApplyFilter(findVeins)
    return listVeins


MotionMap = {
                        "North": (0, -1), 
                        "Right": (+1, -1),
                        "East": (+1, 0),
                        "Down": (+1, +1),
                        "South": (0, +1),
                        "Left": (-1, +1),
                        "West": (-1, 0),
                        "Up": (-1, -1),
                        "North": (0, -1), 
                        "Right": (+1, -1),
                        "East": (+1, 0),
                        "Down": (+1, +1),
                        "South": (0, +1),
                        "Left": (-1, +1),
                        "West": (-1, 0),
                        "Up": (-1, -1),
                        } 

CaveTiles = [ 0x0016, 0x0017, 0x0018, 0x0019, 0x245, 0x246, 0x247, 0x248, 0x249, 0x22b, 0x22c, 0x22d, 0x22e, 0x22f ]    
            
            
def MineSpot():
    x_delta, y_delta = MotionMap[Player.Direction]
    x = Player.Position.X + x_delta
    y = Player.Position.Y + y_delta
    xStart = Player.Position.X
    yStart = Player.Position.Y
    land_id = Statics.GetLandID(x, y, Player.Map)
    Misc.SendMessage("X: {} Y: {} LandID: 0x{:x} ImPassable: {}".format(x, y, land_id, Statics.GetLandFlag(land_id, "Impassable")))
    if not Statics.GetLandFlag(land_id, "Impassable") or land_id in CaveTiles:
        
        Player.Walk('West')
        Misc.Pause(400)
        x_delta, y_delta = MotionMap[Player.Direction]
        x = Player.Position.X + x_delta
        y = Player.Position.Y + y_delta
        xStart = Player.Position.X
        yStart = Player.Position.Y
        land_id = Statics.GetLandID(x, y, Player.Map)
        Misc.SendMessage("X: {} Y: {} LandID: 0x{:x} ImPassable: {}".format(x, y, land_id, Statics.GetLandFlag(land_id, "Impassable")))
        if not Statics.GetLandFlag(land_id, "Impassable") or land_id in CaveTiles:
            
            Player.Walk('North')
            Misc.Pause(400)
            x_delta, y_delta = MotionMap[Player.Direction]
            x = Player.Position.X + x_delta
            y = Player.Position.Y + y_delta
            xStart = Player.Position.X
            yStart = Player.Position.Y
            land_id = Statics.GetLandID(x, y, Player.Map)
            Misc.SendMessage("X: {} Y: {} LandID: 0x{:x} ImPassable: {}".format(x, y, land_id, Statics.GetLandFlag(land_id, "Impassable")))
            
    if Statics.GetLandFlag(land_id, "Impassable") or land_id in CaveTiles:
        Journal.Clear()
        while True:
            if Player.Position.X != xStart:
                return
            if Player.Position.Y != yStart:
                return    
            if Journal.Search('no metal'):
                Player.HeadMessage(5, "NONE")
                break
            if Journal.Search('no sand'):
                Player.HeadMessage(5, "DONE")                
                break
            if Journal.Search('Target cannot be seen'):
                break
            if Journal.Search('You can\'t mine there'):
                break
            tileinfo = Statics.GetStaticsLandInfo(x, y, Player.Map)
              
            if Items.BackpackCount(0x0E86, 0) > 0:
                Items.UseItemByID(0x0E86, -1)    
            else:    
                Items.UseItemByID(shovelID, -1) 
            Target.WaitForTarget(waitForTarget,False)                    
            tiles = Statics.GetStaticsTileInfo(x, y, Player.Map)

            if tileinfo.StaticID in CaveTiles and len(tiles) > 0:
    
                Target.TargetExecute(x, y, tiles[0].StaticZ, tiles[0].StaticID)
            else:
                Target.TargetExecuteRelative(Player.Serial, 1)
            Misc.Pause(waitAfterMining)
            on_me_filter = Mobiles.Filter()
            on_me_filter.Enabled = True
            on_me_filter.RangeMin = -1
            on_me_filter.RangeMax = 2
            on_me_filter.Bodies = List[int] ( [ 0x006F ] )
            on_me_filter.Notorieties = List[Byte](bytes([3,4,5,6]))
            up_close_enemies = Mobiles.ApplyFilter(on_me_filter)
            if len(up_close_enemies) > 0:
                Player.HeadMessage(2, "STOPPING FOR AGRO")
                Stop()
            if Player.WarMode == True:
                Stop()    
            if Target.HasTarget(): 
                Target.Cancel()                    
            CheckWeight()    
    listVeins = getVeins()
    if listVeins != None and len(listVeins) > 0:
        for vein in listVeins:
            while Items.FindBySerial(vein.Serial):
                Items.UseItemByID(pickaxeID,0)
                Target.WaitForTarget(waitForTarget,False)
                Target.TargetExecute(vein)
                Misc.Pause(waitAfterMining)
                CheckWeight()
            if Target.HasTarget(): 
                Target.Cancel()
    
    

def CheckWeight():
    
    if Player.Weight > (Player.MaxWeight*.9) or Player.Weight > 520:
        smelt()
        


            
def Findsecure():
    
    secure = Items.Filter()
    secure.IsContainer = True
    secure.RangeMax = 2
    found = Items.ApplyFilter(secure)
    if len(found) > 0:
        chest = found[0]
        Misc.Pause(400)
        mining = [0x1BF2,0x3193,0x3197,0x3195,0x3192,0x3194,0x0F28,0x0F2A,0x0F2B,0x3198,0x0F26]
        for t in Items.FindBySerial(Player.Backpack.Serial).Contains:
            if t.ItemID in mining:
                Items.Move(t, chest ,0)
                Misc.Pause(1000)
               
                    

                
           
while not Player.IsGhost: 
    for coords in railCoords:
        gotoLocation(coords[0],coords[1])
        Misc.Pause(500)
        Findsecure()
        CheckWeight()
        MineSpot()