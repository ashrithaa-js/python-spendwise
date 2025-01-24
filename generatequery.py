import random
import datetime

# Function to generate random data
def generate_random_data():
    categories = ['food', 'travel', 'education', 'shopping', 'entertainment']
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 12, 31)
    data = []
    for i in range(1, 1001):
        date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
        category = random.choice(categories)
        amount = round(random.uniform(10.0, 500.0), 2)
        data.append(f"{i}|{date.strftime('%d-%m-%Y')}|{category}|{amount}|")
    return data

# Generate random data
random_data = generate_random_data()

# Write data to file
with open('generated_data.txt', 'w') as f:
    for entry in random_data:
        f.write(entry + '\n')

print("Generated 1000 data entries with continuous serial numbers, different dates of 2024, different categories, and random prices.")
