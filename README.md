# ROMPTP
Converts ROM images and binaries to SYM-1/KIM-1 compatible paper tape formats.

## Prerequisite
Ths program is Python 3.x compliant, but it shouldn't be difficult to convert it to Python 2.x if you need to. No special libraries are required, just the base installation.

## Usage
The syntax of this tool is:\
`romptp.py file.bin file.ptp [start address < FFFF]`\
For example, to convert the BASIC_1.1.BIN to SYM-1 paper tape, you must enter:\
`romptp.py BASIC_1.1.BIN basic.ptp C000`\
Right now, there are no plans to support variable length record lines, as there is no real need.

KIM-1 paper tapes are not yet supported, they will be added soon.