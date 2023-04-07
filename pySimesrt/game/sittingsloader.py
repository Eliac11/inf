import json



def GetSittings():

    sittings = json.load(open("sittings.json"))
    return sittings


if __name__ == "__main__":
    print(GetSittings())