
#"C:\Users\boh01\Downloads"

import fnmatch

import os, time,datetime



class Directory(object):
    def __init__(self, path,timeUpdated,DirDict):
        self.path = path
        self.files = []
        self.directories = []
        self.dirClasses = {}
        self.timeUpdated = timeUpdated
        self.DirectoryDictionary = DirDict
        self.root = self.path
        self.scanned = 0
        if self.path.rfind("\\") > 0:
            self.root = self.path[:self.path.rfind("\\")]
            tmp = self.root.split("\\")
            paths = []
            for i in range(len(tmp)):
                dpath = tmp[0]
                for j in range(1,i+1):
                    dpath += "\\"+tmp[j]
                paths.append(dpath)
            for i in paths:
                if not i in  self.DirectoryDictionary.keys():
                    self.DirectoryDictionary[i] = Directory(i,self.timeUpdated,self.DirectoryDictionary)
            try:
                self.DirectoryDictionary[self.root].dirClasses[self.path] = self # linking
            except KeyError:
                print "Assuming",self.root,"to be the global root"
        else:
            print "Assuming",self.root,"to be the global root because there are no slashes"
    def printFiles(self):
        if self.scanned == 0:
            self.update()
        for i in self.files:
            print self.path+"\\"+i
    def writeFiles(self,file):
        if self.scanned == 0:
            self.update()
        for i in self.files:
            file.write(self.path+","+i+"\n")
    def markLower(self):
        for i in self.dirClasses:
            self.dirClasses[i].markLower()
        self.scanned = 1
    def delLower(self):
        #for i in self.dirClasses:
        #    self.dirClasses[i].delLower()
        self.dirClasses = {}
        #del self.DirectoryDictionary[self.path]

    def update(self):
        if os.path.isdir(self.path):
            if datetime.datetime.fromtimestamp(os.path.getmtime(self.path)) > self.timeUpdated:
                #Needs an update
                print "Updating",self.path
                (pathS, directoriesS , filesS) = (0,0,0)
                for (pathS, directoriesS , filesS) in os.walk(self.path):
                    break
                if filesS:
                    self.files = filesS
                if directoriesS:
                    self.directories = directoriesS
                for folder in self.directories:
                    fullfolder = self.path+"\\"+folder
                    if not fullfolder in self.dirClasses.keys():
                        tmpDir = Directory(fullfolder,datetime.datetime(1900,1,1),self.DirectoryDictionary)
                        self.DirectoryDictionary[fullfolder] = tmpDir
                        self.dirClasses[fullfolder] = tmpDir
                for i in self.dirClasses:
                    self.dirClasses[i].update()
            else:
                print "Path is all up to  date:", self.path
                self.markLower()
        else:
            print "Detected deleted path:", self.path
            self.delLower()
        self.scanned = 1
        self.timeUpdated = datetime.date.fromtimestamp(time.time())


rootDIR = "C:\\Projects"

DirectoryDictionary = {}
DirectoryDictionary[rootDIR] = Directory(rootDIR,datetime.datetime(1990,1,1),DirectoryDictionary)


pathToCSV = "H:\\Projects\\Monster\\DB_2.csv"

import csv
"""
with open(pathToCSV , 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar="'")
    daterow = spamreader.next()
    timeUpdated = date_object = datetime.datetime(int(daterow[1]),int(daterow[2]),int(daterow[3]))
    for row in spamreader:
        if spamreader.line_num%1000 == 0:
            print spamreader.line_num
        try:
            path = row[0]
            file = row[1]
            if path in DirectoryDictionary:
                DirectoryDictionary[path].files.append(file)
            else:
                DirectoryDictionary[path] = Directory(path,timeUpdated,DirectoryDictionary)
        except:
            print "Here",Exception
"""

DirectoryDictionary[rootDIR].update()


raw_input("All done")
