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
