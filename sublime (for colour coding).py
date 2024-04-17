#initialise stage
import os
import math
import turtle

plist = []
vlist = []
blist = []
clist = []
coordlist = []

#functions to use for drawing
def drawLine(v1,v2,colorfill):
    turtle.color(colorfill)
    turtle.penup()
    turtle.speed(0)
    turtle.goto(v1)
    turtle.pendown()
    turtle.goto(v2)
    turtle.fillcolor(colorfill)
    turtle.penup()

def drawBezierCurve (v1, v2, v3, v4,colorfill):
    for i in range(101):
        turtle.color(colorfill)
        t = i/100
        x = v1[0]*(1-t)**3 + 3*v2[0]*t*(1-t)**2 + 3*v3[0]*t*t*(1-t) + v4[0]*t**3
        y = v1[1]*(1-t)**3 + 3*v2[1]*t*(1-t)**2 + 3*v3[1]*t*t*(1-t) + v4[1]*t**3
        turtle.speed(0)
        turtle.goto(x, y)
        if i == 0: turtle.pendown()
    turtle.fillcolor(colorfill)

def polygondraw (blist, vlist):
    a = 0
    while True:
        colorfill = input("Enter the colour for the polygon: ")
        turtle.penup()
        turtle.goto(vlist[0]) #move the pen to the start of polygon coordinate
        while a < len(vlist):
            if a in blist:
                if a+1 == len(vlist):
                    drawBezierCurve(vlist[a], vlist[0], vlist[1], vlist[2],colorfill)
                    break
                else:
                    drawBezierCurve(vlist[a], vlist[a+1], vlist[a+2], vlist[a+3],colorfill)
                    a += 3 # move to the last vertex of the curve
            else:
                if a+1 == len(vlist):
                    drawLine(vlist[a], vlist[0],colorfill)
                    break
                else:
                    drawLine(vlist[a], vlist[a+1],colorfill)
                    a += 1 # move to the next vertex
        break

def load_file(file_name):
    if not os.path.exists(file_name):
        raise Exception("File cannot be found")
    
    with open(file_name, "r") as f:
        data = f.read()

    return data


def parse_data(data):
    lines = data.split("\n")
    vlists = []
    blists = []
    bstack = []
    vstack = []
    is_polygon_data = False
    is_curve_data = False
    curve_count = 0
    for l in lines:
        # ignore empty lines
        if len(l) == 0:
            continue
        
        # ! indicate start of polygon
        if l.find('!') == 0:
            is_polygon_data = not is_polygon_data
            if is_polygon_data:
                if vstack and bstack:
                    # save polygon and reset stack
                    vlists.append(vstack)
                    blists.append(bstack)
                    vstack = []
                    bstack = []
            continue
        # # indicate the number of curves exists in the polygon
        elif l.find('#') == 0:
            is_curve_data = True
            curve_count = int(l.split(" ")[1])
            continue
        
        # if curve_count == 0 then just skip
        if curve_count == 0:
            is_curve_data = False

        if is_polygon_data:
            v1, v2 = l.split(" ")
            v1, v2 = float(v1), float(v2)
            vstack.append((v1,v2))
        elif is_curve_data:
            i = int(l)
            if i >= 0 and i < len(vstack):
                bstack.append(i)
            curve_count -= 1
    
    return blists, vlists


def draw(blists, vlists):
    for i in range(len(vlists)):
        polygondraw(blists[i], vlists[i])

prompt = 1


# drawing of the shapes (curves / straights)
while True:
    print("Choose how you would like to input your data:")
    print("1. Manually Key in each coordinates")
    print("2. Import data ")
    
    cond = input("Your selection: ")
    # Manually input data
    if cond == "2":
        while True:
            if __name__ == "__main__":
                filename = input("Enter the filename you wish to import: ")
                data = load_file(filename)
                blists, vlists = parse_data(data)
                draw(blists, vlists)

            print("Choose one of the following options.")
            print("1. Choose another file.")
            print("2. Transform current file.")
            print("3. Accept current drawing.")
                
            neworend = input("Your selection: ")
            if neworend == "1":
                print()
            elif neworend == "2":
                break
            elif neworend == "3":
                turtle.stamp()
                turtle.hideturtle()
                break
            else:
                print("Error, please try again.")

            

    elif cond == "1":
        while True:
            
            #manually key in coordinates (from data set)
            numofpolygons = int(input("Enter the total number of polygons in the logo: "))

            for i in range (0, numofpolygons):
                print("Polygon number ", i+1)
                #ask for number of vertices
                numofvertices = int(input("Enter the number of vertices in the polygon: "))
                for i2 in range (0, numofvertices):
                    vertices = input("Enter the coordinate of the vertice (120 150): ")
                    if "abcdefghijklmnopqrstuvwxyz!,.@#$%&*()-=/?" in vertices:
                        print("Error, try again.")
                        i2 = i2-1
                    
                    else:
                        coordinates = vertices.split()
                        vlist.append([float(coordinates[0]), float(coordinates[1])])
                    
                while True:
                    qcurve = str(input("Is there any curves in the polygon to be drawn? (Y/N): "))
                    qcurve = qcurve.upper()
                    if qcurve == "Y":
                        numofcurves = int(input("How many curves are in the polygon?: "))
                        for i3 in range (0, numofcurves):
                            
                            startofcurve = int(input("Enter the vertex number that starts the curve [example: 4]: "))
                            blist.append(startofcurve)
                            
                        break
                    elif qcurve == "N":
                        break
                    else:
                        print("Invalid input try again.")
                polygondraw(blist, vlist)
                clist = vlist
                blist.clear()
                vlist.clear()
    #crash prevention        
    else:
        print()
        print("Input error, please try again.")
        print()
        
        
#transform functions

def transform(x,y,rotation):
    turtle.setx(turtle.xcor() + x)  # Move turtle along x-axis
    turtle.sety(turtle.ycor() + y)  # Move turtle along y-axis
    turtle.setheading(turtle.heading() + rotation)  # Rotate turtle

def scale(factor):
    turtle.shapesize(factor)

while True:

    print("Please pick your option of what you would like to do with your drawing")
    print("1. Transform")
    print("2. Scale")
    print("3. Skew")
    options = input("Enter your selection: ")
    if options == "1":
        while True:

            qtransform = input("Input the transformation in the form of X, Y, Rotation (in degrees) (example: 50,40,45): ")
            if "cancel" in qtransform:
                break
            elif "abcdefghijklmnopqrstuvwxyz" in qtransform:
                print("Error, try again. Ensure only numbers and comma are entered.")
            else:
                data2 = qtransform.split(",")
                transform(data2[0],data2[1],data2[2])

                qloop = input("Would you like to transform again?(Y/N): ")
                qloop.upper()
                if qloop == "N":
                    break

    elif options == "2":
        while True:
            factor = float(input("How much would you like to scale the drawing?: "))
            if factor.isnumeric():
                qscale = scale(factor)
                break
            else:
                print("Sorry, you have selected a wrong value, please enter a number.")

    elif options == "3":
        print()
    else:
        print()
        print("Error! Please check your selection again")
        print()

