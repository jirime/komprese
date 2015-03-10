def rle_encode(data):
    output = bytearray()

    i = 0

    while i < len(data):
        pismenko = data[i]
        j = i + 1
        while j < len(data) and j-i < 255 and pismenko == data[j]:
            j += 1

        output.append(pismenko)
        output.append(j-i)

        i = j

    return bytes(output)

def rle_decode(data):
    output = bytearray()

    i = 0

    while i < len(data):
        pismenko = data[i]
        k = data[i+1]

        for _ in range(k):
            output.append(pismenko)

        i += 2

    return bytes(output)


if __name__ == "__main__":
    text = b"aabbbcd"
    enc = rle_encode(text)
    dec = rle_decode(enc)
    assert dec == text
