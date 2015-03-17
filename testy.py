from komprese import rle_decode, rle_encode
import unittest

class TestRLE(unittest.TestCase):
    def enc_dec(self, data):
        self.assertEqual(data, rle_decode(rle_encode(data)))

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
