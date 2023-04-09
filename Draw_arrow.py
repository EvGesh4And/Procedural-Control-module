import sys
from math import acos, degrees, sqrt
from PyQt5.Qt import *

class DrawingProcess():
    def __init__(self, parent=None):
        #super().__init__(parent)
        self.parent = parent
   
        self.is_pressed = False
        self.drawingPath = None
        self.begin, self.destination = QPoint(), QPoint()
        self.drawingPath = QPainterPath()
        self.drawingPath.moveTo(self.begin)
        self.drawingPath.lineTo(self.destination)

    def draw(self, parent):
        painter = QPainter(parent)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        if self.drawingPath:
            if not self.begin.isNull() and not self.destination.isNull():
                painter.setPen(
                    QPen(
                        QColor(0, 136, 217),
                        2,
                        Qt.SolidLine,
                        Qt.RoundCap,
                        Qt.RoundJoin
                    )
                )
                painter.drawLine(self.begin, self.destination)

                l = 50
                x_right = QPointF(self.destination)

                right_triangle = QPainterPath()
                right_triangle.lineTo(-0.1 * 4 * l, 0.1 * l)
                right_triangle.lineTo(-0.1 * 4 * l, -0.1 * l)
                right_triangle.closeSubpath()
                right_triangle.translate(x_right)

                painter.setBrush(QColor(0, 136, 217))
                painter.translate(self.destination)

                x1, y1 = self.begin.x(), self.begin.y()
                x2, y2 = self.destination.x(), self.destination.y()
                a = y2 - y1
                c = x2 - x1
                b = sqrt(a**2 + c**2)

                angle = 0
                if a==0 and b==c:
                    angle = 0
                elif c==0 and -a==b:
                    angle = 90
                elif a==0 and b==-c:
                    angle = 180
                elif c==0 and a==b:
                    angle = 270
                elif a<0 and b>0:
                    angle = degrees(acos((b*b + c*c - a*a)/(2.0 * b * c)))
                else:
                    angle = 360 - degrees(acos((b*b + c*c - a*a)/(2.0 * b * c)))

                painter.rotate(-angle)
                painter.translate(-self.destination)
                painter.drawPath(right_triangle)
                    
    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     #painter.drawPixmap(QPoint(), self.image)
    #     if self.is_pressed:
    #         self.draw(self)
    #
    # def mousePressEvent(self, event):
    #     self.is_pressed = True
    #     if event.button() == Qt.LeftButton:
    #         self.drawingPath = QPainterPath()
    #         self.drawingPath.moveTo(event.pos())
    #         self.begin = event.pos()
    #         self.destination = self.begin
    #         self.update()
    #
    # def mouseMoveEvent(self, event):
    #     if event.buttons() and Qt.LeftButton and self.drawingPath:
    #         self.drawingPath.lineTo(event.pos())
    #         self.destination = event.pos()
    #         self.update()
    #
    # def mouseReleaseEvent(self, event):
    #     self.is_pressed = False
    #     self.draw(self.image)
    #     self.update()