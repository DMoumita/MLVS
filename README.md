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
3.  create an empty folderto store the given network and property files


         mkdir uploads

4-a. Run using Docker 

    #Intall Docker Engine - please refer https://docs.docker.com/engine/install/ubuntu/
    #The Dockerfile in FFN folder shows how to install all the dependencies (mostly python and numpy packages) and set up the environment. 

   To build and run mlvs image
    
    sudo docker build . -t mlvs_image 

   To get a shell after building the image:
  
    sudo docker run -i -t mlvs_image bash
    
   Run a script without entering in to the the shell:
   
    sudo docker run -i  mlvs_image 
 
 4-b. Run in local server without docker image
    
       pip install Flask
       cd MLVS
       python app.py

   

To execute on local server: 
--------------------------
   http://127.0.0.1:5000/mlvs

Sample Output :
---------------
       
  ![image](https://user-images.githubusercontent.com/41421406/128775429-84342b71-1d32-42fa-a1ba-a333cd05643a.png)
  
  
Verify :

![image](https://user-images.githubusercontent.com/41421406/128779496-8aaf48b8-d838-49f6-9c07-98f173d80108.png)


To check on AWS EC2 instance: 
--------------------------
http://ec2-3-143-5-170.us-east-2.compute.amazonaws.com:8080/verify
