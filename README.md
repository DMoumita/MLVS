MLVS with custom property
-----------------------------------------------

MLVS verifies a given neural network for a given property specification

The property is specified in two parts:

A vnnlib file for the initial ranges, a custom function in the src/custom_property.py 

for additional constraints. This is only for the RACOS_FFN tool.

NNENUM is as before

 Getting Started
 -------------------------
1. clone MLVS repository 

         git clone https://github.com/DMoumita/MLVS.git

2. Entering into MLVS directory
      
         cd MLVS

3. python RACOS_FFN.py sample_model.onnx prop10.vnnlib prop_y10_0 10

4. python nnenum.py sample_model.onnx prop10.vnnlib prop_y10_0 10

