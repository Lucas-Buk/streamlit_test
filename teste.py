import pickle

with open('ob_cancer_models.pkl', 'rb') as f:
    models = pickle.load(f)
models

# xgb = models['xgboost']
# enc = models['encoder']
# norm = models['normalizer']