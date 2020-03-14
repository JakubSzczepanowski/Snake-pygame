import pygame
import random
from collections import deque
import menuOB
pygame.init()

szer = 600
wys = 600

screen = pygame.display.set_mode((szer,wys))
clock = pygame.time.Clock()
pygame.display.set_caption('Snake')

class Kwadrat:
  KIERUNEK = {'u': (0, -2), 'd': (0, 2), 'l': (-2, 0), 'r': (2, 0)}
  ZABLOKOWANY_KIERUNEK = {'u': 'd', 'd': 'u', 'l': 'r', 'r': 'l'}
  PUNKTY = 0
  def __init__(self, x, y, kierunek="r", wymiar=20):
    self.x = x
    self.y = y
    self.wymiar = wymiar
    self.kierunek = kierunek
    self.kolor = random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)
    self.kolejka = deque((wymiar//Kwadrat.KIERUNEK['d'][1] + 1) * kierunek, wymiar//Kwadrat.KIERUNEK['d'][1] + 1)
    self.ksztalt = pygame.Rect(self.x, self.y, self.wymiar, self.wymiar)
    Kwadrat.PUNKTY += 1

  def rysuj(self):
     pygame.draw.rect(screen, self.kolor, self.ksztalt, 0)

  def ruch(self):
    self.x += Kwadrat.KIERUNEK[self.kierunek][0]
    self.y += Kwadrat.KIERUNEK[self.kierunek][1]
    self.ksztalt.move_ip(*Kwadrat.KIERUNEK[self.kierunek])
    self.kolejka.append(self.kierunek)

  def set_kierunek(self, kierunek):
    if kierunek not in Kwadrat.KIERUNEK:
      raise ValueError("Zły kierunek")
    if kierunek == Kwadrat.ZABLOKOWANY_KIERUNEK[self.kierunek]:
      return
    self.kierunek = kierunek

  def jaki_kierunek_wymiar_ruchow_temu(self):
    return self.kolejka[0]

  @classmethod
  def set_KIERUNEK(cls,x):
    cls.KIERUNEK = {'u': (0, -x), 'd': (0, x), 'l': (-x, 0), 'r': (x, 0)}


class Pyton:
  def __init__(self, x, y):
    self.segmenty = [Kwadrat(x, y)]

  def ruch(self):
    self.segmenty[0].ruch()
    for i in range(1, len(self.segmenty)):
      self.segmenty[i].set_kierunek(self.segmenty[i - 1].jaki_kierunek_wymiar_ruchow_temu())
      self.segmenty[i].ruch()

  def zmien_kierunek(self, k):
    self.segmenty[0].set_kierunek(k)

  def rysuj(self):
    for k in self.segmenty:
      k.rysuj()

  def kolizja(self,player):
    return self.segmenty[0].ksztalt.colliderect(player)

  def gryz(self):
    for i in range(2, len(self.segmenty)):
      if self.segmenty[0].ksztalt.colliderect(self.segmenty[i].ksztalt):
        return True

  def wyjscie(self):
    for s in self.segmenty:
      if s.x >= szer:
        s.x = -s.wymiar
        s.ksztalt.move_ip(-szer-s.wymiar,0)
      elif s.x <= -s.wymiar:
        s.x = szer
        s.ksztalt.move_ip(szer+s.wymiar,0)
      elif s.y >= wys:
        s.y = -s.wymiar
        s.ksztalt.move_ip(0,-wys-s.wymiar)
      elif s.y <= -s.wymiar:
        s.y = wys
        s.ksztalt.move_ip(0,wys+s.wymiar)

  def dodaj_kwadrat(self):
    ostatni_kwadrat = self.segmenty[-1]
    x = ostatni_kwadrat.x
    y = ostatni_kwadrat.y
    w = ostatni_kwadrat.wymiar
    kier = ostatni_kwadrat.kierunek
    dx, dy = Kwadrat.KIERUNEK[kier]
    if dx < 0:
      dx = -1
    elif dx > 0:
      dx = 1
    else:
      if dy < 0:
        dy = -1
      elif dy > 0:
        dy = 1
    self.segmenty.append(Kwadrat(x - w * dx, y - w * dy, kier, w))
    ostatni_kwadrat.kolejka.clear()

class Orb:
    def __init__(self):
        self.x = random.randint(100,500)
        self.y = random.randint(100,500)
        self.wielkosc = 10
        self.grafika = pygame.image.load('orb.png')
        self.ksztalt = pygame.Rect(self.x,self.y,self.wielkosc,self.wielkosc)
    def rysuj(self):
        screen.blit(self.grafika,(self.x,self.y))
        self.ksztalt = pygame.Rect(self.x,self.y,self.wielkosc,self.wielkosc)

def main_menu(cz,cz_big,opcje,grafika,kursor):
  done = False
  while not done:
    screen.fill((0,0,0))
    mx,my = pygame.mouse.get_pos()
    screen.blit(grafika,(130,200))
    for opcja in opcje:
      if opcja.rect.collidepoint(pygame.mouse.get_pos()):
          opcja.hovered = True
      else:
          opcja.hovered = False
      opcja.rysuj(screen,cz)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
          if opcje[0].rect.collidepoint(pygame.mouse.get_pos()):
                gameplay(cz,cz_big,grafika,kursor,opcje)
          if opcje[1].rect.collidepoint(pygame.mouse.get_pos()):
            poziomy = [menuOB.Menu('Easy',246,165,screen,cz),menuOB.Menu('Medium',220,285,screen,cz),menuOB.Menu('Hard',244,405,screen,cz)]
            ok = False
            while not ok:
              screen.fill((0,0,0))
              mx,my = pygame.mouse.get_pos()
              for poziom in poziomy:
                if poziom.rect.collidepoint(pygame.mouse.get_pos()):
                  poziom.hovered = True
                else:
                  poziom.hovered = False
                poziom.rysuj(screen,cz)
              for event in pygame.event.get():
                if event.type == pygame.QUIT:
                  pygame.quit()
                  quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                  if poziomy[0].rect.collidepoint(pygame.mouse.get_pos()):
                    Kwadrat.set_KIERUNEK(2)
                    ok = True
                  if poziomy[1].rect.collidepoint(pygame.mouse.get_pos()):
                    Kwadrat.set_KIERUNEK(4)
                    ok = True
                  if poziomy[2].rect.collidepoint(pygame.mouse.get_pos()):
                    Kwadrat.set_KIERUNEK(5)
                    ok = True
              cursor = pygame.Rect(mx,my,24,36)
              screen.blit(kursor,(mx,my))
              pygame.display.update()
          if opcje[2].rect.collidepoint(pygame.mouse.get_pos()):
                pygame.quit()
                quit()
    cursor = pygame.Rect(mx,my,24,36)
    screen.blit(kursor,(mx,my))
    pygame.display.update()

def gameplay(cz,cz_big,grafika,kursor,opcje):
  cialo = Pyton(200, 200)
  food = Orb()
  while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_UP:
            cialo.zmien_kierunek('u')
          if event.key == pygame.K_DOWN:
            cialo.zmien_kierunek('d')
          if event.key == pygame.K_RIGHT:
            cialo.zmien_kierunek('r')
          if event.key == pygame.K_LEFT:
            cialo.zmien_kierunek('l')
    screen.fill((0,0,0))
    food.rysuj()
    cialo.ruch()
    cialo.rysuj()
    if cialo.kolizja(food.ksztalt):
        food.x = random.randint(100,500)
        food.y = random.randint(100,500)
        cialo.dodaj_kwadrat()
    if cialo.gryz():
      powrot = menuOB.Menu('Return to main menu',100,420,screen,cz)
      gameover(cz,cz_big,powrot,opcje,grafika,kursor)
    cialo.wyjscie()
    pygame.display.update()
    clock.tick(60)

def gameover(cz,cz_big,powrot,opcje,grafika,kursor):
  while True:
    screen.fill((0,0,0))
    mx,my = pygame.mouse.get_pos()
    game_over = cz_big.render('Game Over',True,(255,255,255))
    screen.blit(game_over,(130,180))
    punkty = cz.render(str(Kwadrat.PUNKTY),True,(255,255,255))
    screen.blit(punkty,(280,312))
    if powrot.rect.collidepoint(pygame.mouse.get_pos()):
      powrot.hovered = True
    else:
      powrot.hovered = False
    powrot.rysuj(screen,cz)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if powrot.rect.collidepoint(pygame.mouse.get_pos()):
          main_menu(cz,cz_big,opcje,grafika,kursor)
    cursor = pygame.Rect(mx,my,24,36)
    screen.blit(kursor,(mx,my))
    pygame.display.update()

def main():
  cz = pygame.font.Font('Fipps-Regular.otf',24)
  cz_big = pygame.font.Font('Fipps-Regular.otf',40)
  opcje = [menuOB.Menu('New game',200,330,screen,cz),menuOB.Menu('Level',244,410,screen,cz),menuOB.Menu('Exit',258,490,screen,cz)]
  grafika = pygame.image.load('logo.png')
  kursor = pygame.image.load('cursor24px.png')
  pygame.mouse.set_visible(False)
  main_menu(cz,cz_big,opcje,grafika,kursor)


if __name__ == "__main__":
  main()
