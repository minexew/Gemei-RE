import argparse, os, sys
from enum import Enum
from pathlib import Path
import struct

class SectionType(Enum):
    CODE = 1
    MISC = 6
    FILESYSTEM = 7
    IMPORT = 8
    EXPORT = 9
    UNKNOWN1 = 10       # TODO: seen in the wild?
    UNKNOWN2 = 11       # TODO: AES-encrypted code? seen in the wild?

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

def dump(input, name, offset, size):
    with open(name, 'wb') as output:
        orig = input.tell()
        input.seek(offset)
        data = input.read(size)
        output.write(data)
        input.seek(orig)

def dump_import_export_table(input, offset, size):
    orig = input.tell()
    input.seek(offset)

    num_imports = uint32_t(input.read(4))
    input.read(12)

    tail = input.tell() + num_imports * 16

    for j in range(num_imports):
        name_offset = uint32_t(input.read(4))
        unk2 = uint32_t(input.read(4))      # usually 0
        unk3 = uint32_t(input.read(4))      # usually 00020000
        store_at = uint32_t(input.read(4))

        orig2 = input.tell()
        input.seek(tail + name_offset)
        name = read_sz(input)
        input.seek(orig2)

        print('%08X\t%08X\t%08X\t%s' % (unk2, unk3, store_at, name))

    input.seek(orig)

def save_export_table(input, offset, size, f):
    orig = input.tell()
    input.seek(offset)

    num_imports = uint32_t(input.read(4))
    input.read(12)

    tail = input.tell() + num_imports * 16

    for j in range(num_imports):
        name_offset = uint32_t(input.read(4))
        unk2 = uint32_t(input.read(4))
        unk3 = uint32_t(input.read(4))
        address = uint32_t(input.read(4))

        orig2 = input.tell()
        input.seek(tail + name_offset)
        name = read_sz(input)
        input.seek(orig2)

        print(f"{name} {address:08X} f", file=f)

    input.seek(orig)

parser = argparse.ArgumentParser(description="Analyze/dump CCDL executables")
parser.add_argument('input_file',
        help='input file')
parser.add_argument('-d', dest='dump', action='store_true',
        help='dump sections')
parser.add_argument("--save-exports", type=Path,
        help="specify a file name to save exports in Ghidra format")
args = parser.parse_args()

with open(args.input_file, "rb") as input:
    sign = input.read(4).decode()   # CCDL
    version = uint32_t(input.read(4))  # 00010000
    unk2 = uint32_t(input.read(4))  # 00020001
    num_sections = uint32_t(input.read(4))
    unk3 = uint32_t(input.read(4))
    unk4 = uint32_t(input.read(4))
    unk5 = uint32_t(input.read(4))
    unk6 = uint32_t(input.read(4))

    print('%s\t%08X\t%08X\t%08X\t%08X\t%08X\t%08X' %
            (sign, version, unk2, unk3, unk4, unk5, unk6))

    for i in range(num_sections):
        name = input.read(4).decode()
        type_ = uint32_t(input.read(4))
        offset = uint32_t(input.read(4))
        size = uint32_t(input.read(4))
        unk3 = uint32_t(input.read(4))      # usually 0. indicates special handling in dl_open
        unk4 = uint32_t(input.read(4))      # for RAWD, entry point
        unk5 = uint32_t(input.read(4))      # for RAWD, load address
        unk6 = uint32_t(input.read(4))      # wtf ???

        # ERPT is an embedded filesystem
        # EXPT is import table
        # ICON is uint32_t w, h + raw RGBA data
        # IMPT is import table
        # RAWD is machine code

        print(f'Section "%s"\ttype={SectionType(type_)}\toffset=%08X\tsize=%08X\tunk3=%08X\tunk4=%08X\tunk5=%08X\tunk6=%08X' %
                (name, offset, size, unk3, unk4, unk5, unk6))

        if args.dump:
            dump(input, name, offset, size)

        if name == 'IMPT':
            print('Dumping Import Table...', file=sys.stderr)
            dump_import_export_table(input, offset, size)

        if name == 'EXPT':
            print('Dumping Export Table...', file=sys.stderr)
            dump_import_export_table(input, offset, size)

            if args.save_exports is not None:
                with open(args.save_exports) as f:
                    save_export_table(input, offset, size, f)
