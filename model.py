from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from game import ColorableCliqueGame
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import importlib
import game
importlib.reload(game)

print("????")


def draw(env):
    imgdata = env.frame()
    plt.imshow(imgdata)
    #print(np.max(imgdata), np.min(imgdata), np.average(imgdata))
    plt.show()


filename = 'data\K6D3n.npz'
with open(filename, 'rb') as f:
    a = np.load(f, allow_pickle=True)['data']

X: np.ndarray = a[:, 0]
Y: np.ndarray = a[:, 1]
Y = Y.astype(np.float32)
X = np.array(list(X))

Y = np.tanh(Y)

print("????")

X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.20, random_state=42, shuffle=True)

rfc = RandomForestRegressor(n_estimators=200, n_jobs=-1)
rfc.fit(X_train, y_train)

print("??SDASDAS")

target_predicted = rfc.predict(X_test)
print(target_predicted.min(), target_predicted.max())
print(y_test.mean(), y_test.var())
print(mean_squared_error(y_test, target_predicted))
