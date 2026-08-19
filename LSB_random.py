from PIL import Image
import os
import random


# ==================================================
# TEXTO -> BITS
# ==================================================

def texto_para_bits(texto):

    texto += "####EOF####"

    return ''.join(
        format(ord(c), '08b')
        for c in texto
    )


# ==================================================
# BITS -> TEXTO
# ==================================================

def bits_para_texto(bits):

    texto = ""

    for i in range(0, len(bits), 8):

        byte = bits[i:i+8]

        if len(byte) < 8:
            break

        caractere = chr(
            int(byte, 2)
        )

        texto += caractere

        if texto.endswith("####EOF####"):

            return texto[:-10]

    return None


# ==================================================
# GERAR POSIÇÕES ALEATÓRIAS
# ==================================================

def gerar_posicoes(capacidade, seed):

    posicoes = list(
        range(capacidade)
    )

    gerador = random.Random(seed)

    gerador.shuffle(
        posicoes
    )

    return posicoes


# ==================================================
# INSERÇÃO LSB ALEATÓRIA
# ==================================================

def inserir_lsb_gray(
        imagem_entrada,
        imagem_saida,
        bits,
        seed):

    img = Image.open(
        imagem_entrada
    ).convert("L")

    pixels = list(
        img.getdata()
    )

    capacidade = len(pixels)

    # ------------------------------------------------
    # VERIFICAR CAPACIDADE
    # ------------------------------------------------

    if len(bits) > capacidade:

        raise Exception(
            "Mensagem maior que capacidade da imagem."
        )

    # ------------------------------------------------
    # GERAR POSIÇÕES ALEATÓRIAS
    # ------------------------------------------------

    posicoes = gerar_posicoes(
        capacidade,
        seed
    )

    # ------------------------------------------------
    # COPIAR PIXELS
    # ------------------------------------------------

    novos_pixels = pixels.copy()

    # ------------------------------------------------
    # INSERIR BITS
    # ------------------------------------------------

    for indice in range(
        len(bits)
    ):

        posicao = posicoes[indice]

        bit = int(
            bits[indice]
        )

        pixel = novos_pixels[posicao]

        # altera somente o LSB
        pixel = (
            pixel & 254
        ) | bit

        novos_pixels[posicao] = pixel

    # ------------------------------------------------
    # CRIAR IMAGEM DE SAÍDA
    # ------------------------------------------------

    img_saida = Image.new(
        "L",
        img.size
    )

    img_saida.putdata(
        novos_pixels
    )

    img_saida.save(
        imagem_saida
    )


# ==================================================
# PROCESSAMENTO EM LOTE
# COVER -> STEGO
# ==================================================

def gerar_dataset_stego():

    pasta_cover = input(
        "Pasta das imagens cover: "
    )

    arquivo_txt = input(
        "Arquivo TXT da mensagem: "
    )

    pasta_saida = input(
        "Pasta para salvar stego: "
    )

    seed = int(
        input(
            "Digite a seed: "
        )
    )

    # ------------------------------------------------
    # CRIAR PASTA DE SAÍDA
    # ------------------------------------------------

    if not os.path.exists(
        pasta_saida
    ):

        os.makedirs(
            pasta_saida
        )

    # ------------------------------------------------
    # LER MENSAGEM
    # ------------------------------------------------

    with open(
        arquivo_txt,
        "r",
        encoding="utf-8"
    ) as f:

        mensagem = f.read()

    # ------------------------------------------------
    # TEXTO -> BITS
    # ------------------------------------------------

    bits = texto_para_bits(
        mensagem
    )

    print(
        "\nQuantidade de bits:",
        len(bits)
    )

    print(
        "Seed:",
        seed
    )

    contador = 0

    # ------------------------------------------------
    # PROCESSAR IMAGENS
    # ------------------------------------------------

    for arquivo in os.listdir(
        pasta_cover
    ):

        if arquivo.lower().endswith(
            (".png", ".bmp")
        ):

            entrada = os.path.join(
                pasta_cover,
                arquivo
            )

            saida = os.path.join(
                pasta_saida,
                arquivo
            )

            try:

                inserir_lsb_gray(
                    entrada,
                    saida,
                    bits,
                    seed
                )

                contador += 1

                print(
                    "Gerado:",
                    arquivo
                )

            except Exception as erro:

                print(
                    "Erro em:",
                    arquivo
                )

                print(
                    erro
                )

    print(
        "\nFinalizado"
    )

    print(
        "Total de imagens stego:",
        contador
    )


# ==================================================
# EXTRAÇÃO LSB ALEATÓRIA
# ==================================================

def extrair_lsb_gray(
        imagem_stego,
        seed):

    img = Image.open(
        imagem_stego
    ).convert("L")

    pixels = list(
        img.getdata()
    )

    capacidade = len(pixels)

    # ------------------------------------------------
    # GERAR EXATAMENTE A MESMA SEQUÊNCIA
    # ------------------------------------------------

    posicoes = gerar_posicoes(
        capacidade,
        seed
    )

    bits = ""

    # ------------------------------------------------
    # EXTRAIR BITS
    # ------------------------------------------------

    for posicao in posicoes:

        pixel = pixels[posicao]

        # lê somente o LSB
        bits += str(
            pixel & 1
        )

        # ------------------------------------------------
        # TENTAR IDENTIFICAR O EOF
        # ------------------------------------------------

        if len(bits) % 8 == 0:

            texto = bits_para_texto(
                bits
            )

            if texto is not None:

                return texto

    return "Mensagem não encontrada."


# ==================================================
# EXTRAÇÃO EM LOTE
# ==================================================

def extrair_dataset():

    pasta_stego = input(
        "Pasta das imagens stego: "
    )

    seed = int(
        input(
            "Digite a seed utilizada: "
        )
    )

    contador = 0

    # ------------------------------------------------
    # PROCESSAR IMAGENS
    # ------------------------------------------------

    for arquivo in os.listdir(
        pasta_stego
    ):

        if arquivo.lower().endswith(
            (".png", ".bmp")
        ):

            caminho = os.path.join(
                pasta_stego,
                arquivo
            )

            try:

                mensagem = extrair_lsb_gray(
                    caminho,
                    seed
                )

                print(
                    "\n======================"
                )

                print(
                    "Imagem:",
                    arquivo
                )

                print(
                    "Mensagem:"
                )

                print(
                    mensagem
                )

                contador += 1

            except Exception as erro:

                print(
                    "\nErro em:",
                    arquivo
                )

                print(
                    erro
                )

    print(
        "\nTotal extraído:",
        contador
    )


# ==================================================
# MENU
# ==================================================

while True:

    print("\n======================")
    print(" ESTEGANOGRAFIA LSB")
    print("======================")

    print(
        "1 - Gerar imagens stego"
    )

    print(
        "2 - Extrair mensagem"
    )

    print(
        "3 - Sair"
    )

    opcao = input(
        "Escolha: "
    )

    # ------------------------------------------------
    # GERAR STEGO
    # ------------------------------------------------

    if opcao == "1":

        gerar_dataset_stego()

    # ------------------------------------------------
    # EXTRAIR
    # ------------------------------------------------

    elif opcao == "2":

        extrair_dataset()

    # ------------------------------------------------
    # SAIR
    # ------------------------------------------------

    elif opcao == "3":

        print(
            "Programa encerrado."
        )

        break

    else:

        print(
            "Opção inválida."
        )