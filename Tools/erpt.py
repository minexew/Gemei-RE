from pathlib import Path
import os

ENCRYPTION_KEY = 0x40 # this is still a bit unclear, but seems to be common for all executables


def uint32_t(bytes):
    return int.from_bytes(bytes, byteorder='little')


def read_sz(input):
    s = ''

    while True:
        b = input.read(1)
        if not b or ord(b) == 0:
            break

        s += b.decode()

    return s


def extract_erpt(input, outdir: Path) -> None:
    count = uint32_t(input.read(4))

    for i in range(count):
        filename = read_sz(input)
        input.seek(508 - (len(filename) + 1 + 4 + 4), 1)

        size = uint32_t(input.read(4))
        offset = uint32_t(input.read(4))
        print('%s\t%d @ %08X' % (filename, size, offset))

        filename_out = os.path.join(outdir, filename.replace("\\", "/"))
        dir = os.path.dirname(filename_out)
        os.makedirs(dir, exist_ok=True)

        with open(filename_out, 'wb') as output:
            orig = input.tell()
            input.seek(offset)
            data = input.read(size)

            data_decrypted = bytes(a ^ ENCRYPTION_KEY for a in data)

            output.write(data_decrypted)
            input.seek(orig)
