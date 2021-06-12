# WIA2005-Project Development Notes
## TOC
- [WIA2005-Project Development Notes](#wia2005-project-development-notes)
  - [TOC](#toc)
  - [Refresh](#refresh)
  - [Target Features](#target-features)
    - [Backend (Python)](#backend-python)
    - [Frontend (Javascript)](#frontend-javascript)
  - [Gits Commands](#gits-commands)

## Refresh
- Update requirements.txt
```Shell
pip freeze > requirements.txt
```
- Anaconda (ignore)
```Shell
jupyter notebook --NotebookApp.iopub_data_rate_limit=1.0e10
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
   - Video
     - [YT - How DTW (Dynamic Time Warping) algorithm works](https://www.youtube.com/watch?v=_K1OsqCicBY)
     - [YT - Dynanmic Time Warping](https://www.youtube.com/watch?v=tfOevFKQIjQ)
     - https://www.youtube.com/watch?v=XXusSAdHQ7U - Matlab needed?
   - Paper
     - [Dynamic Programming Algorithms in Speech Recognition Paper](https://www.researchgate.net/publication/26569937_Dynamic_Programming_Algorithms_in_Speech_Recognition)
     - [Speech recognition using Dynamic Time Warping(DTW)](https://iopscience.iop.org/article/10.1088/1742-6596/1366/1/012091/pdf )
   - Article
     - [TD - Dynamic Time Warping](https://towardsdatascience.com/dynamic-time-warping-3933f25fcdd)
     - [How to Do Speech Recognition With a Dynamic Time Warping Algorithm](https://betterprogramming.pub/how-to-do-speech-recognition-with-a-dynamic-time-warping-algorithm-159c2a1bb83c)
     - [Understanding Dynamic Time Warping - Part 1](https://databricks.com/blog/2019/04/30/understanding-dynamic-time-warping.html)
     - [An Illustrative Introduction to Dynamic Time Warping](https://towardsdatascience.com/an-illustrative-introduction-to-dynamic-time-warping-36aa98513b98)
     - [Programatically understanding dynamic time warping (DTW)](https://nipunbatra.github.io/blog/ml/2014/05/01/dtw.html)
     - [Speech.zone - Dynamic Time Warping (DTW) in Python](https://speech.zone/exercises/dtw-in-python/)
   - Library
     - [Lib - dtw-python: Dynamic Time Warping in Python](https://dynamictimewarping.github.io/python/)
      - [GitHub - dtw Sample Code](https://github.com/crawles/dtw)
      - [GitHub - Dynamic Time Warping Python Module](https://github.com/pierre-rouanet/dtw)
      - [Dynamic Time Warping (DTW)](https://dtaidistance.readthedocs.io/en/latest/usage/dtw.html)
      - [mlpy DTW](http://mlpy.sourceforge.net/docs/3.4/dtw.html#)
      - [pyts](https://pyts.readthedocs.io/en/stable/generated/pyts.metrics.dtw.html)
      - https://github.com/aishoot/DTWSpeech
   - [Split speech audio file on words in python](https://stackoverflow.com/questions/36458214/split-speech-audio-file-on-words-in-python) 
   - [Read an audio file / Split audio files using Python](https://dataunbox.com/split-audio-files-using-python/)
   - [Simple Audio Processing in Python With Pydub](https://betterprogramming.pub/simple-audio-processing-in-python-with-pydub-c3a217dabf11)
   - [Automatic splitting of audio files on silence in Python](https://walczak.org/2019/02/automatic-splitting-audio-files-silence-python/) 
   - MFCC
     - [Cepstrum and MFCC](https://wiki.aalto.fi/display/ITSP/Cepstrum+and+MFCC)
     - [Mel Frequency Cepstral Coefficient (MFCC) tutorial](http://practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/)
     - [Understanding Audio data, Fourier Transform, FFT and Spectrogram features for a Speech Recognition System](https://towardsdatascience.com/understanding-audio-data-fourier-transform-fft-spectrogram-and-speech-recognition-a4072d228520)
     - [Introduction To Dynamic Time Warping](https://riptutorial.com/algorithm/example/24981/introduction-to-dynamic-time-warping)

7. Billing infomation
   - [Google Cloud Billing Overview](https://developers.google.com/maps/billing/gmp-billing#billing-overview)
   - [Google Cloud Billing Credit](https://developers.google.com/maps/billing-credits)
   - [Google Cloud Billing Pricing](https://cloud.google.com/maps-platform/pricing/sheet/?_ga=2.42127266.622598182.1620895783-341686522.1608875911)
8. MongoDB
   - [Flask-PyMongo Official](https://flask-pymongo.readthedocs.io/en/latest/)
   - [Integrating MongoDB with Flask Using Flask-PyMongo](https://stackabuse.com/integrating-mongodb-with-flask-using-flask-pymongo/)
   - [How to Set Up Flask with MongoDB](https://pythonbasics.org/flask-mongodb/)
   - [Connecting to a MongoDB in Flask Using Flask-PyMongo (2019)](https://youtu.be/3ZS7LEH_XBg)
   -https://www.youtube.com/watch?v=XT6rcN0O3as
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