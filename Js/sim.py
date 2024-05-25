import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Projectile:
    def __init__(self, side_length=0.25, x_offset=2, z_offset=1.88, y_offset=0.0):
        self.side_length = side_length
        self.x_offset = x_offset
        self.z_offset = z_offset
        self.y_offset = y_offset
        self.g = 9.81  # acceleration due to gravity (m/s^2)


    def calculate_vertices(self):
        # Define the vertices of the equilateral triangle
        # Assume one vertex is at (0, 0, 0) and the base lies along x-axis
        vertex1 = np.array([0, 0, 0])
        vertex2 = np.array([self.length, 0, 0])
        vertex3 = np.array([self.length / 2, np.sqrt(3) * self.length / 2, 0])

        return np.array([vertex1, vertex2, vertex3])
    
    def setupProjectile(self, angle_deg, h, u):
        # Convert angle from degrees to radians
        angle_rad = np.radians(angle_deg)
        initial_height = h * np.sin(angle_rad)  # Compute initial height based on angle

        # Define time array
        t_max = 2/(u * np.cos(angle_rad))
        t = np.linspace(0, t_max, 100)

        # Compute x, y, and z positions
        x = u * np.cos(angle_rad) * t
        y = np.zeros_like(x) 
        z = initial_height + u * np.sin(angle_rad) * t - 0.5 * self.g * t**2 + 0.4*np.sin(angle_deg)

        # Filter out points where y > 0
        x = x[z >= 0]
        z = z[z >= 0]
        y = y[z >= 0]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        vertices = np.array([
            [self.x_offset, 0, self.z_offset],
            [self.x_offset + self.side_length, 0, self.z_offset],
            [self.x_offset, 0, self.z_offset + self.side_length],
            [self.x_offset, 0, self.z_offset]  # Closing the rectangle by returning to the initial vertex
        ])

        # Create a loop to close the triangle
        vertices = np.vstack([vertices, vertices[0]])


        ax.plot(vertices[:, 0], vertices[:, 1], vertices[:, 2], color='red')
        ax.set_xlabel('X (cm)')
        ax.set_ylabel('Y (cm)')
        ax.set_zlabel('Z (cm)')
        ax.set_title('Equilateral Triangle Target')


        # Plot 3D trajectory
        ax.plot(x, y, z, color='green')
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.set_title('Projectile Motion')

        plt.show()
class Target:
    def __init__(self, side_length_cm=55):


        self.side_length_cm = side_length_cm / 100  # Convert from cm to meters

        # Define the coordinates of the vertices of the equilateral triangle
        # Assume one vertex is at the origin, and the other two vertices are on the x-axis
        self.vertices = np.array([
            [0.0, 0.0, 0.0],
            [self.side_length_cm, 0.0, 0.0],
            [self.side_length_cm / 2, np.sqrt(3) * self.side_length_cm / 2, 0.0]
        ])

   

        

    def is_within_target(self, point):
        """
        Check if a given point lies within the target.
        :param point: A numpy array representing the (x, y, z) coordinates of the point.
        :return: True if the point lies within the target, False otherwise.
        """
        # Calculate vectors from the vertices to the point
        vectors_to_point = self.vertices - point
        
        # Calculate vectors between consecutive vertices
        edge1 = self.vertices[1] - self.vertices[0]
        edge2 = self.vertices[2] - self.vertices[1]
        edge3 = self.vertices[0] - self.vertices[2]
        
        # Calculate vectors from the vertices to the point
        vector_to_point1 = point - self.vertices[0]
        vector_to_point2 = point - self.vertices[1]
        vector_to_point3 = point - self.vertices[2]
        
        # Calculate the cross products of the vectors
        cross_product1 = np.cross(edge1, vector_to_point1)
        cross_product2 = np.cross(edge2, vector_to_point2)
        cross_product3 = np.cross(edge3, vector_to_point3)
        
        # Check if the cross products have the same sign (indicating the point is inside the triangle)
        if (np.dot(cross_product1, cross_product2) > 0 and np.dot(cross_product2, cross_product3) > 0 and np.dot(cross_product3, cross_product1) > 0):
            return True
        else:
            return False

# Example usage
if __name__ == "__main__":
    # Create a target
    target = Target()
    projectile = Projectile()
    projectile.setupProjectile(45, 1.2, 6)

    # Define a point to check
    test_point = np.array([2.0, 0.0, 1.0])

    # Check if the point is within the target
    if target.is_within_target(test_point):
        print("The point is within the target.")
    else:
        print("The point is outside the target.")
# Angle in degrees, initial height, initial velocity
