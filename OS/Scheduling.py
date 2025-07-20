import matplotlib.pyplot as plt

# Process class
class Process:
    def __init__(self, pid, burst_time):
        self.pid = pid
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0

# Gantt chart drawing function
def draw_gantt_chart(gantt_chart):
    plt.figure(figsize=(10, 2))
    for idx, (pid, start, end) in enumerate(gantt_chart):
        plt.barh(0, end - start, left=start, edgecolor='black', color='lightblue')
        plt.text(start + (end - start) / 2, 0, f'P{pid}', va='center', ha='center', color='black')
    plt.xlabel('Time')
    plt.yticks([])
    plt.title('Gantt Chart')
    plt.show()

# Average time calculation
def calculate_avg_times(processes):
    total_waiting_time = sum([p.waiting_time for p in processes])
    total_turnaround_time = sum([p.turnaround_time for p in processes])
    avg_waiting_time = total_waiting_time / len(processes)
    avg_turnaround_time = total_turnaround_time / len(processes)
    return avg_waiting_time, avg_turnaround_time
def round_robin(processes, quantum):
    time = 0
    gantt_chart = []
    ready_queue = processes[:]
    waiting_queue = []

    while ready_queue or waiting_queue:
        if ready_queue:
            current_process = ready_queue.pop(0)
            if current_process.remaining_time > quantum:
                gantt_chart.append((current_process.pid, time, time + quantum))
                time += quantum
                current_process.remaining_time -= quantum
                ready_queue.append(current_process)
            else:
                gantt_chart.append((current_process.pid, time, time + current_process.remaining_time))
                time += current_process.remaining_time
                current_process.turnaround_time = time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
        else:
            time += 1  # Idle CPU time if no processes in ready queue

    draw_gantt_chart(gantt_chart)
    avg_waiting_time, avg_turnaround_time = calculate_avg_times(processes)
    return avg_waiting_time, avg_turnaround_time
def sjf(processes):
    time = 0
    gantt_chart = []
    ready_queue = sorted(processes, key=lambda p: p.burst_time)

    while ready_queue:
        current_process = ready_queue.pop(0)
        gantt_chart.append((current_process.pid, time, time + current_process.burst_time))
        time += current_process.burst_time
        current_process.turnaround_time = time
        current_process.waiting_time = current_process.turnaround_time - current_process.burst_time

    draw_gantt_chart(gantt_chart)
    avg_waiting_time, avg_turnaround_time = calculate_avg_times(processes)
    return avg_waiting_time, avg_turnaround_time
def create_processes():
    return [
        Process(pid=1, burst_time=10),
        Process(pid=2, burst_time=5),
        Process(pid=3, burst_time=8),
        Process(pid=4, burst_time=6),
    ]

if __name__ == "__main__":
    processes_rr = create_processes()
    quantum = 3
    print("Round Robin Scheduling:")
    avg_waiting_rr, avg_turnaround_rr = round_robin(processes_rr, quantum)
    print(f"Average Waiting Time (RR): {avg_waiting_rr:.2f}")
    print(f"Average Turnaround Time (RR): {avg_turnaround_rr:.2f}")
    
    processes_sjf = create_processes()
    print("\nShortest Job First Scheduling:")
    avg_waiting_sjf, avg_turnaround_sjf = sjf(processes_sjf)
    print(f"Average Waiting Time (SJF): {avg_waiting_sjf:.2f}")
    print(f"Average Turnaround Time (SJF): {avg_turnaround_sjf:.2f}")
