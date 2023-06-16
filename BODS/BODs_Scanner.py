import clr
import sys

DEF_FILEPATH = "C:\\temp\\bods.txt"
DEF_LARGE_BOD = "Large"
DEF_SMALL_BOD = "Small"


def stopWithError(errorMessage):
    Misc.SendMessage(errorMessage)
    sys.exit(errorMessage)


class Craftable:
    def __init__(self, name, quality, material):
        self.__name = name
        self.__quality = quality
        self.__material = material
        self.__amountmin = 0
        self.__amountmax = 0

    def addAmountStr(self, amountStr):
        self.__amountmin = int(amountStr.split('/')[0].strip())
        self.__amountmax = int(amountStr.split('/')[1].strip())

    def toString(self):
        debugstr = ""
        debugstr = debugstr + self.__name + ";"
        debugstr = debugstr + self.__quality + ";"
        debugstr = debugstr + self.__material + ";"
        debugstr = debugstr + str(self.__amountmin) + "/" + str(self.__amountmax)
        return debugstr


class BodContract:
    def __init__(self, bodtype):
        self.__bodtype = bodtype
        self.__craftableList = []
        self.__pushedamountidx = 0
        self.__buttonid = 0

    def addCraftable(self, name, quality, material, bodbuttonid):
        self.__buttonid = bodbuttonid
        self.__craftableList.append(Craftable(name, quality, material))

    # Returns the number of pushed amounts. If return = len of the list means is full
    def pushAmountStr(self, amountStr):
        idx = self.__pushedamountidx
        if idx >= len(self.__craftableList):
            return None
        
        self.__craftableList[idx].addAmountStr(amountStr)
        self.__pushedamountidx = idx + 1
        return self.__pushedamountidx

    # Return True if not all Amounts have been pushed
    def needPushedAmount(self):
        if self.__pushedamountidx == 0:  # If it's 0 means it's the first value and it needs an amount
            return True

        if self.__pushedamountidx == len(self.__craftableList): # It's for large bods to see when all amount are pushed
            return False
        else:
            return True

    def getBodType(self):
        return self.__bodtype

    def getButtonId(self):
        return self.__buttonid

    def toString(self):
        debugstr = self.__bodtype + ";"
        for i in self.__craftableList:
            debugstr = debugstr + i.toString() + "\n"
        return debugstr


class BookPage:
    def __init__(self, pageNum):
        self.__listBODS = []
        self.__lastpushedbodNum = 0
        self.__pageNum = pageNum
    
    def addBod(self, bodContract):
        self.__listBODS.append(bodContract)

    def getBod(self, bodindex):
        if 0 <= bodindex < len(self.__listBODS):
            return self.__listBODS[bodindex]
        else:
            return None

    def pushAmountStr(self, amountStr):
        if not self.__listBODS[self.__lastpushedbodNum].needPushedAmount():
            self.__lastpushedbodNum = self.__lastpushedbodNum + 1
        self.__listBODS[self.__lastpushedbodNum].pushAmountStr(amountStr)

    def getAllBodsInPage(self):
        return self.__listBODS

    def getNumOfBods(self):
        return len(self.__listBODS)

    def toString(self):
        debugstr = "Page: " + str(self.__pageNum) + "\n"
        for bod in self.__listBODS:
            debugstr = debugstr + bod.toString()
        return debugstr


class Book:
    def __init__(self, item):
        self.bookitem = item
        self.__listBODS = []
    
    def addPage(self, page):
        self.__listBODS = self.__listBODS + page.getAllBodsInPage()

    def getAllBODs(self):
        return self.__listBODS


def scanPage(pageNum):
    gumpdata = Gumps.LastGumpGetLineList()
    page = BookPage(pageNum)

    scanActive = True
    i = 0
    while scanActive:
        #Misc.Pause(1)
        if DEF_SMALL_BOD in gumpdata[i]:
            name = gumpdata[i+1]
            quality = gumpdata[i+2]
            material = gumpdata[i+3]
            buttonid = (i * 2) + (20 * pageNum) + 5
            contract = BodContract(DEF_SMALL_BOD)
            contract.addCraftable(name, quality, material, buttonid)
            page.addBod(contract)
            i = i + 4
        elif DEF_LARGE_BOD in gumpdata[i]:
            largeContract = BodContract(DEF_LARGE_BOD)
            while True:
                name = gumpdata[i + 1]
                quality = gumpdata[i + 2]
                material = gumpdata[i + 3]
                buttonid = (i * 2) + (20 * pageNum) + 5
                largeContract.addCraftable(name, quality, material, buttonid)

                i = i + 3

                if '<BASEFONT COLOR' in gumpdata[i + 1]:
                    page.addBod(largeContract)
                    scanActive = False
                    break

                if DEF_SMALL_BOD in gumpdata[i + 1] or DEF_LARGE_BOD in gumpdata[i + 1]:
                    page.addBod(largeContract)
                    break

        elif '<BASEFONT COLOR' in gumpdata[i]:
            break

        else:
            i += 1

    index = gumpdata.FindIndex(lambda x: x.Contains('<BASEFONT COLOR'))

    # AmountStr are written after the list of the items. I need to push them into the page class and let push
    for i in range(len(gumpdata)):
        if i > index:
            if "/" in gumpdata[i]:
                page.pushAmountStr(gumpdata[i])
    return page
                
 
def bookHasNextPage(gumpSerial):
    gumpdata = Gumps.LastGumpGetLineList()
    return gumpdata.FindIndex(lambda x: x.Contains('Next page')) > 0


def scanBook(bookofBODs):
    Journal.Clear()
    Items.UseItem(bookofBODs)
    Misc.Pause(500)

    if Journal.Search("The book is empty."):
        return Book(bookofBODs.Name) # This returns an empty book
    
    gumpSerial = Gumps.CurrentGump()
    
    bookContent = Book(bookofBODs.Name)
    pageNum = 0
    while True:
        Misc.SendMessage("Scanning page: " + str(pageNum))
        page = scanPage(pageNum)
        bookContent.addPage(page)
        
        if bookHasNextPage(gumpSerial) == False:
            break
        else:
            Gumps.SendAction(gumpSerial, 3)
            Gumps.WaitForGump(gumpSerial, 30000)
        Misc.Pause(10)
        pageNum = pageNum + 1
            
    return bookContent


def removeFirstLargeAvailable(largeBODBookSerial):
    bookofBODs = Items.FindBySerial(largeBODBookSerial)
    Items.UseItem(bookofBODs)
    Misc.Pause(500)

    if Journal.Search("The book is empty."):
        return None

    gumpSerial = Gumps.CurrentGump()

    pageNum = 0
    while True:
        Misc.SendMessage("Scanning for a Large BOD")
        page = scanPage(pageNum)
        for bod in page.getAllBodsInPage():
            if bod.getBodType() == DEF_LARGE_BOD:
                Misc.SendMessage("Found a Large BOD")
                #Gumps.SendAction(gumpSerial, bod.getButtonId())
                #Gumps.WaitForGump(gumpSerial, 30000)
                return bod

        if not bookHasNextPage(gumpSerial):
            Misc.SendMessage("No more pages availabes")
            break
        else:
            Gumps.SendAction(gumpSerial, 3)
            Gumps.WaitForGump(gumpSerial, 30000)
        Misc.Pause(10)
        pageNum = pageNum + 1

    return None



###############################################


## CHECK BOOK IS IN BACKPACK. Altrimenti fallisce lo script. Il gump è diverso se non è nello zaino

smallFilledBookSerial = Target.PromptTarget("Select BODs book")
smallBook = Items.FindBySerial(smallFilledBookSerial)

book = scanBook(smallBook)

f = open(DEF_FILEPATH, "w")
for bod in book.getAllBODs():
    f.write(bod.toString())
f.close()

Misc.SendMessage("Book contains " + str(len(book.getAllBODs())) + " BODs")


