
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


    @patch('sample.Sample.challenge', return_value=2)
    def test01_mock_ok_return_value(self, chal):
        chal.return_value

        self.number = self.obj.main()
        self.assertEqual(self.number, 1)
        self.assertEqual(chal.call_count, 1)
    
    @patch('sample.Sample.challenge')
    def test02_mock_ok_return_value(self, chal):
        chal.return_value = 2

        self.number = self.obj.main()
        self.assertEqual(self.number, 1)
        self.assertEqual(chal.call_count, 1)



    @patch('sample.Sample.challenge')
    def test03_mock_ok(self, chal):
        def _challenge(_conts):
            if chal.call_count <= 3:
                return False
            elif chal.call_count == 4:
                return True
            else:
                raise Exception("no_more_challenges")
        
        chal.side_effect = _challenge

        self.number = self.obj.main()
        self.assertEqual(self.number, 4)
        self.assertNotEqual(self.number, 2)
        self.assertEqual(chal.call_count, 4)


    @patch('sample.Sample.challenge')
    def test04_mock_ok(self, chal):
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




