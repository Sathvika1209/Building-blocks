import tkinter as tk
from tkinter import ttk, messagebox
import random
import subprocess
import json
import os

# Define brick sizes and colors
BRICK_SIZE = {
    'type3': (3.0, 1.5, 1.0),  # Length, Height, Depth
    'type2': (2.0, 1.5, 1.0),
    'type1': (1.0, 1.5, 1.0)
}

MATERIAL_COLORS = {
    'type3': (1.0, 0.0, 0.0, 1.0),  # Red
    'type2': (0.0, 1.0, 0.0, 1.0),  # Green
    'type1': (0.0, 0.0, 1.0, 1.0)   # Blue
}

# Global variables to store wall dimensions and brick counts
wall_dimensions = None
brick_counts = None
brick_positions = None

# Function to draw a 2D wall
def draw_wall():
    global wall_dimensions, brick_counts, brick_positions

    # Getting input values
    try:
        width = int(width_entry.get())
        height = int(height_entry.get())
        type3 = int(type3_entry.get())
        type2 = int(type2_entry.get())
        type1 = int(type1_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid integers for all fields.")
        return

    # Check if wall construction is possible
    original_type3 = type3
    original_type2 = type2
    original_type1 = type1
    possible = True
    brick_positions = []

    for row in range(height):
        remaining_width = width
        row_bricks = []
        while remaining_width > 0:
            if remaining_width >= 15 and type3 > 0:
                row_bricks.append('type3')
                remaining_width -= 15
                type3 -= 1
            elif remaining_width >= 10 and type2 > 0:
                row_bricks.append('type2')
                remaining_width -= 10
                type2 -= 1
            elif remaining_width >= 5 and type1 > 0:
                row_bricks.append('type1')
                remaining_width -= 5
                type1 -= 1
            else:
                possible = False
                break
        if remaining_width > 0:
            possible = False
            break
        brick_positions.append(row_bricks)

    if not possible:
        messagebox.showinfo("Result", "CAN NOT BE DONE")
    else:
        # Reset brick counts to original values for drawing
        type3 = original_type3
        type2 = original_type2
        type1 = original_type1

        # Store wall dimensions and brick counts
        wall_dimensions = (width, height)
        brick_counts = {'type3': type3, 'type2': type2, 'type1': type1}

        # Create simulation window (2D WALL)
        simulation_window = tk.Toplevel(root)
        simulation_window.title("Wall Simulation")
        simulation_window.configure(bg="#F0F8FF")  # blue

        # Calculate canvas size and position to center the wall
        canvas_width = width * 10
        canvas_height = height * 30

        min_canvas_width = 600
        min_canvas_height = 400
        if canvas_width < min_canvas_width:
            canvas_width = min_canvas_width
        if canvas_height < min_canvas_height:
            canvas_height = min_canvas_height

        canvas = tk.Canvas(simulation_window, width=canvas_width, height=canvas_height, bg="#FFFACD")  # yellow
        canvas.pack(expand=True)

        scale_factor = min(canvas_width / (width * 10), canvas_height / (height * 30))

        x_offset = (canvas_width - (width * 10 * scale_factor)) / 2
        y_offset = (canvas_height - (height * 30 * scale_factor)) / 2

        rows = list(range(height))
        random.shuffle(rows)

        for row in rows:
            x = x_offset
            y = y_offset + row * 30 * scale_factor
            row_bricks = brick_positions[row]

            random.shuffle(row_bricks)

            for brick_type in row_bricks:
                if brick_type == 'type3':
                    canvas.create_rectangle(x, y, x + 150 * scale_factor, y + 30 * scale_factor, fill="red", outline="black", width=2)
                    x += 150 * scale_factor
                elif brick_type == 'type2':
                    canvas.create_rectangle(x, y, x + 100 * scale_factor, y + 30 * scale_factor, fill="green", outline="black", width=2)
                    x += 100 * scale_factor
                elif brick_type == 'type1':
                    canvas.create_rectangle(x, y, x + 50 * scale_factor, y + 30 * scale_factor, fill="blue", outline="black", width=2)
                    x += 50 * scale_factor

        with open('brick_positions.json', 'w') as json_file:
            json.dump({'wall_dimensions': wall_dimensions, 'brick_positions': brick_positions}, json_file)

# Function to handle cyclic behavior in entry fields
def cyclic_focus(event, next_widget):
    event.widget.tk_focusNext().focus_set()

# Function to draw a 3D building
def draw_3d_building():
    global wall_dimensions, brick_counts, brick_positions

    if not wall_dimensions or not brick_counts or not brick_positions:
        messagebox.showinfo("No Wall", "Please draw a 2D wall first.")
        return

    print("Brick Positions:", brick_positions)

    with open('brick_positions.json', 'w') as json_file:
        json.dump({'wall_dimensions': wall_dimensions, 'brick_positions': brick_positions}, json_file)

    blender_script_path = r'C:\Users\Sathvika\OneDrive\Documents\VSCODE\blender_script3.py'
    blender_exe_path = r"C:\Blender\blender.exe"
    json_file_path = r'C:\Users\Sathvika\OneDrive\Documents\VSCODE\brick_positions.json'

    try:
        subprocess.run([blender_exe_path, '--python', blender_script_path, '--', json_file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Blender: {e}")

# Function to add tooltips
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip_window:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self, _):
        tw = self.tooltip_window
        self.tooltip_window = None
        if tw:
            tw.destroy()

# Function to change button color on hover
def on_enter_purple_to_yellow(e):
    style.configure("HoverPurpleToYellow.TButton", background="#FFFF00", foreground="black")

def on_leave_purple_to_yellow(e):
    style.configure("HoverPurpleToYellow.TButton", background="#800080", foreground="black")

def on_enter_pink_to_blue(e):
    style.configure("HoverPinkToBlue.TButton", background="#0000FF", foreground="black")

def on_leave_pink_to_blue(e):
    style.configure("HoverPinkToBlue.TButton", background="#FFC0CB", foreground="black")

# Main application window
root = tk.Tk()
root.title("Wall Construction Simulation")
root.configure(bg="#F0F8FF")

# Add background image
background_image = tk.PhotoImage(file=r"C:\Users\Sathvika\Downloads\bg.png")
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Ensure image covers the whole window

# Heading
heading_label = tk.Label(root, text="Building Walls", font=("Helvetica", 24, "bold"), bg="#4682B4", fg="white", relief="solid", borderwidth=2)
heading_label.grid(row=0, column=0, columnspan=2, pady=20)

# Configure column weights for centering
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Input fields for wall dimensions and brick counts
font_style = ("Helvetica", 12)

tk.Label(root, text="Wall Width (in units)", font=font_style, bg="#F0F8FF").grid(row=1, column=0, padx=40, pady=40, sticky="e")
width_entry = tk.Entry(root, font=font_style, width=30)
width_entry.grid(row=1, column=1, padx=40, pady=40)
width_entry.bind("<Return>", lambda event: cyclic_focus(event, height_entry))
ToolTip(width_entry, "Enter the width of the wall in units.")

tk.Label(root, text="Wall Height (in rows)", font=font_style, bg="#F0F8FF").grid(row=2, column=0, padx=10, pady=5, sticky="e")
height_entry = tk.Entry(root, font=font_style, width=20)
height_entry.grid(row=2, column=1, padx=10, pady=5)
height_entry.bind("<Return>", lambda event: cyclic_focus(event, type3_entry))
ToolTip(height_entry, "Enter the height of the wall in rows.")

tk.Label(root, text="Type 3 Bricks (15 units)", font=font_style, bg="#F0F8FF").grid(row=3, column=0, padx=10, pady=5, sticky="e")
type3_entry = tk.Entry(root, font=font_style, width=20)
type3_entry.grid(row=3, column=1, padx=10, pady=5)
type3_entry.bind("<Return>", lambda event: cyclic_focus(event, type2_entry))
ToolTip(type3_entry, "Enter the number of Type 3 bricks (15 units).")

tk.Label(root, text="Type 2 Bricks (10 units)", font=font_style, bg="#F0F8FF").grid(row=4, column=0, padx=10, pady=5, sticky="e")
type2_entry = tk.Entry(root, font=font_style, width=20)
type2_entry.grid(row=4, column=1, padx=10, pady=5)
type2_entry.bind("<Return>", lambda event: cyclic_focus(event, type1_entry))
ToolTip(type2_entry, "Enter the number of Type 2 bricks (10 units).")

tk.Label(root, text="Type 1 Bricks (5 units)", font=font_style, bg="#F0F8FF").grid(row=5, column=0, padx=10, pady=5, sticky="e")
type1_entry = tk.Entry(root, font=font_style, width=20)
type1_entry.grid(row=5, column=1, padx=10, pady=5)
type1_entry.bind("<Return>", lambda event: cyclic_focus(event, draw_button))
ToolTip(type1_entry, "Enter the number of Type 1 bricks (5 units).")

# Style for buttons
style = ttk.Style()
style.configure("TButton", font=font_style, padding=10)
style.configure("PurpleToYellow.TButton", background="#800080", foreground="black")
style.configure("PinkToBlue.TButton", background="#FFC0CB", foreground="black")

# Buttons to draw 2D wall and 3D building
draw_button = ttk.Button(root, text="Draw 2D Wall", command=draw_wall, style="PurpleToYellow.TButton")
draw_button.grid(row=6, column=0, columnspan=2, pady=10)
ToolTip(draw_button, "Click to draw the 2D wall based on the given dimensions and brick counts.")

draw_3d_button = ttk.Button(root, text="Draw 3D Building", command=draw_3d_building, style="PinkToBlue.TButton")
draw_3d_button.grid(row=7, column=0, columnspan=2, pady=10)
ToolTip(draw_3d_button, "Click to draw the 3D building after drawing the 2D wall.")

# Change button colors on hover
draw_button.bind("<Enter>", on_enter_purple_to_yellow)
draw_button.bind("<Leave>", on_leave_purple_to_yellow)

draw_3d_button.bind("<Enter>", on_enter_pink_to_blue)
draw_3d_button.bind("<Leave>", on_leave_pink_to_blue)

# Run the application
root.mainloop()
