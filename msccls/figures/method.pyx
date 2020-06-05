from pyx import *
from pyx.connector import arc, curve
import sys

unit.set(uscale=3)

c = canvas.canvas()

textattrs = [text.halign.center, text.vshift.middlezero]
E = text.text(-2, -0.5, r"""\bf Initial interviews""", textattrs)
D = text.text(0,-0.5, r"\bf Interface (re-)implementation", textattrs)
C = text.text(1,-1, r"\bf Run live user tests", textattrs)
B = text.text(0,-1.5, r"\bf Gather and process data", textattrs)
A = text.text(-1,-1, r"\bf Identifying Improvements", textattrs)

for X in [A, B, C, D, E]:
    c.draw(X.bbox().enlarged(0.1).path(),
        [deco.stroked()])
    c.insert(X)

for X,Y in [[A, B], [B, C], [C, D], [D, A]]:
    c.stroke(arc(Y, X, boxdists=[0.18, 0.18]), [color.rgb.black, deco.earrow.normal])

c.stroke(arc(E, D, boxdists=[0.15,0.15], relangle=0), [color.rgb.black, deco.earrow.normal])
#c.stroke(curve(D, B, boxdists=[0.2, 0.2], relangle1=-45, relangle2=-45, relbulge=0.8),
#         [color.rgb.blue, deco.earrow.normal])

c.writePDFfile(sys.argv[1])
