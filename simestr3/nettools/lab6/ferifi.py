import pyfence
import os
import sys

sys.path.append(os.getcwd())
sys.argv.pop(0)
path = sys.argv[0]
print(exec(compile(open(path).read(), path, 'exec')))