from pathlib import Path
import os
import struct

ENCODING = "gb2312"
ENCRYPTION_KEY = 0x40 # this is still a bit unclear, but seems to be common for all executables
ERPT_ENTRY_SIZE = 508


def uint32_t(bytes):
    return int.from_bytes(bytes, byteorder='little')


def decode_filename(filename: bytes) -> str:
    pos = filename.find(b"\0")

    if pos >= 0:
        filename = filename[:pos]

    return filename.decode(ENCODING)


def extract_erpt(input, outdir: Path) -> None:
    count = uint32_t(input.read(4))
    print(count)

    for i in range(count):
        filename, size, offset = struct.unpack("<500sII", input.read(ERPT_ENTRY_SIZE))
        # file name is stored in a 500-byte field, padded with NUL bytes
        filename = decode_filename(filename)

        print('%s\t%d @ %08X' % (filename, size, offset))

        assert size < 50_000_000

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
