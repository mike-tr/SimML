import importlib
import numpy as np
import game
importlib.reload(game)
from game import ColorableCliqueGame
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error


filename = 'data\K6D3n.npz'
with open(filename, 'rb') as f:
    a = np.load(f, allow_pickle=True)['data']

X : np.ndarray = a[:, 0]
Y : np.ndarray = a[:, 1]
Y = Y.astype(np.float32)
X = np.array(list(X))

# some tests.
# draw test as well

colors = [(255,100,100), (100,100,255)]
env = ColorableCliqueGame(300,300,6, colors)
Y = np.tanh(Y)


X_train,X_test,y_train,y_test =train_test_split(X,Y , test_size=0.20, random_state=42,shuffle=True)

tree = DecisionTreeRegressor(max_depth=21)
print(tree.fit(X_train[0::33], y_train[0::33]))

target_predicted = tree.predict(X_test)
index = 105555
print(Y[index:index+3])
print(target_predicted[index: index + 3])
print(target_predicted.min(),target_predicted.max())


print("y test mean: ",y_test.mean()," y test var: ", y_test.var())
print("Decision Tree MSE:",mean_squared_error(y_test, target_predicted))
