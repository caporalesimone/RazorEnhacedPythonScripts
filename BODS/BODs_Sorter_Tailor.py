#
# Search bods in backpack and sort it into 3 books: cloth, shoes and leather
#
import sys

from System.Collections.Generic import List

cloth_names = ["bandana", "body sash", "bonnet", "cap", "cloak", "doublet", "fancy dress", "fancy shirt", "feathered hat", "full apron", "floppy hat", "half apron", "jester hat", "jester suit", "kilt", "long pants", "plain dress", "robe", "shirt", "short pants", "skirt", "skullcap", "straw hat", "surcoat","tall straw hat", "tricorne hat", "tunic", "wide-brim hat", "wizard's hat" ]
shoes_names = ["boots", "thigh boots","sandals", "shoes"]
leather_names = ["female leather armor", "leather bustier", "leather cap", "leather gloves", "leather gorget", "leather leggings", "leather shorts", "leather skirt", "leather sleeves", "studded sleeves", "studded tunic"]
bones_names = ["bone armor", "bone arms", "bone gloves", "bone helmet", "bone leggings"]

bodID = 0x2258
dragSleep = 1000
headMsgColor = 30

def stopWithError(errorMessage):
    Misc.SendMessage(errorMessage)
    sys.exit(errorMessage)

def getItems( itemID , container = Player.Backpack  ):
    '''
    Recursively looks through backpack for any items in the itemID list
    Returns a list with item serials
    '''
    
    # Create the list
    itemList = []
    
    if isinstance( itemID, int ):
        for item in container.Contains:
            if item.ItemID == itemID:
                itemList.append(item.Serial)

    elif isinstance( itemID, list ):
        for item in container.Contains:
            if item.ItemID in itemID:
                itemList.append(item.Serial)
    else:
        raise ValueError( 'Unknown argument type for itemID passed to FindItem().', itemID, container )

    subcontainers = [ item for item in container.Contains if item.IsContainer ]

    # Iterate through each item in the given list
    for subcontainer in subcontainers:
        wandsInSubContainer = getItems( itemID, subcontainer )
        for i in wandsInSubContainer:
            itemList.append(i)

    return itemList

def getItemNameFromSmallBod(props):
    item = props[len(props) - 1].ToString()
    item = item.split(':')[0]
    return item

# In a Small Bod, gets the item Family (Cloth, Shoes, Leather)
def getItemFamilyFromSmallBod(props):
    
    item = getItemNameFromSmallBod(props)

    if item in cloth_names:
        return "Cloth"
    if item in shoes_names:
        return "Shoes"
    if item in leather_names:
        return "Leather"
    if item in bones_names:
        return "Bones"
    stopWithError("Unable to understand what kind of BOD is this: " + item)

# Iterates through properties and check if is Exceptional
def isExceptional(props):
    for prop in props:
        if "EXCEPTIONAL" in prop.ToString().upper():
            return True
    return False

# Iterates through properties and gets if bod is Small or Large
def isSmallBod(props):
    for prop in props:
        if "SMALL BULK ORDER" in prop.ToString().upper():
            return True
        if "LARGE BULK ORDER" in prop.ToString().upper():
            return False
    stopWithError("Unable to understand bod type [Small/Large]")

# Returns a dictionary of the items
#   key: Item Family (small, large, exceptional with the kind of material)
#   value: list of serials
def catalogItems(itemsList):
    if len(itemsList) > 0:
        bodsType = {}
        for serial in itemsList:
            bod = Items.FindBySerial(serial)
            props = bod.Properties
            
            bodKind = ""

            if isSmallBod(props):
                itemFamily = getItemFamilyFromSmallBod(props)
                if isExceptional(props):
                    bodKind = "Small " + itemFamily + " Exceptional"
                else:
                    bodKind = "Small " + itemFamily
            else:      
                if isExceptional(props):
                    bodKind = "Large Exceptional"
                else:
                    bodKind = "Large Normal"

            if (bodKind in bodsType):
                bodsType[bodKind].append(serial)
            else:
                lista = [serial]
                bodsType[bodKind] = lista
    else:
        stopWithError("List is empty in catalogItems")      

    # Returns bods dictionary
    return bodsType

# Logs Items quantities in Items dictionary
def logItemsDict(bodsDict):
    for key in sorted (bodsDict.keys(), reverse=True):
        Misc.SendMessage("Found: " + key + " : " + str(len(bodsDict[key])))

# Move bods into contaier or Books of BODS
def moveBODs(bodsDict):
    for key in sorted (bodsDict.keys(), reverse=True):
        Player.HeadMessage(headMsgColor, "Select Container " + key.upper())
        container = Target.PromptTarget("Select Container " + key.upper())
        if (container <= 0):
            Misc.SendMessage(key + " skipped")
            continue

        Misc.SendMessage(str(len(bodsDict[key])) + " bods to be moved")
        for bod in bodsDict[key]:
            props = Items.FindBySerial(bod).Properties
            if isSmallBod(props) == True:
                item = getItemNameFromSmallBod(props)
                Player.HeadMessage(headMsgColor, item)
            else:
                Player.HeadMessage(headMsgColor, key)

            Journal.Clear( )
            Items.Move(bod, container, 1)
            Journal.WaitJournal("Deed added to book.", 40000)

#---------------------------------------------#
#                   M A I N                   #
#---------------------------------------------#

bodsList = []
bodsList = getItems(bodID)

if len(bodsList) <= 0:
    stopWithError("Unable to find BODs in Backpack")

itemsDict = {}
itemsDict = catalogItems(bodsList)

logItemsDict(itemsDict)

moveBODs(itemsDict)


        

Player.HeadMessage(headMsgColor, "ALL DONE!")        
