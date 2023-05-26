import sys, math


DRAGGED_SOURCE_CNT = 50
DRAGGED_SPOOL_CNT = 50

linenwhool = [
                0x0DF9, # Cotton
                0x1A9C, # Flax Bundle 1
                0x1A9D, # Flax Bundle 2
             ]
             
wheelID = 0x1015  # 0x1015 0x101c 0x1019
loomID = 0x1062
spoolID = 0x0FA0
boltofclothID = 0x0F95



def distance2D(pos1, pos2):
    return math.sqrt( ((pos1.X - pos2.X)**2) + ((pos1.Y - pos2.Y)**2) )

def stopWithError(errorMessage):
    Misc.SendMessage(errorMessage)
    sys.exit(errorMessage)


def getWheelIfPlayerIsCloseTo():
    wheel = Items.FindByID(wheelID, -1, -1)
    if wheel == None:
        stopWithError('No Spinning Wheel found')
    
    distance = distance2D(Player.Position, wheel.Position)        
    if distance > 2:
        stopWithError('Need to be close to a spinnig wheel')

    return wheel


def getLoomIfPlayerIsCloseTo():
    loom = Items.FindByID(loomID, -1, -1)
    if loom == None:
        stopWithError('No Loom found')
    
    distance = distance2D(Player.Position, loom.Position)        
    if distance > 2:
        stopWithError('Need to be close to a Loom')

    return loom
    
    
def useLoom(fromContainer):
  spool = Items.FindByID(spoolID, 0, fromContainer.Serial)
  if spool != None:
    Items.UseItem(spool.Serial)
    Target.WaitForTarget(20000)
    Target.TargetExecute(loom)
    Misc.Pause(300)
    
    
    
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
        Player.HeadMessage(30, "Taking resource from container")
        Misc.SendMessage("Remaining " + str(source.Amount) + " " + source.Name)
        Items.Move(source, Player.Backpack, DRAGGED_SOURCE_CNT)
        Misc.Pause(1000)
        source = Items.FindByID(resource, 0, container.Serial)
        
        # Start using Items
        using = Items.FindByID(resource, 0, Player.Backpack.Serial)
        while using != None and using.Amount:
            Items.UseItem(using.Serial)
            Target.WaitForTarget(20000)
            Target.TargetExecute(wheel)
            Misc.Pause(700)
            useLoom(Player.Backpack)
            Misc.Pause(700)
            useLoom(Player.Backpack)
            Misc.Pause(700)
            using = Items.FindByID(resource, 0, Player.Backpack.Serial)
            Misc.Pause(3000)
        
        # If there are some spool of threads in the BackPack i put into the resource
        spool = Items.FindByID(spoolID, 0, Player.Backpack.Serial)
        Items.Move(spool, container, 0)
        Misc.Pause(1000)

        # If there are some Bolt of Cloth in the BackPack i put into the resource
        boltofcloth = Items.FindByID(boltofclothID, 0, Player.Backpack.Serial)
        Items.Move(boltofcloth, container, 0)
        Misc.Pause(1000)
        

        
Player.HeadMessage(30, "Batch of material done")
# If there are some spool of threads in the Container i use them
spool = Items.FindByID(spoolID, 0, container.Serial)
while spool != None and spool.Amount:
    Player.HeadMessage(30, "Finishing remaining spool of thread")
    Items.Move(spool, Player.Backpack, DRAGGED_SPOOL_CNT)
    Misc.Pause(1000)
    spoolBackpack = Items.FindByID(spoolID, 0, Player.Backpack.Serial)
    while spoolBackpack != None and spoolBackpack.Amount:
        useLoom(Player.Backpack)
        Misc.Pause(700)
        spoolBackpack = Items.FindByID(spoolID, 0, Player.Backpack.Serial)
    spool = Items.FindByID(spoolID, 0, container.Serial)

    # If there are some Bolt of Cloth in the BackPack i put into the resource
    boltofcloth = Items.FindByID(boltofclothID, 0, Player.Backpack.Serial)
    Items.Move(boltofcloth, container, 0)
    Misc.Pause(1000)
    

Player.HeadMessage(30, "ALL DONE")    
    