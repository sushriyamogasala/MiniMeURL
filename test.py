from flask import Flask
from hashids import *

hashid = Hashids(min_length=6,salt="somestring",alphabet="abcdefghijklmnopqrstuvwxyz")

ev = hashid.encode(12345)
print(ev)
dv = hashid.decode(ev)
print(dv)