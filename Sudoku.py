#!usr/bin/env python
'''
Created on Mar 21, 2013

@author: Sumner Hearth
'''
import math
import sys

class Box():
    def __init__(self):
        self.value = None
        self.possibleValues = [1,2,3,4,5,6,7,8,9]
    def setValue(self, value):
        self.value = value
    def setPossibleValues(self, possibleValues):
        self.possibleValues = possibleValues
    def getValue(self):
        return self.value
    def getPossibleValues(self):
        return self.possibleValues
    
class SudokuGrid():
    def __init__(self, boxGrid, printAll = False):
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
        return self.boxDict[(x,y)]
    def getTable(self):
        sTable = []
        for y in xrange(0,9):
            sLine = []
            for x in xrange(0,9):
                sLine.append(self.get(x, y).getValue())
            sTable.append(sLine)
        return sTable

class Sudoku():
    def __init__(self, boxGrid):
        self.boxgrid = SudokuGrid(boxGrid, True)
    
    def getTable(self):
        return self.boxgrid.getTable()
    
    def getNumberFilled(self):
        i = 0
        for y in xrange(0,9):
            for x in xrange(0,9):
                if self.boxgrid.get(x, y).getValue()!=None:
                    i+=1
        return i
    
    def checkLoop(self):
        madeChanges = False
        # check each box, for that box check each row, column and 3x3 grid. Remove possibilities which interfere with those.
        for x in xrange(0,9):
            for y in xrange(0,9):
                targetBox = self.boxgrid.get(x, y)
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
                        print("Error 1: Box location: "+str(x)+","+str(y))
                    # Going through 3x3 boxes
                    x_gridOffset = 3*int(math.floor(x/3.0)) # 0 for (0,1,2) ; 1 for (3,4,5) ; 2 for (6,7,8)
                    y_gridOffset = 3*int(math.floor(y/3.0))
                    for x_val in xrange(x_gridOffset,x_gridOffset+3):
                        for y_val in xrange(y_gridOffset,y_gridOffset+3):
                            if x_val!=x and y_val!=y:
                                selBox = self.boxgrid.get(x_val,y_val)
                                if selBox.getValue() in poss:
                                    poss.remove(selBox.getValue())
                   
                    if (len(poss)<=0): #If there are no possible values: die! There's a problem.
                        print("Error 2: Box location: "+str(x)+","+str(y))
                    if len(poss)==1:
                        targetBox.setValue(poss[0])
                        madeChanges = True
                    elif len(poss)>1:
                        targetBox.setPossibleValues(poss)
        # Now doing second check, we look through all the possibilities, if there is a column, row or grid wherein
        # only one of the boxes can have a certain value, set that box to that value
        for x in xrange(0,9):
            for y in xrange(0,9):
                targetBox = self.boxgrid.get(x, y)
                # remove intersection of poss and other from poss
                #check poss in column
                poss = targetBox.getPossibleValues()
                for y_val in xrange(0,9):
                    checkPoss = self.boxgrid.get(x, y_val).getPossibleValues()
                    poss = [val for val in poss if val not in checkPoss and y_val != y]
                if len(poss)==1:
                    targetBox.setValue(poss[0])
                    madeChanges = True
                    break
                #check poss in row
                poss = targetBox.getPossibleValues()    #You can't preserve poss
                for x_val in xrange(0,9):
                    checkPoss = self.boxgrid.get(x_val, y).getPossibleValues()
                    poss = [val for val in poss if val not in checkPoss and x_val != x]
                if len(poss)==1:
                    targetBox.setValue(poss[0])
                    madeChanges = True
                    break
                #check poss in 3x3
                poss = targetBox.getPossibleValues()
                x_gridOffset = 3*int(math.floor(x/3.0))
                y_gridOffset = 3*int(math.floor(y/3.0))
                for x_val in xrange(x_gridOffset, x_gridOffset+3):
                    for y_val in xrange(y_gridOffset, y_gridOffset+3):
                        checkPoss = self.boxgrid.get(x_val, y_val).getPossibleValues()
                        poss = [val for val in poss if val not in checkPoss and x_val != x and y_val != y]
                if len(poss)==1:
                    targetBox.setValue(poss[0])
                    madeChanges = True
                    break
        
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
    filename = ""
    if len(sys.argv)<=1:
        print("Please enter sudoku file name:")
        filename = raw_input(">> ")
    else:
        filename = sys.argv[2]
    if fileexists(filename):
        sTable = readSudokuFile(filename)
        print("Processing "+filename)
        s = Sudoku(sTable)
        pre = s.getNumberFilled()
        post = 0
        print("Solving...")
        while (not s.isFilled()):
            if (not s.checkLoop()) and (not s.checkLoop()): #check it twice
                print("We lose")
                post = s.getNumberFilled()
                print("We solved "+str(post-pre)+" boxes")
                break
        sTable = s.getTable()
        for y in xrange(0,9):
            line = ""
            for x in xrange(0,9):
                v = sTable[y][x]
                if v==None:
                    line+="  "
                else:
                    line+=str(v)+" "
            print(line)
    else:
        print("Error 404: File Not Found")

if __name__ == '__main__':
    main()