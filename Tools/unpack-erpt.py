
import argparse, os, sys

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

parser = argparse.ArgumentParser(description="Unpack embedded filesystem (ERPT)")
parser.add_argument('input_file',
        help='input file')
parser.add_argument('outdir',
        help='directory to dump into')
args = parser.parse_args()

with open(args.input_file, "rb") as input:
    count = uint32_t(input.read(4))

    for i in range(count):
        filename = read_sz(input)
        input.seek(508 - (len(filename) + 1 + 4 + 4), 1)

        size = uint32_t(input.read(4))
        offset = uint32_t(input.read(4))
        print('%s\t%d @ %08X' % (filename, size, offset))

        filename_out = os.path.join(args.outdir, filename)
        dir = os.path.dirname(filename_out)
        os.makedirs(dir, exist_ok=True)

        with open(filename_out, 'wb') as output:
            orig = input.tell()
            input.seek(offset)
            data = input.read(size)
            output.write(data)
            input.seek(orig)
