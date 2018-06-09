def readTags():
    with open('tags.txt') as f:
        tags = f.readline()
    tags = tags.split()
    return tags


def main():
    fNames = readTags()
    extension = '.txt'
    for name in fNames:
        with open('texts/' + name + extension) as f:
            file = open('texts_cleaned/' + name + extension, 'w')
            for line in f:
                wczyt = line.find("Wczytuję...")
                dzial = line.find("Działam...")
                zgl = line.find("Zgłoś naruszenie treści")

                if wczyt == -1 and dzial == -1 and zgl == -1 and not line.isspace():
                    file.write(line)

if __name__ == '__main__':
    main()