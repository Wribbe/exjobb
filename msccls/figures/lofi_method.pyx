from pyx import *
from pyx.connector import arc, curve
import sys

unit.set(uscale=2)

c = canvas.canvas()

textattrs = [text.halign.center, text.vshift.middlezero]
E = text.text(0, 5/2, r"""\bf Recoding Information \& Consent""", textattrs)
D = text.text(0, 4/2, r"\bf Prototype Ranking I", textattrs)
C = text.text(0, 3/2, r"\bf ISO Keyword Ranking", textattrs)
B = text.text(0, 2/2, r"\bf Prototype Ranking II", textattrs)

for X in [B, C, D, E]:
    c.draw(X.bbox().enlarged(0.05).path(),
        [deco.stroked()])
    c.insert(X)

for X,Y in [[B, C], [C, D], [D, E]]:
    c.stroke(arc(Y, X, boxdists=[0.10, 0.10], relangle=0), [color.rgb.black, deco.earrow.normal])

#c.stroke(arc(E, D, boxdists=[0.15,0.15], relangle=0), [color.rgb.black, deco.earrow.normal])
##c.stroke(curve(D, B, boxdists=[0.2, 0.2], relangle1=-45, relangle2=-45, relbulge=0.8),
#         [color.rgb.blue, deco.earrow.normal])

c.writePDFfile(sys.argv[1])
