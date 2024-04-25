from System.Collections.Generic import List
from System import Int32 as int
import sys, math


DRAGGED_SOURCE_CNT = 5
DRAGGED_SPOOL_CNT = 25
LOOM_USAGE_PAUSE = 150


linenwhool = [
                0x0DF9, # Cotton
                0x1A9C, # Flax Bundle 1
                0x1A9D, # Flax Bundle 2
             ]
             
wheelID = List[int]([0x1015, 0x101c, 0x1019])
loomID = List[int]([0x1062, 0x105F])
spoolID = 0x0FA0
boltofclothID = 0x0F95

def distance2D(pos1, pos2):
    return math.sqrt( ((pos1.X - pos2.X)**2) + ((pos1.Y - pos2.Y)**2) )

def stopWithError(errorMessage):
    Misc.SendMessage(errorMessage)
    sys.exit(errorMessage)

def getWheelIfPlayerIsCloseTo():
    wheel = Items.FindByID(wheelID, 0, -1, 3, False)
    if wheel == None:
        stopWithError('No Spinning Wheel found')
    
    distance = distance2D(Player.Position, wheel.Position)        
    if distance > 2:
        stopWithError('Need to be close to a spinnig wheel')

    return wheel


def getLoomIfPlayerIsCloseTo():
    loom = Items.FindByID(loomID, 0, -1, 3, False)
    if loom == None:
        stopWithError('No Loom found')
    
    distance = distance2D(Player.Position, loom.Position)        
    if distance > 2:
        stopWithError('Need to be close to a Loom')

    return loom
    
    
def useLoom(fromContainer):
  spools = Items.FindByID(spoolID, 0, fromContainer.Serial)
  if spools != None:
    for i in range(spools.Amount):
        # Use the current spool
        Items.UseItem(spools.Serial)
        Target.WaitForTarget(20000)
        Target.TargetExecute(loom)
        Misc.Pause(LOOM_USAGE_PAUSE)
      
        
def waitWheelEnds(fromContainer):

    spools_count = 0
    spools = Items.FindByID(spoolID, 0, fromContainer.Serial)
    if spools != None:
        spools_count = spools.Amount
    
    Player.HeadMessage(30, "Waiting wheel ends")
    while True:
        spools = Items.FindByID(spoolID, 0, fromContainer.Serial)
        if spools != None and spools.Amount > spools_count:
            break
        else:
            Misc.Pause(200)
        
##########################################################

wheel = getWheelIfPlayerIsCloseTo()
loom = getLoomIfPlayerIsCloseTo()
container = Items.FindBySerial(Target.PromptTarget("Select resource container"))
Misc.Pause(1000)
Items.UseItem(container)
Misc.Pause(1000)

for resource in linenwhool:
    source = Items.FindByID(resource, 0, container.Serial)
    while source != None and source.Amount:
        Player.HeadMessage(30, "Found " + source.Name)
        Player.HeadMessage(30, "Taking " + str(DRAGGED_SOURCE_CNT) + " from the container")
        
        Items.Move(source, Player.Backpack, DRAGGED_SOURCE_CNT)
        Misc.Pause(1000)
        
        # Start using Items
        using = Items.FindByID(resource, 0, Player.Backpack.Serial)
        while using != None:
            Player.HeadMessage(30, "Using the wheel")
            Items.UseItem(using.Serial)
            Target.WaitForTarget(20000)
            Target.TargetExecute(wheel)
            waitWheelEnds(Player.Backpack)
            
            Player.HeadMessage(30, "Using the wheel")
            Items.UseItem(using.Serial)
            Target.WaitForTarget(20000)
            Target.TargetExecute(wheel)
            Misc.Pause(500)
            
            Player.HeadMessage(30, "Using the loom")
            useLoom(Player.Backpack)

            using = Items.FindByID(resource, 0, Player.Backpack.Serial)
            Misc.Pause(500)
        
        # If there are some Bolt of Cloth in the BackPack i put into the resource
        boltofcloth = Items.FindByID(boltofclothID, 0, Player.Backpack.Serial)
        if boltofcloth != None:
            Player.HeadMessage(30, "Moving bolt of cloth into the container")
            Items.Move(boltofcloth, container, 0)
            Misc.Pause(1000)

        source = Items.FindByID(resource, 0, container.Serial)
        
Player.HeadMessage(30, "Batch of material done")
# If there are some spool of threads in the Container i use them
spool = Items.FindByID(spoolID, 0, container.Serial)
while spool != None and spool.Amount:
    Player.HeadMessage(30, "Finishing remaining spool of thread")
    Items.Move(spool, Player.Backpack, DRAGGED_SPOOL_CNT)
    
    Misc.Pause(1000)
    spoolBackpack = Items.FindByID(spoolID, 0, Player.Backpack.Serial)
    if spoolBackpack != None:
        useLoom(Player.Backpack)
        Misc.Pause(700)

    spool = Items.FindByID(spoolID, 0, container.Serial)
    # If there are some Bolt of Cloth in the BackPack i put into the resource
    boltofcloth = Items.FindByID(boltofclothID, 0, Player.Backpack.Serial)
    Items.Move(boltofcloth, container, 0)
    Misc.Pause(1000)
    

Player.HeadMessage(30, "ALL DONE")    
    