import os
import cv2
import numpy as np


# =====================================================
# 1) FILTROS
# =====================================================

filter_class_1 = [
    np.array([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, 0]
    ], dtype=np.float32),

    np.array([
        [0, 1, 0],
        [0, -1, 0],
        [0, 0, 0]
    ], dtype=np.float32),

    np.array([
        [0, 0, 1],
        [0, -1, 0],
        [0, 0, 0]
    ], dtype=np.float32),

    np.array([
        [0, 0, 0],
        [1, -1, 0],
        [0, 0, 0]
    ], dtype=np.float32),

    np.array([
        [0, 0, 0],
        [0, -1, 1],
        [0, 0, 0]
    ], dtype=np.float32),

    np.array([
        [0, 0, 0],
        [0, -1, 0],
        [1, 0, 0]
    ], dtype=np.float32),

    np.array([
        [0, 0, 0],
        [0, -1, 0],
        [0, 1, 0]
    ], dtype=np.float32),

    np.array([
        [0, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ], dtype=np.float32)
]


filter_class_2 = [
    np.array([
        [1, 0, 0],
        [0, -2, 0],
        [0, 0, 1]
    ], dtype=np.float32),

    np.array([
        [0, 1, 0],
        [0, -2, 0],
        [0, 1, 0]
    ], dtype=np.float32),

    np.array([
        [0, 0, 1],
        [0, -2, 0],
        [1, 0, 0]
    ], dtype=np.float32),

    np.array([
        [0, 0, 0],
        [1, -2, 1],
        [0, 0, 0]
    ], dtype=np.float32)
]


filter_class_3 = [
    np.array([
        [-1, 0, 0, 0, 0],
        [0, 3, 0, 0, 0],
        [0, 0, -3, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ], dtype=np.float32),

    np.array([
        [0, 0, -1, 0, 0],
        [0, 0, 3, 0, 0],
        [0, 0, -3, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ], dtype=np.float32),

    np.array([
        [0, 0, 0, 0, -1],
        [0, 0, 0, 3, 0],
        [0, 0, -3, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ], dtype=np.float32),

    np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 1, -3, 3, -1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ], dtype=np.float32),

    np.array([
        [0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, -3, 0, 0],
        [0, 0, 0, 3, 0],
        [0, 0, 0, 0, -1]
    ], dtype=np.float32),

    np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, -3, 0, 0],
        [0, 0, 3, 0, 0],
        [0, 0, -1, 0, 0]
    ], dtype=np.float32),

    np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, -3, 0, 0],
        [0, 3, 0, 0, 0],
        [-1, 0, 0, 0, 0]
    ], dtype=np.float32),

    np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [-1, 3, -3, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ], dtype=np.float32)
]


filter_edge_3x3 = [
    np.array([
        [-1, 2, -1],
        [2, -4, 2],
        [0, 0, 0]
    ], dtype=np.float32),

    np.array([
        [0, 2, -1],
        [0, -4, 2],
        [0, 2, -1]
    ], dtype=np.float32),

    np.array([
        [0, 0, 0],
        [2, -4, 2],
        [-1, 2, -1]
    ], dtype=np.float32),

    np.array([
        [-1, 2, 0],
        [2, -4, 0],
        [-1, 2, 0]
    ], dtype=np.float32)
]


filter_edge_5x5 = [
    np.array([
        [-1, 2, -2, 2, -1],
        [2, -6, 8, -6, 2],
        [-2, 8, -12, 8, -2],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ], dtype=np.float32),

    np.array([
        [0, 0, -2, 2, -1],
        [0, 0, 8, -6, 2],
        [0, 0, -12, 8, -2],
        [0, 0, 8, -6, 2],
        [0, 0, -2, 2, -1]
    ], dtype=np.float32),

    np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [-2, 8, -12, 8, -2],
        [2, -6, 8, -6, 2],
        [-1, 2, -2, 2, -1]
    ], dtype=np.float32),

    np.array([
        [-1, 2, -2, 0, 0],
        [2, -6, 8, 0, 0],
        [-2, 8, -12, 0, 0],
        [2, -6, 8, 0, 0],
        [-1, 2, -2, 0, 0]
    ], dtype=np.float32)
]


square_3x3 = np.array([
    [-1, 2, -1],
    [2, -4, 2],
    [-1, 2, -1]
], dtype=np.float32)


square_5x5 = np.array([
    [-1, 2, -2, 2, -1],
    [2, -6, 8, -6, 2],
    [-2, 8, -12, 8, -2],
    [2, -6, 8, -6, 2],
    [-1, 2, -2, 2, -1]
], dtype=np.float32)


# =====================================================
# 2) NORMALIZAÇÃO DOS FILTROS
# =====================================================

normalized_filter_class_2 = [
    hpf / 2 for hpf in filter_class_2
]

normalized_filter_class_3 = [
    hpf / 3 for hpf in filter_class_3
]

normalized_filter_edge_3x3 = [
    hpf / 4 for hpf in filter_edge_3x3
]

normalized_square_3x3 = square_3x3 / 4

normalized_filter_edge_5x5 = [
    hpf / 12 for hpf in filter_edge_5x5
]

normalized_square_5x5 = square_5x5 / 12


# =====================================================
# 3) CONJUNTO FINAL DE FILTROS
# =====================================================

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


print("Número de filtros:", len(all_normalized_hpf_list))


# =====================================================
# 4) PARÂMETROS DO MODELO
# =====================================================

# Valor máximo do residual considerado.
#
# Os valores serão limitados para:
#
# -T ... 0 ... +T
#
T = 2

# Ordem da coocorrência.
#
# 4 significa:
#
# r1 -> r2 -> r3 -> r4
#
ORDER = 4


# =====================================================
# 5) QUANTIZAÇÃO DO RESIDUAL
# =====================================================

def quantizar_residual(residual, T=2):

    # Truncamento
    residual = np.clip(
        residual,
        -T,
        T
    )

    # Quantização
    residual = np.rint(
        residual
    ).astype(np.int16)

    return residual


# =====================================================
# 6) COOCORRÊNCIA DE ORDEM 4
# =====================================================

def coocorrencia_4_ordem(residual, T=2):

    """
    Calcula coocorrência de 4 resíduos consecutivos.

    Exemplo:

    r1, r2, r3, r4

    Cada valor está entre -T e +T.

    Para T=2:

        -2,-1,0,1,2

    Total:

        5^4 = 625 combinações.
    """

    tamanho = 2 * T + 1

    # ---------------------------------------------
    # Criar vetor deslocado para índice positivo
    # ---------------------------------------------

    r = residual + T

    H, W = r.shape

    # ---------------------------------------------
    # Matriz final de coocorrência
    # ---------------------------------------------

    cooc = np.zeros(
        tamanho ** 4,
        dtype=np.float64
    )

    # =================================================
    # DIREÇÃO HORIZONTAL
    # =================================================

    if W >= 4:

        a = r[:, 0:W-3]
        b = r[:, 1:W-2]
        c = r[:, 2:W-1]
        d = r[:, 3:W]

        indices = (
            ((a * tamanho + b) * tamanho + c)
            * tamanho
            + d
        )

        valores, contagens = np.unique(
            indices,
            return_counts=True
        )

        cooc[valores] += contagens


    # =================================================
    # DIREÇÃO VERTICAL
    # =================================================

    if H >= 4:

        a = r[0:H-3, :]
        b = r[1:H-2, :]
        c = r[2:H-1, :]
        d = r[3:H, :]

        indices = (
            ((a * tamanho + b) * tamanho + c)
            * tamanho
            + d
        )

        valores, contagens = np.unique(
            indices,
            return_counts=True
        )

        cooc[valores] += contagens


    # =================================================
    # DIAGONAL PRINCIPAL
    # =================================================

    if H >= 4 and W >= 4:

        a = r[0:H-3, 0:W-3]
        b = r[1:H-2, 1:W-2]
        c = r[2:H-1, 2:W-1]
        d = r[3:H, 3:W]

        indices = (
            ((a * tamanho + b) * tamanho + c)
            * tamanho
            + d
        )

        valores, contagens = np.unique(
            indices,
            return_counts=True
        )

        cooc[valores] += contagens


    # =================================================
    # DIAGONAL INVERSA
    # =================================================

    if H >= 4 and W >= 4:

        a = r[0:H-3, 3:W]
        b = r[1:H-2, 2:W-1]
        c = r[2:H-1, 1:W-2]
        d = r[3:H, 0:W-3]

        indices = (
            ((a * tamanho + b) * tamanho + c)
            * tamanho
            + d
        )

        valores, contagens = np.unique(
            indices,
            return_counts=True
        )

        cooc[valores] += contagens


    # =================================================
    # NORMALIZAÇÃO
    # =================================================

    soma = np.sum(cooc)

    if soma > 0:

        cooc = cooc / soma

    return cooc


# =====================================================
# 7) EXTRAÇÃO DAS FEATURES
# =====================================================

def extrair_features_imagem(
    imagem,
    filtros,
    T=2
):

    features = []

    for numero_filtro, filtro in enumerate(filtros):

        # =============================================
        # RESIDUAL
        # =============================================

        residual = cv2.filter2D(
            imagem.astype(np.float32),
            -1,
            filtro
        )


        # =============================================
        # QUANTIZAÇÃO
        # =============================================

        residual_quantizado = quantizar_residual(
            residual,
            T
        )


        # =============================================
        # COOCOCORRÊNCIA
        # =============================================

        cooc = coocorrencia_4_ordem(
            residual_quantizado,
            T
        )


        # =============================================
        # ADICIONAR AO VETOR FINAL
        # =============================================

        features.extend(
            cooc
        )


    return np.asarray(
        features,
        dtype=np.float32
    )


# =====================================================
# 8) PROCESSAR DATASET
# =====================================================

def processar_dataset(
    pasta,
    filtros,
    classe,
    T=2
):

    X = []
    y = []

    arquivos = sorted(
        os.listdir(pasta)
    )

    total = len(arquivos)

    for contador, arquivo in enumerate(arquivos):

        caminho = os.path.join(
            pasta,
            arquivo
        )

        imagem = cv2.imread(
            caminho,
            cv2.IMREAD_GRAYSCALE
        )

        if imagem is None:
            continue


        # =============================================
        # EXTRAÇÃO
        # =============================================

        vetor = extrair_features_imagem(
            imagem,
            filtros,
            T
        )


        X.append(vetor)

        y.append(classe)


        # =============================================
        # PROGRESSO
        # =============================================

        print(
            f"\rProcessando {contador + 1}/{total}",
            end=""
        )


    print()

    return X, y


# =====================================================
# 9) CAMINHOS
# =====================================================

pasta_cover = (
    r"C:\Users\douglas.ferreira"
    r"\Desktop\banco_dados_esteganografia"
    r"\cover"
)

pasta_stego = (
    r"C:\Users\douglas.ferreira"
    r"\Desktop\banco_dados_esteganografia"
    r"\stego"
)


# =====================================================
# 10) PROCESSAR COVER
# =====================================================

print("\n====================================")
print("PROCESSANDO COVER")
print("====================================")

X_cover, y_cover = processar_dataset(
    pasta_cover,
    all_normalized_hpf_list,
    0,
    T
)


# =====================================================
# 11) PROCESSAR STEGO
# =====================================================

print("\n====================================")
print("PROCESSANDO STEGO")
print("====================================")

X_stego, y_stego = processar_dataset(
    pasta_stego,
    all_normalized_hpf_list,
    1,
    T
)


# =====================================================
# 12) JUNTAR DATASETS
# =====================================================

X = np.asarray(
    X_cover + X_stego,
    dtype=np.float32
)

y = np.asarray(
    y_cover + y_stego,
    dtype=np.int8
)


# =====================================================
# 13) INFORMAÇÕES
# =====================================================

print("\n====================================")
print("RESULTADO")
print("====================================")

print(
    "Número de imagens:",
    X.shape[0]
)

print(
    "Número de características:",
    X.shape[1]
)

print(
    "Formato X:",
    X.shape
)

print(
    "Formato y:",
    y.shape
)

print(
    "Cover:",
    np.sum(y == 0)
)

print(
    "Stego:",
    np.sum(y == 1)
)


# =====================================================
# 14) SALVAR
# =====================================================

np.save(
    "X_SRM.npy",
    X
)

np.save(
    "y_SRM.npy",
    y
)


print("\n====================================")
print("DATASET SRM GERADO")
print("====================================")

print("Arquivo: X_SRM.npy")
print("Arquivo: y_SRM.npy")