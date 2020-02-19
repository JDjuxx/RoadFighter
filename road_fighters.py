import pygame
from pygame.locals import *
import random
import time

pygame.init()

pygame.display.set_caption("Road Fighters")

font = pygame.font.SysFont("comicsansms", 72)
font1 = pygame.font.SysFont("console", 12)
font2 = pygame.font.SysFont("bodoni", 36)

text = font.render("Empty", True, (255, 0, 0))
text_win=font.render("You Won!", True, (255, 255, 255))
intro_text=font2.render("Press any key to start..", True, (0,0,0))

start_show=[font.render("3", True, (255, 0, 0)),font.render("2", True, (255, 0, 0)),font.render("1", True, (255, 0, 0)),font.render("GO", True, (255, 0, 0))]


width=514
length=429
screen = pygame.display.set_mode((width,length), 0 ,32)

start_background=pygame.image.load("jugar_roadfighter.png")
start_background_ranking=pygame.image.load("ranking_roadfighter.png")
background = [pygame.image.load("car_game.jpg"),pygame.image.load("car_game2.png"),pygame.image.load("car_game3.png"),pygame.image.load("car_game4.png"),pygame.image.load("car_game5.jpg")]
level=0
limits=[(165,328),(140,280),(145,280),(160,264),(163,250)]

flag = pygame.image.load("left_flag.png")
car_yellow=[pygame.image.load("car_yellow.png"),pygame.image.load("car2.jpg"),pygame.image.load("car3.png"),pygame.image.load("hole.png"),pygame.image.load("car5.png"),pygame.image.load("car6.png")]
lights=[pygame.image.load("red_light.png"),pygame.image.load("green_light.png")]
careful=pygame.image.load("careful.jpg")

car= pygame.image.load("car1.png").convert()
rotated_left_car = pygame.transform.rotate(car, 30)
rotated_right_car = pygame.transform.rotate(car, -30)

car_icon=pygame.image.load("car_icon.png").convert()
fuel=pygame.image.load("fuel.png")
low_fuel=pygame.image.load("low_fuel.png")
pause_img=pygame.image.load("pause_img.png")

gas_station=[pygame.image.load("mobil.jpg"),pygame.image.load("petro.png"),pygame.image.load("ps.jpg")]
gas=1000

usuarioId = ''

class enemy():
    y_position=-150

def includeUsuario():
    usuarioId = input('Ingresa el nombre de usuario: ')
    intro()

def intro():
    option=0
    paused = True
    screen.blit(start_background,(0,0))
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_DOWN:
                    screen.blit(start_background_ranking,(0,0)) 
                    option = 1
                if event.key == pygame.K_UP:
                    screen.blit(start_background,(0,0))
                    option = 0
                if event.key == pygame.K_RETURN:
                    if option == 0:
                        start(level,gas)
                        
        pygame.display.flip()
        pygame.display.update()

##
def high_score(level,distance):
    f= open('highest_score.txt','r')
    highest_level= int(f.readline())
    highest_distance=int(f.readline())
    f.close()

    if level>highest_level or (level==highest_level and distance>highest_distance):
        f= open('highest_score.txt','w')
        f.write(str(level) +'\n'+ str(distance))
        f.close()
        



def pause():
    paused = True
    while paused:
        screen.blit(pause_img,(130,70))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    intro()
                else:    
                    paused = False
            

        pygame.display.update()


def start_light(car_x,y_image,level):
    for i in range(4):    
        screen.blit(background[level], (0,y_image))
        screen.blit(car, (car_x,length-80))
        if i==3:
            screen.blit(start_show[i],(int((limits[level][0] + limits[level][1])/2)-36,100))
            screen.blit(lights[1],(415,50))
        else:
            screen.blit(start_show[i],(int((limits[level][0] + limits[level][1])/2)-6,100))
            screen.blit(lights[0],(415,50))
        message_to_screen("START",level,320)#############
        pygame.display.update()
        time.sleep(1)


def message_to_screen(msg,level,y):
    screen_text = font2.render(msg,True, (0,0,0))
    textRect = screen_text.get_rect()
    textRect.center = (limits[level][0] + int((limits[level][1] -limits[level][0])/2)+14, y+13)
    pygame.draw.rect(screen, (255,255,255), (limits[level][0]+5, y-5, limits[level][1] - limits[level][0]+20, 35))
    screen.blit(screen_text, textRect)


def start(level,gas):
    enemies=[]
    oils=[]
    bullet=[-50,-50]
    explosion=[1000,1000,10000]
    bullets=0

    y_image=0
    car_x=(limits[level][0]+limits[level][1])/2
    car_x_move=0

    score=0
    gas=5000
    e=True
    gameOver=False
    round_win=False

    y_start=320
    start_light(car_x,y_image,level)
    
    while e:
        if gameOver:
            ##high_score()
            
            time.sleep(2)
            level=0
            start(level,2000)
        
        if gameOver==False and round_win==False:
            y_image+=1
            gas-=1
        
        if y_image==431:
            y_image=0

        
        screen.blit(background[level], (0,y_image))
        screen.blit(background[level], (0,y_image-431))
        screen.blit(flag, (0,0))
        screen.blit(fuel, (width-125,360))
        if y_start<length:
            message_to_screen("START",level,y_start)
            y_start+=1
        

        if score>340-(length-80)/10:
            message_to_screen("FINISH",level,y_start-450)
            y_start+=1


        

        pygame.draw.rect(screen, (255,255,255), (400, 400, gas/40, 10))

        if gas<5:
            gameOver=True
        elif gas<650:
            screen.blit(low_fuel, (width-95,360))


        if  int(score*10)%100==0: #%200==0:
            danger=enemy()
            danger.x_position=random.randrange(limits[level][0],limits[level][1]) ### 165-328
            danger.rand=random.randrange(0,6)
##            if danger.rand==3:### hole vs gas_bonus not to be in the same position
##                for o in oils:
##                    while abs(o.x_position-danger.x_position)<40:
##                        danger.x_position=random.randrange(limits[level][0],limits[level][1])
            enemies.append(danger)

        if  int(score*10) %500==0:
            oil=enemy()
            oil.x_position=random.randrange(limits[level][0],limits[level][1]-39)
            oil.y_position=-30
            oil.rand=random.randrange(0,3)
            oils.append(oil)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    car_x_move=-1
                if event.key == K_RIGHT:
                    car_x_move=1
                if event.key == K_UP and bullets>0:
                    if bullet[1]<0: 
                        bullet=[car_x+9,length-82]
                        bullets-=1
                if event.key == K_p:
                    pause()
                
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    car_x_move=0
                if event.key == K_RIGHT:
                    car_x_move=0



                    
        pygame.draw.line(screen, (0,0,0), (bullet[0],bullet[1]), (bullet[0],bullet[1]+10),6)
        bullet[1]-=5
        if bullet[1]>0:
            for k in range (len(enemies)):
                if enemies[k].x_position-4<bullet[0]<enemies[k].x_position+30 and enemies[k].y_position-40<bullet[1]<enemies[k].y_position+24 and enemies[k].rand!=3:
                    del enemies[k]
                    explosion=[bullet[0],bullet[1],gas]
                    bullet[1]=-50
                    break
        if abs(explosion[2]-gas)<30:
            explosion[1]+=1
            for i in range(10):
                pygame.draw.circle(screen, (255,0,0), (random.randint(explosion[0]-abs(explosion[2]-gas)/2, explosion[0]+abs(explosion[2]-gas)/2),random.randint(explosion[1]-abs(explosion[2]-gas)/2, explosion[1]+abs(explosion[2]-gas)/2)), random.randint(1,5))#, width=0)
        else:
            explosion[2]=10000
                
                    
        
                
        if gameOver==False and round_win==False:
            screen.blit(car, (car_x,length-80))
            car_x+=car_x_move
            score+=0.1


            for l in oils:
                screen.blit(gas_station[l.rand], (l.x_position,l.y_position))
                l.y_position+=1
                if l.x_position-20<car_x and car_x<l.x_position+38  and  length-80>l.y_position-28  and  length-80<l.y_position+39:
                    oils=[]
                    gas+=550

            pos=0
            for k in enemies:
                screen.blit(car_yellow[k.rand], (k.x_position,k.y_position))
                if k.rand==3: ###it is the hole
                    k.y_position+=1
                elif k.rand==4: ###it is the slow truck
                    screen.blit(careful, (420,280))
                    k.y_position+=3.5
                    if k.x_position<car_x and k.y_position<250:                            
                        k.x_position+=.1
                    elif k.x_position>car_x and k.y_position<250:
                        k.x_position-=.1
                elif k.rand==5: ### it is the fast truck
                    screen.blit(careful, (420,280))
                    k.y_position+=4.5
                    if k.x_position<car_x:                            
                        k.x_position+=.2
                    else:
                        k.x_position-=.2
                else: ##anything else
                    for l in enemies:
                        if l!=k and abs(k.y_position-l.y_position)<70:
                            if 0<=(k.x_position-l.x_position)<50:
                                k.x_position+=1
                            elif 0<=(l.x_position-k.x_position)<50:
                                k.x_position-=1
                        if k.x_position<limits[level][0]:
                            k.x_position+=1
                        elif k.x_position>limits[level][1]-30:
                            k.x_position-=1

                    if k.rand==2: ### the red enemy car
                        k.y_position+=.2
                              
                    else:
                        k.y_position+=.7
                    if k.rand==1 and 40<k.y_position<100:
                        if k.x_position<car_x:                            
                            k.x_position+=.5
                        elif k.x_position>car_x:
                            k.x_position-=.5
                                
                if k.x_position-26<car_x and car_x<k.x_position+22  and  length-80>k.y_position-29  and  length-80<k.y_position+33:
                    gameOver=True
                    screen.blit(rotated_right_car, (car_x,length-80))
                
                if k.y_position>length:
                    del enemies[pos]
                pos+=1

        else:
            if round_win==True:
                
                time.sleep(2)
                if level<4:
                    level+=1
                    start(level,2000)
                else:
                    screen.blit(text_win,(limits[level][0]-80,length/3))###########################################################
                    pygame.display.update()
                    time.sleep(1)
                    round_win=False
                    level=-1

        if car_x< limits[level][0]:
            gameOver=True
            screen.blit(rotated_left_car, (car_x,length-80))
        elif car_x> limits[level][1]:
            gameOver=True
            screen.blit(rotated_right_car, (car_x,length-80))
        else:
            if gameOver==True:
                if car_x_move>0:
                    screen.blit(rotated_right_car, (car_x,length-80))
                elif car_x_move<0:
                    screen.blit(rotated_left_car, (car_x,length-80))
                
        if score>340:
            round_win=True

        text_score = font1.render("Puntuación: "+ str(round(score*100/100,1)), True, (255, 255, 255))
        text_score1 = font1.render("Gasolina: "+ str(int(gas/100)) +" Liters", True, (255, 255, 255))
        text_score2 = font1.render("Nivel: "+ str(level+1), True, (255, 255, 255))
        ##text_score3 = font1.render("Bullets: "+ str(bullets), True, (255, 255, 255))
        percentage = font1.render(str(int(round((score/340)*100,0))) +"%", True, (255, 255, 255))
        
        screen.blit(text_score2,(width-129,3))
        screen.blit(text_score,(width-130,26))
        screen.blit(text_score1,(width-130,49))

        if int(round((score/340)*100>10)):
            screen.blit(percentage,(16,length-50-score+25))
        
        screen.blit(car_icon, (21,length-50-score))


        pygame.display.update()

includeUsuario()
