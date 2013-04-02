#!/usr/bin/env python
'''
Created on Mar 21, 2013

@author: Sumner Hearth
'''
import math
from optparse import OptionParser
debug = False #Will be command line argument
class Box():
    '''
    A box object to store possibilities and values
    '''
    def __init__(self):
        '''
        creates box object with all possible values
        '''
        self.value = None
        self.possibleValues = [1,2,3,4,5,6,7,8,9]
    def setValue(self, value):
        '''
        sets value of box and sets possibleValues to that of value
        '''
        self.value = value
        self.possibleValues = [value]
    def setPossibleValues(self, possibleValues):
        '''
        sets possible values of box
        '''
        self.possibleValues = possibleValues
    def getValue(self):
        '''
        returns value (even if none)
        '''
        return self.value
    def getPossibleValues(self):
        '''
        returns table of possible values
        '''
        return self.possibleValues
    
class SudokuGrid():
    def __init__(self, boxGrid, printAll = False):
        '''
        creates sudoku grid with table of values
        takes optional printall debugger (outdated I think)
        '''
        self.boxDict = {}
        y = -1
        # array of rows
        for k in boxGrid:
            y+=1
            x=-1
            for v in k:
                x+=1
                if v==None:
                    self.boxDict[(x,y)] = Box()
                else:
                    b = Box()
                    b.setValue(int(v))
                    self.boxDict[(x,y)] = b
        if printAll:
            for y in xrange(0,9):
                line = ""
                for x in xrange(0,9):
                    value = self.boxDict[(x,y)].getValue()
                    line+=str(value if value!=None else " ")+" "
                print(line)
    def get(self,x,y):
        '''
        returns value at location
        '''
        return self.boxDict[(x,y)]
    def getTable(self):
        '''
        returns table of values from boxDict
        '''
        sTable = []
        for y in xrange(0,9):
            sLine = []
            for x in xrange(0,9):
                sLine.append(self.get(x, y).getValue())
            sTable.append(sLine)
        return sTable

class Sudoku():
    def __init__(self, boxGrid):
        '''
        creates and adopts sudokuGrid with given table
        creates Sudoku object with grid
        '''
        self.boxgrid = SudokuGrid(boxGrid, True)
    
    def getTable(self):
        '''
        returns table from grid
        '''
        return self.boxgrid.getTable()
    
    def printTable(self):
        '''
        prints values from tables
        '''
        sTable = self.getTable()
        for y in xrange(0,9):
            line = ""
            for x in xrange(0,9):
                v = sTable[y][x]
                if v==None:
                    line+="  "
                else:
                    line+=str(v)+" "
            print(line)
    
    def getNumberFilled(self):
        '''
        counts total number of boxed with none "None" values
        '''
        i = 0
        for y in xrange(0,9):
            for x in xrange(0,9):
                if self.boxgrid.get(x, y).getValue()!=None:
                    i+=1
        return i
    
    def OnlyPossibility(self, targetBox, x, y):
        '''
        Checks row, column and region to see if there is only one possible number
        which can cooexist with the other values; else sets possible values.
        '''
        if targetBox.getValue()==None:
            poss = [1,2,3,4,5,6,7,8,9]
            # Going through rows and columns
            for x_val in xrange(0,9):
                if x_val!=x:
                    selBox = self.boxgrid.get(x_val, y)
                    if selBox.getValue() in poss:
                        poss.remove(selBox.getValue())
            for y_val in xrange(0,9):
                if y_val!=y:
                    selBox = self.boxgrid.get(x, y_val)
                    if selBox.getValue() in poss:
                        poss.remove(selBox.getValue())
            if (len(poss)==0): #If there are no possible values: die! There's a problem.
                if debug: print("Error 1: Box location: "+str(x)+","+str(y))
                self.printTable()
                assert() #temporary
            # Going through 3x3 boxes
            x_gridOffset = 3*int(math.floor(x/3.0)) # 0 for (0,1,2) ; 1 for (3,4,5) ; 2 for (6,7,8)
            y_gridOffset = 3*int(math.floor(y/3.0))
            for x_val in xrange(x_gridOffset,x_gridOffset+3):
                for y_val in xrange(y_gridOffset,y_gridOffset+3):
                    if x_val!=x and y_val!=y:
                        selBox = self.boxgrid.get(x_val,y_val)
                        if selBox.getValue() in poss:
                            poss.remove(selBox.getValue())
            if (len(poss)==0): #If there are no possible values: die! There's a problem.
                if debug: print("Error 2: Box location: "+str(x)+","+str(y))
                self.printTable()
                assert() # temporary
            elif (len(poss)==1):
                if debug: print("OnlyPossibility: ("+str(x)+","+str(y)+") set to "+str(poss[0])+" from "+str(targetBox.getPossibleValues()))
                targetBox.setValue(poss[0])
                return True
            else:
                targetBox.setPossibleValues(list(poss))
            return False
    
    def LastManStanding(self, targetBox, x, y):
        '''
        Checks to see if this is the only box in a row, column or region
        that can take a certain value, then sets that value
        '''
        poss = targetBox.getPossibleValues()
        if debug: print("Performing LastManStanding: "+str(x)+","+str(y))
        
        if debug: print("Column")
        #check column
        newPoss = list(poss)
        for y_val in xrange(0,9):
            if y_val!=y and len(newPoss)>=0 and self.boxgrid.get(x, y_val).getValue()==None:
                if debug: print("  Checking: ("+str(x)+","+str(y_val)+"):")
                if debug: print("    Before: "+str(newPoss))
                checkPoss = self.boxgrid.get(x, y_val).getPossibleValues()
                if debug: print("    Minus: "+str(checkPoss))
                for value in poss:
                    if (value in checkPoss) and (value in newPoss):
                        newPoss.remove(value)
                if debug: print("    After: "+str(newPoss))
        if len(newPoss)==1:
            if debug: print("LastManStanding_column: ("+str(x)+","+str(y)+") set to "+str(newPoss[0])+" from "+str(targetBox.getPossibleValues()))
            targetBox.setValue(newPoss[0])
            return True
        
        if debug: print("Row")
        #check row
        newPoss = list(poss)
        for x_val in xrange(0,9):
            if x_val!=x and len(newPoss)>=0 and self.boxgrid.get(x_val, y).getValue()==None:
                if debug: print("  Checking: ("+str(x_val)+","+str(y)+"):")
                if debug: print("    Before: "+str(newPoss))
                checkPoss = self.boxgrid.get(x_val, y).getPossibleValues()
                if debug: print("    Minus: "+str(checkPoss))
                for value in poss:
                    if (value in checkPoss) and (value in newPoss):
                        newPoss.remove(value)
                if debug: print("    After: "+str(newPoss))
        if len(newPoss)==1:
            if debug: print("LastManStanding_row: ("+str(x)+","+str(y)+") set to "+str(newPoss[0])+" from "+str(targetBox.getPossibleValues()))
            targetBox.setValue(newPoss[0])
            return True
        
        if debug: print("Region")
        #check region
        newPoss = list(poss)
        x_region_bounds = 3*int(math.floor(x/3.0))
        y_region_bounds = 3*int(math.floor(y/3.0))
        if debug: print("X_BOUNDS: "+str(x_region_bounds))
        if debug: print("Y_BOUNDS: "+str(y_region_bounds))
        for x_val in xrange(x_region_bounds, x_region_bounds+3):
            for y_val in xrange(y_region_bounds, y_region_bounds+3):
                if debug: print("Passing over ("+str(x_val)+","+str(y_val)+"):")
                if (len(newPoss)>=0) and (x_val!=x or y_val!=y) and (self.boxgrid.get(x_val, y_val).getValue()==None):
                    if debug: print("  Checking: ("+str(x_val)+","+str(y_val)+"):")
                    if debug: print("    Before: "+str(newPoss))
                    checkPoss = self.boxgrid.get(x_val, y_val).getPossibleValues()
                    if debug: print("    Minus: "+str(checkPoss))
                    for value in poss:
                        if (value in checkPoss) and (value in newPoss):
                            newPoss.remove(value)
                    if debug: print("    After: "+str(newPoss))
        if len(newPoss)==1:
            if debug: print("LastManStanding_region: ("+str(x)+","+str(y)+") set to "+str(newPoss[0])+" from "+str(targetBox.getPossibleValues()))
            targetBox.setValue(newPoss[0])
            return True
        return False
        
    def checkLoop(self):
        madeChanges = False
        # check each box, for that box check each row, column and 3x3 grid. Remove possibilities which interfere with those.
        for x in xrange(0,9):
            for y in xrange(0,9):
                targetBox = self.boxgrid.get(x, y)
                if targetBox.getValue()==None:
                    madeChanges = madeChanges or self.OnlyPossibility(targetBox, x, y)
                    if madeChanges: return True
        
        # Now doing second check, we look through all the possibilities, if there is a column, row or grid wherein
        # only one of the boxes can have a certain value, set that box to that value
        for x in xrange(0,9):
            for y in xrange(0,9):
                targetBox = self.boxgrid.get(x, y)
                if targetBox.getValue()==None:
                    madeChanges = madeChanges or self.LastManStanding(targetBox, x, y)
                    if madeChanges: return True
        # did it change anything?

        # TODO ---> add checks for in line possible exclusion stuff
        return madeChanges   
      
    def isFilled(self):
        for y in xrange(0,9):
            for x in xrange(0,9):
                if self.boxgrid.get(x, y).getValue()==None:
                    return False
        return True

def isnumber(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
    
def readSudokuFile(filename):
    sudokuTable = []
    sudokuFile = open(filename)
    for i in range(0,9):
        line = sudokuFile.readline()
        sudokuTableLine = [value for value in line.split(" ")]
        # Change all empty spaces and errors to None
        for n,i in enumerate(sudokuTableLine):
            if not isnumber(i):
                sudokuTableLine[n]=None
        sudokuTable.append(sudokuTableLine)
    return sudokuTable
    
def fileexists(filename):
    try:
        with open(filename):
            return True
    except IOError:
        return False

def main():
    print("Starting up")
    parser = OptionParser()
    parser.add_option("-f","--file", dest="filename", help="reads sudoku file", metavar="FILE")
    parser.add_option("-v","--verbose", action="store_true",dest="verbose", help="enables verbose (debug) mode")
    (options, args) = parser.parse_args()
    filename = ""
    if options.filename!=None:
        filename = options.filename
    elif len(args)==1:
        filename = args[0]
    else:
        print("Please enter sudoku file name:")
        filename = raw_input(">> ")
    debug = False if options.verbose==None else True
    if fileexists(filename):
        try:
            sTable = readSudokuFile(filename)
            print("Processing "+filename)
            s = Sudoku(sTable)
            pre = s.getNumberFilled()
            post = 0
            print("Solving...")
            
            while (not s.isFilled()):
                madeChanges = s.checkLoop()
                if debug: s.printTable()
                if not madeChanges:
                    print("We lose")
                    post = s.getNumberFilled()
                    print("We solved "+str(post-pre)+" boxes")
                    for y in xrange(0,9):
                        for x in range(0,9):
                            print("("+str(x)+","+str(y)+"): "+str(s.boxgrid.get(x, y).getPossibleValues()))
                    break
            
            print(" ")
            print("===== FINAL =====")
            s.printTable()
        except KeyError:
            print("There was an error processing the file")
            print("Please check to make sure this is a sudoku file")
    else:
        print("Error 404: File Not Found")

if __name__ == '__main__':
    main()
