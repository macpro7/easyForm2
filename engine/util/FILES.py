
import os


def getFileContent(filename):
    cont=""
    try:
        with open(filename ,'r',encoding="UTF-8") as f:
            cont= f.read()
    except(Exception) as e:
        print(e)
        print(">> getFileContent meets an error!")
        cont=""
    return cont