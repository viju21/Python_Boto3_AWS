#import section
import csv
from collections import defaultdict

# Function to read the CSV file and calculate prefix sizes
def process_csv(input_file, output_file):
    prefix_sizes = defaultdict(int)
    rows = []

    # Read the CSV file and calculate the total size for each prefix
    with open(input_file, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip header
        for row in reader:
            if len(row) < 2:  # Skip rows with fewer than 2 columns
                print(f"Skipping invalid row: {row}")
                continue
            prefix = row[0]
            try:
                size = int(row[1])
            except ValueError:
                print(f"Skipping row with invalid size value: {row}")
                continue
            prefix_sizes[prefix] += size
            rows.append(row)

    # Update serial numbers and add the total size column
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Serial Number', 'Prefix', 'Size', 'Total Size'])
        for index, row in enumerate(rows):
            serial_number = index + 1
            prefix = row[0]
            size = row[1]
            total_size = prefix_sizes[prefix]
            writer.writerow([serial_number, prefix, size, total_size])

# Main function
def main():
    input_file = 'prefix_sizes.csv'
    output_file = 'output.csv'

    print(f"Processing CSV file: {input_file}")
    process_csv(input_file, output_file)
    print(f"Updated CSV file written to: {output_file}")

if __name__ == '__main__':
    main()
