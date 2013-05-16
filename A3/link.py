import programext

# link method that produces absolute (i.e. hard coded addresses) code, corresponding to the translated symbolic RAL code, that can be simulated on the RAM simulator
def linker(ralToLink, memObj) :
	linkedCode = ralToLink
	
	# Constants, variables and temps all use a 0 based index and
	# therefore will need 1 added to the index to enter the correct address
	for value, consID in memObj.constants.items() : 
		currCons = int(consID.replace('C', '')) + 1
		linkedCode = linkedCode.replace(consID, str(currCons))

	# Memory is organized in the order of constants, variables, then temps
	# Therefore, the address will be the number of constants added to the 
	# variable index + 1 (per note above
	for value, varID in memObj.nt.items() : 
		currVar = int(varID.replace('V', '')) + 1 + memObj.cCount
		linkedCode = linkedCode.replace(varID, str(currVar))
		
	# Same concept as the previous for loop, but add in the variables too
	for temp in range(0, memObj.tCount) :
		currTemp = temp + 1 + memObj.cCount + memObj.nCount
		linkedCode = linkedCode.replace('T' + str(temp), str(currTemp))
	
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
		if 'L' + str(tempLoc) + ':' in cmd : 
			locations['L' + str(tempLoc)] = lineNum
			tempLoc += 1
			instructions[i]=cmd[(cmd.index(':')+1):].lstrip()

	linkedCode = '\n'.join(instructions)
	# For all the locations, replace the various jump commands with line numbers
	for locID, value in locations.items() : 
		linkedCode = linkedCode.replace('JMN ' + locID, 'JMN ' + str(value))
		linkedCode = linkedCode.replace('JMP ' + locID, 'JMP ' + str(value))
		linkedCode = linkedCode.replace('JMZ ' + locID, 'JMZ ' + str(value))

	return linkedCode
