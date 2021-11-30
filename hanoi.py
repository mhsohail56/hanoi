import imageio
import imgkit
import os
import shutil
from PIL import Image


class Disk:

    def __init__(self, size: int) -> None:
        self.size = size


class Tower:

    def __init__(self, disks: list[Disk]) -> None:
        self.disks = disks


class Game:

    def __init__(self, n: int) -> None:

        self.n = n
        self.towers = []
        self.states = []

        initial_stack = []
        for i in range(n, 0, -1):
            initial_stack.append(Disk(i))

        self.towers.append(Tower(initial_stack))
        self.towers.append(Tower([]))
        self.towers.append(Tower([]))

    def solve(self, n: int, start: Tower, finish: Tower, other: Tower) -> None:

        if n == 1:
            finish.disks.append(start.disks.pop())
            self.print_towers()
            return

        self.solve(n - 1, start, other, finish)
        self.solve(1, start, finish, other)
        self.solve(n - 1, other, finish, start)
        self.print_towers()

        if n == self.n:
            images = []
            filenames = [f"temp/cropped/{f}" for f in os.listdir("temp/cropped") if f[-4:] == ".jpg"]

            for filename in sorted(filenames, key=lambda s: int(s[13:-4])):
                images.append(imageio.imread(filename))

            imageio.mimsave(f'out/solution_{n}.gif', images, fps=2)

    def print_towers(self) -> None:

        state = {i: [disk.size for disk in self.towers[i].disks] for i in range(0, 3)}

        if state in self.states:
            return

        self.states.append(state)

        html_string = '<!DOCTYPE html>\n\n<html><head></head><body>\n\n<svg width="720" height="480" style="fill:rgb(' \
                      '0,0,0)">\n\t<rect width="720" height="480" style="fill:white;stroke:rgb(0,0,' \
                      '0);stroke-width:5"></rect>\n\t<rect x="125" y="90" width="10" height="300" rx="10" ' \
                      'style="fill:rgb(0,0,0)"></rect>\n\t<rect x="355" y="90" width="10" height="300" rx="10" ' \
                      'style="fill:rgb(0,0,0)"></rect>\n\t<rect x="585" y="90" width="10" height="300" rx="10" ' \
                      'style="fill:rgb(0,0,0)"></rect>'

        rect = ["<rect ", "></rect>"]

        for i, tower in enumerate(self.towers):

            for j, disk in enumerate(tower.disks):
                rect_style = f'x="{(130 + i * 230) - (200 - (self.n - disk.size) * (120 / (self.n - 1))) / 2}" y="{375 - 30 * j}" width="{200 - (self.n - disk.size) * (120 / (self.n - 1))}" height="30" ry="20" style="fill:rgb(0,0,0)"'
                html_string += "\n\t" + rect_style.join(rect)

        html_string += '\n</svg>\n\n</body></html>'

        fobj = open("temp/state.html", "w")
        fobj.write(html_string)
        fobj.close()

        imgkit.from_file("temp/state.html", f'temp/uncropped/{len(self.states)}.jpg')
        os.remove("temp/state.html")

        im = Image.open(f'temp/uncropped/{len(self.states)}.jpg')
        im.crop((10, 10, 720, 480)).save(f'temp/cropped/{len(self.states)}.jpg')
        im.close()


def solution(n: int) -> None:
    if not os.path.exists("temp"):
        os.mkdir("temp")
    if not os.path.exists("temp/cropped"):
        os.mkdir("temp/cropped")
    if not os.path.exists("temp/uncropped"):
        os.mkdir("temp/uncropped")
    if not os.path.exists("out"):
        os.mkdir("out")

    game = Game(n)
    game.print_towers()
    game.solve(game.n, game.towers[0], game.towers[1], game.towers[2])

    shutil.rmtree("temp")


if __name__ == "__main__":
    n = int(input("Select you number of disks (note, this program only works feasibly for up to 7 disks): "))
    solution(n)
    print(f"Check out/solution_{n}.gif for your solution!")
