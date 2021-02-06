# Single tracking OpenCV - https://github.com/alexcamargoweb/single-tracking-opencv
# Rastreamento de objetos com OpenCV.
# Referência: Jones Granatyr. Rastreamento de Objetos com Python e OpenCV. IA Expert.
# Disponível em: https://iaexpert.academy/courses/rastreamento-objetos-python-opencv/.
# Acessado em: 06/02/2021.
# Arquivo: single_tracking.py
# Execução via PyCharm/Linux (Python 3.7,OpenCV 3.4.4)

# importa os pacotes necessários
import cv2
import sys
from random import randint

# imprime a versão do OpenCV
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
print(major_ver, minor_ver, subminor_ver)

# tipos de algoritmos
tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT']
tracker_type = tracker_types[6] # algoritmo escolhido
print(tracker_type)

# verifica as versões
if int(minor_ver) < 3:
    tracker = tracker_type
else: # cria o objeto da classe
    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    if tracker_type == 'MOSSE':
        tracker = cv2.TrackerMOSSE_create()
    if tracker_type == 'CSRT':
        tracker = cv2.TrackerCSRT_create()

# print(tracker) # imprime o objeto

# carrega o vídeo
video = cv2.VideoCapture('input/race.mp4')
if not video.isOpened():
    print('Não foi possível carregar o vídeo.')
    sys.exit()

# lê o primeiro frame do vídeo (detecta o objeto a ser rastreado)
ok, frame = video.read()
if not ok:
    print('Não foi possível ler o arquivo de vídeo.')
    sys.exit()

# se não saiu da execução
print("Leitura do vídeo realizada com sucesso.")

# seleciona o objeto a ser rastreado (region of interesting)
bbox = cv2.selectROI('Single tracking', frame, False)
print(bbox) # coordenadas: x, y, altura, largura
# verifica inicialização do tracker (rastreador) passando o primeiro frame
ok = tracker.init(frame, bbox)
print(ok)

# define a bouding box do tracker
rand = False
if rand == True:
    # cores aleatórias (multi tracker)
    colors = (randint(0, 255), randint(0, 255), randint(0, 255)) #BGR
    print(colors)
else:
    colors = (100, 0, 0) #BGR
    print(colors)

# inicia o rastreamento
while True:
    ok, frame = video.read() # recebe os próximos frames a cada iteração
    if not ok:
        break # se terminou de percorrer o vídeo

    # função que retorna os ciclos de relógio de uma execução
    timer = cv2.getTickCount()
    # recebe o frame atual e retorna se conseguiu manter o rastreamento
    ok, bbox = tracker.update(frame)
    # print(ok, bbox)

    # calcula o FPS (Frames Per Second)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    # se conseguiu rastrear
    if ok:
        # recebe as coordenadas
        (x, y, w, h) = [int(v) for v in bbox]
        # desenha a bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), colors, 2, 1)
    else:
        # senão, acusa a falha no rastreamento
        cv2.putText(frame, 'Falha no rastreamento', (100, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 255), 2) # posição (x, y), fonte, tamanho, cor, espessura

    # ADICIONA ALGUMAS INFORMAÇÕES:
    # indica o algoritmo (traker) utilizado
    cv2.putText(frame, 'Tracker: ' + tracker_type , (100, 20),
                cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 255, 0), 2)
    # exibe o FPS atual
    cv2.putText(frame, 'FPS: ' + str(int(fps)), (100, 50),
                cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 255, 0), 2)

    # define um título para o frame
    cv2.imshow('Single Tracking', frame)

    # espera uma tecla específica para parar (ESC)
    if cv2.waitKey(1) & 0XFF == 27:
        break # interrompe o rastreamento

