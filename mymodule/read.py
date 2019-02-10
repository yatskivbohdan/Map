import string
import os

main_path = os.path.realpath(__file__)[:-7]


def read_f(in_file, out_file):
    '''
    (str, str) -> None
    Reads the locations list file and converts it in csv file
    '''

    lst = []
    f = open(main_path + in_file, 'r', errors= 'ignore')
    out = open(main_path + out_file, 'w', errors = 'ignore')
    for i in range(14):
        f.readline()
    for line in f:
        try:
            name_ind = line.index("(")
            if line[name_ind + 1] in string.ascii_letters:
                name_ind = line[name_ind+1:].index("(") + name_ind+1
            name = line[:name_ind-1]
            new_line = line[name_ind:]
            year_ind = new_line.index(")")
            year = new_line[1:year_ind]
            if line[-2] == ")":
                tab_ind1 = line.rindex("\t")
                tab_ind2 = line[:tab_ind1].rindex("\t")
                location = line[tab_ind2+1: tab_ind1+1]
            else:
                tab_ind = line.rindex("\t")
                location = line[tab_ind+1:-1]
            out.write(year + "," + name + "," + location + "\n")
        except ValueError:
            continue
