import random
import math
from card import *
import sys
import time
import threading
from robot import *

#  無聊的小動畫彩蛋

def animated_loading(option, count):
    if option == 1:
        if count == 1:
            print('原住民小石 ： 嗨大家好！ ')
            time.sleep(2.5)
            print('醫學系小馮 ： 你好！')
            print('認識很久後...')
            time.sleep(2.5)
            for _ in range(10):
                print('醫學系小馮：' + 'A' * 15 + '!!!', sep=' ')
                time.sleep(0.5)

        if count >= 2:
            print('原住民小石 ： 嗨大家好！')
            time.sleep(1.5)
            print('醫學系小馮 ：' + '開心認識你' * count)
            print('認識很久後...')
            time.sleep(1.5)
            for _ in range(10):
                print('醫學系小馮：' + 'A' * 15 * count + '!!!', sep=' ')
                time.sleep(max(0.5 - (0.15 * count), 0.2))

    if option == 2:
        print('\n-1 跟 1 是不一樣的\n')
        time.sleep(1)
        print('\n程式需要防錯:')
        print('請重選')
        chars = "/—\\|"*10
        for char in chars:
            sys.stdout.write('\r'+'loading...'+char)
            time.sleep(.1)
            sys.stdout.flush()


# 出牌的人 自己選要出什麼
def choose(person, suite_for_this_turn="♠♥♦♣"):
    person.arrange(get_key)
    print('\n你的手牌', person.cards_on_hand)
    suite = input("請輸入花色 ♠(0) ♥(1) ♦(2) ♣(3): ")
    face = input("請輸入數值 A,2,...J,Q,K: \n")

    # 輸入型態錯誤
    if suite not in "0123" or (face not in map(str, range(2, 11)) and face not in "AJQK"):
        print("您的輸入不合規則! 注意：A 和 JQK 請直接輸入文字，而非數字!")
        return choose(person, suite_for_this_turn)

    # 出的花色不符合本回合花色
    suite = ["♠", "♥", "♦", "♣"][int(suite)]

    if suite_for_this_turn in person.suites_on_hand() and suite not in suite_for_this_turn:
        print("\n您的花色不符合規則，花色要出{0}，除非您已無該花色的牌".format(suite_for_this_turn))
        print("但你還有{0}張{1}牌\n"
              .format(len(person.find_suite(suite_for_this_turn)), suite_for_this_turn))

        return choose(person, suite_for_this_turn)

    key = '%s%s' % (suite, face)

    for card in person.cards_on_hand:
        if card.__repr__() == key:
            person.cards_on_hand.remove(card)
            return card

    # 出的牌不在手中
    print("你選的牌不在你手中！請重新選擇")
    return choose(person, suite_for_this_turn)

# 隨機出牌 待改 花色限制問題

def random_choose(person, num, suite_for_this_turn=-1):  # 出牌的人，它剩幾張牌
    cards_on_hand_for_a_suite = person.find_suite(suite_for_this_turn)
    # 第一個出牌，還沒有決定本回合的花色

    if num == 1:
        card_choosed = person.cards_on_hand[0]

    elif len(cards_on_hand_for_a_suite) == 0:
        card_choosed = person.cards_on_hand[random.randint(0, num-1)]

    else:
        card_choosed = cards_on_hand_for_a_suite[random.randint(
            0, len(cards_on_hand_for_a_suite)-1)]

    person.cards_on_hand.remove(card_choosed)

    return card_choosed

# 展示手牌


def show_cards(close_show=1):
    if close_show != -1:
        print("展示手牌" + "-"*15)
        for player in players:
            print(player.name + ':', end=' ')
            player.arrange(get_key)
            print(player.cards_on_hand)
        print("-"*20)
    return 0

# 每回合玩牌過程

def play(position, players, king, model, close_show, nickname="國家機器"):  # 玩家的名字
    person_on_turn = players[position]

    # 如果不是真人玩家，展示所有電腦的手牌
    if model != 0:
        show_cards(close_show)

    # 第一個玩家出的牌
    if model == 0:  # 玩家和三名電腦對戰
        if person_on_turn.name == nickname:
            fst_card = choose(person_on_turn)
        else:
            fst_card = random_choose(person_on_turn,
                                     len(person_on_turn.cards_on_hand))
    elif model == 1:  # 電腦自動對戰
        if person_on_turn.name == '國家機器的助手' or '國家機器':
            fst_card = person_on_turn.fst_turn_decide(king)
            # print("!"*5, king, fst_card.suite)

        else:
            fst_card = random_choose(person_on_turn,
                                 len(person_on_turn.cards_on_hand))
    if close_show != -1:
        print(person_on_turn, fst_card)

    suite_for_this_turn = fst_card.suite  # 本回合適用的花色
    max_face = fst_card.face
    # end of 第一個玩家出的牌

    person_got_trick = person_on_turn  # 目前牌面最大的人
    max_card = fst_card  # 這回合最終獲勝的牌，預設為第一張牌

    position += 1  # 出完牌後，換下一個人出
    if position == 4:  # 配合座位列表值，滿四就歸零
        position = 0

    # 第一張牌丟出後的牌局
    for _ in range(3):
        person_on_turn = players[position]
        if model == 0:
            if person_on_turn.name == nickname:
                card_on_turn = choose(person_on_turn, fst_card.suite)
                time.sleep(0.3)  # 稍微緩速，增強真實感

            else:
                card_on_turn = random_choose(
                    person_on_turn, len(person_on_turn.cards_on_hand), suite_for_this_turn)
                time.sleep(0.3)  # 稍微緩速，增強真實感

        if model == 1:
            card_on_turn = random_choose(
                person_on_turn, len(person_on_turn.cards_on_hand), suite_for_this_turn)

        if model == 2:
            pass

        face_on_turn = card_on_turn.face
        if close_show != -1:
            print(person_on_turn, card_on_turn)

        # 若花色相同，單純比大小 (註：此處是以字元的 Ascii 碼比對)
        if suite_for_this_turn == card_on_turn.suite:
            if face_on_turn > max_card.face:
                max_card = card_on_turn
                person_got_trick = person_on_turn

        # 挑戰者出king，而守位者非king
        elif suite_for_this_turn != card_on_turn.suite:
            if card_on_turn.suite == king:
                suite_for_this_turn = card_on_turn.suite
                max_card = card_on_turn
                person_got_trick = person_on_turn

        position += 1
        if position == 4:
            position = 0
    # end of 第一張牌丟出後的牌局

    return(person_got_trick, max_card)


def bridge_game(model, close_show):  # 牌局開始
    p = Poker()  # 建立牌組
    p.shuffle()  # 洗牌

    # 發牌
    for _ in range(13):
        for player in players:
            player.get(p.next)

    # random.shuffle(players)  # 玩家座位重排
    team_A = (players[0], players[2])  # A隊伍
    team_B = (players[1], players[3])  # B隊伍

    if close_show != -1:
        print('\n隊伍分組:\nA隊伍:{}\nB隊伍{}\n'.format(team_A, team_B))

    target_for_A = 7  # 待改 叫牌引入
    target_for_B = 14 - target_for_A
    trick_team_A = 0
    trick_team_B = 0

    position = (random.randint(0, 100) % 4)  # 隨機從某人開始，待改
    # position = 0
    # king = Function 叫牌
    # trick = 叫牌()
    king = "♠"

    while trick_team_A != target_for_A and trick_team_B != target_for_B:

        # 各回合開始
        person_got_trick, max_card = play(
            position, players, king, model, close_show)

        # 由贏的人優先出牌
        position = players.index(person_got_trick)

        if person_got_trick in team_A:
            team = "A"  # 用於下面打印
            trick_team_A += 1
        else:
            team = "B"  # 用於下面打印
            trick_team_B += 1

        if close_show != -1:
            print("本回合由{0}隊的{1}拿下，他的牌為{2}"
                  .format(team, person_got_trick, max_card))

            print("A隊墩數為{0}，B隊墩數為{1}"
                  .format(trick_team_A, trick_team_B))
            print("-"*20)
            print()

    if trick_team_A == target_for_A:
        return 1  # A隊贏了
    else:
        return 0


def control_model(count=1):
    num = 1  # 牌局執行次數，預設為1，可由model選擇修改
    close_show = 1  # 是否開啟顯示過程，預設為開啟，可由model選擇修改
    model = input("請輸入本局橋牌型態:\n\t扮演國家機器，和助手一起贏得此局，請輸入 0:\n\
\t電腦自動對戰，請輸入 1: \n\
\t測試橋牌策略，請輸入 2: \n\
\t想告白，請輸入 520:\n")

    if model == "520":
        animated_loading(1, count)  # 顯示小動畫
        count += 1
        return control_model(count)

    if model not in map(str, range(0, 3)):
        print('\n請看清楚指示\n')
        return control_model()

    if model == "1":
        # print('防錯')
        try:
            num = int(input('您希望跑幾次呢？請輸入阿拉伯數字:'))
        except:
            print('\n請輸入阿拉伯數字\n')
            return control_model()

        if num >= 10:
            try:
                close_show = int(input('\n您輸入的模擬遊戲次數過多，若要關閉顯示過程請輸入-1\n\
                    否則會跑很慢，若仍要開啟請輸入1：'))
            except:
                animated_loading(2)  # 顯示小動畫
                return control_model()

    if model == "2":
        print("施工中\n")
        return control_model()

    else:
        return (int(model), num, close_show)


# 設定玩家
# players = [Player('國家機器'), Player('韓國瑜'), Player('國家機器的助手'), Player('李佳芬')]
players = [smart('國家機器'), smart('韓國瑜'), smart('國家機器的助手'), smart('李佳芬')]
model, num, close_show = control_model()  # 此局的遊戲型態

count_A_win = 0

start_time = time.time()
for i in range(num):
    count_A_win += bridge_game(model, close_show)
    percent = (i / num) * 100
    print("目前完成{}次\t進度 | {:>5.3f}%".format(i+1, percent))
end_time = time.time()
win_ratio = count_A_win / num

print('總共執行了{}次，A隊勝利{}次，勝率為{:.5f}'.format(num, count_A_win, win_ratio))
print('共耗費{:.3f}秒'.format(end_time - start_time))
