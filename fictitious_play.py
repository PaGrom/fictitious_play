# -*- coding: utf-8 -*-

from __future__ import division

import csv

class Gamer:
    def __init__(self, number, matr, strg_num):
        self.strg_num = strg_num
        if number == 2:
            self.strategy = zip(*matr)
        else:
            self.strategy = matr
        

class Game:
    def __init__(self, matr, first_gamer = 1, first_strategy = 1, delta = 0.1):
        self.matr = matr
        self.first_gamer = first_gamer - 1
        self.first_strategy = first_strategy - 1
        self.table = []
        self.delta = delta
        self.count = 0
        self.p = [0] * 3
        self.q = [0] * 3
        self.v = 0

        self.gamers = [Gamer(1, self.matr, 0), Gamer(2, self.matr, 1)]

        if self.first_gamer == 1:
            self.gamers.reverse()

    def start(self):
        self.table.append([0] * 14)
        self.count += 1
        self.table[-1][0] = self.count # номер итерации
        self.table[-1][1] = self.first_strategy + 1 # стратегия первого игрока
        
        for i, item in enumerate(self.gamers[0].strategy[self.first_strategy]): # записываем стратегию первого игрока в таблицу
            self.table[-1][2 + i] = item

        self.table[-1][5] = min(self.table[-1][2:5]) / self.count
        # print "Min: ", min(self.table[-1][2:5])
        self.table[-1][6] = self.gamers[1].strg_num + 1 # стратегия второго игрока TODO

        for i, item in enumerate(self.gamers[1].strategy[self.gamers[1].strg_num]): # записываем стратегию второго игрока в таблицу
            self.table[-1][7 + i] = item

        self.table[-1][10] = max(self.table[-1][7:10]) / self.count # максимальный выигрыш второго игрока
        # print "Max: ", max(self.table[-1][7:10])
        self.table[-1][11] = self.table[-1][10]

        self.table[-1][12] = self.table[-1][5]

        self.table[-1][13] = abs(self.table[-1][11] - self.table[-1][12])

        if self.table[-1][1] == 1:
            self.p[0] += 1
        elif self.table[-1][1] == 2:
            self.p[1] += 1
        elif self.table[-1][1] == 3:
            self.p[2] += 1

        if self.table[-1][6] == 1:
            self.q[0] += 1
        elif self.table[-1][6] == 2:
            self.q[1] += 1
        elif self.table[-1][6] == 3:
            self.q[2] += 1

        while self.table[-1][13] > self.delta:
            self.table.append([0] * 14)
            self.count += 1
            self.table[-1][0] = self.count # номер итерации
            # print "Max: ", max(self.table[-2][7:10])
            self.gamers[0].strg_num = self.table[-2][7:10].index(max(self.table[-2][7:10]))
            # print "gamers[0].strg_num", self.gamers[0].strg_num
            self.table[-1][1] = self.gamers[0].strg_num + 1

            for i, item in enumerate(self.gamers[0].strategy[self.gamers[0].strg_num]): # записываем стратегию первого игрока в таблицу
                self.table[-1][2 + i] = self.table[-2][2 + i] + item

            self.table[-1][5] = min(self.table[-1][2:5]) / self.count
            # print "Min: ", min(self.table[-1][2:5])
            self.gamers[1].strg_num = self.table[-1][2:5].index(min(self.table[-1][2:5]))

            self.table[-1][6] = self.gamers[1].strg_num + 1

            for i, item in enumerate(self.gamers[1].strategy[self.gamers[1].strg_num]): # записываем стратегию второго игрока в таблицу
                self.table[-1][7 + i] = self.table[-2][7 + i] + item

            self.table[-1][10] = max(self.table[-1][7:10]) / self.count # максимальный выигрыш второго игрока

            if self.table[-1][10] < self.table[-2][11]: 
                self.table[-1][11] = self.table[-1][10]
            else:
                self.table[-1][11] = self.table[-2][11]

            if self.table[-1][5] > self.table[-2][12]: 
                self.table[-1][12] = self.table[-1][5]
            else:
                self.table[-1][12] = self.table[-2][12]

            self.table[-1][13] = abs(self.table[-1][11] - self.table[-1][12])
            # print self.table[-1][13]

            if self.table[-1][1] == 1:
                self.p[0] += 1
            elif self.table[-1][1] == 2:
                self.p[1] += 1
            elif self.table[-1][1] == 3:
                self.p[2] += 1

            if self.table[-1][6] == 1:
                self.q[0] += 1
            elif self.table[-1][6] == 2:
                self.q[1] += 1
            elif self.table[-1][6] == 3:
                self.q[2] += 1

        self.v = (self.table[-1][11] + self.table[-1][12]) / 2

        
    def result(self):
        return self.table

def main():

    example = [[31,97,45],
               [78,67,69],
               [86,69,52]]

    game = Game(example, first_gamer = 1, first_strategy = 1, delta = 0.1)

    game.start()

    myfile = open("out.csv", 'wb')
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for i in game.result():
        wr.writerow(i)

    print
    print "Сыграно партий: ", game.count
    print
    for i, item in enumerate(game.p):
        print "1-ый игрок играл", i + 1 ,"-й стратегией", item, "раз" 
        print "Частота ее использования р*", i + 1, "=", item / game.count
    print
    for i, item in enumerate(game.q):
        print "2-ой игрок играл", i + 1 ,"-й стратегией", item, "раз" 
        print "Частота ее использования q*", i + 1, "=", item / game.count
    print
    print "Цена игры:", game.v

if __name__ == '__main__':
    main()
