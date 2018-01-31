from Saver import saves
N_PHI = 30*15
N_save = N_PHI

fc = 1
wd = 1080/fc;ht = 1080/fc

nS = 10e-3
nS2 = 1e1
nT = 1e-2
nSf = 1e3   #noise space offset
xoff = 1e-9
yoff = 135.
sep = 45.
fadeamt = .05
nparts = 540
nlines = 9
sw = 5

def settings():
    size(wd,ht)

def setup():
    global saver,ll
    seed = int(random(0,999999))
    print seed
    noiseSeed(seed) 
    noiseDetail(3)
    colorMode(HSB,1.)
    # frameRate(2)
    background(0)
    ll = []
    for i in xrange(nlines):
        y = map(i,0,nlines-1,0,ht)
        ls = linea(nparts,PVector(0,y),PVector(wd,y))
        ll.append(ls)
    saver = saves(N_PHI, N_save)

def draw():
    global T
    T = frameCount*nT
    blendMode(SUBTRACT)
    noStroke()
    fill(fadeamt)
    rect(0,0,width,height)
    blendMode(BLEND)
    # background(0)
    for i in xrange(len(ll)):
        ll[i].show()
        ll[i].update()
    # strokeWeight(1)
    # stroke(1)
    # line(0,ht/2.,wd,ht/2.)
    # stroke(.5)
    # line(0,ht/2.+yoff,wd,ht/2.+yoff)
    # line(0,ht/2.-yoff,wd,ht/2.-yoff)
    saver.save_frame()

###

class part():
    def __init__(self,posi,posf,c,ancho):
        self.posi = posi
        self.posf = posf
        self.maxp = PVector.add(posf,PVector(xoff,yoff))
        self.ioff = PVector(0,0)
        self.foff = PVector(0,0)
        self.c = c
        self.ancho = ancho
    
    def show(self):
        poff = PVector.add(self.foff,self.ioff)
        hx = map((self.posi.y+self.posf.y)/2,0,height,-1,1)
        hy = map((self.foff.y+self.ioff.y)/2.,-yoff,yoff,-.25,.25)
        h = hloop(self.c+hx+hy)
        stroke(h,1,1)
        strokeWeight(self.ancho)
        xi = self.posi.x + self.ioff.x
        yi = self.posi.y + self.ioff.y
        xf = self.posf.x + self.foff.x       
        yf = self.posf.y + self.foff.y
        line(xi,yi,xf,yf)
    
    def update(self,off):
        self.ioff = off
        x = (self.posi.x + self.posf.x)/2.
        y = (self.posi.y + self.posf.y)/2.
        # xf = map(noise(x*nS+nSf,y*nS+nSf,T),0,.8,-xoff,xoff)
        # yf = map(noise(x*nS-nSf,y*nS-nSf,T),0,.8,-yoff,yoff)
        xf = map(nice(cos(x/width)*nS+nSf+sin(x/width)*nS+nSf,T),0,1,-xoff,xoff)
        yf = map(noise(nice(x,0)*nS2+T,y*3e-3),0,.8,-yoff,yoff)
        self.foff = PVector(xf,yf)

###

class linea():
    def __init__(self,n,posi,posf):
        self.n = n
        self.posi = posi
        self.posf = posf
        self.p = []
        self.L = PVector.div(PVector.sub(posf,posi),self.n)
        for i in xrange(self.n):
            xyi = PVector.add(self.posi,PVector.mult(self.L,i))
            xyf = PVector.add(self.posi,PVector.mult(self.L,i+1))
            h = map(i,0,self.n,0,1)
            P = part(xyi,xyf,h,sw)
            self.p.append(P)
    
    def show(self):
        for i in xrange(len(self.p)):
            self.p[i].show()
    
    def update(self):
        for i in xrange(len(self.p)):
            if i != 0:
                    nxy = self.p[i-1].foff
            else:
                nxy = self.p[len(self.p)-1].foff
            self.p[i].update(nxy)

######
######
def hloop(h):
    if not(0<=h<1): return h - floor(h)
    else: return h

def nice(x,y):
    xp = 1.*x/wd
    yp = 1.*y/ht
    h00 = noise(x*nS,y*nS)
    h01 = noise(x*nS,(y+ht)*nS)
    h10 = noise((x+wd)*nS,y*nS)
    h11 = noise((x+wd)*nS,(y+ht)*nS)
    h = xp*yp*h00 + xp*(1-yp)*h01 + \
        (1-xp)*yp*h10 + (1-xp)*(1-yp)*h11
    return h

def keyPressed():
    if key == 'f': saver.onClick()