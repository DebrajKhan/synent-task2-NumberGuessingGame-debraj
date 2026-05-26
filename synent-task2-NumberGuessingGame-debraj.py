import sqlite3
import random
conn = sqlite3.connect("guessing_game.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        guess_count INTEGER,
        target_number INTEGER,
        UNIQUE(user_id, target_number),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')
conn.commit()

target_number = random.randint(1, 100)
guess_number = 0
guess_count = 0

print("Welcome to the Number Guessing Game Adventurer!")
name = input("Enter Your name adventurer: ").strip().lower()
cursor.execute('SELECT id FROM users WHERE name = ?', (name,))
user_record = cursor.fetchone()

if user_record:
    user_id = user_record[0]
    print(f"\nWelcome back {name.capitalize()}! want to guess again?")
else:
    cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
    conn.commit()
    user_id = cursor.lastrowid
    print(f"\nWelcome aboard {name.capitalize()} to the guessing game. We have generated a random number between 1 to 100 want to take a guess?")

print("Choose between YES or NO")
print("Type 1 for YES and 0 for NO")

while True:
    choice = input("enter your choice : ").strip()
    if choice in ['1', '0']:
        break
    print("Invalid input. Please type 1 for YES or 0 for NO.")



if choice == '1':
    while guess_number != target_number:
        try:
            guess_number = int(input(f"Enter your guess {name.capitalize()} : "))
        except ValueError:
            print("Error: Please enter a valid integer number.")
            continue
        
        guess_count = guess_count+1
        print() 
        
        if guess_number > target_number:
            print("lower your guess!")
        elif guess_number < target_number:
            print("higher your guess!")
        else:
            print("Perfect guess!")
            print(f"Congratulations {name.capitalize()} ! you have won the game..")
            
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO game_history (user_id, guess_count, target_number) 
                    VALUES (?, ?, ?)
                ''', (user_id, guess_count, target_number))
                conn.commit()
                print(f"\n[Game Saved! Target Number was: {target_number} | It took you {guess_count} guesses]")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                
            break

if choice == '0':
    print(f"Thank You For considering us {name.capitalize()} !")

conn.close()