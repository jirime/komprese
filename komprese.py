class CompressorBase:
    """
    Base class (interface) for compression algorithms.
    Inherit from this class to implement compression methods.

    Example:

        class MyCompressor(CompressorBase):
            def encode(self, data):
                ...
            def decode(self, data):
                ...

        comp = MyCompressor()
        data = b"Hello, world"
        assert data == comp.decode(comp.encode(data))

    """
    def encode(self, data):
        """
        Compress data

        Arguments:
            data: input data (bytes object)

        Returns:
            compressed data (bytes)

        """
        raise NotImplementedError

    def decode(self, data):
        """
        Decompress data

        Arguments:
            data: input data compressed with encode() method (bytes)

        Returns:
            decompressed data (bytes)

        """
        raise NotImplementedError



class RLECompressor(CompressorBase):
    """
    Run-length Encoding compression

    See http://en.wikipedia.org/wiki/Run-length_encoding

    """
    def encode(self, data):
        output = bytearray()

        i = 0

        while i < len(data):
            pismenko = data[i]
            j = i + 1
            while j < len(data) and j-i < 255 and pismenko == data[j]:
                j += 1

            output.append(pismenko)#zapiseme prvni vyskyt pismenka
            output.append(j-i)#kolikrat tam bylo

            i = j

        return bytes(output)

    def decode(self, data):
        output = bytearray()

        i = 0

        while i < len(data):
            pismenko = data[i]
            k = data[i+1]

            for _ in range(k):
                output.append(pismenko)

            i += 2

        return bytes(output)


class RLEC2ompressor(CompressorBase):
    """
    Run-length Encoding compression with escape characters

    """
    ESCAPE_CHAR = 0xff

    def encode(self, data):
        output = bytearray()

        i = 0

        while i < len(data):
            pismenko = data[i]

            j = i + 1
            while j < len(data) and j-i < 255 and pismenko == data[j]:
                j += 1

            delka_runu = j-i

            if delka_runu > 2 or pismenko == self.ESCAPE_CHAR:
                output.append(self.ESCAPE_CHAR)
                output.append(delka_runu)
                output.append(pismenko)
            else:
                for _ in range(delka_runu):
                    output.append(pismenko)

            i = j

        return bytes(output)


    def decode(self, data):
        output = bytearray()

        i = 0

        while i < len(data):
            pismenko = data[i]

            if pismenko == self.ESCAPE_CHAR:
                k = data[i+1]
                pismenko = data[i+2]
                for _ in range(k):
                    output.append(pismenko)
                i += 3
            else:
                output.append(pismenko)
                i += 1

        return bytes(output)


class LZ77Compressor(CompressorBase):
    """Lempel-Zif 77 compression"""
    def search_prefix(word, data, i, j):
        """
        search data[i:j] for longest prefix of word
        returns k, l such that word[:l] == data[k:k+l]
        """
        k, l = i, 0

        for zacatek in range(i, j):
            delka = 0
            while delka < len(word) and zacatek+delka < j and data[zacatek+delka] == word[delka]:
                delka += 1

            if delka > l:
                k = zacatek
                l = delka

        return k, l

    def encode(self, data):
        output = bytearray()

        i = 0

        while i < len(data):
            k, l = self.search_prefix(data[i:], data, max(0, i-254), i)
            if l > 3:
                offset = i - k
                output.append(0xff)
                output.append(offset)
                output.append(l)
                i = i + l
            else:
                if data[i] == 0xff:
                    output.append(0xff)
                    output.append(0x00)
                else:
                    output.append(data[i])
                i = i + 1

        return bytes(output)

    def decode(self, data):
        output = bytearray()

        i = 0

        while i < len(data):
            if data[i] != 0xff:
                output.append(data[i])
                i = i + 1
            else:
                if data[i + 1] == 0:
                    output.append(data[i])
                    i = i + 2
                else:
                    offset = data[i + 1]
                    length = data[i + 2]
                    j = len(output) - offset
                    for k in range(length):
                        output.append(output[j + k])
                    i = i + 3

        return bytes(output)
