from collections import OrderedDict
import numpy as np

class ranking:
    def __init__(self, data: dict):
        # ranking order
        # short and positive -> short but negative -> long but positive -> long and negative
        self.result = {}
        self.data = data.copy()
        self.ranking = OrderedDict()
        self.getRanking()

    def sortByDistance(self):
        # sort from the shortest distance to the largest distance
        while len(self.data.keys()) > 0:
            first = list(self.data.keys())[0]
            # assign the first distance as minimum distance
            min = {"company":"","distance":0.0}
            for key in self.data:
                if key == first or self.data[key]["distance"] < min["distance"]:
                    min["company"] = key
                    min["distance"] = self.data[key]['distance']
            self.result[min["company"]] = self.data[min["company"]]
            # remove the company with shortest distance from the data and continue with next cycle
            self.data.pop(min["company"])

    def getRanking(self):
        self.sortByDistance()
        # compare 1st and 2nd
        #   if distance smaller than 3, 
        #       compare sentiment, 
        #       if the second one has better sentiment, swap, 
        #       else, keep
        indicator = list(self.result.items())
        indicator = np.array(indicator)
        # transform dict into array to swap elements easier

        for j in range(len(indicator)):
            for i in range(len(indicator)-j):
                if i == len(indicator) -1:
                    break
                # if the difference of distance between 2 consecutive elements is smaller than 10
                if abs(indicator[i+1][1]['distance'] - indicator[i][1]['distance']) < 10:
                    # then we compare their sentiment analysis
                    if indicator[i][1]['sentiment_value'] < indicator[i+1][1]['sentiment_value']:
                        # swap if the next element has better sentiment
                        temp = indicator[i].copy()
                        indicator[i] = indicator[i+1]
                        indicator[i+1] = temp

        for i in range(len(indicator)):
            key = indicator[i][0]
            self.result[key]["ranking"] = i+1
            self.ranking[key] = self.result[key]

        print(self.ranking)
        
        
if __name__ == "__main__":
    rank = ranking(
        {
            "Poslaju": {
                "sentiment_value": -1,
                "distance": 50
            },
            "Citylink": {
                "sentiment_value": 0,
                "distance": 53
            },
            "GDEX": {
                "sentiment_value": 1,
                "distance": 25
            },
            "J&T": {
                "sentiment_value": 0,
                "distance": 58
            },
            "DHL": {
                "sentiment_value": 1,
                "distance": 56
            }
        }
    )