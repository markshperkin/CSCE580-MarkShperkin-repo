#written by Mark Shperkin
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

data = pd.read_csv('german.data-numeric', header=None, delimiter=r'\s+')

X = data.iloc[:, :-1]
y = data.iloc[:, -1]

label_encoders = []
for col in X.columns:
    if X[col].dtype == 'object':
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders.append(le)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

dt_classifier = DecisionTreeClassifier(random_state=42)
dt_classifier.fit(X_train, y_train)

rf_classifier = RandomForestClassifier(random_state=42)
rf_classifier.fit(X_train, y_train)

dt_predictions = dt_classifier.predict(X_test)
rf_predictions = rf_classifier.predict(X_test)

dt_accuracy = accuracy_score(y_test, dt_predictions)
dt_confusion_matrix = confusion_matrix(y_test, dt_predictions)
dt_classification_report = classification_report(y_test, dt_predictions)

rf_accuracy = accuracy_score(y_test, rf_predictions)
rf_confusion_matrix = confusion_matrix(y_test, rf_predictions)
rf_classification_report = classification_report(y_test, rf_predictions)

print("Decision Tree Classifier:")
print("Accuracy:", dt_accuracy)
print("Confusion Matrix:")
print(dt_confusion_matrix)
print("Classification Report:")
print(dt_classification_report)

print("\n" + "-"*50 + "\n")

print("\nRandom Forest Classifier:")
print("Accuracy:", rf_accuracy)
print("Confusion Matrix:")
print(rf_confusion_matrix)
print("Classification Report:")
print(rf_classification_report)

from lime.lime_tabular import LimeTabularExplainer

explainer_dt = LimeTabularExplainer(X_train, mode="classification", training_labels=y_train, discretize_continuous=False)

explainer_rf = LimeTabularExplainer(X_train, mode="classification", training_labels=y_train, discretize_continuous=False)

print("\n" + "-"*50 + "\n")


print("Attribute: gender\n")
attribure_to_explain = X_test[9]

explanation_dt = explainer_dt.explain_instance(attribure_to_explain, dt_classifier.predict_proba)
explanation_text_dt = explanation_dt.as_list()

explanation_rf = explainer_rf.explain_instance(attribure_to_explain, rf_classifier.predict_proba)
explanation_text_rf = explanation_rf.as_list()

formatted_results_dt = [f"Decision Tree: Feature {idx}: {score:.3f}" for idx, score in explanation_text_dt]
formatted_results_rf = [f"Random Forest: Feature {idx}: {score:.3f}" for idx, score in explanation_text_rf]

print("LIME Explanation for Decision Tree Classifier :")
print("\n".join(formatted_results_dt))

print("\nLIME Explanation for Random Forest Classifier:")
print("\n".join(formatted_results_rf))


print("\n" + "-"*50 + "\n")

print("Attribute: age\n")
attribure_to_explain = X_test[13]

explanation_dt = explainer_dt.explain_instance(attribure_to_explain, dt_classifier.predict_proba)
explanation_text_dt = explanation_dt.as_list()

explanation_rf = explainer_rf.explain_instance(attribure_to_explain, rf_classifier.predict_proba)
explanation_text_rf = explanation_rf.as_list()

formatted_results_dt = [f"Decision Tree: Feature {idx}: {score:.3f}" for idx, score in explanation_text_dt]
formatted_results_rf = [f"Random Forest: Feature {idx}: {score:.3f}" for idx, score in explanation_text_rf]

print("LIME Explanation for Decision Tree Classifier :")
print("\n".join(formatted_results_dt))

print("\nLIME Explanation for Random Forest Classifier:")
print("\n".join(formatted_results_rf))



data_points_to_explain = [X_test[0], X_test[1], X_test[2], X_test[3], X_test[4]]
print("\n" + "-"*50 + "\n")

for i, instance_to_explain in enumerate(data_points_to_explain):
    explanation_dt = explainer_dt.explain_instance(instance_to_explain, dt_classifier.predict_proba)
    explanation_text_dt = explanation_dt.as_list()

    explanation_rf = explainer_rf.explain_instance(instance_to_explain, rf_classifier.predict_proba)
    explanation_text_rf = explanation_rf.as_list()

    print(f"Data Point {i+1}:")
    print("LIME Explanation for Decision Tree Classifier:")
    print("\n".join([f"Feature {idx}: {score:.3f}" for idx, score in explanation_text_dt]))

    print("\nLIME Explanation for Random Forest Classifier:")
    print("\n".join([f"Feature {idx}: {score:.3f}" for idx, score in explanation_text_rf]))

    print("\n" + "-"*50 + "\n")






