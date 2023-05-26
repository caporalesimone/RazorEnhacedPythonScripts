#Installare Iron python 2.7

import clr
clr.AddReference("System.Core")
import System
clr.ImportExtensions(System.Linq)
from System.Collections.Generic import List
from System import Byte, Int32, String
import sys
sys.path.append(r'C:\\Program Files\\IronPython 2.7\\Lib')  # D/L and adjust path for your library sorry 
import csv

class BOD:
    def __init__(self, type, item, quality, material, amount):
        self.type = type
        self.item = item
        self.quality = quality
        self.material = material
        self.amount = amount
        
        


BODBook = Target.PromptTarget('Select BOD-Book to export')
Items.UseItem(BODBook)
Gumps.WaitForGump(1425364447, 3000)
gump = Gumps.LastGumpGetLineList()


with open('D:\\Test.csv', 'wb') as csvfile: #ab #wb
    fieldnames = ['Type', 'Item', 'Quality', 'Material', 'Amount']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()

    while gump.FindIndex(lambda x: x.Contains('Next page')) > 0:
        gump = Gumps.LastGumpGetLineList()
        #MAIN LOGIC
        #=====================================================
        bodValues = []
        index = gump.FindIndex(lambda x: x.Contains('<BASEFONT COLOR'))
     
        for i in range(len(gump)):
            if(i > index):
                if(gump[i] != '0'):
                    bodValues.Add(BOD(None, None, None, None, gump[i].split('/')[1]))
                    

        firstTypeIndex = gump.FindIndex(lambda x: x.Contains('Small') or x.Contains('Large'))  
         
        for i in range(len(bodValues)):
            bodValues[i].type = gump[firstTypeIndex+i*4]
            bodValues[i].item = gump[firstTypeIndex+i*4+1]
            bodValues[i].quality = gump[firstTypeIndex+i*4+2]
            bodValues[i].material = gump[firstTypeIndex+i*4+3]
            
        
        for i in range(len(bodValues)):
            writer.writerow({'Type': bodValues[i].type, 
                             'Item': bodValues[i].item, 
                             'Quality': bodValues[i].quality, 
                             'Material': bodValues[i].material, 
                             'Amount': bodValues[i].amount})
            Misc.SendMessage(
                ' Type: '        + bodValues[i].type + 
                ' Item: '       + bodValues[i].item + 
                ' Quality: '    + bodValues[i].quality + 
                ' Material: '   + bodValues[i].material + 
                ' Amount: '     + bodValues[i].amount
                )
        #=====================================================
        Gumps.SendAction(1425364447, 3)
        Misc.Pause(800)