import random

try:
    with open('static/symbols.txt') as f:
        data = f.read().splitlines()
except FileNotFoundError:
    from finsymbols import symbols
    data = [x['symbol'].strip() for x in symbols.get_sp500_symbols()]
    with open('static/symbols.txt', 'w') as f:
        f.write('\n'.join(data))

def get_random(n=2):
    random_symbols = []
    for i in range(n):
        random_symbols.append(random.choice(data))
    return random_symbols

def random_date():
    year = random.choice(range(2013, 2024))
    month = random.choice(range(1, 13))
    if month < 10:
        month = f'0{month}'
    return f'{year}-{month}'
