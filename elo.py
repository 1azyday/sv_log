import pandas as pd
import copy
import csv

class Elo():
    # 初始化容器
    def __init__(self):
        self.k = 64
        self.classes_elo = [100] * 7
        self.class_index = ['forest', 'sword', 'dragon', 'shadow', 'rune', 'blood', 'haven']
        self.csv_list = []
        self.csv_list.append(self.class_index)
        self.csv_list.append([100] * 7)

    # Elo公式：依据积分推测双方胜率情况
    @staticmethod
    def thinked_win_rate(right_class_elo, left_class_elo):
        p = 1 / (1 + 10 ** ( - (right_class_elo - left_class_elo) / 400))
        return p

    # 给定一次胜负情况进行评价，得出Elo分的变动数值。
    def changed_elo(self, play, win, right_class_index, left_class_index):
        # print('win:', win)
        if win == '--':
                return 0
        else:
            play = int(play)
            win = int(win)
        thinked_win_rate= self.thinked_win_rate(self.classes_elo[right_class_index], self.classes_elo[left_class_index])
        changed_elo = (win / play - thinked_win_rate) * self.k
        return changed_elo

    def str_to_list(self, nparray):
        return nparray.values[0].split(' ')
        #for _ in nparray.values:
        #    list.append(_.split(' '))

    # 给定各职业胜负数据数组，转换为各职业间Elo积分变动数组
    def eval_one_changed(self, np_play, np_win):
        one_changed= []
        count = 0
        # print('np:', np_play, np_win)
        right_class_name = np_play.name.split('_')[0]
        right_class_index = self.class_index.index(right_class_name)
        play_count = self.str_to_list(np_play)
        win_count = self.str_to_list(np_win)
        while count < 7:
            left_class_index = count
            changed_elo = self.changed_elo(play_count[count], win_count[count], right_class_index, left_class_index)
            one_changed.append([changed_elo, right_class_index, left_class_index])
            count += 1

        return one_changed

    # 各职业间Elo积分变动数组进行分组统计，得出本周各职业最终Elo分变化情况。
    def eval_week_change(self, week_data):
        print('date', week_data['date'].values)
        week_change = []
        for class_name in self.class_index:
            play_row_name = '{}_play'.format(class_name)
            win_fow_name = '{}_win'.format(class_name)
            one_changed = self.eval_one_changed(week_data[play_row_name], week_data[win_fow_name])
            week_change +=  one_changed
        return week_change

    # 将最终Elo分更新到数据容器中，并记录本周变化。
    def update_elo(self, week_change):
        # print('week:', week_change)
        update_elo = [0] * 7
        #print('week_change;', week_change)
        for one_changed in week_change:
            update_elo[one_changed[1]] += one_changed[0]
            update_elo[one_changed[2]] -= one_changed[0]
        print('before:', self.classes_elo)
        #print('change1:', update_elo )
        update_elo = [class_changed / 2  for class_changed in update_elo]
        #print('change2:', update_elo )
        for index in range(7):
            self.classes_elo[index] +=  update_elo[index]
        copy_elo = copy.copy(self.classes_elo)
        self.csv_list.append(copy_elo)
        print('after:', self.classes_elo)

    # 对多周数据进行遍历，逐一迭代，计算该周Elo分变动情况，并更新。最终得出多周的Elo分拟合结果。
    def eval_some_week_change(self, somw_week_data):
        for index in range(len(somw_week_data)):
            week_data = somw_week_data[index:index + 1]
            week_change = self.eval_week_change(week_data)
            self.update_elo(week_change)

        filename = 'result.csv'
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(self.csv_list)

if __name__ == '__main__':
    batele_data = pd.read_csv('sv_battle_data.csv')
    elo = Elo()
    elo.eval_some_week_change(batele_data)