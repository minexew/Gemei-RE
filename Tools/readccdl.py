import argparse, io, os, sys
from enum import Enum
from pathlib import Path
import struct

class SectionType(Enum):
    CODE = 1
    MISC = 6
    RESOURCES = 7
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

    # sanity check
    assert num_imports < 1000

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

        print('\t\t%08X\t%08X\t%08X\t%s' % (unk2, unk3, store_at, name))

    input.seek(orig)

def save_symbol_table(input, offset, size, f):
    orig = input.tell()
    input.seek(offset)

    num_imports = uint32_t(input.read(4))
    input.read(12)

    # sanity check
    assert num_imports < 1000

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
parser.add_argument("--dump-erpt-to", type=Path,
        help="dump embedded resources into directory")
parser.add_argument("--dump-sections-to", type=Path,
        help='dump section blobs into directory')
parser.add_argument("--save-exports", type=Path,
        help="specify a file name to save exported functions in Ghidra format")
parser.add_argument("--save-imports", type=Path,
        help="specify a file name to save imported functions in Ghidra format")
args = parser.parse_args()

with open(args.input_file, "rb") as input:
    sign = input.read(4).decode()   # CCDL
    version = uint32_t(input.read(4))  # 00010000
    unk2 = uint32_t(input.read(4))  # 00020001
    num_sections = uint32_t(input.read(4))

    unk5, unk6, unk7, unk8 = struct.unpack("<IIII", input.read(16))

    print('%s\tversion=%08X\t%08X\tnum_sections=%d\t%08X\t%08X\t%08X\t%08X' %
            (sign, version, unk2, num_sections, unk5, unk6, unk7, unk8))
    print()

    for i in range(num_sections):
        # ERPT is an embedded filesystem
        # EXPT is import table
        # ICON is uint32_t w, h + raw RGBA data
        # IMPT is import table
        # RAWD is machine code

        name, type_, offset, size = struct.unpack("<4sIII", input.read(16))

        name = name.decode()
        type_ = SectionType(type_)

        print(f'Section "{name}" type={SectionType(type_)} offset={offset:08X}h size={size:08X}h')

        if type_ == SectionType.CODE:
            unk1, entry_point, load_address, alloc_size = struct.unpack("<IIII", input.read(16))
            print(f"\tunk1={unk1:08X}h entry_point={entry_point:08X}h load_address={load_address:08X}h "
                  f"alloc_size={alloc_size:08X}h")
        else:
            unk1, unk2, unk3, unk4 = struct.unpack("<IIII", input.read(16))
            print(f"\tunk1={unk1:08X}h unk2={unk2:08X}h unk3={unk3:08X}h unk4={unk4:08X}h")

        if args.dump_sections_to is not None:
            dump(input, args.dump_sections_to / name, offset, size)

        if type_ == SectionType.RESOURCES and args.dump_erpt_to is not None:
            from erpt import extract_erpt

            orig = input.tell()
            input.seek(offset)
            section_bytes = input.read(size)
            input.seek(orig)

            assert len(section_bytes) == size
            section_io = io.BytesIO(section_bytes)
            extract_erpt(section_io, args.dump_erpt_to)

        if type_ == SectionType.IMPORT:
            print("\tImport table:")
            dump_import_export_table(input, offset, size)

            if args.save_imports is not None:
                with open(args.save_imports, "wt") as f:
                    save_symbol_table(input, offset, size, f)

        if type_ == SectionType.EXPORT:
            print("\tExport table:")
            dump_import_export_table(input, offset, size)

            if args.save_exports is not None:
                with open(args.save_exports, "wt") as f:
                    save_symbol_table(input, offset, size, f)

        print()
