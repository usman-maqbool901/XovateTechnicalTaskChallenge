import pandas as pd
import numpy as np
import os
import time

def generate_large_csv_vectorized(output_file, target_rows=10000000):
    start_time = time.time()
    
    departments = ['Engineering', 'Sales', 'Marketing', 'HR']
    first_names = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'Chris', 'Anna', 'Robert', 'Jessica']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    print(f"Generating {target_rows} rows to {output_file} using vectorized operations...")
    
    # Generate random indices for vectorization
    np.random.seed(42)
    
    ids = np.arange(1001, 1001 + target_rows)
    
    # Choose random names, ages, and departments in bulk
    f_indices = np.random.randint(0, len(first_names), size=target_rows)
    l_indices = np.random.randint(0, len(last_names), size=target_rows)
    ages = np.random.randint(18, 66, size=target_rows)
    dept_indices = np.random.randint(0, len(departments), size=target_rows)
    
    # Map indices to actual values
    f_names = np.array(first_names)[f_indices]
    l_names = np.array(last_names)[l_indices]
    chosen_depts = np.array(departments)[dept_indices]
    
    # Vectorized string concatenation for names
    names = np.char.add(np.char.add(f_names, ' '), l_names)
    
    # Create DataFrame
    # Note: email generation with list comprehension is still faster than some vectorized string ops for this specific pattern
    df = pd.DataFrame({
        'id': ids,
        'name': names,
        'email': [f"user.{i}@xovate-large.com" for i in range(1, target_rows + 1)],
        'age': ages,
        'department': chosen_depts
    })
    
    # Write to CSV
    df.to_csv(output_file, index=False)
    
    end_time = time.time()
    print(f"Generation complete in {end_time - start_time:.2f} seconds!")

if __name__ == "__main__":
    output_directory = "/Users/mac/Desktop/Xovate TechnicalTaskChallenge /data"
    output_path = os.path.join(output_directory, "test_data_large.csv")
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    generate_large_csv_vectorized(output_path)
