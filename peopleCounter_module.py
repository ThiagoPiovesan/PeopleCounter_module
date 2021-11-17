# /*=========================================================*\
# |      /============================================\       |
# |     ||  -   Código para contagem de pessoas,    - ||      |
# |     ||  - Entrando e saindo do ambiente - Zonas - ||      |
# |     ||  -        Projeto: People Counter        - ||      |
# |     ||  -  Tecnologia: OpenCV + Object Trackig  - ||      |
# |     ||  -       Módulo: Camera IP + OpenCV      - ||      |
# |     ||  -             Primer Analytics          - ||      |
# |     ||  -                                       - ||      |
# |     ||  -   Desenvolvido por: Thiago Piovesan   - ||      |
# |     ||  -          Versao atual: 1.0.0          - ||      |
# |      \============================================/       |
# \*=========================================================*/

# Link do Github: https://github.com/ThiagoPiovesan

# O presente programa faz parte de um dos módulos desenvolvidos para plataforma. 
# Tendo esse por objetivo a contagem de pessoas entrando e saindo de ambientes ou zonas.
# Se atente dentro da Seção 'Variáveis de Controle' para realizar ajustes necessários.

#==================================================================================================#
# Bibliotecas utilizadas:

import numpy as np
import cv2 as cv
import Person
import time, datetime
import imutils, schedule
import requests

from imutils.video import FPS
#==================================================================================================#
# Variáveis de Controle:
line_aligment = 'horizontal'									# Define o alinhamento da linha de passagem
log_init = False

#==================================================================================================#
# Variáveis de informação:
person_in = 0													# Número de pessoas que entraram
person_out = 0													# Número de pessoas que saiu
person_total = 0												# Número de pessoas total dentro

last_person_in = 0												# Número de pessoas que entraram última interação
last_person_out = 0												# Número de pessoas que saiu última interação
last_person_total = 0											# Número de pessoas total dentro última interação

# Informações do Bot --> Ainda não está integrado...
bot_token = ''
bot_chatID = ''

#==================================================================================================#
# Demais Variáveis:
line_down_color = (255,0,0)
line_up_color = (0,0,255)

#==================================================================================================#
# Inicializamento do log:

if log_init == True:
    try:
        log = open('log.txt', "w")
    except:
        print( "No se puede abrir el archivo log")

#==================================================================================================#
# Definições para envio de imagem e texto via Bot Telegram:

def telegram_bot_sendtext(bot_message, bot_token, bot_chatID):
    
	send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    
	response = requests.post(send_text)

	return response.json()

def telegram_bot_sendImage(file_opened, bot_token, bot_chatID):
	files = {'photo': file_opened}
	send_photo = 'https://api.telegram.org/bot' + bot_token + '/sendPhoto?chat_id=' + bot_chatID

	response = requests.post(send_photo, files=files)

	return response

#==================================================================================================#
# Função para configuração dos parâmetros adicionais:
def config_param(frame_width, frame_height, line_aligment):
    frameArea = frame_height * frame_width

    areaTH = frameArea / 250
    print( 'Area Threshold', areaTH)

    if line_aligment == 'horizontal':
        # Linhas de entrada/salida
        line_up = int(2*(frame_height/5))
        line_down   = int(3*(frame_height/5))

        up_limit =   int(1*(frame_height/5))
        down_limit = int(4*(frame_height/5))
    else:
        # Linhas de entrada/salida
        line_up = int(2*(frame_width/5))
        line_down   = int(3*(frame_width/5))

        up_limit =   int(1*(frame_width/5))
        down_limit = int(4*(frame_width/5))

    return line_up, line_down, up_limit, down_limit, areaTH

#==================================================================================================#
# Função para configuração das linhas --> Up, Down, Up_limit and Down_limit:
def config_lines(line_up, line_down, up_limit, down_limit, frame_width, frame_height, line_aligment):

#--------------------------------------------------------------------------------------------------#
    print( "Red line:",str(line_down))
    print( "Blue line:", str(line_up))

    if line_aligment == 'horizontal':
#--------------------------------------------------------------------------------------------------#
        pt1 = [0, line_down];
        pt2 = [frame_width, line_down];
        pts_L1 = np.array([pt1,pt2], np.int32)
        pts_L1 = pts_L1.reshape((-1,1,2))
    #--------------------------------------------------------------------------------------------------#
        pt3 = [0, line_up];
        pt4 = [frame_width, line_up];
        pts_L2 = np.array([pt3,pt4], np.int32)
        pts_L2 = pts_L2.reshape((-1,1,2))
    #--------------------------------------------------------------------------------------------------#
        pt5 = [0, up_limit];
        pt6 = [frame_width, up_limit];
        pts_L3 = np.array([pt5,pt6], np.int32)
        pts_L3 = pts_L3.reshape((-1,1,2))
    #--------------------------------------------------------------------------------------------------#
        pt7 = [0, down_limit];
        pt8 = [frame_width, down_limit];
        pts_L4 = np.array([pt7,pt8], np.int32)
        pts_L4 = pts_L4.reshape((-1,1,2))
#--------------------------------------------------------------------------------------------------#
    else: 
        #--------------------------------------------------------------------------------------------------#
        pt1 = [0, line_down];
        pt2 = [frame_height, line_down];
        pts_L1 = np.array([pt1,pt2], np.int32)
        pts_L1 = pts_L1.reshape((-1,1,2))
    #--------------------------------------------------------------------------------------------------#
        pt3 = [0, line_up];
        pt4 = [frame_height, line_up];
        pts_L2 = np.array([pt3,pt4], np.int32)
        pts_L2 = pts_L2.reshape((-1,1,2))
    #--------------------------------------------------------------------------------------------------#
        pt5 = [0, up_limit];
        pt6 = [frame_height, up_limit];
        pts_L3 = np.array([pt5,pt6], np.int32)
        pts_L3 = pts_L3.reshape((-1,1,2))
    #--------------------------------------------------------------------------------------------------#
        pt7 = [0, down_limit];
        pt8 = [frame_height, down_limit];
        pts_L4 = np.array([pt7,pt8], np.int32)
        pts_L4 = pts_L4.reshape((-1,1,2))

    return pts_L1, pts_L2, pts_L3, pts_L4

#==================================================================================================#
# Função para inicialização da camera: 
def camera_init():

    # Define a camera que será utilizada:

    # "rtsp://admin:Primer123@192.168.100.195/live.sdp"
    # cap = cv2.VideoCapture("rtsp://admin:Primer123@192.168.100.195/live.sdp")      # Uncomment to use RTSP Camera

    # cap = cv.VideoCapture(0)
    cap = cv.VideoCapture('Test Files/example_01.mp4')          # cap = cv.VideoCapture('Test Files/TestVideo.avi')

    #Imprime las propiedades de captura a consola
    for i in range(19):
        print( i, cap.get(i))

    frame_width = int(cap.get(3))                               # Returns the width and height of capture video
    # frame_width = int(640)                                    # Returns the width and height of capture video
    frame_height = int(cap.get(4))
    # frame_height = int(480)

    return cap, frame_width, frame_height

#==================================================================================================#
# Função para Envio das informações para Bot: --> Alterar

def send_infos_bot(string, objectID, precision):
    
    # Envia a mensagem de texto paro o usuário
    text = telegram_bot_sendtext("Objeto identificado: " + string + " | ID: " + str(objectID) + " - Precisão: %s" % str(round(precision * 100, 2)))
    
    # Salva a Imagem no dispositivo e Envia a foto
    cv.imwrite('Knife.png', img)

    phot = telegram_bot_sendImage(open('Knife.png', 'rb'))

    # Printa a resposta
    print(text)
    print(phot)

#==================================================================================================#
# Função para Envio das informações para Servidor: --> Alterar

def send_infos_server(string, objectID, precision):
    
    # Envia a mensagem de texto paro o usuário
    text = telegram_bot_sendtext("Objeto identificado: " + string + " | ID: " + str(objectID) + " - Precisão: %s" % str(round(precision * 100, 2)))
    # Salva a Imagem no dispositivo e Envia a foto
    cv.imwrite('Knife.png', img)
    phot = telegram_bot_sendImage(open('Knife.png', 'rb'))

    # Printa a resposta
    print(text)
    print(phot)

#==================================================================================================#
# Função para Envio das informações para Servidor: --> Alterar

def counter(cap, up_limit, down_limit, pts_L1, pts_L2, pts_L3, pts_L4, person_in, person_out, person_total, log_init, areaTH, line_up, line_down):            
    fps = FPS().start()                                         # Inicia a marcação do FPS
#--------------------------------------------------------------------------------------------------#
    # Substração do fundo:
    fgbg = cv.createBackgroundSubtractorMOG2(detectShadows = True)

    # Elementos estruturantes para filtros morfológicos:
    kernelOp = np.ones((3,3), np.uint8)
    kernelOp2 = np.ones((5,5), np.uint8)
    kernelCl = np.ones((11,11), np.uint8)

    # Variáveis:
    font = cv.FONT_HERSHEY_SIMPLEX                              # Fonte
    persons = []                                                # Vetor de pessoas presentes no frame
    max_p_age = 5
    pid = 1

    while(cap.isOpened()):                                      # Verifica se foi aberta com sucesso a camera

        # Captura a imagem (frame) da fonte de vídeo
        ret, frame = cap.read()

        for i in persons:
            i.age_one()                                         # 'Age' (ID) para cada pessoa no frame
#--------------------------------------------------------------------------------------------------#
    # Pré-processamento:
        
        # Aplica a substração de fundo
        fgmask = fgbg.apply(frame)
        fgmask2 = fgbg.apply(frame)

        # Binarização para eliminar as sombras (color gris)
        try:
            ret,imBin= cv.threshold(fgmask,200,255,cv.THRESH_BINARY)
            ret,imBin2 = cv.threshold(fgmask2,200,255,cv.THRESH_BINARY)

            # Opening (erode->dilate) para quitar ruido.
            mask = cv.morphologyEx(imBin, cv.MORPH_OPEN, kernelOp)
            mask2 = cv.morphologyEx(imBin2, cv.MORPH_OPEN, kernelOp)

            # Closing (dilate -> erode) para juntar regiones blancas.
            mask =  cv.morphologyEx(mask , cv.MORPH_CLOSE, kernelCl)
            mask2 = cv.morphologyEx(mask2, cv.MORPH_CLOSE, kernelCl)
#--------------------------------------------------------------------------------------------------#
    # Prints de informações importantes:
        except:
            print('EOF')
            print('In: [', person_in, ']')
            print('Out: [', person_out, ']')
            print('Total: [', person_total, ']')
            break
#--------------------------------------------------------------------------------------------------#
    # Contornos
        
        # RETR_EXTERNAL returns only extreme outer flags. All child contours are left behind.
        contours0, hierarchy = cv.findContours(mask2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours0:
            area = cv.contourArea(cnt)
            
            if area > areaTH:
#--------------------------------------------------------------------------------------------------#
            # Tracking IDs (persons)
                
            # TO-DO:  Falta agregar condições para multiplas pessoas, entradas e saídas do frame.
                
                M = cv.moments(cnt)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                x, y, w, h = cv.boundingRect(cnt)
#--------------------------------------------------------------------------------------------------#
                new = True

                if cy in range(up_limit, down_limit):
                
                    for i in persons:
                
                        if abs(x - i.getX()) <= w and abs(y - i.getY()) <= h:
                
                        # Verifica se o objeto está próximo de outro já identificado anteriormente
                            new = False
                            i.updateCoords(cx, cy)          # Atualiza as coordenadas do objeto identificado 
#--------------------------------------------------------------------------------------------------#                           
                        # Person In e Person Out
                            if i.going_UP(line_down, line_up) == True:
                                person_in += 1;
                                print( "ID:",i.getId(),'crossed going up at',time.strftime("%c"))
                    
                                if log_init == True:
                                    log.write("ID: "+str(i.getId())+' crossed going up at ' + time.strftime("%c") + '\n')

                            elif i.going_DOWN(line_down, line_up) == True:
                                person_out += 1;
                                print( "ID:",i.getId(),'crossed going down at',time.strftime("%c"))
        
                                if log_init == True:
                                    log.write("ID: " + str(i.getId()) + ' crossed going down at ' + time.strftime("%c") + '\n')
                            break
#--------------------------------------------------------------------------------------------------#
                        if i.getState() == '1':
                            if i.getDir() == 'down' and i.getY() > down_limit:
                                i.setDone()
                            elif i.getDir() == 'up' and i.getY() < up_limit:
                                i.setDone()
#--------------------------------------------------------------------------------------------------#
                        if i.timedOut():
                        # sacar i de la lista persons
                            index = persons.index(i)
                            persons.pop(index)
                            del i                           # liberar la memoria de i
#--------------------------------------------------------------------------------------------------#
                    if new == True:
                        p = Person.MyPerson(pid, cx, cy, max_p_age)
                        persons.append(p)
                        pid += 1     
#--------------------------------------------------------------------------------------------------#
                #################
                #   DIBUJOS     #
                #################

                cv.circle(frame, (cx,cy), 5, (0,0,255), -1)
                img = cv.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 2)            
                # cv.drawContours(frame, cnt, -1, (0,255,0), 3)
#--------------------------------------------------------------------------------------------------#               
        # END for cnt in contours0
                
        #########################
        # DIBUJAR TRAYECTORIAS  #
        #########################
        for i in persons:

            cv.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv.LINE_AA)
#--------------------------------------------------------------------------------------------------#           
    # Imagens e prints:
        fps.update()
        person_total = abs(person_out - person_in)
        str_up = 'In: ' + str(person_in)
        str_down = 'Out: ' + str(person_out)
        str_total = 'Total: ' + str(person_total)
        str_fps = 'FPS: ' 

        frame = cv.polylines(frame, [pts_L1], False, line_down_color, thickness=2)      # Linha up
        frame = cv.polylines(frame, [pts_L2], False, line_up_color, thickness=2)        # Linha down
        
        frame = cv.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)            # Linha up limit
        frame = cv.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)            # Linha down limit

        cv.putText(frame, str_up, (10,20), font, 0.5, (255,255,255), 2, cv.LINE_AA)     # String up
        cv.putText(frame, str_up, (10,20), font, 0.5, (0,0,180), 1, cv.LINE_AA)         

        cv.putText(frame, str_down, (10,45), font, 0.5, (255,255,255), 2, cv.LINE_AA)   # String down
        cv.putText(frame, str_down, (10,45), font, 0.5, (180,0,0), 1, cv.LINE_AA)

        cv.putText(frame, str_total, (10,70), font, 0.5, (255,255,255), 2, cv.LINE_AA)  # String total
        cv.putText(frame, str_total, (10,70), font, 0.5, (0,0,0), 1, cv.LINE_AA) 

        cv.putText(frame, str_fps, (320,20), font, 0.5, (255,255,255), 2, cv.LINE_AA)  # String total
        cv.putText(frame, str_fps, (320,20), font, 0.5, (50,50,50), 1, cv.LINE_AA) 

#--------------------------------------------------------------------------------------------------#
    # Mostra o frame de novo
        cv.imshow('Frame', frame)
        cv.imshow('Mask', mask)    
#--------------------------------------------------------------------------------------------------#       
        # Precione ESC para sair:
        k = cv.waitKey(30) & 0xff

        if k == 27:
            break
#--------------------------------------------------------------------------------------------------#    
    # Limpando e finalizando processos:
    if log_init == True:
        log.flush()
        log.close()

    cap.release()

    fps.stop()
    #print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    #print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    cv.destroyAllWindows()
#--------------------------------------------------------------------------------------------------#    

def main():
    # Camera initialization:
    cap, frame_width, frame_height = camera_init()

    line_up, line_down, up_limit, down_limit, areaTH = config_param(frame_width, frame_height, line_aligment) 

    # Lines configuration:
    pts_L1, pts_L2, pts_L3, pts_L4  = config_lines(line_up, line_down, up_limit, down_limit, frame_width, frame_height, line_aligment)

    counter(cap, up_limit, down_limit, pts_L1, pts_L2, pts_L3, pts_L4, person_in, person_out, person_total, log_init, areaTH, line_up, line_down)

main()

#--------------------------------------------------------------------------------------------------#
# Início prgramado da aplicação:
	# Referência: --> Learn more about different schedules here: https://pypi.org/project/schedule/
#if config.Scheduler:
	##Runs for every 1 second
	#schedule.every(1).seconds.do(run)
	##Runs at every day (9:00 am). You can change it.
#	schedule.every().day.at("9:00").do(run)

#	while 1:
#		schedule.run_pending()
#--------------------------------------------------------------------------------------------------#
