import sys
import csv
import signal
import argparse
import signal
import time
from src.RacosFFNEvaluation import runRacos
from src.custom_property import *

printStatus= "Result: "
printTimeout= "\n\nTime taken : "

# Register an handler for the timeout
def handler(signum, frame):
    raise Exception("")#kill running :: Timeout occurs")


def runSingleInstance(onnxFile,vnnlibFile, validateFn):
   #Variable Initialization
   startTime = time.time()

   onnxFileName = onnxFile.split('/')[-1]
   vnnFileName = vnnlibFile.split('/')[-1]

   print(f"\nNetwork model: {onnxFileName}")
   print(f"Property file: {vnnFileName}")

   while(1):
      status = runRacos(onnxFile,vnnlibFile, validateFn)
      endTime = time.time()
      timeElapsed = endTime - startTime
      if (status == "violated"):
          resultStr = ""
          return resultStr

   resultStr = printStatus +"Timeout"
   return resultStr


#Main function
if __name__ == '__main__':

   onnxFile   = sys.argv[1]
   vnnlibFile = sys.argv[2]
   validateFn = globals()[sys.argv[3]]
   timeout    = sys.argv[4]
   # Register the signal function handler
   signal.signal(signal.SIGALRM, handler)

   # Define a timeout for "runSingleInstance"
   signal.alarm(int(timeout))

   '"runSingleInstance" will continue until any adversarial found or timeout occurs'
   'When timeout occurs codes written within exception will be executed'
   try:
       retStatus = runSingleInstance(onnxFile,vnnlibFile, validateFn)
       print(retStatus)
   except Exception as exc:
       printStr = printStatus+"timeout"
       print(printStr)
       print(exc)

