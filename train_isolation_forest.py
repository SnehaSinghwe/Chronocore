"""
train_isolation_forest.py
--------------------------
Loads labeled_dataset.json, trains IsolationForest on normal data only,
evaluates on the full test set, and saves the trained model.
"""

import json
import numpy as np
import joblib
import os
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import StandardScaler

os.makedirs("data", exist_ok=True)
os.makedirs("models", exist_ok=True)

# ── 1. Load dataset ───────────────────────────────────────────────────────────

with open("data/labeled_dataset.json") as f:
    records = json.load(f)

features   = ["fan_1_speed", "fan_2_speed", "temperature"]
X          = np.array([[r[k] for k in features] for r in records])
y_true     = np.array([r["label"] for r in records])  # 0=normal, 1=anomaly
anom_types = [r["anomaly_type"] for r in records]

# ── 2. Split — fit on normal samples only (semi-supervised) ──────────────────

X_normal = X[y_true == 0]
# Full dataset is the test set (both classes)
X_test   = X
y_test   = y_true

scaler = StandardScaler()
X_normal_scaled = scaler.fit_transform(X_normal)
X_test_scaled   = scaler.transform(X_test)

# ── 3. Train IsolationForest ──────────────────────────────────────────────────

# contamination = expected fraction of anomalies in the *scoring* set
contamination = round(200 / 500, 2)  # 0.40

clf = IsolationForest(
    n_estimators=200,
    contamination=contamination,
    max_samples="auto",
    random_state=42,
    n_jobs=-1,
)
clf.fit(X_normal_scaled)  # fit on NORMAL data only

# ── 4. Predict ────────────────────────────────────────────────────────────────

raw_pred   = clf.predict(X_test_scaled)          # +1 normal, -1 anomaly
y_pred     = np.where(raw_pred == -1, 1, 0)      # convert to 0/1
scores     = -clf.score_samples(X_test_scaled)   # higher = more anomalous

# ── 5. Evaluate ───────────────────────────────────────────────────────────────

print("=" * 60)
print("  IsolationForest — Anomaly Detection Report")
print("=" * 60)
print(f"\nFeatures used : {features}")
print(f"Train size    : {len(X_normal)} (normal only)")
print(f"Test size     : {len(X_test)} (normal + anomalous)")
print(f"Contamination : {contamination}\n")

print("── Classification Report ──────────────────────────────────")
print(classification_report(y_test, y_pred, target_names=["Normal", "Anomaly"]))

cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()
print("── Confusion Matrix ───────────────────────────────────────")
print(f"             Predicted Normal  Predicted Anomaly")
print(f"Actual Normal       {tn:>5}              {fp:>5}")
print(f"Actual Anomaly      {fn:>5}              {tp:>5}\n")

auc = roc_auc_score(y_test, scores)
print(f"ROC-AUC Score : {auc:.4f}\n")

# Per anomaly-type breakdown
print("── Per Anomaly-Type Breakdown ─────────────────────────────")
from collections import defaultdict
type_stats = defaultdict(lambda: {"total": 0, "detected": 0})
for i, kind in enumerate(anom_types):
    if kind != "none":
        type_stats[kind]["total"]   += 1
        type_stats[kind]["detected"] += int(y_pred[i] == 1)

for kind, stat in sorted(type_stats.items()):
    recall = stat["detected"] / stat["total"] * 100
    print(f"  {kind:<15}  detected {stat['detected']:>3}/{stat['total']:<3}  ({recall:.0f}%)")

# ── 6. Save model & scaler ────────────────────────────────────────────────────

joblib.dump(clf,    "models/isolation_forest.pkl")
joblib.dump(scaler, "models/scaler.pkl")
print("\n✅  Model saved → models/isolation_forest.pkl")
print("✅  Scaler saved → models/scaler.pkl")
