from src.Racos import RacosOptimization
from src.Components import Dimension
from src.ObjectiveFunction import Sphere
from src.ObjectiveFunction import Ackley
from src.ObjectiveFunction import FFN
from src.ObjectiveFunction import SetCover
from src.ObjectiveFunction import MixedFunction
from src.racos_vnnlib import readVnnlib, getIoNodes
from src.racos_util import removeUnusedInitializers, findObjectiveFuncionType

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
          #print (i, ':--------------------------------------------------------------')
          racos = RacosOptimization(dim, onnxModel,inpDtype, inpShape, specList, targetAndType[0], targetAndType[1]) #FFN 

          # call online version RACOS
          # racos.OnlineTurnOn()
          # racos.ContinueOpt(Ackley, SampleSize, Budget, PositiveNum, RandProbability, UncertainBits)

          ret = racos.ContinueOpt(FFN, SampleSize, MaxIteration, PositiveNum, RandProbability, UncertainBits, validateFn) #FFN
        
          if (ret == 1):
             endTime = time.time()
             timeElapsed = endTime - startTime
             retStmt = "violated"
             return retStmt
          results.append(racos.getOptimal().getFitness())

    retStmt = "Result: unknown "
    retStmt = "Result: timeout"
    return retStmt


# continuous optimization
#Main function
if __name__ == '__main__':

  if True:
  
    # dimension setting
    #DimSize = 100
    #regs.append(0.0)
    #regs.append(1.0)

    #dim = Dimension()
    #dim.setDimensionSize(DimSize)
    #for i in range(DimSize):
    #    dim.setRegion(i, regs, True)

   #FFN starts

    onnxFilename = sys.argv[1]
    vnnlibFilename =  sys.argv[2]
    rStr = runRacos(onnxFilename,vnnlibFilename)
    print(rStr)

   #FFN ends

  # discrete optimization
  if False:

    # dimension setting
    DimSize = 20
    regs = []
    regs.append(0)
    regs.append(1)

    dim = Dimension()
    dim.setDimensionSize(DimSize)
    for i in range(DimSize):
        dim.setRegion(i, regs, False)

    racos = RacosOptimization(dim)

    # call online version RACOS
    #racos.OnlineTurnOn()
    #racos.DiscreteOpt(SetCover, SampleSize, Budget, PositiveNum, RandProbability, UncertainBits)

    ret = racos.DiscreteOpt(SetCover, SampleSize, MaxIteration, PositiveNum, RandProbability, UncertainBits)

    #print (racos.getOptimal().getFeatures())
    #print (racos.getOptimal().getFitness())

  # mixed optimization
  if False:

    # dimension setting
    DimSize = 10
    regs1 = []
    regs1.append(-1)
    regs1.append(1)
    regs2 = []
    regs2.append(0)
    regs2.append(100)

    dim = Dimension()
    dim.setDimensionSize(DimSize)
    for i in range(DimSize):
        if i%2 == 0:
            dim.setRegion(i, regs1, True)
        else:
            dim.setRegion(i, regs2, False)

    racos = RacosOptimization(dim)

    # call online version RACOS
    #racos.OnlineTurnOn()
    #racos.MixOpt(MixedFunction, SampleSize, Budget, PositiveNum, RandProbability, UncertainBits)

    ret = racos.MixOpt(MixedFunction, SampleSize, MaxIteration, PositiveNum, RandProbability, UncertainBits)

    #print (racos.getOptimal().getFeatures())
    #print (racos.getOptimal().getFitness())

