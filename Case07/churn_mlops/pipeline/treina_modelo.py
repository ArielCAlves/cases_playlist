from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
import numpy as np
import joblib
import os

def treina_modelo(X_train, y_train, save_path="modelos"):
    model = RandomForestClassifier()
    param_dist = {
        'n_estimators': [int(x) for x in np.linspace(10, 200, 10)],
        'max_features': ['sqrt', 'log2'],
        'max_depth': [int(x) for x in np.linspace(10, 100, 10)],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'bootstrap': [True, False]
    }
    search = RandomizedSearchCV(
                                model,
                                param_distributions=param_dist,
                                n_iter=100,
                                cv=3,
                                scoring='accuracy',
                                n_jobs=-1
                                )
    search.fit(X_train, y_train)
    best_model = search.best_estimator_
    os.makedirs(save_path, exist_ok=True)
    joblib.dump(best_model, os.path.join(save_path, "model_rf.pkl"))
    return best_model