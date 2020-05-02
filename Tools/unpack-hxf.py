import argparse, os, sys
from pathlib import Path

def uint32_t(bytes):
    return int.from_bytes(bytes, byteorder='little')

parser = argparse.ArgumentParser()
parser.add_argument('input_file',
        help='input file')
parser.add_argument("-o", dest="outdir", type=Path,
        help="output directory")
args = parser.parse_args()

with open(args.input_file, "rb") as input:
    header = input.read(20)
    file_size = uint32_t(input.read(4))
    input.seek(64)

    assert header[:4] == b"WADF"

    print('Header: %s' % header.decode())

    while True:
        file_offset = input.tell()
        filename_length = uint32_t(input.read(4))

        # sanity check
        assert filename_length < 200

        if not filename_length:
            break

        filename = input.read(filename_length).decode("gb2312")
        assert input.read(1) == b" "
        file_size = uint32_t(input.read(4))

        print("%s\t\t[%u bytes @ %08x]" % (filename, file_size, file_offset))

        if args.outdir is not None:
            filename_out = args.outdir / filename
            dir = filename_out.parent
            os.makedirs(dir, exist_ok=True)

            with open(filename_out, 'wb') as output:
                data = input.read(file_size)
                output.write(data)
        else:
            input.seek(file_size, os.SEEK_CUR)
