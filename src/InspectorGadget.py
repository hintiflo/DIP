import os
import re
import shutil
import time

# TODO: difference List fuer noResults
# TODO: eigenltiche Analyse direkt aus diesem py heraus starten
# TODO: Ordnerstruktur ueberarbeiten, am ende des Codes aufraeumen
# TODO: yolo nachtrainieren
# TODO: Praesentationsfolien
# TODO: %te bzw Statkstik der Analyse printen
# TODO: 

# python yolov5-master/detect.py --weights ../smodel/modelV2.pt --source ../img/All --save-txt --max-det 1 --nosave --name ../../../runs/exp --imgsz 416


start = time.perf_counter_ns()
os.system("python yolov5-master/detect.py --weights ../smodel/modelV3.pt --source ../img/All --save-txt --max-det 1 --nosave --name res --imgsz 308 --project ../ ")
end = time.perf_counter_ns()

print("elapsed ms: ")
print( (end - start)/1000000)


resultPath = "../res/labels"
allPath = "../img/All"

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
		result = (resIndex[resultNum] + ":\t" + resFn )

		if( "correct" == resIndex[resultNum]):	# good Indi
			goodResults.append(result.replace(".txt", ".jpg"))
		else:	# bad Indi
			badResults.append(result.replace(".txt", ".jpg"))
		
		resFile.close()
		# print(resFn)


jpgList = [w.replace(".txt", ".jpg") for w in txtList]

'''	resort images section:
'''
if(len(jpgList) > 0):
	goodPath = "../output/good"
	badPath = "../output/bad"
	noResPath = "../output/noResult"
	os.makedirs("../output", exist_ok = True)
	os.makedirs(goodPath, exist_ok = True)
	os.makedirs(badPath, exist_ok = True)
	os.makedirs(noResPath, exist_ok = True)
	
	# print(goodPath, badPath, noResPath)
	
		# os.rename( , ) ... nope, kopieren, NICHT verschieben!
	
	
	for line in goodResults:
		# print(line)
		shutil.copy(allPath + "/" + line.split("\t")[1], goodPath + "/" +line.split("\t")[1])
	# print("\n bad Indies:")

	for line in badResults:
		# print(line)
		shutil.copy(allPath + "/" + line.split("\t")[1], badPath + "/" +line.split("\t")[1])

	noResults = set(picList).difference( set(jpgList))
	for line in noResults:
		# print(line)
		shutil.copy(allPath + "/" + line, noResPath + "/" + line)

	print("input consists of ", len(picList), "Images, with \n ", len(jpgList), "Results: \n ",
	len(goodResults), " good Indies, and\n ", 
	len(badResults), " bad indies, and\n ",
	len(noResults), " no Results found")
	
else:
	print("input consists of ", len(picList), "Images, with no Results found")

shutil.rmtree("../res")