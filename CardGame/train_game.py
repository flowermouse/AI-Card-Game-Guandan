from game import *
from ai import AI_Model

# 牌型target映射
target_map = {'单张': 0, '对子': 1, '三同张': 2, '顺子': 3, '三连对': 4,\
               '炸弹': 5, '飞机': 6, '三带对': 7}

class Game_no_print(Game):
    """
    用于训练，无输出的游戏类
    """
    def __init__(self, p1, p2):
        self.p1, self.p2 = p1, p2
        self.turn = random.choice([self.p1, self.p2])
        self.win = None
        self.p1_history = []
        self.p2_history = []
        self.p1_used = [0 ,0, 0, 0, 0, 0, 0, 0]
        self.p2_used = [0 ,0, 0, 0, 0, 0, 0, 0]
        self.used_cards = ' '
        self.p1_a = []
        self.p2_a = []

    def update(self, display, player):
        self.used_cards += str(display)
        self.used_cards += ' '   
        if player == self.p1:
            self.p1_used[target_map[display.type]] += 1
        else:
            self.p2_used[target_map[display.type]] += 1

    def play_round(self):
        """
        进行一个回合,如果p1获胜,返回0; p2获胜,返回1
        """
        # p1是上家
        if self.turn == self.p1:

            before_hand = self.p1.hand.copy()
            before_used = self.used_cards

            if isinstance(self.p1, AI_Model):
                display = self.p1.play(self.used_cards)
            else:
                display = self.p1.play(self.p2_used)

            target = target_map[display.type]
            self.update(display, self.p1)
            best = self.p1.strategy[0]
            now_strategy = [len(best[x]) for x in best]
            self.p1_history.append((target, now_strategy, self.p2_used.copy(),\
                                     ' '.join(before_hand), before_used))

            if self.p1.check_win():
                self.win = 0
                return True
            while True:
                before_hand = self.p2.hand.copy()
                other_card = target_map[display.type]
                display = self.p2.against(display, len(self.p1.hand), self.p1_used)
                best = self.p2.strategy[0]
                now_strategy = [len(best[x]) for x in best]
                self.p2_a.append((now_strategy, self.p1_used.copy(), other_card, \
                                    ' '.join(before_hand), len(self.p1.hand), self.p2.check_against))
                # p2选择pass
                if not display:
                    self.turn = self.p1
                    return False
                # p2选择出牌
                else:
                    self.update(display, self.p2)
                    if self.p2.check_win():
                        self.win = 1
                        return True
                    before_hand = self.p1.hand.copy()
                    other_card = target_map[display.type]
                    display = self.p1.against(display, len(self.p2.hand), self.p2_used)
                    best = self.p1.strategy[0]
                    now_strategy = [len(best[x]) for x in best]
                    self.p1_a.append((now_strategy, self.p2_used.copy(), other_card, \
                                    ' '.join(before_hand), len(self.p2.hand), self.p1.check_against))
                    # p1选择pass
                    if not display:
                        self.turn = self.p2
                        return False
                    # p1选择出牌
                    else:
                        self.update(display, self.p1)
                        if self.p1.check_win():
                            self.win = 0
                            return True
        # p2是上家
        elif self.turn == self.p2:

            before_hand = self.p2.hand.copy()
            before_used = self.used_cards

            if isinstance(self.p2, AI_Model):
                display = self.p2.play(self.used_cards)
            else:
                display = self.p2.play(self.p1_used)

            target = target_map[display.type]
            self.update(display, self.p2)
            best = self.p2.strategy[0]
            now_strategy = [len(best[x]) for x in best]
            self.p2_history.append((target, now_strategy, self.p1_used.copy(),\
                                     ' '.join(before_hand), before_used))

            if self.p2.check_win():
                self.win = 1
                return True
            while True:
                before_hand = self.p1.hand.copy()
                other_card = target_map[display.type]
                display = self.p1.against(display, len(self.p2.hand), self.p2_used)
                best = self.p1.strategy[0]
                now_strategy = [len(best[x]) for x in best]
                self.p1_a.append((now_strategy, self.p2_used.copy(), other_card, \
                                    ' '.join(before_hand), len(self.p2.hand), self.p1.check_against))
                # p1选择pass
                if not display:
                    self.turn = self.p2
                    return False
                # p1选择出牌
                else:
                    self.update(display, self.p1)
                    if self.p1.check_win():
                        self.win = 0
                        return True
                    before_hand = self.p2.hand.copy()
                    other_card = target_map[display.type]
                    display = self.p2.against(display, len(self.p1.hand), self.p1_used)
                    best = self.p2.strategy[0]
                    now_strategy = [len(best[x]) for x in best]
                    self.p2_a.append((now_strategy, self.p1_used.copy(), other_card, \
                                    ' '.join(before_hand), len(self.p1.hand), self.p2.check_against))
                    # p2选择pass
                    if not display:
                        self.turn = self.p1
                        return False
                    # p2选择出牌
                    else:
                        self.update(display, self.p2)
                        if self.p2.check_win():
                            self.win = 1
                            return True
