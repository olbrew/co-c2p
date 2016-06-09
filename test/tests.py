import unittest
from c2p.C2P import run


class TestVariables(unittest.TestCase):

    def test_scope(self):
        self.assertEqual(run('c/var.c', 'output.p'), "Semantic Error: 2: 0\
                         redifinition of 'i'")


class TestFunctions(unittest.TestCase):

    def test_declarations(self):
        pass

    def test_calling(self):
        pass

if __name__ == '__main__':
    unittest.main()
