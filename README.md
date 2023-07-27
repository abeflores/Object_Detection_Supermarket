# Object detection for in-store inventory management

In a nutshell, this project is an API service that is backed by a Yolov5 model that accepts an image of a shelve and return the image shaded green where the products are detected and red where the missing products are detected.

## Project Architecture

The architecture of the project consists of three different services, each of them in a different docker container: **ML Service** where Yolov5 model is based, **API** where the API service is based, and finally **REDIS** to connect the previous services. 

![Project Architecture](/utils/imgs/Project_arch.png)

## Run the project

After downloading this repository, simply run:

> docker compose up --build -d

The three images will be created and their containers will be up.

There are two ways to run the application, as follows:

### Front-End endpoint

This endpoint takes an image and returned it shaded with the product and missing product (green and red respectively).

![Project Architecture](/utils/imgs/Front-end.png)

Valid Token: secret-token-1-abelardo

![Project Architecture](/utils/imgs/Front-end-1.png)

### Integration-type endpoint

This endpoint takes an image and returns the bounding boxes coordinates, the class (product -> 0 and no product -> 1) and the user. 

![Project Architecture](/utils/imgs/Endpoint-back-0.png)
![Project Architecture](/utils/imgs/Endpoint-back-1.png)
![Project Architecture](/utils/imgs/Endpoint-back-2.png)
![Project Architecture](/utils/imgs/Endpoint-back-3.png)

## Run the API Tests

From /api, run:

> docker build -t flask_api_test --progress=plain --target test .

This will create the API image and automatically run the tests in the conatiner.

## Run the Stress Tests

From /stress_test, run:

> python run_stress_tests.py

This will create and run the three images and will sent GET and POST requests. 

## Model Training

To build yolov5 image, from /model/yolov5 run:
>docker build -t yolo_v5_image -f utils/docker/Dockerfile .

To run the model container
>docker run --rm --net host -it --gpus all -v $(pwd):/home/app/src --workdir /home/app/src yolo_v5_image bash

To run train script
>python train.py --data SKU-110K.yaml --cfg yolov5n.yaml --weights yolov5n.pt --batch-size 16 --epochs 30 --device 0

This will train the model (Yolov5 nano) with the SKU-110K dataset (it will download it if necessary). The only class in this dataset is the product, therefore, the model only will learn to detect products.  
To teach the model how to detect missing products, labeling hundred of images needs to be done. As a result, a new dataset will be created and the yaml file for data will change (2 classes have to be defined in it).  
In the utils folder, there are several scripts to help in that process. To create a subset of data to do the labeling, merge the label for the two classes, etc.

## Notebooks

There are 4 notebooks. 

1. **EDA:** Exploratory Data Analysis. General analysis of the SKU-110K dataset.

2. **Evaluate:** Evaluation of the trained model with 1 class (product). 

3. **Evaluate_2_classes:** Evaluation of the trained model with 2 classes (product and missing product). 

4. **Labels_Checker:** Assessment of the new class labels. 





