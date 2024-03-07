#Need friends list named 'friend' !!!!!!!!!
### DO NOT ADD URSELF TO YOUR FRIENDS LIST
#### to run this u need a folder in your scripts folder named  'Scalpel'
from System import Int32
from time import sleep
from datetime import datetime
import clr, time, sys, System, math
clr.AddReference('System','System.Drawing','System.Windows.Forms','System.Data')
from System.Threading import ThreadStart, Thread
from System.Collections.Generic import List
from System import Byte, Environment 
from System.Drawing import *
from System.Windows.Forms import (Application, Button, Form, BorderStyle, Label, FlatStyle, DataGridView,
 DataGridViewAutoSizeColumnsMode, DataGridViewSelectionMode, DataGridViewEditMode, RadioButton, GroupBox,
 TextBox, CheckBox, ComboBox, ProgressBar,FormBorderStyle,SplitContainer,Orientation,DockStyle,TabControl,TabAlignment,TabPage,PictureBox,PictureBoxSizeMode,FormStartPosition)
from System import Random
rnd = Random()
from System.Data import DataTable
scriptfolder = str(Misc.CurrentScriptDirectory())

################################## BACKGROUND IMAGE ####################

#pathToFile1 = "/".join([scriptfolder, 'Scalpel', 'scal3.jpg'])
#Misc.SendMessage(pathToFile1)


##########################SKILL TRAINER STUFF ##############################
skillCatagories = ['Casting','Crafting','Thievery','Bard','Wilderness']
skillCasting = ['Magery','Mysticism','Necromancy']

####################### SMART TARGET STUFF ################### not implemented yet
beneSpells = ['In Mani','In Lor', 'Ex Uus', 'Uus Wis', 'An Nox', 'Uus Mani', 'Rel Sanct', 'Vas An Nox',
'In Vas Mani','An Lor Xen',
'Myrshalee', 'Haeldril', 'Olorisstra', 'Rauvvrae', 'Thalshara', 'Erelonia', 'Aslavdra', 'Orlavdra', 
'Tarisstree', 'Illorae', 'Alalithra', 'Nylisstra', 'Rathril', 'Anathrae', 'Haelyn', 'Nyraxle'
'Kal In Mani', 'In Corp Ylem', 'In Ort Ylem', 'An Ort Sanct', 'Kal Por Xen', 'In Zu', 'In Jux Por Ylem',
 'In Rel Ylem', 'Vas Zu', 'In Vas Ort Ex', 'Corp Por Ylem', 'In Vas Mani Hur', 'Kal Des Ylem',
 'Vas Rel Jux Ort', 'Grav Hur', 'Kal Vas Xen Corp Ylem']
 
##################  REPAIR CHECKER STUFF ##########
layers = ["RightHand","LeftHand","Shoes","Pants","Shirt","Head","Gloves","Ring","Neck","Waist",
"InnerTorso","Bracelet","MiddleTorso","Arms","Cloak","OuterTorso","OuterLegs","InnerLegs","Talisman"]
BFilter = Items.Filter()
BFilter.RangeMax = 3
BFilter.OnGround = True
BFilter.Enabled = True
BFilter.Movable = True
BFilter.Graphics = List[Int32]([0xA278, 0xA27F])

#########################MINI MAP STUFF ################# 
 
##format = name, leftX, topY, rightX, bottomY   
specialLocations = [
["Fire Docks",2907,3407,2964,3436],
["Fire Dungeon Halls",5671,1410,5823,1508],
["Isle of Mourn",2006,2055,2208,2194],    #for testing :P
['Outside Ice Dungeon',1908,49,2026,127],
["Despise Champ Spawn",5504,792,6691,970],
['Abyssal Spawn',6920,681,7057,826],
['Abyssal Spawn Hallway',7058,681,7160,826],
]
###################### ADD WEPS HERE !!!!!!!!    ################################
####format wep id,spec for 1 mob, spec for >1 Mobile,
#### use 0 for no special 1 for prim 2 for secondary

# with momentem selected will momentum if ability is set to 0 on more than one mob
   
smartWeps = [
[0x0F4B,1,2],#    daxe
[0x143F,0,1],#    halberd 
[0x26BD,1,0],#    bladed staff
[0x2D1F,0,2],#    magical shortbow
[0x26C2,1,1],#    composite bow
[0x406B,1,1],#     soul glave
[0xA28A,0,2],#whip
[0x27A5,1,1]#yumi  
]
ignoreMob = []
chaseIDs = []
honorIgnore = []
discordIgnore = []
provoIgnore = []
Journal.Clear()
Misc.SetSharedValue('run',True)

##########################################################

def go(x1, y1):
    Coords = PathFinding.Route() 
    Coords.X = x1
    Coords.Y = y1
    Coords.MaxRetry = 5
    PathFinding.Go(Coords)
    
def inKeyArea():
    pm = Player.Map
    ppx = Player.Position.X
    ppy = Player.Position.Y   
    for loc in specialLocations:
        if loc[1] < ppx < loc[3] and loc[2] < ppy < loc[4]:
            return loc[0]        
    return None      # return pm?
    
def isSpellBene():
    list = Journal.GetTextBySerial(Player.Serial)
    if len(list):
        lastInList = list[len(list) - 1]    
        #Misc.SendMessage(lastInList)        
        Journal.Clear()
        if lastInList in beneSpells:
            return True,lastInList
        else:
            return False,lastInList
    else:
        return False,'None'     
        
def access(fname):
    rv = False
    try:
        with open(fname, 'r') as f:
            rv = True
    except:
        pass
    return rv

def getenv(name):
    rv = str(Environment.GetEnvironmentVariable(name))
    return rv
    
def readRail(fileName):
    railCoords = []
    railfile = "/".join([scriptfolder, 'Scalpel', '{}.txt'.format(fileName)])
    with open(railfile) as file:
        rail = file.read()
        Misc.Pause(100)
        remove = ["[","]",","]
        for i in remove: 
            rail = rail.replace(i, '') 
        coords = rail.split(" ")
        x = 0
        y = 1
        while y <= len(coords):
            railCoords.append([int(coords[x]),int(coords[y])])
            x += 2
            y += 2
    return railCoords
    
def mobileDist(serial):
    mobile = Mobiles.FindBySerial(serial)
    if mobile:
        if mobile.Position:
            p1 = [Player.Position.X,Player.Position.Y]
            p2 = [mobile.Position.X,mobile.Position.Y]
            distance =int(math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) ))
            return distance
        else:       
            return 30
    else:       
        return 30
        
def selectNearest(list):
        if len(list)>0:
            nearestMob = list[0]
            leastDistance = mobileDist(list[0].Serial)
            for l in list:                
                dist = mobileDist(l.Serial)
                if dist < leastDistance:
                    nearestMob = l
                    leastDistance = mobileDist(l.Serial)
            #Mobiles.Message(nearestMob.Serial,288,"Script Selector {} tiles".format(str(self.mobileDist(nearestMob.Serial))))
            return nearestMob
        else:
            #Misc.SendMessage('No Mobs Found',48)
            return None            
    
#########################   MAIN FORM   ##############################################################################################    
    
class assistant(Form):
    ScriptName = 'RE Scalpel'
    
    def __init__(self):
        Form.__init__(self)        
#        self.setupImages()
        self.BackColor = Color.FromArgb(0,0,0)
        self.ForeColor = Color.FromArgb(231,231,231)
        self.Size = Size(250, 500)
        self.Text = '{}'.format(self.ScriptName)
        self.FormBorderStyle = FormBorderStyle.Fixed3D
        #self.CenterToScreen()
        self.StartPosition = FormStartPosition.Manual
        self.Location = Point(250,50)
        self.TopMost = True
        
        splitter = SplitContainer()
        splitter.Orientation = Orientation.Horizontal
        splitter.SplitterWidth =1
        splitter.Dock = DockStyle.Fill
        self.setupPanel(splitter.Panel1)
        self.setupTabPanel(splitter.Panel2)#,self.image1
        self.Controls.Add(splitter)
        self.Show()
        
    def setupImages(self):
        self.image1 = Image.FromFile(pathToFile1)
        
    def getPictureBox(self, image):
        pictureBox = PictureBox()
        pictureBox.SizeMode = PictureBoxSizeMode.StretchImage
        pictureBox.Image = image
        pictureBox.Dock = DockStyle.Fill
        return pictureBox 

    ###################### TOP OF SPLIT FORM ####################################################################
        
    def setupPanel(self,parent):
        

        ############################### START OF GROUP BOXES ##################       
        
        self.box = GroupBox()
        self.box.BackColor = Color.FromArgb(25,25,25)
        self.box.ForeColor = Color.FromArgb(100,150,250)
        self.box.Size = Size(225, 50)
        self.box.Location = Point(2, 5)
        self.box.Text = Player.Name      #add map or health bars here i dunno
        
        self.box1 = GroupBox()
        self.box1.BackColor = Color.FromArgb(25,25,25)
        self.box1.ForeColor = Color.FromArgb(100,150,250)
        self.box1.Size = Size(225, 50)
        self.box1.Location = Point(2, 55)
        self.box1.Text = "No Friend(s)"
        
        self.box2 = GroupBox()
        self.box2.BackColor = Color.FromArgb(25,25,25)
        self.box2.ForeColor = Color.FromArgb(233,131,23)
        self.box2.Size = Size(225, 50)
        self.box2.Location = Point(2, 105)
        self.box2.Text = "No Target"

        ############################### END OF GROUP BOXES ##################

        ###################### PROGRESS BARS ####################################
        
        self.hb = ProgressBar()
        self.hb.Minimum = 1
        self.hb.Maximum = 100
        self.hb.Step = 1
        self.hb.Value = 1
        self.hb.Location = Point(10, 20)
        self.hb.Width = 210
        self.hb.Height = 25    
        self.prog = self.hb
       
        self.fb = ProgressBar()
        self.fb.Minimum = 1
        self.fb.Maximum = 100
        self.fb.Step = 1
        self.fb.Value = 1
        self.fb.Location = Point(10,70)
        self.fb.Width = 210
        self.fb.Height = 25       
        self.prog = self.fb  
                       
        self.eb = ProgressBar()
        self.eb.Minimum = 1
        self.eb.Maximum = 100
        self.eb.Step = 1
        self.eb.Value = 1
        self.eb.Location = Point(10,120)
        self.eb.Width = 210
        self.eb.Height = 25       
        self.prog = self.eb 
        
        ############### END OF PROGRESS BARS #######################################

        ############### MAIN TOGGLE BUTTONS ###########################

        self.stopAttack = Button()
        self.stopAttack.Text = 'Attack On'
        self.stopAttack.BackColor = Color.FromArgb(10,100,10)
        self.stopAttack.Location = Point(5, 160)
        self.stopAttack.Size = Size(70, 30)
        self.stopAttack.FlatStyle = FlatStyle.Flat
        self.stopAttack.FlatAppearance.BorderSize = 1 
        self.stopAttack.Click += self.btnPressedEvent
            
        self.stopSpell = Button()
        self.stopSpell.Text = 'Spells On'
        self.stopSpell.BackColor = Color.FromArgb(10,100,10)
        self.stopSpell.Location = Point(80, 160)
        self.stopSpell.Size = Size(70, 30)
        self.stopSpell.FlatStyle = FlatStyle.Flat
        self.stopSpell.FlatAppearance.BorderSize = 1 
        self.stopSpell.Click += self.btnPressedEvent
        
        self.stopSkill = Button()
        self.stopSkill.Text = 'Skills On'
        self.stopSkill.BackColor = Color.FromArgb(10,100,10)
        self.stopSkill.Location = Point(155, 160)
        self.stopSkill.Size = Size(70, 30)
        self.stopSkill.FlatStyle = FlatStyle.Flat
        self.stopSkill.FlatAppearance.BorderSize = 1 
        self.stopSkill.Click += self.btnPressedEvent
        
        self.stopAction = Button()
        self.stopAction.Text = 'Actions On'
        self.stopAction.BackColor = Color.FromArgb(10,100,10)
        self.stopAction.Location = Point(5, 195)
        self.stopAction.Size = Size(70, 30)
        self.stopAction.FlatStyle = FlatStyle.Flat
        self.stopAction.FlatAppearance.BorderSize = 1 
        self.stopAction.Click += self.btnPressedEvent
        
        self.stopOther = Button()
        self.stopOther.Text = 'Other On'
        self.stopOther.BackColor = Color.FromArgb(10,100,10)
        self.stopOther.Location = Point(80, 195)
        self.stopOther.Size = Size(70,30)
        self.stopOther.FlatStyle = FlatStyle.Flat
        self.stopOther.FlatAppearance.BorderSize = 1 
        self.stopOther.Click += self.btnPressedEvent
        
        self.stopMaster = Button()
        self.stopMaster.Text = 'Stop All'
        self.stopMaster.BackColor = Color.FromArgb(10,100,10)
        self.stopMaster.Location = Point(155, 195)
        self.stopMaster.Size = Size(70, 30)
        self.stopMaster.FlatStyle = FlatStyle.Flat
        self.stopMaster.FlatAppearance.BorderSize = 1 
        self.stopMaster.Click += self.btnPressedEvent

        ######################## END OF MAIN TOGGLE BUTTONS ###########################


        ############## ADD TO TOP OF SPLIT FORM ###########################################        
        parent.Controls.Add(self.stopAttack)
        parent.Controls.Add(self.stopSpell)
        parent.Controls.Add(self.stopSkill)
        parent.Controls.Add(self.stopAction)
        parent.Controls.Add(self.stopOther)
        parent.Controls.Add(self.stopMaster)
        parent.Controls.Add(self.fb)
        parent.Controls.Add(self.eb)
        parent.Controls.Add(self.hb)
        parent.Controls.Add(self.box2)
        parent.Controls.Add(self.box1)
        parent.Controls.Add(self.box)
        
    ########################## END OF TOP OF SPLIT FORM #########################################################
        
    ############################ START OF BOTTOM OF SPLIT FORM #####################################################

    ################################ TAB PANEL SETUP   #####################################################################
        
    def setupTabPanel(self,parent):#,image
        self.tabControl = TabControl()        
        self.tabControl.Dock = DockStyle.Fill
        self.tabControl.Alignment = TabAlignment.Top
        
        ##################  ATTACK TAB   ######################################  
        
        attackPage = TabPage()
        attackPage.Text = 'Attack'
        attackPage.BackColor = Color.FromArgb(0,0,0)
        
        self.meleeRad = RadioButton()
        self.meleeRad.Text = 'Melee'
        self.meleeRad.Checked = False
        self.meleeRad.Location = Point(35, 12)
        self.meleeRad.Size = Size(75, 20)
        attackPage.Controls.Add(self.meleeRad)
        
        self.rangeRad = RadioButton()
        self.rangeRad.Text = 'Ranged'
        self.rangeRad.Checked = False
        self.rangeRad.BackColor = Color.FromArgb(0,0,0)
        self.rangeRad.Location = Point(120,12)
        self.rangeRad.Size = Size(85, 20)
        attackPage.Controls.Add(self.rangeRad)
        
        self.attackBox = GroupBox()

        self.attackBox.Size = Size(218, 40)
        self.attackBox.Location = Point(2,0)
        attackPage.Controls.Add(self.attackBox)
        
        ### row 1
   
        self.primChk = CheckBox()
        self.primChk.Text = 'Primary Loop'
        self.primChk.Checked = False
        self.primChk.BackColor = Color.FromArgb(0,0,0)
        self.primChk.Location = Point(15, 45)
        self.primChk.Size = Size(100, 20)
        attackPage.Controls.Add(self.primChk) 
        
        self.secChk = CheckBox()
        self.secChk.Text = 'Secondary Loop'
        self.secChk.Checked = False
        self.secChk.BackColor = Color.FromArgb(0,0,0)
        self.secChk.Location = Point(15, 65)
        self.secChk.Size = Size(110, 20)
        attackPage.Controls.Add(self.secChk)
        
        ##### row 2
        
        self.specChk = CheckBox()
        self.specChk.Text = 'Smart Spec'
        self.specChk.Checked = False
        self.specChk.BackColor = Color.FromArgb(0,0,0)
        self.specChk.Location = Point(130, 45)
        self.specChk.Size = Size(100, 20)
        attackPage.Controls.Add(self.specChk)
 
        self.momChk = CheckBox()
        self.momChk.Text = 'Momentum'
        self.momChk.Checked = False
        self.momChk.BackColor = Color.FromArgb(0,0,0)
        self.momChk.Location = Point(130, 65)
        self.momChk.Size = Size(85, 20)
        attackPage.Controls.Add(self.momChk)
 
        ########### dress buttons 
        
        self.reptileBtn = Button()
        self.reptileBtn.Text = 'Reptile'
        self.reptileBtn.BackColor = Color.FromArgb(25,50,25)
        self.reptileBtn.Location = Point(83, 140)
        self.reptileBtn.Size = Size(55, 25)
        self.reptileBtn.FlatStyle = FlatStyle.Flat
        self.reptileBtn.FlatAppearance.BorderSize = 1         
        self.reptileBtn.Click += self.btnPressedEvent
        attackPage.Controls.Add(self.reptileBtn)
        
        self.demonBtn = Button()
        self.demonBtn.Text = 'Demon'
        self.demonBtn.BackColor = Color.FromArgb(50,24,25)
        self.demonBtn.Location = Point(28, 140)
        self.demonBtn.Size = Size(55, 25)
        self.demonBtn.FlatStyle = FlatStyle.Flat
        self.demonBtn.FlatAppearance.BorderSize = 1
        self.demonBtn.Click += self.btnPressedEvent
        attackPage.Controls.Add(self.demonBtn)
        
        self.undeadBtn = Button()
        self.undeadBtn.Text = 'Undead'
        self.undeadBtn.BackColor = Color.FromArgb(50,25,25)
        self.undeadBtn.Location = Point(138, 140)
        self.undeadBtn.Size = Size(55, 25)
        self.undeadBtn.FlatStyle = FlatStyle.Flat
        self.undeadBtn.FlatAppearance.BorderSize = 1         
        self.undeadBtn.Click += self.btnPressedEvent
        attackPage.Controls.Add(self.undeadBtn)
        
        self.eleBtn = Button()
        self.eleBtn.Text = 'Elemen'
        self.eleBtn.BackColor = Color.FromArgb(25,50,25)
        self.eleBtn.Location = Point(28, 165)
        self.eleBtn.Size = Size(55, 25)
        self.eleBtn.FlatStyle = FlatStyle.Flat
        self.eleBtn.FlatAppearance.BorderSize = 1 
        self.eleBtn.Click += self.btnPressedEvent
        attackPage.Controls.Add(self.eleBtn)
        
        self.arachBtn = Button()
        self.arachBtn.Text = 'Arach'
        self.arachBtn.BackColor = Color.FromArgb(50,25,25)
        self.arachBtn.Location = Point(83, 165)
        self.arachBtn.Size = Size(55, 25)
        self.arachBtn.FlatStyle = FlatStyle.Flat
        self.arachBtn.FlatAppearance.BorderSize = 1 
        self.arachBtn.Click += self.btnPressedEvent
        attackPage.Controls.Add(self.arachBtn)
        
        self.repondBtn = Button()
        self.repondBtn.Text = 'Repond'
        self.repondBtn.BackColor = Color.FromArgb(25,50,25)
        self.repondBtn.Location = Point(138, 165)
        self.repondBtn.Size = Size(55, 25)
        self.repondBtn.FlatStyle = FlatStyle.Flat
        self.repondBtn.FlatAppearance.BorderSize = 1 
        self.repondBtn.Click += self.btnPressedEvent        
        attackPage.Controls.Add(self.repondBtn)
        
        self.mainDressBtn = Button()
        self.mainDressBtn.Text = 'Main'
        self.mainDressBtn.BackColor = Color.FromArgb(25,50,25)
        self.mainDressBtn.Location = Point(28, 90)
        self.mainDressBtn.Size = Size(165, 25)
        self.mainDressBtn.FlatStyle = FlatStyle.Flat
        self.mainDressBtn.FlatAppearance.BorderSize = 1 
        self.mainDressBtn.Click += self.btnPressedEvent
        attackPage.Controls.Add(self.mainDressBtn)
        
        self.luckBtn = Button()
        self.luckBtn.Text = 'Luck'
        self.luckBtn.BackColor = Color.FromArgb(50,50,10)
        self.luckBtn.Location = Point(28, 115)
        self.luckBtn.Size = Size(165, 25)
        self.luckBtn.FlatStyle = FlatStyle.Flat
        self.luckBtn.FlatAppearance.BorderSize = 1 
        self.luckBtn.Click += self.btnPressedEvent
        attackPage.Controls.Add(self.luckBtn)
        self.tabControl.TabPages.Add(attackPage)
                        
        ##################   SPELLS TAB  ##################################### 
        
        spellsPage = TabPage()
        spellsPage.Text = 'Spells'
        spellsPage.BackColor = Color.FromArgb(0,0,0)
        self.tabControl.TabPages.Add(spellsPage)
        
        ###row 1 
        
        self.eooChk = CheckBox()
        self.eooChk.Text = 'EoO'
        self.eooChk.Checked = False
        self.eooChk.BackColor = Color.FromArgb(0,0,0)
        self.eooChk.Location = Point(5, 5)
        self.eooChk.Size = Size(85, 20)
        spellsPage.Controls.Add(self.eooChk)
        
        self.consChk = CheckBox()
        self.consChk.Text = 'Con Wep'
        self.consChk.Checked = False
        self.consChk.BackColor = Color.FromArgb(0,0,0)
        self.consChk.Location = Point(5, 25)
        self.consChk.Size = Size(85, 20)
        spellsPage.Controls.Add(self.consChk)
        
        self.devChk = CheckBox()
        self.devChk.Text = 'Dev Fury'
        self.devChk.Checked = False
        self.devChk.BackColor = Color.FromArgb(0,0,0)
        self.devChk.Location = Point(5, 45)
        self.devChk.Size = Size(75, 20)
        spellsPage.Controls.Add(self.devChk)
        
        self.devTxt = TextBox()
        self.devTxt.Text = "70"
        self.devTxt.Location = Point(80,45)
        self.devTxt.Width = 20
        self.devTxt.BackColor = Color.FromArgb(25,25,25)
        self.devTxt.ForeColor = Color.FromArgb(255,255,255)
        spellsPage.Controls.Add(self.devTxt)
                        
        self.percentLbl = Label()
        self.percentLbl.Text = "%"
        self.percentLbl.Location = Point(100,47)
        self.percentLbl.Size = Size(12, 15)
        self.percentLbl.ForeColor = Color.FromArgb(255,255,255)
        spellsPage.Controls.Add(self.percentLbl)
        
        self.confidenceChk = CheckBox()
        self.confidenceChk.Text = 'Conf'
        self.confidenceChk.Checked = False
        self.confidenceChk.BackColor = Color.FromArgb(0,0,0)
        self.confidenceChk.Location = Point(5, 65)
        self.confidenceChk.Size = Size(60, 20)
        spellsPage.Controls.Add(self.confidenceChk)
        
        self.confidenceTxt = TextBox()
        self.confidenceTxt.Text = "70"
        self.confidenceTxt.Location = Point(80,65)
        self.confidenceTxt.Width = 20
        self.confidenceTxt.BackColor = Color.FromArgb(25,25,25)
        self.confidenceTxt.ForeColor = Color.FromArgb(255,255,255)
        spellsPage.Controls.Add(self.confidenceTxt)
        
        self.percentLbl1 = Label()
        self.percentLbl1.Text = "%"
        self.percentLbl1.Location = Point(100,67)
        self.percentLbl1.Size = Size(12, 15)
        self.percentLbl1.ForeColor = Color.FromArgb(255,255,255)
        spellsPage.Controls.Add(self.percentLbl1)
        
        self.evaChk = CheckBox()
        self.evaChk.Text = 'Evade'
        self.evaChk.Checked = False
        self.evaChk.BackColor = Color.FromArgb(0,0,0)
        self.evaChk.Location = Point(5, 85)
        self.evaChk.Size = Size(60, 20)
        spellsPage.Controls.Add(self.evaChk)
        
        self.evaTxt = TextBox()
        self.evaTxt.Text = "90"
        self.evaTxt.Location = Point(80,85)
        self.evaTxt.Width = 20
        self.evaTxt.BackColor = Color.FromArgb(25,25,25)
        self.evaTxt.ForeColor = Color.FromArgb(255,255,255)
        spellsPage.Controls.Add(self.evaTxt)
        
        self.percentLbl2 = Label()
        self.percentLbl2.Text = "%"
        self.percentLbl2.Location = Point(100,87)
        self.percentLbl2.Size = Size(12, 15)
        self.percentLbl2.ForeColor = Color.FromArgb(255,255,255)
        spellsPage.Controls.Add(self.percentLbl2)
        
        self.caChk = CheckBox()
        self.caChk.Text = 'Cntr Attack'
        self.caChk.Checked = False
        self.caChk.BackColor = Color.FromArgb(0,0,0)
        self.caChk.Location = Point(5, 105)
        self.caChk.Size = Size(85, 20)
        spellsPage.Controls.Add(self.caChk)
                
        self.cwChk = CheckBox()
        self.cwChk.Text = 'Curse Wep'
        self.cwChk.Checked = False
        self.cwChk.BackColor = Color.FromArgb(0,0,0)
        self.cwChk.Location = Point(5, 125)
        self.cwChk.Size = Size(85, 20)
        spellsPage.Controls.Add(self.cwChk)
        
        self.masteryChk = CheckBox()
        self.masteryChk.Text = 'Mastery'
        self.masteryChk.Checked = False
        self.masteryChk.BackColor = Color.FromArgb(0,0,0)
        self.masteryChk.Location = Point(5, 145)
        self.masteryChk.Size = Size(85, 20)
        spellsPage.Controls.Add(self.masteryChk)
                        
        self.masteryCombo = ComboBox()
        self.masteryCombo.Location = Point(5, 165)
        self.masteryCombo.DataSource = "Onslaught","Peace","Provo","Body Guard"
        self.masteryCombo.BackColor = Color.FromArgb(0,0,0)
        self.masteryCombo.ForeColor = Color.FromArgb(231,231,231)
        self.masteryCombo.Width = 100
        spellsPage.Controls.Add(self.masteryCombo)
                
        ##row 2
        
        self.invisChk = CheckBox()
        self.invisChk.Text = 'Stay Invis'
        self.invisChk.Checked = False
        self.invisChk.BackColor = Color.FromArgb(0,0,0)
        self.invisChk.Location = Point(115, 5)
        self.invisChk.Size = Size(85, 20)
        spellsPage.Controls.Add(self.invisChk)
        
        self.mageXHealChk = CheckBox()
        self.mageXHealChk.Text = 'Mage XHeal'
        self.mageXHealChk.Checked = False
        self.mageXHealChk.BackColor = Color.FromArgb(0,0,0)
        self.mageXHealChk.Location = Point(115, 25)
        self.mageXHealChk.Size = Size(95, 20)
        spellsPage.Controls.Add(self.mageXHealChk)
        
        self.mageHealChk = CheckBox()
        self.mageHealChk.Text = 'Heal Self'
        self.mageHealChk.Checked = False
        self.mageHealChk.BackColor = Color.FromArgb(0,0,0)
        self.mageHealChk.Location = Point(115, 45)
        self.mageHealChk.Size = Size(69, 20)
        spellsPage.Controls.Add(self.mageHealChk)
        
        self.mageHealTxt = TextBox()
        self.mageHealTxt.Text = "90"
        self.mageHealTxt.Location = Point(183,45)
        self.mageHealTxt.Width = 25
        self.mageHealTxt.BackColor = Color.FromArgb(25,25,25)
        self.mageHealTxt.ForeColor = Color.FromArgb(255,255,255)
        spellsPage.Controls.Add(self.mageHealTxt)
        
        self.percent2Lbl = Label()
        self.percent2Lbl.Text = "%"
        self.percent2Lbl.Location = Point(208,47)
        self.percent2Lbl.Size = Size(12, 40)
        self.percent2Lbl.ForeColor = Color.FromArgb(255,255,255)
        spellsPage.Controls.Add(self.percent2Lbl)
        
        self.witherChk = CheckBox()
        self.witherChk.Text = 'Wither'
        self.witherChk.Checked = False
        self.witherChk.BackColor = Color.FromArgb(0,0,0)
        self.witherChk.Location = Point(115, 65)
        self.witherChk.Size = Size(95, 20)
        spellsPage.Controls.Add(self.witherChk)
        
        self.thunderChk = CheckBox()
        self.thunderChk.Text = 'ThndrStrm'
        self.thunderChk.Checked = False
        self.thunderChk.BackColor = Color.FromArgb(0,0,0)
        self.thunderChk.Location = Point(115, 85)
        self.thunderChk.Size = Size(95, 20)
        spellsPage.Controls.Add(self.thunderChk)
        
        self.vampChk = CheckBox()
        self.vampChk.Text = 'Vamp Emb'
        self.vampChk.Checked = False
        self.vampChk.BackColor = Color.FromArgb(0,0,0)
        self.vampChk.Location = Point(115, 105)
        self.vampChk.Size = Size(95, 20)
        spellsPage.Controls.Add(self.vampChk)
        
        self.honorChk = CheckBox()
        self.honorChk.Text = 'Honor'
        self.honorChk.Checked = False
        self.honorChk.BackColor = Color.FromArgb(0,0,0)
        self.honorChk.Location = Point(115, 125)
        self.honorChk.Size = Size(85, 20)
        spellsPage.Controls.Add(self.honorChk)
        
        self.allKillChk = CheckBox()
        self.allKillChk.Text = 'Pet All Kill'
        self.allKillChk.Checked = False
        self.allKillChk.BackColor = Color.FromArgb(0,0,0)
        self.allKillChk.Location = Point(115,145)
        self.allKillChk.Size = Size(75, 20)        
        spellsPage.Controls.Add(self.allKillChk)
       
        self.allKillTxt = TextBox()
        self.allKillTxt.Text = "5"
        self.allKillTxt.Location = Point(190,145)
        self.allKillTxt.Width = 18
        self.allKillTxt.BackColor = Color.FromArgb(25,25,25)
        self.allKillTxt.ForeColor = Color.FromArgb(255,255,255)
        spellsPage.Controls.Add(self.allKillTxt)
        
        self.allKillLbl = Label()
        self.allKillLbl.Text = "s"
        self.allKillLbl.Location = Point(208,147)
        self.allKillLbl.Size = Size(12, 40)
        self.allKillLbl.ForeColor = Color.FromArgb(255,255,255)
        spellsPage.Controls.Add(self.allKillLbl)
        
        #spellsPage.Controls.Add(self.getPictureBox(image))
                
        ###################  SKILLS TAB    #######################################
        
        skillsPage = TabPage()
        skillsPage.Text = 'Skills'
        skillsPage.BackColor = Color.FromArgb(0,0,0)
        self.tabControl.TabPages.Add(skillsPage)
                
               
        self.skillTypeCombo = ComboBox()
        self.skillTypeCombo.Location = Point(5, 175)
        self.skillTypeCombo.DataSource = skillCatagories
        self.skillTypeCombo.BackColor = Color.FromArgb(0,0,0)
        self.skillTypeCombo.ForeColor = Color.FromArgb(231,231,231)
        self.skillTypeCombo.Width = 70
        self.skillTypeCombo.SelectedIndexChanged += self.btnPressedEvent
        skillsPage.Controls.Add(self.skillTypeCombo)
        
        self.skillCombo = ComboBox()
        self.skillCombo.Location = Point(75, 175)
        self.skillCombo.DataSource = skillCasting
        self.skillCombo.BackColor = Color.FromArgb(0,0,0)
        self.skillCombo.ForeColor = Color.FromArgb(231,231,231)
        self.skillCombo.Width = 100
        skillsPage.Controls.Add(self.skillCombo)
        
        self.skillStopTxt = TextBox()
        self.skillStopTxt.Location = Point(180, 175)
        self.skillStopTxt.Size = Size(40, 80)
        self.skillStopTxt.Text = '120.0'
        self.skillStopTxt.BackColor = Color.FromArgb(0,0,0)
        self.skillStopTxt.ForeColor = Color.FromArgb(231,231,231)
        skillsPage.Controls.Add(self.skillStopTxt)
        
        self.skillLbl = Label()
        self.skillLbl.Location = Point(5, 160)
        self.skillLbl.Size = Size(210, 20)
        self.skillLbl.Text = 'Skill Type       Skill                          Stop at'
        self.skillLbl.BackColor = Color.FromArgb(0,0,0)
        self.skillLbl.ForeColor = Color.FromArgb(100,100,231)
        skillsPage.Controls.Add(self.skillLbl)
        
        self.skillChk = RadioButton()
        self.skillChk.Text = 'Enable Training'
        self.skillChk.Checked = False
        self.skillChk.BackColor = Color.FromArgb(0,0,0)
        self.skillChk.Location = Point(5,135)
        self.skillChk.Size = Size(105, 20)
        skillsPage.Controls.Add(self.skillChk)
        
        self.skillInstructions = Button()
        self.skillInstructions.Text = 'Instructions'
        self.skillInstructions.BackColor = Color.FromArgb(10,100,200)
        self.skillInstructions.Location = Point(115, 132)
        self.skillInstructions.Size = Size(90, 25)
        self.skillInstructions.FlatStyle = FlatStyle.Flat
        self.skillInstructions.FlatAppearance.BorderSize = 1 
        self.skillInstructions.Click += self.btnPressedEvent
        skillsPage.Controls.Add(self.skillInstructions)
        
        

        ######## row 1
        
        self.peaceChk = RadioButton()
        self.peaceChk.Text = 'Area Peace'
        self.peaceChk.Checked = False
        self.peaceChk.BackColor = Color.FromArgb(0,0,0)
        self.peaceChk.Location = Point(5, 5)
        self.peaceChk.Size = Size(85, 20)
        skillsPage.Controls.Add(self.peaceChk)
        
        self.provoChk = RadioButton()
        self.provoChk.Text = 'Provoke'
        self.provoChk.Checked = False
        self.provoChk.BackColor = Color.FromArgb(0,0,0)
        self.provoChk.Location = Point(5, 25)
        self.provoChk.Size = Size(85, 20)
        skillsPage.Controls.Add(self.provoChk)

        self.discordChk = RadioButton()
        self.discordChk.Text = 'Discord'
        self.discordChk.Checked = False
        self.discordChk.BackColor = Color.FromArgb(0,0,0)
        self.discordChk.Location = Point(5, 45)
        self.discordChk.Size = Size(85, 20)
        skillsPage.Controls.Add(self.discordChk)        
        
        ####### row 2
        self.hideChk = RadioButton()
        self.hideChk.Text = 'Stay Hidden'
        self.hideChk.Checked = False
        self.hideChk.BackColor = Color.FromArgb(0,0,0)
        self.hideChk.Location = Point(120, 5)
        self.hideChk.Size = Size(85, 20)
        skillsPage.Controls.Add(self.hideChk)
        
        self.detectChk = RadioButton()
        self.detectChk.Text = 'Detect Hidden'
        self.detectChk.Checked = False
        self.detectChk.BackColor = Color.FromArgb(0,0,0)
        self.detectChk.Location = Point(120, 25)
        self.detectChk.Size = Size(100, 20)
        skillsPage.Controls.Add(self.detectChk)
        

        #skillsPage.Controls.Add(self.getPictureBox(image))
        
        ########################### ACTIONS TAB  #################################
        
        actionsPage = TabPage()
        actionsPage.Text = 'Actions'
        actionsPage.BackColor = Color.FromArgb(0,0,0)
        self.tabControl.TabPages.Add(actionsPage)
        
        self.tbChk = CheckBox()
        self.tbChk.Text = 'Auto T-Box'
        self.tbChk.Checked = False
        self.tbChk.BackColor = Color.FromArgb(0,0,0)
        self.tbChk.Location = Point(5, 5)
        self.tbChk.Size = Size(85, 20)
        actionsPage.Controls.Add(self.tbChk)
        
        self.hChk = CheckBox()
        self.hChk.Text = 'Heal Pot'
        self.hChk.Checked = False
        self.hChk.BackColor = Color.FromArgb(0,0,0)
        self.hChk.Location = Point(5, 25)
        self.hChk.Size = Size(68, 20)
        actionsPage.Controls.Add(self.hChk)
        
        self.hTxt = TextBox()
        self.hTxt.Text = "50"
        self.hTxt.Location = Point(72,25)
        self.hTxt.Width = 25
        self.hTxt.BackColor = Color.FromArgb(25,25,25)
        self.hTxt.ForeColor = Color.FromArgb(255,255,255)
        actionsPage.Controls.Add(self.hTxt)
        
        self.hLbl = Label()
        self.hLbl.Text = "%"
        self.hLbl.Location = Point(95,29)
        self.hLbl.Size = Size(12, 20)
        self.hLbl.ForeColor = Color.FromArgb(255,255,255)
        actionsPage.Controls.Add(self.hLbl)

        self.cChk = CheckBox()
        self.cChk.Text = 'Cure Pot'
        self.cChk.Checked = False
        self.cChk.BackColor = Color.FromArgb(0,0,0)
        self.cChk.Location = Point(5, 45)
        self.cChk.Size = Size(85, 20)
        actionsPage.Controls.Add(self.cChk)
        
        self.apChk = CheckBox()
        self.apChk.Text = 'Apple'
        self.apChk.Checked = False
        self.apChk.BackColor = Color.FromArgb(0,0,0)
        self.apChk.Location = Point(5, 65)
        self.apChk.Size = Size(85, 20)
        actionsPage.Controls.Add(self.apChk)
        
        self.ojChk = CheckBox()
        self.ojChk.Text = 'Oj Petal'
        self.ojChk.Checked = False
        self.ojChk.BackColor = Color.FromArgb(0,0,0)
        self.ojChk.Location = Point(5, 85)
        self.ojChk.Size = Size(85, 20)
        actionsPage.Controls.Add(self.ojChk)
        
        self.roseChk = CheckBox()
        self.roseChk.Text = 'Rose of Trins'
        self.roseChk.Checked = False
        self.roseChk.BackColor = Color.FromArgb(0,0,0)
        self.roseChk.Location = Point(5, 105)
        self.roseChk.Size = Size(105, 20)
        actionsPage.Controls.Add(self.roseChk)
        
        self.armChk = CheckBox()
        self.armChk.Text = 'Rearm'
        self.armChk.Checked = False
        self.armChk.BackColor = Color.FromArgb(0,0,0)
        self.armChk.Location = Point(5, 125)
        self.armChk.Size = Size(85, 20)
        actionsPage.Controls.Add(self.armChk)
        
        self.bandageChk = CheckBox()
        self.bandageChk.Text = 'Band Heal'
        self.bandageChk.Checked = False
        self.bandageChk.BackColor = Color.FromArgb(0,0,0)
        self.bandageChk.Location = Point(5, 145)
        self.bandageChk.Size = Size(78, 20)
        actionsPage.Controls.Add(self.bandageChk)

        self.bandageTxt = TextBox()
        self.bandageTxt.Text = "90"
        self.bandageTxt.Location = Point(82,145)
        self.bandageTxt.Width = 20
        self.bandageTxt.BackColor = Color.FromArgb(25,25,25)
        self.bandageTxt.ForeColor = Color.FromArgb(255,255,255)
        actionsPage.Controls.Add(self.bandageTxt)
        
        self.bLbl = Label()
        self.bLbl.Text = "%"
        self.bLbl.Location = Point(102,149)
        self.bLbl.Size = Size(12, 20)
        self.bLbl.ForeColor = Color.FromArgb(255,255,255)
        actionsPage.Controls.Add(self.bLbl)
        
        self.bandageCombo = ComboBox()
        self.bandageCombo.Location = Point(5, 165)
        self.bandageCombo.DataSource = "Friend/Self","Self","Friend"
        self.bandageCombo.BackColor = Color.FromArgb(0,0,0)
        self.bandageCombo.ForeColor = Color.FromArgb(231,231,231)
        self.bandageCombo.Width = 100
        actionsPage.Controls.Add(self.bandageCombo)

        
        ##################### ROW 2 ################
        
        self.bombardChk = CheckBox()
        self.bombardChk.ForeColor = Color.FromArgb(100,100,100)
        self.bombardChk.Text = 'Bombard'
        self.bombardChk.Checked = False
        self.bombardChk.BackColor = Color.FromArgb(0,0,0)
        self.bombardChk.Location = Point(115, 5)
        self.bombardChk.Size = Size(70, 20)
        actionsPage.Controls.Add(self.bombardChk)
        
        self.bombardTxt = TextBox()
        self.bombardTxt.Text = "10"
        self.bombardTxt.Location = Point(184,5)
        self.bombardTxt.Width = 20
        self.bombardTxt.BackColor = Color.FromArgb(25,25,25)
        self.bombardTxt.ForeColor = Color.FromArgb(255,255,255)
        actionsPage.Controls.Add(self.bombardTxt)
        
        self.bLbl = Label()
        self.bLbl.Text = "%"
        self.bLbl.Location = Point(203,7)
        self.bLbl.Size = Size(14, 20)
        self.bLbl.ForeColor = Color.FromArgb(255,255,255)
        actionsPage.Controls.Add(self.bLbl)
        
        self.shurChk = CheckBox()
        self.shurChk.Text = 'Shur/Fuki'
        self.shurChk.ForeColor = Color.FromArgb(100,100,100)
        self.shurChk.Checked = False
        self.shurChk.BackColor = Color.FromArgb(0,0,0)
        self.shurChk.Location = Point(115, 25)
        self.shurChk.Size = Size(85, 20)
        actionsPage.Controls.Add(self.shurChk)

        self.conflagChk = CheckBox()
        self.conflagChk.ForeColor = Color.FromArgb(100,100,100)
        self.conflagChk.Text = 'Conflag'
        self.conflagChk.Checked = False
        self.conflagChk.BackColor = Color.FromArgb(0,0,0)
        self.conflagChk.Location = Point(115, 45)
        self.conflagChk.Size = Size(85, 20)
        actionsPage.Controls.Add(self.conflagChk)
        
        self.novaChk = CheckBox()
        self.novaChk.ForeColor = Color.FromArgb(100,100,100)
        self.novaChk.Text = 'Nova'
        self.novaChk.Checked = False
        self.novaChk.BackColor = Color.FromArgb(0,0,0)
        self.novaChk.Location = Point(115, 65)
        self.novaChk.Size = Size(85, 20)
        actionsPage.Controls.Add(self.novaChk)
        
        self.solChk = CheckBox()
        self.solChk.ForeColor = Color.FromArgb(100,100,100)
        self.solChk.Text = 'Seed Life'
        self.solChk.Checked = False
        self.solChk.BackColor = Color.FromArgb(0,0,0)
        self.solChk.Location = Point(115, 85)
        self.solChk.Size = Size(85, 20)
        actionsPage.Controls.Add(self.solChk)
        
                
        self.activeChk = CheckBox()
        self.activeChk.Text = 'Stay Active'
        self.activeChk.Checked = False
        self.activeChk.BackColor = Color.FromArgb(0,0,0)
        self.activeChk.Location = Point(115, 165)
        self.activeChk.Size = Size(85, 20)
        actionsPage.Controls.Add(self.activeChk)
        
        
        #actionsPage.Controls.Add(self.getPictureBox(image))
        
        #####################   OTHER TAB   ##########################################
        
        otherPage = TabPage()
        otherPage.Text = 'Other'
        otherPage.BackColor = Color.FromArgb(25,25,25)
        self.tabControl.TabPages.Add(otherPage)
        
        self.box3 = GroupBox()
        self.box3.BackColor = Color.FromArgb(25,25,25)
        self.box3.ForeColor = Color.FromArgb(23,221,23)
        self.box3.Size = Size(218, 104)
        self.box3.Text = 'Chase Mobile and Rail Options'

        
        self.chaseChk = CheckBox()
        self.chaseChk.Text = 'On/Off'
        self.chaseChk.Checked = False
        self.chaseChk.BackColor = Color.FromArgb(25,25,25)
        self.chaseChk.Location = Point(10, 25)
        self.chaseChk.Size = Size(60, 20)
        otherPage.Controls.Add(self.chaseChk)
        
        self.chaseIdChk = CheckBox()
        self.chaseIdChk.Text = 'Chase by ID'
        self.chaseIdChk.Checked = False
        self.chaseIdChk.BackColor = Color.FromArgb(25,25,25)
        self.chaseIdChk.Location = Point(70, 13)
        self.chaseIdChk.Size = Size(90, 20)
        otherPage.Controls.Add(self.chaseIdChk)
        
        self.delayTxt = TextBox()
        self.delayTxt.Text = "Delay (ms)"
        self.delayTxt.Location = Point(70,32 )
        self.delayTxt.Width = 80
        self.delayTxt.BackColor = Color.FromArgb(25,25,25)
        self.delayTxt.ForeColor = Color.FromArgb(255,255,255)
        otherPage.Controls.Add(self.delayTxt)
        
        self.chaseBtn = Button()
        self.chaseBtn.Text ='Add ID'
        self.chaseBtn.BackColor = Color.FromArgb(10,100,100)
        self.chaseBtn.Location = Point(165, 15)
        self.chaseBtn.Size = Size(50, 29)
        self.chaseBtn.FlatStyle = FlatStyle.Flat
        self.chaseBtn.FlatAppearance.BorderSize = 1 
        self.chaseBtn.Click += self.btnPressedEvent
        otherPage.Controls.Add(self.chaseBtn)
        
        self.railChk = CheckBox()        
        self.railChk.Text = 'On/Off'
        self.railChk.Checked = False
        self.railChk.BackColor = Color.FromArgb(25,25,25)
        self.railChk.Location = Point(10, 72)
        self.railChk.Size = Size(60, 20)
        otherPage.Controls.Add(self.railChk)
        
        self.railTxt = TextBox()
        if Misc.ReadSharedValue("railname"):
            self.railTxt.Text = Misc.ReadSharedValue("railname")
        else:
            self.railTxt.Text = "Rail_Name"
        self.railTxt.Location = Point(100,70 )
        self.railTxt.Width = 100
        self.railTxt.BackColor = Color.FromArgb(25,25,25)
        self.railTxt.ForeColor = Color.FromArgb(255,255,255)
        otherPage.Controls.Add(self.railTxt)
        ### row 1
        
        self.railRecBtn = Button()
        self.railRecBtn.Text = 'Open Rail Rec'
        self.railRecBtn.BackColor = Color.FromArgb(10,100,100)
        self.railRecBtn.Location = Point(3, 165)
        self.railRecBtn.Size = Size(98, 30)
        self.railRecBtn.FlatStyle = FlatStyle.Flat
        self.railRecBtn.FlatAppearance.BorderSize = 1 
        self.railRecBtn.Click += self.btnPressedEvent
        otherPage.Controls.Add(self.railRecBtn)
        
        self.friendBtn = Button()
        self.friendBtn.Text = 'Add Friend'
        self.friendBtn.BackColor = Color.FromArgb(10,100,100)
        self.friendBtn.Location = Point(3, 100)
        self.friendBtn.Size = Size(98, 30)
        self.friendBtn.FlatStyle = FlatStyle.Flat
        self.friendBtn.FlatAppearance.BorderSize = 1 
        self.friendBtn.Click += self.btnPressedEvent
        otherPage.Controls.Add(self.friendBtn)
        
        self.partyBtn = Button()
        self.partyBtn.Text = 'Party Friends'
        self.partyBtn.BackColor = Color.FromArgb(10,70,100)
        self.partyBtn.Location = Point(3, 133)
        self.partyBtn.Size = Size(98, 30)
        self.partyBtn.FlatStyle = FlatStyle.Flat
        self.partyBtn.FlatAppearance.BorderSize = 1 
        self.partyBtn.Click += self.btnPressedEvent
        otherPage.Controls.Add(self.partyBtn)
        
        ##### row 2
                
        self.itemBtn = Button()
        self.itemBtn.Text = 'Item Mover'
        self.itemBtn.BackColor = Color.FromArgb(10,70,100)
        self.itemBtn.Location = Point(105, 100)
        self.itemBtn.Size = Size(115, 30)
        self.itemBtn.FlatStyle = FlatStyle.Flat
        self.itemBtn.FlatAppearance.BorderSize = 1 
        self.itemBtn.Click += self.btnPressedEvent
        otherPage.Controls.Add(self.itemBtn)
        
        self.dunnoBtn = Button()
        self.dunnoBtn.Text = 'Dunno Yet'
        self.dunnoBtn.BackColor = Color.FromArgb(10,100,100)
        self.dunnoBtn.Location = Point(105, 133)
        self.dunnoBtn.Size = Size(115, 30)
        self.dunnoBtn.FlatStyle = FlatStyle.Flat
        self.dunnoBtn.FlatAppearance.BorderSize = 1 
        self.dunnoBtn.Click += self.btnPressedEvent
        otherPage.Controls.Add(self.dunnoBtn)
                
        self.repairAmt = TextBox()
        self.repairAmt.Text = '20'
        self.repairAmt.BackColor = Color.FromArgb(200,200,200)
        self.repairAmt.Location = Point(110, 170)
        self.repairAmt.Width = 20
        otherPage.Controls.Add(self.repairAmt)
        
        self.repairBtn = Button()
        self.repairBtn.Text = '     Repair Check'
        self.repairBtn.BackColor = Color.FromArgb(10,70,100)
        self.repairBtn.Location = Point(105, 165)
        self.repairBtn.Size = Size(115, 30)
        self.repairBtn.FlatStyle = FlatStyle.Flat
        self.repairBtn.FlatAppearance.BorderSize = 1 
        self.repairBtn.Click += self.btnPressedEvent
        otherPage.Controls.Add(self.repairBtn)
        otherPage.Controls.Add(self.box3)

        
        #####################  END OF TABS ######################################### 
         
        parent.Controls.Add(self.tabControl) 
        self.Shown += self.startManager
        
        
###################################################### END OF BOTTOM SPLIT FORM  ###################### 
              
###################################################### END OF  MAIN FORM   ######################










######################################  EVENT HANDLERS / THREAD MANAGEMENT ######################################

###########  BUTTON PRESSED EVENT ###########################################################
        
    def btnPressedEvent(self,sender,args):
                           
        ######################################## MASTER PRESS    ############## 
        
        if sender == self.stopMaster: 
         
            ############################# MASTER STOP PRESS   ############################# 
            
            if self.stopMaster.Text == 'Stop All':
                Misc.SetSharedValue('run',False)
                self.stopMaster.Text = 'Start All'
                self.stopMaster.BackColor = Color.FromArgb(120,10,10)
                
                self.stopAttack.Text = 'Attack Off'
                self.stopAttack.BackColor = Color.FromArgb(120,10,10)
                
                self.stopSpell.Text = 'Spells Off'
                self.stopSpell.BackColor = Color.FromArgb(120,10,10)
                
                self.stopSkill.Text = 'Skills Off'
                self.stopSkill.BackColor = Color.FromArgb(120,10,10)
                
                self.stopAction.Text = 'Actions Off'
                self.stopAction.BackColor = Color.FromArgb(120,10,10)
                
                self.stopOther.Text = 'Other Off'
                self.stopOther.BackColor = Color.FromArgb(120,10,10)
                
                self.hb.Value = 1
                self.eb.Value = 1
                self.fb.Value = 1
                self.box1.Text = 'No Friend(s)'
                self.box2.Text = 'No Target'
                
            ############################# MASTER START PRESSED   ##########################
            
            else:                                                 
                self.stopMaster.BackColor = Color.FromArgb(10,100,10)
                self.stopMaster.Text = 'Stop All'
                
                self.stopAttack.BackColor = Color.FromArgb(10,100,10)
                self.stopAttack.Text = 'Attack On'

                self.stopSpell.BackColor = Color.FromArgb(10,100,10)
                self.stopSpell.Text = 'Spells On'                 

                self.stopSkill.BackColor = Color.FromArgb(10,100,10)
                self.stopSkill.Text = 'Skills On'

                self.stopAction.BackColor = Color.FromArgb(10,100,10)
                self.stopAction.Text = 'Actions On'
                
                self.stopOther.BackColor = Color.FromArgb(10,100,10)
                self.stopOther.Text = 'Other On'
                
                if Misc.ReadSharedValue('run') == False:
                    Misc.SetSharedValue('run',True)
                    self.startManager(0,0)
                    
        ############################# INDIVIDUAL THREAD TOGGLE BUTTONS ################################              
                
        elif sender == self.stopAttack:
            self.tabControl.SelectedIndex = 0
            if self.stopAttack.Text == 'Attack On':                
                self.stopAttack.Text = 'Attack Off'
                self.stopAttack.BackColor = Color.FromArgb(120,10,10)
            else:
                self.stopAttack.BackColor = Color.FromArgb(10,100,10)
                self.stopAttack.Text = 'Attack On'
                self.stopMaster.BackColor = Color.FromArgb(10,100,10)
                self.stopMaster.Text = 'Stop All'
                if Misc.ReadSharedValue('run') == False:
                    Misc.SetSharedValue('run',True)
                    self.startManager(0,0)
        elif sender == self.stopSpell:
            self.tabControl.SelectedIndex = 1
            if self.stopSpell.Text == 'Spells On':                
                self.stopSpell.Text = 'Spells Off'
                self.stopSpell.BackColor = Color.FromArgb(120,10,10)
                
            else:
                self.stopSpell.BackColor = Color.FromArgb(10,100,10)
                self.stopSpell.Text = 'Spells On'        
                self.stopMaster.BackColor = Color.FromArgb(10,100,10)
                self.stopMaster.Text = 'Stop All'
                if Misc.ReadSharedValue('run') == False:
                    Misc.SetSharedValue('run',True)
                    self.startManager(0,0)
        elif sender == self.stopSkill:
            self.tabControl.SelectedIndex = 2
            if self.stopSkill.Text == 'Skills On':                
                self.stopSkill.Text = 'Skills Off'
                self.stopSkill.BackColor = Color.FromArgb(120,10,10)
            else:
                self.stopSkill.BackColor = Color.FromArgb(10,100,10)
                self.stopSkill.Text = 'Skills On'
                self.stopMaster.BackColor = Color.FromArgb(10,100,10)
                self.stopMaster.Text = 'Stop All'
                if Misc.ReadSharedValue('run') == False:
                    Misc.SetSharedValue('run',True)
                    self.startManager(0,0)
        elif sender == self.stopAction:
            self.tabControl.SelectedIndex = 3
            if self.stopAction.Text == 'Actions On':                
                self.stopAction.Text = 'Actions Off'
                self.stopAction.BackColor = Color.FromArgb(120,10,10)
            else:
                self.stopAction.BackColor = Color.FromArgb(10,100,10)
                self.stopAction.Text = 'Actions On'
                self.stopMaster.BackColor = Color.FromArgb(10,100,10)
                self.stopMaster.Text = 'Stop All'
                if Misc.ReadSharedValue('run') == False:
                    Misc.SetSharedValue('run',True)
                    self.startManager(0,0)
        elif sender == self.stopOther:
            self.tabControl.SelectedIndex = 4
            if self.stopOther.Text == 'Other On':                
                self.stopOther.Text = 'Other Off'
                self.stopOther.BackColor = Color.FromArgb(120,10,10)
            else:
                self.stopOther.BackColor = Color.FromArgb(10,100,10)
                self.stopOther.Text = 'Other On'
                self.stopMaster.BackColor = Color.FromArgb(10,100,10)
                self.stopMaster.Text = 'Stop All'
                if Misc.ReadSharedValue('run') == False:
                    Misc.SetSharedValue('run',True)
                    self.startManager(0,0)
                    
        ############################ OTHER BUTTONS #######################################################
        
        if sender == self.dunnoBtn:
            Misc.SendMessage('Dunno Yet')
        
        ############################# DRESS BUTTONS #################################################
        if sender == self.demonBtn:
            Dress.ChangeList('demon')
            Dress.DressFStart()
            Misc.SendMessage('Attempting to dress list "{}"'.format('demon'),79)
        if sender == self.undeadBtn:
            Dress.ChangeList('undead')
            Dress.DressFStart()
            Misc.SendMessage('Attempting to dress list "{}"'.format('undead'),79)
        if sender == self.reptileBtn:
            Dress.ChangeList('reptile')
            Dress.DressFStart()
            Misc.SendMessage('Attempting to dress list "{}"'.format('reptile'),79)
        if sender == self.repondBtn:
            Dress.ChangeList('repond')
            Dress.DressFStart()
            Misc.SendMessage('Attempting to dress list "{}"'.format('repond'),79)
        if sender == self.eleBtn:
            Dress.ChangeList('elemen')
            Dress.DressFStart()
            Misc.SendMessage('Attempting to dress list "{}"'.format('elemen'),79)
        if sender == self.arachBtn:
            Dress.ChangeList('arach')
            Dress.DressFStart()
            Misc.SendMessage('Attempting to dress list "{}"'.format('arach'),79)
        if sender == self.mainDressBtn:
            Dress.ChangeList('main')
            Dress.DressFStart()
            Misc.SendMessage('Attempting to dress list "{}"'.format('main'),79)
        if sender == self.luckBtn:
            Dress.ChangeList('luck')
            Dress.DressFStart()
            Misc.SendMessage('Attempting to dress list "{}"'.format('luck'),79)
        
        
        ########################### ADD FRIEND ###############################
        if sender == self.friendBtn:
            Misc.SendMessage('Target Your New Best Bud',78)
            friend = Mobiles.FindBySerial(Target.PromptTarget(' '))
            if friend:
                Friend.AddPlayer('friend',friend.Name,friend.Serial)
            else:
                Misc.SendMessage('Invalid Target',48)
        ################### run repair check ################
        
        if sender == self.repairBtn:
            Misc.SetSharedValue('dur',self.repairAmt.Text)
            Misc.SendMessage('Durability check set at {}'.format(self.repairAmt.Text),78)
            checker = DurabilityChecker()
            checker.Main()
            
        ####################### ITEM MOVER   ###################################    
        if sender == self.itemBtn:
            im = itemMover()
            im.Main()    
            
        ################### Skill Intructions #####################
            
        if sender == self.skillInstructions:
            newform = skillIntructionsForm(self.skillCombo.Text)
            Form.ShowDialog(newform)
            
            
        #################### Party all Friends ###############
        if sender ==  self.partyBtn:
            friendsList = Friend.GetList('friend')
            for f in friendsList:
                friend = Mobiles.FindBySerial(f)
                if friend:
                    Misc.WaitForContext(friend.Serial, 2000)
                    Misc.ContextReply(friend.Serial, 'Add Party Member')
        ####################  ADD CHASE ID##########################
        if sender == self.chaseBtn:
            Misc.SendMessage('Select Mobile Type To Add To Chase List',78)
            id = Mobiles.FindBySerial(Target.PromptTarget(' ')).Body
            if id:
                chaseIDs.append(id)
            
        #################### START path recorder form ############# 
        
        if sender == self.railRecBtn:   
            newform = railRecorderForm() 
            Form.ShowDialog(newform) 
        #############################  skill type combobox event ################   
        if sender == self.skillTypeCombo:
            skillCasting = ['Magery','Mysticism','Necromancy']
            skillCrafting = ['Tinker','Tailor']
            skillThievery = ['Hiding','Stealth']
            skillBard = ['Music','PeaceMaking']
            skillWilderness = ['Lore','Camping']
            if self.skillTypeCombo.Text == 'Casting':
                self.skillCombo.DataSource = skillCasting
            elif self.skillTypeCombo.Text == 'Crafting':
                self.skillCombo.DataSource = skillCrafting
            elif self.skillTypeCombo.Text == 'Thievery':
                self.skillCombo.DataSource = skillThievery
            elif self.skillTypeCombo.Text == 'Bard':
                self.skillCombo.DataSource = skillBard 
            elif self.skillTypeCombo.Text == 'Wilderness':
                self.skillCombo.DataSource = skillWilderness        
                
            
        
############################ END OF BUTTON PRESS EVENT ##############################################################

####################### CHECK BOX HANDLER ###########################

    def startManager(self,s,a):
        
        def threadManager():
            runningThreads = []
            
            ################################## ATTACK ##############################
           
            def attackThread():
                if self.rangeRad.Checked or self.meleeRad.Checked:
                    wep = None 
                    #Misc.SendMessage('attacking')
                    fil = Mobiles.Filter()
                    fil.Enabled = True
                    if self.rangeRad.Checked:
                        fil.RangeMax = 14
                    else:    
                        fil.RangeMax = 1
                    fil.Friend = False
                    fil.Notorieties = List[Byte](bytes([3,4,5,6]))
                    
                    enemies = Mobiles.ApplyFilter(fil)
                    Misc.Pause(50)
                    if len(enemies) > 0:
                        enemy = Mobiles.Select(enemies,'Nearest')
                        Mobiles.WaitForProps(enemy.Serial,1000)
                        oneMobSpec = 0
                        multMobSpec = 0
                        useMomentum = 0
                        smartWepFound = False
                        if self.momChk.Checked:
                            useMomentum = 1
                        if self.specChk.Checked:
                            if Player.GetItemOnLayer('RightHand'):
                                wep = Player.GetItemOnLayer('RightHand')
                            elif Player.GetItemOnLayer('LeftHand'):
                                wep = Player.GetItemOnLayer('LeftHand')
                                
                            if wep != None:
                                for s in smartWeps:
                                    if s[0] == wep.ItemID:
                                        oneMobSpec = s[1]
                                        multMobSpec = s[2]
                                        #Misc.SendMessage('Smart Weapon Found',80)
                                        smartWepFound = True
                                        break
                                if smartWepFound == False:                                    
                                    Misc.SendMessage("Add Current Wep To Smart Weps List",48)
                                    
                                if len(enemies) == 1:
                                    if oneMobSpec == 1:
                                        if not Player.HasSpecial:
                                            Player.WeaponPrimarySA()
                                    elif oneMobSpec == 2:
                                        if not Player.HasSpecial:
                                            Player.WeaponSecondarySA()                                
                                elif len(enemies) == 2:
                                    if useMomentum == 1:
                                       if not Player.SpellIsEnabled('Momentum Strike'):
                                            Spells.CastBushido('Momentum Strike')                               
                                    elif multMobSpec == 1:
                                        if not Player.HasSpecial:
                                            Player.WeaponPrimarySA()
                                    elif multMobSpec == 2:
                                        if not Player.HasSpecial:
                                            Player.WeaponSecondarySA() 
                                elif len(enemies) > 2:
                                    if multMobSpec == 0 and useMomentum == 1:
                                        if not Player.SpellIsEnabled('Momentum Strike'):
                                            Spells.CastBushido('Momentum Strike')                                 
                                    elif multMobSpec == 1:
                                        if not Player.HasSpecial:
                                            Player.WeaponPrimarySA()
                                    elif multMobSpec == 2:
                                        if not Player.HasSpecial:
                                            Player.WeaponSecondarySA()             
                            else:
                                Misc.SendMessage('Youre Disarmed!',48)
                        elif self.primChk.Checked:
                            if not Player.HasSpecial:
                                Player.WeaponPrimarySA()
                        elif self.secChk.Checked:    
                            if not Player.HasSpecial:
                                Player.WeaponSecondarySA()
                        
                        name = Mobiles.GetPropStringByIndex(enemy.Serial,0)
                        #Misc.SendMessage(name,67)
                        if not "Britannian" in name:
                            if not "energy vortex" in name:        
                                Player.Attack(enemy)
                    
                    
                runningThreads.remove('attack')    
             
            ######################   SPELLS #####################################
                   
            def spellsThread(): 
                if Player.Visible:
                    if self.invisChk.Checked:                    
                        Spells.CastMagery('Invisibility')
                        Target.WaitForTarget(3000)
                        Target.Self()
                    if self.eooChk.Checked:                    
                        if not Player.BuffsExist('Enemy Of One'):
                            Spells.CastChivalry('Enemy Of One')
                            Misc.Pause(500)

                    if self.masteryChk.Checked:      
                        if Timer.Check('mastery') == False:
                            if self.masteryCombo.Text == 'Onslaught':
                                Spells.CastMastery('Onslaught')
                                Timer.Create('mastery',10000)
                            elif self.masteryCombo.Text == 'Provo':
                                if Player.Mana > 40:
                                    if not Player.BuffsExist("Inspire"):
                                        Spells.CastMastery("Inspire")
                                        Misc.Pause(5000)
                                    elif not Player.BuffsExist("Invigorate"):
                                        Spells.CastMastery("Invigorate")
                                        Misc.Pause(5000)
                            elif self.masteryCombo.Text == 'Peace':
                                if Player.Mana > 40:
                                    if not Player.BuffsExist("Resilience"):
                                        Spells.CastMastery("Resilience")
                                        Misc.Pause(5000)
                                    elif not Player.BuffsExist("Perseverance"):
                                        Spells.CastMastery("Perseverance")
                                        Misc.Pause(5000)            
                                        
                                        
                            elif self.masteryCombo.Text == 'Body Guard':
                                Misc.SendMessage('body guard not implemented')
#                                if not self.bgMobile:
#                                    Misc.SendMessage("Target Who to Body Guard",78)
#                                    self.bgMobile = Target.PromptTarget("")
#                                    if not Player.BuffsExist('Bodyguard') and Player.Mana > 20:                                     
#                                        if Player.InRangeMobile(buddybg,5):
#                                            Spells.CastMastery('Bodyguard')
#                                            Target.WaitForTarget(2000)
#                                            Target.TargetExecute(buddybg)
                    if self.devChk.Checked:
                        if self.devTxt.Text.isdigit():
                            if ((Player.Stam +.01) / (Player.StamMax+.01)* 100) <= int(self.devTxt.Text):                               
                                Spells.CastChivalry('Divine Fury')
                                Misc.Pause(500)    
                    if self.caChk.Checked:
                        if not Player.BuffsExist('Counter Attack'):
                            Spells.CastBushido('Counter Attack')
                            Misc.Pause(500)
                    if self.cwChk.Checked:
                        if not Player.BuffsExist('Curse Weapon'):
                            Spells.CastNecro('Curse Weapon')
                            Misc.Pause(500)
                            
                    if self.vampChk.Checked:
                        if not Player.BuffsExist('Vampiric Embrace'):
                            Spells.CastNecro('Vampiric Embrace')
                            Misc.Pause(500)
                            
                    if self.mageXHealChk.Checked:
                        list = Friend.GetList('friend')    
                        ffil = Mobiles.Filter()
                        if list:
                            ffil.Serials = list
                        else:
                            ffil.Friend = True     
                        ffil.RangeMax = 12
                        friends = Mobiles.ApplyFilter(ffil)
                        weights = []
                        if len(friends) > 0:
                            for friend in friends: 
                                Mobiles.WaitForStats(friend, 100)            
                                weight = 1 - (friend.Hits / friend.HitsMax) + (0.3 if friend.Poisoned else 0)            
                                if weight < 0.1:
                                    continue                
                                weights.append({ "mobile": friend, "weight": weight })                 
                            if not weights:
                                pass
                            else:
                                weights.sort(key=lambda x: x["weight"], reverse=True)                         
                                tupple = weights[0]
                                mobile = tupple["mobile"]
                                if (mobile.Poisoned):
                                    Mobiles.Message(mobile, 50, 'Poisoned')                                        
                                    Spells.CastMagery('Cure')
                                    Target.WaitForTarget(4000)
                                    Target.TargetExecute(mobile)                                
                                    Misc.Pause(300)                                
                                if (mobile.Hits < mobile.HitsMax * 0.7):
                                    Mobiles.Message(mobile, 50, 'Need Heal')        
                                    Spells.CastMagery('Greater Heal')
                                    Target.WaitForTarget(4000)
                                    Target.TargetExecute(mobile)
                                    Misc.Pause(300)
  
                                    
                    ########### spells that need player hits        
                    if self.confidenceChk.Checked or self.evaChk.Checked or self.mageHealChk.Checked:
                        percentHits = (Player.Hits+.000001)/(Player.HitsMax+.000001) * 100
                        #Misc.SendMessage(percentHits)
                        if self.confidenceChk.Checked:
                            if self.confidenceTxt.Text.isdigit():
                                if percentHits < int(self.confidenceTxt.Text) and not Player.BuffsExist('Confidence'):
                                    Spells.CastBushido("Confidence")
                                    Misc.Pause (500)
                        if self.evaChk.Checked: 
                            if self.evaTxt.Text.isdigit():
                                if percentHits < int(self.evaTxt.Text) and not Player.BuffsExist('Evasion'):
                                    Spells.CastBushido("Evasion")
                                    Misc.Pause (500)
                        if self.mageHealChk.Checked:
                            if Player.Poisoned:
                                Spells.CastMagery('Cure')
                                Target.WaitForTarget(2500)
                                Target.Self()
                            if self.mageHealTxt.Text.isdigit():    
                                if percentHits < int(self.mageHealTxt.Text):
                                    Spells.CastMagery('Heal')
                                    Target.WaitForTarget(2500)
                                    Target.Self()
                                
                    # spells that need mobiles filter            
                    if self.witherChk.Checked or self.consChk.Checked or self.thunderChk.Checked or self.honorChk.Checked or self.allKillChk.Checked:                                                   
                        fil = Mobiles.Filter()
                        fil.Enabled = True                        
                        fil.RangeMax = 10              
                        fil.Friend = False
                        fil.Notorieties = List[Byte](bytes([3,4,5,6]))
                        enemies = Mobiles.ApplyFilter(fil)
                        if enemies:
                            if self.consChk.Checked:                    
                                if not Player.BuffsExist('Consecrate Weapon'):
                                    Spells.CastChivalry('Consecrate Weapon')
                                    Misc.Pause(500)                            
                            if self.witherChk.Checked:
                                for enemy in enemies:
                                    if Player.InRangeMobile(enemy,4):
                                        Spells.CastNecro('Wither')
                                        Misc.Pause(2000)
                                        break
                            if self.thunderChk.Checked:
                                for enemy in enemies:
                                    if Player.InRangeMobile(enemy,8):     #### check ranges
                                        Spells.CastSpellweaving('Thunderstorm')
                                        Misc.Pause(2000)
                                        break
                            if self.honorChk.Checked:
                                if not Player.BuffsExist('Honor'):
                                    for enemy in enemies:
                                        if Player.InRangeMobile(enemy,8):
                                            if not enemy.Serial in honorIgnore:
                                                Player.InvokeVirtue('Honor')
                                                Target.WaitForTarget(1000)
                                                Target.TargetExecute(enemy)
                                                honorIgnore.append(enemy.Serial)
                                                break
                                            
                            if self.allKillChk.Checked:
                                if self.allKillTxt.Text.isdigit():
                                    enemy = Mobiles.Select(enemies,'Nearest')
                                    if Timer.Check('allKill') == False:
                                        Player.ChatSay(87,'All Kill')
                                        Target.WaitForTarget(2000)
                                        Target.TargetExecute(enemy)
                                        Timer.Create('allKill',int(self.allKillTxt.Text) *1000)
                        
                        
                runningThreads.remove('spells')
                
            ##########################   SKILLS #####################################
                
            def skillsThread():
                goodenemies = []
                if Timer.Check("skill") == False and Player.Visible:
                    if self.hideChk.Checked:               
                        Player.UseSkill('Hiding')
                        Timer.Create("skill", 5500)
                
                    elif self.peaceChk.Checked:
                        if not Target.HasTarget():
                            Player.UseSkill('Peacemaking')
                            Target.WaitForTarget(2000)
                            Target.Self()
                            Timer.Create("skill", 11000)            
                    elif self.provoChk.Checked or self.discordChk.Checked:
                        fil = Mobiles.Filter()
                        
                        fil.RangeMax = 10
                        fil.Friend = False
                        fil.Notorieties = List[Byte](bytes([3,4,5,6]))
                        enemies = Mobiles.ApplyFilter(fil)                            
                        if enemies:
                            if self.provoChk.Checked and not Target.HasTarget():
                                if len(enemies) >= 2:
                                    for e in enemies:                                                                               
                                        if not "Britannian" in e.Name:
                                            if not "energy vortex" in e.Name:
                                                goodenemies.append(e)
                                    Misc.Pause(100)                                    
                                    if len(goodenemies) >= 2:        
                                        enemy = selectNearest(goodenemies)
                                        Mobiles.Message(enemy,78,"Provo 1")
                                        goodenemies.remove(enemy)
                                        secondEnemy = goodenemies[Random().Next(0,len(goodenemies)-1)] 
                                        Mobiles.Message(secondEnemy,78,"Provo 2")
                                        if not Target.HasTarget():
                                            Player.UseSkill('Provocation')
                                            Target.WaitForTarget(500)
                                            if Target.HasTarget():
                                                Target.TargetExecute(enemy)                        
                                                Target.WaitForTarget(500)
                                                Target.TargetExecute(secondEnemy) 
                                        if Journal.Search('fight.'):
                                            Journal.Clear()                                      
                                            Timer.Create("skill", 4000)
                                        else: 
                                            Timer.Create("skill", 2000)  # fail timer adjust    
                                            
                            elif self.discordChk.Checked:
                                if not Target.HasTarget():
                                    for enemy in enemies:
                                        if not "Britannian" in enemy.Name:
                                            if not "energy vortex" in enemy.Name:
                                                if not enemy.Serial in discordIgnore:
                                                    Mobiles.WaitForProps(enemy,100)
                                                    Player.UseSkill('Discordance')
                                                    Target.WaitForTarget(500)
                                                    Target.TargetExecute(enemy)
                                                    Misc.Pause(500)
                                                    if Journal.Search('jarring'):
                                                        Journal.Clear()
                                                        discordIgnore.append(enemy.Serial)
                                                        Timer.Create("skill", 7000)  # success timer adjust
                                                    else: 
                                                        Timer.Create("skill", 2000)  # fail timer adjust
                                                    break
                                
                    elif self.detectChk.Checked:
                        if not Target.HasTarget():
                            Player.UseSkill('Detect Hidden')
                            Target.WaitForTarget(1000)
                            Target.TargetExecuteRelative(Player.Serial,1)
                            Timer.Create("skill", 11000)            
                    elif self.skillChk.Checked:
                        skill = self.skillCombo.Text
                        stopAmt = float(self.skillStopTxt.Text)
                        amt = Player.GetSkillValue(skill)
                        if amt < stopAmt:
                            Misc.SendMessage('Training {} at {} stopping at {}'.format(skill,amt,stopAmt),92)
                            st = skillTrainer()
                            st.Main(skill)    
                runningThreads.remove('skills')

            ######################### ACTIONS  ###############################

            def actionsThread():##################change pause to timers??
                
                if self.tbChk.Checked:
                    if Player.BuffsExist("Paralyze")and Player.Hits > 20:
                        tbox = Items.FindByID(0x09a9,-1,Player.Backpack.Serial)
                        if tbox:
                            Items.UseItem(tbox)
                            Misc.Pause(1100)
                        else:
                            Misc.SendMessage('Trap Box Not Found',48)
 
                if self.apChk.Checked:
                    apple = Items.FindByID(0x2FD8,-1,Player.Backpack.Serial)
                    if Player.BuffsExist('Mortal Strike') or Player.BuffsExist('Curse') or Player.BuffsExist('Sleep')and Timer.Check("appletimer") == False:
                        if apple:
                            Items.UseItem(apple)
                            Timer.Create("appletimer", 30500)
                            Misc.Pause(1100)
                        else:
                            Misc.SendMessage('No Apples!!',48)            
                            
                if self.cChk.Checked:
                    curePot = Items.FindByID(0x0F07,-1,Player.Backpack.Serial)
                    if Player.Poisoned and Player.Visible:
                        if curePot:
                            Items.UseItem(curePot)
                            Misc.Pause(1100)
                        else:
                            Misc.SendMessage('No Cure Pots!!',48)
                
                if self.hChk.Checked:
                    if self.hTxt.Text.isdigit():
                        healHits = int(self.hTxt.Text)
                        healPot = Items.FindByID(0x0F0C,-1,Player.Backpack.Serial)       
                        if Player.Hits <= healHits and Player.Visible and not Player.Poisoned and not Player.BuffsExist('Mortal Strike') and Timer.Check("healpottimer") == False:
                            if healPot:
                                Items.UseItem(healPot)
                                Misc.Pause(1100)
                                Timer.Create("healpottimer", 2600)
                            else:
                                Misc.SendMessage('No Heal Pots!!',48)
                            
                if self.ojChk.Checked:
                    ojPetals = Items.FindByID(0x1021,0x002B,Player.Backpack.Serial)
                    if ojPetals:
                        if Player.Poisoned:
                            if not Player.BuffsExist("Orange Petals"):
                                Items.UseItem(ojPetals)
                                Misc.Pause(1100)
                    else:
                        Misc.SendMessage("No Orange Petals",48)
                        
                if self.roseChk.Checked:
                    rosePetals = Items.FindByID(0x1021,0x000E,Player.Backpack.Serial)
                    if rosePetals:
                        if not Player.BuffsExist("Rose Of Trinsic"):
                            Items.UseItem(rosePetals)
                            Misc.Pause(1100)
                    else:
                        Misc.SendMessage("No Rose Petals",48)
                
                if self.armChk.Checked:
                    if Player.GetItemOnLayer('RightHand'):
                        wep = Player.GetItemOnLayer('RightHand')
                        Misc.SetSharedValue('wep',wep.Serial)
                    elif Player.GetItemOnLayer('LeftHand'):
                        wep = Player.GetItemOnLayer('LeftHand')
                        Misc.SetSharedValue('wep',wep.Serial)                 
                    if not Player.GetItemOnLayer('RightHand') and not Player.GetItemOnLayer('LeftHand') and Misc.CheckSharedValue('wep'):
                        Misc.SendMessage('Trying to ReArm',48)
                        Player.EquipItem(Misc.ReadSharedValue('wep'))
                        Misc.Pause(1100)
                    elif not Misc.CheckSharedValue('wep'):
                        Misc.SendMessage("Equip A Wep to Rearm",48)
                    
                if self.activeChk.Checked:            
                    if Timer.Check("logintimer") == False:
                        Items.UseItem(Player.Backpack) 
                        Misc.Pause(1100)
                        Timer.Create("logintimer", 60000)
                        Misc.SendMessage('Staying Active',78)
                        
                runningThreads.remove('actions')
                
            ############################   OTHER    #################################
            def otherThread():
                
                
                def chase():                    
                    cfil = Mobiles.Filter()
                    cfil.Enabled = True
                    cfil.RangeMax = 14           
                    cfil.Notorieties = List[Byte](bytes([3,4,5,6]))
                    if self.delayTxt.Text.isdigit(): 
                        timer = int(self.delayTxt.Text)
                    else:
                        timer = 100
                    if self.chaseIdChk.Checked and len(chaseIDs) > 0:     
                        cfil.Bodies = List[int](chaseIDs)
                    mobs = Mobiles.ApplyFilter(cfil)
                    remove = []
                    for m in mobs:
                        
                        if m.Serial in ignoreMob:
                            remove.append(m)           
                    for r in remove:
                        mobs.Remove(r)
                    newmobs = mobs
                    #Misc.SendMessage(len(newmobs))
                    for m in newmobs:
                        if self.chaseChk.Checked == False or self.stopOther.Text == 'Other Off':
                            break
                        if not Player.InRangeMobile(m,1):    
                            go(m.Position.X,m.Position.Y)
                        if not Player.InRangeMobile(m,1):    
                            go(m.Position.X,m.Position.Y)
                        if not Player.InRangeMobile(m,1):
                            ignoreMob.append(m.Serial)
                            break
                        else:
                            while Mobiles.FindBySerial(m.Serial):
                                Misc.Pause(1000)
                                if self.chaseChk.Checked == False or self.stopOther.Text == 'Other Off':
                                    break
                                go(m.Position.X,m.Position.Y)
                                
                            Misc.Pause(timer)
                
                if self.railChk.Checked:                                            
                    for coords in readRail(self.railTxt.Text):
                        if self.railChk.Checked == False or self.stopOther.Text == 'Other Off':
                            break
                        go(coords[0],coords[1])
                        if self.chaseChk.Checked:
                           chase()
                elif self.chaseChk.Checked:           
                    chase()
                    

                runningThreads.remove('other')



            #####################  BARS THREAD #########################

            def barsThread():
                ###################### PLAYER HEALTH BAR ########################
                hit = 1
                hits = ((Player.Hits + .000001)/(Player.HitsMax +.0000001))* 100        
                hit = int(hits)
                if hit == 0:
                    hit = 1           
                self.hb.Value = hit 
                ################################## FRIEND HEALTH BAR ###################
                
                list = Friend.GetList('friend')
                if list:
                    ffil = Mobiles.Filter()
                    if list:
                        ffil.Serials = list
                    else:
                        ffil.Friend = True     
                    ffil.RangeMax = 12
                    friends = Mobiles.ApplyFilter(ffil)
                    if friends:
                        friend = Mobiles.Select(friends,'Nearest')
                        Mobiles.WaitForStats(friend,200)
                        friendhits = ((friend.Hits + .00001)/(friend.HitsMax+.00001))* 100        
                        friendhit = int(friendhits)
                        if friendhit == 0:
                            friendhit = 1           
                        self.fb.Value = friendhit
                        self.box1.Text = friend.Name
                    else:
                        self.fb.Value = 1
                        self.box1.Text = 'No Friend(s)'
                else:
                    Misc.SendMessage('Need Friends List Named friend',48)
                        
                ######################################  ENEMY HEALTH BAR ########################
                enemySer = None
                if Target.GetLast() != Player.Serial:            
                    if Mobiles.FindBySerial(Target.GetLast()):                    
                        enemySer = Target.GetLast()
                elif Mobiles.FindBySerial(Target.GetLastAttack()):             
                    enemySer = Target.GetLastAttack()    
                        
                else:
                    notoFil = Mobiles.Filter()
                    notoFil.RangeMax = 18
                    notoFil.Notorieties = List[Byte](bytes([3,4,5,6]))
                    enemylist = Mobiles.ApplyFilter(notoFil)
                    if len(enemylist) > 0:
                        enemy = Mobiles.Select(enemylist,'Nearest')
                        enemySer = enemy.Serial
                    else:
                        enemySer = None
                if enemySer:
                    enemy = Mobiles.FindBySerial(enemySer)
                    if Mobiles.FindBySerial(enemySer):
                        Mobiles.WaitForStats(enemy,200)
                        mobhits = ((enemy.Hits + .00001)/(enemy.HitsMax+.00001))* 100        
                        mobhit = int(mobhits)
                        if mobhit == 0:
                            mobhit = 1           
                        self.eb.Value = mobhit
                        self.box2.Text = enemy.Name    
                else:
                    self.eb.Value = 1
                    self.box2.Text = 'No Target' 
                
                runningThreads.remove('bars')

    
            ################################# THREAD STARTER  ###################
               
            while Misc.ReadSharedValue('run')== True:
                if Player.IsGhost:
                    Misc.Pause(2000)
                    
                elif self.stopMaster.Text == 'Stop All':
                    if not 'bars' in runningThreads:
                       runningThreads.append('bars')
                       Thread(ThreadStart(barsThread)).Start()                                         
                    if self.stopAttack.Text == 'Attack On':
                        if not 'attack' in runningThreads:
                            runningThreads.append('attack')
                            Thread(ThreadStart(attackThread)).Start()
                    if self.stopSpell.Text == 'Spells On':
                        if not 'spells' in runningThreads:
                            runningThreads.append('spells')
                            Thread(ThreadStart(spellsThread)).Start()
                    if self.stopSkill.Text == 'Skills On':
                        if not 'skills' in runningThreads:
                            runningThreads.append('skills')
                            Thread(ThreadStart(skillsThread)).Start()
                    if self.stopAction.Text == 'Actions On':
                        if not 'actions' in runningThreads:
                            runningThreads.append('actions')
                            Thread(ThreadStart(actionsThread)).Start()
                    if self.stopOther.Text == 'Other On':
                        if not 'other' in runningThreads:
                            runningThreads.append('other')
                            Thread(ThreadStart(otherThread)).Start()
                                                        
                Misc.Pause(1000)
                #Misc.SendMessage('MAIN THREAD RUNNING',48)
        Thread(ThreadStart(threadManager)).Start() 
            
############################################# END OF MAIN FORM   ######################################################




################################### SKILL INSTRUCTIONS FORM ######################################
string = ''

mageryInst = " 1)A suit with Lower Reagent Cost 100%, 2) Full Spellbook,3)   Over 30.0 Magery."
mystInst = " 1) A suit with Lower Reagent Cost 100%,  2) Full Mysticism Spellbook,3) Over 30.0 Mysticism."   
necroInst = " 1) A suit with Lower Reagent Cost 100%, 2) Full Necromancy Spellbook 3) A weapon Equipped(If under 20 Necro)"
campingInst = "U wanna train Camping, get a job hippy "
class skillIntructionsForm(Form):    
    
    def __init__(self,string):
        if string == 'Magery':
            instr = mageryInst
        elif string == 'Mysticism':
            instr = mystInst
        elif string == 'Necromancy':
            instr = necroInst
        elif string == 'Camping':
            instr = campingInst
        else:
            instr = "No Instructions provided or Skill Not Implemented Yet"
        
        self.Text = "Skill Instructions"
        self.Width = 200
        self.Height =200
        self.TopMost = True                
        self.BackColor = Color.FromArgb(25,25,25)
        self.ForeColor = Color.FromArgb(231,231,231)
        self.FormBorderStyle = FormBorderStyle.Fixed3D
        self.CenterToScreen()

        
        self.text = Label()
        self.text.Width = 160
        self.text.Height = 200
        self.text.Text = instr
        self.text.Location = Point(10, 40)
        self.text.ForeColor = Color.FromArgb(231,231,231)
        self.Controls.Add(self.text)
        

            
###################################### RAIL RECORDER FORM ############################################## 
coordsList = []
class railRecorderForm(Form):    
    
    def __init__(self):
        self.Text = "Fast Rails"
        self.Width = 250
        self.Height = 225
        self.TopMost = True                
        self.BackColor = Color.FromArgb(25,25,25)
        self.ForeColor = Color.FromArgb(231,231,231)
        #        self.FormBorderStyle = FormBorderStyle.Fixed3D
        self.CenterToScreen()
       
        self.button = Button()
        self.button.Text = 'Add Coord'
        self.button.Width = 100
        self.button.Height = 40
        self.button.Location = Point(10, 10)
        self.button.Click += self.add
        
        self.button1 = Button()
        self.button1.Text = 'Del last Coord'
        self.button1.Width = 100
        self.button1.Height = 40
        self.button1.Location = Point(125, 10)
        self.button1.Click += self.delLast

        self.button2 = Button()
        self.button2.Text = 'Clear All'
        self.button2.Width = 100
        self.button2.Height = 40
        self.button2.Location = Point(125, 50)
        self.button2.Click += self.clear
        
        self.button3 = Button()
        self.button3.Text = 'Test Rail'
        self.button3.Width = 100
        self.button3.Height = 40
        self.button3.Location = Point(10, 50)
        self.button3.Click += self.test
        
        self.button4 = Button()
        self.button4.Text = 'INFO'
        self.button4.Width = 100
        self.button4.Height = 40
        self.button4.Location = Point(10, 90)
        self.button4.Click += self.info
        
        self.button5 = Button()
        self.button5.Text = 'SAVE'
        self.button5.Width = 75
        self.button5.Height = 30
        self.button5.Location = Point(135, 135)
        self.button5.BackColor = Color.FromArgb(10,150,10)
        self.button5.Click += self.makefile
        
        self.textbox = TextBox()
        if Misc.ReadSharedValue("railname"):
            self.textbox.Text = Misc.ReadSharedValue("railname")
        else:
            self.textbox.Text = "Rail_Name"
        self.textbox.Location = Point(10, 140)
        self.textbox.BackColor = Color.FromArgb(10,10,10)
        self.textbox.ForeColor = Color.FromArgb(225,225,225) 
        self.textbox.Width = 115

        
        self.Controls.Add(self.button)
        self.Controls.Add(self.button1)
        self.Controls.Add(self.button2)
        self.Controls.Add(self.button3)
        self.Controls.Add(self.button4)
        self.Controls.Add(self.button5)
        self.Controls.Add(self.textbox)
        
    def add(self, sender, event):
        coordsList.append([(Player.Position.X),(Player.Position.Y)])
        
        Misc.SendMessage('{} Total Coords'.format(len(coordsList)))
        
           
    def test(self, sender, event):
        if len(coordsList) > 0:
            for l in coordsList:
                go(l[0],l[1])
        else:
            Misc.SendMessage('You didnt set any Coords!',33)
            
    def delLast(self, sender, event):
        if len(coordsList) > 0:
            del coordsList[-1]
            Misc.SendMessage('{} Total Coords'.format(len(coordsList)))
        else:
            Misc.SendMessage('The Coord list is Empty!',33)
            
    def clear(self, sender, event):
        coordsList.Clear()
        Misc.SendMessage('Coord list Cleared',180)
        
    def info(self, sender, event):
        if len(list) > 0:
            Misc.SendMessage('{} Total Coords'.format(len(coordsList)),75)
            Misc.SendMessage('Last Coords were {}'.format(coordsList[-1]),180)
            Misc.SendMessage('Current Coords are {}'.format(str(Player.Position.X)) + ',' + (str(Player.Position.Y)),285)
        else:
            Misc.SendMessage('You didnt set any Coords!',33)
            Misc.SendMessage('Current Coords are {}'.format(str(Player.Position.X)) + ',' + (str(Player.Position.Y)),285)
            
    def makefile(self, sender, event):
        rail_file = "/".join([scriptfolder, 'Scalpel', '{}.txt'.format(self.textbox.Text)])
        if access(rail_file):
            Misc.SendMessage('Saved {}.txt in Scalpel Folder'.format(self.textbox.Text),30)
            
        file = open(rail_file, 'w+')
        file.write(str(coordsList))
        file.close()
#######################################################################################################


################################## END OF FORMS #####################################

#######################################  ITEM MOVER ####################################
class itemMover(object):
    def Main(self):            
        x = 45
        y = 65        
        item = Items.FindBySerial(Target.PromptTarget('Choose type'))
        container = Items.FindBySerial(item.Container)
        dest = Target.PromptTarget('Choose Destination') 
        for items in container.Contains:
            if items.ItemID == item.ItemID:
                Items.Move(items,dest,0,x,y)
                x +=3
                if x > 140:
                    x = 45
                    y += 20
                Misc.Pause(1100)


                              
################################# REPAIR  ########################################

class DurabilityChecker(object): 

    def hasDurability(self, item):
        Items.WaitForProps(item, 1000)        
        for prop in Items.GetPropStringList(item):
            if prop.find("durability") >= 0:
                return True                
        return False

    def getDurability(self, item):
        Items.WaitForProps(item, 1000)
        return Items.GetPropValue(item, "durability")
        
    def repairshit(self,item,bench):#iterates thru types of repair deeds to try to repair from bench                                  
        Items.UseItem(bench)            
        Gumps.WaitForGump(9237, 10000)
        Gumps.SendAction(9237, 2002)
        Target.WaitForTarget(10000, False)
        Misc.Pause(1000)
        Target.TargetExecute(item)
        Gumps.WaitForGump(9237, 10000)
        Gumps.SendAction(9237, 2001)
        Target.WaitForTarget(10000, False)  # maybe something missing like stone i dunno
        Target.TargetExecute(item)          # multiple type attempts is way less code than deducing repair type for item, not worth it, fast
        Gumps.WaitForGump(9237, 10000)
        Gumps.SendAction(9237, 2003)
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(item)
        Gumps.WaitForGump(9237, 10000)
        Gumps.SendAction(9237, 2006)
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(item)
        Misc.Pause(2000) 
            
    def Main(self):        
        Misc.Pause(1000)                
        for layer in layers:
            item = Player.GetItemOnLayer(layer)            
            if not item:
                continue                
            if not self.hasDurability(item):
                continue                
            durability = self.getDurability(item)    
            minDurability = int(Misc.ReadSharedValue('dur'))    
            if durability < minDurability:
                Misc.SendMessage("{} Needs Repair".format(layer), 38)
                if Gumps.CurrentGump() == 9237:
                    self.repairshit(item.Serial,bench)
                else:
                    Misc.Pause(1000)
                    benches = Items.ApplyFilter(BFilter)
                    if len(benches) > 0:
                        bench = Items.Select(benches,'Nearest')
                        if bench:
                            Misc.SendMessage('Bench Found',80)
                            self.repairshit(item.Serial,bench)
                    else:
                        Misc.SendMessage('No Bench Found',33)
                
        Misc.SendMessage('Check Complete',87)
        Gumps.CloseGump(9237)
        
#############################  END OF REPAIR CLASS  ####################################################################        


####################################### ALL SKILL TRAINERS HERE ######################################        
class skillTrainer(): 
 #############################MAGE ##########################   
    def trainMagery(self):
        Magery = Player.GetSkillValue('Magery')
        if Magery < 20:
            Spells.CastMagery('Harm')
            Target.WaitForTarget(4000,False)
            Target.TargetExecute(Items.FindByID(0x0EFA,-1,-1))
            Misc.Pause(2000)
            
        elif Magery < 43 and Player.Mana > 20:
            Spells.CastMagery('Fireball')
            Target.WaitForTarget(4000,False)
            Target.TargetExecute(Items.FindByID(0x0EFA,-1,-1))
            Misc.Pause(2000)
            
        elif Magery >= 43 and Magery < 55 and Player.Mana > 11:
            Spells.CastMagery('Lightning')
            Target.WaitForTarget(4000,False)
            Target.TargetExecute(Items.FindByID(0x0EFA,-1,-1))
            Misc.Pause(2000)   
       
        elif Magery >= 55 and Magery < 68  and Player.Mana > 40:                       
            Spells.CastMagery('Paralyze')
            Target.WaitForTarget(4000,False)
            Target.TargetExecute(Items.FindByID(0x0EFA,-1,-1))
            Misc.Pause(3000)  
           
        elif Magery >= 68 and Magery < 82  and Player.Mana > 40:
            Spells.CastMagery('Energy Bolt')
            Target.WaitForTarget(4000,False)
            Target.TargetExecute(Items.FindByID(0x0EFA,-1,-1))
            Misc.Pause(3000)

        elif Magery >= 82 and Magery < 93  and Player.Mana > 40:
            Spells.CastMagery('Flamestrike')
            Target.WaitForTarget(4000,False)
            Target.TargetExecute(Items.FindByID(0x0EFA,-1,-1))
            Misc.Pause(3000) 

        elif Magery >= 93 and Player.Mana > 60:
            Spells.CastMagery('Earthquake')
            Misc.Pause(8000)
            
            
#############################MYST #######################################            
    def trainMyst(self):
        Mysticism = Player.GetSkillValue('Mysticism')
        if Mysticism < 63 and Player.Mana > 20:
            Spells.CastMysticism('Stone Form')
            Misc.Pause(4500)
            
        elif Mysticism >= 63 and Mysticism < 80 and Player.Mana > 30:
            Spells.CastMysticism('Cleansing Winds')
            Target.WaitForTarget(4000,False)
            Target.Self()
            Misc.Pause(2000)   
       
        elif Mysticism >= 80 and Mysticism < 95  and Player.Mana > 40:
            Spells.CastMysticism('Hail Storm')
            Target.WaitForTarget(4000,False)
            Target.Self()
            Misc.Pause(3000)  

        elif Mysticism >= 95 and Mysticism != Player.GetSkillCap('Mysticism') and Player.Mana > 60:
            Spells.CastMysticism('Nether Cyclone')
            Target.WaitForTarget(4000,False)
            Target.Self()
            Misc.Pause(3000)                 
################################# NECRO ########################################
    def trainNecro(self):
        Necro = Player.GetSkillValue('Necromancy')
        if Necro < 35 and Player.Mana > 7:
            Spells.CastNecro('Curse Weapon')
            Misc.Pause(2000)
            
        elif Necro >= 35 and Necro < 50 and Player.Mana > 5:
            Spells.CastNecro('Pain Spike')
            Target.WaitForTarget(4000,False)
            Target.Self()
            Misc.Pause(2000)   
       
        elif Necro >= 50 and Necro < 65  and Player.Mana > 11:
            Spells.CastNecro('Horrific Beast')
            Misc.Pause(3500)  
           
        elif Necro >= 65 and Necro < 85  and Player.Mana > 23:
            if Player.BuffsExist('Horrific Beast'):      
                Misc.Pause (400)
                Spells.CastChivalry("Horrific Beast")
                Misc.Pause(3500)
            else:    
                Spells.CastNecro('Wither')
                Misc.Pause(4000)

        elif Necro >= 85 and Necro < 100  and Player.Mana > 23:
            Spells.CastNecro('Lich Form')
            Misc.Pause(4000) 

        elif Necro >= 100 and Player.Mana > 23:
            Spells.CastNecro('Vampiric Embrace')
            Misc.Pause(8000)
            
    def trainTracking(self):
        Player.UseSkill('Tracking')
        Gumps.WaitForGump(12350000, 100)
        Gumps.SendAction(12350000, 0)                
    
    def Main(self,skill):
        Misc.SendMessage(skill)
        if skill == 'Magery':
            self.trainMagery()
        if skill == 'Mysticism':
            self.trainMyst()
        if skill == 'Necromancy':
            self.trainNecro()
                 
    def trainHiding(self):
        Player.UseSkill('Hiding')
                    
#####################   RUN APP   ################################################################################      
Application.EnableVisualStyles()
Application.Run(assistant()) 