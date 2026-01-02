from functions.write_file import write_file


def tests():
    files = {"lorem.txt": "wait, this isn't lorem ipsum", "pkg/morelorem.txt": "lorem ipsum dolor sit amet",
             "/tmp/temp.txt": "this should not be allowed"}

    for file in files.items():
        result = write_file("calculator", file[0], file[1])
        if result:
            print(result)


def main():
    tests()


if __name__ == "__main__":
    main()
