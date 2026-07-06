from ROOT import TFile, TTree, TObject, TChain, TMath
from array import array
from time import time


class TreeMaker:
    def __init__(self, filename, treename, branches, append=False, expand=False):
        self._expand = expand
        self._append = append

        if self._expand or self._append:
            self._ofile = TFile(filename, 'update')
            self._otree = self._ofile.Get(treename)
            if not self._otree:
                self._otree = TTree(treename, treename)
        else:
            self._ofile = TFile(filename, 'recreate')
            self._otree = TTree(treename, treename)
        self._branch = {}
        for branch in branches:
            self.add(branch)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def add(self, branch):
        try:
            name = branch['name']
            try:
                type_name = branch['type']
            except KeyError:
                type_name = 'D'

            try:
                length = branch['length']
            except KeyError:
                length = 1
        except Exception:
            name = branch
            type_name = 'D'
            length = 1

        self._branch[name] = array(type_name.swapcase(), [0] * length)
        if length == 1:
            self._otree.Branch(name, self._branch[name], name + '/' + type_name)
        else:
            self._otree.Branch(name, self._branch[name], name + '[' + str(length) + ']/' + type_name)

    def close(self):
        if self._expand or self._append:
            self._ofile.Write('', TObject.kOverwrite)
        else:
            self._ofile.Write()
        self._ofile.Close()

    def set(self, branch, value):
        try:
            branch = self._branch[branch]
        except KeyError:
            print('No branch named', branch, 'exists')
            return
        try:
            for i in range(min(len(value), len(branch))):
                branch[i] = value[i]
        except TypeError:
            branch[0] = value

    def Fill(self, vars=None):
        vars = vars or {}
        for branch in vars:
            self.set(branch, vars[branch])
        if self._expand:
            for branch in self._branch:
                self._otree.GetBranch(branch).Fill()
        else:
            self._otree.Fill()

    def GetEntries(self):
        return self._otree.GetEntries()


class TreeWrapper:
    def __init__(self, file, name):
        self.shouldPrint = False
        self._branchOnAccess = False
        self._tree = TChain(name)
        self._functions = {}
        if isinstance(file, str):
            self.addFile(file)
        else:
            for f in file:
                self.addFile(f)
        self._cache = {}
        self._aliases = {}

    def addFile(self, file):
        self._tree.Add(file)

    def addFriend(self, friend):
        self._tree.AddFriend(friend)

    def removeFriend(self, friend):
        self._tree.RemoveFriend(friend)

    def getEntry(self):
        return self._currentEntry

    def entry(self, quiet=False, printfreq=1000, Nentries=None, branchonaccess=True, timeremaining=True, offset=0):
        self._branchOnAccess = branchonaccess
        if printfreq <= 0:
            printfreq = 1

        if Nentries is None or Nentries < 0 or Nentries > self._tree.GetEntries():
            Nentries = self._tree.GetEntries()
        if timeremaining:
            starttime = time()
        for i in range(offset, Nentries):
            if not self._branchOnAccess:
                self._tree.GetEntry(i)
            else:
                self._currentEntry = self._tree.LoadTree(i)

            if not quiet and i % int(printfreq) == 0:
                self.shouldPrint = True
                displaystr = 'Processing entry: ' + str(i) + ' ({:.2f}%)'.format(i * 100. / Nentries)
                if timeremaining and i > 0:
                    tr = (time() - starttime) / i * (Nentries - i)
                    timestr = ''
                    if tr > 86400:
                        days = int(tr / 86400)
                        timestr += ' ' + str(days) + ' days'
                        tr -= days * 86400
                    if tr > 3600:
                        hours = int(tr / 3600)
                        timestr += ' ' + str(hours) + ' hours'
                        tr -= hours * 3600
                    if tr > 60:
                        mins = int(tr / 60)
                        timestr += ' ' + str(mins) + ' min'
                        tr -= mins * 60
                    timestr += ' ' + str(int(tr)) + ' s'
                    displaystr += ' Remaining: ' + timestr
                print(displaystr)
            else:
                self.shouldPrint = False
            yield i
        if not quiet:
            try:
                print('Processed ', i + 1, 'entries')
            except Exception:
                print('No entries processed')

    def getFileStartLength(self, filename):
        for whichtree, chainfile in enumerate(self._tree.GetListOfFiles()):
            if chainfile.GetTitle() == filename:
                self._tree.GetEntries()
                start = self._tree.GetTreeOffset()[whichtree]
                try:
                    length = chainfile.GetEntries()
                except Exception:
                    length = None
                return (start, length)
        return None

    def GetEntries(self, selection=None):
        if not selection:
            return self._tree.GetEntries()
        return self._tree.GetEntries(selection)

    def GetMinimum(self, name):
        try:
            name = self._aliases[name]
        except Exception:
            pass
        return self._tree.GetMinimum(name)

    def GetMaximum(self, name):
        try:
            name = self._aliases[name]
        except Exception:
            pass
        return self._tree.GetMaximum(name)

    def tree(self):
        return self._tree

    def addAlias(self, new, old):
        self._aliases[new] = old

    def __getattr__(self, name):
        try:
            name = self._aliases[name]
        except Exception:
            pass

        if not self._branchOnAccess:
            return getattr(self._tree, name)
        try:
            branch = self._tree.GetBranch(name)
            if name not in self._cache:
                title = branch.GetTitle().split('/')
                type_name = title[1].swapcase().replace('o', 'b').replace('s', 'h').replace('S', 'H')
                try:
                    lengthvar = title[0].split('[')[1][:-1]
                except Exception:
                    lengthvar = None
                self._cache[name] = [None, -1, lengthvar, type_name]

            cache = self._cache[name]
            length = 0
            if cache[2]:
                length = getattr(self, cache[2])

            if cache[1] != self._currentEntry:
                if not cache[0] or (cache[2] and len(cache[0]) < length):
                    address = array(cache[3], (2 * length + 1) * [0])
                    cache[0] = address
                    self._tree.SetBranchAddress(name, address)
                branch.GetEntry(self._currentEntry)
                cache[1] = self._currentEntry

            if cache[2]:
                return cache[0][0:length]
            return cache[0][0]
        except Exception as exc:
            raise AttributeError("%r object has no attribute %r" % (self.__class__, name)) from exc

    def get(self, what):
        try:
            return getattr(self, what)
        except Exception:
            try:
                return self._functions[what](self)
            except Exception:
                func = ''
                word = ''
                for l in what:
                    if l in ' +-*/^()[]<>=&|!,':
                        if self.has(word):
                            func += 't.'
                        func += word + l
                        word = ''
                    else:
                        word += l

                if word:
                    if self.has(word):
                        func += 't.'
                    func += word
                func = func.replace('&&', ' and ').replace('||', ' or ').replace('!', ' not ').replace('^', '**').replace('::', '.').replace('Entry$', 't.getEntry()')
                self._functions[what] = eval('lambda t: ' + func)
                return self._functions[what](self)

    def has(self, what):
        try:
            what = self._aliases[what]
        except Exception:
            pass
        return self._tree.GetBranch(what) is not None

    def searchBranch(self, what):
        retlist = []
        for branch in self._tree.GetListOfBranches():
            if what in branch.GetName():
                retlist.append(branch.GetName())
        return retlist
