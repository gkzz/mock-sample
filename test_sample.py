
import unittest
from mock import patch, MagicMock
from sample import Sample

class TestSample(unittest.TestCase):
    def setUp(self):
        self.obj = Sample()
    
    def tearDown(self):
        self.obj = None
        self.number = None

    def test00_no_mock(self):
        self.number = self.obj.main()
        self.assertEqual(self.number, 2)


    @patch('sample.Sample.challenge')
    def test01_mock_ok(self, chal):
        def _challenge(_conts):
            if _conts % 2 == 0:
                return True
            else:
                return False
        
        chal.side_effect = _challenge

        self.number = self.obj.main()
        self.assertEqual(self.number, 2)
        self.assertNotEqual(self.number, 4)
        self.assertEqual(chal.call_count, 2)

    @patch('sample.Sample.challenge')
    def test11_mock_ng(self, chal):
        def _challenge(_conts):
            if _conts % 2 == 0:
                if chal.call_count == 2:
                    return False
                else:
                    return True
            else:
                return False
        
        chal.side_effect = _challenge

        self.number = self.obj.main()
        self.assertNotEqual(self.number, 2)
        self.assertEqual(self.number, 4)
        self.assertEqual(chal.call_count, 4)




