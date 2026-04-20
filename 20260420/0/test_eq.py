import unittest
import prog_root
import asyncio
import time

class TestSome(unittest.TestCase):
    
    def test_0_root(self):
        self.assertEqual(prog_root.sqroots("1 2 1"), "-1.0")

    def test_1_root(self):
        self.assertEqual(prog_root.sqroots("1 2 3"), "")

    def test_2_root(self):
        self.assertEqual(prog_root.sqroots("1 0 -1"), "-1.0 1.0")

    def test_ZeroDivisionError_root(self):
        with self.assertRaises(ZeroDivisionError):
            prog_root.sqroots("0 3 0")

    def test_ValueError_root(self):
        with self.assertRaises(ValueError):
            prog_root.sqroots("5")

# @classmethod
# class setUpClass():
#     cls.proc = multiprocessing.Process(target=sqr_srv.serve)
#     cls.proc.start()
#     time.sleep(1) 
    
#     def tearDown():
#         pass
    
#     def setUp():
#         pass
    
    