# from memory_profiler import profile
import os
import time
import signal
import subprocess
import random
import string

import scandir as sd


def log(*args):
    print "[Test]",
    print time.strftime("%c"),
    print " ",
    for arg in args:
        print arg,
    print ""


def main():
    def scan_dir(a=0):
        path = "O:\\Technical_Support\\Applications_Engineering\\Customer Archives"

        def scan(directory):
            for (pathS, directoriesS, filesS) in sd.walk(directory):
                for d in directoriesS:
                    scan(d)

        t = time.time()
        scan(path)
        return time.time() - t

    for i in range(0, 25, 5):
        children = []
        for x in range(i):
            children.append(subprocess.Popen("python Node.py").pid)
        print i, scan_dir()
        for c in children:
            if c:
                try:
                    os.kill(c, signal.SIGTERM)
                except:
                    pass


def main2():
    from multiprocessing.dummy import Pool as ThreadPool
    from threading import Lock
    import Queue

    import Directory
    import DirectoryDB

    def create_FindIt_folder():
        import sys

        if sys.platform == "win32":
            appdata = os.getenv('APPDATA')
            FindIt = os.path.join(appdata, "FindIt")
            if not os.path.isdir(FindIt):
                os.mkdir(FindIt)
            if os.path.isdir(FindIt):
                return FindIt
            else:
                return False
        elif sys.platform == "linux2":
            home = os.getenv('HOME')
            FindIt = os.path.join(home, "FindIt")
            if not os.path.isdir(FindIt):
                os.mkdir(FindIt)
            if os.path.isdir(FindIt):
                return FindIt
            else:
                return False
        else:
            print "Crashing. Not made to run on mac"

    def init_database():
        FindIt = create_FindIt_folder()
        if not FindIt:
            print "Could not create the FindIt directory. Will now crash."
            quit()
        database_filename = os.path.join(FindIt, "test.db")
        # self.backup_db(database_filename)
        directory_database = DirectoryDB.DirectoryDB(database_filename)
        directory_database.start()
        return directory_database

    def linux_path(path):
        if ":" in path:
            drive = path[0]
            path = "/media/" + drive.upper() + path[2:]
            path = path.replace("\\", "/")
        return path

    import sys
    for times in range(10):

        directory_database = init_database()
        directory_dictionary = {}
        number_of_threads = 16
        update_pool = ThreadPool(number_of_threads)
        update_pool.thread_count = 0
        update_pool.thread_lock = Lock()
        update_pool.messages = Queue.Queue()

        path = "O:\\Technical_Support\\Applications_Engineering"
        if sys.platform == "linux2":
            path = linux_path(path)
        log("Scanning:", path)
        t = time.time()

        if path not in directory_dictionary:
            directory_dictionary[path] = Directory.Directory(path, 0.0,
                                                             directory_dictionary)  # Create Root and reset time.
        update_pool.apply_async(directory_dictionary[path].update,
                                args=(update_pool, directory_database,))  # Go. Scan. Be Free.
        time.sleep(.1)
        while update_pool.thread_count > 0:
            time.sleep(.001)

        update_pool.close()
        update_pool.join()
        log("Time to scan directory:", time.time() - t)
        paths = directory_database.dump_paths()
        if sys.platform == "linux2":
            lpaths = []
            for path, t in paths:
                lpaths.append((linux_path(path), t))
            paths = lpaths
        t = time.time()
        for path, scan_time in paths:
            if os.path.getmtime(path) > scan_time:
                print path
        tt = time.time() - t
        log("Time to scan all", len(paths), "folders:", tt, "(", len(paths) / tt, "Folder/ second)")

        def get_date(path, scan_time):
            return os.path.getmtime(path) > scan_time

        from multiprocessing.pool import ThreadPool as Pool

        pool = Pool(100)
        t = time.time()
        pool.map(lambda (path, scan_time): os.path.getmtime(path) > scan_time, paths)  # This is very fast.
        tt = time.time() - t
        log("Time to scan all folders:", tt, "(", len(paths) / tt, "Folder/ second)")


def main3():
    t = time.time()
    a = range(10000000)
    delta = time.time() - t
    print delta
    t = time.time()
    a += range(10000000)
    delta = time.time() - t
    print delta
    t = time.time()
    a += range(10000000)
    delta = time.time() - t
    print delta
    t = time.time()
    for i in a:
        i = len(a)
    delta = time.time() - t
    print delta
    t = time.time()
    while len(a):
        asdf = a.pop()
    delta = time.time() - t
    print delta


def random_string(len):
    tmp = ""
    for i in range(len):
        tmp += random.choice(string.ascii_letters)
    return tmp


def main4():
    strings = []
    t = time.time()
    for i in range(10000):
        strings.append(random_string(100))
    log("Created in", time.time() - t)
    t = time.time()
    for i in range(1000000):
        strings.append(strings[int(random.random() * len(strings))])
    log("Mishmashed", time.time() - t)
    tmpdict = {}
    t = time.time()
    for s in strings:
        tmpdict[s] = 0
    log("hashed in ", time.time() - t)
    t = time.time()
    for s in strings:
        if s not in tmpdict:
            tmpdict[s] = s
    log("hashed in ", time.time() - t)


class foo():
    def __init__(self):
        self.a = 1
        self.b = 1
        self.aa = 1
        self.ad = 1
        self.af = 1


if __name__ == "__main__":
    asdf = foo()
    att = [a for a in dir(asdf) if not a.startswith('__')]
    log(att)
    log(getattr(asdf, att[0]))
    exit()
