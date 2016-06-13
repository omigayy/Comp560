from PIL import Image
from svmutil import *
from os import listdir
from os.path import isfile, join
import random


# ==================== a =======================
def readImg(fileName):
    img = Image.open(fileName)
    return img
# =============== problem one ==================
def tinyImage(image):
    size = 32,32,3
    image.thumbnail(size)
    imgValue = list(image.getdata())
    if image.mode == "RGB":
        imgValue = [x for sets in imgValue for x in sets]
    return imgValue
# =============== problem two ==================
def colorHistogram(image):
    rBin = [0] * 8
    gBin = [0] * 8
    bBin = [0] * 8
    imgValue = list(image.getdata())
    if image.mode == "L":
        for x in imgValue:
            rBin[x/32] += 1
            gBin[x/32] += 1
            bBin[x/32] += 1
    elif image.mode == "RGB":
        for x in imgValue:
            rBin[x[0]/32] += 1
            gBin[x[1]/32] += 1
            bBin[x[2]/32] += 1
    return rBin+gBin+bBin
# ==============================================

# ==================== b =======================
def setLinearParam():
    param = svm_parameter('-t 0 -c 5 -b 1')
    return param

def readDataSVM(y,x):
    prob = svm_problem(y,x)
    return prob

def buildModel(prob,param):
    model = svm_train(prob,param)
    return model

def main():
    img_val = []
    path = "images"
    fileLst = [f for f in listdir(path) if isfile(join(path, f))]
    fileLst.remove('.DS_Store')
    #randLst = random.sample(range(len(fileLst)), int(len(fileLst)*0.35))
    randNum = random.sample(xrange(len(fileLst)), len(fileLst))
    trainLst = map(lambda x: randNum[x], range(int(len(fileLst)*0.35)))
    holdLst = map(lambda x: randNum[x], range(int(len(fileLst)*0.35),int(len(fileLst)*0.7)))
    testLst = map(lambda x: randNum[x], range(int(len(fileLst)*0.7),int(len(fileLst))))
    trainLst = map(lambda x: fileLst[x],trainLst)
    for i in trainLst:
        fileName = "images/" + i
        img = readImg(fileName)
        img_val.append(tinyImage(img))

    hoboLabel = map(lambda x:1 if x.__contains__("hobo") else -1,trainLst)
    clutchLabel = map(lambda x:1 if x.__contains__("clutch") else -1,trainLst)
    flatsLabel = map(lambda x:1 if x.__contains__("flats") else -1,trainLst)
    pumpsLabel = map(lambda x:1 if x.__contains__("pumps") else -1,trainLst)
    param = setLinearParam()
    hoboProb = readDataSVM(hoboLabel,img_val)
    hoboModel = buildModel(hoboProb,param)
    clutchProb = readDataSVM(clutchLabel,img_val)
    clutchModel = buildModel(clutchProb, param)
    flatProb = readDataSVM(flatsLabel,img_val)
    flatModel = buildModel(flatProb,param)
    pumpsProb = readDataSVM(pumpsLabel,img_val)
    pumpsModel = buildModel(pumpsProb,param)

    # print "===================="
    # print param
    # print "===================="

    # svm_save_model('hoboM', hoboModel)
    # svm_save_model('clutchM', clutchModel)
    # svm_save_model('flatM', flatModel)
    # svm_save_model('pumpsM', pumpsModel)

    # with open("lst",'w') as file:
    #     for item in testLst:
    #         file.write("{}\n".format(item))

# #====== test part here ======
#     hoboModel = svm_load_model('hoboM')
#     cM = svm_load_model('clutchM')
#     fM = svm_load_model('flatM')
#     pM = svm_load_model('pumpsM')
#
#     with open('lst') as f:
#         lines = f.read().splitlines()
#     testLst = map(lambda x:int(x),lines)
    testLst = map(lambda x: fileLst[x],testLst)
    trueHoboLabel = map(lambda x:1 if x.__contains__("hobo") else -1,testLst)
    trueCLabel = map(lambda x:1 if x.__contains__("clutch") else -1,testLst)
    trueFLabel = map(lambda x:1 if x.__contains__("flats") else -1,testLst)
    truePLabel = map(lambda x:1 if x.__contains__("pumps") else -1,testLst)
    # f.close()

    trueLabel = []
    for i in range(len(trueHoboLabel)):
        if trueHoboLabel[i] == 1:
            trueLabel.append(1)
        if trueCLabel[i] == 1:
            trueLabel.append(2)
        if trueFLabel[i] == 1:
            trueLabel.append(3)
        if truePLabel[i] == 1:
            trueLabel.append(4)
    # print trueLabel
    # with open("truelabel",'w') as file:
    #     for item in trueLabel:
    #         file.write("{}\n".format(item))
    # with open('truelabel') as f2:
    #     labels = f2.read().splitlines()
    # trueLabel = map(lambda x:int(x),labels)

    testVal = []
    for i in testLst:
        fileName = "images/" + i
        img = readImg(fileName)
        testVal.append(tinyImage(img))
    hobo_labels, hobo_acc, hobo_vals = svm_predict(trueHoboLabel,testVal,hoboModel)
    print "hobo: ", hobo_labels
    print "hobo_val: " , hobo_vals
    print trueHoboLabel
    print "=================================="
    c_labels, c_acc, c_vals = svm_predict(trueCLabel,testVal,clutchModel)
    print "c: ", c_labels
    print "c_val: " , c_vals
    print trueCLabel
    print "=================================="
    f_labels, f_acc, f_vals = svm_predict(trueFLabel,testVal,flatModel)
    print "f: ", f_labels
    print "f_val: " , f_vals
    print trueFLabel
    print "=================================="
    p_labels, p_acc, p_vals = svm_predict(truePLabel,testVal,pumpsModel)
    print "p: ", p_labels
    print "p_val: " , p_vals
    print truePLabel
    print "============= argmax ==============="
    argmaxResult = []
    tmp = [0]*4
    for i in range(len(hobo_vals)):
        tmp[0] = hobo_vals[i][0]
        tmp[1] = c_vals[i][0]
        tmp[2] = f_vals[i][0]
        tmp[3] = p_vals[i][0]
        argmaxResult.append(tmp.index(max(tmp))+1)
        # if max(tmp)>0:
        #     argmaxResult.append(tmp.index(max(tmp))+1)
        # else:
        #     argmaxResult.append(0)
    print "predict result: " , argmaxResult
    print "true value:     ",trueLabel
    ACC, MSE, SCC = evaluations(trueLabel, argmaxResult)
    print "accuracy of argmax: " , ACC

    hcount = [0] * 4
    cc = [0] * 4
    fc = [0] * 4
    pc = [0] * 4
    for i in range(len(argmaxResult)):
        if trueLabel[i] == 1:
            hcount[argmaxResult[i]-1] += 1
        if trueLabel[i] == 2:
            cc[argmaxResult[i]-1] += 1
        if trueLabel[i] == 3:
            fc[argmaxResult[i]-1] += 1
        if trueLabel[i] == 4:
            pc[argmaxResult[i]-1] += 1
    print hcount,cc,fc,pc



if __name__ == '__main__':
    main()


