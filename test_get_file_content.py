from functions.get_file_content import get_file_content


def tests():
    files = ["main.py", "pkg/calculator.py",
             "/bin/cat", "pgk/does_not_exist.py"]

    for file in files:
        result = get_file_content("calculator", file)
        if result:
            print(result)


def main():
    tests()


if __name__ == "__main__":
    main()
