#!/usr/bin/env python3
# Python3
#
#   Simple array class that dynamically saves temp files to disk to conserve memory
#

import logging
import pickle
from datetime import timedelta
from itertools import islice
from os import makedirs, remove
from os.path import exists
from shutil import rmtree
from time import time

startime = time()
logging.getLogger(__name__).addHandler(logging.NullHandler())
class Array():
    """1D Array class
    Dynamically saves temp files to disk to conserve memory"""

    def __init__(self, name="Array", cachedirectory=".cache/", a=None, maxitems=1):
        # How much data to keep in memory before dumping to disk
        self.maxitems = int(maxitems*1e6)
        self.fc = 0  # file counter
        self.uuid = id(self)
        self.name = name
        logging.debug("[largearray.Array] Instance %d %s created | %s" % (self.uuid, self.name, str(timedelta(seconds=time()-startime))))
        self.dir = cachedirectory + str(self.uuid) # make a unique subfolder (unique as long as the array exists)
        if exists(self.dir):
            rmtree(self.dir)
        makedirs(self.dir)
        logging.debug("[largearray.Array] Instance %d caches in %s with %d items per file" % (self.uuid, self.dir, self.maxitems))
        self.path = self.dir + "/temp%d.dat"  # Name of temp files
        self.hastrim = False
        self.a = []
        if a is not None:
            self.extend(a)

    def append(self, n):
        """Append n to the array.
        If size exceeds self.maxitems, dump to disk
        """
        if self.hastrim:
            raise Exception("ERROR: Class [array] methods append() and extend() cannot be called after method trim()")
        else:
            self.a.append(n)
            if len(self.a) >= self.maxitems:
                logging.debug("[largearray.Array] Instance %d dumps temp %d | %s" % (self.uuid, self.fc, str(timedelta(seconds=time()-startime))))
                with open(self.path % self.fc, 'wb') as pfile:
                    pickle.dump(self.a, pfile)  # Dump the data
                self.a = []
                self.fc += 1

    def trim(self):
        """If there are remaining values in the array stored in memory, dump them to disk (even if there is less than maxitems.
        NOTE: Only run this after all possible appends and extends have been done
        WARNING: This cannot be called more than once, and if this has been called, append() and extend() cannot be called again"""
        if len(self.a) > 0:
            if self.hastrim:
                raise Exception("ERROR: Class [array] method trim() can only be called once")
            else:
                self.hastrim = True
                self.trimlen = len(self.a)
                logging.debug("[largearray.Array] Instance %d trims temp %d | %s" % (self.uuid, self.fc, str(timedelta(seconds=time()-startime))))
                with open(self.path % self.fc, 'wb') as pfile:
                    pickle.dump(self.a, pfile)  # Dump the data
                self.a = []
                self.fc += 1

    def extend(self, values):
        """Convenience method to append multiple values"""
        for n in values:
            self.append(n)

    def __iter__(self):
        """Allows iterating over the values in the array.
        Loads the values from disk as necessary."""
        for fc in range(self.fc):
            logging.debug("[largearray.Array] Instance %d iterates temp %d | %s" % (self.uuid, fc, str(timedelta(seconds=time()-startime))))
            with open(self.path % fc, 'rb') as pfile:
                yield from pickle.load(pfile)
        yield from self.a

    def __repr__(self):
        """The values currently in memory"""
        s = "[..., " if self.fc else "["
        return s + ", ".join(map(str, self.a)) + "]"

    def __getitem__(self, index):
        """Get the item at index or the items in slice.
        Loads all dumps from disk until start of slice for the latter."""
        if isinstance(index, slice):
            return list(islice(self, index.start, index.stop, index.step))
        else:
            fc, i = divmod(index, self.maxitems)
            with open(self.path % fc, 'rb') as pfile:
                return pickle.load(pfile)[i]

    def __len__(self):
        """Length of the array (including values on disk)"""
        if self.hastrim:
            return (self.fc-1) * self.maxitems + self.trimlen
        return self.fc * self.maxitems + len(self.a)

    def __delattr__(self, item):
        """Calling" del <object name>.a
        will delete entire array"""
        if item == 'a':
            super().__delattr__('a')
            rmtree(self.dir)
            logging.debug("[largearray.Array] Instance %d deletes all array data | %s" % (self.uuid, str(timedelta(seconds=time()-startime))))
        else:
            super(Array, self).__delattr__(item)

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            l = list(islice(self, key.start, key.stop, key.step))
            for i in l:
                l[i].__setitem__(value)
                set()
        else:
            fc, i = divmod(key, self.maxitems)
            with open(self.path % fc, 'rb') as pfile:
                l = pickle.load(pfile)
                l[i] = value
            remove(self.path % fc)
            with open(self.path % fc, 'wb') as pfile:
                pickle.dump(l, pfile)

    def __delitem__(self, key):
        fc, i = divmod(key, self.maxitems)
        with open(self.path % fc, 'rb') as pfile:
            l = pickle.load(pfile)
            del l[i]
        remove(self.path % fc)
        with open(self.path % fc, 'wb') as pfile:
            pickle.dump(l, pfile)
