MLVS (Machine Learning Verification Service)
-----------------------------------------------

MLVS verifies a given neural network for a given property specification

Verifies using two tools - FFN and NNENUM


How to run
-----------
1. Enter into MLVS directory and create an empty folder to save .onnx file and property file 

       cd MLVS
       mkdir uploads

2. 
    a. Run in local server using a docker image
     
       sudo docker build . -t mlvs_image
       sudo docker run -i mlvs_image
    
      Note: to get a shell use - 
        
        sudo docker run -i -t mlvs_image bash
    
    b. Run in local server without docker image
    
       pip install Flask
       cd MLVS
       python app.py
    

To check : 
--------
   http://127.0.0.1:5000/mlvs

Output :
---------------
       
  ![image](https://user-images.githubusercontent.com/41421406/128775429-84342b71-1d32-42fa-a1ba-a333cd05643a.png)
  
  
Verify :

![image](https://user-images.githubusercontent.com/41421406/128779496-8aaf48b8-d838-49f6-9c07-98f173d80108.png)


   

