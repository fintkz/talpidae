# Talpidae: Route Optimization App

![Talpidae Logo](assets/Drilbur.png)

Talpidae is a route optimization app built using Streamlit and NetworkX. The name "Talpidae" comes from the family of moles, which are known for their ability to efficiently navigate underground tunnels. Just like moles, this app helps you find the most efficient routes through a network of existing paths.

The logo, inspired by the Drilbur Pokémon, represents the app's focus on digging through complex route networks to find the optimal path. Talpidae allows users to select pickup and drop-off locations on a map and calculates the optimal route based on existing routes and vehicle capacities. It considers factors such as capacity constraints, route overlap, and shortest path algorithms to provide the best possible routing solution

## Features

![UI](assets/ui.png)

- Interactive map for selecting pickup and drop-off locations
- Visualization of existing routes and the calculated optimal route
- Capacity constraints and route overlap considerations
- Dijkstra's algorithm for finding the shortest path
- Haversine distance calculation for accurate distances between points
- Price calculation based on distance, weight, and route overlap

## Requirements

- Python 3.7+
- Streamlit
- NetworkX
- NumPy
- Folium

## How to use

1. Clone the repository:

```
git clone https://github.com/your-username/route-optimization-app.git
cd route-optimization-app
```


2. Run the Streamlit app:

```
uv run -m streamlit run app.py --server.runOnSave true
```

3. Open the app in your web browser.

4. Select the pickup and drop-off locations on the map.

5. Enter the package weight.

6. Click the "Calculate Route and Price" button to see the optimal route and price.

## File Structure

- `app.py`: The main Streamlit app file containing the user interface and app logic.
- `dijkstra.py`: Contains the `FleetOptimizer` class and Dijkstra's algorithm implementation for finding the optimal route.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## TODO 

- Add a flag in app.py to select cities
- Add sophisticated handling for capacity considerations
- Implement dijkstra and other algorithms instead of using networkx

## License

This project is licensed under the [MIT License](LICENSE).