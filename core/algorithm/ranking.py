from collections import OrderedDict

class company:
    def __init__(self, name: str,sentiment_value:int, distance: float):
        self.name = name
        self.sentiment_value = sentiment_value
        self.distance = distance
    
    def get_name(self) -> str:
        return self.name
    
    def get_sentiment_value(self) -> int:
        return self.sentiment_value

    def get_distance(self) -> float:
        return self.distance

    #  greater than here means better than
    def __gt__(self, other):
        # if the difference in distance between first and second item is smaller or equal to 10 and the second one has better sentiment
        # if the second element is shorter than the first element (difference that is more than 10), means that second one is better
        return (abs(other.distance - self.distance) <= 10 and other.sentiment_value <= self.sentiment_value) or other.distance - self.distance > 10

# sorts array from left index to right index 
def insertionSort(arr, left, right):
	for i in range(left + 1, right + 1):
		j = i
		while j > left and arr[j] > arr[j - 1]:
			arr[j], arr[j - 1] = arr[j - 1], arr[j]
			j -= 1

# Merge function merges the sorted runs
def merge(arr, l, m, r):
	
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

def timSort(arr):
    n = len(arr)
    minRun = 3

    # Sort individual subarrays of size RUN
    for start in range (0,n,minRun):
        end = min(start + minRun - 1, n - 1)
        insertionSort(arr, start, end)

	# Start merging from size RUN 

    size = minRun
    while size < n:
		# Pick starting point of left sub array. We
		# are going to merge arr[left..left+size-1]
		# and arr[left+size, left+2*size-1]
		# After every merge, we increase left by 2*size
        for left in range (0,n,2*size):
            # Find ending point of left sub array
			# mid+1 is starting point of right sub array
            mid = min(n-1, left + size - 1)
            right = min((left + 2 * size - 1),(n - 1))

            # Merge sub array arr[left.....mid] &
			# arr[mid+1....right]
            if mid < right:
                merge(arr, left, mid, right)
        size = 2* size
        
if __name__ == "__main__":
    arr = [
        {
            "company":"Poslaju",
            "sentiment_value": 1,
            "distance": 50
        },
        {
            "company":"Citylink",
            "sentiment_value": 2,
            "distance": 53
        },
        {
            "company":"GDEX",
            "sentiment_value": 3,
            "distance": 25
        },
        {
            "company":"J&T",
            "sentiment_value": 3,
            "distance": 58
        },
        {
            "company":"DHL",
            "sentiment_value": 3,
            "distance": 56
        }
    ]
    obj_arr = []
    # store array of objects
    for i in arr:
        obj_arr.append(company(i['company'],i['sentiment_value'],i['distance']))

    # timsort
    timSort(obj_arr)

    # store the objects into orderedDict()
    ranking = OrderedDict()
    # idx to insert ranking into orderedDict
    idx = 1
    for i in obj_arr:
        ranking[i.get_name()] = {'ranking':idx, 'distance':i.get_distance(),'sentiment value':i.get_sentiment_value()}
        idx+=1
    
    print(ranking)