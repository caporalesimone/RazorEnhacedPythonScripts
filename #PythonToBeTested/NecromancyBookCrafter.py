#Necromancy Spellbook Crafter by Frank Castle
#
# Instructions:
#
# Have plenty of Exceptional Scribes Pens with makers mark on them
# Have GM Inscription.  It just makes it easier.
# Have a resource container with plenty of scrolls and regs
# Have at least 100 mana
# Have a trash can within reach
# Have your Necromancy spellbook in your hand.  Do not have any other Necromancy spellbooks in your backpack.
# Having Meditation and a Mana Regen suit is recommended, but not necessary. 
# This will use premade scrolls if they are in the Storage Container. Otherwise it will make them.

from System.Collections.Generic import List

stoCont = Target.PromptTarget('Target your Storage Container')
Items.UseItem(stoCont)
Misc.Pause(2000)

bookBag = Target.PromptTarget('Target your BookBag')
Items.UseItem(stoCont)
Misc.Pause(2000)

regsList = [0x0F78,0x0F8E,0x0F8F,0x0F7D,0x0F8A,0x0EF3]
necScrollList = [0x2260,0x2261,0x2262,0x2263,0x2264,0x2265,
0x2266,0x2267,0x2268,0x2269,0x226A,0x226B,0x226C,0x226D,0x226E,
0x226F,0x2270]
global pen
pen = Items.FindByID(0x0FBF,-1,Player.Backpack.Serial)
global GumpButton            
GumpButton = 100 

GFilter = Items.Filter()
GFilter.RangeMax = 5
GFilter.OnGround = True
GFilter.Enabled = True
GFilter.Movable = True
garbagecan = List[int]((0x0E77, 0x0E77))  
GFilter.Graphics = garbagecan

def getSupplies():
    for i in regsList:
        if Items.BackpackCount(i,-1) < 30:
            reg = Items.FindByID(i,-1,stoCont)
            Misc.Pause(500)
            Items.Move(reg,Player.Backpack.Serial,100)
            Misc.Pause(1100)
           
def makeScrolls():
    
    for S in necScrollList:
        getSupplies()
        checkPen()
        checkMana(41)
        global GumpButton
        GumpButton = GumpButton + 1
        def necScroll():
            Items.UseItem(pen)
            Gumps.WaitForGump(460, 10000)
            Gumps.SendAction(460, GumpButton)
            Misc.Pause(3000)
        storedScroll = Items.FindByID(S,-1,stoCont)
        spellbook = Items.FindByID(0x2253,-1,Player.Backpack.Serial)
        if storedScroll:
            Items.Move(storedScroll, spellbook, 1)
            Misc.Pause(1100)
        else:
            while Items.ContainerCount(Player.Backpack.Serial,S,-1) < 1:
                necScroll()
                Misc.Pause(200)
            packScroll = Items.FindByID(S,-1, Player.Backpack.Serial)
            Misc.Pause(200)
            Items.Move(packScroll, spellbook, 1)
            Misc.Pause(1100)
    GumpButton = 100
                
def makeSpellbook():
    getSupplies()
    Items.UseItem(pen)
    Gumps.WaitForGump(460, 10000)
    Gumps.SendAction(460, 207)
    Misc.Pause(3000)
    spellbook = Items.FindByID(0x2253,-1,Player.Backpack.Serial)
    if not spellbook:
        makeSpellbook()
        
def checkPen():
    curCharges = Items.FindByID(0x0FBF,-1,Player.Backpack.Serial)
    Items.WaitForProps(curCharges,2000)
    props = Items.GetPropStringList(curCharges.Serial)
    Misc.Pause(500)
    prop = props[3].split(' ')[2]
    Misc.SendMessage(prop)
    Misc.Pause(500)
    if int(prop) < 20:
        global pen
        garbagecans = Items.ApplyFilter(GFilter)
        Misc.Pause(500)
        garbagecan = Items.Select(garbagecans, 'Nearest')
        Misc.Pause(500)
        Items.Move(pen,garbagecan,0)
        Misc.Pause(1100)
        checkPen()
        pen = Items.FindByID(0x0FBF,-1,Player.Backpack.Serial)
        
def checkMana(mana):
    while Player.Mana < mana:
        Player.UseSkill('Meditation')
        Misc.Pause(11500)
        
def makeBook():
    while Player.Mana < Player.ManaMax :
        Player.UseSkill('Meditation')
        Misc.Pause(10000)
    makeSpellbook()
    makeScrolls()
    
    spellbook = Items.FindByID(0x2253,-1,Player.Backpack.Serial)
    Misc.Pause(200)
    Items.Move(spellbook,bookBag,0)

while True:
    makeBook()