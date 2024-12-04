import pandas as pd
import numpy as np

from matplotlib import pyplot as pl

from sklearn.model_selection import cross_validate # for cross validation
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix

import joblib
import gzip

##############################################
# Funções para converter e reverter a escala 
###

def scale01(x):
    return (x - x.min())/(x.max() - x.min())

def unscale01(x, lower, upper):
    #return (x * (upper - lower)) + lower
    return (x * upper) - ((x - 1.0) * lower)

#############################################


# Leitura dos dados
df = pd.read_csv('/app/training/training.data', delimiter=';')

data = np.array(df.values[: , 2:], dtype = float)   # Pandas dtype = object, logo tudo é permitido
(N, d) = data.shape

print(N, 'x', d)

# Primeiro, agregar de várias fontes e fazer alinhamento entre os dados
# Neste caso nada a fazer

# Segundo, fazer alguns pre-processamentos: Scaling? missing rows? missing values? outliers?

# Scaling

# keep to revert numbers back to the original range and scale
minv = data.min(0)
maxv = data.max(0)

print(data.min(0))
print(data.max(0))

for var in range(1, 7):
    data[:, var] = scale01(data[:, var])

print()
print(data.min(0))
print(data.max(0))

# Reverter para a escala e gama original 
#data2 = data.copy()
#for var in range(1, 7):
#    data2[:, var] = unscale01(data[:, var], minv[var], maxv[var])
#
#print(data2.min(0))
#print(data2.max(0))

# missing rows não é problema
# missing values?
print()
print(np.isfinite(data[:,0]).all())

# Vamos separar entrada e saída dos modelos

# Entradas são as carateristicas ou variáveis (features) dos dados que medimos e que podem explicar
# as classes da saída

inputs = data[:, 1:] # Neste caso todas as linhas desde a segunda coluna até à última

# A saída representa as classes que pretendemos prever.
# No nosso caso temos duas classes (walk, run - nos dados 0, 1)

output = data[:, 0]

# Separamos os dados com 70% para treinar e 30% para avaliar os modelos

inputs_train, inputs_test, output_train, output_test = train_test_split(inputs,
                                                                        output,
                                                                        test_size = 0.3,
                                                                        shuffle = True)

# Vamos tentar um modelo com K Nearest Neighbors

KNN = KNeighborsClassifier(n_neighbors = 6, weights = 'distance') # weights = 'univform'
KNN.fit(inputs_train, output_train)

# Vejamos a accuracy média nos dados de teste
print('Accuracy:', KNN.score(inputs_test, output_test))

# Vejamos o score F1
output_predicted = KNN.predict(inputs_test)
print('F1-score:', f1_score(output_test, output_predicted))
print('Confusion matrix:')
print(confusion_matrix(output_test, output_predicted, labels = [0.0, 1.0]))

# Export model
joblib.dump(KNN, gzip.open('model/knn-model.dat.gz', "wb"))
