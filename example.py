#!/usr/bin/env python3

from vispy import app, gloo
from dataclasses import dataclass
import numpy as np
import decimal


decimal.getcontext().prec = 50
EPSILON = decimal.Decimal(1e-12)


@dataclass
class particle:
    pos: np.array([decimal.Decimal(0.), decimal.Decimal(0.)])
    speed: np.array([decimal.Decimal(0.), decimal.Decimal(0.)])
    charge: decimal.Decimal = decimal.Decimal(0.)
    mass: decimal.Decimal = decimal.Decimal(0.)
    active: bool = False
    fixed: bool = False


parts = []
for i in range(10):
    parts.append(particle(0, 0, 0))


parts[0].pos = np.array([decimal.Decimal(0.), decimal.Decimal(1.)])
parts[0].speed = np.array([decimal.Decimal(0.00005), decimal.Decimal(0.)])
parts[0].charge = decimal.Decimal(1e-11)
parts[0].mass = decimal.Decimal(1e-3)
parts[0].active = True

parts[1].pos = np.array([decimal.Decimal(0.), decimal.Decimal(0.)])
parts[1].speed = np.array([decimal.Decimal(0.), decimal.Decimal(0.)])
parts[1].charge = decimal.Decimal(-3e-11)
parts[1].active = True
parts[1].mass = decimal.Decimal(10)
parts[1].fixed = True

parts[2].pos = np.array([decimal.Decimal(2.), decimal.Decimal(0.)])
parts[2].speed = np.array([decimal.Decimal(0.), decimal.Decimal(0.)])
parts[2].charge = decimal.Decimal(-3e-11)
parts[2].active = True
parts[2].mass = decimal.Decimal(10)
parts[2].fixed = True


class Canvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self, position=(300, 100), size=(1800, 1800), keys='interactive')

        self.program = gloo.Program(open('kek.vert', 'r').read(), open('kek.frag', 'r').read())
        self.program['a_position'] = [(-1., -1.), (-1., +1.), (+1., -1.), (+1., +1.)]

        self.prevt = 0.0

        for i in range(10):
            if parts[i].active:
                self.program[f'px[{i}]'] = parts[i].pos[0]
                self.program[f'py[{i}]'] = parts[i].pos[1]
                self.program[f'pc[{i}]'] = parts[i].charge

        self.timer = app.Timer('auto', connect=self.on_timer, start=True)

        self.show()

    def on_timer(self, event):
        dt = decimal.Decimal((event.elapsed - self.prevt) / 0.05)
        energy = decimal.Decimal(0)
        for i in range(10):
            if(parts[i].active):
                f = np.array([decimal.Decimal(0.), decimal.Decimal(0.)])
                a = np.array([decimal.Decimal(0.), decimal.Decimal(0.)])

                for j in range(10):
                    if(i != j and parts[j].active):
                        val = decimal.Decimal(parts[i].charge * parts[j].charge * decimal.Decimal(9e9))
                        d = parts[i].pos - parts[j].pos
                        dist = np.linalg.norm(d)
                        f += val / (dist ** 2) * (d / dist)
                        energy += (decimal.Decimal(8.99e9) * parts[i].charge * parts[j].charge) / (dist * decimal.Decimal(2))

                if(not parts[i].fixed):
                    a = f / parts[i].mass
                    parts[i].speed += a * dt
                    parts[i].pos += parts[i].speed * dt

                energy += decimal.Decimal(0.5) * parts[i].mass * (parts[i].speed[0]**2 + parts[i].speed[1]**2)

                self.program[f'px[{i}]'] = parts[i].pos[0]
                self.program[f'py[{i}]'] = parts[i].pos[1]
                self.program[f'pc[{i}]'] = parts[i].charge

        print(energy)  # print total system's energy
        self.update()

    def on_resize(self, event):
        width, height = event.physical_size
        gloo.set_viewport(0, 0, width, height)

    def on_draw(self, event):
        self.program.draw('triangle_strip')


if __name__ == '__main__':
    canvas = Canvas()
    app.run()
