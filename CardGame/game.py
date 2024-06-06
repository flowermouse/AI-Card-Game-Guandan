import random
from functools import cmp_to_key
from copy import deepcopy
from joblib import load

###########
#  Decks  #
###########

# 以下为牌堆
Deck = [
    '3', '3', '3', '3',
    '4', '4', '4', '4',
    '5', '5', '5', '5',
    '6', '6', '6', '6',
    '7', '7', '7', '7',
    '8', '8', '8', '8',
    '9', '9', '9', '9',
    '10', '10', '10', '10',
    'J', 'J', 'J', 'J',
    'Q', 'Q', 'Q', 'Q',
    'K', 'K', 'K', 'K',
    'A', 'A', 'A', 'A',
    '2', '2', '2', '2',
    
    '3', '3', '3', '3',
    '4', '4', '4', '4',
    '5', '5', '5', '5',
    '6', '6', '6', '6',
    '7', '7', '7', '7',
    '8', '8', '8', '8',
    '9', '9', '9', '9',
    '10', '10', '10', '10',
    'J', 'J', 'J', 'J',
    'Q', 'Q', 'Q', 'Q',
    'K', 'K', 'K', 'K',
    'A', 'A', 'A', 'A',
    '2', '2', '2', '2',
]

# 定义牌点大小的顺序
card_order = {'3': 6, '4': 7, '5': 8, '6': 9, '7': 10, '8': 11, '9': 12,
               '10': 13, 'J': 14, 'Q': 15, 'K': 16, 'A': 17, '2': 18}

# 牌型target映射
target_map = {'单张': 0, '对子': 1, '三同张': 2, '顺子': 3, '三连对': 4,\
               '炸弹': 5, '飞机': 6, '三带对': 7}

target_map_inverse = {0: '单张', 1: '对子', 2: '三同张', 3: '顺子', 4: '三连对',\
               5: '炸弹', 6: '飞机', 7: '三带对'}

ROBOT = \
"""
░░░░░░░▄█▄▄▄█▄
▄▀░░░░▄▌─▄─▄─▐▄░░░░▀▄
█▄▄█░░▀▌─▀─▀─▐▀░░█▄▄█
░▐▌░░░░▀▀███▀▀░░░░▐▌
████░▄█████████▄░████
"""

THUMB = \
"""
┈┈┈┈┈┈▕▔╲
┈┈┈┈┈┈┈▏▕
┈┈┈┈┈┈┈▏▕▂▂▂
▂▂▂▂▂▂╱┈▕▂▂▂▏
▉▉▉▉▉┈┈┈▕▂▂▂▏
▉▉▉▉▉┈┈┈▕▂▂▂▏
▔▔▔▔▔▔╲▂▕▂▂▂
"""

#############
# Functions #
#############

def is_sub(s1, s2):
    # 统计 s1 中每个元素的出现次数
    s1_counts = {}
    for item in s1:
        s1_counts[item] = s1_counts.get(item, 0) + 1
    
    # 统计 s2 中每个元素的出现次数
    s2_counts = {}
    for item in s2:
        s2_counts[item] = s2_counts.get(item, 0) + 1
    
    # 检查 s1 中的每个元素是否在 s2 中，并且出现次数不超过 s2 中的对应元素出现次数
    for item, count in s1_counts.items():
        if item not in s2_counts or s2_counts[item] < count:
            return False
    return True

def custom_compare(card1, card2):
    """
    如果card1 > card2,返回>0,
    如果card1 < card2,返回<0,
    否则返回0
    """
    order1 = card_order.get(card1, 0)
    order2 = card_order.get(card2, 0)
    return order1 - order2

# 使用 cmp_to_key() 函数将比较函数转换为关键字比较函数
key_func = cmp_to_key(custom_compare)

# 展示牌
def draw(hand):
    print('┌', end='')
    for card in hand[:-1]:
        if card != '10':
            print('───┬', end='')
        else:
            print('────┬', end='')
    if hand[-1] != '10':
        print('───┐')
    else:
        print('────┐')

    print('│', end='')
    for card in hand:
        print(f' {card} ', end='')
        print('│', end='')
    print('')

    print('└',end='')
    for card in hand[:-1]:
        if card != '10':
            print('───┴', end='')
        else:
            print('────┴', end='')
    if hand[-1] != '10':
        print('───┘')
    else:
        print('────┘')

# 权值由game.py的card_order定义
# 计算每种牌型的权值
def hash(instance):
    if instance.type == '单张':
        return card_order[instance.value]
    elif instance.type == '对子':
        return 2 * card_order[instance.value] + 8
    elif instance.type == '三同张':
        return 3 * card_order[instance.value] + 15
    elif instance.type == '顺子':
        return 5 * card_order[instance.value] + 10 + 25
    elif instance.type == '三连对':
        return 6 * card_order[instance.value] + 6 + 30
    elif instance.type == '炸弹':
        return instance.number * card_order[instance.value] + 40 + 4 * (instance.number - 4)
    elif instance.type == '飞机':
        return 6 * card_order[instance.value] + 3 + 33
    elif instance.type == '三带对':
        return 3 * card_order[instance.three] + 2 * card_order['8'] + 15 + 8
    
def code_data(string):
    n3 = string.count('3')
    n4 = string.count('4')
    n5 = string.count('5')
    n6 = string.count('6')
    n7 = string.count('7')
    n8 = string.count('8')
    n9 = string.count('9')
    n10 = string.count('10')
    nj = string.count('J')
    nq = string.count('Q')
    nk = string.count('K')
    na = string.count('A')
    n2 = string.count('2')
    coded = [n3, n4, n5, n6, n7, n8, n9, n10, nj, nq, nk, na, n2]
    return coded

###########
#  Class  #
###########

class Game:

    def __init__(self, human, AI):
        """
        p1, p2分别为玩家和AI
        """
        self.human, self.AI = human, AI
        self.turn = random.choice([self.human, self.AI])
        self.used_cards = ' '
        self.human_used = [0 ,0, 0, 0, 0, 0, 0, 0]
        self.AI_used = [0, 0, 0, 0, 0, 0, 0, 0]

    def print_cards(self, who, display):
        print(f'{who.name}出的牌是：')
        print(f'<{display.type}>')
        cards = display.__repr__().split(' ')
        draw(cards)
        print(f'{who.name}还剩{len(who.hand)}张牌')
        print('')
        
    def update(self, display, player):
        self.used_cards += str(display)
        self.used_cards += ' '   
        if player == self.human:
            self.human_used[target_map[display.type]] += 1
        else:
            self.AI_used[target_map[display.type]] += 1

    def play_round(self):
        """
        进行一个回合,如果有玩家获胜,返回True,否则返回False
        """
        # 玩家是上家
        if self.turn == self.human:
            print(f'{self.human.name}是上家')
            display = self.human.play(self.AI_used)
            self.update(display, self.human)
            self.print_cards(self.human, display)
            if self.human.check_win():
                print('玩家获胜')
                print(THUMB)
                return True
            while True:
                display = self.AI.against(display, len(self.human.hand), self.human_used)
                # AI选择pass
                if not display:
                    print(f'{self.AI.name}选择pass')
                    print('')
                    self.turn = self.human
                    return False
                # AI选择出牌
                else:
                    self.update(display, self.AI)
                    self.print_cards(self.AI, display)
                    if self.AI.check_win():
                        print('AI获胜')
                        print(ROBOT)
                        return True
                    display = self.human.against(display, len(self.AI.hand), self.AI_used)
                    # 玩家选择pass
                    if not display:
                        print(f'{self.human.name}选择pass')
                        print('')
                        self.turn = self.AI
                        return False
                    # 玩家选择出牌
                    else:
                        self.update(display, self.human)
                        self.print_cards(self.human, display)
                        if self.human.check_win():
                            print('玩家获胜')
                            print(THUMB)
                            return True
        # AI是上家
        elif self.turn == self.AI:
            print(f'{self.AI.name}是上家')
            display = self.AI.play(self.human_used)
            self.update(display, self.AI)
            self.print_cards(self.AI, display)
            if self.AI.check_win():
                print('AI获胜')
                print(ROBOT)
                return True
            while True:
                display = self.human.against(display, len(self.AI.hand), self.AI_used)
                # 玩家选择pass
                if not display:
                    print(f'{self.human.name}选择pass')
                    print('')
                    self.turn = self.AI
                    return False
                # 玩家选择出牌
                else:
                    self.update(display, self.human)
                    self.print_cards(self.human, display)
                    if self.human.check_win():
                        print('玩家获胜')
                        print(THUMB)
                        return True
                    display = self.AI.against(display, len(self.human.hand), self.human_used)
                    # AI选择pass
                    if not display:
                        print(f'{self.AI.name}选择pass')
                        print('')
                        self.turn = self.human
                        return False
                    # AI选择出牌
                    else:
                        self.update(display, self.AI)
                        self.print_cards(self.AI, display)
                        if self.AI.check_win():
                            print('AI获胜')
                            print(ROBOT)
                            return True


class Card:
    type = '单张'

    def __init__(self, value):
        self.value = value

    def compare(self, other):
        """
        如果self > other,返回>0,
        如果self < other,返回<0,
        否则返回0
        """
        return custom_compare(self.value, other.value)

    def __repr__(self):
        """
        Returns a string which is a readable version of
        a card, in the form:
        <type>: value
        """
        return f'{self.value}'
    
class Pair(Card):
    # init只用输入一张
    type = '对子'

    def __repr__(self):
        """
        Returns a string which is a readable version of
        a card, in the form:
        <type>: value value
        """
        return f'{self.value} {self.value}'

class Triple(Card):
    # init只用输入一张
    type = '三同张'

    def __repr__(self):
        """
        Returns a string which is a readable version of
        a card, in the form:
        <type>: value value value
        """
        return f'{self.value} {self.value} {self.value}'
    
class Continuous(Card):
    # init只用输入第一张
    type = '顺子'
    
    def __repr__(self):
        tool = iter(card_order)
        cur = 0
        while self.value != cur:
            cur = next(tool)
        return f'{self.value} {next(tool)} {next(tool)} {next(tool)} {next(tool)}'
    
class ThreePairs(Card):
    # init只用输入第一张
    type = '三连对'

    def __repr__(self):
        tool = iter(card_order)
        cur = 0
        while self.value != cur:
            cur = next(tool)
        next1 = next(tool)
        next2 = next(tool)
        return f'{self.value} {self.value} {next1} {next1} {next2} {next2}'
    
class Boom:
    # init只用输入第一张
    type = '炸弹'

    def __init__(self, value, number):
        self.value = value
        self.number = number

    def compare(self, other):
        """
        如果self > other,返回>0,
        如果self < other,返回<0,
        否则返回0
        """
        if not isinstance(other, Boom):
            return 1
        if self.number < other.number:
            return -1
        elif self.number > other.number:
            return 1
        else:
            return custom_compare(self.value, other.value)
        
    def __repr__(self):
        str = self.value
        for _ in range(self.number - 1):
            str += ' '
            str += self.value
        return f'{str}'

class TwoTriple(Card):
    # init只用输入第一张
    type = '飞机'
    
    def __repr__(self):
        tool = iter(card_order)
        cur = 0
        while self.value != cur:
            cur = next(tool)
        next1 = next(tool)
        return f'{self.value} {self.value} {self.value} {next1} {next1} {next1}'
    
class ThreeTwo:
    type = '三带对'

    # init 先输入三张的一张，再输入一对的一张
    def __init__(self, three, two):
        self.three = three
        self.two = two

    def compare(self, other):
        """
        如果self > other,返回>0,
        如果self < other,返回<0,
        否则返回0
        """
        return custom_compare(self.three, other.three)
    
    def __repr__(self):
        return f'{self.three} {self.three} {self.three} {self.two} {self.two}'