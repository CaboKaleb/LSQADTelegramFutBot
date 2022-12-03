import telebot
import random

Players = []
BackUp = []
Mejenga = ""
TipoMejenga = 0

bot = telebot.TeleBot("5688124986:AAG9rcP_HzinCZMM7FjM3Uf1PmqxOhu-XQA")

def isThereMejenga():
    return Mejenga != ""

def clearPlayers():
    global Players
    global BackUp
    Players = []
    BackUp = []

def setMejenga(mejenga,tipoMejenga):
    global Mejenga
    global TipoMejenga
    Mejenga = mejenga
    TipoMejenga = tipoMejenga

@bot.message_handler(commands=["help","ayuda"])
def help(message):
    bot.reply_to(message," Lista de Comandos activos : /help, /nuevaMejenga @DatoMejenga @TipoMejenga , /finMejenga, /estoyDentro, /estoyFuera, /comoVamos, /voyReserva, /fueraReserva ")

@bot.message_handler(commands=["nuevaMejenga"])
def nuevaMejenga(message):
    try:
        if Mejenga == "" :
            _mejengaData = message.text.split()[1]
            setMejenga(_mejengaData,int(message.text.split()[2]))
            bot.send_message(chat_id=message.chat.id,text=f"La Mejenga {_mejengaData} ha sido creada.Tipo Fut {TipoMejenga}")
        else:
            bot.reply_to( message,"Ya hay una mejenga activa, NO SEA INVECIL.")
    except Exception as err :
        print(err)

@bot.message_handler(commands=["finMejenga"])
def finMejenga(message):
    try:
        if Mejenga != "" :
            _mejengaData = message.text.split()[1:]
            bot.send_message(chat_id=message.chat.id,text=f"La Mejenga {_mejengaData[0]} ha terminado.")
            setMejenga("","")
            clearPlayers()
        else:
            bot.reply_to( message,"Ya hay una mejenga activa, NO SEA INVECIL.")
    except Exception as err :
        print(err)

@bot.message_handler(commands=["comoVamos"])
def comoVamos(message):

    if not isThereMejenga():
        bot.reply_to(message,"No hay Mejenga. Armela <3")
        return

    _message = f" --- {Mejenga} ----\n \n"
    _message = _message + f"Lista de Jugadores - Somos {len(Players)} \n \n"
    _message = _message + '\n'.join(Players) + "\n \n"
    _message = _message + "Lista de Reservas: \n \n"
    _message = _message + '\n'.join(BackUp)
    bot.send_message(chat_id=message.chat.id,text=_message)

@bot.message_handler(commands=["estoyDentro"])
def nuevaMejenga(message):

    if not isThereMejenga():
        bot.reply_to(message,"No hay Mejenga. Armela <3")
        return

    if TipoMejenga == 5 and Players.count == 10 :
         bot.reply_to(message,"Ya esta llena, muy lento pa :(")
         return

    if TipoMejenga == 8 and Players.count == 14 :
         bot.reply_to(message,"Ya esta llena, muy lento pa :(")
         return

    _nplayer = message.from_user.first_name
    if _nplayer not in Players :
        Players.append(message.from_user.first_name)
        bot.send_message(chat_id=message.chat.id,text=f"La perra de {_nplayer} se unio a la mejenga")
    else:
        bot.reply_to(message,"Ya esta en lista retardadito. :)")


@bot.message_handler(commands=["estoyFuera"])
def nuevaMejenga(message):
    if not isThereMejenga():
        bot.reply_to(message,"No hay Mejenga. Armela <3")
        return

    _nplayer = message.from_user.first_name
    if _nplayer in Players :
        Players.remove(message.from_user.first_name)
        bot.send_message(chat_id=message.chat.id,text=f"La GRAN PERRA ASQUEROSA de {_nplayer} deserto a la mejenga")
    else:
        bot.reply_to(message,"Tiene que estar en lista para salirse, subnormal. :)")

@bot.message_handler(commands=["voyReserva"])
def nuevaMejenga(message):
    if not isThereMejenga():
        bot.reply_to(message,"No hay Mejenga. Armela <3")
        return

    _nplayer = message.from_user.first_name
    if _nplayer not in BackUp :
        BackUp.append(message.from_user.first_name)
        bot.send_message(chat_id=message.chat.id,text=f"La perra de {_nplayer} se unio a la mejenga como reserva, esta cagao.")
    else:
        bot.reply_to(message,"Ya esta en lista retardadito. :)")


@bot.message_handler(commands=["fueraReserva"])
def nuevaMejenga(message):
    if not isThereMejenga():
        bot.reply_to(message,"No hay Mejenga. Armela <3")
        return

    _nplayer = message.from_user.first_name
    if _nplayer in BackUp :
        BackUp.remove(message.from_user.first_name)
        bot.send_message(chat_id=message.chat.id,text=f"La GRAN PERRA ASQUEROSA de {_nplayer} deserto a la mejenga.")
    else:
        bot.reply_to(message,"Tiene que estar en lista para salirse, subnormal. :)")

@bot.message_handler(commands=["rifarEquipos"])
def rifarEquipos(message):

    if not isThereMejenga :
         bot.reply_to(message,"No hay Mejenga. Armela <3")
         return
    
    if TipoMejenga == 5 and Players.count != 10 :
         bot.reply_to(message,"Deben de haber al menos 10 Jugadores para rifar los equipos")
         return
    
    if TipoMejenga == 8 and Players.count < 14 :
         bot.reply_to(message,"Deben de haber al menos 14 Jugadores para rifar los equipos")
         return

    _auxList = Players.copy()
    random.shuffle(_auxList)

    length = len(Players)
    middle_index = length//2
    first_half = Players[:middle_index]
    second_half = Players[middle_index:]

    _message = f" --- {Mejenga} ----\n \n"
    _message = _message + f"Lista de Jugadores - Equipo Claro \n \n"
    _message = _message + '\n'.join(first_half) + "\n \n"
    _message = _message + "Lista de Jugadores - Equipo Oscuro \n \n"
    _message = _message + '\n'.join(second_half)
    bot.send_message(chat_id=message.chat.id,text=_message)



bot.polling()
