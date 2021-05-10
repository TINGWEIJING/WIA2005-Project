# WIA2005-Project
## TOC
- [WIA2005-Project](#wia2005-project)
  - [TOC](#toc)
  - [Installation](#installation)
  - [Run](#run)
  - [Target Features](#target-features)
    - [Backend (Python)](#backend-python)
    - [Frontend (Javascript)](#frontend-javascript)
  - [Gits Commands](#gits-commands)

## Installation
- Create venv with the name venv
```Shell
py -m venv venv
```
- Activate venv
```Shell
venv\Scripts\activate
```
- Install required libraries
```Shell
py -m pip install -r requirements.txt
```

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

## Target Features
### Backend (Python)
1. Geocoding & Routing & Distance
   - https://osmnx.readthedocs.io/en/stable/
   - https://shakasom.medium.com/routing-street-networks-find-your-way-with-python-9ba498147342
   - https://pypi.org/project/openrouteservice/
   - https://openrouteservice.org/
   - https://pypi.org/project/geopy/#downloads
1. Web scraping
2. Sentiment Analysis + filtering
3. Data Visualization for sentiment analysis
4. Ranking algorithm
5. Video & audio analysis
6. Dynamic Time Warping (DTW)
   - https://www.youtube.com/watch?v=_K1OsqCicBY
   - https://www.youtube.com/watch?v=tfOevFKQIjQ
   - https://towardsdatascience.com/dynamic-time-warping-3933f25fcdd
   - https://dynamictimewarping.github.io/python/
   Basic implementation rules reference & complexity of the algorithm:
   - https://betterprogramming.pub/how-to-do-speech-recognition-with-a-dynamic-time-warping-algorithm-159c2a1bb83c
   Article Research on DWT:
   - https://iopscience.iop.org/article/10.1088/1742-6596/1366/1/012091/pdf
   Matlab needed?
   - https://www.youtube.com/watch?v=XXusSAdHQ7U
   Implementation in python code (github)?
   - https://github.com/crawles/dtw

   

### Frontend (Javascript)
1. Address input field
2. Display Google Map with waypoint & Draw Routes
3. Display table of distance
4. Ranking

## Gits Commands
- Clone repo
```git
git clone url
```

- Update all local branches
```git
git pull --all
```

- Create a new local branch
```git
git branch branch_name
```

- List all local branches
```git
git branch
```

- Switch local branch
```git
git checkout branch_name
```

- Push a new local branch to remote branch
```git
git push -u origin branch_name
```

- Add all files in staging area
```git
git add .
```

- Check git status
```git
git status
```

- Commit changes with a message
```git
git commit -m "your commit message here"
```

- Push changes
```git
git push
```

- Delete branch
```git
git branch -d branch_name
```

- Remove a remote branch
```git
git push --delete origin branch_name_here
```

- Show commit history
```git
git log --graph --oneline --all
```

- Rollback previous commit
```git
git revert comit_id_here
```



