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

def convertToPtp(bin_f, ptp_f, address, size, chunkSize):
    print("Starting conversion...")
    blocks = int(size / chunkSize)
    remainder = int(size % chunkSize)
    print("# of blocks: " + str(blocks))
    blockCounter = blocks
    while blockCounter > 0:
        blockCounter -= 1
        dataBytes = bin_f.read(chunkSize)
        line = bytearray()
        #print(str(dataBytes))
        ptp_f.write(';')        # print start of record
        ptp_f.write(hex(chunkSize)[2:].upper())
        #ptp_f.write(hex(address)[2:].upper())
        ptp_f.write("{:04x}".format(address).upper())
        ptp_f.write(dataBytes.hex().upper())
        line.extend(dataBytes)
        line.append(chunkSize)
        line.append(address >> 8)
        line.append(address & 0xFF)
        #print(line)
        #print(checksum(line))
        ptp_f.write('{0:0{1}X}'.format(checksum(line),4))
        ptp_f.write('\n')
        address += chunkSize
    if remainder > 0:
        dataBytes = bin_f.read(remainder)
        line = bytearray()
        #print(str(dataBytes))
        ptp_f.write(';')        # print start of record
        #ptp_f.write(hex(remainder)[2:].upper())
        ptp_f.write("{:02x}".format(remainder).upper())
        #ptp_f.write(hex(address)[2:].upper())
        ptp_f.write("{:04x}".format(address).upper())
        ptp_f.write(dataBytes.hex().upper())
        line.extend(dataBytes)
        line.append(remainder)
        line.append(address >> 8)
        line.append(address & 0xFF)
        #print(line)
        #print(checksum(line))
        ptp_f.write('{0:0{1}X}'.format(checksum(line),4))
        ptp_f.write('\n')
        address += remainder
    if chunkSize == 16:
        ptp_f.write(";00")
    if chunkSize == 24:
        ptp_f.write(";00")
        ptp_f.write('{0:0{1}X}'.format(blocks, 4))
        ptp_f.write('{0:0{1}X}'.format((blocks >> 8) + (blocks & 0xFF), 4))
        ptp_f.write(str(0x13))

if __name__ == "__main__":
    boardModel = sys.argv[1]
    binFileName = sys.argv[2]
    ptpFileName = sys.argv[3]
    try:
        startAddress = int(sys.argv[4], 16)
    except:
        print("Invalid start address!")
        exit(-3)
    if len(sys.argv) < 5:
        print("Not enough arguments!")
        exit(-2)
    try:
        if boardModel == "-s":
            chunkSize = 16
        if boardModel == "-k":
            chunkSize = 24
    except:
        print("Invalid board model!")
        exit(-4)
    try:
        bin_f = open(binFileName, "rb")
    except:
        print("File not found!")
        exit(-1)
    ptp_f = open(ptpFileName, "w")
    binFileSize = os.path.getsize(binFileName)
    print("Size of " + binFileName + ": " + str(binFileSize) + " bytes")
    convertToPtp(bin_f, ptp_f, startAddress, binFileSize, chunkSize)
    ptp_f.close()
    bin_f.close()
