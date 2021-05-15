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
   - https://github.com/googlemaps/google-maps-services-python
   - https://developers.google.com/maps/documentation/directions/get-directions
   - [Alternative Routing Libraries](https://www.igismap.com/top-10-map-direction-api-routing-libraries-navigation-free-or-paid/) - _Google Direction API is not free_
1. Web scraping
   - Ways to use bs4
   https://towardsdatascience.com/scraping-1000s-of-news-articles-using-10-simple-steps-d57636a49755
   https://towardsdatascience.com/web-scraping-news-articles-in-python-9dd605799558 
   - Clean tag
   https://medium.com/@jorlugaqui/how-to-strip-html-tags-from-a-string-in-python-7cb81a2bbf44 
   - Progress bar
   https://medium.com/@abhirsk02/web-scraping-weather-data-using-python-4dfe2ee0ba6e 
   - Pyplot
   https://plotly.com/python/bar-charts/ 
   https://plotly.com/python/figure-labels/ 
   - Count Word Frequencies
   https://programminghistorian.org/en/lessons/counting-frequencies
2. Sentiment Analysis + filtering
   - [GitHub python-hash-trie](https://github.com/bzamecnik/python-hash-trie/blob/master/hash_trie/hash_trie.py)
3. Data Visualization for sentiment analysis
4. Ranking algorithm
5. Video & audio analysis
6. Dynamic Time Warping (DTW)
   - https://www.youtube.com/watch?v=_K1OsqCicBY
   - https://www.youtube.com/watch?v=tfOevFKQIjQ
   - https://towardsdatascience.com/dynamic-time-warping-3933f25fcdd
   - https://dynamictimewarping.github.io/python/
   - https://betterprogramming.pub/how-to-do-speech-recognition-with-a-dynamic-time-warping-algorithm-159c2a1bb83c - Basic implementation rules reference & complexity of the algorithm:
   - https://iopscience.iop.org/article/10.1088/1742-6596/1366/1/012091/pdf - Article Research on DWT:
   - https://www.youtube.com/watch?v=XXusSAdHQ7U - Matlab needed?
   - https://github.com/crawles/dtw - Implementation in python code (github)?
   - github.com/pierre-rouanet/dtw - refering by ^
7. Billing infomation
   - [Google Cloud Billing Overview](https://developers.google.com/maps/billing/gmp-billing#billing-overview)
   - [Google Cloud Billing Credit](https://developers.google.com/maps/billing-credits)
   - [Google Cloud Billing Pricing](https://cloud.google.com/maps-platform/pricing/sheet/?_ga=2.42127266.622598182.1620895783-341686522.1608875911)


### Frontend (Javascript)
1. Address input field
   - Use Bootstrap [Form](https://getbootstrap.com/docs/4.6/components/forms/)
2. Display Google Map with waypoint & Draw Routes
   - Draw the route using [polyline](https://www.sitepoint.com/create-a-polyline-using-the-geolocation-and-the-google-maps-api/)
   - [gmplot](https://github.com/gmplot/gmplot) can draw the route for us with the help of [Google Direction API](https://developers.google.com/maps/documentation/directions/overview)
     - [Guide](https://www.tutorialspoint.com/plotting-google-map-using-gmplot-package-in-python) to use gmplot
     - [More Guide](https://www.codedisciples.in/google-map-plots.html)
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



