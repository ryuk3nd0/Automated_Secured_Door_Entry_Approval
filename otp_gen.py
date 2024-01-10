import csv
import random
import string
import time

file_path = 'guest_requests.csv'
initial_rows = sum(1 for _ in open(file_path))

while True:
    with open(file_path, 'r+', newline='') as file:
        rows = list(csv.reader(file))
        current_rows = len(rows)

        if current_rows > initial_rows:
            for new_row in rows[initial_rows:]:
                if len(new_row) < 4:
                    new_row.append('')

                new_row[3] = ''.join(random.choices(string.digits, k=4))
                
            with open(file_path, 'w', newline='') as updated_file:
                csv.writer(updated_file).writerows(rows)
                print(f"OTP: {new_row[3]} generated for new entries")
                
            initial_rows = current_rows

    print("Waiting for new entries...")
    time.sleep(30)
