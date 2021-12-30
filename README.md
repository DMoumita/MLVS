MLVS (Machine Learning Verification Service)
-----------------------------------------------

MLVS verifies a given neural network for a given property specification

Verifies using two tools - FFN and NNENUM

 Getting Started
 
 -------------------------
1. clone MLVS repository     

         git clone https://github.com/DMoumita/MLVS.git

2. Entering into MLVS directory
      
         cd MLVS
                  
3-a. Run using Docker 

    #Intall Docker Engine - please refer https://docs.docker.com/engine/install/ubuntu/
    #The Dockerfile in FFN folder shows how to install all the dependencies (mostly python and numpy packages) and set up the environment. 

   . To build and run mlvs image
    
    sudo docker build . -t mlvs_image 

   To get a shell after building the image:
  
    sudo docker run -i -t mlvs_image bash
    
   Run a script without entering in to the the shell:
   
    sudo docker run -i  mlvs_image 
    
    
    
 
 3-b. [Tested for Ubuntu 16.04 and 18.04]
      Run in local server without docker image
    
       pip install -r requirements.txt
       cd MLVS
       python mlvs.py

   

To execute on local server: 
--------------------------
   http://127.0.0.1:5000/mlvs

Sample Output :
---------------
       
![image](https://user-images.githubusercontent.com/41421406/130942949-b1827f71-f25a-4921-9e54-9a5d6efcca9a.png)
  
  
Verify :
![image](https://user-images.githubusercontent.com/41421406/130942817-64e889bf-31db-4602-97ba-0483469d5971.png)



To check on AWS EC2 instance: 
--------------------------
http://ec2-3-128-200-136.us-east-2.compute.amazonaws.com:8080/mlvs
