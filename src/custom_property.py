import math

#keeping a global dictionary to access custom functions
#keeping a global value of dump_ces cmdline argument

def init(dump_ces):
   global dump_ce
   dump_ce = dump_ces
   global funcdict
   funcdict = {
     'prop_default': prop_default,
     'prop_y10' : prop_y10,
     'prop_y10_0' : prop_y10_0
   }

def prop_default(inputs,outputs):
    #no special checks
    return 1

def prop_y10(inputs,outputs):
    x3 = inputs[3] * 100 + 50
    x4 = inputs[4] * 100 + 50
    x5 = inputs[5] * 100 + 50
    x3Up = math.sqrt(x3 * (100 - x3))
    x4Up = math.sqrt(x4 * (100 - x4))
    x5Up = math.sqrt(x5 * (100 - x5))

    x6 = inputs[6] * 50 + 25
    x7 = inputs[7] * 50 + 25
    x8 = inputs[8] * 50 + 25

    # Validate the constraints on the inputs
    if (x6 > x3Up) or (x7 > x4Up) or (x8 > x5Up):
        return 0
    # Check constraints on output
    y10 = outputs[10]
    limit = -0.2
    if (y10 < limit):
        print("input constraints satisfied -----\n", x6, x3Up, x7, x4Up, x8, x5Up, "---------")
        print("counterexample found -----\n", y10, limit)
        print("Input: ", inputs)
        print("Outputs: ", outputs)
        return 1

    # print("output constraint satisfied")
    return 0

def prop_y10_0(inputs, outputs):
    x3 = inputs[3] * 100 + 50
    x4 = inputs[4] * 100 + 50
    x5 = inputs[5] * 100 + 50
    x3Up = math.sqrt(x3 * (100 - x3))
    x4Up = math.sqrt(x4 * (100 - x4))
    x5Up = math.sqrt(x5 * (100 - x5))

    x6 = inputs[6] * 50 + 25
    x7 = inputs[7] * 50 + 25
    x8 = inputs[8] * 50 + 25

    # Validate the constraints on the inputs
    if (x6 > x3Up) or (x7 > x4Up) or (x8 > x5Up):
        return 0
    # Check constraints on output
    y10 = outputs[10]
    limit = 0.6
    if (y10 > limit):
        print("input constraints satisfied -----\n", x6, x3Up, x7, x4Up, x8, x5Up, "---------")
        print("counterexample found -----\n", y10, limit)
        print("Input: ", inputs)
        print("Outputs: ", outputs)
        return 1

    #print("output constraint satisfied")
    return 0
