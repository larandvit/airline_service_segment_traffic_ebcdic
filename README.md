# Airline Service Segment Traffic EBCDIC Conversion

## Introduction
The repository includes a process of converting [Airline Service Segment Traffic and Capacity data files](https://catalog.archives.gov/search?q=*:*&f.ancestorNaIds=19077075&sort=naIdSort%20asc) located in 
[National Archives Catalog](https://catalog.archives.gov/). The files are coded in mainframe EBCDIC format.

There is comprehensive technical documentation accompanied files. The documentation outlines master data file description along with number of records in each file.

There are 2 issues with data.

1. Files contain Block Descriptor Word (BDW) bytes copied from tape media. Those bytes must be deleted to convert data.
2. File structure is not followed by master data file description. As per instructions, each record must contain at least 1 variable segment but it is not true.

##  Data Preparation
Because of BDW, the files are needed to be fixed removing BDW from the files. It can be done by the tool located in **app** folder. 

The tool usage

```text
Remove Block Descriptor Word (BDW) bytes from EBCDIC coded files. v.1.0.0

usage: fix_data.py [-h] --sourcefile "source file" --outputfile "output file"

optional arguments:
  -h, --help            show this help message and exit
  --sourcefile "source file"
                        Input file path
  --outputfile "output file"
                        Output file path
```

A sample of 1970 data file processing in Windows command prompt 

```bash
fix_data.py --sourcefile .\data\1970\RG197.SERVSEG.Y70 --outputfile .\data\1970\RG197.SERVSEG.Y70.ebc
```

## Data Processing
[EBCDIC Parser](https://github.com/larandvit/ebcdic-parser) is a tool to decode mainframe EBCDIC format into ASCII one. The tool requests developing of a layout file 
which contains conversion rules created based on the master data file description. The layout file is located in **layout** folder. The structure of the EBCDIC file is 
single schema variable record length.

A sample of 1970 data file converting in Windows command prompt

```bash
..\ebcdic-parser\ebcdic_parser.py --inputfile ".\data\1970\RG197.SERVSEG.Y70.ebc" --outputfolder ".\output\1970" --layoutfile "layout\service_segment_data.json" --logfolder ".\log\1970"
```

## Output
There are 2 files located in **output** folder. The first file with **RG197.SERVSEG.Y70__type___main.txt** name contains fixed length part and **RG197.SERVSEG.Y70___type___main__variable.txt** file 
is variable segments.

Each output file includes 2 extra fields at the end of records.

1. File name
2. A key to link fixed length part with variable segments.

## Resources
* [Mainframe Tape Details](http://www.3480-3590-data-conversion.com/article-mainframe-tape-details.html)  
* [Mainframe EBCDIC Data Converter to ASCII](https://github.com/larandvit/ebcdic-parser)
