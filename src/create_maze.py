import matplotlib.pyplot as plt
import numpy as np
import random
import os
import sys

# Configuration for the specific path provided
SAVE_DIR = r"C:\Users\Seratul Mustakim\Desktop\My Works\Maze\data\raw"

class PolarMaze:
    def __init__(self, rings=15, sectors=40):
        self.rings = rings
        self.sectors = sectors
        # Grid: (rings, sectors). Each cell has [bottom_wall, right_wall]
        # 1 = wall exists, 0 = wall open
        self.walls = np.ones((rings, sectors, 2), dtype=int)
        self.visited = np.zeros((rings, sectors), dtype=bool)
        
        # Define entry point (outermost ring, random sector)
        self.entry_sector = random.randint(0, sectors - 1)
        
    def get_neighbors(self, r, c):
        neighbors = []
        
        # 1. Inward (r-1, c)
        if r > 0:
            neighbors.append(('in', r - 1, c))
            
        # 2. Outward (r+1, c)
        if r < self.rings - 1:
            neighbors.append(('out', r + 1, c))
            
        # 3. Clockwise (r, c+1)
        neighbors.append(('cw', r, (c + 1) % self.sectors))
        
        # 4. Counter-Clockwise (r, c-1)
        neighbors.append(('ccw', r, (c - 1) % self.sectors))
        
        return neighbors

    def generate(self):
        """Generates maze using Recursive Backtracker algorithm"""
        stack = [(self.rings - 1, self.entry_sector)]
        self.visited[self.rings - 1, self.entry_sector] = True
        
        while stack:
            r, c = stack[-1]
            neighbors = self.get_neighbors(r, c)
            unvisited = []
            
            for direction, nr, nc in neighbors:
                if not self.visited[nr, nc]:
                    unvisited.append((direction, nr, nc))
            
            if unvisited:
                direction, next_r, next_c = random.choice(unvisited)
                
                # Knock down wall between current and next
                if direction == 'in':
                    # Current's bottom wall
                    self.walls[r, c, 0] = 0 
                elif direction == 'out':
                    # Next's bottom wall
                    self.walls[next_r, next_c, 0] = 0
                elif direction == 'cw':
                    # Current's right wall
                    self.walls[r, c, 1] = 0
                elif direction == 'ccw':
                    # Next's right wall
                    self.walls[next_r, next_c, 1] = 0
                
                self.visited[next_r, next_c] = True
                stack.append((next_r, next_c))
            else:
                stack.pop()
                
        # Create the entrance opening on the outer rim
        # We don't change the grid logic, just visual instructions later, 
        # but for verification, we assume entry is accessible.

    def verify_path(self):
        """
        Verification Function:
        Runs a Breadth-First Search (BFS) to confirm a path exists 
        from the Entry (outer ring) to the Center (ring 0).
        """
        queue = [(self.rings - 1, self.entry_sector)]
        visited_verify = set()
        visited_verify.add((self.rings - 1, self.entry_sector))
        
        found_center = False
        
        while queue:
            r, c = queue.pop(0)
            
            if r == 0:
                found_center = True
                break
            
            # Check actual open paths based on walls
            # 1. Check Inward (must have NO bottom wall at current r, c)
            if r > 0 and self.walls[r, c, 0] == 0:
                if (r-1, c) not in visited_verify:
                    visited_verify.add((r-1, c))
                    queue.append((r-1, c))
            
            # 2. Check Outward (must have NO bottom wall at r+1, c)
            if r < self.rings - 1 and self.walls[r+1, c, 0] == 0:
                if (r+1, c) not in visited_verify:
                    visited_verify.add((r+1, c))
                    queue.append((r+1, c))
                    
            # 3. Check Clockwise (must have NO right wall at r, c)
            nc = (c + 1) % self.sectors
            if self.walls[r, c, 1] == 0:
                if (r, nc) not in visited_verify:
                    visited_verify.add((r, nc))
                    queue.append((r, nc))
                    
            # 4. Check Counter-Clockwise (must have NO right wall at r, c-1)
            nc_prev = (c - 1) % self.sectors
            if self.walls[r, nc_prev, 1] == 0:
                if (r, nc_prev) not in visited_verify:
                    visited_verify.add((r, nc_prev))
                    queue.append((r, nc_prev))

        return found_center

    def save_image(self, filename):
        # Setup Figure with Black Background
        fig = plt.figure(figsize=(10, 10), facecolor='black')
        ax = fig.add_subplot(111, projection='polar')
        ax.set_facecolor('black')
        
        # Remove axis ticks/labels
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['polar'].set_visible(False)
        
        # Draw Walls
        theta = np.linspace(0, 2*np.pi, self.sectors + 1)
        
        # Width of lines
        lw = 3.0
        
        for r in range(self.rings):
            radius_inner = r
            radius_outer = r + 1
            
            for c in range(self.sectors):
                # Angle range for this sector
                theta_start = theta[c]
                theta_end = theta[c+1]
                
                # Draw Bottom Wall (Inner Arc)
                # If wall exists, draw it. (Skip r=0 inner circle as we will fill it)
                if self.walls[r, c, 0] == 1 and r > 0:
                    ax.plot([theta_start, theta_end], [radius_inner, radius_inner], 
                            color='white', linewidth=lw)
                            
                # Draw Right Wall (Radial Line)
                if self.walls[r, c, 1] == 1:
                    ax.plot([theta_end, theta_end], [radius_inner, radius_outer], 
                            color='white', linewidth=lw)

        # Draw Outer Boundary (Rim) except at entry
        for c in range(self.sectors):
            theta_start = theta[c]
            theta_end = theta[c+1]
            # If this is the entry sector, leave it open (or draw partial)
            # For this style, we just leave the arc blank
            if c != self.entry_sector:
                ax.plot([theta_start, theta_end], [self.rings, self.rings], 
                        color='white', linewidth=lw)

        # Draw the Red Target in the Center
        # We create a circle at 0,0 with radius 0.8 (slightly smaller than first ring)
        theta_fill = np.linspace(0, 2*np.pi, 100)
        ax.fill_between(theta_fill, 0, 0.6, color='#D80000', zorder=10)
        
        # Ensure directory exists
        if not os.path.exists(SAVE_DIR):
            try:
                os.makedirs(SAVE_DIR)
                print(f"Created directory: {SAVE_DIR}")
            except OSError as e:
                print(f"Error creating directory: {e}")
                return

        full_path = os.path.join(SAVE_DIR, filename)
        plt.savefig(full_path, facecolor='black', dpi=300, bbox_inches='tight', pad_inches=0.1)
        plt.close()
        print(f"Maze saved to: {full_path}")

def main():
    # 1. Initialize
    maze = PolarMaze(rings=12, sectors=36) # Adjusted to match visual density of example
    
    # 2. Generate
    maze.generate()
    
    # 3. Verify
    is_valid = maze.verify_path()
    
    if is_valid:
        print("VERIFICATION SUCCESS: A valid path from entry to center exists.")
        
        # 4. Save with random filename
        random_id = random.randint(1000, 9999)
        filename = f"maze_{random_id}.png"
        maze.save_image(filename)
    else:
        print("VERIFICATION FAILED: Maze generation error. No path found.")

if __name__ == "__main__":
    main()