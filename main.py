from PIL import Image
import os


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


    return texto



# ==================================================
# INSERÇÃO LSB EM UMA IMAGEM GRAYSCALE
# ==================================================

def inserir_lsb_gray(
        imagem_entrada,
        imagem_saida,
        bits):


    img = Image.open(
        imagem_entrada
    ).convert("L")


    pixels = list(
        img.getdata()
    )


    capacidade = len(pixels)


    if len(bits) > capacidade:

        raise Exception(
            "Mensagem maior que capacidade da imagem."
        )


    novos_pixels = []


    indice = 0


    for pixel in pixels:


        if indice < len(bits):

            bit = int(
                bits[indice]
            )


            # altera somente o LSB
            pixel = (
                pixel & 254
            ) | bit


            indice += 1


        novos_pixels.append(pixel)



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
# PROCESSAMENTO EM LOTE - COVER -> STEGO
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


    if not os.path.exists(pasta_saida):

        os.makedirs(
            pasta_saida
        )



    # lê mensagem

    with open(
        arquivo_txt,
        "r",
        encoding="utf-8"
    ) as f:

        mensagem = f.read()



    bits = texto_para_bits(
        mensagem
    )



    contador = 0



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


            inserir_lsb_gray(
                entrada,
                saida,
                bits
            )


            contador += 1


            print(
                "Gerado:",
                arquivo
            )



    print("\nFinalizado")
    print(
        "Total de imagens stego:",
        contador
    )



# ==================================================
# EXTRAÇÃO DE UMA IMAGEM STEGO
# ==================================================

def extrair_lsb_gray(
        imagem_stego):


    img = Image.open(
        imagem_stego
    ).convert("L")



    pixels = list(
        img.getdata()
    )


    bits = ""



    for pixel in pixels:


        # lê somente o LSB
        bits += str(
            pixel & 1
        )



    mensagem = bits_para_texto(
        bits
    )


    return mensagem



# ==================================================
# EXTRAÇÃO EM LOTE
# ==================================================

def extrair_dataset():


    pasta_stego = input(
        "Pasta das imagens stego: "
    )


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


            mensagem = extrair_lsb_gray(
                caminho
            )


            print("\nImagem:")
            print(arquivo)

            print("Mensagem:")
            print(mensagem)



# ==================================================
# MENU
# ==================================================

while True:


    print("\n======================")
    print(" ESTEGANOGRAFIA LSB")
    print("======================")

    print("1 - Gerar imagens stego")
    print("2 - Extrair mensagem")
    print("3 - Sair")


    opcao = input(
        "Escolha: "
    )


    if opcao == "1":

        gerar_dataset_stego()


    elif opcao == "2":

        extrair_dataset()


    elif opcao == "3":

        break


    else:

        print(
            "Opção inválida"
        )