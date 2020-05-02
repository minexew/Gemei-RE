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

def dump_apis(input, offset):
    print('Dumping FW API Table...', file=sys.stderr)

    orig = input.tell()
    input.seek(offset)

    num_imports = 952
    for j in range(num_imports):
        func_address = uint32_t(input.read(4))
        name_offset = uint32_t(input.read(4))

        orig2 = input.tell()
        input.seek(name_offset - 0x10500000)
        name = read_sz(input)
        input.seek(orig2)

        # print('%08X\t(%08X in file)\t%s' % (func_address, func_address - 0x10500000, name))
        print(f"{name} {func_address:08X} f")

    input.seek(orig)

parser = argparse.ArgumentParser()
parser.add_argument('input_file',
        help='input file (ccpmp.bin)')
args = parser.parse_args()

with open(args.input_file, "rb") as input:
    # 1053AE04 LDR R8, =off_106397CC
    dump_apis(input, 0x1397CC)
