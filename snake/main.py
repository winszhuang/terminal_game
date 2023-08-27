from typing import List
import os
import time
import keyboard
import random

# 1. 寫一個可以產生畫布的功能(函數)
# 2. 讓蛇可以在畫布上移動 (不考慮蛇會自己移動)
# 2-1 如何讓蛇顯示在畫布上
# 2-2
# 3. 自己移動(自己案上下左右去操控)
# 3-1 改變行走方向並繼續移動
# 4. 不能撞到牆壁
# 5. 隨機生成一個星星，並每次吃到改變位置
# 6. 吃到可以增加尾巴

# －－－－－－－－－－－－－－
# －－－－－－－－－－－－－－
# －－－－－－－－－－－－－－
# －－－－－－－－－－－－－－
# －－－－－－－－－－－－－－
# －－－－－－－－－－－－－－
# －－－－－－－－－－－－－－
# －－－－－－－－－－－－－－
# －－－－－－－－－－－－－－
# －－－－－－－－－－－－－－
# －－－－－－－－－－－－－－
# －－－－－－－－－－－－－－
# －－－－－－－－－－－－－－
# －－－－－－－－－－－－－－


# 元素
class Element:

    def __init__(self, x: int, y: int, symbol: str):
        self.x = x
        self.y = y
        self.symbol = symbol


# 繼承
class Star(Element):

    def __init__(self, x: int, y: int):
        super().__init__(x, y, "星 ")


# 蛇的定義
class Snake(Element):

    def __init__(self, x: int, y: int):
        super().__init__(x, y, "蛇 ")
        self.direction = "right"
        self.tailLength = 0
        self.bodyList: List[Element] = []
        self.updatePosition()

    # 增加尾巴長度
    def growLengthOfTail(self):
        self.tailLength += 1

    def getTailAllElements(self):
        return self.bodyList[0:self.tailLength]

    def updateDirection(self, direction):
        self.direction = direction

    def updatePosition(self):
        # 在index0插入元素
        self.bodyList.insert(0, Element(self.x, self.y, self.symbol))
        if self.direction == "right":
            self.x += 1
        elif self.direction == "left":
            self.x -= 1
        elif self.direction == "up":
            self.y -= 1
        elif self.direction == "down":
            self.y += 1


def generateRandomStar(snake: Snake):
    while True:
        randomX = random.randint(1, maxLength - 1)
        randomY = random.randint(1, maxLength - 1)
        if snake.x != randomX and snake.y != randomY:
            return Star(randomX, randomY)


# 全局變數
maxLength = 15
wallSymbol = "牆 "
space = "－ "
snake = Snake(5, 5)
star = generateRandomStar(snake)
sleepTime = 0.1


def handle_key_event(e):
    if e.event_type == keyboard.KEY_DOWN:
        if e.name == 'up':
            snake.updateDirection("up")
        elif e.name == 'down':
            snake.updateDirection("down")
        elif e.name == 'left':
            snake.updateDirection("left")
        elif e.name == 'right':
            snake.updateDirection("right")


def printFrame(elementList: List[Element]):
    # 控制Y軸
    for i in range(0, maxLength):
        # 控制X軸
        str = ""
        for j in range(0, maxLength):
            # 牆的渲染
            if i == 0 or i == maxLength - 1 or j == 0 or j == maxLength - 1:
                str += wallSymbol
                continue

            # 不是牆壁情況的渲染
            matchElement = findMatchElement(elementList, i, j)
            if matchElement:
                str += matchElement.symbol
            else:
                str += space

        print(str)


def findMatchElement(elementList: List[Element], i: int, j: int):
    matchElement = next(
        filter(lambda element: element.x == j and element.y == i, elementList),
        None)
    if matchElement:
        return matchElement


def isCollision(snake: Snake):
    # 是否在最邊界
    if snake.y == 0 or snake.y == maxLength - 1:
        return True
    if snake.x == 0 or snake.x == maxLength - 1:
        return True
    return False


def isEatStar(snake: Snake, star: Star):
    return snake.x == star.x and snake.y == star.y


# 跑動畫
def run():
    while True:
        # 更新蛇的位置
        snake.updatePosition()
        # 判斷是否撞到牆壁
        if isCollision(snake):
            break

        if isEatStar(snake, star):
            # 更新星星位置
            newStar = generateRandomStar(snake)
            star.x = newStar.x
            star.y = newStar.y
            # 更新蛇的尾巴
            snake.growLengthOfTail()

        # 打印畫布
        allElements = [snake, star]
        if snake.tailLength > 0:
            allElements.extend(snake.getTailAllElements())
        printFrame(allElements)

        # 看延遲幾秒
        time.sleep(sleepTime)
        # 清空畫布
        os.system('cls')

    print("遊戲結束!!")


keyboard.hook(handle_key_event)
run()