import numpy as np
def rmse(a, b): a, b = np.asarray(a, float), np.asarray(b, float); return float(np.sqrt(np.mean((a - b) ** 2)))
def bias(a, b): return float(np.mean(np.asarray(a, float) - np.asarray(b, float)))
def corr(a, b): return float(np.corrcoef(a, b)[0, 1])
def r2(y, yhat): y, yhat = np.asarray(y, float), np.asarray(yhat, float); return float(1 - ((y - yhat) ** 2).sum() / ((y - y.mean()) ** 2).sum())
