import streamlit as st
import folium
from streamlit_folium import st_folium
import time
from dijkstra import FleetOptimizer
from utils import haversine


def draw_route(route, color, weight, dash="solid"):
    """Create a route line on the map."""
    return folium.PolyLine(
        locations=route,
        color="red" if dash == "dashed" else color,
        weight=4,
        dash_array="20" if dash == "dashed" else None,
    )


def main():
    st.set_page_config(layout="wide")
    st.title("Route Planner")

    # Initialize session state variables
    if "optimizer" not in st.session_state:
        st.session_state.optimizer = FleetOptimizer()

    if "fixed_routes" not in st.session_state:
        st.session_state.fixed_routes = (
            st.session_state.optimizer.current_routes
        )

    # Initialize other session state variables
    state_vars = [
        "pickup_point",
        "drop_point",
        "route_calculated",
        "combined_map",
        "route_info",
    ]
    for var in state_vars:
        if var not in st.session_state:
            st.session_state[var] = None

    # Display existing routes map
    st.subheader("Existing Routes")
    existing_map = folium.Map(location=[51.5074, -0.1278], zoom_start=13)

    for route in st.session_state.fixed_routes:
        for point in route["route"]:
            folium.CircleMarker(point, radius=5, color="red", fill=True).add_to(
                existing_map
            )
        draw_route(route["route"], "red", 4, "dashed").add_to(existing_map)

    route_info = [
        f"Route {r['id']} (Capacity Used: {r['capacity_used']}kg)"
        for r in st.session_state.fixed_routes
    ]
    st.selectbox("Current Routes", route_info)

    st_folium(existing_map, height=400, width="100%", key="existing_routes")

    # Location selection columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Pickup Location")
        pickup_map = folium.Map(location=[51.5074, -0.1278], zoom_start=13)

        # Add existing routes to pickup map
        for route in st.session_state.fixed_routes:
            draw_route(route["route"], "red", 4, "dashed").add_to(pickup_map)

        if st.session_state.pickup_point:
            folium.Marker(
                st.session_state.pickup_point,
                popup="Pickup",
                icon=folium.Icon(color="red"),
            ).add_to(pickup_map)

        pickup_event = st_folium(
            pickup_map, height=500, width="100%", key="pickup"
        )

        if pickup_event.get("last_clicked"):
            st.session_state.pickup_point = [
                pickup_event["last_clicked"]["lat"],
                pickup_event["last_clicked"]["lng"],
            ]
            st.session_state.route_calculated = False
            st.rerun()

        if st.session_state.pickup_point:
            st.write(
                f"Selected pickup coordinates: {st.session_state.pickup_point}"
            )

    with col2:
        st.subheader("Drop Location")
        drop_map = folium.Map(location=[51.5074, -0.1278], zoom_start=13)

        # Add existing routes to drop map
        for route in st.session_state.fixed_routes:
            draw_route(route["route"], "red", 4, "dashed").add_to(drop_map)

        if st.session_state.drop_point:
            folium.Marker(
                st.session_state.drop_point,
                popup="Drop",
                icon=folium.Icon(color="blue"),
            ).add_to(drop_map)

        drop_event = st_folium(drop_map, height=500, width="100%", key="drop")

        if drop_event.get("last_clicked"):
            st.session_state.drop_point = [
                drop_event["last_clicked"]["lat"],
                drop_event["last_clicked"]["lng"],
            ]
            st.session_state.route_calculated = False
            st.rerun()

        if st.session_state.drop_point:
            st.write(
                f"Selected drop coordinates: {st.session_state.drop_point}"
            )

    # Clear markers button
    if st.button("Clear All Markers"):
        for var in state_vars:
            st.session_state[var] = None
        st.rerun()

    # Route calculation section
    if st.session_state.pickup_point and st.session_state.drop_point:
        st.success("Both locations selected!")

        weight = st.number_input("Package Weight (kg)", 0, 500, 10)

        if (
            st.button("Calculate Route and Price")
            and not st.session_state.route_calculated
        ):
            if weight > 0:
                with st.status("Processing...") as status:
                    st.write("Optimizing fleet assignment...")
                    time.sleep(1)

                    # Find optimal route
                    optimal_route, optimal_distance = (
                        st.session_state.optimizer.find_optimal_route(
                            st.session_state.pickup_point,
                            st.session_state.drop_point,
                            weight,
                        )
                    )

                    # Calculate base distance
                    base_distance = haversine(
                        st.session_state.pickup_point[0],
                        st.session_state.pickup_point[1],
                        st.session_state.drop_point[0],
                        st.session_state.drop_point[1],
                    )

                    st.write("Calculating optimal route...")
                    time.sleep(1)

                    # Price calculation
                    base_price = base_distance * 2
                    weight_factor = 1 + (weight / 500) * 0.5

                    if optimal_route:
                        st.write("Found an optimal route! Applying discount...")
                        discount = 0.2
                    else:
                        st.write(
                            "No existing routes overlap. Calculating standard price..."
                        )
                        discount = 0

                    # Create combined map
                    combined_map = folium.Map(
                        location=[
                            (
                                st.session_state.pickup_point[0]
                                + st.session_state.drop_point[0]
                            )
                            / 2,
                            (
                                st.session_state.pickup_point[1]
                                + st.session_state.drop_point[1]
                            )
                            / 2,
                        ],
                        zoom_start=12,
                    )

                    # Show all existing routes
                    for route in st.session_state.fixed_routes:
                        draw_route(route["route"], "red", 4, "dashed").add_to(
                            combined_map
                        )

                    # Highlight the optimal route
                    if optimal_route:
                        draw_route(optimal_route, "blue", 3).add_to(
                            combined_map
                        )

                    # Add markers
                    folium.Marker(
                        st.session_state.pickup_point,
                        icon=folium.Icon(color="red"),
                    ).add_to(combined_map)
                    folium.Marker(
                        st.session_state.drop_point,
                        icon=folium.Icon(color="blue"),
                    ).add_to(combined_map)

                    # Calculate final price
                    final_price = base_price * weight_factor * (1 - discount)

                    # Store route information
                    st.session_state.route_info = {
                        "base_distance": base_distance,
                        "optimal_distance": optimal_distance,
                        "final_price": final_price,
                    }

                    st.session_state.combined_map = combined_map
                    st.session_state.route_calculated = True

                    status.update(label="Complete!", state="complete")
                    st.rerun()

        # Display route information if calculated
        if st.session_state.route_calculated and st.session_state.combined_map:
            st_folium(
                st.session_state.combined_map,
                height=400,
                width="100%",
                key="route_map",
            )

            info = st.session_state.route_info
            st.write(f"Direct distance: {info['base_distance']:.2f} km")
            st.write(
                f"Optimal route distance: {info['optimal_distance']:.2f} km"
            )
            st.write(f"Final Price: ${info['final_price']:.2f}")


if __name__ == "__main__":
    main()
