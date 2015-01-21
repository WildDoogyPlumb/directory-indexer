
import fnmatch
import shutil

import os, time,datetime, sys
import sqlite3

import gc
gc.disable()



class Directory(object):
    def __init__(self, path, timeUpdated, DirDict):
        self.path = path
        self.files = []
        self.directories = []
        self.dirClasses = {}
        self.timeUpdated = timeUpdated
        self.DirectoryDictionary = DirDict
        self.root = self.path
        self.scanned = 0
        if "\\" in self.path:
            self.root = self.path[:self.path.rfind("\\")]
            tmp_root = self.root
            paths = []
            while "\\" in tmp_root:
                if tmp_root not in DirDict:
                    paths.append(tmp_root)
                    tmp_root = tmp_root[:tmp_root.rfind("\\")]
                else:
                    break
            for i in paths:
                DirDict[i] = Directory(i,self.timeUpdated,DirDict)
            if self.root in DirDict:
                DirDict[self.root].dirClasses[self.path] = self # linking
            else:
                print "Assuming", self.root, "to be the global root"
        else:
            print "Assuming", self.root, "to be the global root because there are no slashes"

    def printFiles(self):
        if self.scanned == 0:
            self.update()
        for i in self.files:
            print self.path+"\\"+i
        for i in self.dirClasses:
            self.dirClasses[i].printFiles()

    def writeFiles(self, mfile):
        if self.scanned == 0:
            self.update()
        self.files.sort()
        for i in self.files:
            mfile.write("\""+self.path+"\",\""+i+"\"\n")
        sortedKeys = self.dirClasses.keys()
        sortedKeys.sort()
        for i in sortedKeys:
            self.dirClasses[i].writeFiles(mfile)

    def markLower(self):
        for i in self.dirClasses:
            self.dirClasses[i].markLower()
        self.scanned = 1

    def delLower(self):
        # for i in self.dirClasses:
        #    self.dirClasses[i].delLower()
        self.dirClasses = {}
        # del self.DirectoryDictionary[self.path]

    def update(self):
        if os.path.isdir(self.path):
            if datetime.datetime.fromtimestamp(os.path.getmtime(self.path)) > self.timeUpdated:
                # Needs an update
                print "Updating",self.path
                (pathS, directoriesS , filesS) = (0,0,0)
                for (pathS, directoriesS, filesS) in os.walk(self.path):
                    break
                if filesS:
                    self.files = filesS
                if directoriesS:
                    self.directories = directoriesS
                for folder in self.directories:
                    fullfolder = os.path.join(self.path, folder)
                    if fullfolder not in self.dirClasses:
                        tmpDir = Directory(fullfolder, datetime.datetime(1900, 1, 1), self.DirectoryDictionary)
                        self.DirectoryDictionary[fullfolder] = tmpDir
                        self.dirClasses[fullfolder] = tmpDir
                for i in self.dirClasses:
                    self.dirClasses[i].update()
            else:
                print "Path is all up to date:", self.path
                self.markLower()
        else:
            print "Detected deleted path:", self.path
            self.delLower()
        self.scanned = 1
        self.timeUpdated = datetime.date.fromtimestamp(time.time())


def importOldScan(oldScanFile,tmpDirectoryDictionary):
    import csv
    print "Attempting to import old Database"
    try:
        with open(oldScanFile, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar="\"")
            daterow = spamreader.next()
            timeUpdated = date_object = datetime.datetime(int(daterow[1]), int(daterow[2]), int(daterow[3]))
            for row in spamreader:
                if spamreader.line_num%10000 == 0:
                    print "reading line:", spamreader.line_num
                path = row[0].strip("\"")
                mfile = row[1].strip("\"")
                if path not in tmpDirectoryDictionary:
                    tmpDirectoryDictionary[path] = Directory(path, timeUpdated, tmpDirectoryDictionary)
                    tmpDirectoryDictionary[path].files.append(mfile)
                else:
                    tmpDirectoryDictionary[path].files.append(mfile)
    except IOError:
        print "Could not read existing database. Scanning from scratch."
        print oldScanFile



