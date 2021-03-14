'''
    Converts a .bin file to paper tape
    SYM-1 or KIM-1 (KIM not implemented yet)
'''
import os, sys

def checksum(line):
    chkSum = 0
    for ch in line:
        chkSum += ch
    return chkSum

def convertToPtp(bin_f, ptp_f, address, size):
    print("Starting conversion...")
    blocks = int(size / 16)
    print("# of blocks: " + str(blocks))
    blockCounter = blocks
    while blockCounter > 0:
        blockCounter -= 1
        dataBytes = bin_f.read(16)
        line = bytearray()
        #print(str(dataBytes))
        ptp_f.write(';')        # print start of record
        ptp_f.write(hex(16)[2:].upper())
        ptp_f.write(hex(address)[2:].upper())
        ptp_f.write(dataBytes.hex().upper())
        line.extend(dataBytes)
        line.append(16)
        line.append(address >> 8)
        line.append(address & 0xFF)
        #print(line)
        #print(checksum(line))
        ptp_f.write('{0:0{1}X}'.format(checksum(line),4))
        ptp_f.write('\n')
        address += 16
    ptp_f.write(";00\r")
    ptp_f.close()
    bin_f.close()

if __name__ == "__main__":
    #boardModel = sys.argv[1]
    binFileName = sys.argv[1]
    ptpFileName = sys.argv[2]
    try:
        startAddress = int(sys.argv[3], 16)
    except:
        print("Invalid start address!")
        exit(-3)
    if len(sys.argv) < 4:
        print("Not enough arguments!")
        exit(-2)
    try:
        bin_f = open(binFileName, "rb")
    except:
        print("File not found!")
        exit(-1)
    ptp_f = open(ptpFileName, "w")
    binFileSize = os.path.getsize(binFileName)
    print("Size of " + binFileName + ": " + str(binFileSize) + " bytes")
    convertToPtp(bin_f, ptp_f, startAddress, binFileSize)
