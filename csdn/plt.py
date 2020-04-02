import matplotlib.pyplot as plt

x = ["战士", "法师", "牧师", "游侠"]

data = [
    [4, 3, 3, 3],
    [3, 3, 3, 4],
    [2, 3, 3, 5],
    [4, 4, 3, 1]
]
for i in range(4):
    print(i)

for line in data:
    plt.plot(x, line)


plt.show()
