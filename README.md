# WIA2005-Project

## TOC
- [WIA2005-Project](#wia2005-project)
  - [Project Description](#project-description)
    - [Problem 1](#problem-1)
    - [Problem 2](#problem-2)
    - [Problem 3](#problem-3)
    - [Problem 4](#problem-4)
  - [Installation & Settings](#installation--settings)
  - [Run](#run)
  - [Snapshots](#snapshots)
    - [Main page](#main-page)
    - [Audio analysis page](#audio-analysis-page)

## Project Description
**University**: University of Malaya
**Programme**: Bachelor of Computer Science
**Course**: WIA2005 Algorithm Analysis and Design
**Year**: 2nd year / 4th semester

### Problem 1
Customer who needs to make a delivery needs to know which courier company can does it fast (assuming that the shorter the distance, the quicker is the delivery). The application will analyse five (5) local courier companies which have their delivery hubs located in various locations in West Malaysia. The details of the courier companies and their delivery hubs are given in Table 1.

### Problem 2
Shortest distance travelled does not mean that the courier company is the most recommended option for customer to use. A sentiment analysis of the related news articles about the courier company must be conducted.

### Problem 3
Customers need to be able to choose the best courier company based on the distance as well as the result of sentiment analysis of related online articles.

### Problem 4
Assuming that video or audio from the news or customer feedback will be used to provide sentiment insights in the future, Dynamic Time Warping (DTW) is one of the algorithms that can potentially be used. Explain the concept of DTW and demonstrate the implementation of DTW in analysing a video or an audio. For example, given the following video (https://www.youtube.com/watch?v=ZwVFj8CfFeE), identify some words, for example “J&T”, “memohon” and “maaf”.

## Installation & Settings
1. Create venv with the name venv
```Shell
py -m venv venv
```
2. Activate venv
```Shell
venv\Scripts\activate
```
3. Install required libraries
```Shell
py -m pip install -r requirements.txt
```
4. Provide your own api key & database URI <br>
   a. Go to `instance\config_ex.py` file <br>
   b. Add Mongo database URI (`MONGO_URI`) <br>
   c. Add Google Direction API key (`GOOGLE_API_KEY`) <br>
   d. Rename the file to `config.py` <br>
   e. Go to `core\templates\index.html` file, line 27 - 28 <br>
   f. Insert the Google Map API key <br>
   

## Run
- Using CMD
```Shell
venv\Scripts\activate
set FLASK_APP=core
set FLASK_ENV=development
flask run
```
- Using Power Shell
```Shell
venv\Scripts\activate
$env:FLASK_APP = "core"
$env:FLASK_ENV = "development"
flask run
```

## Snapshots
### Main page
![](doc/images/Main%20page.png)

### Audio analysis page
![](doc/images/Audio%20Analysis%20page.png)
