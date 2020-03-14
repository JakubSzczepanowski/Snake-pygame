import pygame
pygame.init()

class Menu:
    hovered = False

    def __init__(self,text,x,y,screen,cz):
        self.text = text
        self.x = x
        self.y = y
        self.set_rect(cz)
        self.rysuj(screen,cz)

    def set_rect(self,cz):
        self.set_rend(cz)
        self.rect = self.rend.get_rect(x=self.x,y=self.y)

    def set_rend(self,cz):
        self.rend = cz.render(self.text,True,(255,255,255))
        if self.hovered:
            self.rend = pygame.transform.rotozoom(self.rend,5,1.2)

    def rysuj(self,screen,cz):
        self.set_rend(cz)
        screen.blit(self.rend,(self.x,self.y))
