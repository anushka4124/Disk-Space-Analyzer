import os
import hashlib
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

# Create a Tkinter window
window = tk.Tk()
window.title("Disk Usage Analyzer")

# Variables to store data
results = []  # Store directory information

# Functions for analyzing disk usage
def get_size(path):
    total_size = 0
    total_files = 0
    total_directories = 0

    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    file_size = os.path.getsize(filepath)
                    total_size += file_size
                    total_files += 1
                    # Split the filename to get the extension
                    name, extension = os.path.splitext(filename)
                    results.append((filename, file_size, extension, filepath))
                except OSError as e:
                    print(f"Error accessing {filepath}: {e}")
            total_directories += 1
    except OSError as e:
        print(f"Error accessing {path}: {e}")

    return total_size, total_files, total_directories

# Functions for displaying results
def display_results():
    results_text.delete(1.0, tk.END)
    for i, result in enumerate(results):
        result_str = f"{i + 1}. Name: {result[0]}, Size: {result[1]} bytes, File Type: {result[2]}\n"
        results_text.insert(tk.END, result_str)

# Function for analyzing disk usage and updating the GUI
def analyze_disk_usage():
    results.clear()  # Clear previous results
    directory_path = directory_entry.get()
    if not os.path.exists(directory_path):
        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, "Invalid path. The specified directory does not exist.")
    elif not os.path.isdir(directory_path):
        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, "Invalid directory path. Please provide a valid directory path.")
    else:
        total_size, total_files, total_directories = get_size(directory_path)

        display_results()

# GUI elements
directory_label = tk.Label(window, text="Enter the directory path:")
directory_label.pack()

directory_entry = tk.Entry(window)
directory_entry.pack()

analyze_button = tk.Button(window, text="Analyze Disk Usage", command=analyze_disk_usage)
analyze_button.pack()

results_text = tk.Text(window, height=10, width=60)
results_text.pack()

# Create a graphical chart
def display_chart():
    values = [result[1] for result in results]
    categories = [result[0] for result in results]
    plt.bar(categories, values)
    plt.xlabel("Category")
    plt.ylabel("Value")
    plt.title("Disk Usage Analyzer Results")
    plt.show()

chart_button = tk.Button(window, text="Display Chart", command=display_chart)
chart_button.pack()

# Sorting and Filtering
sort_label = tk.Label(window, text="Sort by:")
sort_label.pack()

sort_option_var = tk.StringVar()
sort_option_var.set("size")
size_radio = tk.Radiobutton(window, text="Size", variable=sort_option_var, value="size")
size_radio.pack()
file_type_radio = tk.Radiobutton(window, text="File Type", variable=sort_option_var, value="file_type")
file_type_radio.pack()

filter_label = tk.Label(window, text="Filter by file type (e.g., .txt):")
filter_label.pack()

filter_entry = tk.Entry(window)
filter_entry.pack()

# Interactive Visualization
def display_interactive_chart():
    selected_index = results_text.index(tk.CURRENT)
    if selected_index:
        selected_index = selected_index.split(".")[0]  # Extract the result index
        index = int(selected_index) - 1  # Convert to 0-based index
        if 0 <= index < len(results):
            file_path = results[index][3]  # Get the file path
            os.system(f"start {file_path}")  # Open the file

chart_button = tk.Button(window, text="Open Selected File", command=display_interactive_chart)
chart_button.pack()

# Largest Files/Directories
def find_largest_items():
    largest_items = sorted(results, key=lambda x: x[1], reverse=True)
    results_text.delete(1.0, tk.END)
    for i, item in enumerate(largest_items[:10]):  # Display the top 10 largest items
        result_str = f"{i + 1}. Name: {item[0]}, Size: {item[1]} bytes, File Type: {item[2]}\n"
        results_text.insert(tk.END, result_str)

largest_files_button = tk.Button(window, text="Find Largest Files", command=find_largest_items)
largest_files_button.pack()

# Storage Recommendations
def find_duplicates(path):
    file_hashes = {}
    duplicates = []

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, "rb") as file:
                    file_hash = hashlib.md5(file.read()).hexdigest()
                if file_hash in file_hashes:
                    duplicates.append((filepath, file_hashes[file_hash]))
                else:
                    file_hashes[file_hash] = filepath
            except OSError as e:
                print(f"Error accessing {filepath}: {e}")
    return duplicates


# Function for providing storage recommendations
def storage_recommendations():
    path = directory_entry.get()
    if not os.path.exists(path):
        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, "Invalid path. The specified directory does not exist.")
    elif not os.path.isdir(path):
        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, "Invalid directory path. Please provide a valid directory path.")
    else:
        duplicates = find_duplicates(path)
        if not duplicates:
            results_text.delete(1.0, tk.END)
            results_text.insert(tk.END, "No duplicate files found.")
        else:
            results_text.delete(1.0, tk.END)
            results_text.insert(tk.END, "Duplicate files found. Recommendations:\n")
            for original, duplicate in duplicates:
                result_str = f"Suggestion: Remove {duplicate} (duplicate of {original})\n"
                results_text.insert(tk.END, result_str)

storage_recommendations_button = tk.Button(window, text="Storage Recommendations", command=storage_recommendations)
storage_recommendations_button.pack()

window.mainloop()

