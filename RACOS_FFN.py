import sys
import csv
import signal
import argparse
import time
import pdb

from src.RacosFFNEvaluation import runRacos
import src.custom_property

printStatus= "Result: "
printTimeout= "\n\nTime taken : "

# Register an handler for the timeout
def handler(signum, frame):
    raise Exception("timeout signal")


def runSingleInstance(onnxFile,vnnlibFile,validateFn):
   #Variable Initialization
   startTime = time.time()

   onnxFileName = onnxFile.split('/')[-1]
   vnnFileName = vnnlibFile.split('/')[-1]

   print(f"\nNetwork model: {onnxFileName}")
   print(f"Property file: {vnnFileName}")
   print(f"custom function: {validateFn}")
   
   while True:
      status = runRacos(onnxFile,vnnlibFile,validateFn)
      print("status:",status)
      endTime = time.time()
      timeElapsed = endTime - startTime
      if (status == "violated"):
          resultStr = "ce found"
          return resultStr

   resultStr = printStatus +"Timeout"
   return resultStr


#Main function
if __name__ == '__main__':

   #pdb.set_trace() 
   # Initialize parser
   parser = argparse.ArgumentParser(description = 'Search for unsafe input(s) to a neural network.')
   
   # Adding optional argument
   parser.add_argument("-m", "--model", required = True, help = "The neural network model file in .onnx format")
   parser.add_argument("-p", "--property", required = True, help = "The property file in vnnlib format")
   parser.add_argument("-c", "--custom_property", required = True, default = "prop_default", help="Custom constraint on inputs, specified by the custom property function name")
   parser.add_argument("-d", "--dump_ces", required = True, default = False, help="To be set as True for enabling. Dumps the unsafe inputs in ce.csv file when enabled. Disabled by default.")
   parser.add_argument("--timeout", required = False, type=int, default = 60, help = "The timeout in seconds. The default is 60 seconds.")
   
   parser.parse_args()
 
   # Read arguments from command line
   args = parser.parse_args()
 
   if args.model:
      onnxFile = args.model
   if args.property:
      vnnlibFile = args.property
   if args.custom_property:
      validateFn = args.custom_property
   if args.dump_ces:
      dumpCe = args.dump_ces
   if args.timeout:
      timeout = args.timeout 

   #initialize the list of custom properties, and the dump_ces argument in global vars
   src.custom_property.init(dumpCe)

   # If ce dumping option is enabled, prepare the ce file
    
   if dumpCe == "True":
       ce_filename = "ce.csv" # file to collect the counterexamples
       fields = ["x0","x1","x2","x3","x4","y0","y1","y2","y3","y4"]
       with open(ce_filename,'w') as csvfile:
          csvwriter = csv.writer(csvfile)
          csvwriter.writerow(fields)
       csvfile.close()
    # adds the fields to the csv file

   # Register the signal function handler
   signal.signal(signal.SIGALRM, handler)

   # Define a timeout for "runSingleInstance" 
   signal.alarm(timeout)
   '"runSingleInstance" will continue until any adversarial found or timeout occurs'
   'When timeout occurs codes written within exception will be executed'
   try:
       retStatus = runSingleInstance(onnxFile,vnnlibFile,validateFn)
       print(retStatus)
       if (args.dump_ces == True):# when ce dumping is enabled
          print("The counterexample(s) are copied to ce.csv file")
       
   except Exception:
       printStr = printStatus+"timeout"
       print(printStr)
       if dumpCe == "True":
          print("ce inputs, if found any, dumped into ce.csv file")

