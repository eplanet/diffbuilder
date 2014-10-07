import os, hashlib


class DiffBuilder :
    def __init__(self, iReference, iCompare, iOutput, iScriptFile) :
        self.ref = iReference
        self.cmp = iCompare
        self.out = iOutput
        self.spt = iScriptFile

    def md5sum(self, iFilepath):
        hasher = hashlib.md5()
        with open(iFilepath, 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        return hasher.hexdigest()

    def generateDiff(self):
        self.scriptFile = open(self.spt, "w")
        self.recursiveLeftCompare("")
        self.recursiveRightCompare("")
        self.scriptFile.close()

    def recursiveLeftCompare(self, iCurrentPath):
        curRefDir = os.path.join(self.ref, iCurrentPath)
        curCmpDir = os.path.join(self.cmp, iCurrentPath)
        for p in os.listdir(curRefDir):
            curRefFile = os.path.join(curRefDir, p)
            if os.path.isdir(curRefFile):
                self.recursiveLeftCompare(os.path.join(iCurrentPath, p))
            else:
                curCmpFile = os.path.join(curCmpDir, p)
                refmd5 = self.md5sum(curRefFile)
                if not os.path.exists(curCmpFile):
                    # Dans ce cas on supprime dans le script cible
                    self.scriptFile.write("rm %s\n" % (os.path.join(iCurrentPath, p)))
                else:
                    cmpmd5 = self.md5sum(curCmpFile)
                    if refmd5 != cmpmd5 :
                        # On garde celui de droite, considéré comme le plus récent
                        curOutDir = os.path.join(self.out, iCurrentPath)
                        curOutFile = os.path.join(curOutDir, p)
                        if not os.path.exists(curOutDir):
                            os.makedirs(curOutDir)
                        os.link(curCmpFile, curOutFile)

    def recursiveRightCompare(self, iCurrentPath):
        curRefDir = os.path.join(self.ref, iCurrentPath)
        curCmpDir = os.path.join(self.cmp, iCurrentPath)
        for p in os.listdir(curCmpDir):
            curRefFile = os.path.join(curRefDir, p)
            if os.path.isdir(curRefFile):
                self.recursiveRightCompare(os.path.join(iCurrentPath, p))
            else:
                curCmpFile = os.path.join(curCmpDir, p)
                if not os.path.exists(curRefFile) :
                    # Il s'agit d'un nouveau fichier
                    curOutDir = os.path.join(self.out, iCurrentPath)
                    curOutFile = os.path.join(curOutDir, p)
                    if not os.path.exists(curOutDir):
                        os.mkdir(curOutDir)
                    os.link(curCmpFile, curOutFile)
