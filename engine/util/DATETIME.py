from datetime import * 

def getNowFull(*a):
    c= str(datetime.now())
    return c[:c.find(".")]


def getDate(*a):
    c=getNowFull(a)
    c=c[:c.find(" ")]
    return c
