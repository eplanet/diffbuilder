#Python 3.4

import unittest, os, random, shutil

from diffbuilder.diffbuilder import DiffBuilder

class TestDiffBuilder(unittest.TestCase):
    def setUp(self):
        rndTestDirPath = "%032x" % random.getrandbits(128)
        self.testDir = os.path.join("/tmp", rndTestDirPath)
        if os.path.exists(self.testDir) :
            shutil.rmtree(self.testDir)
        os.mkdir(self.testDir)
        ref = os.path.join(self.testDir, "reference")
        cmp = os.path.join(self.testDir, "compare")
        out = os.path.join(self.testDir, "output")
        os.mkdir(ref)
        os.mkdir(cmp)
        os.mkdir(out)
        script = os.path.join(self.testDir, "script.sh")
        self.db = DiffBuilder(ref, cmp, out, script)

    def tearDown(self) :
        if os.path.exists(self.testDir) :
            shutil.rmtree(self.testDir)

    def genFile(self, iDir, iFilename, iContent):
        f = open(os.path.join(iDir, iFilename), "w")
        f.write(iContent)
        f.close()

    def genRandomContentFile(self, iDir, iFilename):
        self.genFile(iDir, iFilename, "%032x" % random.getrandbits(128))

    def genIdenticalFiles(self, iDir1, iDir2, iFilename):
        self.genFile(iDir1, iFilename, "IDENTICAL CONTENT")
        self.genFile(iDir2, iFilename, "IDENTICAL CONTENT")

    def genDifferentContentFiles(self, iDir1, iDir2, iFilename):
        self.genRandomContentFile(iDir1, iFilename)
        self.genRandomContentFile(iDir2, iFilename)


    def test_GenerateDiff(self):
        # Premier cas : les deux fichiers sont identiques dans les deux répertoires
        self.genIdenticalFiles(self.db.ref, self.db.cmp, "identiques")

        # Second cas : les deux fichiers ont le même nom mais sont différents
        self.genDifferentContentFiles(self.db.ref, self.db.cmp, "differents")

        # Troisième cas : le fichier est dans la référence mais pas dans le compare
        self.genRandomContentFile(self.db.ref, "onlyref")

        # Quatrième cas : le fichier est dans le compare mais pas dans la référence
        self.genRandomContentFile(self.db.cmp, "onlycmp")

        # On recopie tout ça dans un sous-répertoire pour être sûr que la récursion se passe bien
        shutil.copytree(self.db.ref, os.path.join(self.db.ref, "subdir"))
        shutil.copytree(self.db.cmp, os.path.join(self.db.cmp, "subdir"))

        # Et même qu'on le recopie encore dans le sous-répertoire pour être bien sûr
        shutil.copytree(os.path.join(self.db.ref, "subdir"), os.path.join(self.db.ref, "subdir", "anothersubdir"))
        shutil.copytree(os.path.join(self.db.cmp, "subdir"), os.path.join(self.db.cmp, "subdir", "anothersubdir"))

        self.db.generateDiff()

        # Vérifications
        self.assertTrue(os.path.exists(os.path.join(self.db.out, "differents")))
        self.assertTrue(os.path.exists(os.path.join(self.db.out, "onlycmp")))
        self.assertTrue(os.path.exists(os.path.join(self.db.out, "subdir")))
        self.assertTrue(os.path.exists(os.path.join(self.db.out, "subdir", "differents")))
        self.assertTrue(os.path.exists(os.path.join(self.db.out, "subdir", "onlycmp")))

        scriptFile = open(self.db.spt, 'r')
        scriptLines = [line.strip() for line in scriptFile]
        scriptFile.close()
        self.assertTrue("rm subdir/anothersubdir/onlyref" in scriptLines)
        self.assertTrue("rm subdir/onlyref" in scriptLines)
        self.assertTrue("rm onlyref" in scriptLines)

if __name__ == '__main__':
    unittest.main()