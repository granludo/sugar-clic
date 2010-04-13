"""
 
  @author Francesc Busquets (fbusquets@xtec.net)
  @version 1.0
"""

from Shaper import *

class Rectangular(Shaper):
    
    def __init__(self, nx, ny):
        super(Rectangular, self).__init__(nx, ny)
    
    def rectangularShapes(self):
        return True
        
    def buildShapes(self):
        r = c = 0
        w = self.WIDTH/self.nCols
        h = self.HEIGHT/self.nRows
        x = y = 0
        for r in range(self.nRows):
            for c in range(self.nCols):
                sh = self.shapeData[r*self.nCols+c]
                x=c*w 
                y=r*h
                sh.moveTo(x, y)
                sh.lineTo(x+w, y)
                sh.lineTo(x+w, y+h)
                sh.lineTo(x, y+h)
                sh.lineTo(x, y)
                sh.closePath();
        self.initiated = True