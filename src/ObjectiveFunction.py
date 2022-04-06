import math
import time
import onnx
import onnxruntime as rt
from src.racos_util import predictWithOnnxruntime, propCheck
import numpy as np

import src.custom_property


# FFN evaluation for continue optimization
def nneval(onnxModel,inVals,inpDtype, inpShape, inpSpecs, target, objType, valFn):
   flattenOrder='C'
   inputs = np.array(inVals, dtype=inpDtype)
   inputs = inputs.reshape(inpShape, order=flattenOrder) # check if reshape order is correct
   assert inputs.shape == inpShape

   output = predictWithOnnxruntime(onnxModel, inputs)
   flatOut = output.flatten(flattenOrder) # check order, 'C' for row major order

   # objType = 0 -> maximization
   # objType = 1 -> minimization

   retVal=propCheck(inVals,inpSpecs,flatOut)
   #if unsafe input, then check additional constraints.
   if (retVal==1):
      retVal = src.custom_property.funcdict[valFn](inVals, flatOut)
      
   if (objType == 0):
      flatOut[target] = -flatOut[target]

   return retVal, flatOut[target]

