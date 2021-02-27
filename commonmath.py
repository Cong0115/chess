from math import atan, atan2, degrees, radians, pi, cos, sin

def distancetoline(x1,y1,x2,y2,x3,y3):
    ### Returns normal distance from point (x3,y3)
    ### to line (x1,y1)-(x2,y2)
    
    try:
        x1=float(x1)
        y1=float(y1)
        x2=float(x2)
        y2=float(y2)
        x3=float(x3)
        y3=float(y3)
    except ValueError:
        return None

    # if x1=x2 (i.e. the line is vertical), then Z=|x1-x3|
    # if y1=y2 (i.e. the line is horizontal), then Z=|y1-y3|

    if (x1==x2):
        return abs(x1-x3)
    elif (y1==y2):
        return abs(y1-y3)
    else:
        m1=(y2-y1)/(x2-x1)      # slope of line 1
        b1=(m1*(-x1))+y1        # y-intercept of line 1
        m3=-(1/m1)              # slope of line 3 (from our point to our line)
        b3=(m3*(-x3))+y3        # y-intercept of line 3
        x4=(b3-b1)/(m1-m3)      # x of intersection of line 3 and our line
        y4=(m1*x4)+b1           # y of ""
        b=(((y4-y1)**2)+((x4-x1)**2))**.5       # distance p1 to p4
        a=(((y3-y1)**2)+((x3-x1)**2))**.5       # distance p1 to p3
        return ((a**2)-(b**2))**.5

def angle(x1,y1,x2,y2,indegrees=True):
    ### Returns angle (default=degrees) from point1 (x1,y1) to point2 (x2,y2)
    ### (Returns angle as -180 to 180 degrees, or -pi to pi radians)
    
    try:
        x1=float(x1)
        y1=float(y1)
        x2=float(x2)
        y2=float(y2)
    except ValueError:
        return None
    
    deltax,deltay=(x2-x1),(y2-y1)
    if deltax!=0:
        ang=degrees(atan2(deltay,deltax))
    else:
        if deltay>0:
            ang=90.0
        else:
            ang=270.0
    if (indegrees):
        return ang
    else:
        return radians(ang)

def distance(x1,y1,x2,y2):
    ### Returns distance from point1 (x1,y1) to point2 (x2,y2)
    
    try:
        x1=float(x1)
        y1=float(y1)
        x2=float(x2)
        y2=float(y2)
    except ValueError:
        return None

    deltax,deltay=(x2-x1),(y2-y1)
    return ((deltax**2)+(deltay**2))**.5
    
def vectorbetween(x1,y1,x2,y2,indegrees=True):
    ### Returns vector (angle,distance), default=degrees
    ### from point1 (x1,y1) to point2 (x2,y2)
    ### (Returns angle as -180 to 180 degrees, or -pi to pi radians)
    
    try:
        x1=float(x1)
        y1=float(y1)
        x2=float(x2)
        y2=float(y2)
    except ValueError:
        return None
    
    ang=angle(x1,y1,x2,y2,indegrees)
    dist=distance(x1,y1,x2,y2)
    return (ang,dist)

def ellipseperimeter(axis1,axis2):
    ### Returns perimeter of an ellipse, given 2 axes (axis1 and axis2)
    ### (Either the major or minor axis can be first)

    try:
        axis1=float(axis1)
        axis2=float(axis2)
    except ValueError:
        return None

    rad1=axis1 / 2
    rad2=axis2 / 2
    
    return (pi*(rad1+rad2))*(3*(((rad1-rad2)**2)/(((rad1+rad2)**2)*
        (((-3*((rad1-rad2)**2)/((rad1+rad2)**2)+4)**.5)+10)))+1)

def pointplusvector(x,y,vector):    #takes angles in degrees
    ang,dist=vector[0],vector[1]
    return (x+(dist*cos(radians(ang))),y+(dist*sin(radians(ang))))

def rotatepoints(pointlist,rotpoint,rotangle):    #takes angles in degrees
    result=[]
    for point in pointlist:
        v=vectorbetween(*rotpoint,*point)
        p=pointplusvector(*rotpoint,(v[0]+rotangle,v[1]))
        result.append(p)
    return result
        
##
##print(distancetoline(24.394,13.661,26.079,4.992,26.966,10.308))
##print(distancetoline(1,1,1,5,7,3))
##print(distancetoline(*(2,1),*(3,4),*(6,7)))
##print(angle(0,0,12,0))
##print(vectorbetween(1,1,12,-10))
##print(ellipseperimeter(1,1.030))
##an=angle(0,0,0,5)
##print(an,type(an))

