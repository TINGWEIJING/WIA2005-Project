from collections import OrderedDict


class Company:
    def __init__(self, name: str, mean_ratio: int, distance: float):
        self.name = name
        self.mean_ratio = mean_ratio
        self.distance = distance

    def get_name(self) -> str:
        return self.name

    def get_mean_ratio(self) -> int:
        return self.mean_ratio

    def get_distance(self) -> float:
        return self.distance

    #  greater than here means better than
    def __gt__(self, other: 'Company'):
        # if the difference in distance between first and second item is smaller or equal to 10 and the second one has better sentiment
        # if the second element is shorter than the first element (difference that is more than 10), means that second one is better
        if abs(other.distance - self.distance) <= 10 and self.mean_ratio != other.mean_ratio:
            return self.mean_ratio < other.mean_ratio
        else:
            return self.distance < other.distance
        # return (abs(other.distance - self.distance) <= 10 and other.sentiment_value <= self.sentiment_value) or other.distance - self.distance > 10


class Ranking:
    def __init__(self, routes_data: dict, sentiment_data: dict):
        # filter routes data to get hub name and distance only
        routes = routes_data.get('routes')
        _hub_dists = {}
        for obj in routes:
            _hub = obj.get('hub')
            _dist = obj.get('distance')
            _hub_dists[_hub] = _dist

        # filter sentiment analysis data
        sentiment = sentiment_data.get('result')
        _hub_mean_ratio = {}
        for obj in sentiment:
            _hub = obj.get('courier')
            _value = obj.get('ratio')
            if _hub_mean_ratio.get(_hub) is None:
                _hub_mean_ratio[_hub] = (_value, 1)
            else:
                new_value, new_count = _hub_mean_ratio[_hub]
                new_value += _value
                new_count += 1
                _hub_mean_ratio[_hub] = (new_value, new_count)

        # calculate mean ratio
        for hub, ratio_count in _hub_mean_ratio.items():
            ratio, count = ratio_count
            mean_ratio = ratio / count
            _hub_mean_ratio[hub] = mean_ratio

        self.companies = []
        for hub in _hub_dists.keys():
            new_company = Company(name=hub,
                                  mean_ratio=_hub_mean_ratio[hub],
                                  distance=_hub_dists[hub])
            self.companies.append(new_company)

        # sort
        self.__class__.timSort(self.companies)

    def get_rankings(self):
        result = []
        for i, company in enumerate(self.companies):
            data = {
                'ranking': i,
                'hub': company.name,
                'distance': company.distance,
                'mean_ratio': company.mean_ratio
            }
            result.append(data)
        return result

    @classmethod
    def insertionSort(cls, arr, left, right):
        '''Sorts array from left index to right index'''
        for i in range(left + 1, right + 1):
            j = i
            while j > left and arr[j] > arr[j - 1]:
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
                j -= 1

    @classmethod
    def merge(cls, arr, l, m, r):
        '''Merge function merges the sorted runs'''
        # original array is broken in two parts
        # left and right array
        len1, len2 = m - l + 1, r - m
        left, right = [], []
        for i in range(0, len1):
            left.append(arr[l + i])
        for i in range(0, len2):
            right.append(arr[m + 1 + i])

        i, j, k = 0, 0, l

        # after comparing, we merge those two array
        # in larger sub array
        while i < len1 and j < len2:
            if left[i] > right[j]:
                arr[k] = left[i]
                i += 1

            else:
                arr[k] = right[j]
                j += 1

            k += 1

        # Copy remaining elements of left, if any
        while i < len1:
            arr[k] = left[i]
            k += 1
            i += 1

        # Copy remaining element of right, if any
        while j < len2:
            arr[k] = right[j]
            k += 1
            j += 1

    @classmethod
    def timSort(cls, arr):
        n = len(arr)
        minRun = 3

        # Sort individual subarrays of size RUN
        for start in range(0, n, minRun):
            end = min(start + minRun - 1, n - 1)
            cls.insertionSort(arr, start, end)

            # Start merging from size RUN

        size = minRun
        while size < n:
            # Pick starting point of left sub array. We
            # are going to merge arr[left..left+size-1]
            # and arr[left+size, left+2*size-1]
            # After every merge, we increase left by 2*size
            for left in range(0, n, 2*size):
                # Find ending point of left sub array
                # mid+1 is starting point of right sub array
                mid = min(n-1, left + size - 1)
                right = min((left + 2 * size - 1), (n - 1))

                # Merge sub array arr[left.....mid] &
                # arr[mid+1....right]
                if mid < right:
                    cls.merge(arr, left, mid, right)
            size = 2 * size


if __name__ == "__main__":
    arr = [
        {
            "company": "Poslaju",
            "sentiment_value": 1,
            "distance": 50
        },
        {
            "company": "Citylink",
            "sentiment_value": 2,
            "distance": 53
        },
        {
            "company": "GDEX",
            "sentiment_value": 3,
            "distance": 25
        },
        {
            "company": "J&T",
            "sentiment_value": 3,
            "distance": 58
        },
        {
            "company": "DHL",
            "sentiment_value": 3,
            "distance": 56
        }
    ]
    obj_arr = []
    # store array of objects
    for i in arr:
        obj_arr.append(Company(i['company'], i['sentiment_value'], i['distance']))

    # timsort
    timSort(obj_arr)

    # store the objects into orderedDict()
    ranking = OrderedDict()
    # idx to insert ranking into orderedDict
    idx = 1
    for i in obj_arr:
        ranking[i.get_name()] = {'ranking': idx, 'distance': i.get_distance(), 'sentiment value': i.get_sentiment_value()}
        idx += 1

    print(ranking)
