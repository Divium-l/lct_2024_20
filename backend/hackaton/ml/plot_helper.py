import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from scipy.stats import probplot



def plotHist(data, column, title="Гистограммы распределения"):
    fig = plt.figure(figsize=(10,10))
    st = fig.suptitle(title + " " + str(column))

    plt.subplot(2, 2, 1)
    data[column[0]].hist(edgecolor='black', linewidth=1.2, density=True)

    plt.subplot(2, 2, 2)
    data[column[1]].hist(edgecolor='black', linewidth=1.2, density=True)

    
    plt.subplot(2, 2, 3)
    data[column[2]].hist(edgecolor='black', linewidth=1.2, density=True)
    
    plt.subplot(2, 2, 4)
    data[column[3]].hist(edgecolor='black', linewidth=1.2, density=True)
    
    plt.show()


def plotsDataDenepnds(data, col, metka, num_interval=10, width=10):
    currData = data[[col, metka]].copy()
    currData['bal_bin'], bal_bins = pd.cut(currData[col], num_interval, retbins=True)
    df_gr = currData[[col, metka, 'bal_bin']].groupby('bal_bin')[metka].mean().fillna(0.)
    
    plt.figure(figsize=(30,10))
    plt.bar(bal_bins[1:][:], df_gr.iloc[:], width=width)
    plt.xlabel('Значение прзнака - ' + col)
    plt.ylabel('Значение метки - ' + metka)
    plt.grid(True)
    plt.title('Зависимость нарушений от исследуемого признака')
    plt.show()
    
def plotTableAUCRoc(model, X_test, y_test, thresholder=0.5, typeModel="catboost", normalize=True, plot_savefig=None):
    """
    Отрисовка ROC-кривой и матрицы неточностей
        Входные параметры:
            model       - модель
            X_test      - тестовая выборка
            y_test      - тестовые метки
            thresholder - порог для классификации

        Выходные параметры:
           ---
    """    
    # Расчёт матрицы неточностей
    if typeModel == "catboost":
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        y_pred = (y_pred_proba > thresholder).astype(int)
    cnf_matrix = confusion_matrix(y_test, y_pred)
    f1_score = metrics.f1_score(y_test, y_pred)
    print("F1 = ", f1_score)
    
    # Расчёт метрики AUC-RIOC
    fpr, tpr, _ = metrics.roc_curve(y_test, y_pred_proba)
    auc = metrics.roc_auc_score(y_test, y_pred_proba)
    
    # Отрисовка графика
    plt.rcParams.update({'font.size': 22})
    plt.figure(figsize=(30,10))
    plt.subplot(121)
    mat = plot_confusion_matrix(
        cnf_matrix, classes=["Без нарушения", "С нарушением"], 
        normalize=normalize, plot_savefig=plot_savefig,
        title='')
    plt.title("Матрица ошибок", fontsize=30)
    plt.subplot(122)
    plt.plot(fpr,tpr,label="Тестовая выборка по машинистам, AUC="+str(auc))
    plt.legend(loc=4)
    plt.grid(True)
    plt.title("ROC-кривая", fontsize=30)
    plt.show()
    return auc, f1_score
    
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Матрица неточностей',
                          cmap=plt.cm.Blues, plot_savefig=None):
    """
    Отрисовка матрцы неточностей
        Входные параметры:
            cm        - матрица неточностей
            classes   - классы
            normalize - нормализация
            title     - заголовок изображения
            cmap      - карта цветов

        Выходные параметры:
           ---
    """    
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes)
    
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center", fontsize=30,
                 color="white" if cm[i, j] > thresh else "black")
    
    plt.ylabel('Факт')
    plt.xlabel('Прогноз')
    plt.tight_layout()
    if plot_savefig:
        plt.savefig(plot_savefig, dpi=300, bbox_inches='tight')
    

def plot_qq(data_feature_false, data_feature_true, feature):
    """
        Функция отображения QQ-графика.
        Input params:
            data_feature_false - дата с меткой 0;
            data_feature_true - дата с меткой 1.
        Return:
            None.
    """
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    probplot(data_feature_false[feature], dist="norm", plot=plt)
    plt.title("$Отсутствие грубого нарушения$")
    plt.subplot(1, 2, 2)
    probplot(data_feature_true[feature], dist="norm", plot=plt)
    plt.title("$Факт совершения грубого нарушения$")
    plt.tight_layout()
    plt.show()  
