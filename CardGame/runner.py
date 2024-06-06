from game import *
from ai import *


def main_loop():
    # 初始化
    print(CAT)
    print('┏━━━━━━━━━━━━━━━━━━━━━━┓')
    print('┃  欢迎来到AI掼蛋游戏  ┃')
    print('┃     version: 2.0     ┃')
    print('┃     作者：巫昊聪     ┃')
    print('┗━━━━━━━━━━━━━━━━━━━━━━┛')
    print(WELCOME_GRAPH)
    name = input('请输入你的名字：')
    # 是否提示
    while True:
        remind = input('是否需要出牌提示？(y/n): ')
        if remind == 'y' or remind == 'n':
            break
        else:
            print('输入有误，请重新输入')
    decks = Deck.copy()
    p1 = Player(name=name, decks=decks, model='final_forest.joblib', combat_model='final_combat_forest.joblib')
    available = [
        "AI_random('AI-random', decks)",
        "AI_origin('AI-origin', decks)",
        "AI_final('AI-tree-v4', decks, 'tree_v4.joblib')",
        "AI_final('AI-final', decks, 'final_forest.joblib', 'final_combat_forest.joblib')"
    ]
    while True:
        ai = input('请选择难度 (1. 休闲    2. 简单     3. 一般     4. 较难): ')
        if ai == '1' or ai == '2' or ai == '3' or ai == '4':
            p2 = eval(available[int(ai)-1])
            break
        else:
            print('输入有误，请重新输入')
    if remind == 'y':
        p1.remind = True
    else:
        p1.remind = False

    duel = Game(p1, p2)
    # 开始游戏
    print('┏━━━━━━━━━━━━━━━━━━━━━━┓')
    print('┃   掼蛋游戏正式开始！ ┃')
    print('┗━━━━━━━━━━━━━━━━━━━━━━┛')
    print(GAME)
    print('')
    while True:
        if duel.play_round():
            if remind == 'y':
                print(f'你和对手的初始手牌的赋值分别是：{p1.score, p2.score}')
                if p1.score >= p2.score: 
                    print('你刚才的对局是优势对局')
                else:
                    print('你刚才的对局是劣势对局')
            print('┏━━━━━━━━━━━━━━━━━━━━━━┓')
            print('┃  游戏结束，下次再见  ┃')
            print('┗━━━━━━━━━━━━━━━━━━━━━━┛')
            print(PYTHON)
            return
        

CAT = \
"""
      ▄▀▄     ▄▀▄
     ▄█░░▀▀▀▀▀░░█▄
 ▄▄  █░░░░░░░░░░░█  ▄▄
█▄▄█ █░░▀░░┬░░▀░░█ █▄▄█
"""

WELCOME_GRAPH = \
"""
█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
█░░╦─╦╔╗╦─╔╗╔╗╔╦╗╔╗░░█
█░░║║║╠─║─║─║║║║║╠─░░█
█░░╚╩╝╚╝╚╝╚╝╚╝╩─╩╚╝░░█
█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
"""

GAME = \
"""
 ▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄
█░░░█░░░░░░░░░░▄▄░██░█
█░▀▀█▀▀░▄▀░▄▀░░▀▀░▄▄░█
█░░░▀░░░▄▄▄▄▄░░██░▀▀░█
 ▀▄▄▄▄▄▀─────▀▄▄▄▄▄▄▀
"""

PYTHON = \
"""
▄▄▀█▄───▄───────▄
▀▀▀██──███─────███
░▄██▀░█████░░░█████░░
███▀▄███░███░███░███░▄
▀█████▀░░░▀███▀░░░▀██▀
"""

if __name__ == '__main__':
    main_loop()