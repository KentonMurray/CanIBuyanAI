#!/usr/bin/env python3
"""
Create an accurate Wheel of Fortune wheel image that matches the backend values exactly.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.patches import Wedge
import math

def create_wheel():
    # Wheel values matching backend exactly (24 sections)
    # 0 = LOSE TURN, -1 = BANKRUPT
    wheel_values = [0, -1, 500, 550, 600, 650, 700, 750, 800, 850, 900, -1, 
                   500, 550, 600, 650, 700, 750, 800, 850, 900, 500, 550, 600]
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Colors for different value types
    colors = []
    for value in wheel_values:
        if value == -1:  # BANKRUPT
            colors.append('#FF0000')  # Red
        elif value == 0:  # LOSE TURN
            colors.append('#FFA500')  # Orange
        elif value >= 800:  # High values
            colors.append('#4169E1')  # Royal Blue
        elif value >= 700:  # Medium-high values
            colors.append('#1E90FF')  # Dodger Blue
        elif value >= 600:  # Medium values
            colors.append('#00BFFF')  # Deep Sky Blue
        else:  # Lower values
            colors.append('#87CEEB')  # Sky Blue
    
    # Calculate angles for each section
    n_sections = len(wheel_values)
    angle_per_section = 360 / n_sections
    
    # Draw each section
    for i, (value, color) in enumerate(zip(wheel_values, colors)):
        # Calculate start and end angles (starting from top, going clockwise)
        start_angle = 90 - (i * angle_per_section)  # Start from top (90 degrees)
        end_angle = start_angle - angle_per_section
        
        # Create wedge
        wedge = Wedge((0, 0), 1, end_angle, start_angle, 
                     facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(wedge)
        
        # Calculate text position (middle of wedge)
        mid_angle = math.radians(start_angle - angle_per_section/2)
        text_radius = 0.7
        text_x = text_radius * math.cos(mid_angle)
        text_y = text_radius * math.sin(mid_angle)
        
        # Format text
        if value == -1:
            text = "BANKRUPT"
            fontsize = 8
            fontweight = 'bold'
            color_text = 'white'
        elif value == 0:
            text = "LOSE\nTURN"
            fontsize = 8
            fontweight = 'bold'
            color_text = 'black'
        else:
            text = f"${value}"
            fontsize = 10
            fontweight = 'bold'
            color_text = 'white' if value >= 700 else 'black'
        
        # Add text
        ax.text(text_x, text_y, text, ha='center', va='center', 
               fontsize=fontsize, fontweight=fontweight, color=color_text,
               rotation=0)
    
    # Add center circle
    center_circle = plt.Circle((0, 0), 0.15, color='gold', ec='black', linewidth=3)
    ax.add_patch(center_circle)
    
    # Add pointer at top
    pointer = patches.Polygon([(0, 1.1), (-0.05, 1.0), (0.05, 1.0)], 
                             closed=True, facecolor='red', edgecolor='black', linewidth=2)
    ax.add_patch(pointer)
    
    # Save the wheel
    plt.savefig('/workspace/project/CanIBuyanAI/images/wheel.png', 
                dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    
    print("Accurate wheel created and saved to images/wheel.png")
    print("Wheel values (24 sections):")
    for i, value in enumerate(wheel_values):
        if value == -1:
            print(f"Section {i+1}: BANKRUPT")
        elif value == 0:
            print(f"Section {i+1}: LOSE TURN")
        else:
            print(f"Section {i+1}: ${value}")

if __name__ == "__main__":
    create_wheel()