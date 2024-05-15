import pandas as pd 
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go 
from matplotlib.pyplot import (subplots, scatter, figure, title, show, xlabel, ylabel, legend, contourf, colorbar, subplots_adjust )
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import (train_test_split,GridSearchCV, StratifiedKFold, KFold )
from sklearn.tree import (_tree
                          ,plot_tree,
                          DecisionTreeClassifier as DTC)
from sklearn.ensemble import RandomForestClassifier,BaggingClassifier, AdaBoostClassifier
from ISLP.bart import BART
from sklearn.impute import SimpleImputer 
import seaborn as sb 
from sklearn.linear_model import (LinearRegression ,RidgeCV ,LassoCV ) 
from sklearn.decomposition import PCA 
from sklearn.pipeline import make_pipeline 
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score,mean_squared_error, mean_absolute_error
from sklearn.feature_selection import RFECV  

from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier 
from mpl_toolkits.mplot3d import Axes3D

# Load the Lung Cancer dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/lung-cancer/lung-cancer.data"
column_names = ['diagnosis', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15']
df = pd.read_csv(url, names=column_names)

# Drop rows with missing values
df.replace('?', np.nan, inplace=True)
df.dropna(inplace=True)

# Separate features and target variable
X = df.drop('diagnosis', axis=1) 
y = df['diagnosis'] 

# Classification Tree: 
# Decision Tree Classifier (criterion='gini') 
# Grid Search
param_grid= {'ccp_alpha': np.linspace(0, 0.1, 5),
             'max_depth': [None, 3, 5]
             }  
tree_clf = DTC(random_state=0) 
cv = StratifiedKFold(n_splits=5,shuffle=True, random_state=0)  
grid_search = GridSearchCV(tree_clf, param_grid, cv= cv)  
grid_search.fit(X,y) 

best_alpha = grid_search.best_params_['ccp_alpha']  
best_depth = grid_search.best_params_['max_depth']
print("Best Cost-complexity pruning alpha:", best_alpha) 

# Fit a decision tree clf with ccp 
tree_clf = DTC(ccp_alpha= best_alpha, max_depth= best_depth) 
tree_clf.fit(X, y) 

# Get feature importaances 
importances = tree_clf.feature_importances_ 

# Get indicies of top two features 
top_indicies = np.argsort(importances)[-2:]
top_features_name = [ column_names[1:][i] for i in top_indicies]
X_top = X.iloc[:, top_indicies] 

# Plot training points
fig = figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='3d') 
ax.view_init(elev=90, azim=60)
ax.scatter(X_top.iloc[:, 0], X_top.iloc[:, 1], y, c=y, cmap='viridis', label='Data') 


# Plot the decision surface 
x_min, x_max = X_top.iloc[:, 0].min() -1, X_top.iloc[:, 0].max() +1 
y_min, y_max = X_top.iloc[:, 1].min() -1, X_top.iloc[:, 1].max() +1  
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1), np.arange(y_min, y_max, 0.1))  

# Create Dummy data for reduced feature space 
dummy_X = np.zeros((xx.ravel().shape[0], 15))  
dummy_X[:, top_indicies] = np.c_[ xx.ravel(), yy.ravel() ] 

# Predict the output for each point in the mesh grid 
Z = tree_clf.predict( dummy_X )  
Z = Z.reshape(xx.shape) 

# Using plotly 
# Assuming X_top and y are your data frames
fig = px.scatter_3d(X_top, x=X_top.columns[0], y=X_top.columns[1], z=y, color=y)
fig.show()

# Plot the decision surface 
x_min, x_max = X_top.iloc[:, 0].min() -1, X_top.iloc[:, 0].max() +1 
y_min, y_max = X_top.iloc[:, 1].min() -1, X_top.iloc[:, 1].max() +1  
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1), np.arange(y_min, y_max, 0.1))  

# Create Dummy data for reduced feature space 
dummy_X = np.zeros((xx.ravel().shape[0], 15))  
dummy_X[:, top_indicies] = np.c_[ xx.ravel(), yy.ravel() ] 

# Predict the output for each point in the mesh grid 
Z = tree_clf.predict( dummy_X )  
Z = Z.reshape(xx.shape) 

# Create the 3D surface plot
fig2 = go.Figure(data=[go.Surface(x=xx, y=yy, z=Z, colorscale='Viridis')])

# Set the layout and axis labels
fig2.update_layout(
    title='Prediction Surface of the Decision Tree',
    scene=dict(
        xaxis_title=top_features_name[0],
        yaxis_title=top_features_name[1],
        zaxis_title='Prediction'
    ) 
)  

fig2.show() 



