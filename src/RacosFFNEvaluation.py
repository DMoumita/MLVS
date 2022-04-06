from src.Racos import RacosOptimization
from src.Components import Dimension
from src.racos_vnnlib import readVnnlib, getIoNodes
from src.racos_util import removeUnusedInitializers, findObjectiveFuncionType
from src.ObjectiveFunction import *

import src.custom_property 
import numpy as np
import onnx
import time
import onnxruntime as rt
import sys

# parameters
SampleSize = 20             # the instance number of sampling in an iteration
MaxIteration = 100          # the number of iterations
Budget = 2000               # budget in online style
PositiveNum = 1             # the set size of PosPop
RandProbability = 0.99      # the probability of sample in model
UncertainBits = 1           # the dimension size that is sampled randomly

#dictionary of custom function names defining the input function names
#funcdict = {
#  'prop_default': prop_default,
#  'prop_y10' : prop_y10,
#  'prop_y10_0' : prop_y10_0
#}

def ResultAnalysis(res, top):
    res.sort()
    top_k = []
    for i in range(top):
        top_k.append(res[i])
    mean_r = np.mean(top_k)
    std_r = np.std(top_k)
    #print (mean_r, '#', std_r) 
    return

def runRacos(onnxFilename, vnnlibFilename, validateFn):
    startTime = time.time()
    repeat = 200
    results = []
    regs = []
    onnxModel = onnx.load(onnxFilename)
    onnx.checker.check_model(onnxModel, full_check=True)
    onnxModel = removeUnusedInitializers(onnxModel)
    inp, out, inpDtype = getIoNodes(onnxModel)
    inpShape = tuple(d.dim_value if d.dim_value != 0 else 1 for d in inp.type.tensor_type.shape.dim)
    outShape = tuple(d.dim_value if d.dim_value != 0 else 1 for d in out.type.tensor_type.shape.dim)
    numInputs = 1
    numOutputs = 1

    #Number of inputs
    for n in inpShape:
       numInputs *= n

    #Number of outputs
    for n in outShape:
       numOutputs *= n


    #parsing vnnlib file, get a list of input ranges and property matrix
    boxSpecList = readVnnlib(vnnlibFilename, numInputs, numOutputs)


    #find target output label and objective type
    targetAndType = findObjectiveFuncionType(boxSpecList[0][1],numOutputs)

    for i in range (len(boxSpecList)):
       boxSpec = boxSpecList[i]
       inRanges = boxSpec[0]
       specList = boxSpec[1]
       DimSize = numInputs
       #print("TARGET and OBJTYPE:",targetAndType)

       dim = Dimension()
       dim.setDimensionSize(DimSize)
       for i in range(DimSize):
          dim.setRegion(i, inRanges[i], True)

       for i in range(repeat):
          racos = RacosOptimization(dim, onnxModel,inpDtype, inpShape, specList, targetAndType[0], targetAndType[1]) #FFN 

          # call online version RACOS
          # racos.OnlineTurnOn()
          # racos.ContinueOpt(Ackley, SampleSize, Budget, PositiveNum, RandProbability, UncertainBits)
          ret = racos.ContinueOpt(nneval, SampleSize, MaxIteration, PositiveNum, RandProbability, UncertainBits, validateFn) #FFN

          if (ret == 1):
             retStmt = "violated"
             return retStmt
             
          results.append(racos.getOptimal().getFitness())

    retStmt = "Result: timeout"
    return retStmt

