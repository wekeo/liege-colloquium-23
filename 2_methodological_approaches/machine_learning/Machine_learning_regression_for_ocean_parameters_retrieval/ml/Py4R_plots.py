__author__ = 'Ana Ruescas, Gonzalo Mateo-García'

""" Plots that can be done with the result of the Py4R ML regression methods:
    1. boxplots of the spectrum for summary of info
    2. correlative plot: scatter plots + annotations
    3. partial plots
    4. permutation plots
    5. boxplots of error by model   
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import scipy as sp
from sklearn.metrics import mean_absolute_error

def correlative_plot(preds, measured,ax=None,s=10):
    """
    Correlative plot
    Correlative plot prediction vs. measured: as validation plot using linear regression;
    (also useful for residual vs. measured)
    Inputs:  and measured (y_test) data
    Results from models are stored in:
     predictions = pd.DataFrame(predictions).T
     predictions.to_csv(name_bands + "_preds.csv", index=False)
    :param preds: two arrays with predictions (preds)
    :param measured:
    :param ax:
    :param s:
    :return:
    """

    slope, intercept, r_value, p_value, std_err = sp.stats.linregress(measured, preds)

    a = str("{0:.5f}".format(slope))
    b = str("{0:.5f}".format(intercept))
    c = str("{0:.5f}".format(r_value))
    d = str("{0:.1E}".format(std_err))

    if ax is None:
        ax = plt.gca()

    ax.scatter(measured, preds,s=s)
    ax.set_ylabel("WQ predicted", fontsize=15)
    ax.set_xlabel("WQ measured", fontsize=15)
    ax.xaxis.grid(color='lightgrey', linestyle='dashed')
    ax.yaxis.grid(color='lightgrey', linestyle='dashed')
    ax.patch.set_facecolor('white')
    ax.set(ylim=(0, 60), xlim=(0, 60))
    #ax.set_title("Validation", fontsize=25) #example
    ax.plot(ax.get_xlim(), ax.get_ylim(), ls="--", c="lightgrey")


        ## Annotate plot with regression formula -->
    #ax.text(0.2, np.max(preds)-4, r'$y=$' + a + r'$x$' + b, ha='left', fontsize=15)
    #ax.text(0.2, np.max(preds)-8, r'$r=$' + c, ha='left', fontsize=15)
    #ax.text(0.2, np.max(preds)-12, r'$error=$' + d, ha='left', fontsize=15)


def regression_plot(x_train, x_test, y_train, y_test, models_predict, mean_y_train=0, ax=None):
    if ax is None:
        ax = plt.gca()

    rango_x = np.linspace(np.min((np.min(x_test), np.min(x_train))),
                          np.max((np.max(x_test), np.max(x_train))), 200)
    i = 0
    for model_name, model in models_predict:
        if model_name == "GPR":
            min_max_scaler_ = model.steps[0][1]
            gpr_model_ = model.steps[1][1]
            yp, y_std = gpr_model_.predict(min_max_scaler_.transform(rango_x[:, np.newaxis]),
                                           return_std=True)
            yp += mean_y_train
            ax.fill_between(rango_x, yp - 1.96 * y_std, yp + 1.96 * y_std,
                            alpha=0.2, color="C%d" % i)
        else:
            yp = model.predict(rango_x[:, np.newaxis])
            yp += mean_y_train
        ax.plot(rango_x, yp, label=model_name)
        i += 1

    ax.scatter(x_test, y_test, s=15, label="test", alpha=.5,c="C%d"%i)
    ax.scatter(x_train, y_train, s=15, label="train", alpha=.5,c="C%d"%(i+1))
    ax.patch.set_facecolor('white')
    ax.set_ylabel("WQ predicted", fontsize=15)
    ax.set_xlabel("Ratio", fontsize=15)


def permutation_test(model,X,y, function_error=mean_absolute_error,P=30):
    salida = pd.DataFrame(columns=X.columns, data=np.ndarray((P, X.shape[1])))
    # print("Error inicial: %.3f"%(function_error(model.predict(X),y)))
    for col in X.columns:
        error = np.ndarray((P,))
        X_copia = X.copy()
        for i in range(P):
            x_datos = np.array(X_copia[col])
            x_datos = x_datos[np.random.permutation(X.shape[0])]
            X_copia[col] = x_datos
            y_pred = model.predict(X_copia)
            error[i] = function_error(y, y_pred)
        salida[col] = error
    return pd.melt(salida,value_name=function_error.__name__)
