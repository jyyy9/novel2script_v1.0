import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description='Novel2Script - Convert novel text to script')
    parser.add_argument('--input', required=True, help='Input novel text file path')
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        content = f.read()

    print(content)


if __name__ == '__main__':
    main()
