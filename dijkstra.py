import networkx as nx
import numpy as np
from utils import haversine


class FleetOptimizer:
    def __init__(self):
        self.fleet_size = 10
        self.vehicle_capacity = 500
        self.current_routes = self._generate_fleet_routes()

    def _generate_fleet_routes(self):
        routes = []
        for i in range(self.fleet_size):
            center_lat, center_lon = 51.5074, -0.1278
            num_points = np.random.randint(3, 6)
            route = []
            for _ in range(num_points):
                lat = center_lat + np.random.uniform(-0.02, 0.02)
                lon = center_lon + np.random.uniform(-0.02, 0.02)
                route.append([lat, lon])
            routes.append(
                {
                    "id": f"Vehicle_{i + 1}",
                    "route": route,
                    "capacity_used": np.random.randint(50, 400),
                }
            )
        return routes

    def find_optimal_route(self, pickup, dropoff, weight):
        G = nx.Graph()

        # Add pickup and drop-off nodes
        G.add_node(tuple(pickup))
        G.add_node(tuple(dropoff))

        # Add existing route points as nodes and edges
        for route in self.current_routes:
            path = route["route"]
            capacity = self.vehicle_capacity - route["capacity_used"]

            for i in range(len(path)):
                G.add_node(tuple(path[i]))

                if i > 0:
                    G.add_edge(
                        tuple(path[i - 1]),
                        tuple(path[i]),
                        weight=haversine(*path[i - 1], *path[i]),
                    )

                # Connect pickup point to route point if feasible
                if capacity >= weight:
                    G.add_edge(
                        tuple(pickup),
                        tuple(path[i]),
                        weight=haversine(*pickup, *path[i]),
                    )

                # Connect route point to drop-off point if feasible
                if capacity >= weight:
                    G.add_edge(
                        tuple(path[i]),
                        tuple(dropoff),
                        weight=haversine(*path[i], *dropoff),
                    )

        # Find the shortest path using Dijkstra's algorithm
        try:
            shortest_path = nx.dijkstra_path(G, tuple(pickup), tuple(dropoff))
            shortest_distance = nx.dijkstra_path_length(
                G, tuple(pickup), tuple(dropoff)
            )
            return shortest_path, shortest_distance
        except nx.NetworkXNoPath:
            return None, float("inf")
