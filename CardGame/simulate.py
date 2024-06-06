from train_game import *
from ai import *
import csv
import time

dataset = 'data/data7.csv'
train_times = 50
newdata = 'data/newdata4.csv'

def write_data(data, filename):
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def main_loop():
    decks = Deck.copy()
    p2 = AI_origin('AI-origin', decks)
    # p1 = AI_final('forest-v3', decks, 'forest_v3.joblib')
    # p1 = AI_final('tree-v5', decks, 'tree_v5.joblib')
    # p1 = AI_final('new-tree-v6', decks, 'tree_v6.joblib', 'combat_forest_v1.joblib')
    p1 = AI_final('final', decks, 'final_forest.joblib', 'final_combat_forest.joblib')
    # p2 = AI_final('tree-v4', decks, 'tree_v4.joblib')
    # p2 = AI_final('forest-v4', decks, 'forest_v4.joblib', 'combat_tree_v3.joblib')
    # p2 = AI_random('AI-random', decks)
    # p2 = AI_Model('AI-GNB', decks, 'guass_bayes.joblib')
    # p2 = AI_Model('AI-SVM', decks, 'svm.joblib')
    # p2 = AI_New_Model('new-tree', decks, 'tree_v2.joblib')
    # p2 = AI_New_Model('new-forest', decks, 'forest_v2.joblib')
    duel = Game_no_print(p1, p2)
    while True:
        if duel.play_round():
            winner = duel.win
            print(p1.score, p2.score)
            if winner == 0:
                print(p1.name, 'wins')
                for a, b, c, d, e in duel.p1_history:
                    write_data([p1.name, p1.score, p2.score, a, b, c, d, e], dataset)
                for a, b, c, d, e, f in duel.p1_a:
                    write_data([p1.name, p1.score, p2.score, a, b, c, d, e, f], newdata)
            elif winner == 1:
                print(p2.name, 'wins')
                for a, b, c, d, e in duel.p2_history:
                    write_data([p2.name, p2.score, p1.score, a, b, c, d, e], dataset)
                for a, b, c, d, e, f in duel.p1_a:
                    write_data([p2.name, p2.score, p1.score, a, b, c, d, e, f], newdata)
            print('')
            return winner, p1.score, p2.score
        
if __name__ == '__main__':
    start_time = time.time()
    p1_all, p1_dis, p1_dis_win = 0, 0, 0
    p2_all, p2_dis, p2_dis_win = 0, 0, 0
    for _ in range(train_times):
        winner, p1_s, p2_s = main_loop()
        if p1_s < p2_s:
            p1_dis += 1
        else:
            p2_dis += 1
        if winner == 0:
            p1_all += 1
            if p1_s < p2_s:
                p1_dis_win += 1
        elif winner == 1:
            p2_all += 1
            if p1_s > p2_s:
                p2_dis_win += 1
    print('player1 wins:', p1_all)
    print('player2 wins:', p2_all)
    print('p1劣势对局数:', p1_dis)
    print('p2劣势对局数:', p2_dis)
    print('p1劣势对局胜率:', p1_dis_win / p1_dis * 100, '%')
    print('p2劣势对局胜率:', p2_dis_win / p2_dis * 100, '%')
    print('p1优势对局胜率:', (p1_all - p1_dis_win) / (train_times - p1_dis) * 100, '%')
    print('p2优势对局胜率:', (p2_all - p2_dis_win) / (train_times - p2_dis) * 100, '%')
    end_time = time.time()
    print('time:', end_time - start_time, 's')
    print('train per time:', (end_time - start_time) / train_times, 's')