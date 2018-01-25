try:
    from random import seed, randint
    import json
    import argparse
    import sys
    from time import sleep
    print("Imports are good")
except Exception as e:
    print("IMPORT ERROR", e)

# set for consistent randomness
seed(42)
# for x in range(0, 3):
#     print(randint(0, 99))
#     # should print 63, 2, 27

parser = argparse.ArgumentParser()
parser.add_argument('--numberOfElements', help='Number of Data Elements to create', type=int)
parser.add_argument('--outputFormat', help='Select from JSON, CSV, SQL, TSV, AVRO', type=str)
# parser.add_argument('--foo', help='Foo the program')
args = parser.parse_args()
print(args)
