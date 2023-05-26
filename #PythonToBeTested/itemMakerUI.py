from time import sleep
from datetime import datetime
import clr, time, thread, sys, System, math

clr.AddReference('System')
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Data')
clr.AddReference('IronPython')
from System.Threading import *
from System.Collections.Generic import List
from System import Byte
from System import Environment
from System.Drawing import Point, Color, Size
from System.Windows.Forms import (Application, Button, Form, BorderStyle, Label, FlatStyle, DataGridView,
 DataGridViewAutoSizeColumnsMode, DataGridViewSelectionMode, DataGridViewEditMode, RadioButton, GroupBox,
 TextBox, CheckBox, ProgressBar, ComboBox)
from System.Data import DataTable
import sys
Journal.Clear()
contents = []

tinkerID = 0x1EB9
sewID = 0x0F9D
sawID = 0x1034
tongID = 0x0FBC
scribeID = 0x0FBF
bowcraftID = 0x1022 
 
tinkerTool = Items.FindByID(0x1EB9,0x0000,Player.Backpack.Serial)
kit = Items.FindByID(0x0F9D,0x0000,Player.Backpack.Serial)
tongs = Items.FindByID(0x0FBC,0x0000,Player.Backpack.Serial)
saw = Items.FindByID(0x1034,0x0000,Player.Backpack.Serial)
eleList = ['physical','fire','cold','poison','energy','chaos']

reforgeSet = False
global reforgeSet
GFilter = Items.Filter()
GFilter.RangeMax = 5
GFilter.OnGround = True
GFilter.Enabled = True
GFilter.Movable = True
garbagecan = List[int]((0x0E77, 0x0E77))
GFilter.Graphics = garbagecan

pinkGumpList = [1044064,1044066,1044070,1044072,1044079,1044063, 1044061, 1044091, 1044102, 1044110, 1044077,
1044101, 1044065, 1044100, 1044087, 1044117, 1044103, 1044060, 1044067, 1044068, 1044071, 1044073, 1044083, 1044104,
1044105, 1044094, 1044097, 1044112, 1044111, 1044076, 1044116, 1044085, 1044106, 1044115, 1044109, 1044113, 1044086,
1044114, 1044092, 1044062, 1044095, 1044078, 1044080, 1044098, 1044099, 1044074, 1044081, 1044084, 1044090, 1044108,
1044088, 1044093, 1044107, 1044084, 1044075, 1044089, 1044069, 1044082]

psGumpList = [1044061, 1044091, 1044102, 1044110, 1044077,1044101, 1044065, 1044100, 1044087, 1044117, 1044103, 1044112,
1044111, 1044076, 1044116, 1044085, 1044106, 1044115, 1044109, 1044113, 1044086, 1044114, 1044092, 1044062, 1044095, 
1044099, 1044093, 1044107, 1044075, 1044089, 1044069, 1044082]

pinkMisc = ['Forensics','Item','Taste','Arms','Begging','Camping','Cartography']
pinkCombat = ['Anatomy','Archery','Fencing','Focus','Healing','Mace','Parrying','Swordsmanship','Tactics','Throwing','Wrestling']
pinkTrade = ['Alchemy','Blacksmithing','Fletching','Carpentry','Cooking','Inscription','Lumberjacking','Mining','Tailoring','Tinkering']
pinkMagic = ['Bushido','Chivalry','Eval','Imbuing','Magery','Meditation','Mysticism','Necromancy','Ninjitsu','Resisting','Spellweaving','Spirit']
pinkWilderness = ['Animal','Fishing','Herding','Tracking','Veterinary']
pinkThieving = ['Detecting','Hiding','Lock','Poisoning','Remove','Snooping','Stealing','Stealth']
pinkBard = ['Discordance','Musicianship','Peacemaking','Provocation']


psCombat = ['anatomy','archery','fencing','focus','healing','mace','parrying','swordsmanship','tactics','throwing','wrestling']
psMagic = ['bushido','chivalry','evaluate','imbuing','magery','meditation','mysticism','necromancy','ninjitsu','resisting','spellweaving','spirit']
psOther = ['animal','fishing','herding','tracking','veterinary','detecting','hiding','lock','poisoning','remove','snooping','stealing','stealth', 'discordance','musicianship','peacemaking','provocation']

#######name your bod books like this
bodBookNames = ['SmithIron','SmithRecycle','SmithPOF','SmithShadowHammer','SmithHigh','SmithLarge',
'BowcraftRecycle', 'BowcraftAshKit','BowcraftOakKit']

#imbueing sub menus to allow prop selection from imbue list
slayers = ['Spider Slayer Wep','Dragon Slayer Wep']
superSlayers = ['Undead Slayer Wep','Reptile Slayer Wep','Repond Slayer Wep','Fey Slayer Wep','Elemental Slayer Wep','Demon Slayer Wep','Arachnid Slayer Wep']
hitEffects =['Hit Stamina Leech Wep','Hit Mana Leech Wep','Hit Magic Arrow Wep','Hit Lower Defense Wep','Hit Lower Attack Wep','Hit Lightning Wep',
'Hit Life Leech Wep','Hit Harm Wep','Hit Fireball Wep','Hit Dispel Wep']
hitAreaEffects = ['Hit Poison Area Wep','Hit Physical Area Wep','Hit Fire Area Wep','Hit Energy Area Wep','Hit Cold Area Wep']
casting = ['Spell Channeling Wep','Mage Weapon Wep','Faster Casting Wep','Lower Mana Cost Armor','Lower Reagent Cost Armor','Lower Mana Cost Jewls','Lower Reagent Cost Jewls', 'Faster Casting Jewls', 'Faster Cast Recovery Jewls']
combat = ['Damage Increase Wep','Swing Speed Increase Wep','Hit Chance Increase Wep','Defense Chance Increase Wep','Use Best Weapon Skill Wep','Damage Increase Jewls','Hit Chance Jewls'],['Defence Chance Jewls']
stats = ['Stamina Increase Armor','Hit Point Regeneration Armor','Stamina Regeneration Armor','Mana Regeneration Armor','Mana Increase Armor','Hit Point Increase Armor','Strength Bonus Jewls','Intelligence Bonus Jewls','Dexterity Bonus Jewls']
skillGroup1 = []
skillGroup2 = ['Taming Jewls']
skillGroup3 = []
skillGroup4 = ['Anatomy Jewls']
skillGroup5 = ['Chivalry Jewls','Resist Jewls']
#### items that can fail to be crafted exceptionally for bod filler, these are crafted slower to check 
canFail = ["platemail arms","platemail gloves","platemail gorget","platemail legs","platemail tunic","plate helm"] 

##### (str menu selection, imbue gump to select property)
imbueList = (
['Hit Mana Leech Wep',213],            ###weps
['Hit Life Leech Wep',208],
['Hit Stamina Leech Wep',215],
['Undead Slayer Wep',207],
['Reptile Slayer Wep',206],
['Repond Slayer Wep',205],
['Fey Slayer Wep',204],
['Elemental Slayer Wep',203],
['Demon Slayer Wep',202],
['Arachnid Slayer Wep',201],
['Spider Slayer Wep',217],
['Dragon Slayer Wep',205],
['Hit Lightning Wep',209],
['Hit Lower Defense Wep',211],
['Hit Poison Area Wep',205],
['Hit Physical Area Wep',204],
['Hit Fire Area Wep',203],
['Hit Energy Area Wep',202],
['Hit Cold Area Wep',201],
['Spell Channeling Wep',203],
['Faster Casting Wep',201],
['Damage Increase Wep',206],
['Swing Speed Increase Wep',205],

['Stamina Increase Armor',206],            ####armor
['Hit Point Regeneration Armor',205],
['Stamina Regeneration Armor',204],
['Mana Regeneration Armor',203],
['Mana Increase Armor',202],
['Hit Point Increase Armor',201],
['Lower Reagent Cost Armor',202],
['Lower Mana Cost Armor',201],

['Strength Bonus Jewls',203],                   #### jewls
['Intelligence Bonus Jewls',202],
['Dexterity Bonus Jewls',201],
['Damage Increase Jewls',203],
['Hit Chance Jewls',202],
['Defence Chance Jewls',201],
['Lower Mana Cost Jewls',203],
['Lower Reagent Cost Jewls',204],
['Anatomy Jewls',201],
['Chivalry Jewls',204],
['Resist Jewls',202],
['Taming Jewls',204],
['Faster Casting Jewls',202],
['Faster Cast Recovery Jewls',201]
)
#################  all mats( name , ID ,optional hue)#################   
matIdList = (
['Magical Residue',0x2DB1],  # need all imbue mats here
['Enchanted Essence',0x2DB2],
['Relic Fragment',0x2DB3],
['daemon claw',0x5721],
['undying flesh',0x5731],
['lava serpent crust',0x572D],
['spider carapace',0x5720],
['silver snake skin',0x5744],
['fey wings',0x5726],
['crystal shards',0x5738],
['void orb',0x573E],
['goblin blood',0x572C],
['crystalline blackrock',0x5732],
['raptor teeth',0x5747],
['essence of control',0x571C,0x048D],   
['essence of achievement',0x571C,0x002F],
['essence of precision',0x571C,0x0016],
['essence of singularity',0x571C,0x0497],
['essence of order',0x571C,0x0481],
['essence of diligence',0x571C,0x048e],
['parasitic plant',0x3190],
['luminescent fungi',0x3191],
['blue diamond',0x3198],
['faery dust',0x5745],
['fire ruby',0x3197],
['turquoise',0x3193],
['white pearl',0x3196],

['Ruby',0x0F13],          # all standard mats here
['Rubies',0x0F13],
['Amethyst',0x0F16],
['Sapphire',0x0F11],
['Star Sapphire',0x0F0F],
['Citrine',0x0F15],
['Emerald',0x0F10],
['Tourmaline',0x0F18],
['Diamond',0x0F26],
['Amber',0x0F25],
['iron',0x1BF2,0],
['Ingots',0x1BF2,0],
['ingots',0x1BF2,0],
['dull',0x1BF2,0x0973],
['shadow',0x1BF2,0x0966],
['copper',0x1BF2,0x096D],
['bronze',0x1BF2,0x0972],
['fire',0x1BF2,0x0972],   ##### used for ele dmg reforge
['gold',0x1BF2,0x08A5],
['agapite',0x1BF2,0x0979],
['cold',0x1BF2,0x0979],
['verite',0x1BF2,0x089F],
['energy',0x1BF2,0x089F],
['valorite',0x1BF2,0x08AB],
['leather',0x1081,0],
['barbed',0x1081,0x0851],
['horned',0x1081,0x0845],
['spined',0x1081,0x08AC],
['Leather or Hides',0x1081,0],
['leather or hides',0x1081,0],
['boards or logs',0x1BD7,0],
['Boards or Logs',0x1BD7,0],
['wood',0x1BD7,0],
['oak',0x1BD7,0x07da],
['ash',0x1BD7,0x04a7],
['yew',0x1BD7,0x04a8],
['heartwood',0x1BD7,0x04a9],
['bloodwood',0x1BD7,0x04aa],
['frostwood',0x1BD7,0x047f],
['Cloth',0x1766],
['Shaft',0x1BD4],
['Arrow',0x0f3f],
['Crossbow Bolt',0x1bfb]
)

############################ (str name, id , gump to craft, string tool name)   
dataList = (
["ringmail gloves", 0x13EB, 1, 'tongs'],#########################################  B S 
["ringmail leggings", 0x13F0, 2, 'tongs'],
["ringmail sleeves", 0x13EF, 3, 'tongs'],
["ringmail tunic", 0x13EC, 4, 'tongs'],
["chainmail coif", 0x13BB, 5, 'tongs'],
["chainmail leggings", 0x13BE, 6, 'tongs'],
["chainmail tunic", 0x13BF, 7, 'tongs'],
["platemail arms" , 0x1410 ,8, 'tongs'],
["platemail gloves", 0x1414, 9, 'tongs'],
["platemail gorget", 0x1413, 10, 'tongs'],
["platemail legs", 0x1411, 11, 'tongs'],
["platemail tunic", 0x1415, 12, 'tongs'],
["plate helm", 0x1412, 24, 'tongs'],
["broadsword", 0x0F5E, 42, 'tongs'],
["cutlass", 0x1441, 44, 'tongs'],
["circlet", 0x2B6E,104,'tongs'],
["katana", 0x13FF, 46, 'tongs'],
["longsword", 0x0F61, 48, 'tongs'],
["scimitar", 0x13B6, 49, 'tongs'],
["viking sword", 0x13B9, 50, 'tongs'],
["dagger", 0x0F51, 45, 'tongs'],
["kryss", 0x1401, 47, 'tongs'],
["short spear", 0x1403, 72, 'tongs'],
["spear", 0x0F62, 74, 'tongs'],
["war fork", 0x1405, 75, 'tongs'],
["hammer pick", 0x143D, 76, 'tongs'],
["mace", 0x0F5C, 77, 'tongs'],
["maul", 0x143B, 78, 'tongs'],
["war mace", 0x1407, 80, 'tongs'],
["war hammer", 0x1439, 81, 'tongs'],
["war axe", 0x13B0, 65, 'tongs'],
["axe", 0x0F49, 59, 'tongs'],
["battle axe", 0x0F47, 60, 'tongs'],
["double axe", 0x0F4B, 61, 'tongs'],
["executioner's axe", 0x0F45, 62, 'tongs'], #'
["large battle axe", 0x13FB, 63, 'tongs'],
["two handed axe", 0x1443, 64, 'tongs'],
["bardiche", 0x0F4D, 66, 'tongs'],
["halberd", 0x143F, 69, 'tongs'],
['bladed staff',0x26BD,67,'tongs'],
["female plate", 0x1C04, 13, 'tongs'],
["bascinet", 0x140C, 20, 'tongs'],
["close helmet", 0x1408, 21, 'tongs'],
["helmet", 0x140A, 22, 'tongs'],
["norse helm", 0x140E, 23, 'tongs'],
["buckler ", 0x1B73, 33, 'tongs'],   #### UO TYPO IN BODS EXTRA SPACE, LEAVE IN
["bronze shield", 0x1B72, 34, 'tongs'],
["heater shield", 0x1B76, 35, 'tongs'],
["metal shield", 0x1B7B, 36, 'tongs'],
["metal kite shield", 0x1B74, 37, 'tongs'],
["tear kite shield", 0x1B78, 38, 'tongs'],
["leather gorget", 0x13C7, 608, 'sew'], ################################# tailor
["leather cap", 0x1DB9, 609, 'sew'],
["leather gloves", 0x13C6, 610, 'sew'],
["leather sleeves", 0x13C5, 611, 'sew'],
["leather leggings", 0x13CB, 612, 'sew'],
["leather tunic", 0x13CC, 613, 'sew'],
["leather shorts", 0x1C00, 635, 'sew'],
["leather skirt", 0x1C08, 636, 'sew'],
["leather bustier", 0x1C0A, 637, 'sew'],
["studded bustier", 0x1C0C, 638, 'sew'],
["female leather armor", 0x1C06, 639, 'sew'],
["studded armor", 0x1C02, 640, 'sew'],
["studded gorget", 0x13D6, 625, 'sew'],
["studded gloves", 0x13D5, 626, 'sew'],
["studded sleeves", 0x13D4, 627, 'sew'],
["studded leggings", 0x13DA, 628, 'sew'],
["studded tunic", 0x13DB, 629, 'sew'],
["bone helmet", 0x1456, 641, 'sew'],
["bone gloves", 0x1455, 642, 'sew'],
["bone arms", 0x1453, 643, 'sew'],
["bone leggings", 0x1452, 644, 'sew'],
["bone armor", 0x144F, 645, 'sew'],
["sandals", 0x170D, 604, 'sew'],
["shoes", 0x1710, 605, 'sew'],
["boots", 0x170B, 606, 'sew'],
["thigh boots", 0x1712, 607, 'sew'],
["bandana", 0x1540, 4, 'sew'],
["shirt", 0x1517, 19, 'sew'],
["skirt", 0x1516, 40, 'sew'],
["skullcap", 0x1544, 3, 'sew'],
["doublet", 0x1F7B, 18, 'sew'],
["kilt", 0x1537, 39, 'sew'],
["jester hat", 0x171C, 14, 'sew'],
["jester suit", 0x1F9F, 27, 'sew'],
["cloak", 0x1515, 25, 'sew'],
["straw hat", 0x1717, 8, 'sew'],
["tunic", 0x1FA1, 21, 'sew'],
["long pants", 0x1539, 38, 'sew'],
["wizard's hat", 0x1718, 10, 'sew'], #'
["body sash", 0x1541, 44, 'sew'],
["robe", 0x1F03, 26, 'sew'],
["floppy hat", 0x1713, 5, 'sew'],
["full apron", 0x153D, 46, 'sew'],
["plain dress", 0x1F01, 23, 'sew'],
["bonnet", 0x1719, 11, 'sew'],
["half apron", 0x153B, 45, 'sew'],
["fancy dress", 0x1EFF, 24, 'sew'],
["feathered hat", 0x171A, 12, 'sew'],
["surcoat", 0x1FFD, 22, 'sew'],
["fancy shirt", 0x1EFD, 20, 'sew'],
["short pants", 0x152E, 37, 'sew'],
["tricorn hat", 0x171B, 13, 'sew'],
["cap", 0x1715, 6, 'sew'],
["wide-brim hat", 0x1714, 7, 'sew'],
["tall straw hat", 0x1716, 9, 'sew'],
["star sapphire ring", 0x108A , 100, 'tinker'],############################################ tinker
["star sapphire bracelet", 0x1086 ,105, 'tinker'],
["star sapphire earrings" , 0x1087 , 103, 'tinker'],
["emerald ring", 0x108A, 106, 'tinker'],
["emerald bracelet", 0x1086, 111, 'tinker'],
["emerald earrings", 0x1087, 109, 'tinker'],
["sapphire ring", 0x108A, 112, 'tinker'],
["sapphire bracelet", 0x1086, 117, 'tinker'],
["sapphire earrings", 0x1087, 115, 'tinker'],
["ruby ring", 0x108A, 118, 'tinker'],
["ruby bracelet", 0x1086, 123, 'tinker'],
["ruby earrings", 0x1087, 121, 'tinker'],
["citrine ring", 0x108A, 124, 'tinker'],
["citrine bracelet", 0x1086, 129, 'tinker'],
["citrine earrings", 0x1087, 127, 'tinker'],
["amethyst ring", 0x108A, 130, 'tinker'],
["amethyst bracelet", 0x1086, 135, 'tinker'],
["amethyst earrings", 0x1087, 133, 'tinker'],
["tourmmaline ring", 0x108A, 136, 'tinker'],
["tourmmaline bracelet", 0x1086, 141, 'tinker'],
["tourmmaline earrings", 0x1087, 139, 'tinker'],
["amber ring", 0x108A, 142, 'tinker'],
["amber bracelet", 0x1086, 147, 'tinker'],
["amber earrings", 0x1087, 145, 'tinker'],
["diamond ring", 0x108A, 148, 'tinker'],
["diamond bracelet", 0x1086, 153, 'tinker'],
["diamond earrings", 0x1087, 151, 'tinker'],
["ring", 0x108A, 1, 'tinker'],
["bracelet", 0x1086, 2, 'tinker'],
["key ring", 0x1011, 51, 'tinker'],
["globe", 0x1047, 55, 'tinker'],
["iron key", 0x1010, 54, 'tinker'],
["spyglass", 0x14F5, 56, 'tinker'],
["mortar and pestle", 0x0E9B, 9, 'tinker'],
["smith's hammer", 0x13E3, 21, 'tinker'],
["skillet", 0x097F, 26, 'tinker'],
["sewing kit", 0x0F9D, 14, 'tinker'],
["fletcher's tools", 0x1022, 28, 'tinker'],
["butcher knife", 0x13F6, 39, 'tinker'],
["spoon", 0x09F9, 40, 'tinker'],
["fork", 0x09F5, 43, 'tinker'],
["plate", 0x09D7, 42, 'tinker'],
["knife", 0x09F7, 46, 'tinker'],
["goblet", 0x099A, 48, 'tinker'],
["candelabra", 0x0A27, 52, 'tinker'],
["scales", 0x1851, 53, 'tinker'],
["lantern", 0x0A25, 57, 'tinker'],
["heating stand", 0x1849, 58, 'tinker'],
["fancy wind chimes", 0x2833, 63, 'tinker'],
["wind chimes", 0x2832, 62, 'tinker'],
["pewter mug", 0x1001, 49, 'tinker'],
["skinning knife", 0x0EC5, 50, 'tinker'],
["gears", 0x1053, 31, 'tinker'],
["clock parts", 0x104F, 32, 'tinker'],
["barrel tap", 0x1004, 33, 'tinker'],
["springs", 0x105D, 34, 'tinker'],
["sextant parts", 0x1059, 35, 'tinker'],
["barrel hoops", 0x10E1, 36, 'tinker'],
["hinge", 0x1055, 37, 'tinker'],
["bola balls", 0x0E73, 38, 'tinker'],
["scissors", 0x0F9E, 8, 'tinker'],
["scorp", 0x10E7, 10, 'tinker'],
["tinker's tools", 0x1EB9, 11, 'tinker'], #'
["hatchet", 0x0F43, 12, 'tinker'],
["draw knife", 0x10E4, 13, 'tinker'],
["saw", 0x1034, 15, 'tinker'],
["dovetail saw", 0x1028, 16, 'tinker'],
["froe", 0x10E5, 17, 'tinker'],
["shovel", 0x0F3A, 18, 'tinker'],
["hammer", 0x102A, 19, 'tinker'],
["tongs", 0x0FBC, 20, 'tinker'],
["sledge hammer", 0x0FB5, 22, 'tinker'],
["inshave", 0x10E6, 23, 'tinker'],
["pickaxe", 0x0E86, 24, 'tinker'],
["lockpick", 0x14FB, 25, 'tinker'],
["flour sifter", 0x103E, 27, 'tinker'],
["map maker's pen", 0x0FC0, 29, 'tinker'],  #'
["clippers", (0x0DFC, 0x0DFD), 506, 'tinker'],   #find which is crafted
["pitchfork", 0x0E88, 719, 'tinker'],
["jointing plane", 0x1030, 73, 'tinker'],
["moulding planes", 0x102C, 74, 'tinker'],
["smoothing plane", 0x1032, 75, 'tinker'],
["clock frame", 0x104D, 76, 'tinker'],
["axle", 0x105B, 77, 'tinker'],
["rolling pin", 0x1043, 78, 'tinker'],
["round paper lantern", 0x24CA, 61, 'tinker'],
["paper lantern", 0x24BE, 60, 'tinker'],
["shoji lantern", 0x24BC, 59, 'tinker'],
["nunchaku", 0x27AE, 7, 'tinker'],
["star sapphire necklace", 0x1088, 102, 'tinker'],
["emerald necklace", 0x1088, 108, 'tinker'],
["sapphire necklace", 0x1088, 114, 'tinker'],
["ruby necklace", 0x1088, 120, 'tinker'],
["citrines necklace", 0x1088, 126, 'tinker'],
["amethyst necklace", 0x1088, 132, 'tinker'],
["tourmaline necklace", 0x1088, 138, 'tinker'],
["amber necklace", 0x1088, 144, 'tinker'],
["diamond necklace", 0x1088, 150, 'tinker'],
["clumsy",0x1F2E,1, 'scribe'],################################################### scribe
["create food",0x1F2F,2, 'scribe'],
["feeblemind",0x1F30,3, 'scribe'],
["heal",0x1F31,4, 'scribe'],
["magic arrow",0x1F32,5, 'scribe'],
["night sight",0x1F33,6, 'scribe'],
["reactive armor",0x1F2D,7, 'scribe'],
["weaken",0x1F34,8, 'scribe'],
["agility",0x1F35,9, 'scribe'],
["cunning",0x1F36,10, 'scribe'],
["cure",0x1F37,11, 'scribe'],
["harm",0x1F38,12, 'scribe'],
["magic trap",0x1F39,13, 'scribe'],
["magic untrap",0x1F3A,14, 'scribe'],
["protection",0x1F3B,15, 'scribe'],
["strength",0x1F3C,16, 'scribe'],
["bless",0x1F3D,17, 'scribe'],
["fireball",0x1F3E,18, 'scribe'],
["magic lock",0x1F3F,19, 'scribe'],
["poison",0x1F40,20, 'scribe'],
["telekinesis",0x1F41,21, 'scribe'],
["teleport",0x1F42,22, 'scribe'],
["unlock",0x1F43,23, 'scribe'],
["wall of stone",0x1F44,24, 'scribe'],
["arch cure",0x1F45,25, 'scribe'],
["arch protection",0x1F46,26, 'scribe'],
["curse",0x1F47,27, 'scribe'],
["fire field",0x1F48,28, 'scribe'],
["greater heal",0x1F49,29, 'scribe'],
["lightning",0x1F4A,30, 'scribe'],
["mana drain",0x1F4B,31, 'scribe'],
["recall",0x1F4C,32, 'scribe'],
["blade spirits",0x1F4D,33, 'scribe'],
["dispel field",0x1F4E,34, 'scribe'],
["incognito",0x1F4F,35, 'scribe'],
["magic reflection",0x1F50,36, 'scribe'],
["mind blast",0x1F51,37, 'scribe'],
["paralyze",0x1F52,38, 'scribe'],
["poison field",0x1F53,39, 'scribe'],
["summon creature",0x1F54,40, 'scribe'],
["dispel",0x1F55,41, 'scribe'],
["energy bolt",42, 'scribe'],
["explosion",0x1F57,43, 'scribe'],
["invisibility",0x1F58,44, 'scribe'],
["mark",0x1F59,45, 'scribe'],
["mass curse",0x1F5A,46, 'scribe'],
["paralyze field",0x1F5B,47, 'scribe'],
["reveal",0x1F5C,48, 'scribe'],
["chain lightning",0x1F5D,49, 'scribe'],
["energy field",0x1F5E,50, 'scribe'],
["flamestrike",0x1F5F,51, 'scribe'],
["gate travel",0x1F60,52, 'scribe'],
["mana vampire",0x1F61,53, 'scribe'],
["mass dispel",0x1F62,54, 'scribe'],
["meteor swarm",0x1F63,55, 'scribe'],
["polymorph",0x1F64,56, 'scribe'],
["earthquake",0x1F65,57, 'scribe'],
["energy vortex",0x1F66,58, 'scribe'],
["resurrection",0x1F67,59, 'scribe'],
["summon air elemental",0x1F68,60, 'scribe'],
["summon daemon",0x1F69,61, 'scribe'],
["summon earth elemental",0x1F6A,62, 'scribe'],
["summon fire elemental",0x1F6B,63, 'scribe'],
["summon water elemental",0x1F6C,64, 'scribe'],
["animate dead",0x2260,101, 'scribe'],
["blood oath",0x2261,102, 'scribe'],
["corpse skin",0x2262,103, 'scribe'],
["curse weapon",0x2263,104, 'scribe'],
["evil omen",0x2264,105, 'scribe'],
["horrific beast",0x2265,106, 'scribe'],
["lich form",0x2266,107, 'scribe'],
["mind rot",0x2267,108, 'scribe'],
["pain spike",0x2268,109, 'scribe'],
["poison strike",0x2269,110, 'scribe'],
["strangle",0x226A,111, 'scribe'],
["summon familiar",0x226B,112, 'scribe'],
["vampiric embrace",0x226C,113, 'scribe'],
["vengeful spirit",0x226D,114, 'scribe'],
["wither",0x226E,115, 'scribe'],
["wraith form",0x226F,116, 'scribe'],
["exorcism",0x2270,117, 'scribe'],
["runebook",0x22C5,200, 'scribe'],
["bulk order book",0x2259,201, 'scribe'],
["spellbook",0x0EFA,202, 'scribe'],
["mysticism spellbook",0x2D9D,206, 'scribe'],
["necromancer spellbook",0x2253,207, 'scribe'],
["runic atlas",0x9C16,694, 'scribe'],
["spellbook engraving tool",0x0FBF,205, 'scribe'],
["bow",0x13B2,6,'bowcraft'],              ############################### archery
["heavy crossbow",0x13FD,8,'bowcraft'],
["composite bow",0x26C2,9,'bowcraft'],
["yumi",0x27A5,11,'bowcraft'],             
["magical shortbow",0x2D1F,13,'bowcraft'],
['crossbow',0x0F4F,7,'bowcraft'],
['kindling',0x0DE1,1,'bowcraft'],
['bokuto',0x27A8,121,'saw']
)

###################################################### SUIT FORM   #####################################################
class Content(System.IComparable, System.IConvertible):
    ID = 0
    name = ''
    lmc = ''
    lrc = ''
    physical = ''
    fire = ''
    cold = ''
    energy = ''
    poison = ''
    strength = ''
    dex = ''
    intel = ''
    hits = ''
    stam = ''
    mana = ''
    hci = ''
    dci = ''
    mr = ''
    sr = ''
    hpr= ''
    layer = ''
    luck = ''
    ssi = ''
    ep = ''
    fc = ''
    fcr = ''
    di = ''
    def __init__(self,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,aa):
        self.serial = a
        self.name = b
        self.lmc = c
        self.lrc = d
        self.hpr = e
        self.sr = f
        self.mr =g        
        self.hci =h
        self.dci = i
        self.ssi = j
        self.luck = k
        self.ep = l
        self.fc = m
        self.fcr = n
        self.di = o
        self.physical = p
        self.fire = q
        self.cold = r
        self.energy = s
        self.poison = t
        self.strength = u
        self.dex = v
        self.intel = w
        self.hits = x
        self.stam = y
        self.mana = z
        self.layer = aa


class suitBuilder(Form):
    CurVer = '1.0'
    ScriptName = 'Mourns Suit Builder'
    Contents = []     
    def __init__(self,contents):
        self.cont = None
        self.Contents = contents
        self.BackColor = Color.FromArgb(25,25,25)
        self.ForeColor = Color.FromArgb(231,231,231)
        self.Size = Size(1850, 450)
        self.Text = '{0} - v{1}'.format(self.ScriptName, self.CurVer)
        self.TopMost = True 
        self.DataGridSetup()
        
        self.btnGet = Button()
        self.btnGet.Text = 'Pull Item'
        self.btnGet.BackColor = Color.FromArgb(10,10,100)
        self.btnGet.Location = Point(330, 375)
        self.btnGet.Size = Size(100, 35)
        self.btnGet.FlatStyle = FlatStyle.Flat
        self.btnGet.FlatAppearance.BorderSize = 1
        self.btnGet.Click += self.btnGetPress
        
        self.btnStop = Button()
        self.btnStop.Text = 'Refresh Container Counts'
        self.btnStop.BackColor = Color.FromArgb(15,150,150)
        self.btnStop.Location = Point(170, 375)
        self.btnStop.Size = Size(150, 35)
        self.btnStop.FlatStyle = FlatStyle.Flat
        self.btnStop.FlatAppearance.BorderSize = 1
        self.btnStop.Click += self.btnRefreshPress
        
        self.btnCont = Button()
        self.btnCont.Text = 'Select Container'
        self.btnCont.BackColor = Color.FromArgb(10,150,10)
        self.btnCont.Location = Point(10, 375)
        self.btnCont.Size = Size(150, 35)
        self.btnCont.FlatStyle = FlatStyle.Flat
        self.btnCont.FlatAppearance.BorderSize = 1
        self.btnCont.Click += self.btnContPress
        
        self.btnSlot = Button()
        self.btnSlot.Text = 'Check Slots'
        self.btnSlot.BackColor = Color.FromArgb(10,10,100)
        self.btnSlot.Location = Point(440, 375)
        self.btnSlot.Size = Size(100, 35)
        self.btnSlot.FlatStyle = FlatStyle.Flat
        self.btnSlot.FlatAppearance.BorderSize = 1
        self.btnSlot.Click += self.btnSlotPress
        
        self.btnJewl = Button()
        self.btnJewl.Text = 'Eval Jewelery Box'
        self.btnJewl.BackColor = Color.FromArgb(10,10,100)
        self.btnJewl.Location = Point(540, 375)
        self.btnJewl.Size = Size(100, 35)
        self.btnJewl.FlatStyle = FlatStyle.Flat
        self.btnJewl.FlatAppearance.BorderSize = 1
        self.btnJewl.Click += self.btnSlotPress
                     
        self.Controls.Add(self.DataGrid)
        self.Controls.Add(self.btnGet)
        self.Controls.Add(self.btnStop)
        self.Controls.Add(self.btnCont)
        self.Controls.Add(self.btnSlot)
        self.Controls.Add(self.btnJewl)
    def DataGridSetup(self):
        self.DataGrid = DataGridView()
        self.DataGrid.RowHeadersVisible = False
        self.DataGrid.MultiSelect = False
        self.DataGrid.SelectionMode = DataGridViewSelectionMode.FullRowSelect
        self.DataGrid.BackgroundColor = Color.FromArgb(25,25,25)
        self.DataGrid.RowsDefaultCellStyle.BackColor = Color.Silver
        self.DataGrid.AlternatingRowsDefaultCellStyle.BackColor = Color.Gainsboro
        self.DataGrid.ForeColor = Color.FromArgb(25,25,25)
        self.DataGrid.Location = Point(12, 12)
        self.DataGrid.Size = Size(1810, 350)
        self.DataGrid.DataSource = self.Data()
        self.DataGrid.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.AllCells
        self.DataGrid.EditMode = DataGridViewEditMode.EditProgrammatically
        self.DataGrid.BorderStyle = BorderStyle.None 
        
    def Data(self):
        data = DataTable()
        data.Columns.Add('Serial', clr.GetClrType(str))
        data.Columns.Add('Name', clr.GetClrType(str))
        data.Columns.Add('LMC', clr.GetClrType(str))
        data.Columns.Add('LRC', clr.GetClrType(str))
        data.Columns.Add('HPR', clr.GetClrType(str))
        data.Columns.Add('SR', clr.GetClrType(str))
        data.Columns.Add('MR', clr.GetClrType(str))
        data.Columns.Add('HCI', clr.GetClrType(str))
        data.Columns.Add('DCI', clr.GetClrType(str))
        data.Columns.Add('SSI', clr.GetClrType(str))
        data.Columns.Add('Luck', clr.GetClrType(str))
        data.Columns.Add('EP', clr.GetClrType(str))
        data.Columns.Add('FC', clr.GetClrType(str))
        data.Columns.Add('FCR', clr.GetClrType(str))
        data.Columns.Add('DI', clr.GetClrType(str))
        data.Columns.Add('Physical', clr.GetClrType(str))
        data.Columns.Add('Fire', clr.GetClrType(str))
        data.Columns.Add('Cold', clr.GetClrType(str))
        data.Columns.Add('Poison', clr.GetClrType(str))
        data.Columns.Add('Energy',clr.GetClrType(str))
        data.Columns.Add('Str',clr.GetClrType(str))
        data.Columns.Add('Dex',clr.GetClrType(str))
        data.Columns.Add('Int',clr.GetClrType(str))
        data.Columns.Add('HP',clr.GetClrType(str))
        data.Columns.Add('Stam',clr.GetClrType(str))
        data.Columns.Add('Mana',clr.GetClrType(str))
        data.Columns.Add('Suit Layer',clr.GetClrType(str))
        for content in self.Contents:
            data.Rows.Add(hex(content.serial), content.name, content.lmc ,content.lrc,content.hpr,content.sr,content.mr,content.hci,content.dci,content.ssi,content.luck,content.ep,content.fc,content.fcr,content.di,content.physical,content.fire,content.cold,content.poison,content.energy,content.strength,content.dex,content.intel,content.hits,content.stam,content.mana,content.layer)
           
        return data
        
    def getColor(self):    
        for r in xrange(self.DataGrid.DataSource.Rows.Count): 
            row = self.DataGrid.DataSource.Rows[r]
            for d in range(14):
                quantity = self.DataGrid.Rows[r].Cells[d].Value
                if quantity.isdigit():
                    quantity = int(quantity)
                    Misc.SendMessage('{} {} is {}'.format(r,d,quantity))
                    if quantity > 0 and quantity <= 50:
                        Misc.SendMessage('{} {} is {} changing color {}'.format(r,d,quantity,'Yellow'))
                        self.DataGrid.Rows[r].Cells[d].Style.BackColor = Color.Yellow
                    if quantity > 50 and quantity <= 100:
                        Misc.SendMessage('{} {} is {} changing color {}'.format(r,d,quantity,'Green'))
                        self.DataGrid.Rows[r].Cells[d].Style.BackColor = Color.Green  
                        
    def DeleteRow(self, serial):####   Deletes Row if removed by the get button
        for r in xrange(self.DataGrid.DataSource.Rows.Count):
            row = self.DataGrid.DataSource.Rows[r]
            if row['Serial'] == serial:
                self.DataGrid.DataSource.Rows.Remove(row)
                return
                                
    def btnGetPress(self, sender, args):######## Pulls the item Selected in form to your bag and deletes row
        row = self.DataGrid.SelectedCells[0].RowIndex        
        if row == -1:
            Misc.SendMessage('{0}: No row selected.'.format(self.ScriptName), 33)
            return            
        col = self.DataGrid.SelectedCells[0].ColumnIndex
        serial = self.DataGrid.Rows[row].Cells[col].Value
        self.DeleteRow(serial)
        item = Items.FindBySerial(int(serial,0))
        Items.Move(item,Player.Backpack, 0)            
                
    def sz(self,var):######sets 0s in data grid to empty strings to be oooh so sexy
        if var == 0:
            var = ''
        return var  
        
    def getItemLayer(self,strName,itemID): #### defines item layer for suit building and idiot checks
        strName = strName.lower()
        layer = 'Unknown'
        helmetList = ['helm','hat','circlet','lenses','cap','glasses','kasa','hood','bandana','bascinet','coif','gargish earrings','headdress']
        tunicList = ['tunic','chest','armor','bustier']        
        armsList = ['arms','sleeves']
        legsList = ['legs','leggings','shorts','skirt','suneate']
        gorgetList= ['gorget','mempo','amulet']
        glovesList = ['gloves','mittens','gauntlets']
        shieldList = ['shield','hesph','buckler']
        ringIDList = [0x4212,0x1F09,0x108A]
        braceIDList = [0x1086,0x1F06,0x4211]
        taliIDList = [0x2F59,0x1096,0x2F5A,0x2F5B,0x2F58]
        robeIDList = [0x4002,0x2FB9,0x9985,0x2687,0x1F03,0x7816]
        bootIDList = [0x170B,0x170D,0x1712]
        sashIDList = [0x1541]
        waistIDList = [0x27A0,0x153B,0xA1F6]
        cloakIDList = [0x45A4,0x2309,0x1515,0x2B02]
        for l in helmetList:
            if l in strName:
                layer = "Helmet"
                return layer
        for l in tunicList:            
            if l in strName:
                layer = 'Tunic'
                return layer
        for l in armsList:            
            if l in strName:
                layer = 'Arms'
                return layer
        for l in legsList:            
            if l in strName:
                layer = 'Legs'
                return layer
        for l in gorgetList:            
            if l in strName:
                layer = 'Neck' 
                return layer
        for l in glovesList:            
            if l in strName:
                layer = 'Gloves'
                return layer
        for l in shieldList:
            if l in strName:
                layer = 'Shield'
                return layer
        if itemID in ringIDList:            
            layer = 'Ring'
            return layer
        elif itemID in braceIDList:
            layer = 'Bracelet'
            return layer
        elif itemID in taliIDList:
            layer = 'Talisman'
            return layer
        elif itemID in robeIDList:
            layer = "Robe"
            return layer
        elif itemID in bootIDList:
            layer = "Boots"
            return layer
        elif itemID in sashIDList:
            layer = "Sash"
            return layer
        elif itemID in waistIDList:
            layer = "Waist"
            return layer
        elif itemID in cloakIDList:
            layer = "Cloak"
            return layer
        if layer == 'Unknown':
            Misc.SendMessage('failed to find layer with {} string'.format(strName),48)
        return layer
                
    def btnSlotPress(self,s,e):###### checks container for armor slots that arent in bag or are doubled
        allLayersList = ['Helmet','Tunic','Arms','Legs','Neck','Gloves','Ring','Bracelet','Talisman','Robe','Boots','Sash','Waist','Cloak']
        yourLayerList = []
        if not self.cont:
            Misc.SendMessage('Select Container to Check Slots',80)
            self.cont = Items.FindBySerial(Target.PromptTarget(''))
        
        for i in self.cont.Contains:
            Items.WaitForProps(i,1000)
            layer = self.getItemLayer(Items.GetPropStringByIndex(i,0),i.ItemID)
            yourLayerList.append(layer)
        for yl in yourLayerList:
            if yourLayerList.count(yl) >1:
                Misc.SendMessage('Warning You have {} {} Pieces in your Suit Bag'.format(yourLayerList.count(yl),yl),30)
            if yl in allLayersList:
                allLayersList.remove(yl)
        Misc.SendMessage('You are Missing {} suit slots'.format(len(allLayersList)),48)
        if len(allLayersList) > 0:
            for a in allLayersList:
                Misc.SendMessage(a,48)              
        self.getColor()
        self.updateDataGrid() 
        
    def updateDataGrid(self):   #  Supplys the data for the spread sheet   
        contents.Clear()
        countlmc = 0
        countlrc= 0
        counthci = 0
        countdci = 0
        counthpr = 0
        countsr = 0
        countmr = 0
        countphysical = 0
        countfire = 0
        countcold =0
        countpoison = 0
        countenergy = 0
        countstrength = 0
        countdex = 0
        countintel = 0
        counthit = 0
        countstam = 0
        countmana = 0
        countluck = 0
        countssi = 0
        countep = 0
        countlayer = 0
        countfc = 0
        countfcr = 0
        countdi = 0
        if self.cont != None:
            for i in self.cont.Contains:                
                Items.WaitForProps(i, 8000)
                plist = Items.GetPropStringList(i)
                lmc = Items.GetPropValue(i,"Lower Mana Cost")
                if not "mage armor" in plist:
                    if "studded" in plist[0].lower() or 'bone' in plist[0].lower():
                        Misc.SendMessage("+3 lmc bone/studded no mage armor")
                        lmc += 3
                    elif 'plate' in plist[0].lower():
                        Misc.SendMessage("+1 lmc plate no mage armor")
                        lmc += 1                
                countlmc += lmc
                lrc = Items.GetPropValue(i,'Lower Reagent Cost')
                countlrc += lrc
                hci = Items.GetPropValue(i,'Hit Chance Increase')
                counthci += hci 
                dci= Items.GetPropValue(i,'Defense Chance Increase')
                countdci += dci
                hpr = Items.GetPropValue(i,'Hit Point Regeneration')
                counthpr += hpr
                sr = Items.GetPropValue(i,'Stamina Regeneration')
                countsr += sr
                mr = Items.GetPropValue(i,'Mana Regeneration')
                countmr += mr
                physical = Items.GetPropValue(i,'Physical Resist')
                countphysical += physical
                fire = int(Items.GetPropValue(i,'Fire Resist'))
                countfire += fire
                cold = Items.GetPropValue(i,'Cold Resist')
                countcold += cold
                poison = Items.GetPropValue(i,'Poison Resist')
                countpoison += poison
                energy = Items.GetPropValue(i,'Energy Resist')
                countenergy += energy
                strength = Items.GetPropValue(i,'Strength Bonus')
                countstrength += strength
                dex = Items.GetPropValue(i,'Dexterity Bonus')
                countdex += dex
                intel = Items.GetPropValue(i,'Intelligence Bonus')
                countintel += intel
                hit = Items.GetPropValue(i,'Hit Point Increase')
                counthit += hit
                stam = Items.GetPropValue(i,'Stamina Increase')
                countstam += stam
                mana = Items.GetPropValue(i,'Mana Increase') 
                countmana += mana
                luck = Items.GetPropValue(i,'Luck')
                countluck += luck
                ssi = Items.GetPropValue(i,'Swing Speed Increase')
                countssi += ssi
                ep = Items.GetPropValue(i,'Enhance Potions')
                countep += ep
                fc = Items.GetPropValue(i,'Faster Casting')
                countfc += fc
                fcr = Items.GetPropValue(i,'Faster Cast Recovery')
                countfcr += fcr
                di = Items.GetPropValue(i,'Damage Increase')
                countdi += di
                layer = self.getItemLayer(plist[0],i.ItemID)
                if layer != "Unknown":
                    countlayer += 1
                    contents.append(Content(i.Serial, plist[0], self.sz(lmc),self.sz(lrc),self.sz(hpr),self.sz(sr),self.sz(mr),self.sz(hci),self.sz(dci),self.sz(ssi),self.sz(luck),self.sz(ep),self.sz(fc),self.sz(fcr),self.sz(di),self.sz(physical),self.sz(fire),self.sz(cold),self.sz(poison),self.sz(energy),self.sz(strength),self.sz(dex),self.sz(intel),self.sz(hit),self.sz(stam),self.sz(mana),layer))
            contents.append(Content(0,'Totals',countlmc,countlrc,counthpr,countsr,countmr,counthci,countdci,countssi,countluck,countep,countfc,countfcr,countdi,countphysical,countfire,countcold,countpoison,countenergy,countstrength,countdex,countintel,counthit,countstam,countmana,countlayer))
            contents.append(Content(0,'Caps',55,100,18,24,30,45,45,60,2380,50,4,6,100,70,70,70,70,75,150,150,150,25,210,210," "))
            self.Contents = contents                            
            Misc.SendMessage("refreshing")
            self.DataGrid.DataSource = self.Data()
            self.DataGrid.Refresh()                
        else:
            Misc.SendMessage('No Container to Monitor')                
                     
    def btnContPress(self,s,a):##### Search container button pressed
        self.updateGrid = False 
        Misc.SendMessage('Target a container to eval suit.', 76)       
        contSer = Target.PromptTarget('')       
        self.cont = Items.FindBySerial(contSer)
        if self.cont:
            Items.UseItem(self.cont)
            Misc.Pause(1100)
            Items.WaitForContents(self.cont, 8000)
            Misc.Pause(500)
            self.updateDataGrid()              
        else:
            Misc.SendMessage('No container was targeted.', 33) 
    
    def btnRefreshPress(self,s,a):### recalculate bag button pressed
        self.updateDataGrid()
      

        ############################################################################  
###########################          MAIN FORM               ###########################
####################################################################################################### 
   
class itemMaker(Form):    
    list = []
    def __init__(self):
        self.Text = Player.Name
        self.Width = 500
        self.Height = 250
        self.BackColor = Color.FromArgb(25,25,25)
        self.ForeColor = Color.FromArgb(200,200,200)
        self.TopMost = True
        
        self.box = GroupBox()
        self.box.BackColor = Color.FromArgb(25,25,25)
        self.box.ForeColor = Color.FromArgb(23,221,23)
        self.box.Size = Size(195, 95)
        self.box.Location = Point(180, 5)
        self.box.Text = 'BOD Options'
        
        self.box2 = GroupBox()
        self.box2.BackColor = Color.FromArgb(25,25,25)
        self.box2.ForeColor = Color.FromArgb(23,221,23)
        self.box2.Size = Size(225, 43)
        self.box2.Location = Point(180, 160)
        self.box2.Text = 'Imbue Options'
        
        self.box3 = GroupBox()
        self.box3.BackColor = Color.FromArgb(25,25,25)
        self.box3.ForeColor = Color.FromArgb(23,221,23)
        self.box3.Size = Size(195, 165)
        self.box3.Location = Point(5, 5)
        self.box3.Text = 'Crafting Options'
        
        self.box4 = GroupBox()
        self.box4.BackColor = Color.FromArgb(25,25,25)
        self.box4.ForeColor = Color.FromArgb(23,221,23)
        self.box4.Size = Size(100, 200)
        self.box4.Location = Point(375,5)
        self.box4.Text = 'Scroll Options'
        
        self.button = Button()
        self.button.Text = 'Powder'
        self.button.Width = 85
        self.button.Height = 25
        self.button.BackColor = Color.FromArgb(0,0,0)
        self.button.ForeColor = Color.FromArgb(200,200,200)
        self.button.Location = Point(205, 105)
        self.button.Click += self.powder
        
        self.button1 = Button()
        self.button1.Text = 'Sort Book'
        self.button1.Width = 85
        self.button1.Height = 25
        self.button1.BackColor = Color.FromArgb(10,10,101)
        self.button1.ForeColor = Color.FromArgb(200,200,200)
        self.button1.Location = Point(190, 20)
        self.button1.Click += self.sortBtnPressed
        
        self.button2 = Button()
        self.button2.Text = 'Fill Book'
        self.button2.Width = 85
        self.button2.Height = 25
        self.button2.BackColor = Color.FromArgb(10,10,101)
        self.button2.ForeColor = Color.FromArgb(200,200,200)
        self.button2.Location = Point(280, 20)
        self.button2.Click += self.fillBook
        
        self.button3 = Button()
        self.button3.Text = 'Turn in for:'
        self.button3.Width = 85
        self.button3.Height = 25
        self.button3.BackColor = Color.FromArgb(10,10,101)
        self.button3.ForeColor = Color.FromArgb(200,200,200)
        self.button3.Location = Point(190, 47)
        self.button3.Click += self.TurnInBtnPress
        
        self.button4 = Button()
        self.button4.Text = 'Get BODs'
        self.button4.Width = 85
        self.button4.Height = 25
        self.button4.BackColor = Color.FromArgb(10,10,101)
        self.button4.ForeColor = Color.FromArgb(200,200,200)
        self.button4.Location = Point(190, 73)
        self.button4.Click += self.getBodBtnPress
                
        self.button5 = Button()
        self.button5.Text = 'Imbue Item'
        self.button5.Width = 70
        self.button5.Height = 25
        self.button5.BackColor = Color.FromArgb(10,10,101)
        self.button5.ForeColor = Color.FromArgb(200,200,200)
        self.button5.Location = Point(185, 175)
        self.button5.Click += self.imbueBtnPress
        
        self.button7 = Button()
        self.button7.Text = 'Start'
        self.button7.Width = 75
        self.button7.Height = 30
        self.button7.BackColor = Color.FromArgb(10,100,10)
        self.button7.ForeColor = Color.FromArgb(200,200,200)
        self.button7.Location = Point(10, 170)
        self.button7.Click += self.start
        
        self.button8 = Button()
        self.button8.Text = 'Stop'
        self.button8.Width = 75
        self.button8.Height = 30
        self.button8.BackColor = Color.FromArgb(100,10,10)
        self.button8.ForeColor = Color.FromArgb(200,200,200)
        self.button8.Location = Point(85, 170)
        self.button8.Click += self.stop
        
        self.button9 = Button()
        self.button9.Text = 'Open Suit Builder'
        self.button9.Width = 140
        self.button9.Height = 25
        self.button9.BackColor = Color.FromArgb(10,10,101)
        self.button9.ForeColor = Color.FromArgb(200,200,200)
        self.button9.Location = Point(20, 140)
        self.button9.Click += self.suitForm
        
        self.button10 = Button()
        self.button10.Text = 'Dump Book'
        self.button10.Width = 80
        self.button10.Height = 35
        self.button10.BackColor = Color.FromArgb(10,10,100)
        self.button10.ForeColor = Color.FromArgb(200,200,200)
        self.button10.Location = Point(385,20)
        self.button10.Click += self.dumpBtnPress
        
        self.button11 = Button()
        self.button11.Text = 'Sort Scrolls'
        self.button11.Width = 80
        self.button11.Height = 35
        self.button11.BackColor = Color.FromArgb(10,10,100)
        self.button11.ForeColor = Color.FromArgb(200,200,200)
        self.button11.Location = Point(385,55)
        self.button11.Click += self.sortScrollBtnPress 
        
        self.button12 = Button()
        self.button12.Text = 'Combine Pinks'
        self.button12.Width = 80
        self.button12.Height = 35
        self.button12.BackColor = Color.FromArgb(200,150,150)
        self.button12.ForeColor = Color.FromArgb(0,0,0)
        self.button12.Location = Point(385,90)
        self.button12.Click += self.combinePinkBtnPress
        
        self.button13 = Button()
        self.button13.Text = 'Combine PS'
        self.button13.Width = 80
        self.button13.Height = 35
        self.button13.BackColor = Color.FromArgb(250,250,250)
        self.button13.ForeColor = Color.FromArgb(0,0,0)
        self.button13.Location = Point(385,125)
        self.button13.Click += self.combinePSBtnPress
        
        self.button14 = Button()
        self.button14.Text = 'Reset Cont'
        self.button14.Width = 50
        self.button14.Height = 35
        self.button14.BackColor = Color.FromArgb(250,250,250)
        self.button14.ForeColor = Color.FromArgb(0,0,0)
        self.button14.Location = Point(410,165)
        self.button14.Click += self.resetCont
  
        self.textbox = TextBox()          
        self.textbox.Text = "25"             ############# DEFAULT ATTEMPT AMOUNT
        self.textbox.BackColor = Color.FromArgb(200,200,200)
        self.textbox.Location = Point(130, 35)
        self.textbox.Width = 30
        
        self.textbox2 = TextBox()
        self.textbox2.Text = "11"
        self.textbox2.BackColor = Color.FromArgb(200,200,200)
        self.textbox2.Location = Point(130, 75)
        self.textbox2.Width = 30
        
        self.rb = RadioButton()
        self.rb.Location = Point(65, 75)
        self.rb.Text = ">"
        self.rb.Checked = True
        self.rb.BackColor = Color.FromArgb(25,25,25)
        self.rb.Width = 30
        
        self.cb = ComboBox()
        self.cb.Location = Point(10, 115)
        self.cb.DataSource = "Off","Craft for Resist","Ele Dmg Wep","Luck",'100 Leach'
        self.cb.BackColor = Color.FromArgb(200,200,200)
        self.cb.Width = 100
        
        self.cb2 = CheckBox()
        self.cb2.Location = Point(115, 115)
        self.cb2.Text = "Excep"
        self.cb2.Checked = True 
        self.cb2.Width = 55
        
        self.rb2 = RadioButton()
        self.rb2.Location = Point(95, 75)
        self.rb2.Text = "<"
        self.rb2.BackColor = Color.FromArgb(25,25,25)
        self.rb2.Width = 30
        
        self.combobox = ComboBox()
        craftData = []
        for str in dataList:
            craftData.append(str[0])
        craftData = sorted(craftData) 
        self.combobox.DataSource = craftData
        self.combobox.BackColor = Color.FromArgb(200,200,200)
        self.combobox.Location = Point(10, 35)
        self.combobox.Width = 115
        
        self.combobox1 = ComboBox()
        self.combobox1.DataSource = "RecycleBank","POF","Shadow Hammer","Bowcraft Ash","Bowcraft Oak"
        self.combobox1.BackColor = Color.FromArgb(200,200,200)
        self.combobox1.Location = Point(280, 50)
        self.combobox1.Width = 80
        
        self.combobox2 = ComboBox()
        self.combobox2.DataSource = "Off","Fire","Physical","Cold",'Poison','Energy','Any Resist'
        self.combobox2.BackColor = Color.FromArgb(200,200,200)
        self.combobox2.Location = Point(10, 75)
        self.combobox2.Width = 50
        
        self.combobox4 = ComboBox()
        imbueData = []
        for str in imbueList:
            imbueData.append(str[0])
            self.combobox4.DataSource = imbueData
        self.combobox4.BackColor = Color.FromArgb(200,200,200)
        self.combobox4.Location = Point(260, 177)
        self.combobox4.Width = 135
        
        self.lb = Label()
        self.lb.Text = "Item to Craft"
        self.lb.Location = Point(10, 20)
        self.lb.Size = Size(80, 15)
        self.lb.BackColor = Color.FromArgb(25,25,25)
        self.lb.ForeColor = Color.FromArgb(120,120,223)
        
        self.lb2 = Label()
        self.lb2.Text = "Amount to Make"
        self.lb2.Location = Point(90, 20)
        self.lb2.Size = Size(90, 15)
        self.lb2.BackColor = Color.FromArgb(25,25,25)
        self.lb2.ForeColor = Color.FromArgb(120,120,223)
        
        self.lb3 = Label()
        self.lb3.Text = "Check Armor Resist"
        self.lb3.Location = Point(10,60)
        self.lb3.Size = Size(110, 15)
        self.lb3.BackColor = Color.FromArgb(25,25,25)
        self.lb3.ForeColor = Color.FromArgb(120,120,223)
        
        self.lb4 = Label()
        self.lb4.Text = "Resist"
        self.lb4.Location = Point(125, 60)
        self.lb4.Size = Size(50, 15)
        self.lb4.BackColor = Color.FromArgb(25,25,25)
        self.lb4.ForeColor = Color.FromArgb(120,120,223)
        
        self.lb5 = Label()
        self.lb5.Text = "Reforge Made Item"
        self.lb5.Location = Point(10, 100)
        self.lb5.Size = Size(110, 15)
        self.lb5.BackColor = Color.FromArgb(25,25,25)
        self.lb5.ForeColor = Color.FromArgb(120,120,223)

        self.lb6 = Label()
        self.lb6.Text = "Y/N"
        self.lb6.Location = Point(125, 100)
        self.lb6.Size = Size(50, 15)
        self.lb6.BackColor = Color.FromArgb(25,25,25)
        self.lb6.ForeColor = Color.FromArgb(120,120,223) 
        
        self.b = Button()
        self.b.Text = 'Move ID'
        self.b.Width = 85
        self.b.Height = 25
        self.b.BackColor = Color.FromArgb(0,0,0)
        self.b.ForeColor = Color.FromArgb(200,200,200)
        self.b.Location = Point(205, 130)
        self.b.Click += self.moveID
        
        self.b1 = Button()
        self.b1.Text = 'Salvage'
        self.b1.Width = 85
        self.b1.Height = 25
        self.b1.BackColor = Color.FromArgb(0,0,0)
        self.b1.ForeColor = Color.FromArgb(200,200,200)
        self.b1.Location = Point(290, 130)
        self.b1.Click += self.salvageUse
        
        self.b2 = Button()
        self.b2.Text = 'Clean Bag'
        self.b2.Width = 85
        self.b2.Height = 25
        self.b2.BackColor = Color.FromArgb(0,0,0)
        self.b2.ForeColor = Color.FromArgb(200,200,200)
        self.b2.Location = Point(290, 105)
        self.b2.Click += self.cleanBag
                
        self.Controls.Add(self.b) 
        self.Controls.Add(self.b1) 
        self.Controls.Add(self.b2)
        self.Controls.Add(self.lb)                
        self.Controls.Add(self.lb2)
        self.Controls.Add(self.lb3)                
        self.Controls.Add(self.lb4)
        self.Controls.Add(self.lb5) 
        self.Controls.Add(self.lb6)         
        self.Controls.Add(self.cb)
        self.Controls.Add(self.cb2)
        self.Controls.Add(self.rb)
        self.Controls.Add(self.rb2)
        self.Controls.Add(self.button)
        self.Controls.Add(self.button1)
        self.Controls.Add(self.button2)
        self.Controls.Add(self.button3)
        self.Controls.Add(self.button4)
        self.Controls.Add(self.button5)
        self.Controls.Add(self.button7)
        self.Controls.Add(self.button8)
        self.Controls.Add(self.button9)
        self.Controls.Add(self.button10)
        self.Controls.Add(self.button11)
        self.Controls.Add(self.button12)
        self.Controls.Add(self.button13)
        self.Controls.Add(self.button14)
        self.Controls.Add(self.textbox)
        self.Controls.Add(self.textbox2)
        self.Controls.Add(self.combobox)
        self.Controls.Add(self.combobox1)
        self.Controls.Add(self.combobox2)
        self.Controls.Add(self.combobox4)
        self.Controls.Add(self.box)
        self.Controls.Add(self.box2) 
        self.Controls.Add(self.box3)
        self.Controls.Add(self.box4)
#########################################################################################################        
    def salvageUse(self,s,a):
        self.salvBag = Items.FindByID(0x0E76,0x024e,Player.Backpack.Serial)
        if not self.salvBag:
            Player.HeadMessage(33,'You Need A Salvage Bag!!!!!')
            return
        Misc.WaitForContext(self.salvBag.Serial,2000)
        Misc.ContextReply(self.salvBag.Serial, 910)
        
    def dumpMats(self):
        dumpIDs = []
        for i in matIdList:
            ID = i[1]
            dumpIDs.append(ID)
        for item in Player.Backpack.Contains:
            if item.ItemID in dumpIDs:
                Items.Move(item,self.resCont.Serial,0)
                Misc.Pause(1200)
                                         
    def getMatGump(self,matType):
        matType = matType.lower()        
        if str(matType) == 'iron':
            gumpResponse  = 5000
        elif str(matType) == 'dull':
            gumpResponse  = 5001
        elif str(matType) == 'shadow':
            gumpResponse  = 5002 
        elif str(matType) == 'copper':
            gumpResponse  = 5003
        elif str(matType) == 'bronze':
            gumpResponse  = 5004
        elif str(matType) == 'gold':
            gumpResponse  = 5005    
        elif str(matType) == 'agapite':
            gumpResponse  = 5006
        elif str(matType) == 'verite':
            gumpResponse  = 5007
        elif str(matType) == 'valorite':
            gumpResponse  = 5008
        elif str(matType) == 'cloth':
            gumpResponse  = 5000    
        elif str(matType) == 'leather':
            gumpResponse  = 5000
        elif str(matType) == 'spined':
            gumpResponse  = 5001
        elif str(matType) == 'horned':
            gumpResponse  = 5002
        elif str(matType) == 'barbed':
            gumpResponse  = 5003
        elif str(matType) == 'wood':
            gumpResponse  = 5000
        elif str(matType) == 'oak':
            gumpResponse  = 5001
        elif str(matType) == 'ash':
            gumpResponse  = 5002
        elif str(matType) == 'yew':
            gumpResponse  = 5003
        elif str(matType) == 'heartwood':
            gumpResponse  = 5004
        elif str(matType) == 'bloodwood':
            gumpResponse  = 5005
        elif str(matType) == 'frostwood':
            gumpResponse  = 5006                                                            
        return int(gumpResponse) 
            
    def recycle(self,item,tool):################ chooses smelt or trash or cut up
        if tool == 'tongs':
            tongs = Items.FindByID(0x0FBC,0x0000,Player.Backpack.Serial)
            while Items.FindBySerial(item.Serial):
                Misc.SendMessage('smelting',30)
                Items.UseItem(tongs)
                Gumps.WaitForGump(460, 10000)
                Gumps.SendAction(460, 7000)
                Target.WaitForTarget(2000,False)
                Target.TargetExecute(item.Serial)
                Misc.Pause(1100)
        elif tool == 'sew':
            scissors = Items.FindByID(0x0F9E,0x0000,Player.Backpack.Serial)
            while Items.FindBySerial(item.Serial):
                Misc.SendMessage('recycling tailor',30)
                Items.UseItem(scissors)
                Target.WaitForTarget(2000,False)
                Target.TargetExecute(item.Serial)
                Misc.Pause(1200)
        elif tool == 'bowcraft' or tool == 'saw' or tool == 'tinker':
            garbagecans = Items.ApplyFilter(GFilter)
            Misc.Pause(100)
            garbagecan = Items.Select(garbagecans, 'Nearest')
            Misc.Pause(100)
            Items.Move(item,garbagecan,1)
            Misc.Pause(1100)
                            
    def totalItems(self):####   returns total items in backpack
        Items.WaitForProps(Player.Backpack,1000)
        propLine = Items.GetPropStringByIndex(Player.Backpack,2)
        s = propLine.split("/")[0]
        s2 = s.split(" ")[1] 
        return int(s2)    
            
    def countById(self,ID,hue):#### counts items in main bag by id and hue
        count = 0
        for item in Player.Backpack.Contains:
            if item.ItemID == ID:
                if item.Hue == hue:
                    count += 1
        return count
            
    def getIDandGump(self,str):  #####Returns list from dataList data of gump 460 craftables   
        for int in range(len(dataList)):
            x = dataList[int]
            if str == x[0]:            
                return x
            
    def findItem(self,id ,hue = -1, bagSer = Player.Backpack.Serial):###easy find by id with optional params
        item = Items.FindByID(id,hue,bagSer)
        return item        
                                      
    def checkRunic(self,runicTool):
        if Items.BackpackCount(runicTool.ItemID,runicTool.Hue) > 0:##############checks runic charges
            curCharges = Items.FindByID(runicTool.ItemID,runicTool.Hue,Player.Backpack.Serial)  
            Items.WaitForProps(curCharges,2000)
            props = Items.GetPropStringList(curCharges.Serial)
            Misc.Pause(500)
            prop = props[1].split(' ')[2]
            Misc.SendMessage('Runic tool has {} charges'.format(prop))
            if int(prop) < 10:
                if Items.FindByID(runicTool.ItemID,runicTool.Hue,self.resCont.Serial):
                    newTool = Items.FindByID(runicTool.ItemID,runicTool.Hue,self.resCont.Serial)
                    Misc.Pause(2000)
                    Items.Move(newTool,Player.Backpack.Serial,1)
                    Misc.Pause(2000)
                    Items.UseItem(curCharges)
                    Target.WaitForTarget(2000,False)
                    Target.TargetExecute(newTool)
                    Misc.Pause(1300)
                    return True
                else:
                    Misc.SendMessage("OUT OF {}".format(props[0]),48)
                    return False
                                         
        else:
            newTool = Items.FindByID(runicTool.ItemID,runicTool.Hue,self.resCont.Serial)
            Misc.Pause(2000)
            Items.Move(newTool,Player.Backpack.Serial,1)
            Misc.Pause(2000)
            return True

    def checkTool(self,tool):
        Misc.SendMessage('Checking {} tool'.format(tool),30)
        tinkerTool = Items.FindByID(0x1EB9,-1,Player.Backpack.Serial)
        if not tinkerTool:
            Misc.SendMessage("ERROR NO TINKER TOOL",48)
        if tool == 'tongs':
            toolGump = 20
            toolID = tongID
        elif tool == 'sew':
            toolGump = 14
            toolID = sewID         
        elif tool == 'saw':
            toolID = sawID
            toolGump = 15                      
        elif tool == 'bowcraft':
            toolID = bowcraftID
            toolGump = 28 
        elif tool == 'tinker':
            toolID = tinkerID
            toolGump = 11
        elif tool == 'scribe':
            toolID = scribeID
            toolGump = 30                
        if Items.BackpackCount(0x1BF2,0x0000) < 30:
            Misc.SendMessage('need ingots') 
            themat = Items.FindByID(0x1BF2,0x0000,self.resCont.Serial)
            if not themat:
                Misc.SendMessage("ERROR NO IRON INGOTS",48)
            Misc.Pause(2000)
            Items.Move(themat,Player.Backpack.Serial,50)
            Misc.Pause(2000)        
        tToolNum = Items.BackpackCount(0x1EB9,-1)  #####checks tinker tool      
        while tToolNum < 3:
            Items.UseItem(tinkerTool)
            Gumps.WaitForGump(460, 10000)
            Gumps.SendAction(460, 11)
            Misc.Pause(2000)
            tToolNum = Items.BackpackCount(0x1EB9,-1)
            Gumps.SendAction(460, 0) 
  
        toolNum = Items.BackpackCount(toolID,-1)  ##############CHECKS CRAFTING TOOL
        while toolNum < 2:
            Misc.Pause(1100)
            Items.UseItem(tinkerTool)
            Gumps.WaitForGump(460, 10000)
            Gumps.SendAction(460, toolGump)
            Misc.Pause(2000)
            toolNum = Items.BackpackCount(toolID,-1)
        Gumps.SendAction(460, 0)           

    def makeItem(self,itemID,gumpNum,toolID):
        craftingTool = Items.FindByID(toolID,0x0000,Player.Backpack.Serial)
        Journal.Clear()
        Items.UseItem(craftingTool)
        Gumps.WaitForGump(460, 2000)
        Gumps.SendAction(460, gumpNum)
        Misc.Pause(1200)
        
    def isExceptional(self,item): 
        list = Gumps.LastGumpGetLineList()
        line = Gumps.LastGumpGetLine(len(list)-4)
        Misc.SendMessage(line)
        if line:
            if line == "You create the item.":
                return False
            elif line == "You create an exceptional quality item and affix your maker's mark." or line == "You create an exceptional quality item.": #'
                return True                    
            elif line == "DO NOT COLOR":
                Misc.SendMessage('Nothing Made Yet',48)
                return None
            elif line == "You do not have sufficient metal to make that.":
                Misc.SendMessage('Out of Metal',48)
                return None
            elif line == "You must be near an anvil and a forge to smith items.":
                Misc.SendMessage('No Forge Nearby!!',48)
                return None
            elif line == "You failed to create the item, and some of youre materials are lost.":
                Misc.SendMessage('Failed to make')
                return None
            else:
                Misc.SendMessage('Unknown Gump 460 message',48)##### add failure debug messages for other craft skills 
                return None
        else:
            Misc.SendMessage("No Gump Found",48)
            return None
                       
    def isGoodReforge(self,item,tool):
        Items.WaitForProps(item,1000)
        if self.cb.Text == "Ele Dmg Wep":
            physical = Items.GetPropValue(item,'Physical Damage')
            fire = Items.GetPropValue(item,'Fire Damage')
            cold = Items.GetPropValue(item,'Cold Damage')
            poison = Items.GetPropValue(item,'Poison Damage')
            energy = Items.GetPropValue(item,'Energy Damage')
            if physical >= 50:
                return False                
            elif fire == 100:        
                return True
            elif cold == 100:        
                return True
            elif poison == 100:        
                return True
            elif energy == 100:        
                return True 
            else:
                return False                                          
            if tool == 'tongs':
                Misc.SendMessage('Evaluating metal Item')                       
                if physical >= 50:
                    return False                
                if fire == 100:        
                    return True
                elif cold == 100:        
                    return True
                elif poison == 100:        
                    return True
                elif energy == 100:        
                    return True
                if Player.GetSkillValue("Blacksmith") > 100:     
                    if fire >= 60:                       
                       self.enhance(item,'fire') 
                    elif cold >= 70:
                        self.enhance(item,'cold')
                    elif energy >= 80:
                        self.enhance(item,'energy')
                else:
                    return True
    
        elif self.cb.Text == "Luck":
            Misc.SendMessage('evaluating item for luck')
            if Items.GetPropValue(item,'Luck') < 150:             
                return False
            else:
                return True
                           
        elif self.cb.Text == "100 Leach":
            Items.WaitForProps(item,1000)
            list = Items.GetPropStringList(item)
            for l in list:
                if "leech" in l:
                    m = (l.split(' ')[3])
                    intAmount = int(m.split('%')[0])
                    if intAmount == 100:
                        return True
       
            return False
            
    def enhance(self,item,eleType):######### only implemented for BS  ele dmg enhanceables
        self.getMatsByStrName(eleType,100,20)
        if eleType == 'fire':
            ingotGump = 5004
        if eleType == 'cold':
            ingotGump = 5006
        if eleType == 'energy':
            ingotGump = 5007
        tongs = Items.FindByID(0x0FBC,-1,Player.Backpack.Serial)
        Items.UseItem(tongs)
        Gumps.WaitForGump(460, 10000)
        Gumps.SendAction(460, ingotGump)
        Gumps.WaitForGump(460, 10000)
        Gumps.SendAction(460, 2000)
        Target.WaitForTarget(2000,False)
        Target.TargetExecute(item)
        Misc.Pause(2000)
        Gumps.WaitForGump(460, 10000)
        gumplist = Gumps.LastGumpGetLineList()
        if len(gumplist) >= 73:
            gumpline = gumplist[73]
            Misc.SendMessage(gumpline,30)
            Misc.Pause(2000)
            newitem = Items.FindByID(item.ItemID,-1,Player.Backpack.Serial)
            if gumpline == "You enhance the item with the properties of the special material.":
                Misc.Pause(2000)
                Items.Move(newitem,self.stoCont.Serial,1)
                Misc.Pause(2000)
            if gumpline == "You attempt to enhance the item, but fail. Some material is lost in the process.":  
                Misc.Pause(2000)
                self.enhance(newitem,eleType)
        Gumps.WaitForGump(460, 10000)
        Gumps.SendAction(460, 5000)        
        Misc.Pause(2000)
        
    def checkResist(self,item):#checks single resist selected in drop box 
        Items.WaitForProps(item,2000)
        if self.combobox2.Text == 'Any Resist':
            resists = ['Fire','Cold','Poison','Energy']
            for resist in resists:
                amount = Items.GetPropValue(item.Serial,'{} Resist'.format(resist))
                if self.rb.Checked:  ##### radio button > checked          
                    if amount >= int(self.textbox2.Text):
                        Misc.SendMessage("{} {} is >= {}".format(self.combobox2.Text,amount,self.textbox2.Text),78)
                        return True
                        
                elif self.rb2.Checked:  ##### radio button < checked            
                    if amount <= int(self.textbox2.Text):
                        Misc.SendMessage("{} {} is <= {}".format(self.combobox2.Text,amount,self.textbox2.Text),78)
                        return True
            
            return False
            
        amount = Items.GetPropValue(item.Serial,'{} Resist'.format(self.combobox2.Text))
        if self.rb.Checked:  ##### radio button > checked          
            if amount >= int(self.textbox2.Text):
                Misc.SendMessage("{} {} is >= {}".format(self.combobox2.Text,amount,self.textbox2.Text),78)
                return True
            else:
                return False
                
        elif self.rb2.Checked:  ##### radio button < checked            
            if amount <= int(self.textbox2.Text):
                Misc.SendMessage("{} {} is <= {}".format(self.combobox2.Text,amount,self.textbox2.Text),78)
                return True
            else:
                return False
        else:
            Misc.SendMessage('resist check fail on {}'.format(item.Name),48)
            return False
                            
    def setReforgeGump(self):
        RL = [6,11,12,4]    ##############init gump set
        Misc.Pause(800)
        Gumps.WaitForGump(999086, 3000)
        gumpDataList = Gumps.LastGumpRawData()
        Misc.Pause(800)
        if '19378' in gumpDataList.split('xmfhtmlgumpcolor')[2]:
            Gumps.WaitForGump(999084, 10000)
            Gumps.SendAction(999084, 6)
            Misc.Pause(800)
        if '19378' in gumpDataList.split('xmfhtmlgumpcolor')[3]:
            Gumps.WaitForGump(999084, 10000)
            Gumps.SendAction(999084, 7)
            Misc.Pause(800)
        if '19378' in gumpDataList.split('xmfhtmlgumpcolor')[5]:
            Gumps.WaitForGump(999084, 10000)
            Gumps.SendAction(999084, 9) 
            Misc.Pause(800)
        if '19378' in gumpDataList.split('xmfhtmlgumpcolor')[7]:    
            Gumps.WaitForGump(999084, 2000)
            Gumps.SendAction(999084, 11)
            Misc.Pause(800)                                
        Misc.Pause(1000)
        for i in RL:                    
            Gumps.WaitForGump(999084, 3000)
            Gumps.SendAction(999084, i)                    
            Misc.Pause(800)
        if self.cb.Text == "Ele Dmg Wep":    
            Gumps.WaitForGump(999086, 3000)
            Gumps.SendAction(999086, 19)
        elif self.cb.Text == "Luck":
            Gumps.WaitForGump(999086, 3000)
            Gumps.SendAction(999086, 23)
        elif self.cb.Text == "100 Leach":                
            Gumps.WaitForGump(999086, 3000)
            Gumps.SendAction(999086, 20)
            
 ################################################## RESTOCKING FUNCTIONS ################################################           
 
    def getMatHue(self,type):
        type = type.lower()
        for m in matIdList:
            if type == m[0]:
                
                if len(m) ==3:
                    hue= m[2]
                else:              
                    hue = -1 
        Misc.SendMessage('{} hue is {}'.format(type,hue))            
        return hue    
                
    def getMatsByStrName(self,strName,buildTo,stockAbove):
        strName = strName.lower()     
        returnList = []
        if Items.BackpackCount(0x1BF2,0x0000) < 50:########always stocks iron ingots
            Items.WaitForContents(self.resCont.Serial,2000)
            Misc.Pause(1500)
            ironIngots = Items.FindByID(0x1BF2,0x0000,self.resCont.Serial)
            if not ironIngots:
                Misc.SendMessage('ERROR NO IRON INGOTS',48)
            Items.Move(ironIngots,Player.Backpack,200)
            Misc.Pause(1500)       
        for m in matIdList:
            if strName == m[0]:
                Misc.SendMessage(m[0])
                if len(m) ==3:
                    returnList.append('{},{}'.format(m[1],m[2]))
                else:              
                    returnList.append(str(m[1]))
        for l in returnList:
            if not ',' in l:
                matID = int(l)
                matHue = -1
            elif "," in l:
                m = l.split(',')
                matID = int(m[0])
                matHue = int(m[1])
            mat = Items.FindByID(matID,matHue,self.resCont.Serial)
            currentAmount = Items.BackpackCount(matID,matHue)
            Misc.SendMessage('i have {} in backpack'.format(currentAmount))
            if currentAmount < stockAbove:
                
                if not mat:
                    Misc.SendMessage('MAT NOT FOUND IN CHEST',48)
                
                else:   
                    Items.Move(mat.Serial,Player.Backpack.Serial,buildTo - currentAmount)
                    Misc.SendMessage('stocking {} {}'.format(buildTo - currentAmount,mat.Name))
                    Misc.Pause(1200)
 
    def getMatsFromCraftingGump(self,toolID,gump):    
        infoGump = gump +1000
        returnList = []
        nameList = []
        tool = Items.FindByID(toolID,0,Player.Backpack.Serial)
        Items.UseItem(tool)
        Gumps.WaitForGump(460,5000)
        Gumps.SendAction(460, infoGump)
        Gumps.WaitForGump(685,3000) 
        if Gumps.CurrentGump() != 685:
            Misc.SendMessage('No Gump Found',48)
            return None
        num = 8
        while num < len(Gumps.LastGumpGetLineList()):
            list = Gumps.LastGumpGetLine(num)
            if 'MAKE' in list or 'High Seas' in list or 'Stygian Abyss' in list or 'MAKE MAX' in list:
                break
            if list != "~1_val~" and not 'retains' in list and not 'recipe' in list and list != 'Tailoring' and list != 'Tinkering' and not 'Fletching' in list:
                nameList.append(list.lower())
                #Misc.SendMessage('{} {}'.format(num,list),48)
            num += 1
        Gumps.WaitForGump(685, 1000)
        Gumps.SendAction(685, 0) 
        Misc.Pause(1100)
        return nameList

                
######################################################  buttons   ################################################            
                
    def start(self,s,a): ########################### start button crafts left side of gui options
        global reforgeSet
        Gumps.SendAction(460,0)
        self.salvBag = Items.FindByID(0x0E76,0x024e,Player.Backpack.Serial)
        if not self.salvBag:
            Player.HeadMessage(33,'You Need A Salvage Bag!!!!!')
        if not Misc.ReadSharedValue('resCont'):
            Player.HeadMessage(70,'Target Resource Container')
            Misc.SetSharedValue('resCont',Target.PromptTarget(''))
        self.resCont = Items.FindBySerial(Misc.ReadSharedValue('resCont'))        
#        if not Misc.ReadSharedValue('stoCont'):
#            Player.HeadMessage(70,'Target Keeper Container')
#            Misc.SetSharedValue('stoCont',Target.PromptTarget(''))
#            self.stoCont = Items.FindBySerial(Misc.ReadSharedValue('stoCont'))
#        Misc.SendMessage('Target Storage Container',78)
#        self.resCont = Items.FindBySerial(Target.PromptTarget(' '))
        Misc.SendMessage('Target Keeper Container',78)
        self.stoCont = Items.FindBySerial(Target.PromptTarget(' '))
        Items.UseItem(self.resCont)
        Misc.Pause(1200)
        Items.WaitForContents(self.resCont,2000)
        Misc.Pause(1100)
        
        data = self.getIDandGump(self.combobox.Text)            
        id = data[1]
        gump = data[2]
        tool = data[3]
        if tool == 'tongs':
            toolID = tongID
            runicID = 0x13E3
        elif tool == "sew":
            toolID = 0x0F9D
            runicID = 0x0F9D
        elif tool == 'saw':
            toolID = sawID
            runicID = 0x1029
        elif tool == 'bowcraft':
            toolID = bowcraftID
            runicID = 0x1022
        elif tool == "tinker":
            toolID = tinkerID
        elif tool == 'scribe':
            toolID = scribeID
        self.checkTool(tool) 
        Misc.SetSharedValue("Run",True)
        if self.cb.Text != 'Off': 
            if self.cb.Text == "Ele Dmg Wep":
                if tool == "tongs":                    
                    runicHue = 0x0966              ##### shadow hammer
                elif tool == 'saw':                    
                    runicHue = 0x04A7               ####ash dovetail saw
                elif tool == 'bowcraft':                      
                    runicHue = 0x07DA              ### oak fletching kit
            if self.cb.Text == "Luck":
                if tool == "tongs":
                    runicHue = 0x096d              # copper hammer???????
                elif tool == 'saw':
                    runicHue = 0x07DA             ### oak
                elif tool == 'bowcraft':
                    runicHue = 0x07DA              ###oak
                elif tool == 'sew':                    
                    runicHue = 0x0845             ## horned kit  
            if self.cb.Text == "100 Leach":
                if tool == "tongs":
                    runicHue = 0x096d             # copper hammer???????
                elif tool == 'saw':
                    runicHue = 0x04A7             ### ash
                elif tool == 'bowcraft':
                    runicHue = 0x04A7               ### ash
            rTool = Items.FindByID(runicID,runicHue,Player.Backpack.Serial) 
            if not rTool:
                rTool = Items.FindByID(runicID,runicHue,self.resCont.Serial)
                Items.Move(rTool,Player.Backpack,1)
                Misc.Pause(1200)
        else:
            rTool = 0
            
                   
        matsList = self.getMatsFromCraftingGump(toolID,gump)### get mat list from 460 gump
        for m in matsList:
            self.getMatsByStrName(m,100,20)
        made = 0
        tomake = int(self.textbox.Text)

        while made < tomake:
            for i in Player.Backpack.Contains:
                if i.ItemID == id:
                    Misc.SendMessage("ERROR CLEANING ITEMS OF SAME ID FROM YOUR BAG",48)
                    Items.Move(i,self.stoCont.Serial,1)
                    Misc.Pause(1100)
            self.checkTool(tool)
            Misc.SendMessage('Making {} {}/{}'.format(self.combobox.Text,made,tomake),78)
            for m in matsList:
                self.getMatsByStrName(m,100,20)            
            self.makeItem(id,gump,toolID)
            Misc.Pause(1500)
            theItem = Items.FindByID(id,-1,Player.Backpack.Serial)
            Items.WaitForProps(theItem,200)
            if theItem:                
                if self.cb2.Checked:                               
                    if self.isExceptional(theItem) == False:
                        Misc.SendMessage('Only Keeping Exceptional, recycling')
                        self.recycle(theItem,tool)
                elif self.isExceptional(theItem) == True:
                    Misc.SendMessage("Only Keeping Non Exceptional, recycling")
                    self.recycle(theItem,tool)
                elif self.isExceptional(theItem) == None:
                    continue    
                if self.combobox2.Text != "Off": # IF CRAFT RESISTS Selected
                    Misc.SendMessage('checking resist')
                    if self.checkResist(theItem) == False:
                        self.recycle(theItem,tool)
                                      
                if self.cb.Text != 'Off':  ################ IF reforge selected
                    item = Items.FindBySerial(theItem.Serial) 
                    if item:
                        self.checkRunic(rTool)
                        Misc.Pause(1500)
                        Items.UseItem(rTool.Serial)
                        Target.WaitForTarget(2000)        
                        Target.TargetExecute(item)                        
                        if reforgeSet == False:
                            self.setReforgeGump()
                            reforgeSet = True
                        Gumps.WaitForGump(999084, 10000)
                        Gumps.SendAction(999084, 2) 
                        Misc.Pause(1100)
                        if self.isGoodReforge(item,tool):
                            Misc.SendMessage('Reforge Check Good',78)
                        else:
                            Misc.SendMessage('Reforge Prop Fail',48)
                            self.recycle(item,tool)                       
                Misc.Pause(500)            
                item = Items.FindBySerial(theItem.Serial)
                if item:
                    Misc.Pause(500)
                    for i in Player.Backpack.Contains:
                        if i.Serial == item.Serial:
                            Misc.SendMessage('Item Craft Success',78)
                            Items.Move(item,self.stoCont.Serial,1)
                            Misc.Pause(1500)
                            made += 1
                        
        Misc.SendMessage("Finished Crafting",78)
        Misc.Pause(1200)
        reforgeSet = False
        
    def resetCont(self,s,a):
        Misc.SendMessage('Select New Resource Container',78)
        Misc.SetSharedValue('resCont',Target.PromptTarget(''))
        self.resCont = Items.FindBySerial(int(Misc.ReadSharedValue('resCont')))
        
    def suitForm(self, sender, event):  #####main form suit button pressed              
        newform = suitBuilder(contents)  # suit builder form
        Form.ShowDialog(newform) 
        
    def cleanBag(self,s,a):
        if not Misc.ReadSharedValue('resCont'):
            Player.HeadMessage(70,'Target Resource Container')
            Misc.SetSharedValue('resCont',Target.PromptTarget(''))
        self.resCont = Items.FindBySerial(Misc.ReadSharedValue('resCont'))
        self.dumpMats()
                
    def powder(self,s,a):
        Player.HeadMessage(70,'Target Powder')
        pow = Items.FindBySerial(Target.PromptTarget(''))
        Player.HeadMessage(70,'Target Item')
        item = Items.FindBySerial(Target.PromptTarget(''))  
        for r in range(25):
            if self.getDurability(item) == 255:
                Misc.SendMessage('Item Is Full Durability',78)
                break
            Items.UseItem(pow)
            Target.WaitForTarget(1000)
            Target.TargetExecute(item)
            
            Misc.Pause(1500)
            
    def moveID(self,s,a):            
        x = 45
        y = 65        
        item = Items.FindBySerial(Target.PromptTarget('Choose type'))
        container = Items.FindBySerial(item.Container)
        dest = Target.PromptTarget('Choose Destination') 
        for items in container.Contains:
            if items.ItemID == item.ItemID:
                Items.Move(items,dest,1,x,y)
                x +=3
                if x > 140:
                    x = 45
                    y += 20
                Misc.Pause(1100)
                               
    def stop(self,s,a):########################not implemented until finished
        Misc.SendMessage("Stopping",33)
        Misc.SetSharedValue("Run",False) 
        Misc.ScriptStopAll()

        
###########################################################################################################               
#####################################################   BODS   ##################################
################################################################################################
 
    def getBodBtnPress(self,s,a):
        def findrunicatlas():
            atlas = 0
            Items.WaitForContents(Player.Backpack,2000)
            for item in Player.Backpack.Contains:
                if item.ItemID == 0x9C16:
                    Items.WaitForProps(item,1000)
                    atlasz = len(Items.GetPropStringList(item)) - 1
                    atlasname = Items.GetPropStringByIndex(item,atlasz)
                    if atlasname == "Main":
                        atlas = item.Serial
                        break
            return atlas
            
        
        def findbodbook():
            booktodropin = 0
            Items.WaitForContents(Player.Backpack,2000)
            for item in Player.Backpack.Contains:
                if item.ItemID == 0x2259:
                    Items.WaitForProps(item,1000)
                    baz = len(Items.GetPropStringList(item)) - 1 
                    if "Deeds" in Items.GetPropStringByIndex(item,baz):  
                        boda = Items.GetPropStringByIndex(item,baz).split(':')[1]
                        if int(boda) < 470:
                            booktodropin = item.Serial
                            break
                    else:  
                        booktodropin = item.Serial 
                        break   
                    
            return booktodropin
    
        def dragbodstobook(bodbook):
            Misc.Pause(1100)
            Items.WaitForContents(Player.Backpack,2000)
            Misc.Pause(1100)
            for item in Player.Backpack.Contains:
                if item.ItemID == 0x2258:
                    Items.WaitForProps(item,1000)
                    Items.Move(item,bodbook,1)
                    Misc.Pause(1100)
                    
        def recallfromatlas(atlasid, runenumber, attempts = 0):
            Journal.Clear()
            runechoice = 49999 + runenumber
            Misc.Pause(1500)
            Items.UseItem(atlasid)
            Gumps.WaitForGump(498, 10000)
            Misc.Pause(200)
            Gumps.SendAction(498, runechoice)  
            Gumps.WaitForGump(498, 10000)
            Gumps.SendAction(498, 4000)
            Misc.Pause(3500)
            if Journal.Search("fizzle"):
                attempts = attempts + 1
                if attempts <= 5:
                    recallfromatlas(atlasid, runenumber, attempts) 
            
        theatlas = findrunicatlas()
        if theatlas != 0:
            recallfromatlas(theatlas, 1)
        npcSerials = []
        leftCoords = [[985, 519, -50],[992,519,-50]]
        
        Misc.SendMessage('looking for npcs')      
        fil = Mobiles.Filter()
        fil.Notorieties = List[Byte](bytes([7]))
        fil.Enabled = True
        npcSuffix = ['blacksmith','tailor','bowyer','carpenter']
        NPCS = Mobiles.ApplyFilter(fil)
        for npc in NPCS:            
            for name in npcSuffix:                
                Mobiles.WaitForProps(npc,100)
                if name in Mobiles.GetPropStringByIndex(npc,0) and "guild" not in Mobiles.GetPropStringByIndex(npc,0):
                    npcSuffix.remove(name)
                    npcSerials.append(npc.Serial)
        Misc.SendMessage('done looking')
        Misc.SendMessage(len(npcSerials))
        if len(npcSerials) > 0:
            for s in npcSerials:
                for r in range(3):        
                    Misc.WaitForContext(s, 500)
                    Misc.ContextReply(s, 403)
                    Gumps.WaitForGump(455, 500)
                    Gumps.SendAction(455, 1)
        else:
            Misc.SendMessage('No NPCs Found',48)
 
        bodbookexists = findbodbook()            
        if bodbookexists != 0:
            dragbodstobook(bodbookexists)
        if theatlas != 0:
            recallfromatlas(theatlas, 2)
            r = 0
            while r <= 5:
                Player.Walk("North")
                r = r + 1
            Misc.Resync()

                

    
    def evalBod(self,bod):
        bodsize = Items.GetPropStringByIndex(bod,3).split(' ')[0]
        bodexceptional = Items.GetPropStringByIndex(bod,5)
        if 'iron' in Items.GetPropStringByIndex(bod,4) and not 'shadow' in Items.GetPropStringByIndex(bod,4):
            bodmat = 'iron'
        elif 'cloth' in Items.GetPropStringByIndex(bod,4):
            bodmat = 'cloth'
        elif bod.Hue == 0x044E:###BS STRING IS "all items must be made with X ingots"
            bodmat = Items.GetPropStringByIndex(bod,4).split(' ')[6]
        elif bod.Hue == 0x058D: ### bowcraft bod string is easy
            bodmat = Items.GetPropStringByIndex(bod,4) 
        bodamount = Items.GetPropStringByIndex(bod,6).split(' ')[3]
        stritem = Items.GetPropStringByIndex(bod,7).split(':')[0]
        itemsindeed = Items.GetPropStringByIndex(bod,7).split(':')[1]
            
        return stritem,bodsize,bodexceptional,bodmat,bodamount,itemsindeed 
            
    def findBooks(self):             ####################sets all bod books as global items
        BFilter = Items.Filter()
        BFilter.RangeMax = 5  
        BFilter.Graphics = List[int]([0x2259])
        global ironBook, recycleBook, pofBook, hammerBook, highBook, largeBook,bowcraftrecycle,bowcraftashkit,bowcraftoakkit######### make books global items
        books = Items.ApplyFilter(BFilter)
        col = 10
        for book in books:
            Misc.Pause(100)
            bookNameList = Items.GetPropStringByIndex(book,5).split(':')# parses str name of book after bookname:
            Misc.Pause(110)
            col += 15
            name = bookNameList[1]
            Items.Message(book,col,name)
            Misc.Pause(100)
            if name == ' SmithIron':
                ironBook = book
            elif name == ' SmithRecycle':
                recycleBook = book        
            elif name == ' SmithPOF':
                pofBook = book
            elif name == ' SmithShadowHammer':
                hammerBook = book
            elif name == ' SmithHigh':
                highBook = book
            elif name == ' SmithLarge':
                largeBook = book
            elif name == ' BowcraftRecycle':
                bowcraftrecycle = book
            elif name == ' BowcraftAshKit':
                bowcraftashkit = book
            elif name == ' BowcraftOakKit':
                bowcraftoakkit = book
                
    def sortBook(self,toSortBook):
        garbageList = ["frozen longbow","ranger's shortbow","mystical shortbow","slayer longbow","assassin's shortbow","barbed longbow","longbow of might"]#
        garbagecans = Items.ApplyFilter(GFilter)
        if not garbagecans:
            Misc.SendMessage('Error No Garbage Found',48)
        Misc.Pause(100)
        garbagecan = Items.Select(garbagecans, 'Nearest')
        Items.UseItem(toSortBook)
        Misc.Pause(2000)
        Gumps.WaitForGump(668, 5000)
        Gumps.SendAction(668, 4)
        Misc.Pause(1500)
        bod = Items.FindByID(0x2258,-1,Player.Backpack.Serial)
        if bod:
            if bod.Hue == 0x044E:
                tool = 'tongs'
            elif bod.Hue == 0x0455:
                tool = 'tinker'
            elif bod.Hue == 0x0483:
                tool = 'kit'
            elif bod.Hue == 0x058D:
                tool = 'bowcraft'
                        
            eb = self.evalBod(bod)
            name = eb[0]
            size = eb[1]
            exc = eb[2]
            mat = eb[3].lower()
            amount = int(eb[4])
            Misc.SendMessage('{} {} {} {} {} {}'.format(tool,size,exc,mat,amount,name),80)
            if name in garbageList:
                Items.Move(bod,garbagecan,1)  #### garbage
                Misc.SendMessage("{} name in Garbage List".format(name))
                return
            if tool == 'tongs':
                if size == 'large':
                    Items.Move(bod,largeBook,1)
                    Misc.SendMessage('large book')
                else:
                    if mat == 'iron':
                        Items.Move(bod,ironBook,1)
                        Misc.SendMessage('iron book')
                    elif mat == 'dull' or mat == 'shadow':
                        if exc == 'normal':
                            Items.Move(bod,recycleBook,1)
                            Misc.SendMessage('recycle book')
                        elif mat == 'dull' and amount != 20:
                            Items.Move(bod,recycleBook,1) 
                        else:
                            Items.Move(bod,pofBook,1)
                            Misc.SendMessage('pof book')
                    elif mat == 'copper':
                        if exc == 'normal':
                            Items.Move(bod,recycleBook,1)
                            Misc.SendMessage('recycle book')
                        else:
                            if int(amount) == 20:
                                Items.Move(bod,hammerBook,1)
                                Misc.SendMessage('hammer book')
                            else:    
                                Items.Move(bod,pofBook,1)
                                Misc.SendMessage('pof book')
                    elif mat == 'bronze':
                        if exc == 'normal':
                            Items.Move(bod,recycleBook,1)
                            Misc.SendMessage('recycle book')
                        else:
                            Items.Move(bod,hammerBook,1)
                            Misc.SendMessage('hammer book')                        
                    elif mat == 'gold':
                        if exc == 'normal':
                            if int(amount) == 20:
                                Items.Move(bod,pofBook,1)
                                Misc.SendMessage('pof book')
                            else:    
                                Items.Move(bod,recycleBook,1)
                                Misc.SendMessage('recycle book')
                        else:
                            Items.Move(bod,hammerBook,1)
                            Misc.SendMessage('hammer book')
                    elif mat == 'agapite':
                        if exc == 'normal':
                            Items.Move(bod,pofBook,1)
                            Misc.SendMessage('pof book')
                        else:
                            Items.Move(bod,hammerBook,1)
                            Misc.SendMessage('hammer book')
                    else:
                        Items.Move(bod,highBook,1)
                        Misc.SendMessage('high book')
                        
            if tool == 'bowcraft':            
                if size == 'large':
                    Items.Move(bod,garbagecan,1)  #### garbage
                    Misc.SendMessage("trashing large bowcraft bods")
                elif mat == 'wood' or mat == 'oak':
                    Items.Move(bod,bowcraftrecycle,1) 
                    Misc.SendMessage("bowcraft recycle book")
                elif mat == 'ash':
                    if exc == 'normal':
                        Items.Move(bod,bowcraftrecycle,1) 
                        Misc.SendMessage("bowcraft recycle book")
                    else:
                        Items.Move(bod,bowcraftoakkit,1) 
                        Misc.SendMessage("bowcraft Oak kit book")   
                elif mat == 'yew':
                    if int(amount) == 20 and exc != 'normal':
                        Items.Move(bod,bowcraftashkit,1) 
                        Misc.SendMessage("bowcraft Ash kit book")
                    else:
                        Items.Move(bod,bowcraftoakkit,1) 
                        Misc.SendMessage("bowcraft Oak kit book")
                elif mat == 'heartwood' or mat == 'bloodwood':
                    if exc == 'normal':
                        Items.Move(bod,bowcraftoakkit,1) 
                        Misc.SendMessage("bowcraft Oak kit book")
                    else:
                        Items.Move(bod,bowcraftashkit,1) 
                        Misc.SendMessage("bowcraft Ash kit book")        
                elif mat == 'frostwood':############################worth filling?
                    if exc == 'normal':
                        Items.Move(bod,bowcraftoakkit,1) 
                        Misc.SendMessage("bowcraft Oak kit book")
                    else:
                        Items.Move(bod,bowcraftashkit,1) 
                        Misc.SendMessage("bowcraft Ash kit book")                                     
        Misc.Pause(1500)
            
    def sortBtnPressed(self,s,a):
        Misc.Resync()
        Misc.SendMessage('Target Book to Sort',78)
        toSortBook = Items.FindBySerial(Target.PromptTarget(' '))        
        self.findBooks()
        deedCount = int(Items.GetPropStringByIndex(toSortBook,len(Items.GetPropStringList(toSortBook))-2).split(':')[1])
        for num in range(deedCount):
            Misc.SendMessage('Sorting {} of {} deeds'.format(num,deedCount))
            self.sortBook(toSortBook)
                 
    def fillBook(self,s,a):         
        if not Misc.ReadSharedValue('resCont'):
            Player.HeadMessage(70,'Target Resource Container')
            Misc.SetSharedValue('resCont',Target.PromptTarget(''))
        self.resCont = Items.FindBySerial(Misc.ReadSharedValue('resCont'))
        Misc.SendMessage('Target Book to Fill Deeds From',78)
        toFillBook = Items.FindBySerial(Target.PromptTarget(' '))
        Misc.SendMessage('Target Book to Put Full Deeds ',88)
        storeBook = Items.FindBySerial(Target.PromptTarget(' '))
        Items.WaitForProps(toFillBook,2000)
        deedCount = int(Items.GetPropStringByIndex(toFillBook,len(Items.GetPropStringList(toFillBook))-2).split(':')[1])
        Items.UseItem(self.resCont)
        Misc.Pause(1100)
        self.dumpMats()
        for num in range(deedCount):

            Items.UseItem(toFillBook)
            Gumps.WaitForGump(668, 5000)
            Gumps.SendAction(668, 4)
            Misc.Pause(2000)          ########  timer to assure bod is out of book
            Gumps.SendAction(668, 0)            
            bod = Items.FindByID(0x2258,-1,Player.Backpack.Serial)
            if bod:
                if bod.Hue == 0x044E:
                    tool = 'tongs'
                if bod.Hue == 0x0455:
                    tool = 'tinker'
                if bod.Hue == 0x0483:
                    tool = 'kit'
                if bod.Hue == 0x058D:
                    tool = 'bowcraft'
                eb = self.evalBod(bod)
                name = eb[0]
                size = eb[1]
                exc = eb[2]
                inDeed = int(eb[5])
                if name in canFail:
                    excBool = True
                    Misc.SendMessage('Failable Item',48)
                elif exc == 'normal':
                    excBool = 'All'
                elif tool == 'bowcraft' and exc != 'normal':
                    excBool = True
                else:
                    excBool = 'All'
                mat = eb[3]
                amount = int(eb[4])
                Misc.SendMessage('{} {} {} {}/{} {}'.format(size,exc,mat,inDeed,amount,name))
                if size == 'large':
                    Misc.SendMessage('Filling Large BODs Not Implemented',48)
                    Items.Move(bod,toFillBook,1)
                    Misc.Pause(1300)
                else:
                    Items.WaitForProps(bod,2000)
                    nameIdGump = self.getIDandGump(name)
                    checkListCount = 0
                    while nameIdGump == None: 
                        bod = Items.FindByID(0x2258,-1,Player.Backpack.Serial)                                            
                        nameIdGump = self.getIDandGump(name)
                        Misc.SendMessage('Looking for ID GUMP')      
                        Misc.Pause(1000)
                        if checkListCount > 2:
                            Misc.SendMessage('ERROR str name "{}" not correct in GUMP DATA'.format(name),48)
                        checkListCount += 1 
                    Misc.Pause(500)
                    itemID = nameIdGump[1]
                    gump = nameIdGump[2]
                    self.checkTool(tool)
                    
                    if tool == 'tongs':
                        toolID = tongID
                        tongs = Items.FindByID(0x0FBC,0x0000,Player.Backpack.Serial)
                        Items.UseItem(tongs)
                    elif tool == 'tinker':
                        toolID = tinkerID
                        ttool = Items.FindByID(0x1EB9,0x0000,Player.Backpack.Serial)
                        Items.UseItem(ttool)
                    elif tool == 'kit':
                        toolID = sewID
                        kit = Items.FindByID(sewID,0x0000,Player.Backpack.Serial)
                        Items.UseItem(kit)
                    elif tool == 'bowcraft':
                        toolID = bowcraftID
                        bowcraftkit = Items.FindByID(bowcraftID,0x0000,Player.Backpack.Serial)
                        Items.UseItem(bowcraftkit)
                    Misc.SendMessage('Setting craft with {} material'.format(mat))    
                    Gumps.WaitForGump(460,4000)                         
                    Gumps.SendAction(460, self.getMatGump(mat))
                    Gumps.WaitForGump(460,4000)                         
                    Gumps.SendAction(460, self.getMatGump(mat))##########sets gump to craft with special mats or not
                    Misc.Pause(1000)
                    countHue = self.getMatHue(mat)
                    #Misc.SendMessage('counting {} hue'.format(countHue),40)
                    Misc.Pause(100)
                    itemsInStock = ['arrow','crossbow bolt','shafts']  #not supported to make yet, must stock
                    if name in itemsInStock:
                        if amount != inDeed:
                            self.getMatsByStrName(name,amount - inDeed,0)
                           
                    else:    
                        countId = self.countById(itemID,countHue) + inDeed   
                        while countId < amount:
                            self.checkTool(tool)
                            self.getMatsByStrName(mat,100,20)
                            Misc.SendMessage('Making {}, have {}/{}'.format(name,self.countById(itemID,countHue)+inDeed,amount))                     
                            self.makeItem(int(itemID),int(gump),toolID)
                            Misc.Pause(1200)
                            if excBool == True:
                                for item in Player.Backpack.Contains:
                                    if item.ItemID == itemID:
                                        Items.WaitForProps(item,1000)
                                        if Items.GetPropStringByIndex(item,1) != "exceptional" and Items.GetPropStringByIndex(item,2) != "exceptional":
                                            Misc.SendMessage('Non Exceptional Found')
                                            self.recycle(item,tool)
                                            Misc.Pause(1100)
                            else:                
                                Misc.Pause(800)
                            countId = self.countById(itemID,countHue) + inDeed                        
                    Gumps.SendAction(460, 0)
                    Misc.Pause(1200)    
                    Items.UseItem(bod)
                    Gumps.WaitForGump(456, 4000)
                    Gumps.SendAction(456, 11)
                    Target.WaitForTarget(2000)
                    Target.TargetExecute(Player.Backpack.Serial)
                    Misc.Pause(1500)
                    Items.Move(bod,storeBook,1)
                    Gumps.WaitForGump(668, 5000)
                    Gumps.SendAction(668, 0)
                    Misc.Pause(1100)
                    self.dumpMats()
                Misc.Pause(1100)

    def setBank(self,book,bool):
        Misc.SendMessage('Attempting to set bank points {}'.format(bool))
        Items.UseItem(book)
        Misc.Pause(2000)
        Gumps.WaitForGump(668, 5000)
        Gumps.SendAction(668, 4)            
        Misc.Pause(2000)
        Gumps.SendAction(668, 0)
        bod = Items.FindByID(0x2258,-1,Player.Backpack.Serial)
        Items.UseItem(bod)
        Misc.Pause(1100)
        statusList = ["1157303","1157309","1157306"]
        if Gumps.CurrentGump() == 456:            
            if Gumps.LastGumpRawData().split(' ')[204] in statusList:
                bankStatus = int(Gumps.LastGumpRawData().split(' ')[204])
                banknum = 204
            elif Gumps.LastGumpRawData().split(' ')[193] in statusList:                
                bankStatus = int(Gumps.LastGumpRawData().split(' ')[193])
                banknum = 193
            elif Gumps.LastGumpRawData().split(' ')[205] in statusList:                
                bankStatus = int(Gumps.LastGumpRawData().split(' ')[205])
                banknum  = 205
            Misc.Pause(500)
            
            Misc.SendMessage(bankStatus)
            if bool == False:   
                while not bankStatus == 1157303:
                    Gumps.WaitForGump(456, 10000)
                    Gumps.SendAction(456, 10)
                    Misc.Pause(1000)
                    Misc.SendMessage(bankStatus)
                    bankStatus = int(Gumps.LastGumpRawData().split(' ')[banknum])
                Misc.SendMessage('Banking Disabled')
            elif bool == True:
                while not bankStatus == 1157309: 
                    Gumps.WaitForGump(456, 10000)
                    Gumps.SendAction(456, 10)
                    Misc.Pause(1000)
                    Misc.SendMessage(bankStatus)
                    bankStatus = int(Gumps.LastGumpRawData().split(' ')[banknum])
                Misc.SendMessage('Auto Banking Enabled')    
        else:
            Misc.SendMessage('Unable To Toggle bank NO GUMP',48)
        Items.Move(bod,book,1)
        Misc.Pause(2000)
            
    def TurnInBtnPress(self,s,a):
        reward = self.combobox1.Text            
        if reward == 'RecycleBank':
            bankpnts = True
            gump = 0 
        elif reward == 'POF':
            gump = 112
            bankpnts = False
        elif reward == 'Shadow Hammer':
            gump = 117
            bankpnts = False
        elif reward == 'Bowcraft Ash':
            gump = 112
            bankpnts = False
        elif reward == 'Bowcraft Oak':
            gump = 109
            bankpnts = False    
            
        Misc.SendMessage('Target Book to Turn in for {}'.format(reward),88)
        TurnInBook = Items.FindBySerial(Target.PromptTarget(' '))        
        Misc.SendMessage('Target Book to Put New Deeds ',88)
        storeBook = Items.FindBySerial(Target.PromptTarget(' '))
        Misc.SendMessage('Target NPC',88)
        npc = Mobiles.FindBySerial(Target.PromptTarget(' '))        
        deedCount = int(Items.GetPropStringByIndex(TurnInBook,len(Items.GetPropStringList(TurnInBook))-2).split(':')[1])
        self.setBank(TurnInBook,bankpnts)
        for num in range(deedCount):
            Items.UseItem(TurnInBook)
            Misc.Pause(2000)
            Gumps.WaitForGump(668, 5000)
            Gumps.SendAction(668, 4)            
            Misc.Pause(2000)
            bod = Items.FindByID(0x2258,-1,Player.Backpack.Serial)
            Items.Move(bod,npc,1) 
            Misc.Pause(2000)
            Gumps.WaitForGump(17000, 10000)
            Gumps.SendAction(17000, gump)
            Misc.SendMessage('Turning in for {}'.format(reward))
            if reward != 'RecycleBank':                
                Gumps.WaitForGump(17001, 2000)
                Gumps.SendAdvancedAction(17001,1,List[int]([1]))
                Misc.Pause(1000)
            if Gumps.CurrentGump() == 17000:
                Gumps.SendAction(17000, 0)
            Misc.WaitForContext(npc, 10000)
            Misc.ContextReply(npc, 403)
            Gumps.WaitForGump(455, 10000)
            Misc.Pause(200)
            Gumps.SendAction(455,1)
            
            Misc.Pause(1000)
            for item in Player.Backpack.Contains:
                if item.ItemID == 0x2258:            
                    Items.Move(item,storeBook,1)
                    Misc.Pause(1200)
                    
                    
                    
                    
#########################################################################################################
#####################################  PINKS AND PS ####################################################
#######################################################################################################                    
    def dumpBtnPress(self,s,a):
        Misc.SendMessage("Select Book Dump Scrolls",80)        
        book = Items.FindBySerial(Target.PromptTarget(''))
        
        def pullPS(book,baseGump):
            Gumps.WaitForGump(baseGump,5000)
            lines = Gumps.LastGumpGetLineList()
            Misc.Pause(100)
            skill = lines[0]    
            tens = int(lines[2])
            fifteens = int(lines[3])
            twenties = int(lines[4])
            gumpselection = baseGump * 100
            for r in range(tens):
                if self.totalItems() > 120:
                    Misc.SendMessage("Bag Full",48)
                    break   
                Gumps.SendAction(9157,gumpselection +1)
            for r in range(fifteens):
                if self.totalItems() > 120:
                    Misc.SendMessage("Bag Full",48)
                    break   
                Gumps.SendAction(9157,gumpselection +2)
            for r in range(twenties):
                if self.totalItems() > 120:
                    Misc.SendMessage("Bag Full",48)
                    break   
                Gumps.SendAction(9157,gumpselection +3)
           
        def pullPinks(book,baseGump):
            floatList= []  
            Gumps.WaitForGump(baseGump,5000)
            lines = Gumps.LastGumpGetLineList()
            Misc.Pause(100)
            skill = lines[0]    
            lineNum = 23
            while lineNum >= 14:                
                amountScrolls = 0
                line = lines[lineNum]    
                linesplit =  line.split(' ')
                amountScrolls = int(linesplit[0])
                appendCount = 0
                if lineNum == 14:       # scrolls thru a skill, counts point values, and makes a list of them       
                    while appendCount < amountScrolls:
                        floatList.append(1)
                        appendCount += 1
                elif lineNum == 15:
                    while appendCount < amountScrolls:
                        floatList.append(2)
                        appendCount += 1
                elif lineNum == 16:
                    while appendCount < amountScrolls:
                        floatList.append(3)
                        appendCount += 1
                elif lineNum == 17:
                    while appendCount < amountScrolls:
                        floatList.append(4)
                        appendCount += 1
                elif lineNum == 18:
                    while appendCount < amountScrolls:
                        floatList.append(5)
                        appendCount += 1
                elif lineNum == 19:
                    while appendCount < amountScrolls:
                        floatList.append(6)
                        appendCount += 1
                elif lineNum == 20:
                    while appendCount < amountScrolls:
                        floatList.append(7)
                        appendCount += 1
                elif lineNum == 21:
                    while appendCount < amountScrolls:
                        floatList.append(8)
                        appendCount += 1
                elif lineNum == 22:
                    while appendCount < amountScrolls:
                        floatList.append(9)
                        appendCount += 1
                elif lineNum == 23:
                    while appendCount < amountScrolls:
                        floatList.append(10)
                        appendCount += 1
                lineNum -= 1        
              
            Misc.Pause(100)
            Player.HeadMessage(89,skill)    
            Player.HeadMessage(65,'{}, scrolls'.format(len(floatList)))
            
            gumpselection = baseGump * 100
            for num in floatList:
                if self.totalItems() > 120:
                    Misc.SendMessage("Bag Full",48)
                    break   
                select = gumpselection + (num-1)
                Gumps.WaitForGump(9157, 10000)
                Gumps.SendAction(9157,select)
                                
        if book.Hue == 0x0490:            #### Rosa
            bookList = pinkGumpList
        elif book.Hue == 0x0481:          ##### Blanco
            bookList = psGumpList
        for skillGump in bookList:
            if self.totalItems() > 120:
                Misc.SendMessage("Bag Full Stopping",48)
                break 
            Items.UseItem(book)
            Misc.Pause(500)
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, skillGump) 
            Misc.Pause(1000)
            if book.Hue == 0x0490: 
                pullPinks(book,skillGump)
            elif book.Hue == 0x0481: 
                pullPS(book,skillGump)
             
    def go(self,Xloc,Yloc): 
        global go
        while True:
            if Player.Position.Y < Yloc and Player.Position.X < Xloc:
                go = 'Down'
            elif Player.Position.Y > Yloc and Player.Position.X > Xloc:
                go = 'Up'
            elif Player.Position.Y > Yloc and Player.Position.X < Xloc:
                go = 'Right'          
            elif Player.Position.Y < Yloc and Player.Position.X > Xloc:
                go = 'Left'
            elif Player.Position.Y > Yloc and Player.Position.X == Xloc:
                go = 'North'
            elif Player.Position.Y < Yloc and Player.Position.X == Xloc:
                go = 'South'           
            elif Player.Position.X > Xloc and Player.Position.Y == Yloc:
                go = 'West'          
            elif Player.Position.X < Xloc and Player.Position.Y == Yloc:
                go = 'East'
            if  Player.Position.Y == Yloc and Player.Position.X == Xloc:            
                break      
            if Player.Direction == go:
                    Player.Run(go)                
            else: 
                    Player.Run(go)
                    Player.Run(go)            
        
    def findScrollBooks(self):
        BFilter = Items.Filter()
        BFilter.RangeMax = 15
        BFilter.OnGround = True
        BFilter.Enabled = True
        BFilter.Movable = False  
        BFilter.Graphics = List[int]([0x0FF1])        
        findBooks = Items.ApplyFilter(BFilter)
        Misc.Pause(200)
        if len(findBooks) > 0:
            for book in findBooks:
                bookprops = Items.GetPropStringList(book)
                if bookprops[0] == 'PINKMISC':
                    self.pinkMiscBook = book
                    Items.Message(book,30,'Misc')
                elif bookprops[0] == 'PINKCOMBAT':
                    self.pinkCombatBook = book
                    Items.Message(book,40,'Combat')
                elif bookprops[0] == 'PINKTRADE':
                    self.pinkTradeBook = book
                    Items.Message(book,50,'Trade')
                elif bookprops[0] == 'PINKMAGIC':
                    self.pinkMagicBook = book
                    Items.Message(book,60,'Magic')
                elif bookprops[0] == 'PINKWILDERNESS':
                    self.pinkWildernessBook = book
                    Items.Message(book,70,'Wilderness')
                elif bookprops[0] == 'PINKTHIEVERY':
                    self.pinkThieveryBook = book
                    Items.Message(book,80,'Thievery')
                elif bookprops[0] == 'PINKBARD':
                    self.pinkBardBook = book
                    Items.Message(book,90,'Bard')
                elif bookprops[0] == 'PSMAGIC':
                    self.psMagicBook = book
                    Items.Message(book,90,'Misc')
                elif bookprops[0] == 'PSCOMBAT':
                    self.psCombatBook = book
                    Items.Message(book,90,'Combat')
                elif bookprops[0] == 'PSOTHER':
                    self.psOtherBook = book
                    Items.Message(book,90,'Other')
                elif bookprops[0] == 'PS120':
                    self.ps20Book = book
                    Items.Message(book,90,'20')
        else:
            Misc.SendMessage("filter error , try relogging in",48)
                                                
    def sortScrolls(self):
        PiFilter = Items.Filter()
        PiFilter.RangeMax = 0
        PiFilter.OnGround = True
        PiFilter.Enabled = True
        PiFilter.Movable = False
        pinkbook = List[int]((0x577E, 0x577E))  
        PiFilter.Graphics = pinkbook
        PSFilter = Items.Filter()
        PSFilter.RangeMax = 0
        PSFilter.OnGround = True
        PSFilter.Enabled = True
        PSFilter.Movable = False
        psbook = List[int]((0x9A95, 0x9AA7))  
        PSFilter.Graphics = psbook
        Player.HeadMessage(95,'Sorting Scrolls')
        if Items.BackpackCount(0x14EF,-1) == 0:
            Misc.SendMessage("No Scrolls in Backpack",48)
            return
        for item in Items.FindBySerial(Player.Backpack.Serial).Contains:           
            if item.ItemID == 0x14EF:
                if item.Hue == 0x0490:
                    Misc.Pause(300)
                    Items.WaitForProps(item, 500)
                    props = Items.GetPropStringList(item)
                    propline = props[3]
                    propsplit = propline.split(' ')
                    prop = propsplit[1]
                    Misc.SendMessage(prop)            
                    if prop in pinkMisc:                
                        self.go(self.pinkMiscBook.Position.X, self.pinkMiscBook.Position.Y)                            
                    elif prop in pinkCombat:                
                        self.go(self.pinkCombatBook.Position.X,self.pinkCombatBook.Position.Y)
                    elif prop in pinkTrade:
                        self.go(self.pinkTradeBook.Position.X,self.pinkTradeBook.Position.Y)
                    elif prop in pinkMagic:               
                        self.go(self.pinkMagicBook.Position.X,self.pinkMagicBook.Position.Y)
                    elif prop in pinkWilderness:               
                        self.go(self.pinkWildernessBook.Position.X,self.pinkWildernessBook.Position.Y)                            
                    elif prop in pinkThieving:            
                        self.go(self.pinkThieveryBook.Position.X,self.pinkThieveryBook.Position.Y)
                    elif prop in pinkBard:        
                        self.go(self.pinkBardBook.Position.X,self.pinkBardBook.Position.Y)
                    pinkbooks = Items.ApplyFilter(PiFilter)
                    Misc.Pause(500)
                    pinkbook = Items.Select(pinkbooks, 'Nearest')
                    Misc.Pause(500)
                    Items.Move(item.Serial,pinkbook,0)
                    Misc.Pause(600)
                        
                elif item.Hue == 0x0481:
                    Misc.Pause(300)
                    Items.WaitForProps(item, 500)
                    props = Items.GetPropStringList(item)
                    propline = props[0]
                    propsplit = propline.split(' ')
                    propsplit2 = propsplit[4]
                    prop = propsplit2.split(' ')[0]
                    Misc.SendMessage(prop)            
                    if prop in psOther:                
                        self.go(self.psOtherBook.Position.X, self.psOtherBook.Position.Y)                            
                    elif prop in psCombat:                
                        self.go(self.psCombatBook.Position.X,self.psCombatBook.Position.Y)
                    elif prop in psMagic:               
                        self.go(self.psMagicBook.Position.X,self.psMagicBook.Position.Y)
                    psbooks = Items.ApplyFilter(PSFilter)
                    Misc.Pause(500)
                    psbook = Items.Select(psbooks, 'Nearest')
                    Items.Move(item.Serial,psbook,0)
                    Misc.Pause(600) 
                    
        Misc.Pause(300)
        
        
    def pscatagory(self,bookType):
        PSFilter = Items.Filter()
        PSFilter.RangeMax = 0
        PSFilter.OnGround = True
        PSFilter.Enabled = True
        PSFilter.Movable = False
        psbook = List[int]((0x9A95, 0x9AA7))  
        PSFilter.Graphics = psbook  
        Misc.Pause(500)
        pinkBooks = Items.ApplyFilter(PSFilter)
        Misc.Pause(100)
        pinkBook = Items.Select(pinkBooks,'Nearest')
        Items.UseItem(pinkBook)
        Misc.Pause(500)
        if bookType == self.psCombatBook:     
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044061) #anatomy 
            Misc.Pause(1000)
            self.pscountSkill(1044061,bookType) #anatomy
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044091) #archery 
            Misc.Pause(1000)
            self.pscountSkill(1044091,bookType) #archery
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044102) #fencing 
            Misc.Pause(1000)
            self.pscountSkill(1044102,bookType) #fencing
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044110) #focus
            Misc.Pause(1000)
            self.pscountSkill(1044110,bookType) #focus
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044077) #healing
            Misc.Pause(1000)
            self.pscountSkill(1044077,bookType) #healing
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044101) #mace fighting
            Misc.Pause(1000)
            self.pscountSkill(1044101,bookType) #mace fighting
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044065) #parrying
            Misc.Pause(1000)
            self.pscountSkill(1044065,bookType) #parrying
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044100) #swords
            Misc.Pause(1000)
            self.pscountSkill(1044100,bookType) #swords
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044087) #tactics
            Misc.Pause(1000)
            self.pscountSkill(1044087,bookType) #tactics
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044117) #throwing
            Misc.Pause(1000)
            self.pscountSkill(1044117,bookType) #throwing
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044103) #wrestling
            Misc.Pause(1000)
            self.pscountSkill(1044103,bookType) #wrestling
                            
        if bookType == self.psMagicBook:
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044112)#bush
            Misc.Pause(1000)
            self.pscountSkill(1044112,bookType)#bush
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044111)#chiv
            Misc.Pause(1000)
            self.pscountSkill(1044111,bookType)#chiv
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044076)#eval
            Misc.Pause(1000)
            self.pscountSkill(1044076,bookType)#eval
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044116)#imbue
            Misc.Pause(1000)
            self.pscountSkill(1044116,bookType)#imbue
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044085)#magery
            Misc.Pause(1000)
            self.pscountSkill(1044085,bookType)#magery
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044106)#med
            Misc.Pause(1000)
            self.pscountSkill(1044106,bookType)#med
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044115)#myst
            Misc.Pause(1000)
            self.pscountSkill(1044115,bookType)#myst
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044109)#necro
            Misc.Pause(1000)
            self.pscountSkill(1044109,bookType)#necro
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044113)#ninja
            Misc.Pause(1000)
            self.pscountSkill(1044113,bookType)#ninja
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044086)#resist
            Misc.Pause(1000)
            self.pscountSkill(1044086,bookType)#resist
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044114)#spellweaving
            Misc.Pause(1000)
            self.pscountSkill(1044114,bookType)#spellweaving
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044092)#spirit speak
            Misc.Pause(1000)
            self.pscountSkill(1044092,bookType)#spirit speak
            
        if bookType == self.psOtherBook:    
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044062)#lore
            Misc.Pause(1000)
            self.pscountSkill(1044062,bookType)#lore
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044095)#taming
            Misc.Pause(1000)
            self.pscountSkill(1044095,bookType)#taming
                                    
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044099)#vet
            Misc.Pause(1000)
            self.pscountSkill(1044099,bookType)#vet
                                    
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044093)#stealing
            Misc.Pause(1000)
            self.pscountSkill(1044093,bookType)#stealing
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044107)#stealth
            Misc.Pause(1000)
            self.pscountSkill(1044107,bookType)#stealth
                
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044075)#discord
            Misc.Pause(1000)
            self.pscountSkill(1044075,bookType)#discord
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044089)#music
            Misc.Pause(1000)
            self.pscountSkill(1044089,bookType)#music
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044069)#peace
            Misc.Pause(1000)
            self.pscountSkill(1044069,bookType)#peace
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044082)#provo
            Misc.Pause(1000)
            self.pscountSkill(1044082,bookType)#provo    

    def pscountSkill(self,baseGump,book):
        PSFilter = Items.Filter()
        PSFilter.RangeMax = 0
        PSFilter.OnGround = True
        PSFilter.Enabled = True
        PSFilter.Movable = False
        psbook = List[int]((0x9A95, 0x9AA7))  
        PSFilter.Graphics = psbook 
        lines = Gumps.LastGumpGetLineList()
        Misc.Pause(1000)
        skill = lines[0]
        tens = int(lines[2])
        fifteens = int(lines[3])
        twenties = int(lines[4])
        
        if twenties > 0:
            for r in range(twenties):
                Gumps.SendAction(9157,baseGump * 100 + 3)
            self.goToBook(self.ps20Book)
            pinkBooks = Items.ApplyFilter(PSFilter)
            Misc.Pause(100)
            pinkBook = Items.Select(pinkBooks,'Nearest')
            for item in Player.Backpack.Contains:
                if item.ItemID == 0x14EF:
                    Items.Move(item,pinkBook,1)
                    Misc.Pause(1100)                
            self.goToBook(book)
            pinkBooks = Items.ApplyFilter(PSFilter)
            Misc.Pause(100)
            pinkBook = Items.Select(pinkBooks,'Nearest')
            Misc.Pause(1100)
            Items.UseItem(pinkBook)
                
        if tens >= 12:
            Misc.SendMessage('You can make a 15',67)
            Items.WaitForContents(self.bag,1000)
            combiner = Items.FindByID(0x14EF,0x0664,self.bag.Serial) 
            Misc.Pause(1200)
            Items.Move(combiner,Player.Backpack.Serial,0)  # moves combiner to main bag
            Misc.Pause(1200)
            for r in range(12):
                Gumps.SendAction(9157,baseGump * 100 + 1)
                Items.UseItem(combiner)            
                Target.WaitForTarget(2000)
                scroll = Items.FindByID(0x14EF,0x0481,Player.Backpack.Serial)
                Target.TargetExecute(scroll)
                Misc.Pause(1100)
            scroll = Items.FindByID(0x14EF,0x0481,Player.Backpack.Serial)
            pinkBooks = Items.ApplyFilter(PSFilter)
            Misc.Pause(100)
            pinkBook = Items.Select(pinkBooks,'Nearest')
            Items.Move(scroll,pinkBook.Serial,1)        
            Misc.Pause(1100)
            Items.UseItem(pinkBook)

        if fifteens >= 10:
            Misc.SendMessage('You can make a 20',67)
            Items.WaitForContents(self.bag,1000)
            combiner = Items.FindByID(0x14EF,0x0664,self.bag.Serial) 
            Misc.Pause(1200)
            Items.Move(combiner,Player.Backpack.Serial,0)  # moves combiner to main bag
            Misc.Pause(1200)
            for r in range(10):
                Gumps.SendAction(9157,baseGump * 100 + 2)
                Items.UseItem(combiner)            
                Target.WaitForTarget(2000)
                scroll = Items.FindByID(0x14EF,0x0481,Player.Backpack.Serial)
                Target.TargetExecute(scroll)
                Misc.Pause(1100)
            scroll = Items.FindByID(0x14EF,0x0481,Player.Backpack.Serial)
            self.goToBook(self.ps20Book)
            pinkBooks = Items.ApplyFilter(PSFilter)
            Misc.Pause(100)
            pinkBook = Items.Select(pinkBooks,'Nearest')
            for item in Player.Backpack.Contains:
                if item.ItemID == 0x14EF:
                    Items.Move(item,pinkBook,1)
                    Misc.Pause(1100)                
            self.goToBook(book)
            pinkBooks = Items.ApplyFilter(PSFilter)
            Misc.Pause(100)
            pinkBook = Items.Select(pinkBooks,'Nearest')
            Items.Move(scroll,pinkBook.Serial,1)    
            Misc.Pause(1100)
            Items.UseItem(pinkBook)

    def pinkcatagory(self,bookType):
        PiFilter = Items.Filter()
        PiFilter.RangeMax = 0
        PiFilter.OnGround = True
        PiFilter.Enabled = True
        PiFilter.Movable = False
        pinkbook = List[int]((0x577E, 0x577E))  
        Misc.Pause(500)
        pinkBooks = Items.ApplyFilter(PiFilter)
        Misc.Pause(100)
        pinkBook = Items.Select(pinkBooks,'Nearest')
        Items.UseItem(pinkBook)
        Misc.Pause(500)
        if bookType == self.pinkMiscBook:
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044064) 
            Misc.Pause(1000)
            self.pinkcountSkill(1044064)#arms lore
                
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044066) 
            Misc.Pause(1000)
            self.pinkcountSkill(1044066)#begging
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044070) 
            Misc.Pause(1000)
            self.pinkcountSkill(1044070)#camping
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044072) 
            Misc.Pause(1000)
            self.pinkcountSkill(1044072) # carto
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044079) #forensics 
            Misc.Pause(1000)
            self.pinkcountSkill(1044079) #forensics
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044063) #tasteid
            Misc.Pause(1000)
            self.pinkcountSkill(1044063) #tasteid
            
        if bookType == self.pinkCombatBook:     
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044061) #anatomy 
            Misc.Pause(1000)
            self.pinkcountSkill(1044061) #anatomy
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044091) #archery 
            Misc.Pause(1000)
            self.pinkcountSkill(1044091) #archery
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044102) #fencing 
            Misc.Pause(1000)
            self.pinkcountSkill(1044102) #fencing
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044110) #focus
            Misc.Pause(1000)
            self.pinkcountSkill(1044110) #focus
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044077) #healing
            Misc.Pause(1000)
            self.pinkcountSkill(1044077) #healing
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044101) #mace fighting
            Misc.Pause(1000)
            self.pinkcountSkill(1044101) #mace fighting
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044065) #parrying
            Misc.Pause(1000)
            self.pinkcountSkill(1044065) #parrying
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044100) #swords
            Misc.Pause(1000)
            self.pinkcountSkill(1044100) #swords
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044087) #tactics
            Misc.Pause(1000)
            self.pinkcountSkill(1044087) #tactics
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044117) #throwing
            Misc.Pause(1000)
            self.pinkcountSkill(1044117) #throwing
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044103) #wrestling
            Misc.Pause(1000)
            self.pinkcountSkill(1044103) #wrestling
            
        if bookType == self.pinkTradeBook:     
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044060) #alchemy
            Misc.Pause(1000)
            self.pinkcountSkill(1044060) #alchemy
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044067) #blacksmith
            Misc.Pause(1000)
            self.pinkcountSkill(1044067) #blacksmith
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044068) #fletching
            Misc.Pause(1000)
            self.pinkcountSkill(1044068) #fletching
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044071) #carpentry
            Misc.Pause(1000)
            self.pinkcountSkill(1044071) #carpentry
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044073) #cooking
            Misc.Pause(1000)
            self.pinkcountSkill(1044073) #cooking
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044083) #inscription
            Misc.Pause(1000)
            self.pinkcountSkill(1044083) #inscription
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044104) #lumberjacking
            Misc.Pause(1000)
            self.pinkcountSkill(1044104) #lumberjacking
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044105) #mining
            Misc.Pause(1000)
            self.pinkcountSkill(1044105) #mining
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044094) #tailor
            Misc.Pause(1000)
            self.pinkcountSkill(1044094) #tailor
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044097) #tinker
            Misc.Pause(1000)
            self.pinkcountSkill(1044097) #tinker
            
        if bookType == self.pinkMagicBook:
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044112)#bush
            Misc.Pause(1000)
            self.pinkcountSkill(1044112)#bush
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044111)#chiv
            Misc.Pause(1000)
            self.pinkcountSkill(1044111)#chiv
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044076)#eval
            Misc.Pause(1000)
            self.pinkcountSkill(1044076)#eval
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044116)#imbue
            Misc.Pause(1000)
            self.pinkcountSkill(1044116)#imbue
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044085)#magery
            Misc.Pause(1000)
            self.pinkcountSkill(1044085)#magery
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044106)#med
            Misc.Pause(1000)
            self.pinkcountSkill(1044106)#med
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044115)#myst
            Misc.Pause(1000)
            self.pinkcountSkill(1044115)#myst
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044109)#necro
            Misc.Pause(1000)
            self.pinkcountSkill(1044109)#necro
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044113)#ninja
            Misc.Pause(1000)
            self.pinkcountSkill(1044113)#ninja
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044086)#resist
            Misc.Pause(1000)
            self.pinkcountSkill(1044086)#resist
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044114)#spellweaving
            Misc.Pause(1000)
            self.pinkcountSkill(1044114)#spellweaving
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044092)#spirit speak
            Misc.Pause(1000)
            self.pinkcountSkill(1044092)#spirit speak
            
        if bookType == self.pinkWildernessBook:    
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044062)#lore
            Misc.Pause(1000)
            self.pinkcountSkill(1044062)#lore
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044095)#taming
            Misc.Pause(1000)
            self.pinkcountSkill(1044095)#taming
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044078)#fishing
            Misc.Pause(1000)
            self.pinkcountSkill(1044078)#fishing
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044080)#herding
            Misc.Pause(1000)
            self.pinkcountSkill(1044080)#herding
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044098)#tracking
            Misc.Pause(1000)
            self.pinkcountSkill(1044098)#tracking
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044099)#vet
            Misc.Pause(1000)
            self.pinkcountSkill(1044099)#vet
            
        if bookType == self.pinkThieveryBook:    
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044074)#detect
            Misc.Pause(1000)
            self.pinkcountSkill(1044074)#detect
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044081)#hiding
            Misc.Pause(1000)
            self.pinkcountSkill(1044081)#hiding
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044084)#lock picking
            Misc.Pause(1000)
            self.pinkcountSkill(1044084)#lock picking
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044090)# poisoning
            Misc.Pause(1000)
            self.pinkcountSkill(1044090)# poisoning
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044108)#remove trap
            Misc.Pause(1000)
            self.pinkcountSkill(1044108)#remove trap
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044088)#snooping
            Misc.Pause(1000)
            self.pinkcountSkill(1044088)#snooping
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044093)#stealing
            Misc.Pause(1000)
            self.pinkcountSkill(1044093)#stealing
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044107)#stealth
            Misc.Pause(1000)
            self.pinkcountSkill(1044107)#stealth
            
        if bookType == self.pinkBardBook:    
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044075)#discord
            Misc.Pause(1000)
            self.pinkcountSkill(1044075)#discord
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044089)#music
            Misc.Pause(1000)
            self.pinkcountSkill(1044089)#music
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044069)#peace
            Misc.Pause(1000)
            self.pinkcountSkill(1044069)#peace
            
            Gumps.WaitForGump(9157, 10000)
            Gumps.SendAction(9157, 1044082)#provo
            Misc.Pause(1000)
            self.pinkcountSkill(1044082)#provo
            
    def pinkcountSkill(self,baseGump):
        PiFilter = Items.Filter()
        PiFilter.RangeMax = 0
        PiFilter.OnGround = True
        PiFilter.Enabled = True
        PiFilter.Movable = False
        pinkbook = List[int]((0x577E, 0x577E))  
        floatList= []
        floatList.Clear()
        Misc.Pause(500)
        while Gumps.HasGump() == False:
            Misc.Pause(500)
        lines = Gumps.LastGumpGetLineList()
        Misc.Pause(1000)
        skill = lines[0]    
        lineNum = 23
        while lineNum >= 14:  
            amountScrolls = 0
            line = lines[lineNum]    
            linesplit =  line.split(' ')
            amountScrolls = int(linesplit[0])
            appendCount = 0
            if lineNum == 14:       # scrolls thru a skill counts point values and makes a list of them       
                while appendCount < amountScrolls:
                    floatList.append(1)
                    appendCount += 1
            elif lineNum == 15:
                while appendCount < amountScrolls:
                    floatList.append(2)
                    appendCount += 1
            elif lineNum == 16:
                while appendCount < amountScrolls:
                    floatList.append(3)
                    appendCount += 1
            elif lineNum == 17:
                while appendCount < amountScrolls:
                    floatList.append(4)
                    appendCount += 1
            elif lineNum == 18:
                while appendCount < amountScrolls:
                    floatList.append(5)
                    appendCount += 1
            elif lineNum == 19:
                while appendCount < amountScrolls:
                    floatList.append(6)
                    appendCount += 1
            elif lineNum == 20:
                while appendCount < amountScrolls:
                    floatList.append(7)
                    appendCount += 1
            elif lineNum == 21:
                while appendCount < amountScrolls:
                    floatList.append(8)
                    appendCount += 1
            elif lineNum == 22:
                while appendCount < amountScrolls:
                    floatList.append(9)
                    appendCount += 1
            elif lineNum == 23:
                while appendCount < amountScrolls:
                    floatList.append(10)
                    appendCount += 1
            lineNum -=1
        Misc.Pause(100)
        Player.HeadMessage(89,skill)    
        Player.HeadMessage(65,sum(floatList))
        if sum(floatList) >= 50:   # Sum of total points of that skill
            combineCount = 0
            gumpselection = baseGump * 100
            Misc.SendMessage('You can combine a 5.0',67)
            Items.WaitForContents(self.bag,1000)
            combiner = Items.FindByID(0x14EF,0x0664,self.bag.Serial) 
            Misc.Pause(1500)
            Items.Move(combiner,Player.Backpack.Serial,0)  # moves combiner to main bag
            listNum = 0
            while combineCount < 50:          # loops until over 5.0
                number = floatList[listNum]
                if number == 10:
                    useGump = gumpselection + 9  # sets which scroll gump to press based on point value             
                elif number == 9:
                    useGump = gumpselection + 8    
                elif number == 8:
                    useGump = gumpselection + 7
                elif number == 7:
                    useGump = gumpselection + 6
                elif number == 6:
                    useGump = gumpselection + 5
                elif number == 5:
                    useGump = gumpselection + 4
                elif number == 4:
                    useGump = gumpselection + 3
                elif number == 3:
                    useGump = gumpselection + 2
                elif number == 2:
                    useGump = gumpselection + 1
                elif number == 1:
                    useGump = gumpselection 
                if combineCount + number == 20:   # skips that scroll if adds to 2.0
                    listNum += 1

                else:    
                    Gumps.WaitForGump(9157, 10000)
                    Gumps.SendAction(9157, (useGump)) # pulls pink               
                    combineCount += int(number)  # adds to count of combiner
                    floatList.remove(number)  # removes that scroll from list of known scrolls
                    listNum = 0
                    Misc.Pause(1500)
                    pink = Items.FindByID(0x14EF,0x0490,Player.Backpack.Serial) # finds pulled out scroll
                    Items.UseItem(combiner)   
                    Target.WaitForTarget(1000,False)
                    Target.TargetExecute(pink)   # combines scroll
                Misc.Pause(1000)
            Gumps.WaitForGump(9082, 10000) # if added too many points gump 
            Gumps.SendAction(9082, 1)    # agree to waste extra points
            pinkBooks = Items.ApplyFilter(PiFilter)
            Misc.Pause(100)
            pinkBook = Items.Select(pinkBooks,'Nearest')
            Misc.Pause(1500)
            while Items.BackpackCount(0x14EF,0x0490) > 0:  # move all pinks to nearest book
                pink = Items.FindByID(0x14EF,0x0490,Player.Backpack.Serial)
                Items.Move(pink,pinkBook,1)
                Misc.Pause(1500)
            Gumps.SendAction(9006, 0)    
            Items.UseItem(pinkBook)   # reopen book for next loop        
                
    def goToBook(self,book):
        self.go(book.Position.X,book.Position.Y)
        Misc.Pause(1000)
        
    def sortScrollBtnPress(self,s,a):           
        self.findScrollBooks()            
        self.sortScrolls()

    def combinePSBtnPress(self,s,a):
        self.bag = Items.FindByID(0x0E76,-1,Player.Backpack.Serial) ##### SET UR COMBINER CONTAINER TYPE
        if not self.bag:
            Misc.SendMessage('Bag with id 0x0E76 with combiners not found',48)
            return
        if Items.BackpackCount(0x14EF,0x0664) == 0:
            Misc.SendMessage('combiners not found',48)
            return
        Misc.SendMessage('You have {} Combiners in bag'.format(Items.BackpackCount(0x14EF,0x0664)),48)
        self.findScrollBooks()
        self.goToBook(self.psCombatBook)
        self.pscatagory(self.psCombatBook)
        self.goToBook(self.psMagicBook)
        self.pscatagory(self.psMagicBook)
        self.goToBook(self.psOtherBook)
        self.pscatagory(self.psOtherBook)
        
    def combinePinkBtnPress(self,s,a):
        self.bag = Items.FindByID(0x0E76,-1,Player.Backpack.Serial) ##### SET UR COMBINER CONTAINER TYPE
        if not self.bag:
            Misc.SendMessage('Bag with id 0x0E76 with combiners not found',48)
            return
        if Items.BackpackCount(0x14EF,0x0664) == 0:
            Misc.SendMessage('combiners not found',48)
            return
        Misc.SendMessage('You have {} Combiners in bag'.format(Items.BackpackCount(0x14EF,0x0664)),48)
        self.findScrollBooks()
        self.goToBook(self.pinkMiscBook)
        self.pinkcatagory(self.pinkMiscBook)    
        self.goToBook(self.pinkCombatBook)
        self.pinkcatagory(self.pinkCombatBook)
        self.goToBook(self.pinkTradeBook)
        self.pinkcatagory(self.pinkTradeBook)
        self.goToBook(self.pinkMagicBook)
        self.pinkcatagory(self.pinkMagicBook)
        self.goToBook(self.pinkWildernessBook)
        self.pinkcatagory(self.pinkWildernessBook)
        self.goToBook(self.pinkThieveryBook)
        self.pinkcatagory(self.pinkThieveryBook)
        self.goToBook(self.pinkBardBook)
        self.pinkcatagory(self.pinkBardBook)
            
                                   
######################################################################################################                    
############################################# IMBUEING  ##############################################
######################################################################################################

    def getDurability(self,item):
        Items.WaitForProps(item,1000)
        propLen = len(Items.GetPropStringList(item))
        if 'durability' in Items.GetPropStringByIndex(item,propLen-1):
            durability = Items.GetPropStringByIndex(item,propLen - 1).split('/')[1]
            return int(durability)
        elif 'durability' in Items.GetPropStringByIndex(item,propLen-2):
            durability = Items.GetPropStringByIndex(item,propLen - 2).split('/')[1]
            return int(durability)
        if propLen > 2:
            if 'durability' in Items.GetPropStringByIndex(item,propLen-3):
                durability = Items.GetPropStringByIndex(item,propLen-3).split('/')[1]
                return int(durability)    
        else: 
            Misc.SendMessage('Error finding durability of {}'.format(item.Name))
            return 255
    
    def getMatFromImbueGump(self):###########################gets imbueing mats from reading imbue gump
        list = Gumps.LastGumpGetLineList()        
        mat1name = list[10]
        mat2name = list[12]
        mat3name = list[14]
        Misc.SendMessage('{} {} {}'.format(mat1name,mat2name,mat3name))
        for int in range(len(matIdList)):
            x = matIdList[int]
            if mat1name in x:
                mat1ID = x[1]
            elif mat2name in x:
                mat2ID = x[1]                
            elif mat3name in x:
                mat3ID = x[1]
                if mat3ID == 0x571C: #BLOB MATS change to if len of list
                    mat3hue = x[2] 
                else:
                    mat3hue = -1 
            Misc.Pause(50)

        Misc.SendMessage('{} {} {} {}'.format(mat1ID,mat2ID,mat3ID,mat3hue))        
        return mat1ID,mat2ID,mat3ID,mat3hue
        
    def getImbueGump(self,strName):
        for int in range(len(imbueList)):
            x = imbueList[int]
            if strName in x:            
                return x[1]
            Misc.Pause(50)
        Misc.SendMessage(x[1])
        
    def imbueBtnPress(self,s,a):
        Journal.Clear()
        if not Misc.ReadSharedValue('resCont'):
            Player.HeadMessage(70,'Target Resource Container')
            Misc.SetSharedValue('resCont',Target.PromptTarget(''))
        self.resCont = Items.FindBySerial(Misc.ReadSharedValue('resCont'))
        Misc.SendMessage('Target Item to Imbue',88)
        item = Items.FindBySerial(Target.PromptTarget(' '))
        Items.UseItem(self.resCont)
        Misc.Pause(1500)        
        name = self.combobox4.Text
        Misc.SendMessage(name)
        if self.getDurability(item) < 255 and "Jewls" not in name:
            for r in range(5):
                Misc.SendMessage('POWDER IT FIRST DUMBASS',41)
            return
        success = Journal.Search('You successfully imbue the item!') 
        while not success:
            Player.UseSkill('Imbuing')
            Gumps.WaitForGump(999059, 10000)
            Gumps.SendAction(999059, 1)
            Target.WaitForTarget(2000)
            Target.TargetExecute(item)
            if name in casting:
                typeGump = 1114248
            elif name in combat:
                typeGump = 1114249
            elif name in hitAreaEffects:
                typeGump = 1114250
            elif name in hitEffects:
                typeGump = 1114251
            elif name in superSlayers:
                typeGump = 1114264
            elif name in slayers:
                typeGump = 1114263    
            elif name in stats:
                typeGump = 1114262
            elif name in skillGroup1:
                typeGump = 1114255
            elif name in skillGroup2:
                typeGump = 1114256
            elif name in skillGroup3:
                typeGump = 1114257
            elif name in skillGroup4:
                typeGump = 1114258
            elif name in skillGroup5:
                typeGump = 1114259
            Misc.SendMessage(typeGump)        
            Gumps.WaitForGump(999056, 10000)
            Gumps.SendAction(999056, typeGump)
            Gumps.WaitForGump(999056, 10000)
            gump = self.getImbueGump(name)
            Gumps.SendAction(999056, int(gump))
            Gumps.WaitForGump(999056, 10000)
            Gumps.SendAction(999056, 313)  ### set to max prop weight
            Misc.Pause(2000)
            mats = self.getMatFromImbueGump() 
            mat1 = Items.FindByID(mats[0],-1,self.resCont.Serial)
            mat2 = Items.FindByID(mats[1],-1,self.resCont.Serial)
            mat3 = Items.FindByID(mats[2],mats[3],self.resCont.Serial)
            mat3hue = mats[3]

            if Items.BackpackCount(mats[0],-1) < 10:    
                Items.Move(mat1,Player.Backpack,50)
                Misc.Pause(1200)
            if Items.BackpackCount(mats[1],-1) < 10:            
                Items.Move(mat2,Player.Backpack,50)
                Misc.Pause(1200) 
            if Items.BackpackCount(mats[2],mat3hue) < 10:            
                Items.Move(mat3,Player.Backpack,10)
                Misc.Pause(1200)
  
            Gumps.WaitForGump(999056, 10000)
            Gumps.SendAction(999056, 302)
            Misc.Pause(2000)
            success = Journal.Search('You successfully imbue the item!')
        xtramat1 = Items.FindByID(mats[0],-1,Player.Backpack.Serial)
        xtramat2 = Items.FindByID(mats[1],-1,Player.Backpack.Serial)
        if xtramat1:
            Items.Move(xtramat1,self.resCont,50)
            Misc.Pause(1300)
        if xtramat2:
            Items.Move(xtramat2,self.resCont,50)
            Misc.Pause(1300)
        Journal.Clear() 
##############################################################################################################################            
form = itemMaker()
Application.Run(form)

  

 