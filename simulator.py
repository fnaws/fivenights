import random

try:
    with open('static/symbols.txt') as f:
        data = f.read().splitlines()
except FileNotFoundError:
    from finsymbols import symbols
    data = [x['symbol'].strip() for x in symbols.get_sp500_symbols()]
    with open('static/symbols.txt', 'w') as f:
        f.write('\n'.join(data))

def get_random(n=3):
    random_symbols = []
    for i in range(n):
        random_symbols.append(random.choice(data))
    return random_symbols
