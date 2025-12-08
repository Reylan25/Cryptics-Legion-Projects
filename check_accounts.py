import sys
sys.path.insert(0, 'Cryptics_legion/src')
from core import db

conn = db.connect_db()
cur = conn.cursor()
cur.execute('SELECT id, name, currency FROM accounts WHERE user_id = 11')
rows = cur.fetchall()
print('Your Accounts:')
print('ID | Name | Currency')
print('-' * 40)
for r in rows:
    currency = r[2] if r[2] else 'NULL/Empty'
    print(f'{r[0]:3} | {r[1]:20} | {currency}')
conn.close()
