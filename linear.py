import importlib
import numpy as np
import game
importlib.reload(game)
from game import ColorableCliqueGame
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
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
index = 45000
print("player turn:", X[45000][-1])
colors = [(255,100,100), (100,100,255)]
env = ColorableCliqueGame(300,300,6, colors)
Y = np.tanh(Y)


X_train,X_test,y_train,y_test =train_test_split(X,Y , test_size=0.20, random_state=42,shuffle=True)

lin_reg = LinearRegression()
lin_reg.fit(X_train,y_train)
lin_pred_test = lin_reg.predict(X_test)
lin_pred_train = lin_reg.predict(X_train)
r2_test = r2_score(y_test,lin_pred_test)
r2_train = r2_score(y_train,lin_pred_train)
print('R squared of Linear Regression for Test Date :', r2_test)
print('R squared of Linear Regression for Train Date :', r2_train)

print(Y.min(), Y.max(), Y.mean())

Y /= Y.max()
print(Y.min(), Y.max(), Y.mean())

target_predicted = lin_reg.predict(X_test)
print("y test mean: ",y_test.mean(), " y test var: ",y_test.var())
print("Linear Regression MSE:",mean_squared_error(y_test, target_predicted))

