#!/usr/bin/python
import curses
import random

screen = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_WHITE)
curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_YELLOW)
curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_WHITE)
curses.init_pair(8, curses.COLOR_RED, curses.COLOR_BLACK)
dims = screen.getmaxyx()
gridsize = [9, 9]
mines = 10
curses.noecho()
screen.keypad(1)

topguy = {'Happy': ':-)', 'Surprised': ':-o', 'Dead': 'X-(', 'Done': 'B-)'}

def gridpos((y, x)):
  return (y-((dims[0]-gridsize[0])/2), x-((dims[1]-gridsize[1])/2))

def dig(display, minegrid, gameover, grid, (y, x)):
  if display[y][x] == 0:
    display[y][x] = 1
    if grid[y][x] == 0:
      dig(display, minegrid, gameover, grid, (y, x))
    if minegrid[y][x] == 1:
      gameover = True
  elif display[y][x] == 1:
    if y>0:
      if display[y-1][x]==0:
        dig(display, minegrid, gameover, grid, (y-1, x))
      if x>0:
        if display[y-1][x-1] == 0:
          dig(display, minegrid, gameover, grid, (y-1, x-1))
      if x<gridsize[1]-1:
        if display[y-1][x+1] == 0:
          dig(display, minegrid, gameover, grid, (y-1, x+1))
    if x>0:
      if display[y][x-1] == 0:
        dig(display, minegrid, gameover, grid, (y, x-1))
    if x<gridsize[1]-1:
      if display[y][x+1]==0:
        dig(display, minegrid, gameover, grid, (y, x+1))
    if y<gridsize[0]-1:
      if display[y+1][x] == 0:
        dig(display, minegrid, gameover, grid, (y+1, x))
      if x>0:
        if display[y+1][x-1] == 0:
          dig(display, minegrid, gameover, grid, (y+1, x-1))
      if x<gridsize[1]-1:
        if display[y+1][x+1]==0:
          dig(display, minegrid, gameover, grid, (y+1, x+1))      

def game():
  screen.refresh()
  gameover = False
  win = False
  action = - 1
  display = []
  row = []
  minegrid = []
  grid = []
  face = 'Happy'
  refresh = True
  for z in range(gridsize[1]):
    row.append(0)
  for z in range(gridsize[0]):
    grid.append(row[:])
    display.append(row[:])
    minegrid.append(row[:])
  gridmade = False
  cursor = [(dims[0]-gridsize[0])/2, (dims[1]-gridsize[1])/2]
  while action != ord('q') and not gameover:
    if refresh:
      win = True
      screen.clear()
      for z in range(len(display)):
        for r in range(len(display[z])):
          if display[z][r] == -1:
            screen.addch((dims[0]-gridsize[0])/2+z, (dims[1]-gridsize[1])/2+r, ord('F'), curses.color_pair(8)|curses.A_BOLD|curses.A_REVERSE)
            if grid[z][r] < 9:
              win = False
          elif display[z][r] == 1:
            if grid[z][r]:
              screen.addch((dims[0]-gridsize[0])/2+z, (dims[1]-gridsize[1])/2+r, ord(str(grid[z][r])), curses.color_pair(grid[z][r] % 6 + grid[z][r]/6))
            else:
              screen.addch((dims[0]-gridsize[0])/2+z, (dims[1]-gridsize[1])/2+r, ord(str(grid[z][r])), curses.color_pair(7))
            if grid[z][r] == 9:
              gameover = True
          else:
            screen.addch((dims[0]-gridsize[0])/2+z, (dims[1]-gridsize[1])/2+r, ord('+'))
            if grid[z][r]<9:
              win = False
      for r in range((dims[0]-gridsize[0])/2, (dims[0]+gridsize[0])/2):
        screen.addch(r, (dims[1]-gridsize[1])/2-1, ord('|'))
        screen.addch(r, (dims[1]+gridsize[1])/2, ord('|'))
      for r in range((dims[1]-gridsize[1])/2, (dims[1]+gridsize[1])/2):
        screen.addch((dims[0]-gridsize[0])/2-1, r, ord('-'))
        screen.addch((dims[0]+gridsize[0])/2, r, ord('-'))
      screen.refresh()
      refresh = False
    screen.addstr((dims[0]-gridsize[0])/2-2, dims[1]/2-2, topguy[face], curses.color_pair(6))
    screen.move(cursor[0], cursor[1])
    if win:
      gameover = True
    if not gameover:
      action = screen.getch()
    if action == curses.KEY_LEFT:
      if screen.inch(cursor[0], cursor[1]-1) == ord('|'):
        cursor[1] += gridsize[1]
      face = 'Surprised'
      cursor[1] -= 1
    elif action == curses.KEY_RIGHT:
      if screen.inch(cursor[0], cursor[1]+1) == ord('|'):
        cursor[1] -= gridsize[1]
      face = 'Surprised'
      cursor[1] += 1
    elif action == curses.KEY_DOWN:
      if screen.inch(cursor[0]+1, cursor[1]) == ord('-'):
        cursor[0] -= gridsize[0]
      face = 'Surprised'
      cursor[0] += 1
    elif action == curses.KEY_UP:
      if screen.inch(cursor[0]-1, cursor[1]) == ord('-'):
        cursor[0] += gridsize[0]
      face = 'Surprised'
      cursor[0] -= 1
    elif action == ord('d') and display[gridpos(cursor)[0]][gridpos(cursor)[1]] >=0:
      face = 'Happy'
      refresh = True
      if not gridmade:
        gridmade = True
        firstmove = gridpos(cursor)
        minesmade = 0
        while minesmade < mines:
          minemade=False
          while not minemade:
            mine = (random.randrange(gridsize[0]), random.randrange(gridsize[1]))
            if grid[mine[0]][mine[1]] >= 0 and mine != firstmove:
              minemade = True
          minesmade += 1
          minegrid[mine[0]][mine[1]] = 1
        for r in range(len(grid)):
          for z in range(len(grid[r])):
            if minegrid[r][z] == 0:
              if r>0:
                grid[r][z] += minegrid[r-1][z]
                if z>0:
                  grid[r][z] += minegrid[r-1][z-1]
                if z<gridsize[1]-1:
                  grid[r][z] += minegrid[r-1][z+1]
              if z>0:
                grid[r][z] += minegrid[r][z-1]
              if z<gridsize[1]-1:
                grid[r][z] += minegrid[r][z+1]               
              if r<gridsize[0]-1:
                grid[r][z] += minegrid[r+1][z]
                if z>0:
                  grid[r][z] += minegrid[r+1][z-1]
                if z<gridsize[1]-1:
                  grid[r][z] += minegrid[r+1][z+1]
            else:
              grid[r][z] = 9
      if minegrid[gridpos(cursor)[0]][gridpos(cursor)[1]]:
        gameover = True
        display[gridpos(cursor)[0]][gridpos(cursor)[1]] = 1
      else:
        dig(display, minegrid, gameover, grid, gridpos(cursor))
    elif action == ord('f') and display[gridpos(cursor)[0]][gridpos(cursor)[1]]<=0:
      refresh = True
      display[gridpos(cursor)[0]][gridpos(cursor)[1]] = -(display[gridpos(cursor)[0]][gridpos(cursor)[1]] +1)
      face = 'Happy'
  if not win:
    face = 'Dead'
  else:
    face = 'Done'
  screen.addstr((dims[0]-gridsize[0])/2-2, dims[1]/2-2, topguy[face], curses.color_pair(6))
  for z in range(len(display)):
    for r in range(len(display[z])):
      if display[z][r] == -1:
        if minegrid[z][r] == 1:
          screen.addch((dims[0]-gridsize[0])/2+z, (dims[1]-gridsize[1])/2+r, ord('F'), curses.A_BOLD|curses.color_pair(8)|curses.A_REVERSE)
        else:
          screen.addch((dims[0]-gridsize[0])/2+z, (dims[1]-gridsize[1])/2+r, ord('x'))
      elif minegrid[z][r] == 1:
        if not win:
          if not display[z][r]:
            screen.addch((dims[0]-gridsize[0])/2+z, (dims[1]-gridsize[1])/2+r, ord('*'), curses.color_pair(8))
          else:
            screen.addch((dims[0]-gridsize[0])/2+z, (dims[1]-gridsize[1])/2+r, ord('*'), curses.color_pair(8)|curses.A_REVERSE)
        else:
          screen.addch((dims[0]-gridsize[0])/2+z, (dims[1]-gridsize[1])/2+r, ord('F'), curses.A_BOLD|curses.color_pair(8)|curses.A_REVERSE)
      elif display[z][r] == 1:
        if minegrid[z][r] < 9:
          if grid[z][r]>0:
            screen.addch((dims[0]-gridsize[0])/2+z, (dims[1]-gridsize[1])/2+r, ord(str(grid[z][r])), curses.color_pair(grid[z][r]%6 + grid[z][r]/6))
          else:
            screen.addch((dims[0]-gridsize[0])/2+z, (dims[1]-gridsize[1])/2+r, ord(str(grid[z][r])), curses.color_pair(7))
        if grid[z][r] == 9:
          gameover = True
      else:
        screen.addch((dims[0]-gridsize[0])/2+z, (dims[1]-gridsize[1])/2+r, ord('+'))
  if win:
    screen.addstr((dims[0]+gridsize[0])/2+1, dims[1]/2-4, 'You won!')
  else:
    screen.addstr((dims[0]+gridsize[0])/2+1, dims[1]/2-4, 'You lost')
  r = screen.getch()
  if r == ord(' '):
    game()
  elif r == ord('q'):
    pass
  else:
    menu()


def menu():
  global gridsize, mines
  selection = - 1
  option = 0
  while selection < 0:
    graphics = [curses.A_NORMAL]*5
    graphics[option] = curses.A_BOLD
    screen.clear()
    screen.addstr(0, dims[1]/2-6, 'Minesweeper')
    screen.addstr(dims[0]/2-2, dims[1]/2-6, 'Beginner Game', graphics[0])
    screen.addstr(dims[0]/2-1, dims[1]/2-8, 'Intermediate Game', graphics[1])
    screen.addstr(dims[0]/2, dims[1]/2-5, 'Expert Game', graphics[2])
    screen.addstr(dims[0]/2+1, dims[1]/2-5, 'Custom Game', graphics[3])
    screen.addstr(dims[0]/2+2, dims[1]/2-2, 'Quit', graphics[4])
    action = screen.getch()
    if action == curses.KEY_DOWN:
      option = (option+1)%5
    elif action == curses.KEY_UP:
      option = (option-1)%5
    elif action == ord(' ') or action == ord('\n'):
      selection = option
  if selection == 0:
    gridsize = [9, 9]
    mines = 10
  elif selection == 1:
    gridsize = [16, 16]
    mines = 40
  elif selection == 2:
    gridsize = [16, 30]
    mines = 100
  if selection < 3:
    game()
  elif selection == 3:
    customgame()

def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def customgame():
  global gridsize, mines
  selection = - 1
  option = 0
  while selection < 3:
    graphics = [curses.A_NORMAL]*5
    graphics[option] = curses.A_BOLD
    screen.clear()
    menuwords = ['Width: '+ str(gridsize[1]), 'Height: '+ str(gridsize[0]), 'Mines: ' + str(mines), 'Play', 'Back']
    for z in range(len(menuwords)):
      screen.addstr(dims[0]/2+z-2, (dims[1]-len(menuwords[z]))/2, menuwords[z], graphics[z])
    action = screen.getch()
    if action == curses.KEY_DOWN:
      option += 1
    elif action == curses.KEY_UP:
      option -= 1
    elif action == ord('\n') or action == ord(' '):
      selection = option
    if selection == 0:
      curses.echo()
      screen.clear()
      screen.addstr(0, 0, 'Enter Width: ')
      x = screen.getstr()
      if isint(x):
        x = int(x)
        if x < 9:
          gridsize[1] = 9
        elif x > dims[1]-2:
          gridsize[1] = dims[1]-2
        else:
          gridsize[1] = x
      curses.noecho()
      selection = - 1
    if selection == 1:
      curses.echo()
      screen.clear()
      screen.addstr(0, 0, 'Enter Height: ')
      x = screen.getstr()
      if isint(x):
        x = int(x)
        if x < 9:
          gridsize[0] = 9
        elif x > dims[0]-4:
          gridsize[0] = dims[0]-4
        else:
          gridsize[0] = x
      curses.noecho()
      selection = -1
    if selection == 2:
      curses.echo()
      screen.clear()
      screen.addstr(0, 0, 'Enter Mines: ')
      x = screen.getstr()
      if isint(x):
        x = int(x)
        mines = x
      curses.noecho()
      selection = -1
    if mines < (gridsize[0])*(gridsize[1])/9:
      mines = gridsize[0]*gridsize[1]/9
    elif mines > (gridsize[1]-1)*(gridsize[0]-1):
      mines = (gridsize[1]-1)*(gridsize[0]-1)
  if selection == 3:
    game()
  else:
    menu()
    
    

menu()
curses.endwin()
