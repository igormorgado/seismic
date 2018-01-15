# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 07:12:30 2016

"""
import math

def azimuth(u1,u2,v1,v2):
    return math.atan2(v2-u2,v1-u1)

def layerDistance(x, t, v):
    """Calculates the layer bottom distance
    x: receiver offset distance
    t: two way travel time    
    v: layer velocity    
    """
    return math.sqrt((v**2*t**2 - x**2))/2.

def traveltime(x, h, v):
    """ Calculates the two way travel time
    x:  receiver offset distance
    h:  layer bottom distance
    v:  layer velocity
    """
    return math.sqrt(((x/float(v))**2)+(((2*h)/float(v))**2))

def channelOffset(c, x0, dc):
    """Calculates the channel offset
    c: Channel number
    x0: Initial channel distance in meters
    dc: Delta Channel (distance between channels)
    """
    return x0 + (c-1) * dc

def midx(x1,x2):
    return (x1 + x2)/2.

def midy(y1, y2):
    return (y1 + y2)/2.

def offset(x1, y1, x2, y2):
    return math.sqrt( (x2-x1)**2 + (y2-y1)**2 )

def subline(y, dy):
    return round(y/dy)+1

def crossline(x, dx):
    return round(x/dx)+1

def cdp(il, xl):
    return 10000*il + xl

if __name__ == "__main__":
    shotx=558.25            # in meters
    shoty=539.75            # in meters
    recvx=1024.07           # in meters
    recvy=397.07            # in meters
    layerVelocity=1.5       # in meters per milisecond
    nearOffset=300          # in meters
    deltaReceiver=25        # in meters
    numberReceiver=400      # in units
    nearChannelTravelTime=1732      # in miliseconds
    deltaCDPX=12.5
    deltaCDPY=40

    az=math.degrees(azimuth(shotx,shoty,recvx,recvy))
    print("Azimuth {0:.2f} degrees".format(az))

    ld=layerDistance(nearOffset, nearChannelTravelTime, layerVelocity)
    print ("Water bottom: {0:.2f} meters".format(ld))

    t10=traveltime(
        channelOffset(10,nearOffset,deltaReceiver),
        ld,
        layerVelocity
        )

    t100=traveltime(
        channelOffset(100,nearOffset,deltaReceiver),
        ld,
        layerVelocity
        )

    t400=traveltime(
        channelOffset(400,nearOffset,deltaReceiver),
        ld,
        layerVelocity
        )

    print("TT channel 10 : {0:.2f} ms".format(t10))
    print("TT channel 100: {0:.2f} ms".format(t100))
    print("TT channel 400: {0:.2f} ms".format(t400))

    mx=midx(shotx,recvx)
    my=midy(shoty,recvy)
    offs=offset(shotx,shoty,recvx,recvy)

    print("MidX {0:.2f} meters".format(mx))
    print("MidY {0:.2f} meters".format(my))
    print("Offset {0:.2f} meters".format(offs))

    il=subline(my,deltaCDPY)
    print("Inline: {0}".format(il))

    xl=crossline(mx,deltaCDPX)
    print("Crossline: {0}".format(xl))

    CDP=cdp(il,xl)
    print("CDP: {0}".format(CDP))
