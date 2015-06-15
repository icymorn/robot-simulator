import cv2
import numpy as np
import os
import pickle
from math import pi, fabs
import random
import time

FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing
FLANN_INDEX_LSH    = 6

path = './data/'
dirs = os.listdir(path)

typeNum    = len(dirs)
dictionary = {}
detector = cv2.FeatureDetector_create("SIFT")
extractor = cv2.DescriptorExtractor_create("SIFT")

bowTrain = cv2.BOWKMeansTrainer(3)
vocFile = './vocabulary.data'
classifierFile = './classifier.xml'

if os.path.isfile(vocFile):
    file = open(vocFile, 'rb')
    vocdata = pickle.load(file)
    voc = vocdata['vocabulary']
    typeList = vocdata['list']
else:
    typeList = []
    for types in dirs:
        typePath = os.path.join(path, types)
        typeList.append(types)
        for typeImage in os.listdir(typePath):
            file = os.path.join(path, types, typeImage)
            img = cv2.imread(file, 0)
            skp = detector.detect(img)
            dsp = extractor.compute(img, skp)[1]
            bowTrain.add(dsp)
    voc = bowTrain.cluster()

flann_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
matcher = cv2.FlannBasedMatcher(flann_params, {})
bowExtractor = cv2.BOWImgDescriptorExtractor(extractor, matcher)
bowExtractor.setVocabulary( voc )
pickle.dump( {"vocabulary": voc, "list": typeList}, open( "vocabulary.data", "wb" ) )
print "bow vocab", np.shape(voc)
print "type", typeList

if os.path.isfile(classifierFile):
# if False:
    svm = cv2.SVM()
    svm.load(classifierFile)
else:
    traindata, trainlabels = [],[]
    i = 0
    print "svm training..."
    for types in dirs:
        typePath = os.path.join(path, types)
        for typeImage in os.listdir(typePath):
            file = os.path.join(path, types, typeImage)
            img = cv2.imread(file, 0)
            skp = detector.detect(img)
            dsp = bowExtractor.compute(img, skp)
            traindata.extend(dsp)
            trainlabels.append(i)
        print i, ':', types
        i += 1

    print "svm items", len(traindata), len(traindata[0])

    svm = cv2.SVM()
    params = dict( kernel_type = cv2.SVM_POLY,
                   svm_type = cv2.SVM_C_SVC,
                   degree = 3)
    svm.train(np.array(traindata), np.array(trainlabels), params = params)
    svm.save(classifierFile)

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(1,1))
fgbg = cv2.BackgroundSubtractorMOG()
current  = time.time()
lasttime = current

textLastTime = 1
lastDisplayTime = 0
typetext = "unknown object"
rotate = 0
arm_rotate_diff = 0

catch_history = []

while True:
    _, frame = cap.read()
    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    contours, hierarchy = cv2.findContours(fgmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    lasttime = current
    current  = time.time()
    
    maxcontour = None
    maxarea    = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > maxarea:
            maxarea = area
            maxcontour = contour

    if maxcontour is not None:
        x,y,w,h = cv2.boundingRect(maxcontour)
        if current - lastDisplayTime > textLastTime:
            testimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            testdsp = bowExtractor.compute(testimg, detector.detect(testimg))
            if testdsp is not None:
                lastDisplayTime = current
                predict = svm.predict(testdsp)
                typetext = typeList[int(predict)]

        cv2.putText(frame, typetext, (x, y + 23), font, 1.1,(0,0,255),2)
            
        rect = cv2.minAreaRect(maxcontour)
        box = cv2.cv.BoxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame,[box],0,(0,0,255),2)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        if rect[1][0] < rect[1][1]:
            rotate = - 90 - rect[2]
            cv2.putText(frame, "w%.0f h%.0f r%.0f" % (rect[1][1], rect[1][0], - 90 - rect[2]), (int(rect[0][0]), int(rect[0][1])), font, 1.05,(0,0,255),2)     
        else:
            rotate = -rect[2]
            cv2.putText(frame, "w%.0f h%.0f r%.0f" % (rect[1][0], rect[1][1], -rect[2]), (int(rect[0][0]), int(rect[0][1])), font, 1.05,(0,0,255),2)

    cv2.imshow('frame',frame)

    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break
    elif k == 13:
        print "==============="
        print "detect: ", typetext
        print "rotate: ", rotate
        accept = raw_input("accpet(y/n) ?: ")
        if accept == "y":
            if arm_rotate_diff > 90:
                arm_rotate_diff = 0
            r1 = rotate + arm_rotate_diff
            r2 = rotate - arm_rotate_diff
            if fabs(r1) > fabs(r2):
                arm_rotate = r2
            else:
                arm_rotate = r1
            print "arm_rotate: ", arm_rotate
            print "diff: ", arm_rotate_diff
            arm_rotate_diff += 10

            # do grasp
            # get value
            c = raw_input("does it caught? (1 for yes, 0 for no): ")
            if c == "0":
                catch_history.append((typetext, arm_rotate_diff, False))
            else:
                catch_history.append((typetext, arm_rotate_diff, True))
            # caught = True if random.randint(1, 10) > 8 else False
            # print "caught: ", caught

        print catch_history