def listfromtxt(file):
    with open(file, 'r') as f:
        name = [line.strip() for line in f]
        return name


def txtfromlist(file, list):
    import pathlib
    file = pathlib.Path(file)
    if file.exists():
        with open(file, 'w') as filehandle:
            for element in list:
                filehandle.write('%s\n' % element)
    else:
        print("File not exist")