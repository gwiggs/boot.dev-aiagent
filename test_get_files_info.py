from functions.get_files_info import get_files_info


def tests():
    paths = [".", "pkg", "/bin", "../"]

    try:
        for p in paths:
            result = get_files_info("calculator", p)
            if result:
                print(result)
    except Exception as e:
        print("Error: ", e)


def main():
    tests()


if __name__ == "__main__":
    main()
