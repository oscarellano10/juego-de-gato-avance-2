import turtle
from turtle import Turtle, Screen
from random import randint
import time


screen = Screen()
screen.setup(width=600,height=600)
screen.bgcolor('black')
screen.tracer(0)


global turns
turns = 0


global winner
winner = False


global rounds
rounds = 0


numbers = []


crosses = [0, 0, 0, 0, 0, 0, 0, 0, 0]


coor_grid = [(-200,200),(0,200),(200,200),(-200,0),(0,0),(200,0),(-200,-200),(0,-200),(200,-200)]


grid = ['-','-','-','-','-','-','-','-','-']


# Aqui la computadora hace el board de 3 x 3
def make_board():
   turtle = Turtle()
   turtle.color('white')
   turtle.pensize(20)
   turtle.up()
   x_pos = -250
   y_pos = 100
   for i in range(2):
       turtle.setpos(x_pos,y_pos)
       turtle.down()
       x_pos = 250
       turtle.goto(x_pos,y_pos)
       turtle.up()
       x_pos = -250
       y_pos = -100
   x_pos = -100
   y_pos = 250
   for i in range(2):
       turtle.up()
       turtle.setpos(x_pos,y_pos)
       turtle.down()
       y_pos = -250
       turtle.goto(x_pos,y_pos)
       turtle.up()
       x_pos = 100
       y_pos = 250
   for i in range(0, 9):
       add_number(i)
   print(numbers)


# Utilizando turtles, agrega los numeros en cada seccion del board
def add_number(i):
   coordinates = coor_grid[i]
   turtle = Turtle()
   turtle.up()
   turtle.goto(coordinates)
   turtle.color('white')
   turtle.hideturtle()
   turtle.write(arg=i+1,align='center',font=('arial',20,'normal'))
   numbers.append(turtle)

# Borra todos los numeros del board
def clear_board():
   global rounds
   global grid
   global turns
   global numbers
   global crosses
   screen.update()
   time.sleep(1)
   turns = 0
   grid = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
   rounds += 1
   print(f"ROUND {rounds + 1} REACHED")
   n = 0
   print(crosses)
   for cross in crosses:
       n *= 1
       if cross != 0:
           cross.clear()
           cross = 0
       else:
           print("0")
   print(numbers)
   numbers = []
   screen.update()
   make_board()


# Con el input de user dibuja una X blanca en el slot seleccionado
def make_x(x):
   global winner
   global turns
   if grid[x] == '-':
       coords = coor_grid[x]
       turtle = Turtle()
       turtle.hideturtle()
       turtle.up()
       turtle.goto(coords)
       turtle.color('white')
       turtle.pensize(10)
       turtle.right(45)
       turtle.down()
       for i in range(4):
           turtle.forward(50)
           turtle.backward(50)
           turtle.right(90)
       grid[x] = 'x'
       crosses[x] = turtle
       check_availability('x')
   if turns >= 8:
       print("Game over")
       clear_board()
   else:
       print(turns)
       check_center()
   screen.update()


# Checa si el centro esta disponible
def check_center():
   if grid[4] == '-':
       print("Center taken!")
       make_o(4)
   else:
       o_defense1()


# Despues de las funciones inteligentes, aqui hace el dibujo de una X roja. Si no está disponible. Escoge una random
def make_o(chosen):
   global turns
   if grid[chosen] == '-':
       screen.update()
       time.sleep(0.5)
       numbers[chosen].clear()
       numbers[chosen] = 0
       coords = coor_grid[chosen]
       turtle = Turtle()
       turtle.hideturtle()
       turtle.up()
       turtle.goto(coords)
       turtle.color('red')
       turtle.pensize(10)
       turtle.right(45)
       turtle.down()
       for i in range(4):
           turtle.forward(50)
           turtle.backward(50)
           turtle.right(90)
       grid[chosen] = 'o'
       crosses[chosen] = turtle
       screen.update()
       turns += 2
   else:
       print("RANDOM CHOSEN")
       chosen = randint(0,8)
       make_o(chosen)
   check_availability('o')

# Busca si alguna de las esquinas esta disponible. Solo funciona al inicio del juego
def intelligent_o():
   global turns
   print(turns)
   if turns <= 2:
       print("Intelligent O")
       if grid[0] == "-":
           make_o(0)
           return
       elif grid[2] == "-":
           make_o(2)
           return
       elif grid[6] == "-":
           make_o(6)
           return
       elif grid[8] == "-":
           make_o(8)
           return
       else:
           print("Nothing found!")
           rand = randint(0,8)
           make_o(rand)
   else:
       rand = randint(0,8)
       make_o(rand)


# Checa patrones para poder ganar
def lines_to_win():
   for i in range(3):
       if grid[i] == 'o' and grid[i + 3] == 'o' and grid[i + 6] == '-':
           make_o(i + 6)
           return
   for i in range(3):
       if grid[i] == '-' and grid[i + 3] == 'o' and grid[i + 6] == 'o':
           make_o(i)
           return
   for i in range(0,9,3):
       if grid[i] == 'o' and grid[i + 1] == 'o' and grid[i + 2] == '-':
           make_o(i + 2)
           return
   for i in range(0,9,3):
       if grid[i] == '-' and grid[i + 1] == 'o' and grid[i + 2] == 'o':
           make_o(i)
           return
   for i in range(0, 9, 3):
       if grid[i] == 'o' and grid[i + 1] == '-' and grid[i + 2] == 'o':
           make_o(i + 1)
           return
   for i in range(3):
       if grid[i] == 'o' and grid[i + 3] == '-' and grid[i + 6] == 'o':
           make_o(i + 3)
           return
   print("not found")

   # Esta funcion busca soluciones cuando el X rojo esta en el centro.
   # Esto funciona porque la diferencia de 8 - un slot siempre será igual al slot adjacente.
   # Esto se hace usando un ciclo for que funciona asi:
   # El primer slot vale 0, entonces el slot del otro lado del centro vale 8.
   # Asi que 8 - 0 = 8. Y asi checa el slot 8 si está disponible

   if grid[4] == 'o':
       print("OPTION 1 ")
       for i in range(9):
           if grid[i] == 'x' and grid[4] == 'x':
               if i == 4:
                   continue
               difference = 8 - i
               make_o(difference)
               return
       make_o(randint(0,8))
       print("Nothing found")
   elif grid[0] == 'o' and grid[4] == '-' and grid[8] == 'o':
       make_o(4)
       return
   elif grid[2] == 'o' and grid[4] == '-' and grid[6] == 'o':
       make_o(4)
       return
   else:
       intelligent_o()

def o_defense1():
   #print(turns)
   if turns % 2 == 0 and turns == 2 and grid[4] == 'x':

       # Este ciclo for es igual que el pasado
       # Nada mas que está hecho para jugar defensa.

       for i in range(9):
           if grid[i] == 'x' and grid[4] == 'x':
               if i == 4:
                   continue
               difference = 8 - i
               if grid[difference] != "-":
                   intelligent_o()
                   return
               print("O DEFENSE 1 TAKEN")
               print(difference)
               make_o(difference)
               return
   else:
       print("Going to O DEFENSE 2")
       o_defense2()

def o_defense2():

   # Aqui la computadora checa todos los slots individualmente para bloquear el jugador

   for i in range(3):
       if grid[i] == 'x' and grid[i + 3] == 'x' and grid[i + 6] == '-':
           make_o(i + 6)
           return
   for i in range(3):
       if grid[i] == '-' and grid[i + 3] == 'x' and grid[i + 6] == 'x':
           make_o(i)
           return
   for i in range(0,9,3):
       if grid[i] == 'x' and grid[i + 1] == 'x' and grid[i + 2] == '-':
           make_o(i + 2)
           return
   for i in range(0,9,3):
       if grid[i] == '-' and grid[i + 1] == 'x' and grid[i + 2] == 'x':
           make_o(i)
           return
   for i in range(0,9,3):
       if grid[i] == 'x' and grid[i + 1] == '-' and grid[i + 2] == 'x':
           make_o(i + 1)
           return
   for i in range(3):
       if grid[i] == 'x' and grid[i + 3] == '-' and grid[i + 6] == 'x':
           make_o(i + 3)
           return
   if grid[0] == 'x' and grid[4] == '-' and grid[8] == 'x':
       make_o(4)
       return
   elif grid[2] == 'x' and grid[4] == '-' and grid[6] == 'x':
       make_o(4)
       return
   else:
       print("Going to O DEFENSE 3")
       o_defense3()


def o_defense3():

   # Hace lo mismo que o_defense1. La diferencia es que aqui es para cualquier turno.
   # Mientras o_defense1 solo lo hace el inicio del juego.

   for i in range(9):
       if grid[i] == 'x' and grid[4] == 'x':
           if i == 4:
               continue
           difference = 8 - i
           if grid[difference] != '-':
               continue
           print("O DEFENSE 3 TAKEN")
           make_o(difference)
           return
   print("Going to Lines to win!")
   lines_to_win()

def check_availability(shape):

   # Checa la disponabilidad de todas las combinaciones para poder ganar.
   # Me falta aun optimizarlo usando ciclos for.

   global rounds
   x = 0
   if grid[x] == shape and grid[x+3] == shape and grid[x+6] == shape:
       print(f"{shape} wins!")
       clear_board()
   if grid[x+1] == shape and grid[x+4] == shape and grid[x+7] == shape:
       print(f"{shape} wins!")
       clear_board()
   if grid[x+2] == shape and grid[x+5] == shape and grid[x+8] == shape:
       print(f"{shape} wins!")
       clear_board()
   if grid[x] == shape and grid[x+1] == shape and grid[x+2] == shape:
       print(f"{shape} wins!")
       clear_board()
   if grid[x+3] == shape and grid[x+4] == shape and grid[x+5] == shape:
       print(f"{shape} wins!")
       clear_board()
   if grid[x+6] == shape and grid[x+7] == shape and grid[x+8] == shape:
       print(f"{shape} wins!")
       clear_board()
   if grid[x] == shape and grid[x+4] == shape and grid[x+8] == shape:
       print(f"{shape} wins!")
       clear_board()
   if grid[x+2] == shape and grid[x+4] == shape and grid[x+6] == shape:
       print(f"{shape} wins!")
       clear_board()


# Funciones para los inputs del usuario.
def add_x_0():
   numbers[0].clear()
   numbers[0] = 0
   screen.update()
   make_x(0)


def add_x_1():
   numbers[1].clear()
   numbers[1] = 0
   screen.update()
   make_x(1)


def add_x_2():
   numbers[2].clear()
   numbers[2] = 0
   screen.update()
   make_x(2)


def add_x_3():
   numbers[3].clear()
   numbers[3] = 0
   screen.update()
   make_x(3)


def add_x_4():
   global center
   center = True
   numbers[4].clear()
   numbers[4] = 0
   screen.update()
   make_x(4)


def add_x_5():
   numbers[5].clear()
   numbers[5] = 0
   screen.update()
   make_x(5)


def add_x_6():
   numbers[6].clear()
   numbers[6] = 0
   screen.update()
   make_x(6)


def add_x_7():
   numbers[7].clear()
   numbers[7] = 0
   screen.update()
   make_x(7)


def add_x_8():
   numbers[8].clear()
   numbers[8] = 0
   screen.update()
   make_x(8)




make_board()
screen.listen()
screen.onkey(add_x_0, '1')
screen.onkey(add_x_1, '2')
screen.onkey(add_x_2, '3')
screen.onkey(add_x_3, '4')
screen.onkey(add_x_4, '5')
screen.onkey(add_x_5, '6')
screen.onkey(add_x_6, '7')
screen.onkey(add_x_7, '8')
screen.onkey(add_x_8, '9')


screen.exitonclick()

