"""
This is a simple performance test to verify in practice, that the complexity
of the use_item operation is really O(1).

We perform the following experiment one million times:

1. Use the new item id given by iteration number
2. Pick a random id from those used already and use it as well

During the process above described, we keep track of the time  taken
in calling the use_item method. For each # of items used so far, we
average the two calls above (one for new item not seen, and the other
for already seen item).

At the end we just plot these average times vs # items. Accurate plotting
requires high-precision clock, probably up to nano-seconds; hence, we
use an scatter plot to avoid paying attention to the cases which were fast
enough to get a zero delay.

"""
from random import randint
from time import process_time

import matplotlib.pyplot as plt
import numpy as np

from urank.UsageRanking import UsageRanking

n = 1000000
x = np.zeros(n)
y = np.zeros(n)
urank = UsageRanking()
for id in range(n):
    x[id] = id + 1
    start = process_time()
    urank.use_item(id)
    end = process_time()
    dur = end - start
    start = process_time()
    urank.use_item(randint(0, id))
    end = process_time()
    dur += end - start
    y[id] = dur / 2
plt.xlabel('# of items')
plt.ylabel('duration of use_item (secs)')
plt.title('Does use_item have O(1) time complexity?')
plt.scatter(x, y)
plt.show()
