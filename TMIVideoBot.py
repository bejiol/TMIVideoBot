#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
from telebot import types
import os
import time
import sys
import codecs
import io

"""
    COMANDOS
    /start: Saludo del bot, oferta de opciones --> Bea
    /help: Listado de todo lo que se puede hacer en el bot --> Bea
    /convert: Convertir un vídeo a otro formato
    /compress: Comprimir un vídeo en calidad baja, media o alta
    /youtube <url> : Obtener un vídeo de youtube --> Bea:Revisar tildes
    /youtubetomp3 <url>: Obtener el audion de un vídeo de youtube --> Bea:Revisar tildes
    /gif: Crear un GIF de un vídeo indicando segundos de inicio y fin --> Bea
    /onlyaudio: Extraer audio de un vídeo
    /onlyvideo: Extraer imagen de un vídeo
    /clip: Cortar vídeo de segundo inicio a segundo fin --> Bea
    /videoaudio: Unir vídeo con determinado audio en formato MKV
"""


reload(sys)  
sys.setdefaultencoding('utf8')

# TMIVideoBot - @TMIVideo_bot
token = "BOT_TOKEN"
bot = telebot.TeleBot(token)

# Variables
userStep = {}
formats = ["mp4", "mkv", "mov", "ogg", "flv", "webm", "mpg", "avi"]
oldMessages = {}


# Consulta del paso en el que se encuentra el usuario
# Si es nuevo, paso 0
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        userStep[uid] = 0
        return 0


# Mensaje de saludo al entrar al bot, se da información de consulta de la lista de comandos disponibles
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,
                     "Hola, <strong> TMIVideoBot </strong> es un bot de tratamiento de vídeos. Estamos aquí para ayudarte a poder trabajar con tus vídeos en todas partes. Para ver todo lo que puedes hacer usa el comando /help", parse_mode="HTML")


# Listado de todas las opciones disponibles en el bot
@bot.message_handler(commands=['help'])
def send_help_message(message):
    helpMsg = """ Estas son todas las opciones disponibles en TMIVideoBot:
                /convert : Puedes enviar tu vídeo y especificar el formato de salida en el que quieras que te lo devolvamos convertido.
                /compress : Puedes enviar tu vídeo y seleccionar la compresión que se aplique a tu vídeo (Baja, Media, Alta). Ten en cuenta que esto afecta a la calidad de tu vídeo.
                /youtube <url>: Envíanos la URL del vídeo que quieras descargar de youtube
                /youtubetomp3 <url>: Envíanos la URL del vídeo de youtube del que quieras tener el audio
                /gif : Envíanos tu vídeo, selecciona los segundos que quieres que dure tu GIF y crea gif de tus vídeos
                /onlyaudio: Te devolvemos el audio de tus vídeos en formato mp3
                /onlyvideo: Te devolvemos el vídeo que quieras sin sonido
                /clip:  Envíanos tu vídeo, indícanos segundo de inicio y de fin y te devolvemos tu vídeo recortado
                /videoaudio : Envíanos un vídeo y el audio que quieras que tenga
            """
    bot.send_message(message.chat.id,helpMsg)

# Extraer audio de un vídeo de youtube
"""@bot.message_handler(commands=['youtubetomp3'])
def youtube_to_mp3(message):
    if len(message.text.split()) == 2:
        bot.send_message(message.chat.id,"Perfecto, ¡estamos en ello! Ten un poco de paciencia, esto puede tardar...")
        # os.system("youtube-dl --get-title " + message.text.split()[1] + " > filename.txt")
        # os.system("youtube-dl --extract-audio --audio-format mp3 --output '%(title)s.%(ext)s' " + message.text.split()[1])
        os.system("youtube-dl --extract-audio --audio-format mp3 --output " + str(message.chat.id) + ".mp3 "+ message.text.split()[1])
        cadena = str(message.chat.id) + ".mp3"
        audio = open(cadena,'r')
        bot.send_audio(message.chat.id, audio)
        os.remove(cadena)
    else:
        bot.send_message(message.chat.id,"Mándanos la URL del vídeo en el siguiente formato: /youtubetomp3 <URL> ")

"""
# Extraer audio de un vídeo de youtube
@bot.message_handler(commands=['youtubetomp3'])
def youtube_to_mp3(message):
    if len(message.text.split()) == 2:
        bot.send_message(message.chat.id,"Perfecto, ¡estamos en ello! Ten un poco de paciencia, esto puede tardar...")
        os.system("youtube-dl --get-title " + message.text.split()[1] + " > filename.txt")
        os.system("youtube-dl --extract-audio --audio-format mp3 --output '%(title)s.%(ext)s' " + message.text.split()[1])
        file = open("filename.txt", "r")
        cadena = file.readline()[:-1] + ".mp3"
        audio = open(cadena, 'r')
        bot.send_audio(message.chat.id, audio)
        os.remove(cadena)
        os.remove("filename.txt")
    else:
        bot.send_message(message.chat.id,"Mándanos la URL del vídeo en el siguiente formato: /youtubetomp3 <URL> ")



# Descargar vídeo de youtube
@bot.message_handler(commands=['youtube'])
def youtube(message):
    if len(message.text.split()) == 2:
        bot.send_message(message.chat.id,"Perfecto, ¡estamos en ello! Ten un poco de paciencia, esto puede tardar...")
        os.system("youtube-dl --get-title " + message.text.split()[1] + " > filename.txt")
        os.system("youtube-dl --output '%(title)s.%(ext)s' -f mp4 " + message.text.split()[1])
        file = open("filename.txt", "r")
        cadena = file.readline()[:-1] + ".mp4"
        video = open(cadena, 'r')
        bot.send_video(message.chat.id, video)
        os.remove(cadena)
        os.remove("filename.txt")
    else:
        bot.send_message(message.chat.id,"Mándanos la URL del vídeo en el siguiente formato: /youtube <URL> ")


# Video a Gif
"""
    video_to_gif_ask_video: Mensaje de inicio tras mandar /gif, pide video al usuario
    video_to_gif_ask_seconds: Recibe el vídeo del usuario y le pide los segundos de inicio y fin
    video_to_gif: Recoge los segundos de inicio y fin y envía el GIF al usuario
"""
@bot.message_handler(commands=['gif'], func=lambda message: len(message.text.split()) == 3)
def video_to_gif(message):
    msg = message.text.split()
    inicio = int(msg[1])
    final = int(msg[2])
    duracion = final - inicio
    if inicio < 0:
        bot.send_message(message.chat.id, "¿Segundo de inicio negativo? Qué malo eres...")
    elif final < 0:
        bot.send_message(message.chat.id, "¿Segundo de fin negativo? Qué malo eres...")
    else:
        file = open("filename.txt", "r")
        cadena = file.readline()[:-1]
        #Duracion del video
        os.system("ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 " + cadena + " > duracion.txt")
        fileDuracion = open("duracion.txt", "r")
        segundosvideo = int(fileDuracion.readline()[:-1].split(".")[0])
        if duracion < 0:
            bot.send_message(message.chat.id, "Los datos que nos has indicado no son correctos, indica correctamente segundo de inicio y fin")
        elif inicio > segundosvideo or final > segundosvideo:
            bot.send_message(message.chat.id, "El vídeo es más corto, indica otro segundo de inicio o fin.")
        else:
            os.system("mkdir frames")
            os.system("ffmpeg -i " + cadena + " -ss " + str(inicio) + " -t " + str(duracion) + 
                " -vf scale=320:-1:flags=lanczos,fps=10 frames/ffout%03d.png")
            os.system("convert -loop 0 frames/ffout*.png " + str(message.chat.id) + ".gif")
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, "Aquí tienes tu gif recién salido del horno!")
            gif = open(str(message.chat.id) + ".gif", 'r')
            bot.send_video(message.chat.id, gif)
            os.remove(str(message.chat.id) + ".gif")
            os.remove("filename.txt")
            os.system("rm -Rf frames/")
        os.remove("duracion.txt")

@bot.message_handler(commands=['gif'])
def video_to_gif_ask_video(message):
    bot.send_message(message.chat.id, "Mándanos el vídeo que quieres que convirtamos a gif!")
    userStep[message.chat.id] = 2

@bot.message_handler(content_types=['video', 'document'], func=lambda message: get_user_step(message.chat.id) == 2)
def video_to_gif_ask_seconds(message):
    file_info = None
    filename = ''

    if not message.document:
        file_info = bot.get_file(message.video.file_id)
        filename = file_info.file_path.split("/")[len(file_info.file_path.split("/")) - 1]
    else:
        file_info = bot.get_file(message.document.file_id)
        filename = message.document.file_name

    downloaded_file = bot.download_file(file_info.file_path)
    new_File = open(file_info.file_path.split("/")[1], 'wb')
    os.system("echo " + file_info.file_path.split("/")[1] + " > filename.txt")
    new_File.write(downloaded_file)
    new_File.close()
    bot.send_message(message.chat.id,
                     "Perfecto, ya tenemos tu vídeo, ahora dinos el segundo de inicio y el de fin de tu GIF en este formato: /gif <segundo-inicio> <segundo-fin>")

# Video --> Audio
"""
    onlyaudio_ask_video: Mensaje de inicio tras mandar /onlyaudio, pide video al usuario
    onlyaudio: Recibe el vídeo del usuario, extrae el audio y se lo devuelve en mp3
"""


@bot.message_handler(commands=['onlyaudio'])
def onlyaudio_ask_video(message):
    bot.send_message(message.chat.id, "Mándanos el vídeo del que quieres obtener el audio")
    userStep[message.chat.id] = 3


@bot.message_handler(content_types=['video', 'document'], func=lambda message: get_user_step(message.chat.id) == 3)
def onlyaudio(message):
    file_info = None
    filename = ''

    if not message.document:
        file_info = bot.get_file(message.video.file_id)
        filename = file_info.file_path.split("/")[len(file_info.file_path.split("/")) - 1]
    else:
        file_info = bot.get_file(message.document.file_id)
        filename = message.document.file_name

    downloaded_file = bot.download_file(file_info.file_path)
    new_File = open(file_info.file_path.split("/")[1], 'wb')
    new_File.write(downloaded_file)
    new_File.close()
    fn = file_info.file_path.split("/")[1].split('.')[0]
    os.system(" ffmpeg -i " + file_info.file_path.split("/")[1] + " -vn -ar 44100 -ac 2 -ab 192 -f mp3 " + fn + "-audio.mp3")
    audio = open(fn + "-audio.mp3", 'r')
    bot.send_message(message.chat.id, "Aquí tienes tu audio!")
    bot.send_audio(message.chat.id, audio)
    os.remove(fn + "-audio.mp3")

# Video --> Imagen únicamente
"""
    onlyvideo_ask_video: Mensaje de inicio tras mandar /onlyvideo, pide video al usuario
    onlyvideo: Recibe el vídeo del usuario, extrae la imagen y se lo devuelve
"""

@bot.message_handler(commands=['onlyvideo'])
def onlyvideo_ask_video(message):
    bot.send_message(message.chat.id, "Mándanos el vídeo del que quieres quitar el audio")
    userStep[message.chat.id] = 4


@bot.message_handler(content_types=['video', 'document'], func=lambda message: get_user_step(message.chat.id) == 4)
def onlyvideo(message):

    file_info = None
    filename = ''

    if not message.document:
        file_info = bot.get_file(message.video.file_id)
        filename = file_info.file_path.split("/")[len(file_info.file_path.split("/")) - 1]
    else:
        file_info = bot.get_file(message.document.file_id)
        filename = message.document.file_name

    downloaded_file = bot.download_file(file_info.file_path)
    new_File = open(file_info.file_path.split("/")[1], 'wb')
    new_File.write(downloaded_file)
    new_File.close()
    fn = file_info.file_path.split("/")[1].split('.')[0]
    os.system("ffmpeg -i " + file_info.file_path.split("/")[1] + " -an -vcodec copy " + fn + "-mute.mp4")
    video = open( fn + "-mute.mp4", 'r')
    bot.send_message(message.chat.id, "Aquí tienes tu vídeo sin sonido!")
    bot.send_video(message.chat.id, video)
    os.remove(fn + "-mute.mp4")

# Video recortado
'''
    clip_ask_video: Mensaje de inicio tras mandar /gif, pide video al usuario
    clip_ask_seconds: Recibe el vídeo del usuario y le pide los segundos de inicio y fin
    clip: Recoge los segundos de inicio y fin y envía el video recortado
'''

@bot.message_handler(commands=['clip'], func=lambda message: len(message.text.split()) == 3)
def clip(message):
    msg = message.text.split()
    inicio = int(msg[1])
    final = int(msg[2])
    duracion = final - inicio
    if inicio < 0:
        bot.send_message(message.chat.id, "¿Segundo de inicio negativo? Qué malo eres...")
    elif final < 0:
        bot.send_message(message.chat.id, "¿Segundo de fin negativo? Qué malo eres...")
    else:
        file = open("filename.txt", "r")
        cadena = file.readline()[:-1]
        #Duracion del video
        os.system("ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 " + cadena + " > duracion.txt")
        fileDuracion = open("duracion.txt", "r")
        segundosvideo = int(fileDuracion.readline()[:-1].split(".")[0])
        if duracion < 0:
            bot.send_message(message.chat.id, "Los datos que nos has indicado no son correctos, indica correctamente segundo de inicio y fin")
        elif inicio > segundosvideo or final > segundosvideo:
            bot.send_message(message.chat.id, "El vídeo es más corto, indica otro segundo de inicio o fin.")
        else:
            os.system("mkdir frames")
            fn = cadena.split('.')[0]
            os.system("ffmpeg -ss " + str(inicio) + " -t " + str(duracion) + " -i " + cadena + " " + fn +"-recortado.mp4")
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, "Aquí tienes tu vídeo recortado")
            video = open(fn +"-recortado.mp4", 'r')
            bot.send_video(message.chat.id, video)
            os.remove(cadena)
            os.remove(fn +"-recortado.mp4")
            os.remove("filename.txt")
            os.system("rm -Rf frames/")
        os.remove("duracion.txt")

@bot.message_handler(commands=['clip'])
def clip_ask_video(message):
    bot.send_message(message.chat.id, "Mándanos el vídeo que quieres que recortemos")
    userStep[message.chat.id] = 5


@bot.message_handler(content_types=['video', 'document'], func=lambda message: get_user_step(message.chat.id) == 5)
def clip_ask_seconds(message):

    file_info = None
    filename = ''

    if not message.document:
        file_info = bot.get_file(message.video.file_id)
        filename = file_info.file_path.split("/")[len(file_info.file_path.split("/")) - 1]
    else:
        file_info = bot.get_file(message.document.file_id)
        filename = message.document.file_name
    downloaded_file = bot.download_file(file_info.file_path)
    new_File = open(file_info.file_path.split("/")[1], 'wb')
    os.system("echo " + file_info.file_path.split("/")[1] + " > filename.txt")
    new_File.write(downloaded_file)
    new_File.close()
    bot.send_message(message.chat.id,"Perfecto, ya tenemos tu vídeo, ahora dinos el segundo de inicio y el de fin de tu video en este formato: /clip <segundo-inicio> <segundo-fin>")



# Video + audio
"""
    videoaudio_ask_video: Recibe el comando del usuario y le pide el vídeo
    videoaudio_ask_audio: Recibe el video del usuario y le pide el audio
    videoaudio: Recibe el audio del usuario, lo une con el vídeo y se lo devuelve al usuario
"""


@bot.message_handler(commands=['videoaudio'])
def videoaudio_ask_video(message):
    bot.send_message(message.chat.id, "Mándanos el vídeo que quieres que unamos con el audio")
    userStep[message.chat.id] = 6


@bot.message_handler(content_types=['video', 'document'], func=lambda message: get_user_step(message.chat.id) == 6)
def videoaudio_ask_audio(message):
    file_info = None
    filename = ''

    if not message.document:
        file_info = bot.get_file(message.video.file_id)
        filename = file_info.file_path.split("/")[len(file_info.file_path.split("/")) - 1]
    else:
        file_info = bot.get_file(message.document.file_id)
        filename = message.document.file_name

    downloaded_file = bot.download_file(file_info.file_path)
    new_File = open(file_info.file_path.split("/")[1], 'wb')
    os.system("echo " + file_info.file_path.split("/")[1] + " > video.txt")
    new_File.write(downloaded_file)
    new_File.close()
    bot.send_message(message.chat.id, "Perfecto, ya tenemos tu vídeo, ahora envíanos el archivo de audio")
    userStep[message.chat.id] = 7


@bot.message_handler(content_types=['audio'], func=lambda message: get_user_step(message.chat.id) == 7)
def videoaudio(message):
    file_info = bot.get_file(message.audio.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    new_File = open(str(message.chat.id) + ".mp3", 'wb')
    new_File.write(downloaded_file)
    new_File.close()
    filevideo = open("video.txt", "r")
    videoinput = filevideo.readline()[:-1]
    os.system("ffmpeg -i " + videoinput + " -i " + str(message.chat.id) + ".mp3" + " -map 0:v -map 1:a -c:v libx264 -c:a libvorbis -shortest " + str(message.chat.id) + "-join.mkv")
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "Aquí tienes tu vídeo con el audio que querías")
    video = open(str(message.chat.id) + "-join.mkv", 'r')
    bot.send_video(message.chat.id, video)
    os.remove(str(message.chat.id) + "-join.mkv")
    os.remove("video.txt")
    os.remove(videoinput)
    os.remove(str(message.chat.id) + ".mp3")

# Conversión de vídeo

"""
    convert_ask_video: Pide el vídeo al usuario que desea convertir
    convert_ask_format: Recibe el vídeo y pide el formato en el que quiere el vídeo
    convert: Recibe el formato a convertir de convert o la calidad a comprimir y realiza la operación
"""


@bot.message_handler(commands=['convert'])
def convert_ask_video(message):
    bot.send_message(message.chat.id, "Mándanos el vídeo que quieres que cambiemos de formato")
    userStep[message.chat.id] = 8


@bot.message_handler(content_types=['video', 'document'], func=lambda message: get_user_step(message.chat.id) == 8)
def convert_ask_format(message):
    file_info = None
    filename = ''

    if not message.document:
        file_info = bot.get_file(message.video.file_id)
        filename = file_info.file_path.split("/")[len(file_info.file_path.split("/")) - 1]
    else:
        file_info = bot.get_file(message.document.file_id)
        filename = message.document.file_name

    downloaded_file = bot.download_file(file_info.file_path)
    new_File = open(filename, 'wb')
    new_File.write(downloaded_file)
    new_File.close()

    if message.document:
        formatFile = message.document.mime_type.split("/")[len(message.document.mime_type.split("/")) - 1]
    else:
        formatFile = filename.split(".")[len(filename.split(".")) - 1]

    # Sacar las opciones de conversión posibles menos la del formato del video recibido.
    reply_markup = types.InlineKeyboardMarkup(row_width=1)
    for f in formats:
        if formatFile != f:
            reply_markup.add(types.InlineKeyboardButton(f.upper(), callback_data=f))

    lastMsg = bot.send_message(message.chat.id, "El video que has enviado es " + filename.split(".")[
        len(filename.split(".")) - 1].upper() + ". Selecciona el formato al que deseas convertir el video:",
                               reply_markup=reply_markup)
    oldMessages[lastMsg.message_id] = filename

# Compresión de vídeo

"""
    compress_ask_video: Pide el vídeo al usuario que desea comprimir
    compress_ask: Recibe el vídeo y pide el la calidad a la que se quiere comprimir el vídeo
    convert: Recibe el formato a convertir de convert o la calidad a comprimir y realiza la operación
"""

@bot.message_handler(commands=['compress'])
def compress_ask_video(message):
    bot.send_message(message.chat.id, "Mándanos el vídeo que quieres comprimir")
    userStep[message.chat.id] = 9


@bot.message_handler(content_types=['video', 'document'], func=lambda message: get_user_step(message.chat.id) == 9)
def compress_ask(message):
    file_info = None
    filename = ''

    if not message.document:
        file_info = bot.get_file(message.video.file_id)
        filename = file_info.file_path.split("/")[len(file_info.file_path.split("/")) - 1]
    else:
        file_info = bot.get_file(message.document.file_id)
        filename = message.document.file_name

    downloaded_file = bot.download_file(file_info.file_path)
    new_File = open(filename, 'wb')
    new_File.write(downloaded_file)
    new_File.close()

    if message.document:
        formatFile = message.document.mime_type.split("/")[len(message.document.mime_type.split("/")) - 1]
    else:
        formatFile = filename.split(".")[len(filename.split(".")) - 1]

    # Sacar las opciones de conversión posibles menos la del formato del video recibido.
    reply_markup = types.InlineKeyboardMarkup(row_width=1)
   
    reply_markup.add(types.InlineKeyboardButton("Baja", callback_data="Baja"))
    reply_markup.add(types.InlineKeyboardButton("Media", callback_data="Media"))
    reply_markup.add(types.InlineKeyboardButton("Alta", callback_data="Alta"))

    lastMsg = bot.send_message(message.chat.id, "Selecciona la calidad a la que deseas comprimir el video:",
                               reply_markup=reply_markup)
    oldMessages[lastMsg.message_id] = filename


@bot.callback_query_handler(func=lambda call: True)
def convert(call):
    if call.data in formats:

        convertMsg = send_message_with_action(call.from_user.id, "Convirtiendo a " + call.data.upper(), 'typing')
        oldFile = oldMessages[call.message.message_id]
        # Saca información del video: codec, audio, formato, etc.
        # bot.answer_callback_query(call.id, text="Esto es una prueba de notificación")

        # Para que se convierta el video hay que cambiar algo del video aparte del formato. Esto es provisional pero habría que mejorarlo.
        newFile = oldFile.split(".")[0] + "." + call.data
        msg = "ffmpeg -i " + oldFile + " -ar 44100 " + newFile
        os.system(msg)

        time.sleep(1)
        bot.edit_message_text("¡Conversión completada!", chat_id=call.from_user.id, message_id=convertMsg.message_id)

        video = open(newFile, 'rb')
        bot.send_video(call.from_user.id, video)
        os.remove(oldFile)
        os.remove(newFile)

    else:
        compressMsg = send_message_with_action(call.from_user.id, "Comprimiendo en calidad " + call.data, 'typing')
        oldFile = oldMessages[call.message.message_id]
        # Saca información del video: codec, audio, formato, etc.
        # bot.answer_callback_query(call.id, text="Esto es una prueba de notificación")

        newFile = oldFile.split(".")[0] + "_Comprimido." + oldFile.split(".")[1] 
        msg = "ffprobe -v error -select_streams v:0 -show_entries stream=bit_rate -of default=noprint_wrappers=1:nokey=1 " + oldFile 
        os.system(msg + " > bitrate.txt")
        fileBitrate = open("bitrate.txt", "r")
        bitrate = int(fileBitrate.readline()[:-1])
        if call.data == "Baja":
            bitrate = bitrate * 0.1
        elif call.data == "Media":
            bitrate = bitrate * 0.2
        elif call.data == "Alta" :
            bitrate = bitrate * 0.5
        msg1 = "ffmpeg -i " + oldFile +" -b " +  str(bitrate) + " " + newFile
        os.system(msg1);
        bot.edit_message_text("¡Compresión completada!", chat_id=call.from_user.id, message_id=compressMsg.message_id)

        video = open(newFile, 'rb')
        bot.send_video(call.from_user.id, video)
        os.remove(oldFile)
        os.remove(newFile)
        os.remove("bitrate.txt")

def send_message_with_action(chat_id, msg, action, parse_mode=None):
  
  bot.send_chat_action(chat_id, action)
  if len(msg) > 35:
    time.sleep(2)
  else:
    time.sleep(1)
  return bot.send_message(chat_id, msg, parse_mode=parse_mode)

bot.polling()
