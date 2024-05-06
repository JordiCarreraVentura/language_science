from collections import Counter
import pickle


class Cache:

    def __init__(self, size=5000, path='cache.p'):
        self.size = size
        self.data = dict([])
        self.calls = Counter()
        self.path = path
        self.reload()

    def reload(self):
        try:
            with open(self.path, 'rb') as f:
                self.data, self.calls = pickle.load(f)
        except FileNotFoundError:
            pass

    def persist(self):
        with open(self.path, 'wb') as f:
            pickle.dump((self.data, self.calls), f)

    def prune(self):
        excess = len(self) - self.size
        keys = sorted(
            list(self.data.keys()),
            key=lambda x: self.calls[x]
        )
        if excess < 1:
            return
        #print(f'pruned {excess}')
        while excess:
            key = keys.pop(0)
            del self.data[key]
            del self.calls[key]
            excess -= 1

    def add(self, key, val):
        self.data[key] = val
        self.prune()
        self.persist()

    def __contains__(self, text):
        self.calls[text] += 1
        return text in self.data

    def __getitem__(self, key):
        return self.data[key]

    def __len__(self):
        return len(self.data)



if __name__ == '__main__':

    cache = Cache(size=3)

    e1 = (1, 'uno')
    e2 = (2, 'dos')
    e3 = (3, 'tres')
    e4 = (4, 'cuatro')
    e5 = (5, 'cinco')

    tests = [
        e1, e2, e1, e1,
        e3, e4, e2, e3,
        e5
    ]

    for key_val in tests:
        key, val = key_val

        cached = key in cache

        print()
        print(len(cache), 'current elements')
        if cached:
            print('cached: ', key, val)
        else:
            print('not cached: ', key, val)
        cache.add(key, val)
        print(len(cache), 'outgoing elements')
        print(cache.calls.most_common())
        print(cache.data.keys())

