import re

with open('.\StrumBot\cities.txt', mode='r', encoding='utf-8') as inp_file:
    with open('.\StrumBot\cities_clean.txt', mode='w', encoding='utf-8') as out_file:
        for line in inp_file.readlines():
            pattern = r'^[^\(]+'
            match = re.match(pattern, line)
            # line = re.sub(pattern, line)
            # print(match)
            line2 = match.group().strip()
            print(line2)
            out_file.write(line2 + '\n')

