import unittest
import mood.client.__main__ as client
from unittest.mock import MagicMock, patch, call


class TestClient(unittest.TestCase):
    def setUp(self):
        self.mocker = MagicMock()
        self.cmdline = client.CMD(sock=self.mocker)
        self.cmdline.prompt = ''

    def test_down(self):
        """Test down"""
        self.cmdline.do_down("")
        self.mocker.sendall.assert_called_with("move 0 1\n".encode())

    def test_left(self):
        """Test left"""
        self.cmdline.do_left("")
        self.mocker.sendall.assert_called_with("move -1 0\n".encode())

    def test_addmon1(self):
        """Test add dragon"""
        self.cmdline.do_addmon("dragon hp 1 coords 1 0 hello hi")
        self.mocker.sendall.assert_called_with("addmon dragon hp 1 coords 1 0 hello hi\n".encode())

    def test_addmon2(self):
        """Test add cow"""
        self.cmdline.do_addmon("cow hp 5 coords 9 9 hello hihihih")
        self.mocker.sendall.assert_called_with("addmon cow hp 5 coords 9 9 hello hihihih\n".encode())
 
    @patch('builtins.input', side_effect=[
        'addmon dragon coords 164 209 hello nothelllo hp -5',
        EOFError,
    ])
    def test_5(self, inp):
        """Test add with incorrect arguments"""
        with patch('builtins.print') as mock_print:
            with patch('mood.client.__main__.time.sleep', return_value=None):
                self.cmdline.cmdloop()
        mock_print.assert_any_call("Invalid arguments")
    
    def tearDown(self):
        self.mocker.reset_mock()


if __name__ == "__main__":
    unittest.main()