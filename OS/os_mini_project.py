import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Function to calculate total seek time and return head movement for FCFS
def FCFS(requests, head):
    seek_sequence = []
    seek_time = 0
    current_head = head
    for req in requests:
        seek_sequence.append(req)
        seek_time += abs(current_head - req)
        current_head = req
    return seek_sequence, seek_time

# Function to calculate total seek time and return head movement for SSTF
def SSTF(requests, head):
    seek_sequence = []
    seek_time = 0
    current_head = head
    requests = sorted(requests)  # Sort requests for easy selection
    while requests:
        closest = min(requests, key=lambda x: abs(x - current_head))
        seek_sequence.append(closest)
        seek_time += abs(current_head - closest)
        current_head = closest
        requests.remove(closest)
    return seek_sequence, seek_time

# Function to calculate total seek time and return head movement for SCAN
def SCAN(requests, head, disk_size, direction):
    seek_sequence = []
    seek_time = 0
    current_head = head
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    left.sort(reverse=True)
    right.sort()

    if direction == 'left':
        seek_sequence += left + [0] + right
    else:
        seek_sequence += right + [disk_size - 1] + left

    for req in seek_sequence:
        seek_time += abs(current_head - req)
        current_head = req
    return seek_sequence, seek_time

# Function to calculate total seek time and return head movement for C-SCAN
def C_SCAN(requests, head, disk_size):
    seek_sequence = []
    seek_time = 0
    current_head = head
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    left.sort()
    right.sort()

    seek_sequence += right + [disk_size - 1, 0] + left

    for req in seek_sequence:
        seek_time += abs(current_head - req)
        current_head = req
    return seek_sequence, seek_time

# Function to calculate total seek time and return head movement for LOOK
def LOOK(requests, head, direction):
    seek_sequence = []
    seek_time = 0
    current_head = head
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    left.sort(reverse=True)
    right.sort()

    if direction == 'left':
        seek_sequence += left + right
    else:
        seek_sequence += right + left

    for req in seek_sequence:
        seek_time += abs(current_head - req)
        current_head = req
    return seek_sequence, seek_time

# Function to calculate total seek time and return head movement for C-LOOK
def C_LOOK(requests, head):
    seek_sequence = []
    seek_time = 0
    current_head = head
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    left.sort()
    right.sort()

    seek_sequence += right + left  # Move in one direction only

    for req in seek_sequence:
        seek_time += abs(current_head - req)
        current_head = req
    return seek_sequence, seek_time

# Visualize head movements
def plot_seek_time(algorithm, requests, head, disk_size, direction=None):
    if algorithm == 'FCFS':
        seek_sequence, seek_time = FCFS(requests, head)
    elif algorithm == 'SSTF':
        seek_sequence, seek_time = SSTF(requests, head)
    elif algorithm == 'SCAN':
        seek_sequence, seek_time = SCAN(requests, head, disk_size, direction)
    elif algorithm == 'C-SCAN':
        seek_sequence, seek_time = C_SCAN(requests, head, disk_size)
    elif algorithm == 'LOOK':
        seek_sequence, seek_time = LOOK(requests, head, direction)
    elif algorithm == 'C-LOOK':
        seek_sequence, seek_time = C_LOOK(requests, head)

    messagebox.showinfo("Seek Time", f"Total Seek Time for {algorithm}: {seek_time}\nSeek Sequence: {seek_sequence}")

    # Plot the head movement
    plt.figure(figsize=(10, 6))
    plt.plot([head] + seek_sequence, marker='o', linestyle='-', color='b')
    plt.title(f"{algorithm} Disk Scheduling")
    plt.xlabel("Seek Sequence")
    plt.ylabel("Disk Cylinder")
    plt.grid(True)
    plt.show()

# Function to handle the simulation based on user input
def simulate():
    try:
        requests = list(map(int, entry_requests.get().split()))
        head = int(entry_head.get())
        disk_size = int(entry_disk_size.get())
        algorithm = entry_algorithm.get().upper()
        direction = entry_direction.get().lower() if algorithm in ['SCAN', 'LOOK'] else None

        # Only SCAN and LOOK require a direction
        if algorithm in ['SCAN', 'LOOK'] and direction not in ['left', 'right']:
            messagebox.showerror("Input Error", "Direction must be 'left' or 'right' for SCAN and LOOK.")
            return

        plot_seek_time(algorithm, requests, head, disk_size, direction)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for requests, head position, and disk size.")


# Setting up the GUI
root = tk.Tk()
root.title("Disk Scheduling Simulation")

tk.Label(root, text="Enter the disk requests (separated by spaces):").pack()
entry_requests = tk.Entry(root, width=50)
entry_requests.pack()

tk.Label(root, text="Enter the initial head position:").pack()
entry_head = tk.Entry(root, width=10)
entry_head.pack()

tk.Label(root, text="Enter the disk size:").pack()
entry_disk_size = tk.Entry(root, width=10)
entry_disk_size.pack()

tk.Label(root, text="Enter the disk scheduling algorithm (FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK):").pack()
entry_algorithm = tk.Entry(root, width=10)
entry_algorithm.pack()

tk.Label(root, text="Enter direction (left/right) for SCAN and LOOK:").pack()
entry_direction = tk.Entry(root, width=10)
entry_direction.pack()

tk.Button(root, text="Simulate", command=simulate).pack()

root.mainloop()




