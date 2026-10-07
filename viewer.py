import glob
import os
import sys

import numpy as np
import pygame


from TSPWorld import TspWorld
from GeneticAlgo import TSPGA
from RandomGen import RandomGen             # <- your random search file
from Baseline import nearestNeighbour, computeDistance, nnTwoOpt, twoOpt
from config import GAConfigs                 # your config class (popSize, generations, ...)

OPTIMA = {'eil51': 426, 'eil76': 538, 'eil101': 629}   # verify against TSPLIB
WIDTH, HEIGHT = 1500, 720      # two panels side by side
PANEL = WIDTH // 2
MARGIN = 40            # empty border around the cities
TOP = 80               # room for the text at the top
SHOW_EVERY = 1000      # GA: redraw the best tour every this many generations


def findOptimalFile(name):
    # optimal tours live in data/optimal/ and are named after the instance, e.g. data/optimal/eil51.opt.tour
    matches = sorted(glob.glob(os.path.join('data', 'optimal', name + '.*')))
    return matches[0] if matches else None


def loadOptimalTour(name, numCities):
    path = findOptimalFile(name)
    if path is None:
        return None
    with open(path) as fl:
        lines = [line.strip() for line in fl]
    start = 0                                              # TSPLIB files: numbers start after TOUR_SECTION
    for i, line in enumerate(lines):
        if line.startswith('TOUR_SECTION'):
            start = i + 1
            break
    tour, done = [], False
    for line in lines[start:]:
        for part in line.split():
            if part == '-1':                               # -1 marks the end of the list
                done = True
                break
            if part.isdigit():                             # skips header words like NAME / TYPE
                tour.append(int(part) - 1)                 # our cities start at 0, the file's at 1
        if done:
            break
    if sorted(tour) != list(range(numCities)):             # wrong length or repeated cities: do not trust it
        print(f'{path}: not a valid tour for {numCities} cities, ignoring it')
        return None
    return np.array(tour)


def edgeSet(tour):
    # every leg of the closed tour as a sorted pair, so (3,7) and (7,3) count as the same edge
    n = len(tour)
    return {tuple(sorted((int(tour[i]), int(tour[(i + 1) % n])))) for i in range(n)}


class ViewLogger:
    """Looks like your Logger to the GA, but it draws the best tour instead of saving rows."""

    def __init__(self, viewer, every, generations, label='GA'):
        self.viewer = viewer
        self.every = every
        self.generations = generations
        self.label = label                                     # 'GA' or 'Random', shown in the title

    def record(self, gen, numEvals, population, distances, bestDistance, bestTour):
        if gen % self.every == 0 or gen == self.generations - 1:
            self.viewer.show(bestTour, f'{self.label}  gen {gen}/{self.generations}  evals {numEvals}')
        self.viewer.checkQuit()                                # keeps the window responsive


class Viewer:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('TSP viewer')
        self.font = pygame.font.SysFont(None, 26)
        self.problem = None

    def checkQuit(self):
        for event in pygame.event.get():                       # also lets the OS see we are alive
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def waitForKey(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    return

    def loadProblem(self, path):
        name = os.path.basename(path).replace('.tsp', '')
        self.optimum = OPTIMA.get(name, 0)                     # 0 = unknown, then no gap is shown
        self.problem = TspWorld(path, self.optimum)
        self.name = name
        coords = np.array(self.problem.cordinates)
        self.minX, self.minY = coords.min(axis=0)
        spanX = max(coords[:, 0].max() - self.minX, 1e-9)
        spanY = max(coords[:, 1].max() - self.minY, 1e-9)
        # ONE scale for both axes so the map is not stretched
        self.scale = min((PANEL - 2 * MARGIN) / spanX, (HEIGHT - TOP - MARGIN) / spanY)
        self.coords = coords
        self.optTour = loadOptimalTour(name, self.problem.numCities)   # None if no file in data/optimal/
        if self.optTour is not None:
            self.optEdges = edgeSet(self.optTour)
            self.optLen = computeDistance(self.optTour, self.problem.distanceMatrix)

    def toScreen(self, city, left):
        x, y = self.coords[city]                           # left = x pixel where this panel starts
        return (int(left + MARGIN + (x - self.minX) * self.scale),
                int(TOP + (y - self.minY) * self.scale))

    def text(self, message, x, y):
        self.screen.blit(self.font.render(message, True, (255, 255, 255)), (x, y))

    def drawPanel(self, tour, left, edgeColour, otherEdges=None):
        # draw one tour inside the panel that starts at x = left
        n = len(tour)
        points = [self.toScreen(c, left) for c in tour]
        for i in range(n):
            colour = edgeColour
            if otherEdges is not None:                     # found tour: green if the ideal tour uses this edge too
                key = tuple(sorted((int(tour[i]), int(tour[(i + 1) % n]))))
                colour = (80, 200, 120) if key in otherEdges else (230, 80, 80)
            pygame.draw.line(self.screen, colour, points[i], points[(i + 1) % n], 1)   # (i+1)%n closes the loop
        for p in points:
            pygame.draw.circle(self.screen, (240, 240, 240), p, 3)

    def show(self, tour, title):
        # recompute the length ourselves, closed tour, so every mode is measured the same way
        length = computeDistance(tour, self.problem.distanceMatrix)
        self.screen.fill((20, 20, 30))
        hasOpt = self.optTour is not None

        # ---- left panel: the tour found by the chosen method ----
        line2 = f'{self.name}  {self.problem.numCities} cities  length {length:.0f}'
        if hasOpt:
            line2 += f'  gap {100 * (length - self.optLen) / self.optLen:.1f}%'
        elif self.optimum > 0:
            line2 += f'  gap {100 * (length - self.optimum) / self.optimum:.1f}% (best known {self.optimum})'
        self.text(title, 10, 10)
        self.text(line2, 10, 40)
        self.drawPanel(tour, 0, (80, 200, 120), self.optEdges if hasOpt else None)

        # ---- right panel: the ideal tour from the TSPLIB file ----
        pygame.draw.line(self.screen, (90, 90, 110), (PANEL, 0), (PANEL, HEIGHT), 2)
        if hasOpt:
            shared = len(edgeSet(tour) & self.optEdges)
            self.text('Ideal tour (from data/optimal)', PANEL + 10, 10)
            self.text(f'length {self.optLen:.0f}   edges shared with found tour: {shared}/{len(tour)}', PANEL + 10, 40)
            self.drawPanel(self.optTour, PANEL, (90, 160, 240))
        else:
            self.text(f'No file for {self.name} in data/optimal/ - nothing to compare with', PANEL + 10, 10)
        pygame.display.flip()

    def runGA(self):
        config = GAConfigs()
        logger = ViewLogger(self, SHOW_EVERY, config.generations)
        tour, length, history = TSPGA(self.problem, config, 0, logger).run()
        self.show(tour, 'GA finished (press a key)')

    def runRandom(self):
        config = GAConfigs()
        logger = ViewLogger(self, SHOW_EVERY, config.generations, 'Random search')
        tour, length, history = RandomGen(self.problem, config, 0, logger).run()
        self.show(tour, 'Random search finished (press a key)')

    def runNN(self):
        # try every start city and keep the shortest tour
        bestTour, bestLen = None, float('inf')
        for start in range(self.problem.numCities):
            tour, length = nearestNeighbour(self.problem.distanceMatrix, start)
            if length < bestLen:
                bestTour, bestLen = tour, length
        self.show(bestTour, 'Nearest neighbour, best of all start cities (press a key)')

    def runTwoOpt(self):
        tour, length = nearestNeighbour(self.problem.distanceMatrix, 0)    # your nearest neighbour ...
        tour, length = nnTwoOpt(self.problem.distanceMatrix, tour)         # ... improved by your 2-opt
        self.show(tour, 'NN + 2-opt (press a key)')

    def runPlainTwoOpt(self):
        # your twoOpt builds its own random starting tour from the rng, then improves it
        self.screen.fill((20, 20, 30))
        self.text('Running 2-opt from a random tour...', 10, 10)    # it takes a few seconds on 100 cities
        pygame.display.flip()
        rng = np.random.default_rng(0)
        tour, length = twoOpt(self.problem.distanceMatrix, rng)
        self.show(tour, '2-opt from a random tour (press a key)')

    def menu(self, files, chosen):
        self.screen.fill((20, 20, 30))
        self.text('Pick an instance with UP / DOWN, then a method:', 10, 10)
        self.text('G = GA   R = random search   N = nearest neighbour   T = NN + 2-opt   O = 2-opt alone   ESC = quit', 10, 40)
        for i, f in enumerate(files):
            marker = '> ' if i == chosen else '  '
            self.text(marker + os.path.basename(f), 30, 90 + 30 * i)
        pygame.display.flip()

    def loop(self):
        files = sorted(glob.glob('data/*.tsp'))
        if not files:
            print('no .tsp files found in data/')
            return
        chosen = 0
        while True:
            self.menu(files, chosen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type != pygame.KEYDOWN:
                    continue
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_UP:
                    chosen = (chosen - 1) % len(files)
                elif event.key == pygame.K_DOWN:
                    chosen = (chosen + 1) % len(files)
                elif event.key in (pygame.K_g, pygame.K_r, pygame.K_n, pygame.K_t, pygame.K_o):
                    self.loadProblem(files[chosen])
                    if event.key == pygame.K_g:
                        self.runGA()
                    elif event.key == pygame.K_r:
                        self.runRandom()
                    elif event.key == pygame.K_n:
                        self.runNN()
                    elif event.key == pygame.K_o:
                        self.runPlainTwoOpt()
                    else:
                        self.runTwoOpt()
                    self.waitForKey()                          # look at the result, then back to the menu


if __name__ == '__main__':
    Viewer().loop()
    pygame.quit()