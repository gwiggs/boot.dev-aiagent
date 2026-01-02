from functions.run_python_file import run_python_file


def tests():
    files = [("main.py", None),
             ("main.py", ["3 + 5"]),
             ("tests.py", None),
             ("../main.py", None),
             ("nonexistent.py", None),
             ("lorem.txt", None),
             ]

    for file_path, args in files:
        result = run_python_file("calculator", file_path, args)

        if result:
            print(result)


def main():
    tests()


if __name__ == "__main__":
    main()
