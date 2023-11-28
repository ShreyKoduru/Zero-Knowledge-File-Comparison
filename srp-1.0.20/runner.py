# import os
# directory = 'server files'
# otherdir = 'client files'

# for filename in os.listdir(directory):
#     f = os.path.join(directory, filename)
#     if os.path.isfile(f):
#         print(f)        
#     for filename in os.listdir(otherdir):
#         f = os.path.join(otherdir, filename)
#         if os.path.isfile(f):
#             print(f)
        
from test_srp import *

tester(1,1)
tester(2,2)
tester(3,3)
tester(4,4)
tester(5,5)
