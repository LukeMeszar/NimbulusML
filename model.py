import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.feature_extraction import DictVectorizer
from sklearn.cluster import KMeans

def read_csv(filename):
    data = []
    with open(filename, 'rt') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        for row in datareader:
            data.append(row)
    return data[1:]

def separate_data(data):
    module_data = []
    action_data = []
    user_id_data = []
    time_data = []
    for row in data:
        module_data.append(row[0])
        action_data.append(row[1])
        user_id_data.append(row[2])
        time_data.append(row[3])
    separated_data = {"module": module_data, "action" : action_data, "user_id" : user_id_data, "time" : time_data}
    return separated_data

def process_module_data(module_data):
    le = preprocessing.LabelEncoder()
    le.fit(module_data)
    transformed_data = le.transform(module_data)
    return transformed_data

def process_action_data(action_data):
    le = preprocessing.LabelEncoder()
    le.fit(action_data)
    transformed_data = le.transform(action_data)
    return transformed_data

def process_user_id_data(user_id_data):
    le = preprocessing.LabelEncoder()
    le.fit(user_id_data)
    transformed_data = le.transform(user_id_data)
    return transformed_data

def process_time_data(time_data):
    datatime_data = []
    for datetime in time_data:
        split_on_dash = datetime.split('-')
        year = int(split_on_dash[0])
        month = int(split_on_dash[1])
        day_and_time = split_on_dash[2]
        split_on_colon = day_and_time.split(':')
        day_hour = split_on_colon[0]
        day_hour_split = day_hour.split('T')
        day = int(day_hour_split[0])
        hour = int(day_hour_split[1])
        morning_afternoon = 0
        if hour >= 12:
            morning_afternoon = 1
        date_dict = {"year" : year, "month" : month, "day" : day, "morning_afternoon" : morning_afternoon}
        datatime_data.append(date_dict)
    v = DictVectorizer(sparse=False)
    X = v.fit_transform(datatime_data)
    return X.flatten()
def k_means(data):
    k = 16
    kmeans = KMeans(n_clusters=k, random_state=0).fit(data)
    y_kmeans = kmeans.predict(data)
    plt.scatter(data[:, 0], data[:, 1], c=y_kmeans, s=50, cmap='viridis')
    centers = kmeans.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
    plt.savefig('kmean' + str(k) + '.png')

if __name__ == '__main__':
    accentus_data = read_csv('AccentusActivityLoggerTrace.csv')
    separated_data = separate_data(accentus_data)
    module_data_t = process_module_data(separated_data.get('module',[]))
    action_data_t = process_action_data(separated_data.get('action',[]))
    user_id_data_t = process_user_id_data(separated_data.get('user_id',[]))
    time_data_t = process_time_data(separated_data.get('time',[]))
    combined_data = np.array(list(zip(module_data_t, action_data_t, user_id_data_t, time_data_t)))
    k_means(combined_data)
