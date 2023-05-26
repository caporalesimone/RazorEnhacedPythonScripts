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
def Log(string):
    Misc.SendMessage(">{}".format(string), 201)
 
#===================================================================================
currentTime = 0
def SetUnixTime():
    global currentTime
    currentTime = int(time.time()* 1000)

#===================================================================================
class ItemButtonDataContainer():
    def __init__(self, updateTick, Serial, Container, item, button):
        self.updateTick     = updateTick    # byValue
        self.Serial         = Serial        # byValue
        self.Container      = Container     # byValue
        self.item           = item          # byReference
        self.button         = button        # byReference

#===================================================================================
def enum(**enums):
    return type('Enum', (), enums)
    
#===================================================================================
class RunForm(Form):

    def __init__(self):
        Form.__init__(self)
        self.Text               = "Advanced Backpack - " + str(Player.Name)
        self.HelpButton         = False
        self.MinimizeBox        = True 
        self.MaximizeBox        = False
        self.Width              = 750
        self.Height             = 750
        self.BackColor          = Color.Black
        self.FormBorderStyle    = FormBorderStyle.Sizable
        self.StartPosition      = FormStartPosition.CenterScreen
        self.Opacity            = 100
        #self.FormClosed         += FormClosedEventHandler(self._OnFormClosed)
        #self.Resize             += EventHandler(self._OnResizeForm)
        self.TopMost            = True
        self.ActiveControl      = None
        self.SetStyle(ControlStyles.DoubleBuffer, True)
        self.Show()
        self.Visible            = True

        self.brushBlack  = SolidBrush(Color.Black)
        self.brushGreen  = SolidBrush(Color.Green)
        self.brushRed    = SolidBrush(Color.Red)
        self.brushYellow = SolidBrush(Color.Yellow)
        self.brushWhite  = SolidBrush(Color.White)
        
        self.MainLoop()

#===================================================================================
    def _OnFormClosed(self, e):
        self.Dispose()
        self.isFormRunning = False

#===================================================================================
    def _OnResizeForm(self, e, ee):
        try:
            startingPointX = 300
            if self.Width-300 > 300:
                startingPointX = self.Width-300               
            
            self.multiLinedTextbox.Location          = Point(startingPointX, 50)
            self.multiLinedTextbox.Width             = 300
            self.multiLinedTextbox.Height            = self.Height
            
            self.hasDatasetChanged = True
        except:
            Log("Exception: _OnResizeForm()")
    
#===================================================================================
    def _CreateMultiLinedTextBox(self):
        t = TextBox()
        
        startingPointX = 300
        if self.Width-300 > 300:
            startingPointX = self.Width-300   
        
        t.Location          = Point(startingPointX, 50)
        t.Width             = 300
        t.Height            = self.Height
        t.Multiline         = True
        t.ForeColor         = Color.White
        t.BackColor         = Color.Black
        t.Font              = Font("Consolas", 12)
        
        self.Controls.Add(t)
        
        self.multiLinedTextbox = t
        
        return t

#===================================================================================
    def _CreateButton(self, buttonType, buttonData):

        try:
            b = Button()
            
            b.Width                     = 50
            b.Height                    = 50
            b.ForeColor                 = Color.White
            b.BackColor                 = Color.Gray
            b.Location                  = Point(0, 0)
            b.TabStop                   = False
            b.FlatStyle                 = FlatStyle.Flat
            b.FlatAppearance.BorderSize = 0            
            b.Cursor                    = Cursors.Hand
            b.Tag                       = [buttonType, buttonData]
            
            if buttonType == self.ButtonType.SetLootbag:
                path = Misc.CurrentScriptDirectory()
                path += "\\"
                b.BackgroundImage           = Image.FromFile(path + "lootbag.png")
                b.MouseDown                 += MouseEventHandler(self._OnMouseClick)
                
            elif buttonType == self.ButtonType.ItemWorld:
                b.ImageAlign                = ContentAlignment.MiddleCenter
                b.BackgroundImageLayout     = ImageLayout.Zoom
                Misc.Pause(100)
                itm = Items.FindBySerial(buttonData.item.Serial)
                b.BackgroundImage           = itm.Image
                b.MouseDown                 += MouseEventHandler(self._OnMouseClick)
                b.MouseHover                += EventHandler(self._OnMouseHoverEnter)
                b.MouseLeave                += EventHandler(self._OnMouseHoverLeave)
            
            self.Controls.Add(b)

            return b                
        except:
            Log("Exception: _CreateButton("+str(buttonType)+")")

#===================================================================================
    def _DisplayItemInformation(self, item):
        self.multiLinedTextbox.Clear()

        string = str(hex(Player.Serial)).upper()
        string = string[:0] + string[2:]
        string = "0x"+string
        self.multiLinedTextbox.Text += "PC S_ID         : "+ string +"\r\n"
        string = str(hex(Player.Backpack.Serial)).upper()
        string = string[:0] + string[2:]
        string = "0x"+string
        self.multiLinedTextbox.Text += "PC Bag S_ID     : "+ string +"\r\n"
        itemBank = Player.Bank
        if itemBank != None:        
            string = str(hex(itemBank.Serial)).upper()
            string = string[:0] + string[2:]
            string = "0x"+string
            self.multiLinedTextbox.Text += "PC Bank S_ID    : "+ string +"\r\n"
        
        self.multiLinedTextbox.Text += "\r\n"
        
        self.multiLinedTextbox.Text += "Name            : "+str(item.Name) +"\r\n"
        self.multiLinedTextbox.Text += "Amount          : "+str(item.Amount) +"\r\n"
        string = str(hex(item.Serial)).upper()
        string = string[:0] + string[2:]
        string = "0x"+string
        self.multiLinedTextbox.Text += "SerialID        : "+ string +"\r\n"
        string = str(hex(item.ItemID)).upper()
        string = string[:0] + string[2:]
        string = "0x"+string
        self.multiLinedTextbox.Text += "ItemID          : "+ string +"\r\n"
        self.multiLinedTextbox.Text += "Hue             : "+str(item.Hue) +"\r\n"
        self.multiLinedTextbox.Text += "Position        : "+str(item.Position.X)+", "+str(item.Position.Y)+", "+str(item.Position.Z) +"\r\n"

        self.multiLinedTextbox.Text += "\r\n"

        string = str(hex(item.Container)).upper()
        string = string[:0] + string[2:]
        string = "0x"+string
        self.multiLinedTextbox.Text += "Container       : "+ string +"\r\n"
        string = str(hex(item.RootContainer)).upper()
        string = string[:0] + string[2:]
        string = "0x"+string
        self.multiLinedTextbox.Text += "RootContainer   : "+ string +"\r\n"

        self.multiLinedTextbox.Text += "\r\n"
        
        self.multiLinedTextbox.Text += "IsContainer     : "+str(item.IsContainer) +"\r\n"
        self.multiLinedTextbox.Text += "IsCorpse        : "+str(item.IsCorpse) +"\r\n"
        self.multiLinedTextbox.Text += "IsDoor          : "+str(item.IsDoor) +"\r\n"
        self.multiLinedTextbox.Text += "IsPotion        : "+str(item.IsPotion) +"\r\n"
        self.multiLinedTextbox.Text += "Movable         : "+str(item.Movable) +"\r\n"
        self.multiLinedTextbox.Text += "IsTwoHanded     : "+str(item.IsTwoHanded) +"\r\n"
        self.multiLinedTextbox.Text += "OnGround        : "+str(item.OnGround) +"\r\n"
        self.multiLinedTextbox.Text += "Visible         : "+str(item.Visible) +"\r\n"
        self.multiLinedTextbox.Text += "IsInBank        : "+str(item.IsInBank) +"\r\n"
        self.multiLinedTextbox.Text += "Durability      : "+str(item.Durability) +"\r\n"

        self.multiLinedTextbox.Text += "\r\n"

        for property in item.Properties:
            self.multiLinedTextbox.Text += "Property        : "+ str(property) +"\r\n"
        
        self.multiLinedTextbox.Text += "\r\n"

        if item.OnGround == True:
            self.multiLinedTextbox.Text += "Distance        : "+str(item.DistanceTo(self.mobilePlayer)) +"\r\n"

#===================================================================================
    def _OnMouseHoverEnter(self, event, eventArgs):
        buttonType = event.Tag[0]
        buttonData = event.Tag[1]
        
        if buttonType == self.ButtonType.ItemWorld:
            self._DisplayItemInformation(buttonData.item)
            
#===================================================================================
    def _OnMouseHoverLeave(self, event, eventArgs):
        buttonType = event.Tag[0]
        buttonData = event.Tag[1]
            
#===================================================================================
    def _OnMouseClick(self, event, mouseEventArgs):
        buttonType = event.Tag[0]
        buttonData = event.Tag[1]
        
        try:
            if mouseEventArgs.Button == MouseButtons.Left:

                if buttonType == self.ButtonType.SetLootbag:
                    self.serialID_lootbag = Target.PromptTarget("Target your loot bag.")
                    lootbag = Items.FindBySerial(self.serialID_lootbag)
                    if lootbag == None:
                        self.serialID_lootbag = 0
                    elif lootbag.IsContainer == False:
                        self.serialID_lootbag = 0
                    elif self.serialID_lootbag == Player.Backpack.Serial:
                        self.serialID_lootbag = 0
                    else:
                        self._UpdateForm()

                elif buttonType == self.ButtonType.ItemWorld:

                    if buttonData.item.RootContainer == Player.Serial and buttonData.item.Container == Player.Backpack.Serial:
                        # Drop item from backpack onto the ground
                        Items.DropItemGroundSelf(buttonData.item, 0)
                    else:
                        # Pickup item from ground and place it into the players backpack
                        if self.serialID_lootbag == 0:
                            Items.Move(buttonData.item.Serial, Player.Backpack.Serial, 0)
                        else:
                            Items.Move(buttonData.item.Serial, self.serialID_lootbag, 0)

            Misc.FocusUOWindow()
        except:
            Log("Exception: _OnMouseClick("+str(buttonType)+")")            

#===================================================================================
    def _ProcessItemList(self, container):
        self.updateTick += 1

        itemList = []
        hasException = False

        for item in container.Contains:
            itemList.append(item)

        wasListUpdated = False
        for item in itemList:

            if item.IsInBank == True:
                continue

            if item.RootContainer > 0 and item.Container > 0:
                if item.RootContainer == item.Container:
                    continue

            # Item found, skip
            itemDataObjectFound = False
            for itemDataObject in self.itemDataObjectList:
                if itemDataObject.Serial == item.Serial:
                    itemDataObjectFound = True
                    itemDataObject.updateTick = self.updateTick
                    
                    if itemDataObject.Container != item.Container:
                        itemDataObject.Container = item.Container
                        wasListUpdated = True
                    break

            # Add New Item
            if itemDataObjectFound == False:
                wasListUpdated = True
                #Misc.SendMessage("New item")
                #Misc.Pause(1000)
                #item = Items.FindBySerial(item.Serial)
                newItemDataObject = ItemButtonDataContainer(self.updateTick
                                                           , item.Serial
                                                           , item.Container
                                                           , item
                                                           , self._CreateButton(self.ButtonType.ItemWorld, ItemButtonDataContainer(0, item.Serial, item.Container, item, None)))
                self.itemDataObjectList.append(newItemDataObject)

        # Remove Old Item
        for i in range(len(self.itemDataObjectList) - 1, -1, -1):
            if self.itemDataObjectList[i].updateTick < self.updateTick:
                wasListUpdated = True
                
                self.Controls.Remove(self.itemDataObjectList[i].button)
                del self.itemDataObjectList[i]
        
        if wasListUpdated == True:
            self._UpdateForm()
        
#===================================================================================
    def _UpdateForm(self):
        
        captionDataList = []
        self.graphicsLayer.FillRectangle(self.brushBlack, -5, -5, self.Width + 5, self.Height + 5)

        
        self.itemDataObjectIndexList = []
        for index in range(len(self.itemDataObjectList)):
            self.itemDataObjectIndexList.append(index)

        linePosX = 0
        linePosZ = 0
            
        # Unsorted Items
        if len(self.itemDataObjectIndexList) > 0:
            linePosX = 0
            linePosZ += 150
            captionDataList.append(["Unsorted items, this is considered a bug!", 0, linePosZ-15])
            for index in range(len(self.itemDataObjectIndexList) - 1, -1, -1):
                indexResult = self.itemDataObjectIndexList[index]
                itemDataObject = self.itemDataObjectList[indexResult]

                # Set Button Position
                if linePosX > self.Width - 350:
                    linePosX = 0
                    linePosZ += 51
                
                itemDataObject.button.Visible = True
                itemDataObject.button.Enabled = True
                itemDataObject.button.Location = Point(linePosX, linePosZ)
                linePosX += 51

                self.itemDataObjectIndexList.pop(index)


        # Draw text captions
        for caption in captionDataList:
            TextRenderer.DrawText(self.graphicsLayer, caption[0], self.Font, Point(caption[1], caption[2]), Color.White, Color.Black, TextFormatFlags.Default)
        
#===================================================================================
    def MainLoop(self):
        
        self.ButtonType = enum( MainForm     = 0
                              , ItemWorld    = 1
                              , SetLootbag   = 2)

                              
        self.serialID_lootbag = 0
        self._CreateButton(self.ButtonType.SetLootbag, 0)

        self.mobilePlayer   = Mobiles.FindBySerial(Player.Serial)
        
        self.graphicsLayer = self.CreateGraphics()
        
        
        self.lapseTimer__ProcessItemList = 0
        self.itemDataObjectList = []
        self.itemDataObjectIndexList = []
        
        self._CreateMultiLinedTextBox()
        self.hasDatasetChanged = False
        
        self.lastCountDataSetUpdate = 0
        self.updateTick     = 0
        self.elapsedTime    = 0
        self.elapsedCounter = 0
        self.isFormRunning  = True

        self.headMessageTimer = 0
        
        src = Target.PromptTarget("")
        container = Items.FindBySerial(src)
        

        while self.isFormRunning == True:

            SetUnixTime()
            
            self.elapsedCounter += 1
            if currentTime >= self.elapsedTime:
                self.elapsedTime = currentTime + 1000
                #Log(str(self.elapsedCounter))    
                TextRenderer.DrawText(self.graphicsLayer, str(self.elapsedCounter), self.Font, Point(self.Width - 60, 0), Color.White, Color.Black, TextFormatFlags.Default)            
                self.elapsedCounter = 0            

            self.lapseTimer__ProcessItemList += 1
            hasItemListChanged = False
            if self.lapseTimer__ProcessItemList > 50:
                self.lapseTimer__ProcessItemList = 0
                self._ProcessItemList(container)
            
            Application.DoEvents()
            continue
            
f = RunForm()