import pickle
import os
import numpy as np


def save_pickle(data, path: str):
    with open(path + '.pickle', 'wb') as f:
        pickle.dump(data, f)
    pass


def read_pickle(path: str):
    with open(path + '.pickle', 'rb') as f:
        data = pickle.load(f)
    return data


def count(l: list, n):
    c = 0
    for i in l:
        if i == n:
            c += 1
    return c


def delete(l: list, n):
    return [i for i in l if i != n]


class MainServer:
    queue = {}
    cash_size = 50
    round_requests = {}
    threshold = 0.5

    def __init__(self, name):
        self.name = name
        if os.path.exists(f'database/{self.name}.pickle'):
            self.data = read_pickle(f'database/{self.name}')
            print(f'{self.name} server already exist')
            print(self.data)
        else:
            self.data = {}
            for i in range(self.cash_size):
                self.data[i] = 0
            save_pickle(self.data, f'database/{self.name}')
            print(f'{self.name} server created')

        if os.path.exists(f'database/{self.name}queue.pickle'):
            self.queue = read_pickle(f'database/{self.name}queue')

    def submit_request(self, owner, key, val):
        self.round_requests[owner] = [key, val]
        if owner in self.queue:
            self.queue[owner] += [key]
        else:
            self.queue[owner] = [key]

    def update(self):
        for key in self.data:
            if np.random.rand() > self.threshold:
                self.data[key] = 0
            else:
                self.data[key] += 1

        self.round_requests = {}

    def process(self):
        tmp = {}
        for k, v in self.round_requests.items():
            self.round_requests[k] = [v[0], self.data[v[0]], v[1] - self.data[v[0]]]
            tmp[k] = count(self.queue[k], v[0]) + self.round_requests[k][2]
        mood_1 = max(self.round_requests, key=lambda x: self.round_requests[x][2])
        mood_2 = max(tmp, key=lambda x: tmp[x])
        self.queue[mood_2] = delete(self.queue[mood_2], self.round_requests[mood_2][0])
        return self.round_requests, mood_1, [mood_2, tmp[mood_2] - self.round_requests[mood_2][2]]

    def process_2(self):
        print(self.round_requests)
        tmp = {}
        for k, v in self.round_requests.items():
            self.round_requests[k] = [v[0], self.data[v[0]], v[1] - self.data[v[0]]]
            tmp[k] = count(self.queue[k], v[0]) + self.round_requests[k][2]
        tmp_sorted = sorted(tmp, key=lambda x: tmp[x], reverse=True)
        mood_2 = {}
        for i in tmp_sorted:
            mood_2[i] = tmp[i] - self.round_requests[i][2]
        for c, f in enumerate(mood_2):
            if c > 2:
                break
            self.queue[f] = delete(self.queue[f], self.round_requests[f][0])
        return self.round_requests, mood_2

    def get_data(self, key):
        return self.data[key]

    def __del__(self):
        save_pickle(self.data, f'database/{self.name}')
        save_pickle(self.queue, f'database/{self.name}queue')
