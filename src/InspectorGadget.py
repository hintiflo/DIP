import os
import re
import shutil

# TODO: difference List fuer noResults
# TODO: eigenltiche Analyse direkt aus diesem py heraus starten
# TODO: Ordnerstruktur ueberarbeiten, am ende des Codes aufraeumen
# TODO: yolo nachtrainieren
# TODO: Praesentationsfolien
# TODO: %te bzw Statkstik der Analyse printen
# TODO: 


resultPath = "../res/labels"
allPath = "../img/All"
# results = []

resIndex = {	0 : "Combo", 
				1 : "NoArm", 
				2 : "NoFace", 
				3 : "NoHand", 
				4 : "NoHat", 
				5 : "NoHead", 
				6 : "NoLeg", 
				7 : "NoPrint", 
				8 : "correct"
			}

# for i in range(len(resIndex)):
	# print(resIndex[i])

goodResults = []
badResults = []


txtList = os.listdir(resultPath)
picList = os.listdir(allPath)

for resFn in txtList:
	if ".txt" in resFn:
		resFile = open(resultPath + '/' + resFn, 'r')
		result = resFile.read()
		result = result.replace("\n","")
		resultNum = int(result[0])
		result = (resIndex[resultNum] + ":\t" + resFn.replace(".txt", ".jpg") )

		if( "correct" == resIndex[resultNum]):	# good Indi
			goodResults.append(result)
		else:	# bad Indi
			badResults.append(result)
		
		resFile.close()
		# print(resFn)

'''	resort images section:
'''
if(len(txtList) > 0):
	goodPath = "../output/good"
	badPath = "../output/bad"
	noResPath = "../output/noResult"
	os.makedirs("../output", exist_ok = True)
	os.makedirs(goodPath, exist_ok = True)
	os.makedirs(badPath, exist_ok = True)
	os.makedirs(noResPath, exist_ok = True)
	
	# print(goodPath, badPath, noResPath)
	
		# os.rename( , ) ... nope, kopieren, NICHT verschieben!
	
	print("input consists of ", len(picList), "Images, with ", len(txtList), "Results: \n good Indies:")
	for line in goodResults:
		print(line)
		shutil.copy(allPath + "/" + line.split("\t")[1], goodPath + "/" +line.split("\t")[1])
	print("\n bad Indies:")

	for line in badResults:
		print(line)
		shutil.copy(allPath + "/" + line.split("\t")[1], badPath + "/" +line.split("\t")[1])
	
	noResults = set(picList).difference(txtList)
	print(len(noResults))

else:
	print("input consists of ", len(picList), "Images, with no Results found")

# shutil.rmtree("../res")