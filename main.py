#!/bin/env python3
from pprint import PrettyPrinter
import sqlite3, sys

def pprint(content):
  PrettyPrinter(indent=2).pprint(content)

db = sys.argv[1] if len(sys.argv) != 1 else "./domoticz.db"

connect = sqlite3.connect(db)
c = connect.cursor()

# Correct overflow values
c.execute("UPDATE Meter SET Usage = (((Usage/10) - 16777216)*10) WHERE DeviceRowID = 230 AND Usage > 100000")
connect.commit()

Value = [i[0] for i in c.execute("SELECT Value FROM Meter WHERE DeviceRowID = 230 ORDER BY Date ASC")]
Usage = [i[0] for i in c.execute("SELECT Usage FROM Meter WHERE DeviceRowID = 230 ORDER BY Date ASC")]
BaseValue = 2497359

tmp = 0
ValueClear = []

for i in Usage:
  ValueClear.append(BaseValue + tmp)
  tmp += int(i*(5/600))

# Printing edited values in a txt file
r = c.execute("SELECT * FROM Meter WHERE DeviceRowID = 230")

merged = []
for i in range(len(Value)):
  merged.append((Value[i], ValueClear[i]))

with open("tmp.txt", "w+") as f:
  for i in merged:
    txt = f"{i[0]}, {i[1]}\n"
    f.write(txt)
pprint(merged)