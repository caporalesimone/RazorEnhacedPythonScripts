# Test gump
#
from System.Collections.Generic import List

class GumpPicID:
    BLACK_RECT = 2624
    WHITE_RECT_ROUND = 555
    ARROW_LEFT = 4015
    ARROW_LEFT_PRESS = 4016
    BLUE_DOT = 2117
    BLUE_DOT_PRESS = 2118
    DRAGON_EDGE_LEFT = 10440
    DRAGON_EDGE_RIGHT = 10441
    
class GumpBuilder():
    def __init__(self):
        self.elements = []
    
    def add(self,element):
        self.elements.append(element)
    
    def send(self, x, y, gumpID=1, gumpSerial=1):
        textList = []
        structure = ""
        for element in self.elements:
            structure += element.render()
            text = element.getText()
            if text is not None:
                textList.append(str(text))
        #
        # Misc.SendMessage("len: {}".format(structure))
        Gumps.SendGump(gumpID,gumpSerial,x,y,structure,List[str](textList))
        
    
class GumpElement():
    def __init__(self, name, *params):
        self.name = name
        self.params = [(str(param) if params is not None else 0) for param in params]
        self.text = None
    
    def render(self):
        
        params = " ".join(self.params)
        #Misc.SendMessage("{} {} {}".format(self.name, self.params, params))
        return "{ %s %s }" % (self.name, params)
        
    def getText(self): return self.text
        
class GumpPage(GumpElement):
    def __init__(self, pageNum):
        super().__init__("page", pageNum)
        
class GumpResizePic(GumpElement):
    def __init__(self, x, y,  width, height, picID):
        super().__init__("resizepic", x, y, width, height, picID)
        
class GumpPicTited(GumpElement):
    def __init__(self, x, y, width, height, picID):
        super().__init__("gumppictiled", x, y, width, height, picID)

class GumpCheckerTrans(GumpElement):
    def __init__(self, x, y, width, height):
        super().__init__("checkertrans", x, y, width, height)
        
class GumpPic(GumpElement):
    def __init__(self, x, y, picID):
        super().__init__("gumppic", x, y, picID)
        
class GumpTextHTML(GumpElement):
    data_index = 0
    
    def __init__(self, x, y, width, height, html, highlight=0, scrollbars=0):
        super().__init__("htmlgump", x, y, width, height, GumpTextHTML.data_index, highlight, scrollbars )
        GumpTextHTML.data_index += 1
        self.text = html

class GumpButton(GumpElement):
    def __init__(self, x, y, action_id, normal_picID, pressed_picID, send_gump=1, unknown=0 ):
        super().__init__("button", x, y, normal_picID, pressed_picID, send_gump, unknown, action_id )
 
 
def htmlColorText(text, color="FFFFFF"): 
    return "<basefont color=#{}>{}</basefont>".format(color,text)
        
def mainBuilder():
    builder = GumpBuilder()
    
    #add page
    builder.add( GumpPage(0) )
    # background
    builder.add( GumpResizePic(50,0,5054,400, GumpPicID.WHITE_RECT_ROUND ) )
    
    # header
    builder.add( GumpPicTited(58,8,384,24, GumpPicID.BLACK_RECT ) )
    builder.add( GumpCheckerTrans(58,8,384,24 ) )
    text = htmlColorText("CREDZBAs Teleporter")
    builder.add( GumpTextHTML(200,12,200, 15,text) )
    
    # background body 
    builder.add( GumpPicTited(58, 38, 384, 509, GumpPicID.BLACK_RECT )  )
    builder.add( GumpCheckerTrans(58, 38, 384, 509 )  )
    text = htmlColorText("Choose Your Destination:" )
    builder.add( GumpTextHTML(75,40,150,15,text)  )
    
    # dragons 
    builder.add( GumpPic(0,0,GumpPicID.DRAGON_EDGE_LEFT )  )
    builder.add( GumpPic(418,0,GumpPicID.DRAGON_EDGE_RIGHT )  )
    
    
    categories = [ 
        "Trammel Towns", "Trammel Dungeons", ["Felucca Towns", "FF0000"], ["Felucca Dungeons", "FF0000"], 
        "Public Moongates", "Ilshenar", "Ilshenar Shrines", "Malas", "Tokuno",
        "TerMur", ["Faraan","2A9952"], ["Dead Vales","8A46FF"], "Custom Locations"
    ]
    action_id = 100
    x_button = 70
    x_text = x_button + 20
    y_offset = 25
    y = 70
    for category in categories:
        color = "FFFFFF"
        if not isinstance(category, str):
            color = category[1]
            category = category[0]
        #
        builder.add( GumpButton(x_button,y,action_id,GumpPicID.BLUE_DOT,GumpPicID.BLUE_DOT_PRESS) )
        text = htmlColorText(category,color)
        builder.add( GumpTextHTML(x_text,y, 150, 15, text) )
        action_id += 1
        y += y_offset
    
    
    
    
    towns = [ 
        "TownCenter","Britain","BucsDen","Cove","Delucia",
        "NewHaven","Jhelom","Magincia","Minoc","Moonglow",
        "Nujel'm","Papua","SerpentsHold","SkaraBrae",
        "Trinsic","Vesper","Wind","Yew"
    ]
    
    action_id = 200
    x_button = 238
    x_text = x_button + 70
    y_offset = 25
    y = 70
    for town in towns:
        builder.add( GumpButton(x_button,y,action_id,GumpPicID.ARROW_LEFT,GumpPicID.ARROW_LEFT_PRESS) )
        text = htmlColorText(town)
        builder.add( GumpTextHTML(x_text,y, 150, 15, text) )
        action_id += 1
        y += 20
    
    
    
        
    
    
    builder.send(20,20)
    
    
    
def main():
    gumpDefinition = """
    { page 0 }
    { resizepic 50 0 5054 400 555 }

    { gumppictiled 58 38 384 509 2624 }
    { checkertrans 58 38 384 509 }
    
    { gumppictiled 58 8 384 24 2624 }
    { checkertrans 58 8 384 24 }
    

    { gumppic 0 0 10440 }
    { gumppic 418 0 10441 }
    { htmlgump 75 40 150 15 0 0 0 }
    { htmlgump 200 12 200 15 1 0 0 }

    { htmlgump 273 70 150 20 2 0 0 }{ button 238 70 4015 4016 1 0 100 }
    { htmlgump 273 90 150 20 3 0 0 }{ button 238 90 4015 4016 1 0 101 }
    { htmlgump 273 110 150 20 4 0 0 }{ button 238 110 4015 4016 1 0 102 }
    { htmlgump 273 130 150 20 5 0 0 }{ button 238 130 4015 4016 1 0 103 }
    { htmlgump 273 150 150 20 6 0 0 }{ button 238 150 4015 4016 1 0 104 }
    { htmlgump 273 170 150 20 7 0 0 }{ button 238 170 4015 4016 1 0 105 }
    { htmlgump 273 190 150 20 8 0 0 }{ button 238 190 4015 4016 1 0 106 }
    { htmlgump 273 210 150 20 9 0 0 }{ button 238 210 4015 4016 1 0 107 }
    { htmlgump 273 230 150 20 10 0 0 }{ button 238 230 4015 4016 1 0 108 }
    { htmlgump 273 250 150 20 11 0 0 }{ button 238 250 4015 4016 1 0 109 }
    { htmlgump 273 270 150 20 12 0 0 }{ button 238 270 4015 4016 1 0 110 }
    { htmlgump 273 290 150 20 13 0 0 }{ button 238 290 4015 4016 1 0 111 }
    { htmlgump 273 310 150 20 14 0 0 }{ button 238 310 4015 4016 1 0 112 }
    { htmlgump 273 330 150 20 15 0 0 }{ button 238 330 4015 4016 1 0 113 }
    { htmlgump 273 350 150 20 16 0 0 }{ button 238 350 4015 4016 1 0 114 }
    { htmlgump 273 370 150 20 17 0 0 }{ button 238 370 4015 4016 1 0 115 }
    { htmlgump 273 390 150 20 18 0 0 }{ button 238 390 4015 4016 1 0 116 }
    { htmlgump 273 410 150 20 19 0 0 }{ button 238 410 4015 4016 1 0 117 }

    { button 67 70 2117 2118 1 0 1 }{ htmlgump 87 70 150 20 20 0 0 }
    { button 67 95 2117 2118 1 0 2 }{ htmlgump 87 95 150 20 21 0 0 }
    { button 67 120 2117 2118 1 0 3 }{ htmlgump 87 120 150 20 22 0 0 }
    { button 67 145 2117 2118 1 0 4 }{ htmlgump 87 145 150 20 23 0 0 }
    { button 67 170 2117 2118 1 0 5 }{ htmlgump 87 170 150 20 24 0 0 }
    { button 67 195 2117 2118 1 0 6 }{ htmlgump 87 195 150 20 25 0 0 }
    { button 67 220 2117 2118 1 0 7 }{ htmlgump 87 220 150 20 26 0 0 }
    { button 67 245 2117 2118 1 0 8 }{ htmlgump 87 245 150 20 27 0 0 }
    { button 67 270 2117 2118 1 0 9 }{ htmlgump 87 270 150 20 28 0 0 }
    { button 67 295 2117 2118 1 0 10 }{ htmlgump 87 295 150 20 29 0 0 }
    { button 67 320 2117 2118 1 0 11 }{ htmlgump 87 320 150 20 30 0 0 }
    { button 67 345 2117 2118 1 0 12 }{ htmlgump 87 345 150 20 31 0 0 }
    { button 67 370 2117 2118 1 0 17 }{ htmlgump 87 370 150 20 32 0 0 }
    """
    gumpDefinition = gumpDefinition.replace("\n","")
    gumpTextList = []
    gumpTextList.append("<basefont color=#FFFFFF>Choose Your Destination:</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>CREDZBA's Teleporter</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Town Center</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Britain</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Bucs Den</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Cove</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Delucia</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>New Haven</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Jhelom</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Magincia</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Minoc</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Moonglow</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Nujel'm</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Papua</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Serpents Hold</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Skara Brae</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Trinsic</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Vesper</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Wind</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Yew</basefont>")

    gumpTextList.append("<basefont color=#FFFFFF>Trammel Towns</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Trammel Dungeons</basefont>")
    gumpTextList.append("<basefont color=#FF0000>Felucca Towns</basefont>")
    gumpTextList.append("<basefont color=#FF0000>Felucca Dungeons</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Public Moongates</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Ilshenar</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Ilshenar Shrines</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Malas</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Tokuno</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>TerMur</basefont>")
    gumpTextList.append("<basefont color=#2A9952>Faraan</basefont>")
    gumpTextList.append("<basefont color=#8A46FF>Dead Vales</basefont>")
    gumpTextList.append("<basefont color=#FFFFFF>Custom Locations</basefont>")

    Gumps.SendGump(1,1,10,10,gumpDefinition,List[str](gumpTextList))
    
    
main()

mainBuilder()