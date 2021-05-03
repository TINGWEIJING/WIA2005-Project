# WIA2005-Project
## TOC
- [Installation](#installation)
- [Run](#run)
- [Target Features](#target-features)
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

### Frontend (Javascript)
1. Address input field
   - Use Bootstrap [Form](https://getbootstrap.com/docs/4.6/components/forms/)
2. Display Google Map with waypoint & Draw Routes
   - Draw the route using [polyline](https://www.sitepoint.com/create-a-polyline-using-the-geolocation-and-the-google-maps-api/)
   - [gmplot](https://github.com/gmplot/gmplot) can draw the route for us with the help of [Google Direction API](https://developers.google.com/maps/documentation/directions/overview)
     - [Guide](https://www.tutorialspoint.com/plotting-google-map-using-gmplot-package-in-python) to use gmplot
   - GCP Account needed to have API Key
3. Display table of distance
   - Use Bootstrap [Table](https://getbootstrap.com/docs/4.6/content/tables/)
4. Ranking
   - Use Bootstrap Table
5. General Info
   - [Bootstrap](https://getbootstrap.com/docs/4.6/getting-started/introduction/) version is 4.6
   - Use [iframe](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe) to diaplay map in index.html
   - [normalize.css](https://necolas.github.io/normalize.css/) used to maintain cross-browser compatability

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



