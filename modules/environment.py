import os

def run(**args):
    print "[*] In enviroment module"
    x=os.environ
    p=str(x)
    return p