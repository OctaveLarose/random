#!/usr/bin/python

def part1(instrs: [(str, int)]) -> (int, int):
    h, d = 0, 0

    for dir, val in instrs:
        if dir == "forward":
            h = h + val
        elif dir == "down":
            d = d + val
        elif dir == "up":
            d = d - val

    return h, d


def main():
    instrs = [(line[:-1].split()[0], int(line[:-1].split()[1])) for line in open("input2", 'r').readlines()]

    print(instrs)
    print("Part 1:", part1(instrs))


if __name__ == "__main__":
    main()
