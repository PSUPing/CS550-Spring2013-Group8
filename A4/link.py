import programext
memFile = "simulator/mem.txt"
# link method that produces absolute (i.e. hard coded addresses) code, corresponding to the translated symbolic RAL code, that can be simulated on the RAM simulator
def linker(ralToLink, memObj,memorySize) :
	linkedCode = ralToLink

	f = open(memFile, "w+")
	# switch constant id and constant value in memObj
	constants_dict = dict(zip(memObj.constants.values(), memObj.constants.keys()))
	# sort by correct order of constants:
	# - map "C1"->"1", "C10"->"10", "C134"->"134"
	# - sort in correct order: 1,10,134
	sorted_constants_keys = sorted(map(lambda x: x[1:], constants_dict.keys()), key=int) 
	mem = [constants_dict["C" + i] for i in sorted_constants_keys] 
	# add all the variables and temps, set up as 0
	mem += [0 for i in range(memObj.tCount + memObj.cCount)]
	#print to mem file
	mem.insert(0,0)#insert fp,sp and scratch
	mem.insert(0,0)
	mem.insert(0,0)
	mem.insert(0,0)
	mem.insert(0,0)
	mem.insert(0,0)
	mem.insert(0,0)
	for i in range(memorySize):
		if i<len(mem):
			f.write(str(i+1) + " " + str(mem[i]) + " ;\n")
		else:
			f.write(str(i+1) + " " + str(0) + " ;\n")
			
	f.close()

	if "SP" in linkedCode : 
		linkedCode = linkedCode.replace("SP", str(1))

	scratchCount = 5

	# We only have 5 scratch variables at most
	for x in range(1, 5) : 
		if "S" + str(x) in linkedCode : 
			linkedCode = linkedCode.replace("S" + str(x), str(x + 2))
	
	if "FP" in linkedCode : 
		linkedCode = linkedCode.replace("FP", str(2))

	# Constants, variables and temps all use a 0 based index and
	# therefore will need 1 added to the index to enter the correct address
	for value, consID in memObj.constants.items() : 
		currCons = int(consID.replace('C', '')) + 3 + scratchCount
		linkedCode = linkedCode.replace(consID, str(currCons))

	# Memory is organized in the order of constants, variables, then temps
	# Therefore, the address will be the number of constants added to the 
	# variable index + 1 (per note above

	#Should never happen
	'''for value, varID in memObj.nt.items() : 
		currVar = int(varID.replace('V', '')) + 1 + memObj.cCount + spCount + scratchCount + fpCount
		linkedCode = linkedCode.replace(varID, str(currVar))'''
		
	# Same concept as the previous for loop, but add in the variables too

	#should never happen
	'''for temp in range(0, memObj.tCount) :
		currTemp = temp + 1 + memObj.cCount + memObj.nCount + spCount + scratchCount + fpCount
		linkedCode = linkedCode.replace('T' + str(temp), str(currTemp))'''
	
	# Each line needs to be counted
	instructions = linkedCode.split('\n')

	# Variables for setting locations
	lineNum = 0
	tempLoc = 0
	locations = {}

	# Loop through all the lines and look for the location identifiers
	for i in range(len(instructions)) :
		cmd = instructions[i]
		lineNum += 1;
		if instructions[i].find(':') > -1 : 
			tempLoc = instructions[i][1:instructions[i].find(':')]
			locations[str('L' + tempLoc)] = lineNum
			instructions[i]=cmd[(cmd.index(':')+1):].lstrip()

	linkedCode = '\n'.join(instructions)

	# For all the locations, replace the various jump commands with line numbers
	for locID, value in locations.items() : 
		linkedCode = linkedCode.replace('JMN ' + locID, 'JMN ' + str(value))
		linkedCode = linkedCode.replace('JMP ' + locID, 'JMP ' + str(value))
		linkedCode = linkedCode.replace('JMZ ' + locID, 'JMZ ' + str(value))
		linkedCode = linkedCode.replace('CAL ' + locID, 'CAL ' + str(value))

	return linkedCode
