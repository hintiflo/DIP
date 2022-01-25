import os
import re
import shutil
import time


start = time.perf_counter_ns()
os.system("python yolov5-master/detect.py --weights ../smodel/modelV3.pt --source ../img/All --save-txt --max-det 1 --nosave --name res --imgsz 416 --project ../ ")
end = time.perf_counter_ns()

print("time total: \n\t", round((end - start)/10**9, 2), "s")


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

	print("\ninput consists of ", len(picList), "Images, with ", len(jpgList), "Results: \n\t ",
	len(goodResults), " good Indies, and\n\t ", 
	len(badResults), " bad indies, and\n\t ",
	len(noResults), " no Results found")
	
else:
	print("input consists of ", len(picList), "Images, with no Results found")

shutil.rmtree("../res")