# ArmedSpiderMonkey

Generates random data based on an AVRO schema.

SAMPLE execution:

`python data_generator.py --MaxNumberOfElements 1000000
                          --MinNumberOfElements 10000
                          --NumberOfFiles 10
                          --SchemaPath ./schemas/example.avsc
                          --OutputPath ./dataOutput`


#ISSUES

*flat avro only, no nested data or lists
