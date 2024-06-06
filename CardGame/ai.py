from game import *
import numpy as np

class Player:
    def __init__(self, name, decks=Deck, model='', combat_model=''):
        """ Initialize an object. """
        self.name = name
        self.hand = []
        for _ in range(27):
            card = random.choice(decks)
            self.hand.append(card)
            decks.remove(card)
        self.hand.sort(key=key_func)
        self.change = True
        self.strategy = None
        self.score = 0
        self.model = 'model/' + model
        self.combat_model = 'model/' + combat_model
        self.check_against = 'pass'
        self.remind = False

    def display_hand(self):
        print('您的手牌是：')
        draw(self.hand)
        print('')

    def check_type(self, cards):
        """检测手牌是否为特定类型"""
        # 单张
        if len(cards) == 1:
            return Card(cards[0])
        # 对子
        if len(cards) == 2 and cards[0] == cards[1]:
            return Pair(cards[0])
        # 三同张
        if len(cards) == 3 and cards[0] == cards[1] and cards[1] == cards[2]:
            return Triple(cards[0])
        # 炸弹
        if len(cards) >= 4 and len(set(cards)) == 1:
            return Boom(cards[0], len(cards))
        # 顺子
        if len(cards) == 5:
            check = [custom_compare(x, y) for x, y in zip(cards[:-1], cards[1:])]
            if check == [-1, -1, -1, -1]:
                return Continuous(cards[0])
        # 三带对
        if len(cards) == 5:
            if cards[0] == cards[1] and cards[1] == cards[2]:
                if cards[3] == cards[4]:
                    return ThreeTwo(cards[0], cards[3])
            elif cards[2] == cards[3] and cards[3] == cards[4]:
                if cards[0] == cards[1]:
                    return ThreeTwo(cards[2], cards[0])
        # 飞机
        if len(cards) == 6:
            if cards[0] == cards[1] and cards[1] == cards[2] and cards[3] == cards[4] and cards[4] == cards[5]:
                if custom_compare(cards[3], cards[0]) == 1:
                    return TwoTriple(cards[0])
        # 三连对
        if len(cards) == 6:
            check = [custom_compare(x, y) for x, y in zip(cards[:-1], cards[1:])]
            if check == [0, -1, 0, -1, 0]:
                return ThreePairs(cards[0])
        return None
    
    def recognize(self, hand):
        """
        返回一个所有出牌方式的list, 每个元素是一个字典, 记录了每种牌型的数量
        """
        # 用字典记录每种牌的数量
        ways = {'单张': [], '对子': [], '三同张': [], '顺子': [], '三连对': [], '炸弹': [], '飞机': [], '三带对': []}

        # dfs 递归遍历所有可能的牌型
        def count_cards(cards, card_count):

            res = []
            # 减少递归深度，提高运行速度
            if len(card_count['单张']) >= 7:
                return []
            
            if len(cards) == 0:
                return [card_count]
            if len(cards) == 1:
                current = deepcopy(card_count)
                current['单张'].append(Card(cards[0]))
                return [current]
            
            else:
                unique = list(set(cards))
                unique.sort(key=key_func)

                # 单张
                current = deepcopy(card_count)
                current['单张'].append(Card(cards[0]))
                res.extend(count_cards(cards[1:], current))
                # 对子
                if len(cards) >= 2 and cards[0] == cards[1]:
                    current = deepcopy(card_count)
                    current['对子'].append(Pair(cards[0]))
                    res.extend(count_cards(cards[2:], current))
                # 三同张
                if len(cards) >= 3 and cards[0] == cards[1] and cards[1] == cards[2]:
                    current = deepcopy(card_count)
                    current['三同张'].append(Triple(cards[0]))
                    res.extend(count_cards(cards[3:], current))
                # 炸弹
                if len(cards) >= 4 and cards[0] == cards[1] and cards[1] == cards[2] and cards[2] == cards[3]:
                    current = deepcopy(card_count)
                    current['炸弹'].append(Boom(cards[0], 4))
                    res.extend(count_cards(cards[4:], current))
                    if len(cards) >= 5 and cards[3] == cards[4]:
                        current = deepcopy(card_count)
                        current['炸弹'].append(Boom(cards[0], 5))
                        res.extend(count_cards(cards[5:], current))
                        if len(cards) >= 6 and cards[4] == cards[5]:
                            current = deepcopy(card_count)
                            current['炸弹'].append(Boom(cards[0], 6))
                            res.extend(count_cards(cards[6:], current))
                            if len(cards) >= 7 and cards[5] == cards[6]:
                                current = deepcopy(card_count)
                                current['炸弹'].append(Boom(cards[0], 7))
                                res.extend(count_cards(cards[7:], current))
                                if len(cards) >= 8 and cards[6] == cards[7]:
                                    current = deepcopy(card_count)
                                    current['炸弹'].append(Boom(cards[0], 8))
                                    res.extend(count_cards(cards[8:], current))
                # 顺子
                if len(unique) >= 5:
                    con = self.check_type([unique[0], unique[1], unique[2], unique[3], unique[4]])
                    if isinstance(con, Continuous):
                        now = deepcopy(card_count)
                        now['顺子'].append(con)
                        current = cards.copy()
                        for i in range(5):
                            current.remove(unique[i])
                        res.extend(count_cards(current, now))
                # 三连对
                if len(cards) >= 6 and len(unique) >= 3:
                    tp = self.check_type([unique[0], unique[0], unique[1], unique[1], unique[2], unique[2]])
                    if isinstance(tp, ThreePairs):
                        if all(cards.count(unique[i]) >= 2 for i in range(3)):
                            now = deepcopy(card_count)
                            now['三连对'].append(tp)
                            current = cards.copy()
                            for i in range(3):
                                current.remove(unique[i])
                                current.remove(unique[i])
                            res.extend(count_cards(current, now))
                # 飞机
                if len(cards) >= 6 and len(unique) >= 2:
                    pl = self.check_type([unique[0], unique[0], unique[0], unique[1], unique[1], unique[1]])
                    if isinstance(pl, TwoTriple):
                        if all(cards.count(unique[i]) >= 3 for i in range(2)):
                            now = deepcopy(card_count)
                            now['飞机'].append(pl)
                            current = cards.copy()
                            for i in range(2):
                                current.remove(unique[i])
                                current.remove(unique[i])
                                current.remove(unique[i])
                            res.extend(count_cards(current, now))

                return res
            
        return count_cards(hand, ways)
    
    def choose_best(self, ways):
        """
        选择最优的出牌方式, 为一个字典, 记录了每种牌型的instance。
        而且由于是顺序查找, 牌值也是从小到大的
        """
        def hash_ways(ways):
            sum = 0
            for category in ways.values():
                for card in category:
                    sum += hash(card)
            return sum
        
        self.change == False
        for way in deepcopy(ways):
            while len(way['三同张']) > 0 and len(way['对子']) > 0:
                three = way['三同张'].pop(0)
                two = way['对子'].pop(0)
                way['三带对'].append(ThreeTwo(three.value, two.value))
                ways.append(way)
        ways.sort(key=hash_ways, reverse=True)
        if self.strategy is None:
            self.score = hash_ways(ways[0])
        # 取前5个最优策略
        return ways[:5]
    
    def remove_hand(self, instance):
        pass
    
    def reminder(self, used):
        """
        返回值为出牌的instance对象
        used:对手出牌型的list[int]
        """
        return AI_final.play(self, used)
            
    def combat_remind(self, other, remain, used):
        return AI_final.against(self, other, remain, used)
          
    def print_reminder(self, display):
        print('提示出牌：')
        if display is not None:
            print(f'<{display.type}>')
            cards = display.__repr__().split(' ')
            draw(cards)
        else:
            print('pass')
        print('已经提示')
        print('')

    def play(self, used=None):
        """玩家是上家时出牌，返回玩家的出牌, 是相应class的instance"""
        # 显示手牌
        self.display_hand()
        # 提示
        if self.remind:
            reminder = self.reminder(used)
            self.print_reminder(reminder)
        # 出牌
        while True:   
            cards = input('请选择你要出的牌(输入牌面值,空格隔开): ').split()
            if len(cards) == 0:
                print('无效出牌，请重试')
                continue
            cards.sort(key=key_func)
            # 检测牌是否在手牌中
            if not is_sub(cards, self.hand):
                print('无效出牌，请重试')
                continue
            # 检测牌型
            if self.check_type(cards) == None:
                print('无效出牌，请重试')
                continue
            for card in cards:
                self.hand.remove(card)
            cards = self.check_type(cards)
            return cards        
        
    def check_win(self):
        if len(self.hand) == 0:
            return True
        else:
            return False
        
    def against(self, other, remain=None, used=None):
        """
        如果pass返回None,否则返回出的牌
        """
        # 显示手牌
        self.display_hand()
        # 提示
        if self.remind:
            reminder = self.combat_remind(other, remain, used)
            self.print_reminder(reminder)
        # 出牌
        while True:   
            cards = input('请选择你要出的牌(输入牌面值,空格隔开)(如果输入空白则表示pass): ').split()
            # pass
            if len(cards) == 0:
                return None
            cards.sort(key=key_func)
            # 检测牌是否在手牌中
            if not is_sub(cards, self.hand):
                print('无效出牌，请重试')
                continue
            # 检测牌型是否存在
            if self.check_type(cards) == None:
                print('无效出牌，请重试')
                continue
            cards_instance = self.check_type(cards)
            # 检测牌型与大小
            if cards_instance.type != other.type and cards_instance.type != '炸弹':
                print('出牌类型错误，请重试')
                continue
            if cards_instance.compare(other) <= 0:
                print('出牌大小错误，请重试')
                continue
            # 出牌
            for card in cards:
                self.hand.remove(card)
            return cards_instance
    
class AI_origin(Player):

    def remove_hand(self, instance):
        """remove the cards from hand"""
        if instance.type == '单张':
            self.hand.remove(instance.value)
        elif instance.type == '对子':
            self.hand.remove(instance.value)
            self.hand.remove(instance.value)
        elif instance.type == '三同张':
            self.hand.remove(instance.value)
            self.hand.remove(instance.value)
            self.hand.remove(instance.value)
        elif instance.type == '顺子':
            self.hand.remove(instance.value)
            tool = iter(card_order)
            cur = 0
            while instance.value != cur:
                cur = next(tool)
            for _ in range(4):
                self.hand.remove(next(tool))
        elif instance.type == '三连对':
            tool = iter(card_order)
            cur = 0
            while instance.value != cur:
                cur = next(tool)
            next1 = next(tool)
            next2 = next(tool)
            self.hand.remove(instance.value)
            self.hand.remove(instance.value)
            self.hand.remove(next1)
            self.hand.remove(next1)
            self.hand.remove(next2)
            self.hand.remove(next2)
        elif instance.type == '炸弹':
            for _ in range(instance.number):
                self.hand.remove(instance.value)
        elif instance.type == '飞机':
            tool = iter(card_order)
            cur = 0
            while instance.value != cur:
                cur = next(tool)
            next1 = next(tool)
            self.hand.remove(instance.value)
            self.hand.remove(instance.value)
            self.hand.remove(instance.value)
            self.hand.remove(next1)
            self.hand.remove(next1)
            self.hand.remove(next1)
        elif instance.type == '三带对':
            self.hand.remove(instance.three)
            self.hand.remove(instance.three)
            self.hand.remove(instance.three)
            self.hand.remove(instance.two)
            self.hand.remove(instance.two)

    def play(self, used=None):
        """
        在已选择的最优的出牌方式下，按优先级出牌
        优先级：顺子 > 三连对 > 三带对 > 飞机 > 三同张 > (单张 > 对子) > 炸弹

        返回值为出牌的instance对象
        """
        if self.change:
            self.strategy = self.choose_best(self.recognize(self.hand))

        ########测试#########
        # self.display_hand()
        # print(self.strategy)
        ####################
           
        best = self.strategy[0]
        # 每次出牌将change置为True
        self.change = True

        if len(best['顺子']) > 0:
            show = best['顺子'][0]
            self.remove_hand(show)
            return show
        elif len(best['三连对']) > 0:
            show = best['三连对'][0]
            self.remove_hand(show)
            return show
        elif len(best['三带对']) > 0:
            show = best['三带对'][0]
            self.remove_hand(show)
            return show
        elif len(best['飞机']) > 0:
            show = best['飞机'][0]
            self.remove_hand(show)
            return show
        elif len(best['三同张']) > 0:
            show = best['三同张'][0]
            self.remove_hand(show)
            return show
        # 先出小于J的单牌
        elif len(best['单张']) > 0 and hash(best['单张'][0]) <= 8:
            show = best['单张'][0]
            self.remove_hand(show)
            return show
        # 再出小于J的对子
        elif len(best['对子']) > 0 and hash(best['对子'][0]) <= 22:
            show = best['对子'][0]
            self.remove_hand(show)
            return show
        # 再出剩下的单张
        elif len(best['单张']) > 0:
            show = best['单张'][0]
            self.remove_hand(show)
            return show
        # 最后出剩下的对子
        elif len(best['对子']) > 0:
            show = best['对子'][0]
            self.remove_hand(show)
            return show
        # 最后出炸弹
        elif len(best['炸弹']) > 0:
            show = best['炸弹'][0]
            self.remove_hand(show)
            return show


    def against(self, other, remain, used=None):
        """
        remain: 对手剩余的牌数
        other: 对手出的牌的instance对象
        return value: 出牌的instance对象

        根据对手的出牌情况, 选择出牌策略, None为pass
        如果对手牌数多于7张, 则不改变strategy, 否则改变strategy
        """
        def in_plan():
            best = self.strategy[0]
            for category in best.values():
                if len(category) > 0 and category[0].type == other.type:
                        for card in category:
                            if card.compare(other) > 0:
                                self.change = True
                                self.remove_hand(card)
                                return card
            return None

        def check_combat():
            for strategy in self.strategy[1:]:
                for category in strategy.values():
                    if len(category) > 0 and category[0].type == other.type:
                        for card in category:
                            if card.compare(other) > 0:
                                self.change = True
                                self.remove_hand(card)
                                return card
            return None
                
        if self.change:
            self.strategy = self.choose_best(self.recognize(self.hand))

        self.change = False
        ########测试#########
        # self.display_hand()
        # print(self.strategy)
        ####################
        
        # 只剩炸弹
        if len(self.strategy[0]['炸弹']) > 0:
            best = self.strategy[0]
            bomb = best['炸弹'][0]
            if len(self.hand) == self.strategy[0]['炸弹'][0].number:
                if bomb.compare(other) > 0:
                    self.change = True
                    self.remove_hand(bomb)
                    return bomb

        if remain > 7:
            # 按最优策略
            plan_a = in_plan()
            if plan_a:
                self.check_against = 'best'
                self.change = True
                return plan_a
            self.check_against = 'pass'
            return None
                            
        else:
            # 按最优策略对牌
            plan_a = in_plan()
            if plan_a:
                self.change = True
                return plan_a
            # 最优策略出炸弹
            best = self.strategy[0]
            for bomb in best['炸弹']:
                if bomb.compare(other) > 0:
                    self.remove_hand(bomb)
                    self.change = True
                    return bomb
            # 次优策略对牌
            combat = check_combat()
            if combat is not None:
                self.change = True
                return combat
            # 次优策略炸弹
            for strategy in self.strategy[1:]:
                for bomb in strategy['炸弹']:
                    if bomb.compare(other) > 0:
                        self.remove_hand(bomb)
                        self.change = True
                        return bomb
        # 无计可施
        return None
    
class AI_random(AI_origin):
    def play(self, used=None):
        """
        返回值为出牌的instance对象
        """
        if self.change:
            self.strategy = self.choose_best(self.recognize(self.hand))

        best = self.strategy[0]
        # 每次出牌将change置为True
        self.change = True

        ways = list(best.keys())
        ways = list(filter(lambda x: len(best[x]) > 0, ways))
        way = random.choice(ways)
        show = best[way][0]
        self.remove_hand(show)
        return show
    
class AI_Model(AI_origin):
    def play(self, used):
        # 输入为自己的手牌和所有已经出的牌
        """
        返回值为出牌的instance对象
        used是所有已经出的牌的string
        """
        if self.change:
            self.strategy = self.choose_best(self.recognize(self.hand))

        best = self.strategy[0]
        # 每次出牌将change置为True
        self.change = True

        hand = code_data(''.join(self.hand))
        used_card = code_data(used)
        clf = load(self.model)
        probs = clf.predict_proba([hand + used_card])
        probs = probs[0]
        # enumerate函数的应用
        sorted_probs = sorted(enumerate(probs), key=lambda x: x[1], reverse=True)
        for i, prob in sorted_probs:
            way = target_map_inverse[i]
            if len(best[way]) > 0:
                show = best[way][0]
                self.remove_hand(show)
                return show
            
class AI_New_Model(AI_origin):
    def play(self, used):
        # 输入为自己的策略和对手的出牌
        """
        返回值为出牌的instance对象
        used:对手出牌型的list[int]
        """
        if self.change:
            self.strategy = self.choose_best(self.recognize(self.hand))

        best = self.strategy[0]
        # 每次出牌将change置为True
        self.change = True

        now_strategy = [len(best[x]) for x in best]
        opponent_used = used
        clf = load(self.model)
        probs = clf.predict_proba([now_strategy + opponent_used])
        probs = probs[0]
        # enumerate函数的应用
        sorted_probs = sorted(enumerate(probs), key=lambda x: x[1], reverse=True)
        for i, prob in sorted_probs:
            way = target_map_inverse[i]
            if len(best[way]) > 0:
                show = best[way][0]
                self.remove_hand(show)
                return show
            
class AI_final(AI_origin):
    # forest_v3, tree_v4 输入为自己的策略，对手的出牌和自己的手牌
    def play(self, used):
        """
        返回值为出牌的instance对象
        used:对手出牌型的list[int]
        """
        if self.change:
            self.strategy = self.choose_best(self.recognize(self.hand))

        best = self.strategy[0]
        # 每次出牌将change置为True
        self.change = True

        # 只剩三带对
        if len(self.hand) == 5:
            if self.check_type(self.hand) != None:
                show = self.check_type(self.hand)
                self.remove_hand(show)
                return show

        hand = code_data(''.join(self.hand))
        now_strategy = [len(best[x]) for x in best]
        opponent_used = used
        clf = load(self.model)
        probs = clf.predict_proba([now_strategy + opponent_used + hand])
        probs = probs[0]
        # enumerate函数的应用
        sorted_probs = sorted(enumerate(probs), key=lambda x: x[1], reverse=True)
        for i, prob in sorted_probs:
            way = target_map_inverse[i]
            if len(best[way]) > 0:
                show = best[way][0]
                self.remove_hand(show)
                return show
        
    def against(self, other, remain, used=None):
        # 输入为：自己的策略，对手出过的牌型，对手的出牌，自己的手牌，对手的剩余张数
        # 输出为0,1和2, 0表示次优，1表示炸弹, 2表示pass
        """
        remain: 对手剩余的牌数
        other: 对手出的牌的instance对象
        used:对手出牌型的list[int]
        return value: 出牌的instance对象
        """
        def in_plan():
            best = self.strategy[0]
            for category in best.values():
                if len(category) > 0 and category[0].type == other.type:
                        for card in category:
                            if card.compare(other) > 0:
                                self.change = True
                                self.remove_hand(card)
                                return card
            return None

        def check_combat():
            for strategy in self.strategy[1:]:
                for category in strategy.values():
                    if len(category) > 0 and category[0].type == other.type:
                        for card in category:
                            if card.compare(other) > 0:
                                self.change = True
                                self.remove_hand(card)
                                return card
            return None
                
        if self.change:
            self.strategy = self.choose_best(self.recognize(self.hand))

        self.change = False

        # 只剩炸弹
        if len(self.strategy[0]['炸弹']) > 0:
            best = self.strategy[0]
            bomb = best['炸弹'][0]
            if len(self.hand) == self.strategy[0]['炸弹'][0].number:
                if bomb.compare(other) > 0:
                    self.change = True
                    self.remove_hand(bomb)
                    return bomb

        if remain > 10:
            # 按最优策略
            if other.type != '炸弹':
                plan_A = in_plan()
                if plan_A:
                    self.check_against = 'best'
                    return plan_A
            # 处理数据
            best = self.strategy[0]
            if self.combat_model == 'model/':
                probs = [np.random.choice([0, 0, 1, 1, 2])]
            else:
                hand = code_data(''.join(self.hand))
                now_strategy = [len(best[x]) for x in best]
                sc = target_map[other.type]
                opponent_used = used
                clf = load(self.combat_model)
                sample = np.array(now_strategy + opponent_used + [sc] + hand + [remain]).reshape(1, -1)
                probs = clf.predict(sample)
            # 是否次优策略出牌
            if probs[0] == 0:
                combat = check_combat()
                if combat is not None:
                    self.check_against = 'combat'
                    return combat
            # 是否出炸弹
            elif probs[0] == 1:
                bomb_list = self.strategy[0]['炸弹']
                bomb_list.sort(key=lambda x: x.number * 100 + card_order[x.value])
                for bomb in bomb_list:
                    if bomb.compare(other) > 0:
                        self.remove_hand(bomb)
                        self.change = True
                        return bomb
            else:
                self.check_against = 'pass'
                return None
            self.check_against = 'pass'
            return None
        
        else:
            # 按最优策略对牌
            plan_a = in_plan()
            if plan_a:
                return plan_a
            # 最优策略出炸弹
            best = self.strategy[0]
            for bomb in best['炸弹']:
                if bomb.compare(other) > 0:
                    self.remove_hand(bomb)
                    self.change = True
                    return bomb
            # 次优策略对牌
            combat = check_combat()
            if combat is not None:
                self.change = True
                return combat
            # 次优策略炸弹
            for strategy in self.strategy[1:]:
                bomb_list = strategy['炸弹']
                bomb_list.sort(key=lambda x: x.number * 100 + card_order[x.value])
                for bomb in bomb_list:
                    if bomb.compare(other) > 0:
                        self.remove_hand(bomb)
                        self.change = True
                        return bomb
        # 无计可施
        return None
            