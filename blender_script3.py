import bpy
import json
import os
import sys


# Define the scaling factor for brick sizes
SCALE_FACTOR = 2

# Define brick sizes and colors (doubled in size)
BRICK_SIZE = {
    'type3': (3.0 * SCALE_FACTOR, 1.5 * SCALE_FACTOR, 1.0 * SCALE_FACTOR),  # Length, Height, Depth
    'type2': (2.0 * SCALE_FACTOR, 1.5 * SCALE_FACTOR, 1.0 * SCALE_FACTOR),
    'type1': (1.0 * SCALE_FACTOR, 1.5 * SCALE_FACTOR, 1.0 * SCALE_FACTOR)
}

MATERIAL_COLORS = {
    'type3': (1.0, 0.0, 0.0, 1.0),  # Red
    'type2': (0.0, 1.0, 0.0, 1.0),  # Green
    'type1': (0.0, 0.0, 1.0, 1.0)   # Blue
}

# Function to create a brick
def create_brick(position, brick_type):
    bpy.ops.mesh.primitive_cube_add(size=1, location=position)
    brick = bpy.context.object
    brick.scale = BRICK_SIZE[brick_type]

    # Assign material color
    material = bpy.data.materials.new(name=f"BrickMaterial_{brick_type}")
    material.diffuse_color = MATERIAL_COLORS[brick_type]
    if brick.data.materials:
        # Assign to existing material slot
        brick.data.materials[0] = material
    else:
        # Add new material slot
        brick.data.materials.append(material)

# JSON file path
json_file_path = r'C:\Users\Sathvika\OneDrive\Documents\VSCODE\brick_positions.json'

# Ensure the JSON file exists and is not empty
if not os.path.isfile(json_file_path) or os.path.getsize(json_file_path) == 0:
    print(f"Error: JSON file {json_file_path} is missing or empty.")
    sys.exit(1)

# Load brick positions from JSON file
with open(json_file_path, 'r') as json_file:
    try:
        data = json.load(json_file)
        wall_dimensions = data['wall_dimensions']
        brick_positions = data['brick_positions']
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        sys.exit(1)

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Define the starting point for building the wall
start_point = (0, 0, 0)

# Create bricks
for row, brick_row in enumerate(brick_positions):
    current_x = start_point[0]  # Start at x = 0 for each row
    for brick_type in brick_row:
        x = current_x + BRICK_SIZE[brick_type][0] / 2  # Adjust x based on brick size
        y = start_point[1]  # y remains constant for a row
        z = start_point[2] + row * BRICK_SIZE[brick_type][2]  # Adjust z based on row number
        create_brick((x, y, z), brick_type)
        current_x += BRICK_SIZE[brick_type][0]  # Move to the next brick position

print("3D wall created successfully")
