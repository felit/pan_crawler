import time
print time.ctime(1468563800)
print time.ctime(1468563800)

print time.strftime('%Y-%m-%d %H-%M-%S',time.gmtime(1468563800))
def params(**args):
    print args.__class__
    print args
params(ss=900)