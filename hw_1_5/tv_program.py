import sys

from service import search

if __name__ == "__main__" or __name__ == "tv_program":
    program_name = " ".join(sys.argv[1:])
    program = search(program_name)
    print(f"Name: {program.name}")
    print(f"Network Name: {program.network.name}")
    print(f"Network Country Name: {program.network.country.name}")
    print(f"Summary: {program.summary}")
