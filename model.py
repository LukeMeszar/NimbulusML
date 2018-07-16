import csv

def read_csv(filename):
    data = []
    with open(filename, 'rt') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        for row in datareader:
            data.append(row)
    return data[1:]

def fix_data(data):
    new_data = []
    over_counter = 0
    for row in data:
        if len(row) == 4:
            new_data.append(row)
    with open('new_data.csv', 'wt', newline='') as csvfile:
        datawriter = csv.writer(csvfile, delimiter=',')
        for item in new_data:
            datawriter.writerow(item)

def separate_data(data):
    module_data = []
    action_data = []
    user_id_data = []
    time_data = []
    exception_list = []
    for row in data:
        module_data.append(row[0])
        action_data.append(row[1])
        user_id_data.append(row[2])
        try:
            time_data.append(row[3])
        except Exception as e:
            exception_list.append(row[0])
    print(module_data[0:2], len(module_data))
    print(action_data[0:2], len(action_data))
    print(user_id_data[0:2], len(user_id_data))
    print(time_data[0:2], len(time_data))


if __name__ == '__main__':
    accentus_data = read_csv('AccentusActivityLoggerTrace.csv')
    #fix_data(accentus_data)
    separate_data(accentus_data)
