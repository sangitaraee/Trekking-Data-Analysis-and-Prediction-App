import streamlit as st
import time

# Example function to simulate Streamlit processing
def process_request():
    # Simulate processing time (e.g., model prediction or data processing)
    time.sleep(1)  # Sleep for 1 second to simulate processing
    return "Processed Output"

# Measure latency
start_time = time.time()
result = process_request()
end_time = time.time()

# Calculate latency
latency = end_time - start_time

# Display result and latency in Streamlit
st.write(f"Result: {result}")
st.write(f"Latency: {latency:.4f} seconds")

# Function to simulate a process in Streamlit (e.g., model prediction)
def process_request():
    # Simulate a process (this can be anything, like ML prediction or data processing)
    return "Processed Output"

# Perform reliability test
iterations = 100
errors = []

for i in range(iterations):
    try:
        result = process_request()  # Simulate processing
    except Exception as e:
        errors.append(str(e))

# Display results
st.write(f"Number of Successful Requests: {iterations - len(errors)}")
st.write(f"Number of Errors: {len(errors)}")
if errors:
    st.write(f"Errors: {errors}")


import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import time

# Function to simulate request and measure latency
def measure_latency():
    start_time = time.time()
    # Simulate some processing with a random delay between 0.5 and 1.5 seconds
    time.sleep(np.random.uniform(0.5, 1.5))
    end_time = time.time()
    return end_time - start_time

# Run latency tests and collect values
latency_values = [measure_latency() for _ in range(10)]  # Running 10 tests

# Plot the latency values using Matplotlib
fig, ax = plt.subplots()
ax.plot(latency_values, marker='o', linestyle='-', color='b')
ax.set_xlabel('Test Run')
ax.set_ylabel('Latency (seconds)')
ax.set_title('Latency of Streamlit Application (per test run)')

# Display the plot in Streamlit
st.pyplot(fig)

# Also display the latency values as text
st.write(f"Latency values: {latency_values}")
