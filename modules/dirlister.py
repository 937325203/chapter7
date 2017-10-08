import os

def run(**args):

    print '[*] In dirlister module'
    n=os.listdir('.')
    n=str(n)
    return n