import os
from flask import Flask, render_template, request, redirect, url_for, abort, request
from werkzeug.utils import secure_filename
import subprocess


app = Flask(__name__)

app.config['UPLOAD_EXTENSION_ONNX'] = ['.onnx']
app.config['UPLOAD_EXTENSION_VNNLIB'] = ['.vnnlib']
subprocess.run("mkdir -p uploads", shell=True, check=True)

#All uploaded files are saved into this "upload" folder
app.config['UPLOAD_PATH'] = 'uploads'

#index.html should be kept in templates folder
@app.route('/mlvs')
def index():
    return render_template('index.html')

@app.route('/genTest')
def nn():
    return render_template('genTest.html')


@app.route('/genProp')
def genProp():
    return render_template('genProp.html')

@app.route('/ffn')
def ffn():
    return render_template('ffn.html')

@app.route('/nnenum')
def nnenum():
    return render_template('nnenum.html')

@app.route("/verify",methods=['GET','POST'])
def verify():

   if request.method == 'POST' :
      #get uploaded .onnx file from user

      uploadedOnnxFile = request.files['file1']
      onnxFilename = secure_filename(uploadedOnnxFile.filename)

      if onnxFilename != '':
           #delete uploaded .onnx files from "uploads" folder
           removeFiles = "rm " + app.config['UPLOAD_PATH'] + "/ACAS*"
           subprocess.run(removeFiles, shell=True)
           file_ext = os.path.splitext(onnxFilename)[1]

           #check for a .onnx file
           if file_ext not in app.config['UPLOAD_EXTENSION_ONNX']:
              abort(400,"Wrong .onnx file")

           #.onnx file saved in 'UPLOAD_PATH'
           uploadedOnnxFile.save(os.path.join(app.config['UPLOAD_PATH'], onnxFilename))
      #get uploaded .vnnlib file from user

      uploadedVnnlibFile = request.files['file2']
      vnnlibFilename = secure_filename(uploadedVnnlibFile.filename)

      if vnnlibFilename != '':
         #delete uploaded .onnx files from "uploads" folder
         removeFiles = "rm " + app.config['UPLOAD_PATH'] + "/prop*"
         subprocess.run(removeFiles, shell=True)
         file_ext = os.path.splitext(vnnlibFilename)[1]

         #check for a .onnx file
         if file_ext not in app.config['UPLOAD_EXTENSION_VNNLIB']:
            abort(400,"Wrong .vnnlib file")

         #.vnnlib file saved in 'UPLOAD_PATH'
         uploadedVnnlibFile.save(os.path.join(app.config['UPLOAD_PATH'], vnnlibFilename))

      #get timeout value from user
      timeOut = request.form['timeout']

      #set default value for timeOut if not metioned
      printTimeout=""
      if timeOut == '':
         timeOut = "20"
         printTimeout = "\nDefault Timeout = 20 sec"

      #create absolute path for .onnx and .vnnlib file
      output1=""
      if (onnxFilename == ''):
          onnxFilename = subprocess.check_output("ls " + app.config['UPLOAD_PATH']+"/ACAS*",shell=True)
          onnxFilename=onnxFilename.decode('utf8')
          actualmodel = onnxFilename.rstrip("\n")
      else :
          actualmodel = app.config['UPLOAD_PATH']+ "/" + onnxFilename
      if (vnnlibFilename == ''):
          vnnlibFilename = subprocess.check_output("ls " + app.config['UPLOAD_PATH']+"/prop*",shell=True)
          vnnlibFilename=vnnlibFilename.decode('utf8')
          propVnnlib = vnnlibFilename.rstrip("\n")
      else:
          propVnnlib = app.config['UPLOAD_PATH'] + "/" + vnnlibFilename

      output=""
      if request.form['action'] == 'FFN':
      #run FFN
         pythonProg ="RACOS_FFN.py " + actualmodel + " " + propVnnlib+"  "+timeOut
         output = subprocess.check_output("python3 " +pythonProg, shell=True)
         printToolName = "FFN results -\n"
         output=output.decode('utf8')
         output = output.replace('\n\n','\n')
      elif request.form['action'] == 'NNENUM':
         #run NNENUM
         pythonProg ="nnenum.py " + actualmodel + " " + propVnnlib+"  "+timeOut
         output = subprocess.check_output("python3 " +pythonProg, shell=True)
         printToolName = "NNenum results -\n"
         output=output.decode('utf8')
         output = output.replace('\n\n','\n')
      output = output.replace('Warning: numerical instability (primal simplex, phase II)','')
      output = output.replace('\n\n\n','\n')
      output = printToolName+printTimeout+output

      #delete all upload files from "uploads" folder
      #removeFiles = "rm " + app.config['UPLOAD_PATH'] + "/*"
      #subprocess.run(removeFiles, shell=True)

      return render_template('runTool1.html',output=output)
   else:
      return render_template('runTool.html')

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)

