from tkinter import *
import tkinter as tk
from tkinter import messagebox
from time import sleep
from random import randint as rd, choice

win = tk.Tk()
win.geometry( '600x500' )
win.title( 'Наша игра' )

losers = []
winners = []
ladders = []
players = {}
traps = ( -2, -1, 0, 2, "+", "!", "?", ":(", ":)" )
# -2 2шага назад
# -1 минус ход
# 0 в самое начало
# 2 шага вперед
# + дополнительный уход
# ! поменяться местами с рандомным игроком
# ? перемещение на рандомную точку
# :( поражение
# :) победа

# все новости игры
lbl = Label( win, text='ваша карта будет здесь' )
lbl.pack()


# создаем карту
def create_map( n: int ):
    global ladders
    ladders = [ 0 ] * n

#plus players
def plus( name ):
    global players
    
    players[ name ] = len( players )
    lbl.config( text=ladders )
    q_entry.pack_forget()
    


# добавление игрока
def add_players( n: int, ladders: int ):
    global val, q_entry
    if n < 2 or n > 6:
        lbl.config( text="неа так это не работает, возвращайся найди друзей и продолжим" )
        return
    
    quantity = StringVar()
    q_entry = Entry( textvariable=quantity )
    q_entry.pack()
    val = quantity.get()
    tk.Button( win, text='submit', command=lambda : plus( val  ) ).pack()
    back_btn = Button( win, text='back', command=exite )
    back_btn.pack()

    create_map( ladders )
    

# проверяем место положение лесенки
def check_ladder( index: int ) -> bool:
    return ladders[ index ] == 1


# создание ловушек
def add_traps( n: int = 5 ):
    for i in range( n ):
        trap = rd( 3, len( ladders ) - 3 )
        if check_ladder( trap ): ladders[ trap ] = choice( traps )


# проверка игрока 
def check_player( name: str ) -> bool:
    return name in list( players.keys() )
        

# удаляем игрока
def delete_player( name: str, check: bool = True ):
    if check:
        winners.append
        del players[ name ]
        lbl.config( text=f"Игрок { name } победил" )

    else:
        lbl.config( text=f"Игрок {name} проиграл" )
        del players[ name ]


# проверяем лузера
def check_loser( name: str ) -> bool:
    return name in losers


# добавляем проигравшего
def add_loser( name: str ):
    losers.append( name )


# удаление из списка лузеров
def delete_from_losers( name: str ):
    losers.remove( name )
    lbl.config( text="Игрок " + name + " удалён из лузеров" )


# если несколько игроков на 1 позиции
def update( name: str, pos: int ):
    if pos >= len( ladders ):
        delete_player( name = name )
        return
    if pos not in players.values(): players[ name ] = pos
    else: 
        lbl.config( text="Это место занят, ты пройдёшь на шаг назад" )
        check_position(name = name, pos = pos - 1)
    players[ name ] = pos
    lbl.config( text="Игрок " + name + " перемещён на новую позицию: " + str( pos ) )


# меняемся местами с игроками 
def exchange_players( name: str, pos: int ):
    new_player = choice( list( players.keys() ) )
    lbl.config( text="Игрок " + name + " поменялся местами с " + new_player )
    temp = players.get( name )
    players[ name ] = players.get( new_player )
    players[ new_player ] = temp


# проверка позиции
def check_position( name: str, pos: int ):
    if pos >= len( ladders ):
        delete_player( name = name )
        return

    if ladders[ pos ] == -2: 
        lbl.config( text="2 шага назад")
        update( name = name, pos = pos - 2 )
    elif ladders[ pos ] == -1: 
        lbl.config( text="Пропуск хода" )
        add_loser( name )
    elif ladders[ pos ] == 0:
        lbl.config( text="Обратно на старт" ) 
        update( name = name, pos = 0 )
    elif ladders[ pos ] == 2: 
        lbl.config( text="Плюс два шага" )
        update( name = name, pos = pos + 2 )
    elif ladders[ pos ] == "!": 
        lbl.config( text="Поменяться с рандомным игроком местами" )
        exchange_players( name = name, pos = pos )
    elif ladders[ pos ] == "?": 
        lbl.config( text="Перемещение на рандомную точку" )
        update( name = name, pos = rd( 0, len( ladders ) ) )
    elif ladders[ pos ] == ":(":
        lbl.config( text="Проигрыш" )
        delete_player( name = name, check = False )
        ladders[ pos ] = 1

    elif ladders[ pos ] == ":)":
        lbl.config( text="Выигрыш" )
        delete_player( name = name )
        ladders[ pos ] = 1

    elif ladders[ pos ] == "+":
        lbl.config( text="Дополнительный ход" )
        check_position( name = name, pos = rd( 1, 7 ) + pos )  # кидаем кубик

    else: update( name = name, pos = pos )


# проверка победителя
def check_winner() -> bool:
    return len( list( players.keys() ) ) < 2


#меню со стратом и выходом
def menu():
    global starts, exite
    starts = Button( win, text='Start', command=start )
    exite = Button( win, text='Exit', command=exit )

    starts.pack()
    exite.pack()


# основная игра
def start( players_number: int = 6, ladders_number: int = 30 ):
    starts.pack_forget()
    exite.pack_forget()
    add_players( players_number, ladders_number )
    add_traps( ladders_number // 10 )
    lbl.config( text=str( ladders ) )
    while not check_winner():
        for name in players.keys():
            lbl.config( text="Настала очередь: " + name )
            if not check_loser( name = name ): check_position( name = name, pos = rd( 1, 7 ) + players[ name ] ) # кидаем кубик
            else: delete_from_losers( name = name )
            sleep( 2 )

def exit():
    win.destroy()


menu()

win.mainloop()
