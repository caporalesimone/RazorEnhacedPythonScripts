#===============================================#
#               Alchemist Crafts                #
#===============================================#
#                                               #
#   Author: CookieLover                         #
#   Latest Release: 11/12/2017                  #
#                                               #
#===============================================#
#                                               #
#   What you need:                              #
#   - a container with reagents, bottles and    #
#     ingots                                    #
#   - tinkering and at least a toolkit          #
#                                               #
#===============================================#

import clr, thread

clr.AddReference("System.Collections")
clr.AddReference("System.Drawing")
clr.AddReference("System.Windows.Forms")

from System.Collections import *
from System.Drawing import Point, Color, Size
from System.Windows.Forms import (Application, Button, Form, 
    BorderStyle, GroupBox, Label, TextBox, RadioButton,
    FlatStyle)
    
class Prep(object):
    Ingr = None
    ID = Cat = Sub = 0
    Text = ''
    def __init__(self, typ, ingredients, category, submenu, text):
        self.ID = typ
        self.Ingr = ingredients
        self.Cat = category
        self.Sub = submenu
        self.Text = text
            
class AlchemistForm(Form):
    Delay = {
        'base' : 500,
        'drag' : 600,
        'tout' : 3000
        }
    IDs = {
        'ingot' : 0x1BF2,
        'bottle' : 0x0F0E,
        'mortar' : 0xE9B,
        'tool' : 0x1EB8
        }
    Potions = {
        'gheal' : Prep(0x0F0C, [(0xf85, 7)], 22, 16, 'lesser heal'),
        'invisibility' : Prep(0x0F06, [(0xf88, 3), (0xf7b, 4)], 57, 2, 'Invisibility'),
        'dpoison' : Prep(0x0F0A, [(0xf88, 8)], 36, 23, 'lesser poison'), # for pvp
        'gpoison' : Prep(0x0F0A, [(0xf88, 4)], 36, 16, 'lesser poison'), # for gardening
        'grefresh' : Prep(0x0F0B, [(0xf7a, 5)], 1, 9, 'refresh'),
        'gstrength' : Prep(0x0F09, [(0xf86, 5)], 29, 9, 'strength'),
        'gexplosion' : Prep(0x0F0D, [(0xf8c, 10)], 43, 16, 'lesser explosion'),
        'gcure' : Prep(0x0F07, [(0xf84, 6)], 22, 44, 'lesser heal'),
        'gagility' : Prep(0x0F08, [(0xf7b, 3)], 8, 9, 'agility')
        }
    
    Reags = [3962, 3973, 3976, 3963, 3974, 3980, 3972]
    
    ScriptName = 'Alchemist Crafts'
    CurVer = '1.0.1'
    
    BGWorker = None
    Working = False
    
    CHEST = None # replace with serial not to be prompted
    COUNT = 0
    POT = None
    TOBEMADE = 0
    
    def __init__(self):
        self.BackColor = Color.FromArgb(25,25,25)
        self.ForeColor = Color.FromArgb(231,231,231)
        self.Size = Size(300, 350)
        self.Text = '{0}'.format(self.ScriptName)
        
        self.CountersSetup()
        
        self.PotsSetup()
        
        self.btnStart = Button()
        self.btnStart.Text = 'Start'
        self.btnStart.BackColor = Color.FromArgb(50,50,50)
        self.btnStart.Location = Point(222, 226)
        self.btnStart.Size = Size(50, 30)
        self.btnStart.FlatStyle = FlatStyle.Flat
        self.btnStart.FlatAppearance.BorderSize = 1
        self.btnStart.Click += self.btnStartPressed
        
        self.btnStop = Button()
        self.btnStop.Text = 'Stop'
        self.btnStop.BackColor = Color.FromArgb(50,50,50)
        self.btnStop.Location = Point(222, 266)
        self.btnStop.Size = Size(50, 30)
        self.btnStop.FlatStyle = FlatStyle.Flat
        self.btnStop.FlatAppearance.BorderSize = 1
        self.btnStop.Click += self.btnStopPressed
        
        self.Controls.Add(self.btnStart)
        self.Controls.Add(self.btnStop)
        self.Controls.Add(self.pnlCounters)
        self.Controls.Add(self.pnlTools)
    
    def CountersSetup(self):
        self.pnlCounters = GroupBox()
        self.pnlCounters.BackColor = Color.FromArgb(25,25,25)
        self.pnlCounters.ForeColor = Color.FromArgb(231,231,231)
        self.pnlCounters.Size = Size(194, 60)
        self.pnlCounters.Location = Point(14, 12)
        self.pnlCounters.Text = 'Options'
        
        self.lblCount = Label()
        self.lblCount.BackColor = Color.FromArgb(25,25,25)
        self.lblCount.ForeColor = Color.FromArgb(231,231,231)
        self.lblCount.Size = Size(40, 30)
        self.lblCount.Location = Point(12, 22)
        self.lblCount.Text = 'Count:'
        
        self.txtCount = Label()
        self.txtCount.BackColor = Color.FromArgb(25,25,25)
        self.txtCount.ForeColor = Color.FromArgb(231,231,231)
        self.txtCount.Size = Size(30, 30)
        self.txtCount.Location = Point(52, 22)
        self.txtCount.Text = '0'
        
        self.lblMake = Label()
        self.lblMake.BackColor = Color.FromArgb(25,25,25)
        self.lblMake.ForeColor = Color.FromArgb(231,231,231)
        self.lblMake.Size = Size(40, 30)
        self.lblMake.Location = Point(92, 22)
        self.lblMake.Text = 'Make:'
        
        self.txtMake = TextBox()
        self.txtMake.BackColor = Color.FromArgb(25,25,25)
        self.txtMake.ForeColor = Color.FromArgb(231,231,231)
        self.txtMake.Size = Size(30, 30)
        self.txtMake.Location = Point(132, 20)
        self.txtMake.Text = '0'
        
        self.pnlCounters.Controls.Add(self.lblCount)
        self.pnlCounters.Controls.Add(self.txtCount)
        self.pnlCounters.Controls.Add(self.lblMake)
        self.pnlCounters.Controls.Add(self.txtMake)
        
    def PotsSetup(self):
        self.pnlTools = GroupBox()
        self.pnlTools.BackColor = Color.FromArgb(25,25,25)
        self.pnlTools.ForeColor = Color.FromArgb(231,231,231)
        self.pnlTools.Size = Size(194, 214)
        self.pnlTools.Location = Point(14, 82)
        self.pnlTools.Text = 'Potions'
        
        self.rbHeal = RadioButton()
        self.rbHeal.Text = 'Greater Heal'
        self.rbHeal.Checked = True
        self.rbHeal.Location = Point(12, 12)
        self.rbHeal.BackColor = Color.FromArgb(25,25,25)
        self.rbHeal.ForeColor = Color.FromArgb(231,231,231)
        self.rbHeal.Size = Size(80, 30)
        
        self.rbCure = RadioButton()
        self.rbCure.Text = 'Greater Cure'
        self.rbCure.Location = Point(12, 52)
        self.rbCure.BackColor = Color.FromArgb(25,25,25)
        self.rbCure.ForeColor = Color.FromArgb(231,231,231)
        self.rbCure.Size = Size(80, 30)
        
        self.rbRefresh = RadioButton()
        self.rbRefresh.Text = 'Greater Refresh'
        self.rbRefresh.Location = Point(12, 92)
        self.rbRefresh.BackColor = Color.FromArgb(25,25,25)
        self.rbRefresh.ForeColor = Color.FromArgb(231,231,231)
        self.rbRefresh.Size = Size(80, 30)
        
        self.rbStrength = RadioButton()
        self.rbStrength.Text = 'Greater Strength'
        self.rbStrength.Location = Point(12, 132)
        self.rbStrength.BackColor = Color.FromArgb(25,25,25)
        self.rbStrength.ForeColor = Color.FromArgb(231,231,231)
        self.rbStrength.Size = Size(80, 30)
        
        self.rbAgility = RadioButton()
        self.rbAgility.Text = 'Greater Agility'
        self.rbAgility.Location = Point(12, 172)
        self.rbAgility.BackColor = Color.FromArgb(25,25,25)
        self.rbAgility.ForeColor = Color.FromArgb(231,231,231)
        self.rbAgility.Size = Size(80, 30)
        
        self.rbInvis = RadioButton()
        self.rbInvis.Text = 'Invisibility'
        self.rbInvis.Location = Point(102, 12)
        self.rbInvis.BackColor = Color.FromArgb(25,25,25)
        self.rbInvis.ForeColor = Color.FromArgb(231,231,231)
        self.rbInvis.Size = Size(80, 30)
        
        self.rbGPoison = RadioButton()
        self.rbGPoison.Text = 'Greater Poison'
        self.rbGPoison.Location = Point(102, 52)
        self.rbGPoison.BackColor = Color.FromArgb(25,25,25)
        self.rbGPoison.ForeColor = Color.FromArgb(231,231,231)
        self.rbGPoison.Size = Size(80, 30)
        
        self.rbDPoison = RadioButton()
        self.rbDPoison.Text = 'Deadly Poison'
        self.rbDPoison.Location = Point(102, 92)
        self.rbDPoison.BackColor = Color.FromArgb(25,25,25)
        self.rbDPoison.ForeColor = Color.FromArgb(231,231,231)
        self.rbDPoison.Size = Size(80, 30)
        
        self.rbExplosion = RadioButton()
        self.rbExplosion.Text = 'Greater Explosion'
        self.rbExplosion.Location = Point(102, 132)
        self.rbExplosion.BackColor = Color.FromArgb(25,25,25)
        self.rbExplosion.ForeColor = Color.FromArgb(231,231,231)
        self.rbExplosion.Size = Size(80, 30)
               
        self.pnlTools.Controls.Add(self.rbHeal)
        self.pnlTools.Controls.Add(self.rbCure)
        self.pnlTools.Controls.Add(self.rbRefresh)
        self.pnlTools.Controls.Add(self.rbStrength)
        self.pnlTools.Controls.Add(self.rbAgility)
        self.pnlTools.Controls.Add(self.rbInvis)
        self.pnlTools.Controls.Add(self.rbGPoison)
        self.pnlTools.Controls.Add(self.rbDPoison)
        self.pnlTools.Controls.Add(self.rbExplosion)
        
    def btnStartPressed(self, sender, args):
        if not self.Working:
            if self.rbHeal.Checked:
                self.POT = self.Potions['gheal']
            elif self.rbCure.Checked:
                self.POT = self.Potions['gcure']
            elif self.rbRefresh.Checked:
                self.POT = self.Potions['grefresh']
            elif self.rbStrength.Checked:
                self.POT = self.Potions['gstrength']
            elif self.rbAgility.Checked:
                self.POT = self.Potions['gagility']
            elif self.rbInvis.Checked:
                self.POT = self.Potions['invisibility']
            elif self.rbGPoison.Checked:
                self.POT = self.Potions['gpoison']
            elif self.rbDPoison.Checked:
                self.POT = self.Potions['dpoison']
            elif self.rbExplosion.Checked:
                self.POT = self.Potions['gexplosion']
            else:
                Misc.SendMessage('{0}: No potion selected.'.format(self.ScriptName), 33)
                return
                
            self.SetChest()
            
            if self.CHEST == -1:
                Misc.SendMessage('{0}: No container selected.'.format(self.ScriptName), 33)
                return
            
            make = 0
            
            try:
                make = int(self.txtMake.Text)
            except:
                make = 100
                self.txtMake.Text = 100
                pass
                
            self.TOBEMADE = make
            self.Working = True
            self.BGWorker = thread.start_new_thread(self.Main,(1,))
            
        else:
            Misc.SendMessage('{0}: Already at work, sir!'.format(self.ScriptName), 33)
        
    def btnStopPressed(self, sender, args):
        if self.Working:
            self.COUNT = 0
            self.Working = False
        
    def SetChest(self):
        if self.CHEST is None:
            Misc.SendMessage("Target the container you wish to restock with.", 50)
            c = Target.PromptTarget()
            Items.WaitForContents(Items.FindBySerial(c), 5000)
            self.CHEST = c

    def Restocka(self):
        chest = Items.FindBySerial(self.CHEST)
        if Items.BackpackCount(self.IDs['ingot'], 0) < 10:
            ingots = next(i for i in chest.Contains if (i.ItemID == self.IDs['ingot'] and i.Hue == 0))
            if ingots is None:
                return True
            amount = 100 if ingots.Amount >= 100 else 0
            Items.Move(ingots, Player.Backpack, amount)
            Misc.Pause(self.Delay['drag'])

        if Items.BackpackCount(self.IDs['bottle'], 0) == 0:
            bottles = next(i for i in chest.Contains if i.ItemID == self.IDs['bottle'])
            if bottles is None:
                return True
            amount = 100 if bottles.Amount >= 100 else 0
            Items.Move(bottles, Player.Backpack, amount)
            Misc.Pause(self.Delay['drag'])

        for ingr in self.POT.Ingr:
            if Items.BackpackCount(ingr[0], 0) < 10:
                ingredient = next(i for i in chest.Contains if i.ItemID == ingr[0])
                if ingredient is None:
                    return True
                amount = 50 * ingr[1] if ingredient.Amount >= 50 * ingr[1] else 0
                Items.Move(ingredient, Player.Backpack, amount)
                Misc.Pause(self.Delay['drag'])

        return False
                    
    def Destocka(self):            
        todestock = 25 if self.TOBEMADE - self.COUNT >= 25 else self.TOBEMADE - self.COUNT
        
        if Items.BackpackCount(self.POT.ID, -1) >= todestock:
            
            if self.COUNT == 0:
                self.COUNT = Items.BackpackCount(self.POT.ID, -1)
            else:
                self.COUNT += Items.BackpackCount(self.POT.ID, -1)
                
            self.txtCount.Text = str(self.COUNT)
                
            itm = next(i for i in Player.Backpack.Contains if i.ItemID == self.POT.ID)
            
            if not itm is None:
                Items.Move(itm, self.CHEST, 0)
                Misc.Pause(self.Delay['drag'])

            if self.COUNT >= self.TOBEMADE:
                return True

        return False
    def DestockaReag(self):
        reag = [i for i in Player.Backpack.Contains if i.ItemID in self.Reags]
        for r in xrange(len(reag)):
            Items.Move(reag[r], self.CHEST, 0)
            Misc.Pause(self.Delay['drag'])
            
    def CheckTools(self):
        Gumps.ResetGump()
        while Items.BackpackCount(self.IDs['tool'], 0) < 2:
            
            if Items.BackpackCount(self.IDs['tool'], 0) == 0:
                return True
            
            Items.UseItemByID(self.IDs['tool'], 0)
            Gumps.WaitForGump(949095101, self.Delay['tout'])
            
            if not Gumps.LastGumpTextExist("scissors"):
                Gumps.SendAction(949095101, 8)
                Gumps.WaitForGump(949095101, self.Delay['tout'])
                
            Gumps.SendAction(949095101, 23)
            Gumps.WaitForGump(949095101, self.Delay['tout'])

        
        while Items.BackpackCount(self.IDs['mortar'], 0) == 0:
            Items.UseItemByID(self.IDs['tool'], 0)
            Gumps.WaitForGump(949095101, self.Delay['tout'])
            
            if not Gumps.LastGumpTextExist("scissors"):
                Gumps.SendAction(949095101, 8)
                Gumps.WaitForGump(949095101, self.Delay['tout'])
                
            Gumps.SendAction(949095101, 9)
            Gumps.WaitForGump(949095101, self.Delay['tout'])

    def SaveCheck(self):
        if Journal.Search("will save in"):
            Journal.Clear()
            Player.HeadMessage(33, "Incoming Save!") 
            while not Journal.Search("save complete"):
                Misc.Pause(self.Delay['base'])
            Player.HeadMessage(33, "Here we go!")
    
    def Main(self, num):
        while self.COUNT < self.TOBEMADE:
            if not self.Working:
                break
                
            if self.Destocka():
                break
            
            if self.Restocka() or self.CheckTools():
                break

            Gumps.ResetGump()
            Items.UseItemByID(self.IDs['mortar'], 0)
            Gumps.WaitForGump(949095101, self.Delay['tout'])
            
            if not Gumps.LastGumpTextExist(self.POT.Text):
                Gumps.SendAction(949095101, self.POT.Cat)
                Gumps.WaitForGump(949095101, self.Delay['tout'])
                
            Gumps.SendAction(949095101, self.POT.Sub)
            Gumps.WaitForGump(949095101, self.Delay['tout'])
        
        self.DestockaReag()    
        self.Working = False
    
    
AF = AlchemistForm()
Application.Run(AF)