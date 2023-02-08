def split_data(data):
    ndata = []

    nowlist = []
    for i in data:
        nowlist += [i]
        if int(i[0])%5 == 0:
            ndata += [nowlist.copy()]
            nowlist = []

    if len(nowlist) != 0:
        ndata += [nowlist.copy()]

    return ndata