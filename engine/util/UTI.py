import random,copy


def getRandom(MIN=0,MAX=10):
    return ((int(random.random()*(MAX-MIN+1))+MIN))
##
def genCode(code_format="XXXX",character=15):  #15  or 9
    alphabet="1234567890abcdefg"
    section=code_format.split("-")
    c=""
    for sec in section:
        for i in range(len(sec)):
            c+=alphabet[getRandom(0,character)]
        c+="-"
    return c[0:-1]
##
def dpcp(oldlist):
    return copy.deepcopy(oldlist)
##
def g(cc,*p):
    counts =int(cc)
    re=""
    for i in range(counts):
        re=re+genCode("X",15)
    return re
def g32():
    return g(32)
############################################################################
def defaultFun(*a):
    return ""
##
def same(a,*p):
    return a
##
def getGenWithPrefix(prefix,digital,*p):
    return prefix+"_"+g(digital)
##
def putUid(page,*p):
    return page.uid
##
def textGen(prefix,*p):
    return getGenWithPrefix(prefix,16)
##

    
##

##

##
