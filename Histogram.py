# coding=utf-8

# Author: $￥
# @Time: 2020/08/24 14:59

import matplotlib.pyplot as plt
import numpy as np

size = 2 # 几个组
y1 = [1, 2]
y2 = [3, 4]
y3 = [5, 6]
y4 = [7, 8]
y5 = [9, 10]

name = ["750", "900"]

x = np.arange(size)
total_width, n = 0.8, 5     # 有多少个类型，只需更改n即可
width = total_width / n
x = x - (total_width - width) / 2

plt.bar(x, y1,  width=width, edgecolor='black', label='name1')
plt.bar(x + width, y2, width=width, edgecolor='black', label='name2')
plt.bar(x + 2 * width, y3, width=width, edgecolor='black', label='name3', tick_label=name)
plt.bar(x + 3 * width, y4, width=width, edgecolor='black', label='name4')
plt.bar(x + 4 * width, y5, width=width, edgecolor='black', label='name5')

plt.legend()

plt.ylabel('xlabel')
plt.xlabel('ylabel')

# plt.title("title")
# plt.savefig('D:\\result.png')

plt.show()
