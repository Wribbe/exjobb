from pyx import *
from pyx.connector import arc, curve, twolines, line
import sys

unit.set(uscale=2)

c = canvas.canvas()

textattrs = [text.halign.center, text.vshift.middlezero]
#E = text.text(-1*2.5, -1*0.5, r"""\bf Information and consent""", textattrs)
#D = text.text(-0.3, -1*0.5, r"\bf Pre-survey", textattrs)
#C = text.text(1*1.4, -1*0.5, r"\bf Task-run \#1", textattrs)
#F = text.text(1*1.4, -2*0.5, r"\bf Task-run \#2", textattrs)
#G = text.text(-0.3, -2*0.5, r"\bf Task-run \#3", textattrs)
#H = text.text(-1*2.0, -2*0.5, r"\bf Task-run \#4", textattrs)
#J = text.text(-1*2.0, -3*0.5, r"\bf Task-run \#5..n", textattrs)
#K = text.text(-0.3, -3*0.5, r"\bf Post-survey", textattrs)

L = text.text(3.3, -0.9*0.5, r"\bf Task-Selection", textattrs)
M = text.text(3.3, -2*0.5, r"\bf Task-Info", textattrs)
N = text.text(3.3, -3.1*0.5, r"\bf Task-Execution", textattrs)

#c.stroke(
#  path.circle(0, 0, 0.1),
#  [
#    style.linestyle.dashed,
#    deco.earrow(),
#    trafo.rotate(210),
#    trafo.translate(-2.82, -1.51)
#  ]
#)

#for X in [C, D, E, F, G, H, J, K, L, M, N]:
for X in [L, M, N]:
    c.draw(X.bbox().enlarged(0.05).path(),
        [deco.stroked()])
    c.insert(X)

links = [
  [M, L],
  [N, M],
]

for X,Y in links:
    c.stroke(arc(Y, X, boxdists=[0.10, 0.10], relangle=0), [color.rgb.black, deco.earrow.normal])

c.stroke(
  path.curve(
    3.3-0.75, -3.1*0.5,
    3.3-1.4, -3.1*0.5,
    3.3-1.4, -0.9*0.5,
    3.3-0.7, -0.9*0.5
  ),
  [
    color.rgb.black,
    deco.earrow.normal
  ]
)
#c.stroke(arc(E, D, boxdists=[0.15,0.15], relangle=0), [color.rgb.black, deco.earrow.normal])
##c.stroke(curve(D, B, boxdists=[0.2, 0.2], relangle1=-45, relangle2=-45, relbulge=0.8),
#         [color.rgb.blue, deco.earrow.normal])

#E = text.text(2*2.5/2, -1*0.6-1*0.1, r"""\bf Initial Consent \& Information""", textattrs)
#D = text.text(2*2.5/2, -2*0.6-1*0.1, r"\bf Pre-survey complete", textattrs)
#C = text.text(2*2.5/2, -3*0.6-1*0.1, r"\bf Post-survey complete", textattrs)

#for X in [C, D, E]:
#    c.draw(X.bbox().enlarged(0.05).path(),
#        [deco.stroked()])
#    c.insert(X)
#
#for X,Y in [[C, D], [D, E]]:
#    c.stroke(arc(Y, X, boxdists=[0.20, 0.10], relangle=0), [color.rgb.black, deco.earrow.normal])
#

c.writePDFfile(sys.argv[1])
