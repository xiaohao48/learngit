import matplotlib.pyplot as plt

x_value = list(range(1, 5001))
y_value = [x ** 3 for x in x_value]
plt.scatter(x_value, y_value, c=y_value, cmap=plt.cm.Greens, s=50)
plt.title("cube_value", fontsize=20)
plt.xlabel("value", fontsize=14)
plt.ylabel("cube of value", fontsize=14)
plt.show()
