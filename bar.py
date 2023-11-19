import os
import matplotlib.pyplot as plt


def get_size(path):
    total_size = 0
    total_files = 0
    total_directories = 0

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                file_size = os.path.getsize(filepath)
                total_size += file_size
                total_files += 1
            except OSError as e:
                print(f"Error accessing {filepath}: {e}")
        total_directories += 1

    return total_size, total_files, total_directories


def visualize_results(total_size, total_files, total_directories):
    categories = ["Total Size (bytes)", "Total Files", "Total Directories"]
    values = [total_size, total_files, total_directories]

    plt.bar(categories, values)
    plt.xlabel("Category")
    plt.ylabel("Value")
    plt.title("Disk Usage Analyzer Results")
    plt.show()


def main():
    path = input("Enter the directory path to analyze: ")

    if not os.path.exists(path):
        print("Invalid path. The specified directory does not exist.")
        return
    if not os.path.isdir(path):
        print("Invalid directory path. Please provide a valid directory path.")
        return

    total_size, total_files, total_directories = get_size(path)

    # Display results
    print(f"Total Size: {total_size} bytes")
    print(f"Total Files: {total_files}")
    print(f"Total Directories: {total_directories}")

    # Visualize results with a bar chart
    visualize_results(total_size, total_files, total_directories)


if __name__ == "__main__":
    main()
