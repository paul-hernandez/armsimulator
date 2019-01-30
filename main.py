import sys
import os


class WriteBack:
    def run(self):
        if sim.postALU[1] != -1:
            sim.R[sim.destReg[sim.postALU[1]]] = main.get_bin(sim.postALU[0], 64)
            sim.postALU = [-1, -1]
        if sim.postMEM[1] != -1:
            sim.R[sim.destReg[sim.postMEM[1]]] = main.get_bin(sim.postMEM[0], 64)
            sim.postMEM = [-1, -1]

class ALUClass:
    def run(self):
        # elif (op == "ADDI"):
        # registers[arg3[x]] = main.get_bin(main.getRegInt(registers[arg1[x]]) + arg2[x], 64)
        i = sim.preALU [0]
        if i != -1:
            if (sim.opcode[i] == "ADDI"):
                sim.postALU = [main.getRegInt(sim.R[sim.arg1[i]]) + sim.arg2[i], i]
            elif (sim.opcode[i] == "SUBI"):
                sim.postALU = [main.getRegInt(sim.R[sim.arg1[i]]) - sim.arg2[i], i]
            elif (sim.opcode[i] == "ADD"):
                sim.postALU = [main.getRegInt(sim.R[sim.arg1[i]]) + main.getRegInt(sim.R[sim.arg2[i]]), i]
            elif (sim.opcode[i] == "SUB"):
                sim.postALU = [main.getRegInt(sim.R[sim.arg1[i]]) - main.getRegInt(sim.R[sim.arg2[i]]), i]
            elif (sim.opcode[i] == "LSL"):
                sim.postALU = [main.getRegInt(   sim.R[sim.arg1[i]][sim.arg2[i]:64] + '0' * sim.arg2[i]  ), i]
                #registers[arg3[x]] = registers[arg1[x]][arg2[x]:64] + '0' * arg2[x]
            elif (sim.opcode[i] == "LSR"):
                sim.postALU = [main.getRegInt(  sim.arg2[i] * '0' + sim.R[sim.arg1[i]][0:64 - sim.arg2[i]]  ), i]
                #registers[arg3[x]] = arg2[x] * '0' + registers[arg1[x]][0:64 - arg2[x]]
            elif (sim.opcode[i] == "ASR"):
                sim.postALU = [main.getRegInt(sim.arg2[i] * '1' + sim.R[sim.arg1[i]][0:64 - sim.arg2[i]]), i]
                #registers[arg3[x]] = arg2[x] * '1' + registers[arg1[x]][0:64 - arg2[x]]
            elif (sim.opcode[i] == "AND"):
                sim.postALU = [(main.getRegInt((sim.R[sim.arg1[i]])) & (main.getRegInt(sim.R[sim.arg2[i]]))), i]
            elif (sim.opcode[i] == "ORR"):
                sim.postALU = [(main.getRegInt((sim.R[sim.arg1[i]])) | (main.getRegInt(sim.R[sim.arg2[i]]))), i]
            elif (sim.opcode[i] == "EOR"):
                sim.postALU = [(main.getRegInt((sim.R[sim.arg1[i]])) ^ (main.getRegInt(sim.R[sim.arg2[i]]))), i]
            elif (sim.opcode[i] == "MOVZ"):
                returnValue = '0000000000000000000000000000000000000000000000000000000000000000'
                if (sim.arg2[i] == 0):
                    sim.postALU = [main.getRegInt(returnValue[0:48] + main.get_bin(sim.arg3[i], 16)), i]
                if (sim.arg2[i] == 16):
                    sim.postALU = [main.getRegInt(returnValue[0:32] + main.get_bin(sim.arg3[i], 16) + returnValue[48:64]), i]
                if (sim.arg2[i] == 32):
                    sim.postALU = [main.getRegInt(returnValue[0:16] + main.get_bin(sim.arg3[i], 16) + returnValue[32:64]), i]
                if (sim.arg2[i] == 48):
                    sim.postALU = [main.getRegInt(main.get_bin(sim.arg3[i], 16) + returnValue[16:64]), i]
            elif (sim.opcode[i] == "MOVK"):
                returnValue = sim.R[sim.arg1[i]]
                if (sim.arg2[i] == 0):
                    sim.postALU = [main.getRegInt(returnValue[0:48] + main.get_bin(sim.arg3[i], 16)), i]
                if (sim.arg2[i] == 16):
                    sim.postALU = [main.getRegInt(returnValue[0:32] + main.get_bin(sim.arg3[i], 16) + returnValue[48:64]), i]
                if (sim.arg2[i] == 32):
                    sim.postALU = [main.getRegInt(returnValue[0:16] + main.get_bin(sim.arg3[i], 16) + returnValue[32:64]), i]
                if (sim.arg2[i] == 48):
                    sim.postALU = [main.getRegInt(main.get_bin(sim.arg3[i], 16) + returnValue[16:64]), i]
            else:
                sim.postALU = [0, sim.preALU[0]]
            sim.preALU[0] = sim.preALU[1]
            sim.preALU[1] = -1



class MEMClass:
    def run(self):
        i = sim.preMEM[0]
        if i != -1:
            if (sim.opcode[i] == "LDUR"):

                    dataNum = int((int(((main.getRegInt(sim.R[sim.arg1[i]]) + (sim.arg2[i] * 4)))) - ((sim.numInstructions * 4) + 96)) / 4)

                    cacheLoad = sim.cache.accessMem(dataNum, -1, 0, 0)
                    if cacheLoad[0] == True:
                            sim.postMEM = [(cacheLoad[1]), i]

                    else:
                        return

            elif (sim.opcode[i] == "STUR"):
                dataNum = int((int(((main.getRegInt(sim.R[sim.arg1[i]]) + (sim.arg2[i] * 4)))) - ((sim.numInstructions * 4)+96))/4)

                cacheLoad = sim.cache.accessMem(dataNum, -1, 1, main.getRegInt(sim.R[sim.arg3[i]]))
                if cacheLoad[0] == True:
                    pass
                else:
                    if len(sim.memory) < dataNum:
                         for d in range(dataNum - len(sim.memory) + 1):
                              sim.memory.append('00000000000000000000000000000000')
                    return
            sim.preMEM[0] = sim.preMEM[1]
            sim.preMEM[1] = -1

class IssueUnit:

    def RAWhazardExists(self, i, current):

        for x in range (current):
            if sim.src1Reg[i] == sim.destReg[sim.preIssueBuff[x]] or sim.src2Reg[i] == sim.destReg[sim.preIssueBuff[x]]:
                return True

        if sim.src1Reg[i] == sim.destReg[sim.preALU[0]] or sim.src1Reg[i] == sim.destReg[sim.preALU[1]]:
            #sim.output.write("\nHazard1\n")
            return True
        if sim.src2Reg[i] == sim.destReg[sim.preALU[0]] or sim.src2Reg[i] == sim.destReg[sim.preALU[1]]:
            #sim.output.write("\n" + str(sim.src2Reg[i]) + " " + str(sim.destReg[sim.preALU[0]]) + " " + str(sim.destReg[sim.preALU[1]]) +"\n")
            #sim.output.write("\nHazard2\n")
            return True
        if sim.src1Reg[i] == sim.destReg[sim.preMEM[0]] or sim.src1Reg[i] == sim.destReg[sim.preMEM[1]]:
            #sim.output.write("\nHazard3\n")
            return True
        if sim.src2Reg[i] == sim.destReg[sim.preMEM[0]] or sim.src2Reg[i] == sim.destReg[sim.preMEM[1]]:
            #sim.output.write("\nHazard4\n")
            return True
        if int(sim.src1Reg[i]) == int(sim.destReg[sim.postALU[1]]):
            #sim.output.write("\nHazard5\n")
            return True
        if int(sim.src1Reg[i]) == int(sim.destReg[sim.postMEM[1]]):
            #sim.output.write("\nHazard6\n")
            return True
        if int(sim.src2Reg[i]) == int(sim.destReg[sim.postALU[1]]):
            #sim.output.write("\nHazard7\n")
            return True
        if int(sim.src2Reg[i]) == int(sim.destReg[sim.postMEM[1]]):
            #sim.output.write("\nHazard8\n")
            return True
        if sim.opcode[i] == "STUR":
            return False
        for x in range (current):
            if sim.destReg[i] == sim.destReg[sim.preIssueBuff[x]] or sim.src2Reg[i] == sim.destReg[sim.preIssueBuff[x]]:
                # sim.output.write("\nHazard1\n")
                return True

        if sim.destReg[i] == sim.destReg[sim.preALU[0]] or sim.destReg[i] == sim.destReg[sim.preALU[1]]:
            #sim.output.write("\nHazard1\n")
            return True
        if sim.destReg[i] == sim.destReg[sim.preMEM[0]] or sim.destReg[i] == sim.destReg[sim.preMEM[1]]:
            #sim.output.write("\nHazard3\n")
            return True
        if int(sim.destReg[i]) == int(sim.destReg[sim.postALU[1]]):
            #sim.output.write("\nHazard5\n")
            return True
        if int(sim.destReg[i]) == int(sim.destReg[sim.postMEM[1]]):
            #sim.output.write("\nHazard6\n")
            return True

        return False

    def run(self):
        numIssued = 0
        numInPreIssueBuff = sim.returnNumPreIssue()
        curr = 0

        while (numIssued < 2 and numInPreIssueBuff > 0 and curr < 4):  # curr is current pre issue element
            issueMe = True
            # get an instruction from preissueBuff starting with element 0
            index = sim.preIssueBuff[curr]
            # make sure there is an instruction to execute
            if index == -1:
                break
            if sim.isMemOp(index) and not -1 in sim.preMEM:
                issueMe = False
                break
            # if another instruction type same for preALUbuff
            if not sim.isMemOp(index) and not -1 in sim.preALU:
                issueMe = False
                break
            #checks hazards
            #Checks destination register in preALU

            if self.RAWhazardExists(index, curr):
                issueMe = False
                curr = curr + 1
                continue

            if numIssued == 1:
                pass

            if issueMe:
                numIssued += 1
                # copy the instruction to the appropriate buffer
                # the assumption here is that we will have a -1 in the right spot! Think we will.
                if sim.isMemOp(index):
                    sim.preMEM[sim.preMEM.index(-1)] = index
                else:
                    sim.preALU[sim.preALU.index(-1)] = index

                # move the instrs in the preissue buff down one level
                sim.preIssueBuff[0:curr] = sim.preIssueBuff[0:curr]
                sim.preIssueBuff[curr:3] = sim.preIssueBuff[curr + 1:]  # dropped 4, think will go to end always
                sim.preIssueBuff[3] = -1
                numInPreIssueBuff -= 1



class FetchUnit:

    def isStillRunning(self):
        if sim.preMEM == [-1, -1] and sim.preALU == [-1, -1] and sim.postMEM == [-1, -1] and sim.postALU == [-1, -1] and sim.preIssueBuff == [-1, -1, -1, -1]:
            return False
        return True
        pass


    def pushToIssueBuff(self, i):

        if sim.preIssueBuff[0] == -1:
            sim.preIssueBuff = [i, -1, -1, -1]
        elif sim.preIssueBuff[1] == -1:
            sim.preIssueBuff = [sim.preIssueBuff[0], i, -1, -1]
        elif sim.preIssueBuff[2] == -1:
            sim.preIssueBuff = [sim.preIssueBuff[0], sim.preIssueBuff[1], i, -1]
        elif sim.preIssueBuff[3] == -1:
            sim.preIssueBuff = [sim.preIssueBuff[0], sim.preIssueBuff[1], sim.preIssueBuff[2], i]

    def cBranchReady(self, i):
        if sim.src1Reg[i] == sim.destReg[sim.preALU[0]] or sim.src1Reg[i] == sim.destReg[sim.preALU[1]]:
            return False

        if sim.src1Reg[i] == sim.destReg[sim.preMEM[0]] or sim.src1Reg[i] == sim.destReg[sim.preMEM[1]]:
            return False

        if int(sim.src1Reg[i]) == int(sim.destReg[sim.postALU[1]]):
            return False

        if int(sim.src1Reg[i]) == int(sim.destReg[sim.postMEM[1]]):
            return False

        return True

    def __init__(self):
        self.waitOnSecond = False


    def run(self):
        first = sim.currentIndex()
        sec = first + 1
        onlyFirst = False

        if not -1 in sim.preIssueBuff:
            return True



        cacheTest = sim.cache.accessMem( -1, first, 0, 0)

        if cacheTest[0] == True:
            if (first < sim.numInstructions - 1) and sim.preIssueBuff[2] == -1 and not sim.opcode[first] == "B" and not ((0 == main.getRegInt(sim.R[first])) and sim.opcode[first] == "CBZ") and not ((0 != main.getRegInt(sim.R[first])) and sim.opcode[first] == "CBNZ"):
                cacheTest2 = sim.cache.accessMem(-1, sec, 0, 0)
                if cacheTest2[0] == True:
                    pass
                else:
                    onlyFirst = True

            else:
                onlyFirst = True


        elif cacheTest[0] == False:
            return True




        if sim.opcode[first] == "BREAK":
            if self.isStillRunning():
                return True
            return False #This ends the program

        if sim.opcode[first] == "B":
            sim.PC = sim.PC + (sim.arg1[first] * 4)

            return True

        if sim.opcode[first] == "CBZ":
            if self.cBranchReady(first):
                if (0 == main.getRegInt(sim.R[first])):
                    sim.PC = sim.PC + (sim.arg1[first] * 4)
                    return True
                else:
                    sim.PC = sim.PC + 4
                    return True
            return True

        if sim.opcode[first] == "CBNZ":
            if self.cBranchReady(first):
                if (0 != main.getRegInt(sim.R[first])):
                    sim.PC = sim.PC + (sim.arg1[first] * 4)
                else:
                    sim.PC = sim.PC + 4
                    return True

            return True

        if sim.opcode[first] == "NOP":
            if onlyFirst:
                sim.PC = sim.PC + 4
                return True

            if sim.opcode[sec] == "BREAK":
                if self.isStillRunning():
                    sim.PC = sim.PC + 4
                    return True
                return False  # This ends the program

            if sim.opcode[sec] == "B":
                sim.PC = sim.PC + (sim.arg1[sec] * 4) + 4
                return True

            if sim.opcode[sec] == "CBZ":
                if self.cBranchReady(sec):
                    if (0 == main.getRegInt(sim.R[sec])):
                        sim.PC = sim.PC + (sim.arg1[sec] * 4) + 4
                    else:
                        sim.PC = sim.PC + 8
                        return True
                return True

            if sim.opcode[sec] == "CBNZ":
                if self.cBranchReady(sec):
                    if (0 != main.getRegInt(sim.R[sec])):
                        sim.PC = sim.PC + (sim.arg1[sec] * 4) + 4
                    else:
                        sim.PC = sim.PC + 8
                        return True
                return True

            if sim.opcode[sec] == "NOP":
                sim.PC = sim.PC + 8
                return True

            self.pushToIssueBuff(sec)
            sim.PC = sim.PC + 8
            return True

        self.pushToIssueBuff(first)

        if onlyFirst:
            sim.PC = sim.PC + 4
            return True

        if not -1 in sim.preIssueBuff:
            sim.PC = sim.PC +4
            return True

        if sim.opcode[sec] == "BREAK":
            if self.isStillRunning():
                sim.PC = sim.PC + 4
                return True
            return False  # This ends the program

        if sim.opcode[sec] == "B":
            sim.PC = sim.PC + (sim.arg1[sec] * 4) + 4
            return True



        if sim.opcode[sec] == "CBZ":
            if self.cBranchReady(sec):
                if (0 == main.getRegInt(sim.R[sec])):
                    sim.PC = sim.PC + (sim.arg1[sec] * 4) + 4
                    return True
                else:
                    sim.PC = sim.PC + 8
                    return True
            sim.PC = sim.PC + 4
            return True

        if sim.opcode[sec] == "CBNZ":
            if self.cBranchReady(sec):
                if (0 != main.getRegInt(sim.R[sec])):
                    sim.PC = sim.PC + (sim.arg1[sec] * 4) + 4
                    return True
                else:
                    sim.PC = sim.PC + 8
                    return True
            sim.PC = sim.PC + 4
            return True

        if sim.opcode[sec] == "NOP":
            sim.PC = sim.PC + 8
            return True


        self.pushToIssueBuff(sec)
        sim.PC = sim.PC + 8
        return True


class cacheClass:

    def accessMem(self, memIndex, instructionIndex, isWriteToMem, dataToWrite):

        dataToWrite = dataToWrite
        addressLocal = None
        dataWord = None
        data1 = None
        data2 = None
        hit = False
        assocblock = None
        wbAddr = 0
        self.tagMask = 4294967264  # -> 11111111111111111111111111100000
        self.setMask = 24  # -> 0000000000000000000000000011000

        if (memIndex == -1):   # If memIndex = 0 and instructionIndex = 1, then addressLocal = 100
            addressLocal = 96 + ( 4 * instructionIndex ) # correct

        # Memory index: If memIndex = 0, then addressLocal = 212...  If memIndex = 1, then addressLocal = 216
        else:
            addressLocal = 96 + (4 *  (sim.numInstructions) ) + (4 * memIndex)

        if addressLocal % 8 == 0: 
            dataWord = 0
            address1 = addressLocal
            address2 = addressLocal + 4

        if addressLocal % 8 != 0:
            dataWord = 1
            address1 = addressLocal - 4
            address2 = addressLocal



        if address1 < 96 + (4 * sim.numInstructions):
            data1 = sim.instruction[sim.indexOfAddress(address1)]
        else:
            try:
                data1 = sim.memory[sim.indexOfAddress(address1)- sim.numInstructions]
            except (IndexError):
                data1 = 0

        if address2 < 96 + (4 * sim.numInstructions):
            data2 = sim.instruction[sim.indexOfAddress(address2)]
        else:
            try:
                data2 = sim.memory[sim.indexOfAddress(address2)- sim.numInstructions]
            except (IndexError):
                data2 = 0


        if isWriteToMem and dataWord == 0:
            data1 = dataToWrite

        elif isWriteToMem and dataWord == 1:
            data2 = dataToWrite

        setNum = (address1 & self.setMask) >> 3
        tag = (address1 & self.tagMask) >> 5

        if (self.cacheSets[setNum][0][0] == 1 and self.cacheSets[setNum][0][2] == tag):
            hit = True
            assocblock = 0

        elif self.cacheSets[setNum][1][0] == 1 and self.cacheSets[setNum][1][2] == tag:
            hit = True
            assocblock = 1


        if (hit):
            if hit and isWriteToMem:
                self.cacheSets[setNum][assocblock][1] = 1  # dirty bit
                self.lruBit[setNum] = (assocblock + 1) % 2  # lru bit
                self.cacheSets[setNum][assocblock][dataWord + 3] = dataToWrite
                # if len(sim.memory) < memIndex:
                #      for d in range(memIndex - len(sim.memory) + 1):
                #          sim.memory.append('00000000000000000000000000000000')
                # sim.memory[memIndex] = main.get_bin(dataToWrite ,32)


            elif hit:
                self.lruBit[setNum] = (assocblock + 1) % 2



            return [True, self.cacheSets[setNum][assocblock][dataWord + 3]]

        if address1 in self.justMissedList:
            while (self.justMissedList.count(address1) > 0):
                self.justMissedList.remove(address1)

            if self.cacheSets[setNum][self.lruBit[setNum]][1] == 1:
                wbAddr = self.cacheSets[setNum][self.lruBit[setNum]][2]
                wbAddr = (wbAddr << 5) + (setNum << 3)
            if (wbAddr >= (sim.numInstructions * 4) + 96):
                sim.memory[memIndex] = self.cacheSets[setNum][self.lruBit[setNum]][3]
                # if len(sim.memory) < memIndex:
                #     for d in range(memIndex - len(sim.memory) + 1):
                #         sim.memory.append('00000000000000000000000000000000')
                # sim.memory[memIndex] = self.cacheSets[setNum][self.lruBit[setNum]][3]
            if (wbAddr + 4 >= (sim.numInstructions * 4) + 96):
                sim.memory[memIndex] = self.cacheSets[setNum][self.lruBit[setNum]][4]
                # if len(sim.memory) < memIndex:
                #     for d in range(memIndex - len(sim.memory) + 1):
                #         sim.memory.append('00000000000000000000000000000000')
                # sim.memory[memIndex] = self.cacheSets[setNum][self.lruBit[setNum]][3]

            self.cacheSets[setNum][self.lruBit[setNum]][0] = 1  # valid  we are writing a block
            self.cacheSets[setNum][self.lruBit[setNum]][1] = 0  # reset the dirty bit
            if (isWriteToMem):
                self.cacheSets[setNum][self.lruBit[setNum]][1] = 1
            self.cacheSets[setNum][self.lruBit[setNum]][2] = tag  # tag
            self.cacheSets[setNum][self.lruBit[setNum]][3] = data1  # data
            self.cacheSets[setNum][self.lruBit[setNum]][4] = data2  # nextData
            self.lruBit[setNum] = (self.lruBit[setNum] + 1) % 2  # set lru to show block is recently used  1 means block 0 MRU and 0 means block 1 MRU
            return [True, self.cacheSets[setNum][(self.lruBit[setNum] + 1) % 2][dataWord + 3]]
        else:
            if (self.justMissedList.count(address1) == 0):
                self.justMissedList.append(address1)

            return [False, 0]

    def __init__(self):
        self.cacheSets = [[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
                     [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]]

        self.lruBit = [0, 0, 0, 0]

        self.justMissedList = []



class simClass:

    def testFunction(self):

        self.run()


    def currentIndex(self):
        return int(((self.PC-96) / 4))


    def indexOfAddress(self, address):
        return int(((address-96) / 4))


    def isMemOp(self, index):
        if self.opcode[index] == "LDUR" or self.opcode[index] == "STUR":
            return True
        return False

    def returnNumPreIssue(self):
        num = 0
        for x in self.preIssueBuff:
            if x != -1:
                num = num + 1
        return num


    def __init__ (self, instrs, opcodes, mem, valids, addrs, arg1, arg2, arg3, arg1Str, arg2Str, arg3Str, numInstrs, dest, src1, src2, outputFileName):
        self.instruction = instrs
        self.opcode = opcodes
        self.memory = mem
        self.address = addrs
        self.numInstructions = numInstrs
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.arg1Str = arg1Str
        self.arg2Str = arg2Str
        self.arg3Str = arg3Str
        self.destReg = dest
        self.src1Reg = src1
        self.src2Reg = src2
        self.outputFileName = outputFileName
        self.output = open(outputFileName + "_out_pipeline.txt", "w")
        self.cycle = 1
        self.R = ['0000000000000000000000000000000000000000000000000000000000000000'] * 32
        self.PC = 96
        #R is for registers 0-31
        self.preIssueBuff = [-1,-1,-1,-1]
        self.preALU = [-1, -1]
        self.postALU = [-1, -1]
        self.preMEM = [-1, -1]
        self.postMEM = [-1, -1]
        self.WB = WriteBack()
        self.ALU = ALUClass()
        self.MEM = MEMClass()
        self.issue = IssueUnit()
        self.fetch = FetchUnit()
        self.cache = cacheClass()




    def run(self):

        go = True
        while go:
            self.WB.run()
            self.ALU.run()
            self.MEM.run()
            self.issue.run()
            go = self.fetch.run()
            self.printState()
            self.cycle += 1
            if go:
                self.output.write("\n")
        self.output.close()

    def printState(self):


        self.output.write("--------------------\n")
        self.output.write("Cycle:" + str(self.cycle) + "\n\n")
        self.output.write("Pre-Issue Buffer:\n")
        for x in range(4):
            self.output.write("\tEntry " + str(x) + ":")
            if self.preIssueBuff[x] == -1:
                self.output.write("\n")
                continue
            self.output.write(
                '\t' + '[' + self.opcode[self.preIssueBuff[x]] + self.arg1Str[self.preIssueBuff[x]] + self.arg2Str[
                    self.preIssueBuff[x]] + self.arg3Str[self.preIssueBuff[x]] + ']')
            self.output.write("\n")
        self.output.write("Pre_ALU Queue:\n")
        for x in range(2):
            self.output.write("\tEntry " + str(x) + ":")
            if self.preALU[x] != -1:
                self.output.write(
                    '\t' + '[' + self.opcode[self.preALU[x]] + self.arg1Str[self.preALU[x]] + self.arg2Str[
                        self.preALU[x]] + self.arg3Str[self.preALU[x]] + ']')
            self.output.write("\n")
        self.output.write("Post_ALU Queue:\n")
        self.output.write("\tEntry 0:")
        if sim.postALU[1] != -1:
            self.output.write('\t' + '[' + self.opcode[self.postALU[1]] + self.arg1Str[self.postALU[1]] + self.arg2Str[
                self.postALU[1]] + self.arg3Str[self.postALU[1]] + ']')
        self.output.write("\n")
        self.output.write("Pre_MEM Queue:\n")
        for x in range(2):
            self.output.write("\tEntry " + str(x) + ":")
            if self.preMEM[x] != -1:
                self.output.write(
                    '\t' + '[' + self.opcode[self.preMEM[x]] + self.arg1Str[self.preMEM[x]] + self.arg2Str[
                        self.preMEM[x]] + self.arg3Str[self.preMEM[x]] + ']')
            self.output.write("\n")
        self.output.write("Post_MEM Queue:\n")
        self.output.write("\tEntry 0:")
        if sim.postMEM[1] != -1:
            self.output.write('\t' + '[' + self.opcode[self.postMEM[1]] + self.arg1Str[self.postMEM[1]] + self.arg2Str[
                self.postMEM[1]] + self.arg3Str[self.postMEM[1]] + ']')
        self.output.write("\n")
        self.output.write("\nRegisters")

        for y in range(0, 32, 8):
            self.output.write("\nR" + str(y).zfill(2) + ":")
            for z in range(0, 8):
                try:
                    self.output.write("\t" + str(main.getRegInt(self.R[y + z])))
                except IndexError:
                    break

        a = 0



        self.output.write("\n\nCache\n")
        for i in range(4):
            self.output.write("Set " + str(i) + ": LRU=" + str(self.cache.lruBit[i]) + "\n")
            self.output.write("\tEntry 0:[(" + str(self.cache.cacheSets[i][0][0]) + "," + str(
                self.cache.cacheSets[i][0][1]) + "," + str(self.cache.cacheSets[i][0][2]) + ")<" + str(
                self.cache.cacheSets[i][0][3]) + "," + str(self.cache.cacheSets[i][0][4]) + ">]"  "\n")
            self.output.write("\tEntry 1:[(" + str(self.cache.cacheSets[i][1][0]) + "," + str(
                self.cache.cacheSets[i][1][1]) + "," + str(self.cache.cacheSets[i][1][2]) + ")<" + str(
                self.cache.cacheSets[i][1][3]) + "," + str(self.cache.cacheSets[i][1][4]) + ">]"  "\n")

        self.output.write("\n")
        self.output.write("Data")

        try:
            tempAddress = self.address[self.numInstructions]
            for y in range(0, len(self.memory), 8):
                self.output.write("\n" + str(tempAddress) + ":")
                for z in range(0, 8):
                    if z == 0:
                        try:
                            self.output.write(
                                str(main.twos_comp(int(self.memory[a + z], 2), len(self.memory[a + z]))))

                        except (IndexError, TypeError):
                            # self.output.write("\t0")
                            pass

                    else:
                        try:
                            self.output.write("\t" + str(main.twos_comp(int(self.memory[a + z], 2), len(self.memory[a + z]))))

                        except (IndexError, TypeError):
                            #self.output.write("\t0")
                            pass
                a = a + 8
                tempAddress = tempAddress + 32
        except (IndexError):
            self.output.write("\n\n")







class Main:


    def run(self):

        inputFileNames = []
        outputFileNames = []

        for i in range(len(sys.argv)):
            if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
                inputFileNames.append(sys.argv[i + 1])
            elif (sys.argv[i] == '-o' and i < (len(sys.argv) - 1)):
                outputFileNames.append(sys.argv[i + 1])
        for i, names in enumerate(inputFileNames):
            self.run2(inputFileNames[i],outputFileNames[i]);


    def __init__(self):
        pass

    def get_bin(self, value, bits):
        if value < 0:
            value = (1 << bits) + value
        formatstring = '{:0%ib}' % bits
        return formatstring.format(value)

    def getRegInt(self, value):

        return int((self.twos_comp(int(value, 2), len(value))))

    def twos_comp(self, value, bits):
        #Credit: https://stackoverflow.com/questions/1604464/twos-complement-in-python
        if ((value & (1 << (bits - 1))) != 0):
            value = value - (1 << bits)
        return value


    def run2(self, inputFileName, outputFileName ):
        opcodeStr = []  # <type 'list'>: ['Invalid Instruction', 'ADDI', 'SW', 'Invalid Instruction', 'LW', 'BLTZ', 'SLL',...]
        validStr = []  # <type 'list'>: ['N', 'Y', 'Y', 'N', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y',...]
        instrSpaced = []  # <type 'list'>: ['0 01000 00000 00001 00000 00000 001010', '1 01000 00000 00001 00000 00000 001010',...]
        instr = []
        arg1 = []  # <type 'list'>: [0, 0, 0, 0, 0, 1, 1, 10, 10, 0, 3, 4, 152, 4, 10, 1, 0, 112, 0]
        arg2 = []  # <type 'list'>: [0, 1, 1, 0, 1, 0, 10, 3, 4, 5, 0, 5, 0, 5, 6, 1, 1, 0, 0]
        arg3 = []  # <type 'list'>: [0, 10, 264, 0, 264, 48, 2, 172, 216, 260, 8, 6, 0, 6, 172, -1, 264, 0, 0]
        dest = []
        src1 = []
        src2 = []
        arg1Str = []  # <type 'list'>: ['', '\tR1', '\tR1', '', '\tR1', '\tR1', '\tR10', '\tR3', '\tR4', .....]
        arg2Str = []  # <type 'list'>: ['', ', R0', ', 264', '', ', 264', ', #48', ', R1', ', 172', ', 216', ...]'
        arg3Str = []  # <type 'list'>: ['', ', #10', '(R0)', '', '(R0)', '', ', #2', '(R10)', '(R10)', '(R0)',...]
        mem = []  # <type 'list'>: [-1, -2, -3, 1, 2, 3, 0, 0, 5, -5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        data = []  # <type 'list'>: ['11111111111111111111111111111111', '11111111111111111111111111111110', ...]
        valid = []
        opcode = []

        rnMask = 0x3E0
        rmMask = 0x1F0000
        rdMask = 0x1F
        addrMask = 0x1FF000



        with open(inputFileName, 'r') as file:
            for line in file:
                instr.append(line.strip())
        for readInstr in instr:
            sizeOne = readInstr[:8]
            sizeTwo = readInstr[8:11]
            sizeThree = readInstr[11:16]
            sizeFour = readInstr[16:21]
            sizeFive = readInstr[21:26]
            sizeSix = readInstr[26:32]
            space = " "

            spaced = sizeOne + space + sizeTwo + space + sizeThree + space + sizeFour + space + sizeFive + space + sizeSix

            instrSpaced.append(spaced.strip())

        address = 96 #starting instruction address



        i = 0 #Loop counter
        for bitCode in instr:
            if bitCode[:6] == '000101':
                opcodeStr.append("B")
                arg1.append(int((self.twos_comp(int(bitCode[6:32], 2), len(bitCode[6:32])))))
                arg2.append('')
                arg3.append('')
                dest.append(-1)
                src1.append(-1)
                src2.append(-1)
                arg1Str.append('\t#' + str(arg1[i]))
                arg2Str.append('')
                arg3Str.append('')
            elif bitCode[:8] == '10110100':
                opcodeStr.append("CBZ")
                arg1.append(int((self.twos_comp(int(bitCode[8:27], 2), len(bitCode[8:27])))))
                arg2.append('')
                arg3.append((int(bitCode, base=2) & rdMask) >> 0)
                dest.append(-2)
                src1.append(arg3[i])
                src2.append(-2)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append('')
                arg3Str.append(', #' + str(arg1[i]))
            elif bitCode[:8] == '10110101':
                opcodeStr.append("CBNZ")
                arg1.append(int((self.twos_comp(int(bitCode[8:27], 2), len(bitCode[8:27])))))
                arg2.append('')
                arg3.append((int(bitCode, base=2) & rdMask) >> 0)
                dest.append(-3)
                src1.append(arg3[i])
                src2.append(-3)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append('')
                arg3Str.append(', #' + str(arg1[i]))
            elif bitCode[:9] == '110100101':
                opcodeStr.append("MOVZ")
                arg1.append((int(bitCode[27:32], base=2)))
                arg2.append((int(bitCode[9:11], base=2))*16)
                arg3.append((int(bitCode[11:27], base=2)))
                dest.append(arg1[i])
                src1.append(-4)
                src2.append(-4)
                arg1Str.append('\tR' + str(arg1[i]))
                arg2Str.append(', ' + str(arg3[i]))
                arg3Str.append(', LSL ' + str(arg2[i]))
            elif bitCode[:9] == '111100101':
                opcodeStr.append("MOVK")
                arg1.append((int(bitCode[27:32], base=2)))
                arg2.append((int(bitCode[9:11], base=2))*16)
                arg3.append((int(bitCode[11:27], base=2)))
                dest.append(arg1[i])
                src1.append(-5)
                src2.append(-5)
                arg1Str.append('\tR' + str(arg1[i]))
                arg2Str.append(', ' + str(arg3[i]))
                arg3Str.append(', LSL ' + str(arg2[i]))
            elif bitCode[:10] == '1001000100':
                opcodeStr.append("ADDI")
                arg1.append((int(bitCode, base=2) & rnMask) >> 5)
                arg2.append(int((self.twos_comp(int(bitCode[10:22], 2), len(bitCode[10:22])))))
                arg3.append((int(bitCode, base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(-6)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', R' + str(arg1[i]))
                arg3Str.append(', #' + str(arg2[i]))
            elif bitCode[:10] == '1101000100':
                opcodeStr.append("SUBI")
                arg1.append((int(bitCode, base=2) & rnMask) >> 5)
                arg2.append(int((self.twos_comp(int(bitCode[10:22], 2), len(bitCode[10:22])))))
                arg3.append((int(bitCode, base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(-7)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', R' + str(arg1[i]))
                arg3Str.append(', #' + str(arg2[i]))
            elif bitCode[:10] == '1111111011':
                opcodeStr.append("BREAK")
                arg1.append('')
                arg2.append('')
                arg3.append('')
                dest.append(-8)
                src1.append(-8)
                src2.append(-8)
                arg1Str.append('')
                arg2Str.append('')
                arg3Str.append('')
                stopmarker = i
                mem.append(address)
                address = address + 4
                break
            elif bitCode[:11] == '10001011000':
                opcodeStr.append("ADD")
                arg1.append((int(bitCode, base=2) & rnMask) >> 5)
                arg2.append((int(bitCode, base=2) & rmMask) >> 16)
                arg3.append((int(bitCode, base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', R' + str(arg1[i]))
                arg3Str.append(', R' + str(arg2[i]))
            elif bitCode[:11] == '11001011000':
                opcodeStr.append("SUB")
                arg1.append((int(bitCode, base=2) & rnMask) >> 5)
                arg2.append((int(bitCode, base=2) & rmMask) >> 16)
                arg3.append((int(bitCode, base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', R' + str(arg1[i]))
                arg3Str.append(', R' + str(arg2[i]))
            elif bitCode[:11] == '11010011011':
                opcodeStr.append("LSL")
                arg1.append((int(bitCode, base=2) & rnMask) >> 5)
                arg2.append((int(bitCode[16:22], base=2)))
                arg3.append((int(bitCode, base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(-11)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', R' + str(arg1[i]))
                arg3Str.append(', #' + str(arg2[i]))
            elif bitCode[:11] == '11010011010':
                opcodeStr.append("LSR")
                arg1.append((int(bitCode, base=2) & rnMask) >> 5)
                arg2.append((int(bitCode[16:22], base=2)))
                arg3.append((int(bitCode, base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(-12)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', R' + str(arg1[i]))
                arg3Str.append(', #' + str(arg2[i]))
            elif bitCode[:11] == '11010011100':
                opcodeStr.append("ASR")
                arg1.append((int(bitCode, base=2) & rnMask) >> 5)
                arg2.append((int(bitCode[16:22], base=2)))
                arg3.append((int(bitCode, base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(-13)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', R' + str(arg1[i]))
                arg3Str.append(', #' + str(arg2[i]))
            elif bitCode[:11] == '00000000000':
                opcodeStr.append("NOP")
                arg1.append('')
                arg2.append('')
                arg3.append('')
                dest.append(-14)
                src1.append(-14)
                src2.append(-14)
                arg1Str.append('')
                arg2Str.append('')
                arg3Str.append('')
            elif bitCode[:11] == '10001010000':
                opcodeStr.append("AND")
                arg1.append((int(bitCode, base=2) & rnMask) >> 5)
                arg2.append((int(bitCode, base=2) & rmMask) >> 16)
                arg3.append((int(bitCode, base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', R' + str(arg1[i]))
                arg3Str.append(', R' + str(arg2[i]))
            elif bitCode[:11] == '10101010000':
                opcodeStr.append("ORR")
                arg1.append((int(bitCode, base=2) & rnMask) >> 5)
                arg2.append((int(bitCode, base=2) & rmMask) >> 16)
                arg3.append((int(bitCode, base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', R' + str(arg1[i]))
                arg3Str.append(', R' + str(arg2[i]))
            elif bitCode[:11] == '11101010000':
                opcodeStr.append("EOR")
                arg1.append((int(bitCode, base=2) & rnMask) >> 5)
                arg2.append((int(bitCode, base=2) & rmMask) >> 16)
                arg3.append((int(bitCode, base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', R' + str(arg1[i]))
                arg3Str.append(', R' + str(arg2[i]))
            elif bitCode[:11] == '11111000010':
                opcodeStr.append("LDUR")
                arg1.append((int(bitCode, base=2) & rnMask) >> 5)
                arg2.append((int(bitCode, base=2) & addrMask) >> 12)
                arg3.append((int(bitCode, base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(-18)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', [R' + str(arg1[i]))
                arg3Str.append(', #' + str(arg2[i]) + ']')
            elif bitCode[:11] == '11111000000':
                opcodeStr.append("STUR")
                arg1.append((int(bitCode, base=2) & rnMask) >> 5)
                arg2.append((int(bitCode, base=2) & addrMask) >> 12)
                arg3.append((int(bitCode, base=2) & rdMask) >> 0)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(-18)
                arg1Str.append('\tR' + str(arg3[i]))
                arg2Str.append(', [R' + str(arg1[i]))
                arg3Str.append(', #' + str(arg2[i]) + ']')
            i = i + 1 #Iterate to next instruction
            mem.append(address)
            address = address + 4

        for bitCode in instr[(i+1):]: #This iterates through the memory instructions following the break instruction, using i as a marker to show where the memory 32bits start
            data.append(bitCode)
            opcodeStr.append("memoryData")
            mem.append(address)
            address = address + 4


        output = open(outputFileName + "_dis.txt", "w")

        memoryCount = 0
        lastBackspace = 0

        for x, op in enumerate(opcodeStr):
            if op == "memoryData":
                output.write(data[memoryCount] + '\t' + str(mem[x]) + '\t' + str(self.twos_comp(int(data[memoryCount],2), len(data[memoryCount]))))
                if (x < (len(opcodeStr) -1)):
                    output.write('\n') #So we don't get last line space at the end
                memoryCount = memoryCount + 1
                continue
            output.write(instrSpaced[x] + '\t' + str(mem[x]) + '\t' + op + arg1Str[x] + arg2Str[x] + arg3Str[x] + '\n')
        output.close()






        global sim


        sim = simClass(instr, opcodeStr, data, valid, mem, arg1, arg2, arg3, arg1Str, arg2Str, arg3Str, len(arg1), dest, src1, src2, outputFileName)

        sim.testFunction()

        print ("Saved simulator as " + outputFileName + "_out_pipeline.txt")




main = Main()
sim = None
main.run()

