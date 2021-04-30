
import matplotlib.pyplot as plt

import math
from random import random


xPosPool = []
yPosPool = []
travelDistPool = []
posIndex = -1

conste = 19.14

def distCalc(x1, y1, x2, y2):
    return math.sqrt(pow(abs(float(x1) - float(x2)), 2) + pow(abs(float(y1) - float(y2)), 2))


def cal_angle(left, sec, third, last):
    angle = []

    angle.append(math.atan2(sec[1] - left[1], sec[0] - left[0]))
    angle.append(math.atan2(last[1] - left[1], last[0] - left[0])) # point1  
    angle.append(math.atan2(third[1] - sec[1], third[0] - sec[0]))
    angle.append(math.atan2(left[1] - sec[1], left[0] - sec[0])) # point2  
    angle.append(math.atan2(last[1] - third[1], last[0] - third[0])) 
    angle.append(math.atan2(sec[1] - third[1], sec[0] - third[0])) # point3
    angle.append(math.atan2(left[1] - last[1], left[0] - last[0]))
    angle.append(math.atan2(third[1] - last[1], third[0] - last[0])) # point4

    return angle

def gen_shell(a, b, c, d, circle, width, gcode, angle):  #generate the shell
    #calculate the four new points
    #draw circle
    #gcode += moveLnXY(a[0], a[1])
    #gcode += moveLnExtrudeXY(b[0], b[1], distCalc(b[0], b[1], a[0], a[1])/conste, f)
    #gcode += moveLnExtrudeXY(c[0], c[1], distCalc(c[0], c[1], b[0], b[1])/conste, f)
    #gcode += moveLnExtrudeXY(d[0], d[1], distCalc(d[0], d[1], c[0], c[1])/conste, f)
    #gcode += moveLnExtrudeXY(a[0], a[1], distCalc(a[0], a[1], d[0], d[1])/conste, f)
    plt.plot([a[0], b[0], c[0], d[0], a[0]], [a[1], b[1], c[1], d[1], a[1]])
    #nangle = [0, 0, 0, 0]
    #na = (a[0] + width*math.cos(angle[0]) + width*math.cos(angle[1]), a[1] + width*math.sin(angle[0]) + width*math.sin(angle[1])) 
    #nb = (b[0] + width*math.cos(angle[2]) + width*math.cos(angle[3]), b[1] + width*math.sin(angle[2]) + width*math.sin(angle[3]))
    #nc = (c[0] + width*math.cos(angle[4]) + width*math.cos(angle[5]), c[1] + width*math.sin(angle[4]) + width*math.sin(angle[5]))
    #nd = (d[0] + width*math.cos(angle[6]) + width*math.cos(angle[7]), d[1] + width*math.sin(angle[6]) + width*math.sin(angle[7]))

            
    na = (a[0] + width/math.sin((angle[0] - angle[1])/2)*math.cos((angle[0] + angle[1])/2), a[1] + width/math.sin((angle[0] - angle[1])/2)*math.sin((angle[0] + angle[1])/2)) 
    nb = (b[0] + width/math.sin((angle[2] - angle[3])/2)*math.cos((angle[2] + angle[3])/2), b[1] + width/math.sin((angle[2] - angle[3])/2)*math.sin((angle[2] + angle[3])/2))
    nc = (c[0] + width/math.sin((angle[4] - angle[5])/2)*math.cos((angle[4] + angle[5])/2), c[1] + width/math.sin((angle[4] - angle[5])/2)*math.sin((angle[4] + angle[5])/2))
    nd = (d[0] + width/math.sin((angle[6] - angle[7])/2)*math.cos((angle[6] + angle[7])/2), d[1] + width/math.sin((angle[6] - angle[7])/2)*math.sin((angle[6] + angle[7])/2))
    if circle == 1:
        return gcode, na, nb, nc, nd
    else:
        return gen_shell(na, nb, nc, nd, circle-1, width, gcode, angle)

def sort_point(a, b, c, d): #sort four point as A B C D
    pointx = []
    pointy = []
    angle = []
    pointx.extend((a[0], b[0], c[0], d[0]))
    pointy.extend((a[1],b[1],c[1],d[1]))
    left_index = pointx.index(min(pointx))
    left = (pointx[left_index], pointy[left_index])
    for i in range(4):
        if pointx[i] <= left[0] and pointy[i] < left[1]:
            left_index = i
            left = (pointx[i], pointy[i])
    
    for i in range(4):
        angle.append(math.atan2(pointy[i] - left[1], pointx[i] - left[0]))
    
    #print(angle)
    angle.remove(0)
    b_index = angle.index(max(angle))
    #print(b_index)
    if left_index == 0:
        b_index += 1
    elif left_index == 1 and b_index >= 1:
        b_index += 1
    elif left_index == 2 and b_index == 2:
        b_index += 1 
    
    sec = (pointx[b_index], pointy[b_index])
    
    d_index = angle.index(min(angle))
    #print(d_index)
    if left_index == 0:
        d_index += 1
    elif left_index == 1 and d_index >= 1:
        d_index += 1
    elif left_index == 2 and d_index == 2:
        d_index += 1
    
    last = (pointx[d_index], pointy[d_index])
    
    l = [0, 1, 2, 3]
    l.remove(left_index)
    l.remove(b_index)
    l.remove(d_index)
    
    c_index = l[0]
    third = (pointx[c_index], pointy[c_index])
    

    return left, sec, third, last

def repair_next(nextx, nexty, point, angle, degree):
    #dist = distCalc(nextx, nexty, point[0], point[1])
    #print(angle)
    cur_angle = math.atan2(nexty - point[1], nextx - point[0])
    #print(cur_angle)
    if cur_angle - angle > math.pi/180:
        while cur_angle - angle >= math.pi/180:
            nextx += 0.1*math.cos(math.pi/2 - degree)
            nexty += 0.1*math.sin(math.pi/2 - degree)
            cur_angle = math.atan2(nexty - point[1], nextx - point[0])
            #print(cur_angle)
    elif cur_angle - angle < -math.pi/180:
        while cur_angle - angle <= -math.pi/180:
            nextx -= 0.1*math.cos(math.pi/2 - degree)
            nexty -= 0.1*math.sin(math.pi/2 - degree)
            cur_angle = math.atan2(nexty - point[1], nextx - point[0])
            #print(cur_angle)
    
    return nextx, nexty


def fill_quadrangle(a, b, c, d, delta_upx, delta_upy, delta_downx, delta_downy, angle, cnt):
    gcode = ""
    tri = 0

    nextx = a[0] + delta_upx
    nexty = a[1] + delta_upy
    #nextx, nexty = repair_next(nextx, nexty, a, angle[0], degree)
    #print(nextx, nexty)

    while True:
            if cnt%2 == 1 and abs(math.atan2(b[1] - nexty, b[0] - nextx) - angle[0]) <= math.pi/2:
                #gcode += moveLnXY(nextx, nexty)
                lastx = nextx
                lasty = nexty
                nextx = a[0] + cnt*delta_downx
                nexty = a[1] + cnt*delta_downy
                #nextx, nexty = repair_next(nextx, nexty, a, angle[1], degree)
                if abs(math.atan2(d[1] - nexty, d[0] - nextx) - angle[1]) <= math.pi/2:
                    #e = distCalc(nextx, nexty, lastx, lasty) / conste
                    #gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                    plt.plot([lastx, nextx], [lasty, nexty],"r")
                    #print(math.atan2(lasty - nexty, lastx - nextx))
                    #print(nextx, nexty)
                    nextx = a[0] + (cnt + 1)*delta_downx
                    nexty = a[1] + (cnt + 1)*delta_downy
                    #print(nextx, nexty)
                    
                    #nextx, nexty = repair_next(nextx, nexty, a, angle[1], degree)
                else:
                    delta = distCalc(d[0], d[1], nextx, nexty)
                    add = delta/math.sin(math.pi/2 - degree - angle[5])*math.sin( - math.pi/2 + degree + angle[4])
                    newx = d[0] + add*math.cos(angle[5])
                    newy = d[1] + add*math.sin(angle[5])
                    #e = distCalc(newx, newy, lastx, lasty) / conste
                    #gcode += moveLnExtrudeXY(newx, newy, e, f)
                    #newx, newy = repair_next(newx, newy, d, angle[5], degree)
                    plt.plot([lastx, newx], [lasty, newy],"r")
                    #print(newx, newy)
                    nb = (a[0] + cnt*delta_upx, a[1] + cnt*delta_upy)
                    na = (newx, newy)
                    nc = b
                    nd = c
                    break
            elif cnt%2 == 0 and abs(math.atan2(d[1] - nexty, d[0] - nextx) - angle[1]) <= math.pi/2:
                #gcode += moveLnXY(nextx, nexty)
                lastx = nextx
                lasty = nexty
                nextx = a[0] + cnt*delta_upx
                nexty = a[1] + cnt*delta_upy
                #print(nextx, nexty)
                #nextx, nexty = repair_next(nextx, nexty, a, angle[0], degree)
                if abs(math.atan2(b[1] - nexty, b[0] - nextx) - angle[0]) <= math.pi/2:
                    #e = distCalc(nextx, nexty, lastx, lasty) / conste
                    #gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                    plt.plot([lastx, nextx], [lasty, nexty],"b")
                    #print(math.atan2(nexty - lasty, nextx - lastx))
                    #print(nextx, nexty)
                    nextx = a[0] + (cnt + 1)*delta_upx
                    nexty = a[1] + (cnt + 1)*delta_upy
                    #nextx, nexty = repair_next(nextx, nexty, a, angle[0], degree)
                else:
                    delta = distCalc(b[0], b[1], nextx, nexty)
                    add = delta/math.sin(math.pi/2 + degree + angle[2])*math.sin(- math.pi/2 - degree - angle[3])
                    newx = b[0] + add*math.cos(angle[2])
                    newy = b[1] + add*math.sin(angle[2])
                    #e = distCalc(newx, newy, lastx, lasty) / conste
                    #gcode += moveLnExtrudeXY(newx, newy, e, f)        
                    #newx, newy = repair_next(newx, newy, b, angle[2], degree)
                    plt.plot([lastx, newx], [lasty, newy],"b")
                    #print(newx, newy)
                    na = (a[0]+cnt*delta_downx, a[1]+cnt*delta_downy)
                    nb = (newx, newy)
                    nc = c
                    nd = d
                    break
            else:
                if cnt%2 == 1:
                    delta = distCalc(b[0], b[1], nextx, nexty)
                    #print(delta)
                    add = delta/math.sin(math.pi/2 + degree + angle[2])*math.sin(- math.pi/2 - degree - angle[3])
                    #print(add)
                    newx = b[0] + add*math.cos(angle[2])
                    newy = b[1] + add*math.sin(angle[2])
                    #nextx, nexty = repair_next(nextx, nexty, b, angle[2], degree)
                    #print(newx, newy)
                    nb = (newx, newy)
                    #print(nb)
                    #gcode += moveLnXY(newx, newy)  
                    lastx = newx
                    lasty = newy
                    nextx = a[0] + cnt*delta_downx
                    nexty = a[1] + cnt*delta_downy
                    print(3)
                    print(add)
                    print(degree)
                    #nextx, nexty = repair_next(nextx, nexty, a, angle[1], degree)
                    if abs(math.atan2(d[1] - nexty, d[0] - nextx) - angle[1]) <= math.pi/2:
                        #e = distCalc(nextx, nexty, lastx, lasty) / conste
                        #gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                        plt.plot([lastx, nextx], [lasty, nexty],"r")
                        #print(math.atan2(lasty - nexty, lastx - nextx))
                        #print(nextx, nexty)
                        na = (nextx, nexty)
                        nc = c
                        nd = d
                    else:
                        #print(nextx, nexty)
                        delta = distCalc(d[0], d[1], nextx, nexty)
                        add = delta/math.sin(math.pi/2 - degree - angle[5])*math.sin( -math.pi/2 + degree + angle[4])
                        #print(d[0], d[1])
                        newx = d[0] + add*math.cos(angle[5])
                        newy = d[1] + add*math.sin(angle[5])
                        #e = distCalc(newx, newy, lastx, lasty) / conste
                        #gcode += moveLnExtrudeXY(newx, newy, e, f)
                        #newx, newy = repair_next(newx, newy, d, angle[5], degree)
                        #print(newx, newy)
                        #print(lastx, lasty)
                        #print(math.atan2(lasty - newy, lastx - newx))
                        plt.plot([lastx, newx], [lasty, newy],"r")
                        #print(nextx, nexty)
                        na = (newx, newy)
                        nc = c
                        nd = d
                        tri = 1
                else:
                    delta = distCalc(d[0], d[1], nextx, nexty)
                    #print(nextx, nexty)
                    #print(math.atan2(d[1] - nexty, d[0] - nextx))
                    add = delta/math.sin(math.pi/2 - degree - angle[5])*math.sin( - math.pi/2 + degree + angle[4])
                    newx = d[0] + add*math.cos(angle[5])
                    newy = d[1] + add*math.sin(angle[5])
                    #nextx, nexty = repair_next(nextx, nexty, d, angle[5], degree)
                    na = (newx, newy)
                    #print(newx, newy)
                    #gcode += moveLnXY(newx, newy)
                    lastx = newx
                    lasty = newy
                    #print(a)
                    #print(delta_upy)
                    #print(cnt)
                    nextx = a[0] + cnt*delta_upx
                    nexty = a[1] + cnt*delta_upy
                    #print(nextx, nexty)
                    #nextx, nexty = repair_next(nextx, nexty, a, angle[0], degree)
                    if abs(math.atan2(b[1] - nexty, b[0] - nextx) - angle[0]) <= math.pi/2:
                        #e = distCalc(nextx, nexty, lastx, lasty) / conste
                        #gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                        #print(math.atan2(nexty - lasty, nextx - lastx))
                        plt.plot([lastx, nextx], [lasty, nexty],"b")
                        #print(nextx, nexty)
                        nb = (nextx, nexty)
                        #print(nb)
                        nc = b
                        nd = c
                    else:
                        delta = distCalc(b[0], b[1], nextx, nexty)
                        add = delta/math.sin(math.pi/2 + degree + angle[2])*math.sin(- math.pi/2 - degree - angle[3])
                        newx = b[0] + add*math.cos(angle[2])
                        newy = b[1] + add*math.sin(angle[2])
                        #nextx, nexty = repair_next(nextx, nexty, b, angle[2], degree)
                        #e = distCalc(newx, newy, lastx, lasty) / conste
                        #gcode += moveLnExtrudeXY(newx, newy, e, f)
                        #print(math.atan2(lasty - newy, lastx - newx))
                        plt.plot([lastx, newx], [lasty, newy],"b")
                        #print(nextx, nexty)
                        nb = (newx, newy)
                        nc = c
                        nd = c
                        tri = 1
                break

            cnt += 1    
    
    cnt += 1

    return gcode, na, nb, nc, nd, cnt, tri

def fillparal_quadrangle(a, b, c, d, cnt, degree, width):
    gcode = ""

    angle = cal_angle(a, b, c, d)
    fin = 0
    layer = 1

    alpha = math.pi/2 - degree - angle[2]
    step1 = width/math.sin(alpha)
    delta_upx = step1*math.cos(angle[2])
    delta_upy = step1*math.sin(angle[2])
        #gcode += moveLnXY(a[0] + delta_upx, a[1] + delta_upy)       

    beta = math.pi/2 + degree + angle[1]
    step2 = width/math.sin(beta)
    delta_downx = step2*math.cos(angle[1])
    delta_downy = step2*math.sin(angle[1])


    if cnt%2 == 1:
        nextx = b[0] + delta_upx
        nexty = b[1] + delta_upy
        cnt = 1
    else:
        nextx = a[0] + delta_downx
        nexty = a[1] + delta_downy
        cnt = 2
    

    while True:
            if cnt%2 == 1 and abs(math.atan2(c[1] - nexty, c[0] - nextx) - angle[2]) <= math.pi/2:
                #gcode += moveLnXY(nextx, nexty)
                lastx = nextx
                lasty = nexty
                nextx = a[0] + layer*delta_downx
                nexty = a[1] + layer*delta_downy
                if abs(math.atan2(d[1] - nexty, d[0] - nextx) - angle[1]) <= math.pi/2:
                    #e = distCalc(nextx, nexty, lastx, lasty) / conste
                    #gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                    plt.plot([lastx, nextx], [lasty, nexty],"r")
                    nextx = a[0] + (layer+1)*delta_downx
                    nexty = a[1] + (layer+1)*delta_downy
                else:
                    delta = distCalc(d[0], d[1], nextx, nexty)
                    add = delta/math.sin(math.pi/2 - degree - angle[7])*math.sin( - math.pi/2 + degree + angle[6])
                    newx = d[0] + add*math.cos(angle[7])
                    newy = d[1] + add*math.sin(angle[7])
                    #e = distCalc(newx, newy, lastx, lasty) / conste
                    #gcode += moveLnExtrudeXY(newx, newy, e, f)
                    plt.plot([lastx, newx], [lasty, newy],"r")
                    nb = (b[0] + layer*delta_upx, b[1] + layer*delta_upy)
                    na = (newx, newy)
                    nc = c
                    break
            elif cnt%2 == 0 and abs(math.atan2(d[1] - nexty, d[0] - nextx) - angle[1]) <= math.pi/2:
                #gcode += moveLnXY(nextx, nexty)
                lastx = nextx
                lasty = nexty
                nextx = b[0] + layer*delta_upx
                nexty = b[1] + layer*delta_upy
                if abs(math.atan2(c[1] - nexty, c[0] - nextx) - angle[2]) <= math.pi/2:
                    #e = distCalc(nextx, nexty, lastx, lasty) / conste
                    #gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                    plt.plot([lastx, nextx], [lasty, nexty],"b")
                    nextx = b[0] + (layer+1)*delta_upx
                    nexty = b[1] + (layer+1)*delta_upy
                    #print(nextx, nexty)
                else:
                    delta = distCalc(c[0], c[1], nextx, nexty)
                    add = delta/math.sin(math.pi/2 + degree + angle[4])*math.sin(3*math.pi/2 - degree - angle[5])
                    newx = c[0] + add*math.cos(angle[4])
                    newy = c[1] + add*math.sin(angle[4])
                    #print(newx, newy)
                    #e = distCalc(newx, newy, lastx, lasty) / conste
                    #gcode += moveLnExtrudeXY(newx, newy, e, f)        
                    plt.plot([lastx, newx], [lasty, newy],"b")
                    #print(math.atan2(newy - lasty, newx - lastx))
                    na = (a[0]+layer*delta_downx, a[1]+layer*delta_downy)
                    nb = (newx, newy)
                    print(math.atan2(nb[1] - na[1], nb[0] - na[0]))
                    nc = d
                    break
            else:
                if cnt%2 == 1:
                    delta = distCalc(c[0], c[1], nextx, nexty)
                    add = delta/math.sin(math.pi/2 + degree + angle[4])*math.sin(3*math.pi/2 - degree - angle[5])
                    newx = c[0] + add*math.cos(angle[4])
                    newy = c[1] + add*math.sin(angle[4])
                    nb = (newx, newy)
                    #print(nb)
                    #gcode += moveLnXY(newx, newy) 
                    lastx = newx
                    lasty = newy
                    nextx = a[0] + layer*delta_downx
                    nexty = a[1] + layer*delta_downy
                    if abs(math.atan2(d[1] - nexty, d[0] - nextx) - angle[1]) <= math.pi/2:
                        #e = distCalc(newx, newy, lastx, lasty) / conste
                        #gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                        plt.plot([lastx, nextx], [lasty, nexty],"r")
                        #print(math.atan2(lasty - nexty, lastx - nextx))
                        na = (nextx, nexty)
                        nc = d
                    else:
                        na = (0, 0)
                        nc = (0, 0)
                        fin = 1
                        break
                else:
                    delta = distCalc(d[0], d[1], nextx, nexty)
                    add = delta/math.sin(math.pi/2 - degree - angle[5])*math.sin(math.pi/2 + degree - angle[6])
                    newx = d[0] + add*math.cos(angle[7])
                    newy = d[1] + add*math.sin(angle[7])
                    na = (newx, newy)
                    #print(na)
                    #gcode += moveLnXY(newx, newy)
                    lastx = newx
                    lasty = newy
                    #print(a)
                    #print(delta_upx)
                    #print(delta_upy)
                    nextx = b[0] + layer*delta_upx
                    nexty = b[1] + layer*delta_upy
                    #print(nextx, nexty)
                    if abs(math.atan2(c[1] - nexty, c[0] - nextx) - angle[2]) <= math.pi/2:
                        #e = distCalc(newx, newy, lastx, lasty) / conste
                        #gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                        plt.plot([lastx, nextx], [lasty, nexty],"b")
                        #print(math.atan2(lasty - nexty, lastx - nextx))
                        nb = (nextx, nexty)
                        nc = c
                    else:
                        nb = (0, 0)
                        nc = (0, 0)
                        fin = 1
                        break
                break

            cnt += 1    
            layer += 1
    
    cnt += 1

    return gcode, na, nb, nc, cnt, fin

def fill_triangle(a, b, c, cnt, degree, width):
    gcode = ""
    layer = 1
    angle = []
    angle.append(math.atan2(c[1] - a[1], c[0] - a[0]))
    angle.append(math.atan2(c[1] - b[1], c[0] - b[0]))

    step_up = width/math.sin(math.pi/2 + degree + angle[1])

    delta_upx = step_up*math.cos(angle[1])
    delta_upy = step_up*math.sin(angle[1])

    step_down = width/math.sin(math.pi/2 - degree - angle[0])
 
    delta_downx = step_down*math.cos(angle[0])
    delta_downy = step_down*math.sin(angle[0])
    
    #print(cnt)

    if cnt%2 == 1:
        nextx = b[0] + delta_upx
        nexty = b[1] + delta_upy
        cnt = 1
    else:
        nextx = a[0] + delta_downx
        nexty = a[1] + delta_downy
        cnt = 2
    
    #print(delta_upx)
    #print(delta_upy)
    #print(delta_downx)
    #print(delta_downy)
    #print(nextx, nexty)

    while True:
            if cnt%2 == 1 and abs(math.atan2(c[1] - nexty, c[0] - nextx) - angle[1]) <= math.pi/2:
                #gcode += moveLnXY(nextx, nexty)
                lastx = nextx
                lasty = nexty
                nextx = a[0] + layer*delta_downx
                nexty = a[1] + layer*delta_downy
                #print(nextx, nexty)
                if abs(math.atan2(c[1] - nexty, c[0] - nextx) - angle[0]) <= math.pi/2:
                    #e = distCalc(nextx, nexty, lastx, lasty) / conste
                    #gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                    plt.plot([lastx, nextx], [lasty, nexty],"r")
                    #print(math.atan2(lasty - nexty, lastx - nextx))
                    nextx = a[0] + (layer+1)*delta_downx
                    nexty = a[1] + (layer+1)*delta_downy
                else:
                    break
            elif cnt%2 == 0 and abs(math.atan2(c[1] - nexty, c[0] - nextx) - angle[0]) <= math.pi/2:
                #gcode += moveLnXY(nextx, nexty)
                lastx = nextx
                lasty = nexty
                nextx = b[0] + layer*delta_upx
                nexty = b[1] + layer*delta_upy
                if abs(math.atan2(c[1] - nexty, c[0] - nextx) - angle[1]) <= math.pi/2:
                    #e = distCalc(nextx, nexty, lastx, lasty) / conste
                    #gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                    plt.plot([lastx, nextx], [lasty, nexty],"b")
                    nextx = b[0] + (layer+1)*delta_upx
                    nexty = b[1] + (layer+1)*delta_upy
                else:     
                    break
            else:
                break

            cnt += 1    
            layer += 1

    return gcode


def merge_quadrangle(a, b, c, d, degree, width, shell_width, circle):
    gcode = ""
    #dis = []
    left, sec, third, last = sort_point(a, b, c, d) #if neccessary
    angle = cal_angle(left, sec, third, last)
    #dis.append(distCalc(a[0], b[0], a[1], b[1]))
    #dis.append(distCalc(b[0], c[0], b[1], c[1]))
    #dis.append(distCalc(c[0], d[0], c[1], d[1]))
    #dis.append(distCalc(d[0], a[0], d[1], a[1]))

    gcode, na, nb, nc, nd = gen_shell(left, sec, third, last, circle, shell_width, gcode, angle)

    #gcode += moveLnXY(na[0], na[1])

    if angle[0] > math.pi/2 - degree:
        alpha = math.pi/2 - degree - angle[2]
        delta_upx = width/math.sin(alpha)*math.cos(angle[2])
        delta_upy = width/math.sin(alpha)*math.sin(angle[2])
        #gcode += moveLnXY(a[0] + delta_upx, a[1] + delta_upy)       

        beta = math.pi/2 + degree + angle[3]
        delta_downx = width/math.sin(beta)*math.cos(angle[3])
        delta_downy = width/math.sin(beta)*math.sin(angle[3])
        newangle = [angle[2], angle[3], angle[4], angle[5], angle[0], angle[1]]

        cnt = 1
        gcode1, na, nb, nc, nd, cnt, tri = fill_quadrangle(nb, nc, nd, na, delta_upx, delta_upy, delta_downx, delta_downy, newangle, cnt)
        #print(na, nb, nc, nd)
        #print(tri)

        if tri == 1:
            gcode += gcode1
            gcode += fill_triangle(na, nb, nc, cnt, degree, width)
        else:
            gcode2, na, nb, nc, cnt, fin = fillparal_quadrangle(na, nb, nc, nd, cnt, degree, width)
            #print(na, nb, nc)
            if fin == 1:
                gcode += gcode1
                gcode += gcode2
            else:
                gcode += gcode1
                gcode += gcode2
                gcode += fill_triangle(na, nb, nc, cnt, degree, width)

    elif angle[0] == math.pi/2 - degree:
        cnt = 1
        gcode2, na, nb, nc, cnt, fin = fillparal_quadrangle(na, nb, nc, nd, cnt, degree, width)
        if fin == 1:
                gcode += gcode2
        else:
                gcode += gcode2
                gcode += fill_triangle(na, nb, nc, cnt, degree, width)
    else:
        #draw_line(nb, nc, na)
        alpha = math.pi/2 - degree - angle[0]
        delta_upx = width/math.sin(alpha)*math.cos(angle[0])
        delta_upy = width/math.sin(alpha)*math.sin(angle[0])
        #gcode += moveLnXY(a[0] + delta_upx, a[1] + delta_upy)       

        beta = math.pi/2 + degree + angle[1]
        delta_downx = width/math.sin(beta)*math.cos(angle[1])
        delta_downy = width/math.sin(beta)*math.sin(angle[1])

        newangle = [angle[0], angle[1], angle[2], angle[3], angle[6], angle[7]]

        cnt = 1
        #print(na, nb, nc, nd)
        gcode1, na, nb, nc, nd, cnt, tri = fill_quadrangle(na, nb, nc, nd, delta_upx, delta_upy, delta_downx, delta_downy, newangle, cnt)
        #print(na, nb, nc, nd)
        #print(math.atan2(nb[1] - na[1], nb[0] - na[0]))
        #print(tri)

        if tri == 1:
            gcode += gcode1
            gcode += fill_triangle(na, nb, nc, cnt, degree, width)
        else:
            gcode2, na, nb, nc, cnt, fin = fillparal_quadrangle(na, nb, nc, nd, cnt, degree, width)
            #print(na, nb, nc)
            if fin == 1:
                gcode += gcode1
                gcode += gcode2
            else:
                gcode += gcode1
                gcode += gcode2
                gcode += fill_triangle(na, nb, nc, cnt, degree, width)
        




def gcodeMerging():
    baseGcode = fileRead()
    mainGcode = merge_quadrangle(a, b, c, d, degree, width, shell_width, circle)
    
    gcode = baseGcode + mainGcode
    return gcode



def fileRead():
    baseGcodePath = '/Users/deyingpan/Documents/ZJU/2021 CHI LBW Archive/G-code/startingScript/starting_TPU_01.gcode'
    with open(baseGcodePath, "r") as f:
        gcode = f.read()
    return gcode



if __name__ == '__main__':
    a = (150, 180)
    b = (230, 230)
    c = (180, 230)
    d = (230, 180)
    e = (195, 180)
    f = (205, 200)
    g = (195, 200)
    h = (205, 180)
    degree = -math.pi/4
    width = 0.75
    shell_width = 0.3
    circle = 3

    # generate the final print Gcode
    f#inalGcode = gcodeMerging()
    
    merge_quadrangle(a, b, c, d, degree, width, shell_width, circle)
    #merge_quadrangle(e, f, g, h, degree, width, shell_width, circle)
    #plt.plot([188, 197], [190, 190])
    
     # save the Gcode file
    #savedFilePath = "C:\VScode\gcode\1.gcode"
    #with open(savedFilePath, "w") as f:
    #    f.write(finalGcode)
    #fileRead()