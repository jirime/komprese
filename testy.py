from komprese import RLECompressor
import unittest

class TestRLE(unittest.TestCase):
    def setUp(self):
        self.comp = RLECompressor()

    def enc_dec(self, data):
        self.assertEqual(data, self.comp.decode(self.comp.encode(data)))

    def test_empty(self):
        self.enc_dec(b"")

    def test_0_ff(self):
        self.enc_dec(bytes(range(256)))

    def test_100a(self):
        self.enc_dec(100*b"A")

    def test_aabbbcd(self):
        self.enc_dec(b"aabbbcd")

if __name__ == '__main__':
    unittest.main()
