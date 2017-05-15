import random

from arbitrary_pieces import r_int


class C(object):
    r = random.randint

for i in range(40):
    inst = C()
    print(inst.r(0,10))