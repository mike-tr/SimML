import importlib
import numpy as np
import game
importlib.reload(game)
from game import ColorableCliqueGame
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
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

rfc = RandomForestRegressor(n_estimators=10, warm_start=True, n_jobs=-1)
skip = 33
for i in range(skip):
    rfc.fit(X[i::skip], Y[i::skip])
    rfc.n_estimators += 3

target_predicted = rfc.predict(X_test)
print(target_predicted.min(),target_predicted.max())
print("y test mean: ",y_test.mean()," y test var: ", y_test.var())
print("Random Forest MSE:",mean_squared_error(y_test, target_predicted))
