
def level_from_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        poss = []
        number_of_blocks = lines[0]
        for b in lines[1:]:
            pos = b.split(', ')
            x = int(pos[0])
            y = int(pos[1])
            poss.append([x, y])
        return poss
