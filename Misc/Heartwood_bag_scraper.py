talismans = [ 0x2F59,  # Serpente
              0x2F58,  # Scudo
              0x2F5B,  # Y
              0x2F5A,  # Croce
            ]

recipes = [ 0x2831 ]  # Recipe              

skills = ["Alchemy", "Blacksmithing", "Cartography", "Carpentry", "Cooking", "Fletching", "Inscription", "Tailoring", "Tinkering"]

max_skill = {}
max_skill_exceptional = {}

max_skill               = {"Alchemy": [29,0], "Blacksmithing": [24,0], "Cartography": [26,0], "Carpentry": [24,0],
                           "Cooking": [26,0], "Fletching": [18,0], "Inscription": [30,0], "Tailoring": [28,0], "Tinkering": [24,0]
                          }
                          
max_skill_exceptional   = {"Alchemy": [26,0], "Blacksmithing": [29,0], "Cartography": [28,0], "Carpentry": [23,0],
                           "Cooking": [24,0], "Fletching": [18,0], "Inscription": [23,0], "Tailoring": [27,0], "Tinkering": [21,0]
                          }


needed_recipes = {}
known_recipes = [ # In lowercase
                
                    # rare items
                    #"acid proof rope"
                    #"bramble coat"
                    #"ironwood crown"
                    #"phantom staff"
                    #"warrior statue (east)"

                 "ancient wild staff",
                 "arcanist's wild staff",
                 "hardened wild staff",
                 
                 "thorned wild staff",
                 
                 "arcane bookshelf (east)",
                 "arcane bookshelf (south)",
                 "elven armoire",
                 "elven armoire (fancy)",
                 "elven dresser",
                 "elven dresser (east)",
                 "elven dresser (south)",
                 "ornate elven chair",
                 "ornate elven chest (east)",
                 "ornate elven chest (south)",
                 "tall elven bed (east)",
                 "tall elven bed (south)",
                 
                 
                 "stone anvil (east)",
                 "stone anvil (south)",
                 
                 "squirrel statue (east)",
                 "squirrel statue (south)",
                 #"warrior statue (east)",  # rare
                 "warrior statue (south)",
                 
  
                 "assassin's shortbow",
                 "blight gripped longbow",
                 "barbed longbow",
                 #"faerie fire",  # rare
                 "frozen longbow",
                 "lightweight shortbow",
                 "longbow of might",
                 "mischief maker",
                 "mystical shortbow",
                 "ranger's shortbow",
                 "silvani's feywood bow",
                 "slayer longbow",
                ]
                          

def getItems( itemID , container = Player.Backpack  ):
    
    itemList = []
    
    if container.RootContainer != Player.Serial:
        #Misc.SendMessage("The item is either in your pack (somewhere) or in the bank")
        Items.UseItem(container.Serial)
        Misc.Pause(700)
        
    for item in container.Contains:
        if item.ItemID in itemID:
            itemList.append(item.Serial)
    
    subcontainers = [ item for item in container.Contains if item.IsContainer ]

    # Iterate through each item in the given list
    for subcontainer in subcontainers:
        itemInsideContainer = getItems( itemID, subcontainer )
        for i in itemInsideContainer:
            itemList.append(i)

    return itemList
    
    
def getSkillLevel(proptext):
    skill = proptext.split(':')[1]
    return skill[:-1]
    
def isExceptional(proptext):
    if "Exceptional" in proptext:
        return True
    else:
        return False

     
     
def analizeTalismans(serial):
    item = Items.FindBySerial(serial)
    
    if (item.ItemID not in talismans):
        return
    
    props = item.Properties
    for prop in props:
        proptext = prop.ToString()
        for skill in skills:
            if skill in proptext:
                skillLevel = int(getSkillLevel(proptext))
                isExcept = isExceptional(proptext)
                if isExcept:
                    if skill in max_skill_exceptional:
                        level = int(max_skill_exceptional[skill][0])
                        if skillLevel > level:
                            max_skill_exceptional[skill] = [skillLevel, serial]
                        else:
                            pass
                    else:
                        max_skill_exceptional[skill] = [skillLevel, serial]
                        
                else:
                    if skill in max_skill:
                        level = int(max_skill[skill][0])
                        if skillLevel > level:
                            max_skill[skill] = [skillLevel, serial]
                        else:
                            pass
                    else:
                        max_skill[skill] = [skillLevel, serial]    
     

                
                
def analizeRecipes(serial):
    item = Items.FindBySerial(serial)
    
    if (item.ItemID not in recipes):
        return     
    
    props = item.Properties
    for prop in props:     
        propText = prop.ToString()
        if propText.startswith('[') and propText.endswith(']'):
            propText = propText[1:] # removes [
            propText = propText[:-1] # removes [
            if propText.lower() not in known_recipes: 
                needed_recipes[propText] = serial
                Misc.SendMessage("Recipe to be taken: " + propText)
        pass
        


def grabAllTalismansFromDictionary(dict):
    count = 0  
    for item in dict:            
        serial =  dict[item][1]
        if serial > 0:
            Items.Move(serial, mybag, 1)
            Misc.Pause(500)
            count = count + 1
    return count


def grabAllRecipesFromDictionary(dict):
    count = 0  
    for item in dict:            
        serial =  dict[item]
        if serial > 0:
            Items.Move(serial, mybag, 1)
            Misc.Pause(500)
            count = count + 1
    return count
    
    
        
############################################################
    

Player.HeadMessage(30,"Source bag")
searchbag = Target.PromptTarget("Source bag")      
Player.HeadMessage(30,"Bag for found items")
mybag = Target.PromptTarget("Bag for found items")
  
    
        
found = []    

findBag = Items.FindBySerial(searchbag)
Misc.Pause(100)
found = getItems(talismans + recipes, findBag)
Misc.Pause(100)

Player.HeadMessage(44,"Found talismani: " + str(len(found)))


for serial in found:
    analizeTalismans(serial)
    analizeRecipes(serial)
    

#for tali in max_skill:
#    Misc.SendMessage("N:" + tali + " " + str(max_skill[tali][0]) + " " + str(max_skill[tali][1]))
#    pass    

#for tali in max_skill_exceptional:
#    Misc.SendMessage("E:" + tali + " " + str(max_skill_exceptional[tali][0]) + " " + str(max_skill_exceptional[tali][1]))
#    pass
    
    
for tali1 in max_skill:
    serial1 = max_skill[tali1][1]
    for tali2 in max_skill_exceptional:
        serial2 = max_skill_exceptional[tali2][1]
        if serial1 == serial2:
            max_skill_exceptional[tali2][1] = 0 #Set serial to 0 for ignore it
            break
    
Misc.Pause(800)
            
cnt_talismans = 0
cnt_recipes = 0

cnt_talismans = cnt_talismans + grabAllTalismansFromDictionary(max_skill)
#for tali in max_skill:            
#    serial =  max_skill[tali][1]
#    if serial > 0:
#        Items.Move(serial, mybag, 1)
#        Misc.Pause(200)
#        count = count + 1

cnt_talismans = cnt_talismans + grabAllTalismansFromDictionary(max_skill_exceptional)    
#for tali in max_skill_exceptional:
#    serial =  max_skill_exceptional[tali][1]       
#    if serial > 0:
#        Items.Move(serial, mybag, 1)
#        Misc.Pause(200)
#        count = count + 1
    
 
cnt_recipes = grabAllRecipesFromDictionary(needed_recipes)
        
        
Misc.SendMessage("Talismans taken: " + str(cnt_talismans))
Misc.SendMessage("Recipes taken: " + str(cnt_recipes))
    