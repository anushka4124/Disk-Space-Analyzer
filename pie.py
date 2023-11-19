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
    labels = ['Files', 'Directories']
    sizes = [total_files, total_directories]
    colors = ['lightcoral', 'lightskyblue']
    explode = (0.1, 0)  # explode the first slice (Files)

    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
    shadow=True, startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Proportion of Files and Directories in Total Size")
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

    # Visualize results with a pie chart
    visualize_results(total_size, total_files, total_directories)


if __name__ == "__main__":
    main()
