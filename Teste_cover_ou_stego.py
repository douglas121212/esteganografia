import numpy as np
import cv2
import joblib

from tkinter import Tk
from tkinter.filedialog import askopenfilename


# ==========================================
# CARREGAR MODELO TREINADO
# ==========================================

modelo = joblib.load(
    "modelo_svm.pkl"
)

scaler = joblib.load(
    "scaler.pkl"
)


# ==========================================
# FILTROS SRM
# ==========================================

filter_class_1 = [

np.array([
[1,0,0],
[0,-1,0],
[0,0,0]
],dtype=np.float32),

np.array([
[0,1,0],
[0,-1,0],
[0,0,0]
],dtype=np.float32),

np.array([
[0,0,1],
[0,-1,0],
[0,0,0]
],dtype=np.float32),

np.array([
[0,0,0],
[1,-1,0],
[0,0,0]
],dtype=np.float32),

np.array([
[0,0,0],
[0,-1,1],
[0,0,0]
],dtype=np.float32),

np.array([
[0,0,0],
[0,-1,0],
[1,0,0]
],dtype=np.float32),

np.array([
[0,0,0],
[0,-1,0],
[0,1,0]
],dtype=np.float32),

np.array([
[0,0,0],
[0,-1,0],
[0,0,1]
],dtype=np.float32)

]


filter_class_2 = [

np.array([
[1,0,0],
[0,-2,0],
[0,0,1]
],dtype=np.float32),

np.array([
[0,1,0],
[0,-2,0],
[0,1,0]
],dtype=np.float32),

np.array([
[0,0,1],
[0,-2,0],
[1,0,0]
],dtype=np.float32),

np.array([
[0,0,0],
[1,-2,1],
[0,0,0]
],dtype=np.float32)

]


filter_class_3 = [

np.array([
[-1,0,0,0,0],
[0,3,0,0,0],
[0,0,-3,0,0],
[0,0,0,1,0],
[0,0,0,0,0]
],dtype=np.float32),

np.array([
[0,0,-1,0,0],
[0,0,3,0,0],
[0,0,-3,0,0],
[0,0,1,0,0],
[0,0,0,0,0]
],dtype=np.float32),

np.array([
[0,0,0,0,-1],
[0,0,0,3,0],
[0,0,-3,0,0],
[0,1,0,0,0],
[0,0,0,0,0]
],dtype=np.float32),

np.array([
[0,0,0,0,0],
[0,0,0,0,0],
[0,1,-3,3,-1],
[0,0,0,0,0],
[0,0,0,0,0]
],dtype=np.float32),

np.array([
[0,0,0,0,0],
[0,1,0,0,0],
[0,0,-3,0,0],
[0,0,0,3,0],
[0,0,0,0,-1]
],dtype=np.float32),

np.array([
[0,0,0,0,0],
[0,0,1,0,0],
[0,0,-3,0,0],
[0,0,3,0,0],
[0,0,-1,0,0]
],dtype=np.float32),

np.array([
[0,0,0,0,0],
[0,0,0,1,0],
[0,0,-3,0,0],
[0,3,0,0,0],
[-1,0,0,0,0]
],dtype=np.float32),

np.array([
[0,0,0,0,0],
[0,0,0,0,0],
[-1,3,-3,1,0],
[0,0,0,0,0],
[0,0,0,0,0]
],dtype=np.float32)

]


# ==========================================
# FILTROS RESTANTES SRM
# ==========================================

filter_edge_3x3 = [

np.array([
[-1,2,-1],
[2,-4,2],
[0,0,0]
],dtype=np.float32),

np.array([
[0,2,-1],
[0,-4,2],
[0,2,-1]
],dtype=np.float32),

np.array([
[0,0,0],
[2,-4,2],
[-1,2,-1]
],dtype=np.float32),

np.array([
[-1,2,0],
[2,-4,0],
[-1,2,0]
],dtype=np.float32)

]


filter_edge_5x5 = [

np.array([
[-1,2,-2,2,-1],
[2,-6,8,-6,2],
[-2,8,-12,8,-2],
[0,0,0,0,0],
[0,0,0,0,0]
],dtype=np.float32),

np.array([
[0,0,-2,2,-1],
[0,0,8,-6,2],
[0,0,-12,8,-2],
[0,0,8,-6,2],
[0,0,-2,2,-1]
],dtype=np.float32),

np.array([
[0,0,0,0,0],
[0,0,0,0,0],
[-2,8,-12,8,-2],
[2,-6,8,-6,2],
[-1,2,-2,2,-1]
],dtype=np.float32),

np.array([
[-1,2,-2,0,0],
[2,-6,8,0,0],
[-2,8,-12,0,0],
[2,-6,8,0,0],
[-1,2,-2,0,0]
],dtype=np.float32)

]


square_3x3 = np.array([

[-1,2,-1],
[2,-4,2],
[-1,2,-1]

],dtype=np.float32)


square_5x5 = np.array([

[-1,2,-2,2,-1],
[2,-6,8,-6,2],
[-2,8,-12,8,-2],
[2,-6,8,-6,2],
[-1,2,-2,2,-1]

],dtype=np.float32)


# ==========================================
# NORMALIZAÇÃO DOS FILTROS
# ==========================================

normalized_filter_class_2 = [
    hpf / 2 for hpf in filter_class_2
]

normalized_filter_class_3 = [
    hpf / 3 for hpf in filter_class_3
]

normalized_filter_edge_3x3 = [
    hpf / 4 for hpf in filter_edge_3x3
]

normalized_filter_edge_5x5 = [
    hpf / 12 for hpf in filter_edge_5x5
]

normalized_square_3x3 = square_3x3 / 4

normalized_square_5x5 = square_5x5 / 12


# ==========================================
# CONJUNTO FINAL SRM
# ==========================================

all_normalized_hpf_list = (

    filter_class_1
    +
    normalized_filter_class_2
    +
    normalized_filter_class_3
    +
    normalized_filter_edge_3x3
    +
    normalized_filter_edge_5x5
    +
    [
        normalized_square_3x3,
        normalized_square_5x5
    ]

)


# ==========================================
# PARÂMETRO DE TRUNCAMENTO
# ==========================================

T = 2


# ==========================================
# COOCOCORRÊNCIA
# ==========================================

def coocorrencia_4_ordem(
    residual,
    T=2
):

    estados = 2 * T + 1

    # ------------------------------------------------
    # Residual:
    #
    # -2 -1 0 1 2
    #
    # vira:
    #
    #  0  1 2 3 4
    # ------------------------------------------------

    r = residual + T

    H, W = r.shape

    cooc = np.zeros(
        estados ** 4,
        dtype=np.float64
    )


    # ==============================================
    # HORIZONTAL
    # ==============================================

    if W >= 4:

        a = r[:, 0:W-3]
        b = r[:, 1:W-2]
        c = r[:, 2:W-1]
        d = r[:, 3:W]

        indices = (
            ((a * estados + b) * estados + c)
            * estados + d
        )

        valores, contagens = np.unique(
            indices,
            return_counts=True
        )

        cooc[valores] += contagens


    # ==============================================
    # VERTICAL
    # ==============================================

    if H >= 4:

        a = r[0:H-3, :]
        b = r[1:H-2, :]
        c = r[2:H-1, :]
        d = r[3:H, :]

        indices = (
            ((a * estados + b) * estados + c)
            * estados + d
        )

        valores, contagens = np.unique(
            indices,
            return_counts=True
        )

        cooc[valores] += contagens


    # ==============================================
    # DIAGONAL PRINCIPAL
    # ==============================================

    if H >= 4 and W >= 4:

        a = r[0:H-3, 0:W-3]
        b = r[1:H-2, 1:W-2]
        c = r[2:H-1, 2:W-1]
        d = r[3:H, 3:W]

        indices = (
            ((a * estados + b) * estados + c)
            * estados + d
        )

        valores, contagens = np.unique(
            indices,
            return_counts=True
        )

        cooc[valores] += contagens


    # ==============================================
    # DIAGONAL INVERSA
    # ==============================================

    if H >= 4 and W >= 4:

        a = r[0:H-3, 3:W]
        b = r[1:H-2, 2:W-1]
        c = r[2:H-1, 1:W-2]
        d = r[3:H, 0:W-3]

        indices = (
            ((a * estados + b) * estados + c)
            * estados + d
        )

        valores, contagens = np.unique(
            indices,
            return_counts=True
        )

        cooc[valores] += contagens


    # ==============================================
    # NORMALIZAÇÃO
    # ==============================================

    soma = np.sum(cooc)

    if soma > 0:
        cooc /= soma


    return cooc


# ==========================================
# EXTRAÇÃO DAS CARACTERÍSTICAS SRM
# ==========================================

def extrair_srm(imagem):

    features = []


    for filtro in all_normalized_hpf_list:


        # ======================================
        # 1. APLICAR FILTRO
        # ======================================

        residual = cv2.filter2D(

            imagem.astype(np.float32),

            -1,

            filtro

        )


        # ======================================
        # 2. ARREDONDAMENTO
        # ======================================

        residual = np.rint(
            residual
        )


        # ======================================
        # 3. TRUNCAMENTO
        # ======================================

        residual = np.clip(

            residual,

            -T,

            T

        )


        residual = residual.astype(
            np.int16
        )


        # ======================================
        # 4. COOCOCORRÊNCIA
        # ======================================

        cooc = coocorrencia_4_ordem(

            residual,

            T

        )


        # ======================================
        # 5. ADICIONAR CARACTERÍSTICAS
        # ======================================

        features.extend(
            cooc
        )


    return np.array(
        features,
        dtype=np.float32
    )


# ==========================================
# ESCOLHER IMAGEM
# ==========================================

Tk().withdraw()


arquivo = askopenfilename(

    title="Selecione uma imagem",

    filetypes=[

        ("PNG","*.png"),

        ("BMP","*.bmp"),

    ]

)


if arquivo == "":

    print(
        "Nenhuma imagem selecionada"
    )

    exit()


print(
    "\nImagem:"
)

print(
    arquivo
)


# ==========================================
# LER IMAGEM
# ==========================================

imagem = cv2.imread(

    arquivo,

    cv2.IMREAD_GRAYSCALE

)


if imagem is None:

    raise Exception(
        "Erro ao abrir imagem"
    )


# ==========================================
# EXTRAIR SRM
# ==========================================

features = extrair_srm(

    imagem

)


print(
    "\nNúmero de características:"
)

print(
    features.shape
)


# ==========================================
# AJUSTAR FORMATO
# ==========================================

features = features.reshape(

    1,

    -1

)


# ==========================================
# VERIFICAR COMPATIBILIDADE
# ==========================================

if features.shape[1] != scaler.n_features_in_:

    print(
        "\nERRO:"
    )

    print(
        "O número de características "
        "não corresponde ao modelo."
    )

    print(
        "Características extraídas:",
        features.shape[1]
    )

    print(
        "Características esperadas:",
        scaler.n_features_in_
    )

    print(
        "\nÉ necessário treinar novamente "
        "o modelo usando esta mesma extração."
    )

    exit()


# ==========================================
# NORMALIZAÇÃO
# ==========================================

features = scaler.transform(

    features

)


# ==========================================
# CLASSIFICAÇÃO
# ==========================================

resultado = modelo.predict(

    features

)


prob = modelo.predict_proba(

    features

)


# ==========================================
# RESULTADO
# ==========================================

if resultado[0] == 0:

    print(
        "\nRESULTADO: COVER"
    )

else:

    print(
        "\nRESULTADO: STEGO"
    )


# ==========================================
# PROBABILIDADE
# ==========================================

print(
    "\nProbabilidade:"
)

print(

    "Cover:",

    round(
        prob[0][0] * 100,
        2
    ),

    "%"

)

print(

    "Stego:",

    round(
        prob[0][1] * 100,
        2
    ),

    "%"

)
