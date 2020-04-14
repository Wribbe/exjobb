from pyx import *
from pyx.connector import arc, curve, twolines, line
import sys

unit.set(uscale=2)

c = canvas.canvas()

textattrs = [text.halign.center, text.vshift.middlezero]
E = text.text(0*2.5, 0, r"""\bf Application deployed""", textattrs)
D = text.text(1*2.5, 0, r"\bf Link Shared on Facebook", textattrs)
C = text.text(2*2.5, 0, r"\bf Link Shared at Massive", textattrs)

for X in [C, D, E]:
    c.draw(X.bbox().enlarged(0.05).path(),
        [deco.stroked()])
    c.insert(X)

for X,Y in [[C, D], [D, E]]:
    c.stroke(arc(Y, X, boxdists=[0.10, 0.10], relangle=0), [color.rgb.black, deco.earrow.normal])

#c.stroke(arc(E, D, boxdists=[0.15,0.15], relangle=0), [color.rgb.black, deco.earrow.normal])
##c.stroke(curve(D, B, boxdists=[0.2, 0.2], relangle1=-45, relangle2=-45, relbulge=0.8),
#         [color.rgb.blue, deco.earrow.normal])

E = text.text(2*2.5/2, -1*0.6-1*0.1, r"""\bf Initial Consent \& Information""", textattrs)
D = text.text(2*2.5/2, -2*0.6-1*0.1, r"\bf Pre-survey complete", textattrs)
C = text.text(2*2.5/2, -3*0.6-1*0.1, r"\bf Post-survey complete", textattrs)

for X in [C, D, E]:
    c.draw(X.bbox().enlarged(0.05).path(),
        [deco.stroked()])
    c.insert(X)

for X,Y in [[C, D], [D, E]]:
    c.stroke(arc(Y, X, boxdists=[0.20, 0.10], relangle=0), [color.rgb.black, deco.earrow.normal])


c.writePDFfile(sys.argv[1])
