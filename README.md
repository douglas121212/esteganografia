# Esteganálise - Projeto classificador de esteganografia

O projeto implementa um sistema de esteganálise baseado em LSB, SRM e SVM. Inicialmente, o algoritmo LSB é utilizado para gerar imagens estego, inserindo uma mensagem secreta nos bits menos significativos dos pixels de imagens originais (Cover). Em seguida, as imagens Cover e Stego são processadas pelo Spatial Rich Model (SRM), responsável por extrair características estatísticas relacionadas aos resíduos e às variações locais dos pixels. Essas características são organizadas em vetores e utilizadas como entrada para o treinamento de um Support Vector Machine (SVM), que aprende a distinguir imagens originais de imagens que possuem dados ocultos. Por fim, uma nova imagem pode ser submetida ao mesmo processo de extração de características e classificada pelo modelo como Cover ou Stego.



