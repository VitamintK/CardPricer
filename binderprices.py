#!/usr/bin/python  
# Hello World from Python
import pickle
import requests
import sys
import os
import datetime
# minidom import xml.dom.minidom
import xml.etree.ElementTree as ET
"""data structure: outputs are tuples of (array,int). The array contains arrays of the form [price,cardID].
the int is the total price of the output."""


#todo:
#1.error handling for all steps
#2. ignore damaged lightly played listings, or be able to set condition
#3. ultimate/ultra and secret/super rarities
#4. set 1st edition etc
#5. "x2" or "x3" will account for multiple of a card
#6. seperate the functions that add cards to binderlist (from wikia and file and user input), and the functions that return values for those cards
#7. close files after handling.
#8. add saving methods, and be able to sortlist() and printout() without running a get...() method again
#9. learn github
#10. perhaps save the results of getNameFromSet() to a list before printing?
#ignore lots, ignore oricas

#binderlist = []
#output = []
#totalprice = 0

def getBestPrice(line):
    r = requests.get("http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.12.0&SECURITY-APPNAME=BigWangG-bf74-456b-b2ab-74125859229c&RESPONSE-DATA-FORMAT=XML&REST-PAYLOAD&sortOrder=PricePlusShippingLowest&keywords="+line+"&paginationInput.entriesPerPage=1&itemFilter(0).name=ListingType&itemFilter(0).value(0)=FixedPrice&itemFilter(0).value(1)=AuctionWithBIN""")
    tree = ET.fromstring(r.text.encode('ascii', 'ignore'))
    asdf=tree.find(".//{http://www.ebay.com/marketplace/search/v1/services}buyItNowAvailable")
    try:
        if asdf.text == "true":
            price = float(tree.find(".//{http://www.ebay.com/marketplace/search/v1/services}convertedBuyItNowPrice").text)
        else:
            price = float(tree.find(".//{http://www.ebay.com/marketplace/search/v1/services}convertedCurrentPrice").text)
        #print tree.findall(".//")
        #print r.text
        try:
            price+=float(tree.find(".//{http://www.ebay.com/marketplace/search/v1/services}shippingServiceCost").text)
        except AttributeError:
            print "shipping cost uncertain - estimated as $2"
            price+=2
        return price
    #print line+" "+str(price)
    except:
        print "error in getBestPrice"
        return 0
def getTextInput(g):
    binderlist = []
    totalprice = 0
    f=g.split('\n')
    print f
    for line in f:
        line = line.strip()
        try:
            if (line[0]=="/" and line[1]=="/"):
                print line.strip()
            elif (line[0]=="x"):
                for x in range(int(line[1])):
                    temp=line[2:].strip()
                    price = getBestPrice(temp)
                    binderlist.append([temp,price])
                    totalprice+=price
                    print temp+": "+str(price)
            elif (line[1] == "x"):
               for x in range(int(line[0])):
                    temp=line[2:].strip()
                    price = getBestPrice(temp)
                    binderlist.append([temp,price])
                    totalprice+=price
                    print temp+": "+str(price)    
            else:
                line=line.strip()
                price = getBestPrice(line)
                binderlist.append([line,price])
                totalprice+=price
                print line+": "+str(price)
        except:
            print "empty line"
    return binderlist,totalprice
def getFileInput(thefile):
    binderlist = []
    totalprice = 0
    #global totalprice
    f = open(thefile, 'r')
    for line in f:
        if (line[0]=="/" and line[1]=="/"):
            print line.strip()
        elif (line[0]=="x"):
            for x in range(int(line[1])):
                temp=line[2:].strip()
                price = getBestPrice(temp)
                binderlist.append([temp,price])
                totalprice+=price
                print temp+": "+str(price)
        elif (line[1] == "x"):
           for x in range(int(line[0])):
                temp=line[2:].strip()
                price = getBestPrice(temp)
                binderlist.append([temp,price])
                totalprice+=price
                print temp+": "+str(price)
        else:
            line=line.strip()
            price = getBestPrice(line)
            binderlist.append([line,price])
            totalprice+=price
            print line+": "+str(price)
    return binderlist,totalprice

def addUserInput():
    while True:
        print "hi"
        addTo = raw_input("enter shit nigga")
        if addTo == "q":
            break
        else:
            pass
            #binderlist.append(addTo)

def getSet(setname):
    binderlist = []
    totalprice = 0
    totalcards = raw_input("Enter the number of the last card in the set of "+setname+"\n")
    for i in range(0,int(totalcards)+1):
        if i<10:
            leadingz = "00"
        elif i<100:
            leadingz = "0"
        elif i<1000:
            leadingz = ""
        line = setname+"-EN"+leadingz+str(i)
        price = getBestPrice(line)
        #print r.text
        binderlist.append([line,price])
        totalprice+=float(price)
        print line+" "+str(price)
    return binderlist,totalprice

def getSetOld(setname):
    binderlist = []
    totalprice = 0
    totalcards = raw_input("Enter the number of the last card in the set of "+setname+"\n")
    for i in range(0,int(totalcards)+1):
        if i<10:
            leadingz = "00"
        elif i<100:
            leadingz = "0"
        elif i<1000:
            leadingz = ""
        line = setname+"-"+leadingz+str(i)
        price = getBestPrice(line)
        #print r.text
        binderlist.append([line,price])
        totalprice+=float(price)
        print line+" "+str(price)
    return binderlist,totalprice

def getNameFromSet(cardID):
    #print "cardID.upper() is "+cardID.upper()
    q = requests.get("http://yugioh.wikia.com/api.php?action=parse&page="+cardID.upper()+"&format=xml")
    tree = ET.fromstring(q.text.encode('ascii', 'ignore'))
    #if tree.find("pl").text:
    try:
        return tree.find(".//pl").text
    except:
        return q.text
    #print q.text
    #else:
    #    price = tree.find(".//{http://www.ebay.com/marketplace/search/v1/services}convertedCurrentPrice").text

def getFiles(directory=""):
    for dirname, dirnames, filenames in os.walk(directory+'.'):
        # print path to all subdirectories first.
        for subdirname in dirnames:
            print os.path.join(dirname, subdirname)
            # print path to all filenames.
        for filename in filenames:
            print os.path.join(dirname, filename)
    
def saveListToFile(contents,f):
    d = os.path.dirname(f)
    if not os.path.exists(d) and d!="":
        os.makedirs(d)
    with open(f,'w') as p:
        pickle.dump(contents, p)

def compareNewToOld(newfile,oldfile):
    with open(newfile, 'r') as f:
        newprices = pickle.load(f)
    return compareFromOldFile(newprices,oldfile)

def compareFromOldFile(newprices,oldfile):
    with open(oldfile, 'r') as f:
        oldprices = pickle.load(f)
    return comparePrices(newprices,oldprices)
    
def comparePrices(newray,oldray):
    totalprices = 0
    listofdifs = []
    newprices = newray[0]
    oldprices = oldray[0]
    if len(newprices) == len(oldprices):
        for i in range(0,len(newprices)):
            dif = newprices[i][1] - oldprices[i][1]
            listofdifs.append([newprices[i][0],dif])
            totalprices+=dif
            #
            if(dif>0):
                printstring = "Now $" + str(dif) + "more. (From $"+str(oldprices[i][1])+" to $"+str(newprices[i][1])+")"
            else:
                printstring =  "Now $" + str(dif) + "less. (From $"+str(oldprices[i][1])+" to $"+str(newprices[i][1])+")"
            #if(withNames == true):
            printstring += getNameFromSet(newprices[i][0])
            print printstring
            #
        return listofdifs,totalprices
    else:
        print "not the same size"
        return
    
def sortList(pricelist):
    pricelist[0].sort(key=lambda price: price[1])

def printOut(output,withNames=False,trashThreshold = 0):
    priceandnames = output[0]
    totalprice=0
    if withNames:
        for item in priceandnames:
            if abs(item[1])>trashThreshold:
                print "$"+str(item[1]) + ": "+item[0]+" (" + getNameFromSet(item[0]) + ")"
                totalprice+=item[1]
    else:
        for item in priceandnames:
            if abs(item[1])>trashThreshold:
                print "$"+str(item[1]) + ": "+item[0]
                totalprice+=item[1]
    print "Total prices: $"+str(totalprice) or str(output[1])
    print str(output[1])

def formatDate():
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

if __name__ == "__main__":
    ltgy = getSet("LTGY")
    printOut(ltgy,True,False)
    saveListToFile(ltgy,"output//LTGYoutput"+formatDate()+".txt")
    #this = getFileInput("ebay")
    #printOut(this,True)
