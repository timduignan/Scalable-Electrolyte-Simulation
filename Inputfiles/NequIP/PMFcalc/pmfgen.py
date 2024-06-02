# Initialize the prefix number
prefix_number = 1.0

# Open and read the file
with open('pe.dat', 'r') as file:
    lines = file.readlines()

    # Convert lines to a list of floats and find the last value
    num_list = [float(line.strip()) for line in lines]
    last_value = num_list[-1]

    for num in num_list:
        # Subtract the last value from the current value
        adjusted_num = num - last_value

        # Print prefix number and adjusted number
        print(f"{prefix_number} {adjusted_num}")

        # Increment the prefix number by 0.1
        prefix_number += 0.1

        # If prefix_number exceeds 9.9, reset it back to 2.0
        if prefix_number > 9.9:
            prefix_number = 2.0
