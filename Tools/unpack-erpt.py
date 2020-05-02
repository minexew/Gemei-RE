from pathlib import Path

from erpt import extract_erpt

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Unpack embedded filesystem (ERPT)")
    parser.add_argument('input_file', type=Path,
            help='input file')
    parser.add_argument('outdir', type=Path,
            help='directory to dump into')
    args = parser.parse_args()

    with open(args.input_file, "rb") as f:
        extract_erpt(f, args.outdir)
