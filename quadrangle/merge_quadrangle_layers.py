import os

import math
from random import random
import random


xPosPool = []
yPosPool = []
travelDistPool = []
posIndex = -1

conste = 19.14   # to be changed
f = 1200

def distCalc(x1, y1, x2, y2):
    return math.sqrt(pow(abs(float(x1) - float(x2)), 2) + pow(abs(float(y1) - float(y2)), 2))

def moveLnXY(x, y):
    gcode = ""
    gcode += "G0"
    gcode += " X" + str(x)
    gcode += " Y" + str(y)
    gcode += "\n"

    #posIndex += 1
    xPosPool.append(x)
    yPosPool.append(y)

    #travel = distCalc(xPosPool[posIndex-1], yPosPool[posIndex-1], xPosPool[posIndex], yPosPool[posIndex])

    #travelDistPool.append(travel)

    #print("Linear XY Movement" + str(travel) + "mm: from pos#" + str(posIndex) + " (" + str(xPosPool[posIndex-1]) + ", " + str(yPosPool[posIndex-1]) + "), to pos#" + str(posIndex+1) + " (" + str(xPosPool[posIndex]) + ", " + str(yPosPool[posIndex]) + ")")

    return gcode

def moveLnZ(z):
    gcode = ""
    gcode += "G0"
    gcode += " Z" + str(z)
    gcode += "\n"
    
    return gcode

def moveLnExtrudeXY(x, y, e, f):
    posIndex = -1
    gcode = ""
    gcode += "G1"
    gcode += " X" + str(x)
    gcode += " Y" + str(y)
    gcode += " E" + str(e)
    gcode += " F" + str(f)
    gcode += "\n"

    #posIndex += 1
    xPosPool.append(x)
    yPosPool.append(y)

    #travel = math.sqrt(pow(abs(float(xPosPool[posIndex-1]) - float(xPosPool[posIndex])), 2) + pow(abs(float(yPosPool[posIndex-1]) - float(yPosPool[posIndex])), 2))
    #travelDistPool.append(travelDist)

    #print("Linear XY Extrusion Movement" + str(travel) + "mm: from pos#" + str(posIndex) + " (" + str(xPosPool[posIndex-1]) + ", " + str(yPosPool[posIndex-1]) +
    #"), to pos#" + str(posIndex+1) + " (" + str(xPosPool[posIndex]) + ", " + str(yPosPool[posIndex]) + ")")

    return gcode

def stationaryExtrude(e, f):
    gcode = ""
    gcode += "G1"
    gcode += " E" + str(e)
    gcode += " F" + str(f)
    gcode += "\n"
    return gcode

def waitSec(s):
    gcode = ""
    gcode += "G4"
    gcode += " S" + str(s)
    gcode += "\n"

def waitMSec(p):
    gcode = ""
    gcode += "G4"
    gcode += " P" + str(p)
    gcode += "\n"



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

def gen_shell(a, b, c, d, circle, width, gcode, angle, e):  #generate the shell
    #calculate the four new points
    #draw circle
    gcode += moveLnXY(a[0], a[1])
    e += distCalc(b[0], b[1], a[0], a[1])/conste
    gcode += moveLnExtrudeXY(b[0], b[1], e, f)
    e += distCalc(c[0], c[1], b[0], b[1])/conste
    gcode += moveLnExtrudeXY(c[0], c[1], e, f)
    e += distCalc(d[0], d[1], c[0], c[1])/conste
    gcode += moveLnExtrudeXY(d[0], d[1], e, f)
    e += distCalc(a[0], a[1], d[0], d[1])/conste
    gcode += moveLnExtrudeXY(a[0], a[1], e, f)
    na = (a[0] + width/math.sin((angle[0] - angle[1])/2)*math.cos((angle[0] + angle[1])/2), a[1] + width/math.sin((angle[0] - angle[1])/2)*math.sin((angle[0] + angle[1])/2)) 
    nb = (b[0] + width/math.sin((angle[2] - angle[3])/2)*math.cos((angle[2] + angle[3])/2), b[1] + width/math.sin((angle[2] - angle[3])/2)*math.sin((angle[2] + angle[3])/2))
    nc = (c[0] + width/math.sin((angle[4] - angle[5])/2)*math.cos((angle[4] + angle[5])/2), c[1] + width/math.sin((angle[4] - angle[5])/2)*math.sin((angle[4] + angle[5])/2))
    nd = (d[0] + width/math.sin((angle[6] - angle[7])/2)*math.cos((angle[6] + angle[7])/2), d[1] + width/math.sin((angle[6] - angle[7])/2)*math.sin((angle[6] + angle[7])/2))
    if circle == 1:
        return gcode, na, nb, nc, nd, e
    else:
        return gen_shell(na, nb, nc, nd, circle-1, width, gcode, angle, e)

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


def fill_quadrangle(a, b, c, d, degree, delta_upx, delta_upy, delta_downx, delta_downy, angle, cnt, e):
    gcode = ""
    tri = 0

    nextx = a[0] + delta_upx
    nexty = a[1] + delta_upy

    lastx = a[0]
    lasty = a[1]

    while True:
            if cnt%2 == 1 and abs(math.atan2(b[1] - nexty, b[0] - nextx) - angle[0]) <= math.pi/2:
                gcode += moveLnXY(nextx, nexty)
                lastx = nextx
                lasty = nexty
                nextx = a[0] + cnt*delta_downx
                nexty = a[1] + cnt*delta_downy
                if abs(math.atan2(d[1] - nexty, d[0] - nextx) - angle[1]) <= math.pi/2:
                    e += distCalc(nextx, nexty, lastx, lasty) / conste
                    gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                    nextx = a[0] + (cnt+1)*delta_downx
                    nexty = a[1] + (cnt+1)*delta_downy
                else:
                    delta = distCalc(d[0], d[1], nextx, nexty)
                    add = delta/math.sin(math.pi/2 - degree - angle[5])*math.sin( - math.pi/2 + degree + angle[4])
                    newx = d[0] + add*math.cos(angle[5])
                    newy = d[1] + add*math.sin(angle[5])
                    e += distCalc(newx, newy, lastx, lasty) / conste
                    gcode += moveLnExtrudeXY(newx, newy, e, f)
                    nb = (a[0] + cnt*delta_upx, a[1] + cnt*delta_upy)
                    na = (newx, newy)
                    nc = b
                    nd = c
                    break
            elif cnt%2 == 0 and abs(math.atan2(d[1] - nexty, d[0] - nextx) - angle[1]) <= math.pi/2:
                gcode += moveLnXY(nextx, nexty)
                lastx = nextx
                lasty = nexty
                nextx = a[0] + cnt*delta_upx
                nexty = a[1] + cnt*delta_upy
                if abs(math.atan2(b[1] - nexty, b[0] - nextx) - angle[0]) <= math.pi/2:
                    e += distCalc(nextx, nexty, lastx, lasty) / conste
                    gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                    nextx = a[0] + (cnt+1)*delta_upx
                    nexty = a[1] + (cnt+1)*delta_upy
                else:
                    delta = distCalc(b[0], b[1], nextx, nexty)
                    add = delta/math.sin(math.pi/2 + degree + angle[2])*math.sin(- math.pi/2 - degree - angle[3])
                    newx = b[0] + add*math.cos(angle[2])
                    newy = b[1] + add*math.sin(angle[2])
                    e += distCalc(newx, newy, lastx, lasty) / conste
                    gcode += moveLnExtrudeXY(newx, newy, e, f)        
                    na = (a[0]+cnt*delta_downx, a[1]+cnt*delta_downy)
                    nb = (newx, newy)
                    nc = c
                    nd = d
                    break
            else:
                if cnt%2 == 1:
                    delta = distCalc(b[0], b[1], nextx, nexty)
                    add = delta/math.sin(math.pi/2 + degree + angle[2])*math.sin(- math.pi/2 - degree - angle[3])
                    newx = b[0] + add*math.cos(angle[2])
                    newy = b[1] + add*math.sin(angle[2])
                    nb = (newx, newy)
                    gcode += moveLnXY(newx, newy)  
                    lastx = newx
                    lasty = newy
                    nextx = a[0] + cnt*delta_downx
                    nexty = a[1] + cnt*delta_downy
                    if abs(math.atan2(d[1] - nexty, d[0] - nextx) - angle[1]) <= math.pi/2:
                        e += distCalc(nextx, nexty, lastx, lasty) / conste
                        gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                        na = (nextx, nexty)
                        nc = c
                        nd = d
                    else:
                        delta = distCalc(d[0], d[1], nextx, nexty)
                        add = delta/math.sin(math.pi/2 - degree - angle[5])*math.sin( -math.pi/2 + degree + angle[4])
                        newx = d[0] + add*math.cos(angle[5])
                        newy = d[1] + add*math.sin(angle[5])
                        e += distCalc(newx, newy, lastx, lasty) / conste
                        gcode += moveLnExtrudeXY(newx, newy, e, f)
                        na = (newx, newy)
                        nc = c
                        nd = d
                        tri = 1
                else:
                    delta = distCalc(d[0], d[1], nextx, nexty)
                    add = delta/math.sin(math.pi/2 - degree - angle[5])*math.sin( - math.pi/2 + degree + angle[4])
                    newx = d[0] + add*math.cos(angle[5])
                    newy = d[1] + add*math.sin(angle[5])
                    na = (newx, newy)
                    gcode += moveLnXY(newx, newy)
                    lastx = newx
                    lasty = newy
                    nextx = a[0] + cnt*delta_upx
                    nexty = a[1] + cnt*delta_upy
                    if abs(math.atan2(b[1] - nexty, b[0] - nextx) - angle[0]) <= math.pi/2:
                        e += distCalc(nextx, nexty, lastx, lasty) / conste
                        gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                        nb = (nextx, nexty)
                        nc = b
                        nd = c
                    else:
                        delta = distCalc(b[0], b[1], nextx, nexty)
                        add = delta/math.sin(math.pi/2 + degree + angle[2])*math.sin(- math.pi/2 - degree - angle[3])
                        newx = b[0] + add*math.cos(angle[2])
                        newy = b[1] + add*math.sin(angle[2])
                        e += distCalc(newx, newy, lastx, lasty) / conste
                        gcode += moveLnExtrudeXY(newx, newy, e, f)
                        nb = (newx, newy)
                        nc = c
                        nd = c
                        tri = 1
                break

            cnt += 1    
    
    cnt += 1

    return gcode, na, nb, nc, nd, cnt, tri, e

def fillparal_quadrangle(a, b, c, d, cnt, degree, width, e):
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
        lastx = b[0]
        lasty = b[1]
        cnt = 1
    else:
        nextx = a[0] + delta_downx
        nexty = a[1] + delta_downy
        lastx = a[0]
        lasty = a[1]
        cnt = 2

    while True:
            if cnt%2 == 1 and abs(math.atan2(c[1] - nexty, c[0] - nextx) - angle[2]) <= math.pi/2:
                gcode += moveLnXY(nextx, nexty)
                lastx = nextx
                lasty = nexty
                nextx = a[0] + layer*delta_downx
                nexty = a[1] + layer*delta_downy
                if abs(math.atan2(d[1] - nexty, d[0] - nextx) - angle[1]) <= math.pi/2:
                    e += distCalc(nextx, nexty, lastx, lasty) / conste
                    gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                    nextx = a[0] + (layer+1)*delta_downx
                    nexty = a[1] + (layer+1)*delta_downy
                else:
                    delta = distCalc(d[0], d[1], nextx, nexty)
                    add = delta/math.sin(math.pi/2 - degree - angle[7])*math.sin( - math.pi/2 + degree + angle[6])
                    newx = d[0] + add*math.cos(angle[7])
                    newy = d[1] + add*math.sin(angle[7])
                    e += distCalc(newx, newy, lastx, lasty) / conste
                    gcode += moveLnExtrudeXY(newx, newy, e, f)
                    nb = (b[0] + layer*delta_upx, b[1] + layer*delta_upy)
                    na = (newx, newy)
                    nc = c
                    break
            elif cnt%2 == 0 and abs(math.atan2(d[1] - nexty, d[0] - nextx) - angle[1]) <= math.pi/2:
                gcode += moveLnXY(nextx, nexty)
                lastx = nextx
                lasty = nexty
                nextx = b[0] + layer*delta_upx
                nexty = b[1] + layer*delta_upy
                if abs(math.atan2(c[1] - nexty, c[0] - nextx) - angle[2]) <= math.pi/2:
                    e += distCalc(nextx, nexty, lastx, lasty) / conste
                    #print(e)
                    gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                    nextx = b[0] + (layer+1)*delta_upx
                    nexty = b[1] + (layer+1)*delta_upy
                else:
                    delta = distCalc(c[0], c[1], nextx, nexty)
                    add = delta/math.sin(math.pi/2 + degree + angle[4])*math.sin(3*math.pi/2 - degree - angle[5])
                    newx = c[0] + add*math.cos(angle[4])
                    newy = c[1] + add*math.sin(angle[4])
                    e += distCalc(newx, newy, lastx, lasty) / conste
                    gcode += moveLnExtrudeXY(newx, newy, e, f)        
                    na = (a[0]+layer*delta_downx, a[1]+layer*delta_downy)
                    nb = (newx, newy)
                    nc = d
                    #print(nb)
                    break
            else:
                if cnt%2 == 1:
                    delta = distCalc(c[0], c[1], nextx, nexty)
                    add = delta/math.sin(math.pi/2 + degree + angle[4])*math.sin(3*math.pi/2 - degree - angle[5])
                    newx = c[0] + add*math.cos(angle[4])
                    newy = c[1] + add*math.sin(angle[4])
                    nb = (newx, newy)
                    #print(nb)
                    gcode += moveLnXY(newx, newy) 
                    nextx = a[0] + layer*delta_downx
                    nexty = a[1] + layer*delta_downy
                    if abs(math.atan2(d[1] - nexty, d[0] - nextx) - angle[1]) <= math.pi/2:
                        e += distCalc(newx, newy, nextx, nexty) / conste
                        gcode += moveLnExtrudeXY(nextx, nexty, e, f)
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
                    gcode += moveLnXY(newx, newy)
                    nextx = b[0] + layer*delta_upx
                    nexty = b[1] + layer*delta_upy
                    if abs(math.atan2(c[1] - nexty, c[0] - nextx) - angle[2]) <= math.pi/2:
                        e += distCalc(newx, newy, nextx, nexty) / conste
                        #print(e)
                        gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                        nb = (nextx, nexty)
                        #print(nb)
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

    return gcode, na, nb, nc, cnt, fin, e

def fill_triangle(a, b, c, cnt, degree, width, e):
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

    if cnt%2 == 1:
        nextx = b[0] + delta_upx
        nexty = b[1] + delta_upy
        cnt = 1
    else:
        nextx = a[0] + delta_downx
        nexty = a[1] + delta_downy
        cnt = 2

    while True:
            if cnt%2 == 1 and abs(math.atan2(c[1] - nexty, c[0] - nextx) - angle[1]) <= math.pi/2:
                gcode += moveLnXY(nextx, nexty)
                lastx = nextx
                lasty = nexty
                nextx = a[0] + layer*delta_downx
                nexty = a[1] + layer*delta_downy
                if abs(math.atan2(c[1] - nexty, c[0] - nextx) - angle[0]) <= math.pi/2:
                    e += distCalc(nextx, nexty, lastx, lasty) / conste
                    gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                    nextx = a[0] + (layer+1)*delta_downx
                    nexty = a[1] + (layer+1)*delta_downy
                else:
                    break
            elif cnt%2 == 0 and abs(math.atan2(c[1] - nexty, c[0] - nextx) - angle[0]) <= math.pi/2:
                gcode += moveLnXY(nextx, nexty)
                lastx = nextx
                lasty = nexty
                nextx = b[0] + layer*delta_upx
                nexty = b[1] + layer*delta_upy
                if abs(math.atan2(c[1] - nexty, c[0] - nextx) - angle[1]) <= math.pi/2:
                    e += distCalc(nextx, nexty, lastx, lasty) / conste
                    gcode += moveLnExtrudeXY(nextx, nexty, e, f)
                    nextx = b[0] + (layer+1)*delta_upx
                    nexty = b[1] + (layer+1)*delta_upy
                else:     
                    break
            else:
                break

            cnt += 1    
            layer += 1

    return gcode


def merge_quadrangle(a, b, c, d, degree, width, shell_width, circle, e):
    gcode = ""
    #dis = []
    left, sec, third, last = sort_point(a, b, c, d) #if neccessary
    angle = cal_angle(left, sec, third, last)
    #dis.append(distCalc(a[0], b[0], a[1], b[1]))
    #dis.append(distCalc(b[0], c[0], b[1], c[1]))
    #dis.append(distCalc(c[0], d[0], c[1], d[1]))
    #dis.append(distCalc(d[0], a[0], d[1], a[1]))

    gcode, na, nb, nc, nd, e = gen_shell(left, sec, third, last, circle, shell_width, gcode, angle, e)

    gcode += '; end of circle \n'

    gcode += moveLnXY(na[0], na[1])

    if angle[0] > math.pi/2 - degree:
        alpha = math.pi/2 - degree - angle[2]
        step1 = width/math.sin(alpha)
        delta_upx = step1*math.cos(angle[2])
        delta_upy = step1*math.sin(angle[2])
        #gcode += moveLnXY(a[0] + delta_upx, a[1] + delta_upy)       

        beta = math.pi/2 + degree + angle[3]
        step2 = width/math.sin(beta)
        delta_downx = step2*math.cos(angle[3])
        delta_downy = step2*math.sin(angle[3])
        newangle = [angle[2], angle[3], angle[4], angle[5], angle[0], angle[1]]

        cnt = 1
        gcode1, na, nb, nc, nd, cnt, tri, e = fill_quadrangle(nb, nc, nd, na, degree, delta_upx, delta_upy, delta_downx, delta_downy, newangle, cnt, e)
        #print(na, nb, nc, nd)

        if tri == 1:
            gcode += gcode1
            gcode += fill_triangle(na, nb, nc, cnt, degree, width, e)
        else:
            gcode2, na, nb, nc, cnt, fin, e = fillparal_quadrangle(na, nb, nc, nd, cnt, degree, width, e)
            #print(na, nb, nc)
            if fin == 1:
                gcode += gcode1
                gcode += gcode2
            else:
                gcode += gcode1
                gcode += gcode2
                gcode += fill_triangle(na, nb, nc, cnt, degree, width, e)

    elif angle[0] == math.pi/2 - degree:
        cnt = 1
        gcode2, na, nb, nc, cnt, fin, e = fillparal_quadrangle(na, nb, nc, nd, cnt, degree, width, e)
        if fin == 1:
                gcode += gcode2
        else:
                gcode += gcode2
                gcode += fill_triangle(na, nb, nc, cnt, degree, width, e)
    else:
        #draw_line(nb, nc, na)
        alpha = math.pi/2 - degree - angle[0]
        step1 = width/math.sin(alpha)
        delta_upx = step1*math.cos(angle[0])
        delta_upy = step1*math.sin(angle[0])
        #gcode += moveLnXY(a[0] + delta_upx, a[1] + delta_upy)       

        beta = math.pi/2 + degree + angle[1]
        step2 = width/math.sin(beta)
        delta_downx = step2*math.cos(angle[1])
        delta_downy = step2*math.sin(angle[1])

        newangle = [angle[0], angle[1], angle[2], angle[3], angle[6], angle[7]]

        cnt = 1
        gcode1, na, nb, nc, nd, cnt, tri, e = fill_quadrangle(na, nb, nc, nd, degree, delta_upx, delta_upy, delta_downx, delta_downy, newangle, cnt, e)
        #print(tri)
        #print(na, nb, nc, nd)

        if tri == 1:
            gcode += gcode1
            gcode += fill_triangle(na, nb, nc, cnt, degree, width, e)
        else:
            gcode2, na, nb, nc, cnt, fin, e = fillparal_quadrangle(na, nb, nc, nd, cnt, degree, width, e)
            #print(na, nb, nc)
            if fin == 1:
                gcode += gcode1
                gcode += gcode2
            else:
                gcode += gcode1
                gcode += gcode2
                gcode += fill_triangle(na, nb, nc, cnt, degree, width, e)
        

    return gcode




def gcodeMerging():
    baseGcode = fileRead()
    #mainGcode = merge_quadrangle(a, b, c, d, degree, width, shell_width, circle)
    mainGcode = "\n"
    cur_z = z0
    deg = degree
    while cur_z < height_sum + z0:
        if deg > 0:
            deg -= math.pi/2
        else:
            deg += math.pi/2
        mainGcode += moveLnZ(cur_z)
        mainGcode += merge_quadrangle(a, b, c, d, deg, width, shell_width, circle, 0)
        cur_z += height_each
        
    
    gcode = baseGcode + mainGcode + 'G10\nG11\nG0 Z10'
    return gcode



def fileRead():
    baseGcodePath = 'C:/VScode/gcode/starting_TPU_01.gcode'
    with open(baseGcodePath, "r") as f:
        gcode = f.read()
    return gcode



if __name__ == '__main__':

    a = (150, 180)
    b = (230, 230)
    c = (180, 230)
    d = (230, 180)
    degree = -math.pi/4
    width = 0.75
    shell_width = 0.3
    circle = 3
    z0 = 0.2
    height_each = 0.2
    height_sum = 1.2

    # generate the final print Gcode
    finalGcode = gcodeMerging()

     # save the Gcode file
    savedFilePath = "C:/VScode/gcode/test1.gcode"
    with open(savedFilePath, "w") as f:
        f.write(finalGcode)
    print("Successfully generate Gcode!")
    #fileRead()