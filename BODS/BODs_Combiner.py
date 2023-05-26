import clr
import sys

# DEF_FILEPATH = "d:\\bods.txt"
EMPTY_BODS_ALLOWED = 100 #  100 Means fill what you can

DEF_LARGE_BOD = "Large"
DEF_SMALL_BOD = "Small"
DEF_BODS_GRAPHICID = 0x2258


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

    def smartCompareWithAFilled(self, cratable):
        a = (self.__name == cratable.__name)
        b = (self.__quality == cratable.__quality)
        c = (self.__material == cratable.__material)
        d = (self.__amountmax == cratable.__amountmax)
        e = (self.__amountmax == cratable.__amountmin)  # Must be filled so min = max
        if a == b == c == d == e:
            return True
        else:
            return False

    def isFilled(self):
        return self.__amountmin > 0 and self.__amountmin == self.__amountmax


class BodContract:
    def __init__(self, bodtype):
        self.__bodtype = bodtype
        self.__craftableList = []
        self.__pushedamountidx = 0
        self.__bodindexinbook = 0

    def addCraftable(self, name, quality, material, bodindexinbook):
        self.__bodindexinbook = bodindexinbook
        self.__craftableList.append(Craftable(name, quality, material))

    def setBodIndexInBook(self, index):
        self.__bodindexinbook = index

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

        if self.__pushedamountidx == len(
                self.__craftableList):  # It is for large bods to see when all amount are pushed
            return False
        else:
            return True

    def getBodType(self):
        return self.__bodtype

    def getCraftables(self):
        return self.__craftableList

    def getBodIndexInBook(self):
        return self.__bodindexinbook

    def getButtonId(self):
        return 5 + (2 * self.__bodindexinbook)

    def removeCraftable(self, craftale):
        self.__craftableList.remove(craftale)

    def toString(self):
        debugstr = ""
        debugstr = debugstr + "BodIndex: " + str(self.__bodindexinbook) + ";"
        debugstr = debugstr + self.__bodtype + ";"
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

    def haveThisBod(self, bodContract):
        for bod in self.__listBODS:
            if bod == bodContract:
                return True

    def getAllBodsInPage(self):
        return self.__listBODS

    def getNumOfBods(self):
        return len(self.__listBODS)

    def removeBod(self, bodNumber):
        pass

    def toString(self):
        debugstr = "Page: " + str(self.__pageNum) + "\n"
        for bod in self.__listBODS:
            debugstr = debugstr + bod.toString()
        return debugstr


class Book:
    def __init__(self, item):
        self.bookitem = item  # Razor Item object
        self.__listBODS = []

    def addPage(self, page):
        self.__listBODS = self.__listBODS + page.getAllBodsInPage()

    def getAllBODs(self):
        return self.__listBODS

    def findSmallBod(self, craftable):
        found = None
        for bod in self.__listBODS:
            if bod.getBodType() == DEF_SMALL_BOD:
                if craftable.smartCompareWithAFilled(bod.getCraftables()[0]):
                    return bod
        return found

    def removeBod(self, bod):
        bodNumber = bod.getBodIndexInBook()
        buttonID = -1
        for i in range(len(self.__listBODS)):
            if self.__listBODS[i].getBodIndexInBook() == bodNumber:
                buttonID = self.__listBODS[i].getButtonId()
                del self.__listBODS[i]
                break

        # Updating all indexes
        for i in range(len(self.__listBODS)):
            self.__listBODS[i].setBodIndexInBook(i)

        return buttonID


def scanPage(pageNum):
    gumpdata = Gumps.LastGumpGetLineList()
    page = BookPage(pageNum)

    scanActive = True
    i = 0
    bodcnt = 0
    while scanActive:
        if DEF_SMALL_BOD in gumpdata[i]:
            name = gumpdata[i + 1]
            quality = gumpdata[i + 2]
            material = gumpdata[i + 3]
            # buttonid = (bodcnt * 2) + (20 * pageNum) + 5
            bodNumber = (pageNum * 10) + bodcnt
            contract = BodContract(DEF_SMALL_BOD)
            contract.addCraftable(name, quality, material, bodNumber)
            page.addBod(contract)
            bodcnt += 1
            i = i + 4
        elif DEF_LARGE_BOD in gumpdata[i]:
            largeContract = BodContract(DEF_LARGE_BOD)
            while True:
                name = gumpdata[i + 1]
                quality = gumpdata[i + 2]
                material = gumpdata[i + 3]
                # buttonid = (bodcnt * 2) + (20 * pageNum) + 5
                bodNumber = (pageNum * 10) + bodcnt
                largeContract.addCraftable(name, quality, material, bodNumber)
                i = i + 3

                if '<BASEFONT COLOR' in gumpdata[i + 1]:
                    page.addBod(largeContract)
                    bodcnt += 1
                    scanActive = False
                    break

                if DEF_SMALL_BOD in gumpdata[i + 1] or DEF_LARGE_BOD in gumpdata[i + 1]:
                    page.addBod(largeContract)
                    bodcnt += 1
                    break

        elif '<BASEFONT COLOR' in gumpdata[i]:
            break

        else:
            i += 1

    index = gumpdata.FindIndex(lambda x: '<BASEFONT COLOR' in x)

    # AmountStr are written after the list of the items. I need to push them into the page class and let push
    for i in range(len(gumpdata)):
        if i > index:
            if "/" in gumpdata[i]:
                page.pushAmountStr(gumpdata[i])
    return page


def bookHasNextPage(gumpSerial):
    gumpdata = Gumps.LastGumpGetLineList()
    return gumpdata.FindIndex(lambda x: 'Next page' in x) > 0


def openBookOfBods(bookItem):
    Gumps.CloseGump(0)
    Journal.Clear()
    Items.UseItem(bookItem)
    Misc.Pause(500)

    if Journal.Search("The book is empty."):
        return None

    Gumps.WaitForGump(0, 30000)
    return Gumps.CurrentGump()


def scanBook(bookofBODsItem):
    gumpSerial = openBookOfBods(bookofBODsItem)
    if gumpSerial is None:
        return Book(bookofBODsItem.Name)  # This returns an empty book

    bookContent = Book(bookofBODsItem.Name)
    pageNum = 0
    while True:
        Misc.SendMessage("Scanning page: " + str(pageNum))
        page = scanPage(pageNum)
        bookContent.addPage(page)

        if not bookHasNextPage(gumpSerial):
            break
        else:
            Gumps.SendAction(gumpSerial, 3)
            Gumps.WaitForGump(gumpSerial, 30000)
        Misc.Pause(10)
        pageNum = pageNum + 1

    Gumps.CloseGump(gumpSerial)
    return bookContent


def readFirstLargeAvailable(bookofBODs):
    gumpSerial = openBookOfBods(bookofBODs)
    if gumpSerial is None:
        return [None, None]

    pageNum = 0
    while True:
        Misc.SendMessage("Scanning for a Large BOD")
        page = scanPage(pageNum)
        for bod in page.getAllBodsInPage():
            if bod.getBodType() == DEF_LARGE_BOD:
                Misc.SendMessage("Found a Large BOD")

                # Now I do a trick. If there are already some BODS in backpack i get all their serial
                # then i pop out the bod and search again all serial.
                # The latest BOD is the difference between the 2 lists of serials
                before = listOfBODsInBackpack()
                Gumps.SendAction(gumpSerial, bod.getButtonId())
                Gumps.WaitForGump(gumpSerial, 30000)
                Misc.Pause(500)
                after = listOfBODsInBackpack()
                serial = list(set(after) - set(before))[0]  # First element of the difference
                return [bod, serial]

        if not bookHasNextPage(gumpSerial):
            Misc.SendMessage("No more pages availabes")
            break
        else:
            Gumps.SendAction(gumpSerial, 3)
            Gumps.WaitForGump(gumpSerial, 30000)
        Misc.Pause(10)
        pageNum = pageNum + 1

    Gumps.CloseGump(gumpSerial)
    return [None, None]


def removeSmallBods(smallBookItem, bookContent, largeBod, emptyBODsAllowed=1):
    Misc.SendMessage("Searching for valid BODS")

    foundBods = []
    foundCnt = 0
    pulledOut = 0
    for tobefilled in largeBod.getCraftables():
        # Manage partially filled BOD
        if tobefilled.isFilled():
            foundCnt += 1
            continue

        found = bookContent.findSmallBod(tobefilled)
        if found is not None:
            foundCnt += 1
            foundBods.append(found)

    # It is ok if not all the large bod is filled.
    if foundCnt >= len(largeBod.getCraftables()) - emptyBODsAllowed:
        Misc.SendMessage("Found minimum amount")
        gumpSerial = openBookOfBods(smallBookItem)
        if gumpSerial is None:
            return
        Misc.Pause(500)
        # Misc.SendMessage("Pulling out from the book")
        for bod in foundBods:
            Misc.SendMessage(bod.toString())
            buttonID = bookContent.removeBod(bod)
            Misc.SendMessage(buttonID)
            Gumps.SendAction(gumpSerial, buttonID)
            Gumps.WaitForGump(gumpSerial, 30000)
            Misc.Pause(800)
            pulledOut += 1
    else:
        Misc.SendMessage("This large bod it not fillable", 33)
        return False

    # I am here if the bod is considered valid for the emptyBODsAllowed rule but no small bods have been added
    # this means that bod was a partial bod and search did not find anything useful.
    if pulledOut > 0:
        Gumps.CloseGump(gumpSerial)
        return True

    return False


def listOfBODsInBackpack():
    itemList = []
    for item in Player.Backpack.Contains:
        if item.ItemID == DEF_BODS_GRAPHICID:
            itemList.append(item.Serial)
    return itemList


def isLargeBodFilled(largeSerial):
    bod = Items.FindBySerial(largeSerial)
    
    amount = None
    for prop in bod.Properties:
        s = prop.ToString()
        if s.lower().find("amount to make:") != -1:
            amount = s.split(':')[1]
            continue
        if amount is not None:
            if ":" in s:
                done = s.split(':')[1]
                if done != amount:
                    return False

    if amount is None:
        return False
    return True
    
    
def combineBods(largeSerial):
    bods = listOfBODsInBackpack()
    Misc.Pause(1000)
    Items.UseItem(largeSerial)
    Gumps.WaitForGump(0, 30000)
    gumpSerial = Gumps.CurrentGump()
    Misc.Pause(500)
    Gumps.SendAction(gumpSerial, 2)  # Button Combine
    Target.WaitForTarget(30000, False)
    
    for bod in bods:
        if bod != largeSerial:
            Misc.SendMessage("Adding small bod to large", 66)
            Target.TargetExecute(bod)
        Misc.Pause(500)
                
    Target.Cancel()
        
    Gumps.CloseGump(gumpSerial)
    return isLargeBodFilled(largeSerial)

##############################################

# TODO:
# CHECK BOOK IS IN BACKPACK. Altrimenti fallisce lo script. Il gump è diverso se non è nello zaino
# CLEAR BODS FILTER IF CLEAR_FILTER == True  (Farlo nella funzione openBookOfBods)
# READ THE NUMBER OF BODS IN THE LARGE BOOK AND USE A FOR INSTEAD OF WHILE TRUE
# IMPROVE combineBods finding only needed bods and repeat untill all are taken

#combineBods(0x41224AA9)


largeBookSerial = Target.PromptTarget("Select large BODs book")
if largeBookSerial == -1:
    stopWithError("Target Canceled")
largeBookItem = Items.FindBySerial(largeBookSerial)

smallBookSerial = Target.PromptTarget("Select Small BODs book")
if smallBookSerial == -1:
    stopWithError("Target Canceled")
smallBookItem = Items.FindBySerial(smallBookSerial)

filledBookSerial = Target.PromptTarget("Select Book where move FILLED BODs")
partialBookSerial = Target.PromptTarget("Select Book where move PARTIALLY FILLED BODs")

smallBook = scanBook(smallBookItem)

while True:
    Misc.Pause(100)

    [largeBod, largeBodSerial] = readFirstLargeAvailable(largeBookItem)
    if largeBod is None:
        break

    removedBods = removeSmallBods(smallBookItem, smallBook, largeBod, EMPTY_BODS_ALLOWED)
    if not removedBods:
        Items.Move(largeBodSerial, largeBookSerial, 1)
        Misc.Pause(250)
        Gumps.CloseGump(0)
        Misc.Pause(250)
    else:
        fullFilled = combineBods(largeBodSerial)
        if not fullFilled:
            # If not fully filled i put in partially filled book
            Items.Move(largeBodSerial, partialBookSerial, 1)
        else:
            # If fully filled i put in filled book
            Items.Move(largeBodSerial, filledBookSerial, 1)

        Misc.Pause(250)
        Gumps.CloseGump(0)
        Misc.Pause(250)
