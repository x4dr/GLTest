import numpy as np
from vispy import app
from vispy import gloo
from OpenGL import GL as gl

c = app.Canvas(keys='interactive')
vertex = """
    uniform float scale;
    //uniform float theta;
    attribute vec4 color;
    attribute vec2 position;
    varying vec4 v_color;
    void main()
    {
        gl_Position = vec4(position*scale, 0.0, 1.0);
        v_color = color;
    } """

fragment = """
    varying vec4 v_color;
    void main()
    {
        gl_FragColor = v_color;
    } """

tiles = 6
loffs = int(np.sqrt(tiles))
print(loffs)
linewidth = int(tiles / loffs)
hexx = []
hexy = []
program = gloo.Program(vertex, fragment)

for i in [2, 1, 3, 3, 1, 4, 1, 4, 6, 6, 4, 5]:
    hexx.append(np.sin(i / 6.0 * 2 * np.pi + (np.pi / 2)))
    hexy.append(np.cos(i / 6.0 * 2 * np.pi + (np.pi / 2)))

xcor = np.tile(hexx, tiles)
ycor = np.tile(hexy, tiles)

xcor = np.reshape(xcor, (-1, loffs, 12))
ycor = np.reshape(ycor, (-1, loffs, 12))
print(xcor)
print("\n\n\n\n\n\n\n\n\n")

for line in range(len(xcor)):
    for hexf in range(len(xcor[line])):
        for i in range(len(xcor[line][hexf])):
            xcor[line][hexf][i] += hexf

print(xcor)
print("\n\n\n\n\n\n\n\n\n")

for line in range(len(ycor)):
    for hexf in range(len(ycor[line])):
        for i in range(len(ycor[line][hexf])):
            ycor[line][hexf][i] += hexf


yloffs = np.repeat(np.arange(loffs), 12 + linewidth * 12)
yloffs = yloffs * 2 * np.sin(np.pi / 3)
yloffs = np.split(yloffs, [12 * tiles])[0]

yoffs = np.append(np.zeros(12), np.ones(12)) * np.sin(np.pi / 3)
yoffs = np.tile(yoffs, int(1 + tiles / 2))
yoffs = np.split(yoffs, [12 * tiles])[0]
# yoffs = yoffs * alternate
yoffs = np.add(yoffs, yloffs)

xoffs = np.tile(np.repeat(np.arange(1 + linewidth), 12), loffs)
xoffs = np.add(xoffs, 0.5 - np.sqrt(tiles / 2.0))
xoffs = np.split(xoffs, [12 * tiles])[0]

xcor = np.add(xoffs * 1.5, xcor)
ycor = np.add(yoffs, ycor + 0.5 - np.sqrt(tiles / 2.0))
program['position'] = np.c_[
    np.array(xcor),
    np.array(ycor)].astype(np.float32)

r = np.arange(0, 1, (1 / 12))
g = np.arange(0, 1, (1 / 12))
b = np.arange(0, 1, (1 / 12))

r = np.repeat(r, tiles)
g = np.repeat(g, tiles)
b = np.repeat(b, tiles)

program['color'] = np.c_[
    r,
    g,
    b,
    np.tile([1.0], 12 * tiles)].astype(np.float32)
program['scale'] = 0.2


@c.connect
def on_resize(event):
    (width, height) = event.size
    if width > height:
        x = (width - height) / 2
        y = 0
        w = h = height
    else:
        x = 0
        y = (height - width) / 2
        w = h = width
    gloo.set_viewport(x, y, w, h)
    gloo.set_viewport(0, 0, *event.size)


@c.connect
def on_draw(event):
    gloo.clear((1, 1, 1, 1))
    program.draw(gl.GL_TRIANGLES)


clock = 0

# t = app.Timer(connect=tick, start=True, interval=(1/60), iterations=-1)


c.show()
app.run();
