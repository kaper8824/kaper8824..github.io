#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# захват лкм и отпуск по отпуску лкм с ограничением занятой клетки и границ поля.
import sys
import os
import pygame

pygame.init()
n=5# количество клеток квадратного поля игры
width  = 120#ширина клетки( и объекта)
height = 120#высота клетки ( и объекта)

margin = 1# промежуток между клетками


window = pygame.display.set_mode(((width +margin)*n+margin,(height+margin)*n+margin))# создаём окно
pygame.display.set_caption('Masha and Misha') # титул строка
screen = pygame.Surface(((width +margin)*n+margin,(height+margin)*n+margin)) # создаем игровое поле(экран)



koo = []# список нач. координат до перемещения
all_s = []# список всех объектов

koor = []# список координат разницы между обьуктом и мышкой
grid = []# список занятых и свободных клеток
for row in range(n):
    # заполняем пустую матрицу
    
    grid.append([])
    for column in range(n):
        grid[row].append(0) 
class Sprite:
    # (нач.коорд-х,у,имя файла,нач.скорость-х,у)
    def __init__(self,xpos,ypos,filename):
        self.x = xpos
        self.y = ypos
        self.image=pygame.image.load(filename) # создаем рисунок-загрузка из файла
        self.rect = self.image.get_rect() # представляем его прямоугольником
        all_s.append(self)
        self.w = self.image.get_width()   #ширина
        self.h = self.image.get_height()  #высота
        #self.row = None
        #self.column = None
        self.action = False
        self.column = self.x // (width + margin)
        self.row = self.y // (height + margin)            
        grid[self.row][self.column] = 1
    def bum (self):# проверка попадания мышки на объект
        if self.x<mp[0]<self.x+self.w and self.y<mp[1]<self.y+self.h:
            a = mp[0]-self.x# разница кооздинаты мышки и объекта
            b = mp[1]-self.y  
            koor.append(a)# запись в список координат
            koor.append(b)
            self.action = True# разрешение на перемещение
            c = self.x# первоначальные кооздинаты объекта 
            d = self.y
            koo.append(c)# запись первоначального положения выбранного объекта
            koo.append(d)
           
    def funtion (self):# функция движения точно в клетку
        mp = pygame.mouse.get_pos()# получ коорд мышки        
        self.x = (mp[0]// (width + margin))*(width + margin)+margin# коорд. клетки где находится мышь
        self.y = (mp[1] // (height + margin))*(height + margin)+margin
        self.column = self.x // (width + margin)# координ. в списке грид
        self.row = self.y // (height + margin)
        grid[ koo[1] // (height + margin)][ koo[0]// (width + margin)] =0# старой клетке = 0
        if  grid[self.row][self.column] ==1 : # если клетка куда переместили занята
            self.x = koo[0]# откат на обратные координаты
            self.y = koo[1]
        
        
    def render (self):# отображение обьекта на игровом поле(экране)
        screen.blit(self.image,(self.x,self.y))
       
    def mouv(self):# движение объекта с мышкой    
        
       
        #pygame.mouse.set_visible(False) # скрытие курсора   
        # Получить текущее положение мыши. Это возвращает позицию
        # в виде списка двух чисел.
        pos = pygame.mouse.get_pos()
        
        # Теперь  игрок имеет координаты мышки с учетом разницы координат           
        self.x = pos[0]-koor[0]
        self.y = pos[1]-koor[1]
        # условие границ поля
        
        if self.x<-10 :
            self.x = koo[0]
            self.y = koo[1]
            self.action = False
        if self.x+width>((margin+width)*n+10+margin):
            self.x = koo[0]
            self.y = koo[1]
            self.action = False
        if self.y<-10:
            self.x = koo[0]
            self.y = koo[1]
            self.action = False
        if self.y+height>((margin+height)*n+10+margin) :
            self.x = koo[0]
            self.y = koo[1]
            self.action = False
           
    def mesto(self):# запись положения объектов в список грид             
        self.column = self.x // (width + margin)
        self.row = self.y // (height + margin)            
        grid[self.row][self.column] = 1
    
        
hero1 = Sprite(margin,margin,('cheb1.gif'))
hero2 = Sprite(margin+(width +margin)*(n-1),margin,('cheb4.gif'))
hero3 = Sprite(margin,margin+(margin+height)*(n-1),('cheb3.gif'))
hero4 = Sprite((width +margin)*(n-1)+margin,margin+(height +margin)*(n-1),('cheb2.gif'))
                                
dum = True
while dum:# условие существования игрового цикла      
    
    screen.fill((0,0,90))
    for e in pygame.event.get():# для любого события
        
        if e.type == pygame.QUIT:# если было закрытие окна
            sys.exit()
    
    # захват объекта лкм и перемещение при удержании кнопки    
    if e.type == pygame.MOUSEBUTTONDOWN and e.button ==1:                                        
        
            mp = pygame.mouse.get_pos()
            for i in all_s :# захват объекта
                i.bum() 
    
    if e.type == pygame.MOUSEBUTTONUP and e.button ==1:# если отпущена лкм         
            
           
            for i in all_s:
                if i.action ==True:
                    i.funtion()# перемещение объекта точно в клетку
            for i in all_s :
                i.action = False# движение запрещено
            
            for i in all_s:# запись положения объекта в список grid
                i.mesto() # запись положения объектов в список грид
            koor = []# список координат разницы между обьуктом и мышкой
            koo = []# обнуление списка захвачен. объекта
    for i in all_s:
        if i.action == True:
            i.mouv()# перемещение объекта мышкой    
   
   
             
    
    for i in all_s:# отображаем все объекты
        i.render()        
         
    
    window.blit(screen,(0,0))# на окне прорисовываем поле игры
   
    pygame.display.flip()# отображаем полностью дисплей(окно)
    