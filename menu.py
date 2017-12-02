import os

class Menu(object):

    def __init__(self, title, items, prompt='Entrer votre choix: '):
        self._title = title
        self._items = items
        self._prompt = prompt
        self._index_hash = {i: items[k] for i, k in enumerate(items.keys())}

    def show(self):
        # os.system('cls' if os.name == 'nt' else 'clear')
        print('{0}'.format(self._title))
        print('-' * len(self._title))

        for i, item in enumerate(sorted(self._items.keys())):
            print('{0}. {1}'.format(i + 1, item))

        print()

    def get_input(self):
        try:
            idx = int(input(self._prompt)) - 1
            mthd = self._index_hash[idx]

        except (ValueError, KeyError):
            print('Erreur: Entrer un nombre entre 1 et {}'.format(len(self._items.keys())))
            print()
            self.get_input()

        else:
            try:
                mthd()

            except Exception as e:
                print(e)
