import csv
import os
import matplotlib.pyplot as plt

frames = []
avg_distances = []

with open("flock_data.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["frame"] == "frame":  # optional double-check
            continue
        frames.append(int(float(row["frame"])))  # ensure numeric parsing
        avg_distances.append(float(row["avg_neighbor_distance"]))

plt.figure(figsize=(10, 5))
plt.plot(frames, avg_distances, label="Average Neighbor Distance")
plt.xlabel("Frame")
plt.ylabel("Distance")
plt.title("Flock Cohesion Over Time")
plt.legend()
plt.grid(True)

plt.savefig("data_pics/flock_plot.png")
plt.close()

