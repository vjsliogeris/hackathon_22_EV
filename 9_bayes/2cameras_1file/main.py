import os



cwd_file_names = os.listdir()
cwd_file_names.remove("main.py")

for file in cwd_file_names:
    print(f"\nreading {file[:-4]}\n\n")
    file = open(file, "r")
    full_list = []

    while file:
        line = file.readline()
        # remove \n
        line = line[:-1]
        # if eof
        if line == "":
            break
        full_list.append(line)

    # extract distinct values
    distinct = list(set(full_list))
    print(f"distinct values:\n{distinct}\n")

    # find appearances
    appearances = {}
    for lp in distinct:
        appearances[lp] = full_list.count(lp)
    print(f"appearances for each value:\n{appearances}\n")

    max_lp = str(max(appearances, key=appearances.get))
    print(f"max lp {max_lp}")


    input("\n\npress any key to continue")
    os.system("clear")
