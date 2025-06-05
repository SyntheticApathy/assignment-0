from dataclasses import dataclass
import pygame
from statistics import fmean
from vi import Agent, Config, Simulation
import os
import csv


@dataclass
class FlockingConfig(Config):
    alignment_weight: float = 1
    cohesion_weight: float = 1
    separation_weight: float = 1
    delta_time: float = 3
    mass: int = 20
    max_vel: int = 30

    def weights(self) -> tuple[float, float, float]:
        return self.alignment_weight, self.cohesion_weight, self.separation_weight


class FlockingAgent(Agent):
    config: FlockingConfig
    log_file_path = "flock_data.csv"
    counter = 0
    has_logged_header = False


    def average_neighbor_distance(self) -> float:
        neighbors = list(self.in_proximity_accuracy())
        if not neighbors:
            return 0.0
        distances = [self.pos.distance_to(agent.pos) for agent, _ in neighbors]
        return sum(distances) / len(distances)


    def get_weigths(self) -> tuple[float, float, float]:
        return self.config.weights()

    def change_position(self):
        #keep to 10,000 time steps
        if FlockingAgent.counter > 10000:
            pygame.quit()
            exit()
       

        #logging for testing into csv file

        if self.id == 0:  # Log only once per frame from one agent
            avg_dist = self.average_neighbor_distance()
            write_header = not FlockingAgent.has_logged_header

            with open(FlockingAgent.log_file_path, mode="a", newline="") as f:
                writer = csv.writer(f)
                if write_header:
                    writer.writerow(["frame", "avg_neighbor_distance"])
                    FlockingAgent.has_logged_header = True
                writer.writerow([FlockingAgent.counter, avg_dist])
                FlockingAgent.counter += 1



        neighbors = list(self.in_proximity_accuracy())
        if not neighbors:
            self.pos += self.move * self.config.delta_time
            self.there_is_no_escape()
            return

        alignment = pygame.math.Vector2(0, 0)
        cohesion = pygame.math.Vector2(0, 0)
        separation = pygame.math.Vector2(0, 0)

        for agent, _ in neighbors:
            alignment += agent.move
            cohesion += agent.pos
            separation += self.pos - agent.pos

        one_by_N = 1 / len(neighbors)

        alignment = (one_by_N * alignment) - self.move
        cohesion_center = one_by_N * cohesion
        cohesion = (cohesion_center - self.pos) - self.move
        separation = one_by_N * separation

        w_align, w_coh, w_sep = self.get_weigths()

        total_force = (alignment * w_align + cohesion * w_coh + separation * w_sep) / self.config.mass
        self.move += total_force

        if self.move.length_squared() > 0:
            self.move = self.move.normalize() * min(self.move.length(), self.config.max_vel)

        self.pos += self.move * self.config.delta_time
        self.there_is_no_escape()


# Final Stage 1 Setup for Visualization and Testing
Simulation(
    FlockingConfig(
        image_rotation=True,
        movement_speed=1,
        radius=50,
        alignment_weight=1.0,
        cohesion_weight=1.0,
        separation_weight=1.5,
        delta_time=3,
        mass=20,
        max_vel=30
    )
).batch_spawn_agents(
    50,
    FlockingAgent,
    images=["images/triangle.png"]
).run()
