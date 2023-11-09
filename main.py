import pygame
from node import Node
from a_star import aStar
from dijkstra import dijkstra
from timeit import timeit

pygame.init()

HEIGHT, WIDTH = 900, 900
window = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("Pathfinding visualizer")

GREY = (128, 128, 128)


def algorithm(draw, grid, start, end):
    aStar(draw, grid, start, end)
    # dijkstra(draw, grid, start, end)


def buildGrid(row, width):

    grid = []
    node_width = width // row
    for i in range(row):
        grid.append([])
        for j in range(row):
            grid[i].append(Node(i, j, node_width, row))
    return grid


def drawGridLines(window, rows, width):
    gap=width//rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))
        pygame.draw.line(window, GREY, (i * gap, 0), (i * gap, width))
        


def draw(window, grid, rows, width):
    for row in grid:
        for node in row:
            node.draw(window)
    drawGridLines(window, rows, width)
    pygame.display.update()


def getClickedPosition(position, rows, width):
    gap = width // rows
    x, y = position
    row, column = x // gap, y // gap
    return (row, column)
def cg(window):
    count=0
    for y in range(window.get_height()):
        for x in range(window.get_width()):
            if window.get_at((x,y))==(128, 0, 128):
                count +=1
    return count
    
def main(window, WIDTH):
    ROWS = 90
    grid = buildGrid(ROWS, WIDTH)

    start, end = None, None
    started = False
    run = True

    started = False
    while run:
        draw(window, grid, ROWS, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, column = getClickedPosition(position, ROWS, WIDTH)
                node = grid[row][column]
                if not start and node != end:
                    start = node
                    start.makeStartNode()
                elif not end and node != start:
                    end = node
                    end.makeEndNode()
                elif node != start and node != end:
                    node.makeObstacle()

            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, column = getClickedPosition(position, ROWS, WIDTH)
                node = grid[row][column]
                node.resetNode()
                if node == start:
                    start = None
                if node == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    started = True
                    for row in grid:
                        for node in row:
                            node.updateNeighbors(grid)
                            ti = timeit(lambda: node.updateNeighbors(grid),number=1)
                    print('Execution time :',ti) 
                    algorithm(lambda: draw(window, grid, ROWS, WIDTH), grid, start, end)
                    gg=cg(window)
                    print("Shortest Distance From Start To end is:%d Grids"%((gg/81)-1))
                    started = False
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = buildGrid(ROWS, WIDTH)
                    draw(window, grid, ROWS, WIDTH)
    
    pygame.quit()


main(window, WIDTH)
