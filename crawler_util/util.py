import re


def get_num(s):
    if s.find('(') >= 0:
        s = s[:s.find('(')]
    res = ''
    pattern = '[0-9]+'
    numlist = re.findall(pattern, s)
    for item in numlist:
        res += item
    if res != '':
        return int(res)
    else:
        return 0
