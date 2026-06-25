import numpy as np

hfun_min = 12.0    # Grid distance (km) in refinement region


def get_hfun(longitude, latitude):
    # Refinement center location (degrees)
    center_lat, center_lon = 38.0, -95.0

    # Earth radius in MPAS-A (km)
    r_earth = 6371.229

    # Convert center location to Cartesian coordinates (unit sphere)
    x_c, y_c, z_c = geo_to_cartesian(np.radians(center_lon), np.radians(center_lat))
    p_center = np.array([x_c, y_c, z_c])

    # Convert input longitues and latitudes (radians) to Cartesian coordinates (unit sphere)
    x, y, z = geo_to_cartesian(longitude, latitude)
    p = np.column_stack((x.flatten(), y.flatten(), z.flatten()))

    # Compute distance (km) to refinement center on the unit sphere
    r = r_earth * unit_sphere_distance(p_center, p)

    # Return grid distances
    return h(r)


def h(r):
   t_begin = 2600.0         # Radial distance (km) to begin transition from fine to coarse
   t_end = 2600.0 + 1600.0  # Radial distance (km) to end transition from fine to coarse
   h_min = hfun_min         # Grid distance (km) in refinement region
   h_max = 60.0             # Grid distance (km) outside refinement region and transition

   hires_mask = r < t_begin
   transition_mask = np.logical_and(r >= t_begin, r < t_end)
   lowres_mask = r >= t_end

   ret = np.zeros_like(r)
   ret[hires_mask] = h_min
   ret[transition_mask] = h_min + (r[transition_mask] - t_begin) * (h_max - h_min) / (t_end - t_begin)
   ret[lowres_mask] = h_max

   return ret


def geo_to_cartesian(lam, phi):
    x = np.cos(lam) * np.cos(phi)
    y = np.sin(lam) * np.cos(phi)
    z = np.sin(phi)

    return (x, y, z)


def unit_sphere_distance(p, q_arr):
    return np.arccos(q_arr @ p)
