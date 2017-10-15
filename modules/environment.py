import os

def run(**args):
    print "[*] In enviroment module"
    x=os.environ
    return str(x)