#!/bin/python3
import sys


class CFGParser:
    def __init__(self, filename):
        self._filename = filename

    def parse(self):
        with open(self._filename, "rb") as fn:
            # print(fn.read().encode('utf-8').strip())
            for l in fn.read().splitlines():
                print(l)
            # lines = fn.read().splitlines()
            # print(lines)
            # print(len(lines))
            print(self._filename)


def main():
    filename = sys.argv[1]
    cfg_parser = CFGParser(filename)
    cfg_parser.parse()


if __name__ == "__main__":
    main()
