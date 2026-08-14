import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

import joblib



# ==========================================
# CARREGAR SRM
# ==========================================

X = np.load(
    "X_SRM.npy"
)

y = np.load(
    "y_SRM.npy"
)


print("Características:", X.shape)
print("Classes:", y.shape)



# ==========================================
# SEPARAR TREINO E TESTE
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42,

    stratify=y

)



# ==========================================
# NORMALIZAÇÃO
# ==========================================

scaler = StandardScaler()


X_train = scaler.fit_transform(
    X_train
)


X_test = scaler.transform(
    X_test
)



# ==========================================
# TREINAR SVM
# ==========================================

modelo = SVC(

    kernel="rbf",

    C=10,

    gamma="scale",

    probability=True

)


modelo.fit(

    X_train,

    y_train

)



# ==========================================
# TESTE
# ==========================================

y_pred = modelo.predict(
    X_test
)



# ==========================================
# MÉTRICAS
# ==========================================

acc = accuracy_score(

    y_test,

    y_pred

)


relatorio = classification_report(

    y_test,

    y_pred,

    target_names=[
        "Cover",
        "Stego"
    ],

    output_dict=True

)



matriz = confusion_matrix(

    y_test,

    y_pred

)



print("\n================================")
print("        RESULTADOS SVM")
print("================================")


print(
    f"Acurácia: {acc*100:.2f}%"
)


print(
    f"Precisão Cover: {relatorio['Cover']['precision']*100:.2f}%"
)


print(
    f"Recall Cover: {relatorio['Cover']['recall']*100:.2f}%"
)


print(
    f"Precisão Stego: {relatorio['Stego']['precision']*100:.2f}%"
)


print(
    f"Recall Stego: {relatorio['Stego']['recall']*100:.2f}%"
)


print(
    f"F1-score: {relatorio['weighted avg']['f1-score']*100:.2f}%"
)


print("\nMatriz de confusão:")

print(matriz)



# ==========================================
# SALVAR MODELO
# ==========================================

joblib.dump(

    modelo,

    "modelo_svm.pkl"

)


joblib.dump(

    scaler,

    "scaler.pkl"

)



print("\n================================")
print("Arquivos salvos com sucesso:")
print("✓ modelo_svm.pkl")
print("✓ scaler.pkl")
print("================================")