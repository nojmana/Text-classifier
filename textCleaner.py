


fNames = ['biznes', 'film', 'literatura', 'motoryzacja', 'nauka', 'politechnika', 'polityka', 'sport', 'uniwersytet', 'uroda']
extension = '.txt'

for name in fNames:
    with open(name + extension) as f:
        file = open(name + "C" + extension, 'w')
        for line in f:
            wczyt = line.find("Wczytuję...")
            dzial = line.find("Działam...")
            zgl = line.find("Zgłoś naruszenie  treści")

            if wczyt == -1 and dzial == -1 and zgl == -1 and not line.isspace():
                file.write(line)
