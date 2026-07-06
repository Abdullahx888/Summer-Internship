import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb

# 1. Load the extracted features spreadsheet
df = pd.read_csv('extracted_features.csv')

# Define target labels and structural linguistic feature subsets
X_text = df['raw_text']
y = df['label']

linguistic_cols = [
    'believability', 'sentence_length_total', 'clause_count', 
    'avg_parse_depth', 'max_parse_depth', 'q1_type', 'q2_type', 'qc_type', 
    'p1_negations', 'p2_negations', 'c_negations', 'total_negations', 
    'lexical_overlap', 'entity_freq_p1', 'entity_freq_c', 'semantic_similarity'
]
X_ling = df[linguistic_cols]

# 2. Train/Test Splits (keeping the random split state identical across models for a fair test)
X_text_train, X_text_test, y_train, y_test = train_test_split(X_text, y, test_size=0.2, random_state=42)
X_ling_train, X_ling_test, _, _ = train_test_split(X_ling, y, test_size=0.2, random_state=42)

print("="*60)
print(f" TRAINING PIPELINE STARTED: 80% Train ({len(y_train)}), 20% Test ({len(y_test)})")
print("="*60)

# ---------------------------------------------------------
# STRATEGY 1: TEXT-ONLY BASELINE (TF-IDF -> SVM)
# ---------------------------------------------------------
print("\n[Strategy 1] Training Text Baseline (TF-IDF -> SVM)...")
tfidf = TfidfVectorizer(max_features=500)
X_text_train_vec = tfidf.fit_transform(X_text_train)
X_text_test_vec = tfidf.transform(X_text_test)

svm_model = SVC(kernel='linear', random_state=42)
svm_model.fit(X_text_train_vec, y_train)
svm_preds = svm_model.predict(X_text_test_vec)
svm_acc = accuracy_score(y_test, svm_preds)

# ---------------------------------------------------------
# STRATEGY 2: LINGUISTIC FEATURES ONLY
# ---------------------------------------------------------
print("\n[Strategy 2] Training Linguistic Only Classifiers...")
# Standardize numerical spreads for tree safety
scaler = StandardScaler()
X_ling_train_scaled = scaler.fit_transform(X_ling_train)
X_ling_test_scaled = scaler.transform(X_ling_test)

# Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_ling_train_scaled, y_train)
rf_preds = rf_model.predict(X_ling_test_scaled)
rf_acc = accuracy_score(y_test, rf_preds)

# XGBoost
xgb_ling = xgb.XGBClassifier(n_estimators=100, eval_metric='logloss', random_state=42)
xgb_ling.fit(X_ling_train_scaled, y_train)
xgb_preds = xgb_ling.predict(X_ling_test_scaled)
xgb_acc = accuracy_score(y_test, xgb_preds)

# ---------------------------------------------------------
# STRATEGY 3: HYBRID ML MODELS (TEXT + LINGUISTIC FEATURES)
# ---------------------------------------------------------
print("\n[Strategy 3] Training Hybrid Classifiers (TF-IDF + Linguistics)...")

# Combine sparse text matrices with dense numerical arrays safely
X_hybrid_train = np.hstack((X_text_train_vec.toarray(), X_ling_train_scaled))
X_hybrid_test = np.hstack((X_text_test_vec.toarray(), X_ling_test_scaled))

# Hybrid Logistic Regression
lr_hybrid = LogisticRegression(max_iter=1000, random_state=42)
lr_hybrid.fit(X_hybrid_train, y_train)
lr_preds = lr_hybrid.predict(X_hybrid_test)
lr_acc = accuracy_score(y_test, lr_preds)

# Hybrid XGBoost
xgb_hybrid = xgb.XGBClassifier(n_estimators=100, eval_metric='logloss', random_state=42)
xgb_hybrid.fit(X_hybrid_train, y_train)
xgb_hybrid_preds = xgb_hybrid.predict(X_hybrid_test)
xgb_hybrid_acc = accuracy_score(y_test, xgb_hybrid_preds)

# =========================================================
# FINAL SYSTEM PERFORMANCE COMPARISON
# =========================================================
print("\n" + "="*60)
print("             FINAL MODEL PERFORMANCE METRICS              ")
print("="*60)
print(f"1. Text-Only Baseline (TF-IDF -> SVM):             {svm_acc*100:.2f}% Accuracy")
print("-" * 60)
print(f"2. Linguistic-Only -> Random Forest:               {rf_acc*100:.2f}% Accuracy")
print(f"3. Linguistic-Only -> XGBoost:                     {xgb_acc*100:.2f}% Accuracy")
print("-" * 60)
print(f"4. Hybrid Features -> Logistic Regression:          {lr_acc*100:.2f}% Accuracy")
print(f"5. Hybrid Features -> XGBoost:                      {xgb_hybrid_acc*100:.2f}% Accuracy")
print("="*60)

print("\nDetailed Performance for Top Hybrid XGBoost Model:")
print(classification_report(y_test, xgb_hybrid_preds, target_names=['Invalid (0)', 'Valid (1)']))