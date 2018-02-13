#! /Users/pls8208/anaconda3/bin/python

# author James Etheredge

# sample arguments
# --MaxNumberOfElements
# 1000000
# --MinNumberOfElements
# 10000
# --NumberOfFiles
# 100
# --SchemaPath
# ./schemas/example.avsc
# --OutputPath
# ./dataOutput


try:
    import timeit
    from random import seed, randint
    import random
    import json
    import csv
    import argparse
    import sys
    from time import sleep
    import avro.schema
    from avro.datafile import DataFileReader, DataFileWriter
    from avro.io import *
    import uuid
    import string
    print("Imports are good")
except Exception as e:
    print("IMPORT ERROR", e)

# set for consistent randomness
seed(42)
# for x in range(0, 3):
#     print(randint(0, 99))
#     # should print 63, 2, 27

parser = argparse.ArgumentParser()
# parser.add_argument('--foo', help='Foo the program')
parser.add_argument('--MaxNumberOfElements', help='Max number of Data Elements to create per file', type=int)
parser.add_argument('--MinNumberOfElements', help='Number of Data Elements to create file', type=int)
parser.add_argument('--NumberOfFiles', help='Number of Data Elements to create file', type=int)
parser.add_argument('--SchemaPath', help='path to schema', type=str)
parser.add_argument('--OutputPath', help='path to schema', type=str)


#limiting to avro for now
#parser.add_argument('--outputFormat', help='Select from JSON, CSV, SQL, TSV, AVRO', type=str)

args = parser.parse_args()
print(args)

# load file as json object
jsonSchema = json.loads(open(args.SchemaPath).read())
#convert to avro schema
curSchema = avro.schema.Parse(json.dumps(jsonSchema))

#load some less boring names
names = []
with open('./data/avengers.csv') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
        n = (row['Name/Alias'])
        if len(n) > 5:
            names.append(n)

# fetch random name
def getName():
    return names[randint(0, len(names)-1)]

# generate a random randomly sized ASCII string (no spaces)
def getString(size=25, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# iterate fields and create appropriate data
def genFakeDataFromSchema(inSchema):
    newData = {}
    for field in curSchema.fields:
        print(field.type)
        if "name" in field.name.lower():
            newData[field.name] = getName()
        elif field.name.lower() == "id":
            newData[field.name] = str(uuid.uuid4())
        elif "string" in str(field.type).lower():
             newData[field.name] = getString(size=randint(0,100))
        elif "boolean" in str(field.type).lower():
            newData[field.name] = bool(random.getrandbits(1))
        elif "int" in str(field.type).lower():
            newData[field.name] = randint(0, 60000)
        elif "float" in str(field.type).lower():
            newData[field.name] = float(random.random() * randint(0, 60000))
        elif "double" in str(field.type).lower():
            newData[field.name] = float(random.random() * randint(0, 60000))
        #randomly null nullable fields
        if "null" in str(field.type).lower():
            if bool(random.getrandbits(1)) and bool(random.getrandbits(1)):
                newData.pop(field.name)

    # print(newData)
    return newData

totalRecords = 0
# main loop/writer
start = timeit.default_timer()

for count in range(0, abs(args.NumberOfFiles)):
     curUUID = uuid.uuid4()
     writer = DataFileWriter(open(args.OutputPath + "/" + str(curUUID) + ".armed.spider.monkey.avro", "wb"), DatumWriter(), curSchema)
     recordCount = randint(args.MinNumberOfElements, args.MaxNumberOfElements)
     print("Generating %d records for %s" % (recordCount, str(curUUID)))
     for rec in range(0, recordCount):
         if rec % 10000 < 1:
             print("%d of %d records complete for %s file %d of %d" % (rec, recordCount, str(curUUID), count+1, args.NumberOfFiles))
         writer.append(genFakeDataFromSchema(curSchema))
         totalRecords += 1

     writer.close()

stop = timeit.default_timer()
print("%d records generated in %.1f minutes" % (totalRecords, (stop - start)/60.0 ))
recPerSec = totalRecords/float(stop - start)
print("%.4f records per second" % recPerSec)
