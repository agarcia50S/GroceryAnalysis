import sys

# script takes txt file, removes duplicate items, and
# creates txt of the SAME NAME w/out duplicate items

path = sys.argv[1]

# make list of unique items
with open(path, mode='r') as in_f:
    content = in_f.readlines()
    uniques = []
    for item in content:
        if item not in uniques: uniques.append(item)

# make list into txt file    
with open(path, mode='w') as out_f:
    for u_val in uniques:
        out_f.write()
