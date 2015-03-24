from komprese import RLECompressor, RLEC2ompressor, LZ77Compressor
import unittest

class TestRLE(unittest.TestCase):
    def setUp(self):
        self.comp = RLECompressor()

    def enc_dec(self, data):
        self.assertEqual(data, self.comp.decode(self.comp.encode(data)))
        # print(data)
        # print(self.comp.decode(self.comp.encode(data)))

    def test_empty(self):
        self.enc_dec(b"")

    def test_0_ff(self):
        self.enc_dec(bytes(range(256)))

    def test_100a(self):
        self.enc_dec(100*b"A")

    def test_aabbbcd(self):
        self.enc_dec(b"aabbbcd")


class TestRLE2(TestRLE):
    def setUp(self):
        self.comp = RLEC2ompressor()


class TestLZ77(TestRLE):
    def setUp(self):
        self.comp = LZ77Compressor()

    def test_search_prefix(self):
        self.assertEqual(self.comp.search_prefix("ahoj", "hojahoj", 0, 7), (3, 4))
        self.assertEqual(self.comp.search_prefix("ahoj", "hojahoj", 0, 3), (0, 0))
        self.assertEqual(self.comp.search_prefix("ahoj", "hojahoj", 3, 7), (3, 4))


if __name__ == '__main__':
    unittest.main()
