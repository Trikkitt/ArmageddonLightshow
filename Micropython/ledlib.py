import machine, neopixel
import utime, random, math

def anim_sparkles(np,backgroundcolour,sparklecolour,cycles,stepdelay):
    n=np.n
    sparkles=n // 30
    sparkletracks={}

    np.fill(backgroundcolour)
    for cycle in range(cycles):
        while len(sparkletracks)<sparkles:
            pixel=random.randint(0,n-1)
            sparkletracks[pixel]=random.randint(2,4)
            np[pixel]=sparklecolour
        for pixel in sparkletracks.keys():
            sparkletracks[pixel]-=1
            if sparkletracks[pixel]==0:
                np[pixel]=backgroundcolour
                del sparkletracks[pixel]
        np.write()
        if stepdelay>0: utime.sleep_ms(stepdelay)


def anim_fadecolours(np,oldhue,newhue,steps,maxv):
    n=np.n
    if oldhue>newhue:
        bighue=oldhue
        smallhue=newhue
    else:
        bighue=newhue
        smallhue=oldhue
    huegapdirect=bighue-smallhue
    huegapwrap=(1-bighue) + oldhue
    if huegapdirect<huegapwrap:
        if oldhue>newhue:
            huestep=0-(huegapdirect/steps)
        else:
            huestep=huegapdirect/steps
    else:
        if oldhue>newhue:
            huestep=hugegapwrap/steps
        else:
            huestep=0-(hugegapwrap/steps)
    hue=oldhue
    for x in range(steps):
        colour=hsv2rgb(hue,1,maxv)
        np.fill(colour)
        np.write()
        hue+=huestep
        if hue<0: hue=1
        if hue>1: hue=0


def anim_fadecyclecolours(np,steps,maxv):
    n=np.n
    hue=0
    huestep=1/steps
    for x in range(steps):
        colour=hsv2rgb(hue,1,maxv)
        np.fill(colour)
        np.write()
        hue+=huestep


def anim_fadeupdown(np,hue,steps,direction):
    n=np.n
    s=1
    if direction==0:
        v=1
        valuestep=0-(1/steps)
    else:
        v=0
        valuestep=1/steps
    for stepcount in range(steps):
        vfixed=hsvgammacorrect(v)
        rgb=hsv2rgb(hue,s,vfixed)
        np.fill(rgb)
        np.write()
        v+=valuestep

def anim_rainbowchase(np,length,steps,stepdelay,maxv):
    n=np.n
    huestep=1/length
    hue=0
    huerange=[]
    for x in range(length):
        huerange.append(hsv2rgb(hue,1,maxv))
        hue+=huestep
        if hue>1: hue=0
    hueindex=0
    for x in range(n):
        np[x]=huerange[hueindex]
        hueindex+=1
        if hueindex>=length: hueindex=0
    np.write()
    for stepcount in range(steps):
        np.buf=np.buf[3:] + b'\x00\x00\x00'
        np[n-1]=huerange[hueindex]
        hueindex+=1
        if hueindex>=length: hueindex=0
        np.write()
        if stepdelay>0: utime.sleep_ms(stepdelay)


def anim_flashrandom(np,steps,stepdelay,maxv):
    n=np.n
    hue=0
    for step in range(steps):
        oldhue=hue
        hue=random.random()
        while closecolour(oldhue,hue):
            print("Hue bounce")
            hue=random.random()
        colour=hsv2rgb(hue,1,maxv)
        np.fill(colour)
        np.write()
        if stepdelay>0: utime.sleep_ms(stepdelay)

def anim_pixelmix(np,colour,pixelsperframe,stepdelay,maxv):
    n=np.n
    pixels=list(random_range(n))

    if colour==None:
        randomcolour=True
    else:
        randomcolour=False

    framecounter=pixelsperframe
    for step in range(n):
        pixel=pixels[step]
        if randomcolour==True:
            colour=hsv2rgb(random.random(),1,maxv)
        np[pixel]=colour
        framecounter-=1
        if framecounter==0:
            np.write()
            if stepdelay>0: utime.sleep_ms(stepdelay)
            framecounter=pixelsperframe
    if randomcolour==False:
        np.fill(colour)
        np.write()

def anim_pixelmixrandom(np,colourcount,pixelsperframe,stepdelay,holdtime,maxv):
    hue=0
    for c in range(colourcount):
        oldhue=hue
        hue=random.random()
        while closecolour(oldhue,hue):
            print("Hue bounce")
            hue=random.random()
        colour=hsv2rgb(hue,1,maxv)
        if random.randint(0,10)==5: colour=None
        anim_pixelmix(np,colour,pixelsperframe,stepdelay,maxv)
        if holdtime>0: utime.sleep_ms(holdtime)

def anim_flash(np,stepcount,blankdelay,litdelay):
    existingbuf=bytearray(len(np.buf))
    existingbuf[:]=np.buf
    for x in range(stepcount):
        np.fill((0,0,0))
        np.write()
        if blankdelay>0: utime.sleep_ms(blankdelay)
        np.buf[:]=existingbuf
        np.write()
        if litdelay>0: utime.sleep_ms(litdelay)

def anim_blank(np):
    np.fill((0,0,0))
    np.write()

def anim_onecolour(np,colour):
    np.fill(colour)
    np.write()

def anim_slowtrain(np,colour,stepdelay):
    n=np.n
    while n>0:
        np.fill((0,0,0))
        n-=1
        np[n]=colour
        np.write()
        if stepdelay>0: utime.sleep_ms(stepdelay)

def anim_rings(np,colour,stepdelay,repeatcount):
    while repeatcount>0:
        repeatcount-=1
        for count in range(0,9):
            np.fill((0,0,0))
            fillring(np,colour,count)
            np.write()
            if stepdelay>0: utime.sleep_ms(stepdelay)
        for count in range(8,-1,-1):
            np.fill((0,0,0))
            fillring(np,colour,count)
            np.write()
            if stepdelay>0: utime.sleep_ms(stepdelay)
        
def anim_rainbowring(np,stepdelay,huestep,repeatcount,maxv):
    while repeatcount>0:
        hue=1
        repeatcount-=1
        while hue>0:
            temphue=hue
            hue-=huestep
            for ringnumber in range(0,9):
                fillring(np,hsv2rgb(temphue,1,maxv),ringnumber)
                temphue-=huestep
                if temphue<0:
                    temphue+=1
            np.write()
            if stepdelay>0: utime.sleep_ms(stepdelay)

ringstart=[0,1,9,21,37,61,93,133,181]
ringlength=[1,8,12,16,24,32,40,48,60]

def fillring(np,colour,ringnumber):
    n=ringstart[ringnumber]
    c=ringlength[ringnumber]
    while c>0:
        np[n]=colour
        c-=1
        n+=1
        
    

def closecolour(oldhue,newhue):
    closevalue=0.15
    if oldhue>newhue:
        bighue=oldhue
        smallhue=newhue
    else:
        bighue=newhue
        smallhue=oldhue
    huegap=bighue-smallhue
    if huegap<closevalue: return(True)
    huegap=(1-bighue) + smallhue
    if huegap<closevalue: return(True)
    return(False)

def random_range(maximum):
    found=0
    mapping=lambda i: i+1
    value=random.randint(0,maximum)
    offset = random.randint(0,maximum) * 2 + 1
    multiplier = 4*(maximum//4) + 1
    modulus = int(2**math.ceil(math.log2(maximum)))
    while found<maximum:
        if value<maximum:
            found+=1
            yield mapping(value-1)
        value=(value*multiplier + offset) % modulus

def hsv2rgb(h, s, v):
        if s == 0.0: return (v, v, v)
        i = int(h*6.) # XXX assume int() truncates!
        f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
        v=round(v * 255)
        p=round(p * 255)
        t=round(t * 255)
        q=round(q * 255)
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        if i == 5: return (v, p, q)

def hsvgammacorrect(v):
    index=int(v*255)
    return(gammatable[index]/255)

gammatable=[
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255 ]

np = neopixel.NeoPixel(machine.Pin(0),242)
maxbrightness=0.5

while True:
    effectid=random.randint(1,19)
    #effectid=19
#for effectid in range(15,16):
    
    if effectid==1:
        anim_rainbowchase(np,5,400,30,maxbrightness)
    if effectid==2:
        anim_pixelmixrandom(np,10,3,0,2000,maxbrightness)
    if effectid==3:
        hue=random.random()
        colour=hsv2rgb(hue,1,maxbrightness)
        anim_pixelmix(np,colour,5,0,maxbrightness)
        anim_sparkles(np,colour,(255,255,255),350,1)
    if effectid==4:
        anim_pixelmix(np,(0,0,255),5,0,maxbrightness)
        anim_sparkles(np,(0,0,255),(255,255,255),450,1)
    if effectid==5:
        anim_flashrandom(np,30,250,maxbrightness)
        anim_pixelmix(np,(0,0,0),5,0,maxbrightness)
    if effectid==6:
        anim_rainbowchase(np,50,400,2,maxbrightness)
    if effectid==7:
        anim_pixelmix(np,(255,0,100),5,0,maxbrightness)
        anim_sparkles(np,(255,0,100),(255,255,255),450,1)
    if effectid==8:
        anim_pixelmix(np,None,5,0,maxbrightness)
    if effectid==9:
        anim_rainbowchase(np,300,500,0,maxbrightness)
    if effectid==10:
        anim_fadecyclecolours(np,200,maxbrightness)
        anim_fadecyclecolours(np,200,maxbrightness)
        anim_fadecyclecolours(np,200,maxbrightness)
    if effectid==11:
        rainbowlen=random.randint(6,250)
        avglen=(250-rainbowlen)//8
        delaylen=random.randint(avglen-3,avglen+3)
        if delaylen<0: delaylen=0
        cycles=200+(150*((31-delaylen)/6))
        anim_rainbowchase(np,rainbowlen,cycles,delaylen,maxbrightness)
    if effectid==12:
        colourcount=random.randint(10,50)
        colourdelay=random.randint(200,400)
        anim_flashrandom(np,colourcount,colourdelay,maxbrightness)
    if effectid==13:
        colourdelay=random.randint(25,400)
        repeatcount=random.randint(2,5)
        for x in range(repeatcount):
            anim_fadecyclecolours(np,colourdelay,maxbrightness)
    if effectid==14:
        anim_pixelmix(np,None,5,0,maxbrightness)
        anim_pixelmix(np,(0,0,0),10,0,maxbrightness)
        anim_pixelmix(np,None,5,0,maxbrightness)
        anim_pixelmix(np,(0,0,0),10,0,maxbrightness)
        anim_pixelmix(np,None,5,0,maxbrightness)
        anim_pixelmix(np,(0,0,0),10,0,maxbrightness)
    if effectid==15:
        anim_pixelmix(np,None,5,0,maxbrightness)
        anim_flash(np,20,150,50)
    if effectid==16:
        rndhue=random.random()
        colour=hsv2rgb(rndhue,1,1)
        anim_slowtrain(np,colour,0)
    if effectid==17:
        rndhue=random.random()
        colour=hsv2rgb(rndhue,1,maxbrightness)
        anim_rings(np,colour,100,1)
    if effectid==18:
        #anim_rainbowring(np,40,0.04,1,maxbrightness)
        #anim_rainbowring(np,20,0.05,1,maxbrightness)
        #anim_rainbowring(np,10,0.08,10,maxbrightness)
        anim_rainbowring(np,0,0.01,1,maxbrightness)
    if effectid==19:
        #anim_rainbowring(np,40,0.04,1,maxbrightness)
        #anim_rainbowring(np,20,0.05,1,maxbrightness)
        anim_rainbowring(np,10,0.08,10,maxbrightness)
        #anim_rainbowring(np,0,0.01,1,maxbrightness)
        



