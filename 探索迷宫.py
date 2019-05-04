#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import turtle
import time

PART_OF_PATH = '路径的一部分'
TRIED = '已经搜索过'
OBSTACLE = '+'
DEAD_PATH = '死路'


class Maze():
    def __init__(self):
        self.mazelist = []
        row = 0
        for i in open('迷宫示例数据.txt', 'r'):
            col = 0
            for j in i:
                if j == 's':
                    self.start_row = row
                    self.start_col = col
                col += 1
            row += 1
            self.mazelist.append(list(i))
            self.col = len(i)
        self.row = row
        self.t = turtle.Turtle(shape='turtle')
        turtle.setup(600, 600)
        # 建立坐标系 例如,10行10列,则左下角坐标为-5,-5,右上角坐标为5,5,刚好有10*10个大小为1*1的方块
        turtle.setworldcoordinates(
            -(self.col-1)/2-0.5,
            -(self.row-1)/2-0.5,
            (self.col-1)/2+0.5,
            (self.row-1)/2+0.5
        )

    def draw_maze(self):
        for y in range(self.row):
            for x in range(self.col):
                if self.mazelist[y][x] == '+':
                    self.draw_centerbox(x-self.col/2+0.5,
                                        -y+self.row/2-0.5,
                                        'tan')
        self.t.color('black', 'blue')

    def draw_centerbox(self, x, y, color):
        turtle.tracer(False)
        self.t.up()
        self.t.goto(x-0.5, y+0.5)
        self.t.color('black', color)
        self.t.setheading(-90)
        self.t.down()
        self.t.begin_fill()
        for i in range(4):
            self.t.forward(1)
            self.t.left(90)
        self.t.end_fill()
        turtle.update()  # 不用update()也行,不知道有何意义
        turtle.tracer(True)

    def move(self, x, y):
        self.t.up()
        # setheading乌龟转向,该语句没有不影响结果
        self.t.setheading(self.t.towards(x-self.col/2+0.5, -y+self.row/2-0.5))
        self.t.goto(x-self.col/2+0.5, -y+self.row/2-0.5)

    def flag(self, color):
        self.t.dot(color)

    def update_position(self, row, col, val=None):
        if val:
            self.mazelist[row][col] = val
        self.move(col, row)
        if val == PART_OF_PATH:
            color = 'green'
        elif val == OBSTACLE:
            color = 'red'
        elif val == TRIED:
            color = 'black'
        elif val == DEAD_PATH:
            color = 'red'
        else:
            color = None
        if color:
            self.flag(color)

    def isexit(self, row, col):
        return (row == 0 or
                row == self.row-1 or
                col == 0 or
                col == self.col-1)

    def __getitem__(self, index):
        return self.mazelist[index]

def search_maze(maze, startrow, startcol):
    maze.update_position(startrow, startcol)
    # case1: 遇到墙壁
    if maze[startrow][startcol] == OBSTACLE:
        return False
    # case2: 已经搜索过
    if maze[startrow][startcol] == TRIED:
        return False
    # case3 成功找到出口
    if maze.isexit(startrow, startcol):
        maze.update_position(startrow, startcol, PART_OF_PATH)
        return True
    maze.update_position(startrow, startcol, TRIED)

    found = search_maze(maze, startrow-1, startcol) or \
            search_maze(maze, startrow+1, startcol) or \
            search_maze(maze, startrow, startcol+1) or \
            search_maze(maze, startrow, startcol-1)
    if found:
        maze.update_position(startrow, startcol, PART_OF_PATH)
    else:
        maze.update_position(startrow, startcol, DEAD_PATH)
    return found

if __name__ == '__main__':
    maze = Maze()
    maze.draw_maze()
    search_maze(maze, maze.start_row, maze.start_col)
    turtle.done()
