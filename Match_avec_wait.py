# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import rsk
import random
import time
from rsk import constants
field_length = constants.field_length
field_width = constants.field_width
goal_width = constants.goal_width
defense_area_length = constants.defense_area_length
defense_area_width = constants.defense_area_width
pi = np.pi
continuer=True
x_positiv=False
c_bleu =rsk.Client("127.0.0.1","bleu")
c_vert =rsk.Client("127.0.0.1","vert")



def place_et_tir(c,robot,x_positiv):
    y_vise = -c.ball[1]+(random.random()-0.5)*goal_width
    if not(x_positiv):
        angle = float(np.arctan(y_vise/((field_length/2)-c.ball[0])))
        if (angle<-pi/3):
            robot.goto(((c.ball[0]-0.3),(c.ball[1]+0.3),angle),)
        elif (angle>pi/3):
            robot.goto(((c.ball[0]-0.3),(c.ball[1]-0.3),angle),)
        else :
            robot.goto(((c.ball[0]-0.3),(c.ball[1]),angle),)    
        robot.goto(((c.ball[0]-0.08*np.cos(angle)),(c.ball[1]-0.08*np.sin(angle)),angle),)
    else:
        angle = float(np.arctan(y_vise/((field_length/2)+c.ball[0])))
        if (angle<-pi/3):
            robot.goto(((c.ball[0]+0.3),(c.ball[1]+0.3),pi-angle),)
        elif (angle>pi/3):
            robot.goto(((c.ball[0]+0.3),(c.ball[1]-0.3),pi-angle),)
        else :
            robot.goto(((c.ball[0]+0.3),(c.ball[1]),pi-angle),)
   
        robot.goto(((c.ball[0]+0.08*np.cos(angle)),(c.ball[1]-0.08*np.sin(angle)),pi-angle),)
    robot.kick()
                           
def defense(c,attaquant,defenseur,ennemi1,ennemi2,x_positiv):
    if not(x_positiv):
        if (c.ball[0]>(field_length/2-defense_area_length)):
            x,y = c.ball[0],c.ball[1]
            x_visé,y_visé = 0,y+(x*np.tan(pi-ennemi2.orientation))
            angle = -np.arctan((y_visé+(random.random()-0.5)*goal_width)/(field_length/2))
            attaquant.goto((x_visé,y_visé,angle),)
        else:     
            x,y = ennemi1.position[0],ennemi1.position[1]
            x_visé,y_visé = -field_length/2+defense_area_length/2,y+(x*np.tan(pi-ennemi1.orientation))
            angle = -np.arctan((y_visé+(random.random()-0.5)*goal_width)/(field_length-x))
            defenseur.goto((x_visé,y_visé,angle),)
    else:
         if (c.ball[0]<(-field_length/2+defense_area_length)):
             x,y = -ennemi2.position[0],ennemi2.position[1]
             x_visé,y_visé = 0,y+(x*np.tan(ennemi2.orientation))
             angle = -np.arctan((y_visé+(random.random()-0.5)*goal_width)/(-field_length/2))
             attaquant.goto((x_visé,y_visé,pi-angle),)
         else:     
             x,y = ennemi1.position[0],ennemi1.position[1]
             x_visé,y_visé = field_length/2-defense_area_length/2,y+(x*np.tan(pi-ennemi1.orientation))
             angle = -np.arctan((y_visé+(random.random()-0.5)*goal_width)/(-field_length+x))
             defenseur.goto((x_visé,y_visé,pi-angle),)   
def jouer(c,attaquant,defenseur,ennemi1,ennemi2,x_positiv):
    if not(x_positiv):
        try:
            #c.goto_configuration("side")
            #c.goto_configuration('side')
            #c.goto_configuration('game')
            # change_attaquant(c,False, attaquant, defenseur)
            defense(c,attaquant,defenseur,ennemi1,ennemi2,x_positiv)  
            if (c.ball[0]<(-field_length/2+defense_area_length)):
                place_et_tir(c,defenseur,x_positiv)
            elif (c.ball[0]>(field_length/2-defense_area_length)):
                None
            else :
                place_et_tir(c,attaquant,x_positiv)
  
            
        except rsk.client.ClientError:
            None
    else:
        try:
            #c.goto_configuration("side")
            #c.goto_configuration('side')
            #c.goto_configuration('game')
            # change_attaquant(c,False, attaquant, defenseur)
            defense(c,attaquant,defenseur,ennemi1,ennemi2,x_positiv)
            if (c.ball[0]<(-field_length/2+defense_area_length)):
                None
            elif (c.ball[0]>(field_length/2-defense_area_length)):
                place_et_tir(c,defenseur,x_positiv)
            else :
                place_et_tir(c,attaquant,x_positiv)
    
            
        except rsk.client.ClientError:
            None
        
def jouer_bleu(c):
    
    attaquant = c.blue1
    defenseur= c.blue2
    ennemi1 = c.green1
    ennemi2 = c.green2
    x_positiv = False
    while True:
        c.on_update = jouer(c,attaquant,defenseur,ennemi1,ennemi2,x_positiv)
    
def jouer_vert(c):
    attaquant = c.green1
    defenseur= c.green2
    ennemi1 = c.blue1
    ennemi2 = c.blue2
    x_positiv = True
    while True:
        c.on_update = jouer(c,attaquant,defenseur,ennemi1,ennemi2,x_positiv)
"""       
#while continuer:
#   jouer_bleu(c_bleu)
#   jouer_vert(c_vert)
alpha = 14*pi/5
c_bleu.blue1.goto((0.3*np.cos(alpha),0.3*np.sin(alpha),alpha+5*pi/6))
c_bleu.blue1.control(0.2,-0.6,0.7*pi)
time.sleep(1)
print("stop")
c_bleu.stop_motion()
        time.sleep(1)
c_bleu.blue1.control(-0.2,0.6,-0.7*pi)
"""