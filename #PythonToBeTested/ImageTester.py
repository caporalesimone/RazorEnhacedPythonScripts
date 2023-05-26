playerLayersList = [
                        "RightHand", "LeftHand", "Shoes", "Pants", "Shirt", 
                        "Head", "Gloves", "Ring", "Neck", "Waist", 
                        "InnerTorso", "Bracelet", "MiddleTorso", "Earrings", "Arms", 
                        "Cloak", "OuterTorso", "OuterLegs", "InnerLegs", "Talisman",
                        "Hair"
                    ]

#===================================================================================
import System, math, time, datetime
import Misc, Player, Statics, Mobiles

import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
 
from System import *
from System.Windows.Forms import *
from System.Drawing import *
from System.Drawing.Imaging import *
from System.Drawing.Drawing2D import *

#===================================================================================
logTime = 0    
def Log(string):
    global logTime 
    if currentTime - logTime < 250:
        delay = 250 - (currentTime - logTime)
        Misc.SendMessage(">{}".format(string), 40)
        Misc.Pause(delay)
    else:
        logTime = currentTime
        Misc.SendMessage(">{}".format(string), 201)
 
#===================================================================================
currentTime = 0
def SetUnixTime():
    global currentTime
    currentTime = int(time.time()* 1000)

#===================================================================================
class ItemData():
    def __init__(self, updateTick, Serial, item, button):
        self.updateTick = updateTick    # byValue
        self.Serial     = Serial        # byValue
        self.item       = item          # byReference
        self.button     = button        # byReference
    
#===================================================================================
class RunForm(Form):

    def __init__(self):
        Form.__init__(self)
        
        self.Text = "Visualizer"
        self.HelpButton = False
        self.MinimizeBox = True 
        self.MaximizeBox = False
        self.Width = 750
        self.Height = 750
        self.BackColor = Color.Black
        self.FormBorderStyle = FormBorderStyle.Sizable
        self.StartPosition = FormStartPosition.CenterScreen
        self.Opacity = 100
        self.SetStyle(ControlStyles.DoubleBuffer, True)
        self.FormClosed += FormClosedEventHandler(self.OnFormClosed)
        self.Resize += EventHandler(self.OnResizeForm)
        self.TopMost = True
        self.Show()
        self.Visible = True

        self.brushBlack  = SolidBrush(Color.Black)
        self.brushGreen  = SolidBrush(Color.Green)
        self.brushRed    = SolidBrush(Color.Red)
        self.brushYellow = SolidBrush(Color.Yellow)
        self.brushWhite  = SolidBrush(Color.White)
        
        self.Main()
        
    def OnFormClosed(self, e):
        self.Dispose()
        self.isFormRunning = False

    def OnResizeForm(self, e, ee):
        try:
            startingPointX = 500
            if self.ClientRectangle.Width-500 > 500:
                startingPointX = self.ClientRectangle.Width-500               
            
            # self.multiLinedTextbox.Location          = Point(startingPointX, 50)
            # self.multiLinedTextbox.Width             = 500
            # self.multiLinedTextbox.Height            = self.ClientRectangle.Height
            
            self.hasDatasetChanged = True
        except:
            Log("Exception: OnResizeForm()")
            Misc.Pause(1000)
        
    def OnMouseHoverButtonEnter(self, event, eventArgs):
        # self.multiLinedTextbox.Clear()
        
        bitmap = event.Tag.bitmap
        item = event.Tag.item
        
        # self.multiLinedTextbox.Text += "Name            : "+str(item.Name) +"\r\n"
        # self.multiLinedTextbox.Text += "Amount          : "+str(item.Amount) +"\r\n"
        # if item.OnGround == True:
            # self.multiLinedTextbox.Text += "Distance        : "+str(item.DistanceTo(self.mobilePlayer)) +"\r\n"
        
        # self.multiLinedTextbox.Text += "\r\n"
        
        # string = str(hex(item.Serial)).upper()
        # string = string[:0] + string[2:]
        # string = "0x"+string
        # self.multiLinedTextbox.Text += "ItemID          : "+ string +"\r\n"
        # string = str(hex(item.ItemID)).upper()
        # string = string[:0] + string[2:]
        # string = "0x"+string
        # self.multiLinedTextbox.Text += "SerialID        : "+ string +"\r\n"
        # self.multiLinedTextbox.Text += "Hue             : "+str(item.Hue) +"\r\n"
        # self.multiLinedTextbox.Text += "Position        : "+str(item.Position.X)+", "+str(item.Position.Y)+", "+str(item.Position.Z) +"\r\n"
        # string = str(hex(item.Container)).upper()
        # string = string[:0] + string[2:]
        # string = "0x"+string
        # self.multiLinedTextbox.Text += "Container       : "+ string +"\r\n"
        # string = str(hex(item.RootContainer)).upper()
        # string = string[:0] + string[2:]
        # string = "0x"+string
        # self.multiLinedTextbox.Text += "RootContainer   : "+ string +"\r\n"

        # for property in item.Properties:
            # self.multiLinedTextbox.Text += "Property        : "+ str(property) +"\r\n"
        
       
        
    def OnMouseHoverButtonLeave(self, event, eventArgs):
        self.multiLinedTextbox.Clear()
    
    def CreateMultiLinedTextBox(self,):
        t                   = TextBox()
        
        startingPointX = 500
        if self.ClientRectangle.Width-500 > 500:
            startingPointX = self.ClientRectangle.Width-500   
        
        t.Location          = Point(startingPointX, 50)
        t.Width             = 500
        t.Height            = self.ClientRectangle.Height
        t.Multiline         = True
        t.ForeColor         = Color.White
        t.BackColor         = Color.Black
        t.Font              = Font("Consolas", 12)
        self.Controls.Add(t)
        self.multiLinedTextbox = t
        
    def CreateImageButton(self, item):
        try:
            positionX = 0
            positionZ = 0
            
            b = Button()
            
            b.Width                     = 50
            b.Height                    = 50
            b.ForeColor                 = Color.White
            b.BackColor                 = Color.Gray
            b.Location                  = Point(positionX, positionZ)
            b.TabStop                   = False
            b.FlatStyle                 = FlatStyle.Flat
            b.FlatAppearance.BorderSize = 0            
            b.ImageAlign                = ContentAlignment.MiddleCenter
            b.BackgroundImageLayout     = ImageLayout.Zoom
            b.BackgroundImage           = item.Image
            #b.MouseDown?                 += MouseEventHandler(self.OnMouseClickEvent)
            #b.MouseHover                += EventHandler(self.OnMouseHoverButtonEnter)
            #b.MouseLeave                += EventHandler(self.OnMouseHoverButtonLeave)
            b.Tag                       = ItemData(0, item.Serial, item, None)
            
            self.Controls.Add(b)

            return b
            
        except:
            Log("Exception: CreateImageButton()")
            
    def OnMouseClickEvent(self, event, mouseEventArgs):
        item   = event.Tag.item
        bitmap = event.Tag.bitmap
        
        if mouseEventArgs.Button == MouseButtons.Left:
            
            # Drop item from backpack onto the ground
            if item.RootContainer == Player.Serial and item.Container == Player.Backpack.Serial:
                Items.DropItemGroundSelf(item, 0)
                
            # Pickup item from ground and place it into the players backpack
            elif item.OnGround == True:
                Items.Move(item.Serial, Player.Backpack.Serial, 0)
                
    def Main(self):

        self.mobilePlayer   = Mobiles.FindBySerial(Player.Serial)
        
        self.graphicsLayer = self.CreateGraphics()
        
        self.itemDataObjectList = []
        self.itemDataObjectIndexList = []
        
        self.updateTick     = 0
        self.elapsedTime    = 0
        self.elapsedCounter = 0
        self.isFormRunning  = True
        while self.isFormRunning == True:

            SetUnixTime()
            
            #self.elapsedCounter += 1
            #if currentTime >= self.elapsedTime:
                #self.elapsedTime = currentTime + 1000
                #Log(str(self.elapsedCounter))    
                #TextRenderer.DrawText(self.graphicsLayer, str(self.elapsedCounter), self.Font, Point(0, 0), Color.White, Color.Black, TextFormatFlags.Default)            
                #self.elapsedCounter = 0
            
            itemList = []
            mobileList = []
            
            hasException = False
            try:
                filter = Items.Filter()
                filter.Enabled = False
                itemList = Items.ApplyFilter(filter)
                
                if itemList == None:
                    hasException = True
            except:
                Log("Exception: Main.Items.ApplyFilter()")
                hasException = True

            try:
                filter = Mobiles.Filter()
                filter.Enabled = False
                mobileList = Mobiles.ApplyFilter(filter)
                
                if mobileList == None:
                    hasException = True
            except:
                Log("Exception: Main.Mobiles.ApplyFilter()")
                hasException = True

            if hasException == True:
                Application.DoEvents()
                continue

            self.updateTick += 1
            if self.updateTick > 99999999:
                self.updateTick = 0
                for i in range(len(self.itemDataObjectList) - 1, -1, -1):
                    self.Controls.Remove(self.itemDataObjectList[i].button)
                    del self.itemDataObjectList[i]                

            updateFormButtons = False
            for item in itemList:
                # Filter
                if item.Movable == False:
                    continue
                        
                if item.IsContainer == True:
                    continue
                
                if item.RootContainer > 0 and item.Container > 0:
                    if item.RootContainer == item.Container:
                        continue

                itemDataObjectFound = False
                for itemDataObject in self.itemDataObjectList:

                    # Filter
                    if itemDataObject.Serial == item.Serial:
                        itemDataObjectFound = True
                        itemDataObject.updateTick = self.updateTick
                        break

                        
                if itemDataObjectFound == False:
                    updateFormButtons = True
                    newItemDataObject = ItemData(self.updateTick
                                                , item.Serial
                                                , item
                                                , self.CreateImageButton(item))
                    self.itemDataObjectList.append(newItemDataObject)
            
            for i in range(len(self.itemDataObjectList) - 1, -1, -1):
                if self.itemDataObjectList[i].updateTick < self.updateTick:
                    updateFormButtons = True
                    self.Controls.Remove(self.itemDataObjectList[i].button)
                    del self.itemDataObjectList[i]
            
            # Create Index List
            index = 0
            self.itemDataObjectIndexList = []
            for itemDataObject in self.itemDataObjectList:
                if itemDataObject.updateTick >= self.updateTick:
                    self.itemDataObjectIndexList.append(index)
                index += 1
                
            linePosX = 0
            linePosZ = 0
            for indexResult in range(len(self.itemDataObjectIndexList) - 1, -1, -1):

                listIndex = self.itemDataObjectIndexList[indexResult]
                itemDataObject = self.itemDataObjectList[listIndex]

                if linePosX > self.Width - 50:
                    linePosX = 0
                    linePosZ += 51
                
                
                #  Set Button Position
                itemDataObject.button.Location = Point(linePosX, linePosZ)
                linePosX += 51
                
                del self.itemDataObjectIndexList[indexResult]                    
                    
                    
            Application.DoEvents()
            continue
            
                    
            if updateFormButtons == False:
                Application.DoEvents()
                continue
  
            
            # Create Index List
            index = 0
            self.itemDataObjectIndexList = []
            for itemDataObject in self.itemDataObjectList:
                if itemDataObject.updateTick >= self.updateTick:
                    self.itemDataObjectIndexList.append(index)
                index += 1

            linePosX = 0
            linePosZ = 0

            Log("len_1: "+str(len(self.itemDataObjectIndexList)))
            # Items in PC Backpack   
            linePosX = 0
            linePosZ += 51
            for indexResult in range(len(self.itemDataObjectIndexList) - 1, -1, -1):
                listIndex = self.itemDataObjectIndexList[indexResult]
                itemDataObject = self.itemDataObjectList[listIndex]
                
                # Filter
                ignoreItemDataObject = True
                if itemDataObject.item.Container == Player.Backpack.Serial:
                    ignoreItemDataObject = False
                
                if ignoreItemDataObject == True:
                    continue                    

                #  Set Button Position
                linePosX += 51
                itemDataObject.button.Location = Point(linePosX, linePosZ)
                
                del self.itemDataObjectIndexList[indexResult]
        
            #Log("len_2: "+str(len(self.itemDataObjectIndexList)))
            # Items on floor
            linePosX = 0
            linePosZ += 71
            for indexResult in range(len(self.itemDataObjectIndexList) - 1, -1, -1):

                listIndex = self.itemDataObjectIndexList[indexResult]
                itemDataObject = self.itemDataObjectList[listIndex]
                
                # Filter
                ignoreItemDataObject = True
                if itemDataObject.item.Visible == True and \
                    ( itemDataObject.item.RootContainer == None and \
                        itemDataObject.item.Container == None): 
                    ignoreItemDataObject = False
                
                if ignoreItemDataObject == True:
                    continue
                    
                #  Set Button Position
                itemDataObject.button.Location = Point(linePosX, linePosZ)
                linePosX += 51
                
                del self.itemDataObjectIndexList[indexResult]

            # Items on NPC
            linePosX = 0
            linePosZ += 71
            for indexResult in range(len(self.itemDataObjectIndexList) - 1, -1, -1):

                listIndex = self.itemDataObjectIndexList[indexResult]
                itemDataObject = self.itemDataObjectList[listIndex]
                
                for mobile in mobileList:
                    # Filter
                    ignoreItemDataObject = True
                    if itemDataObject.item.OnGround == False and \
                        itemDataObject.item.Visible == True and \
                        mobile.Serial == itemDataObject.item.Container:
                        ignoreItemDataObject = False
                        break
                
                if ignoreItemDataObject == True:
                    continue
                    
                #  Set Button Position
                itemDataObject.button.Location = Point(linePosX, linePosZ)
                linePosX += 51
                
                del self.itemDataObjectIndexList[indexResult]
                
            #Log("len_3: "+str(len(self.itemDataObjectIndexList)))

            
                
          
            
            # self.graphicsLayer.FillRectangle(self.brushBlack, 0, 0, self.ClientRectangle.Width + 50, self.ClientRectangle.Height + 50)
            # self.graphicsLayer.DrawLine(Pen(Color.White), 0, 51, self.ClientRectangle.Width + 50, 51)
            # TextRenderer.DrawText(self.graphicsLayer, str(mobile.Name), self.Font, Point(0, headerLineY-15), Color.White, Color.Black, TextFormatFlags.Default)

        
f = RunForm()