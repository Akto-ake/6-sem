import unittest
import prog

class TestSome(unittest.TestCase):
    
    def test_normal(self):
        """Norm div"""
        self.assertEqual(prog.func(1, 2), 1.5)
        self.assertEqual(prog.func(1, 3),(1 /9) * 12)
        
    def test_exception(self):
        with self.assertRaises(ZeroDivisionError):
            prog.func(1, 0)
    
    def test_untype(self):
        with self.assertRaises(TypeError):
            prog.func(1, 'ss')     
            