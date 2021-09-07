import sys
import csv
import signal
import argparse
import signal
import time
from src.RacosFFNEvaluation import runRacos

printStatus= "Result: "
printTimeout= "\n\nTime taken : "

# Register an handler for the timeout
def handler(signum, frame):
    raise Exception("")#kill running :: Timeout occurs")


def runSingleInstance(onnxFile,vnnlibFile):
   #Variable Initialization
   startTime = time.time()

   onnxFileName = onnxFile.split('/')[-1]
   vnnFileName = vnnlibFile.split('/')[-1]

   print(f"\nNetwork model: {onnxFileName}")
   print(f"Property file: {vnnFileName}")

   while(1):
      status = runRacos(onnxFile,vnnlibFile)
      endTime = time.time()
      timeElapsed = endTime - startTime
      if (status == "violated"):
          resultStr = "violated"
          return resultStr

   resultStr = printStatus +"Timeout"
   return resultStr


#Main function
if __name__ == '__main__':

   onnxFile= sys.argv[1]
   vnnlibFile=sys.argv[2]
   timeout=sys.argv[3]
   # Register the signal function handler
   signal.signal(signal.SIGALRM, handler)

   # Define a timeout for "runSingleInstance"
   signal.alarm(int(timeout))

   '"runSingleInstance" will continue until any adversarial found or timeout occurs'
   'When timeout occurs codes written within exception will be executed'
   try:
       retStatus = runSingleInstance(onnxFile,vnnlibFile)
       print(retStatus)
   except Exception as exc:
       printStr = printStatus+"timeout"
       print(printStr)
       print(exc)

