import argparse, sys

parser = argparse.ArgumentParser(description="Encrypt/decrypt configuration files")
parser.add_argument('input_file',
        help='input file')
parser.add_argument('-o', dest='output_file', required=True,
        help='output file')
args = parser.parse_args()

pattern = b'HXFCC1600V10'

with open(args.input_file, 'rb') as input, open(args.output_file, 'wb') as output:
    while True:
        bytes = input.read(len(pattern))

        if not bytes:
            return

        for i, b in enumerate(bytes):
            b ^= pattern[i]

            if b == 0:
                return

            output.write(bytearray([b]))
