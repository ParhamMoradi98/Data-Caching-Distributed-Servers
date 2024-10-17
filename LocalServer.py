import pickle
import os
import numpy as np


def read_pickle(path: str):
    with open(path + '.pickle', 'rb') as f:
        data = pickle.load(f)
    return data


def save_pickle(data, path: str):
    with open(path + '.pickle', 'wb') as f:
        pickle.dump(data, f)
    pass


class LocalServer:
    distribution_param = 1
    cash_size = 10
    max_life_time = 5
    cnt = 0

    def __init__(self, name: str, fav):
        self.favorite = fav
        self.name = name
        self.data = {}
        if os.path.exists('database/' + self.name + '.pickle'):
            self.data = read_pickle('database/' + self.name)
            print(f'{name} already exist: ', self.data)
        else:
            self.data = {}
            save_pickle(self.data, 'database/' + self.name)
            print(f'{name} created')

        if os.path.exists('database/cnt/' + self.name + '.pickle'):
            self.cnt = read_pickle('database/cnt/' + self.name)
        else:
            self.cnt = 0
            save_pickle(self.cnt, 'database/cnt/' + self.name)

    def update(self):
        for each in self.data:
            self.data[each] += 1

    def request_data(self, key):
        if key in self.data:
            return self.data[key]
        return 1024

    def upgrade(self, key, val):
        if key in self.data:
            print(f'server {self.name} upgraded')
            self.data[key] = val

    def set_data(self, key, val):
        if len(self.data) >= self.cash_size:
            del self.data[max(self.data, key=self.data.get)]
        self.data[key] = val

    def ask_main_server(self, cache_size, threshold):
        n = np.random.randint(0, cache_size - 1, 1, np.uint8)[0]
        while self.request_data(n) < threshold:
            n = np.random.randint(0, cache_size - 1, 1, np.uint8)[0]
        if self.cnt > 5:
            n = self.favorite
            self.cnt = 0
        self.cnt += 1
        return n

    def __del__(self):
        save_pickle(self.data, 'database/' + self.name)
        save_pickle(self.cnt, 'database/cnt/' + self.name)
