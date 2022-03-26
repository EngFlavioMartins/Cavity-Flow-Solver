import tkinter as tk
from tkinter import DISABLED, filedialog
from tkinter import messagebox

import matplotlib.pyplot as plt
from   matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

#=================================================================
# Flags and other variables:
#=================================================================
t = 0                        # simulation time

flag_dir_was_selected = 0    # flag if directory was selected or not
flag_simulation_complete = 0 # flag for a simulation that was completed
flag_too_much_time = 0       # flag for a simulation that is taken too long
flag_all_inputs_are_ok = 0   # all inputs are ok

#=================================================================
# Seet size of the software:
#=================================================================
my_colour = '#F7F4EF'
second_colour = '#F7F4EF'
root = tk.Tk()
root['bg'] = my_colour
root.title("Lid-driven cavity flow solver v.: 0.1")
root.iconbitmap("./uiLibs/smoke_icon.ico")
root.geometry("800x550")

# Configure the weight size of each column and row:
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=7)

#=================================================================
# Define sub-functions:
#=================================================================

# Submit inputs to solver and plot grid:
def submit():
      global flag_all_inputs_are_ok
      # Check if all entries were given by the user:
      my_check = len(e_nx.get())*len(e_ny.get())*len(e_lx.get())*len(e_ly.get())*len(e_co.get())*len(e_nt.get())*len(e_re.get())

      
      if my_check == 0: # If at least on entry is null:
            messagebox.showinfo('Message', 'Please, check for empty entries.')
      else:             # otherwise, pass info to algorithm and display grid to user
            global nx, ny, lx, ly, co, nt, re

            # Get values from input box:
            re = float(e_re.get()) # Reynolds number
            lx = float(e_lx.get()) # number of grid-point in x-dir
            ly = float(e_ly.get()) # number of grid-point in x-dir
            co = float(e_co.get()) # number of time-steps
            nt = int(e_nt.get())   # number of time-steps
            nx = int(e_nx.get())   # number of grid-point in x-dir
            ny = int(e_ny.get())   # number of grid-point in x-dir

            # Inform user:
            flag_all_inputs_are_ok = 1
            l_sub.pack(anchor="e", side="right", padx=5, pady=5) # print label stating that all is good with the inputs

            # Plot grid:
            xgrid = np.linspace(0,lx,nx)
            ygrid = np.linspace(0,ly,ny)

            ax.clear()
            [ax.axhline(y=i, linestyle='-.') for i in xgrid]
            [ax.axvline(x=i, linestyle='-.') for i in ygrid]
            ax.set_ylabel(r'$ly$')
            ax.set_xlabel(r'$lx$')
            ax.set_title(r"$U \rightarrow$")
            ax.set_aspect('equal', 'box')
            canvas.draw_idle()

            # Switch state of button Run:
            if flag_dir_was_selected and flag_all_inputs_are_ok:
                  switchButtonRunState()
                             
#=================================================================

def select_dir():
      global my_dir
      global flag_dir_was_selected

      my_dir = filedialog.askdirectory()

      # Print directory:
      e_dir.configure(fg='#000000') # change color of button after click
      e_dir.delete(0,'end')         # delete initial entry
      e_dir.insert(0,my_dir)        # show current directory on entry widget
      flag_dir_was_selected = 1     # flag for selection of directory

#=================================================================

def switchButtonRunState():
      button_run['state'] = tk.NORMAL

#=================================================================

def run():
      #Disable run button again:
      button_run['state'] = tk.DISABLED
      my_dir = str(e_dir.get()) # get directory to save solutions at:

      # Run simulation!
      from solver_lidDrivenCavityFlow import solve_flow
      solve_flow(lx,ly,nx,ny,nt,re,co,my_dir) # solve flow!

      if flag_too_much_time:
            messagebox.showinfo('Message', 'Simulation failed.')
      else:
            messagebox.showinfo('Message', 'Simulation complete!')
            
#=================================================================
# Create three frames:
#=================================================================
# Create frames:
frame_inputs = tk.LabelFrame(root, text='Inputs', relief="sunken", bg=second_colour)
frame_run    = tk.LabelFrame(root, text='Run', relief="sunken", bg=my_colour)
frame_visual = tk.LabelFrame(root, text='Computational grid',   relief="sunken", bg=my_colour)

# Position frames into the grid (0,0) = top-right corner:
frame_inputs.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
frame_run.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
frame_visual.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

#=================================================================
# Frame inputs:
#=================================================================

l_nx = tk.Label(frame_inputs, text="Enter number of elements in x-direction, nx:", anchor="nw")
e_nx = tk.Entry(frame_inputs, width=10, borderwidth=3)
e_nx.insert(0,'32')

l_ny = tk.Label(frame_inputs, text="Enter number of elements in y-direction, ny:", anchor="nw")
e_ny = tk.Entry(frame_inputs, width=10, borderwidth=3)
e_ny.insert(0,'32')

l_lx = tk.Label(frame_inputs, text="Enter x-dimension of the cavity, lx:", anchor="nw")
e_lx = tk.Entry(frame_inputs, width=10, borderwidth=3)
e_lx.insert(0,'1')

l_ly = tk.Label(frame_inputs, text="Enter y-dimension of the cavity, ly:", anchor="nw")
e_ly = tk.Entry(frame_inputs, width=10, borderwidth=3)
e_ly.insert(0,'1')

l_nt = tk.Label(frame_inputs, text="Enter number of time-steps, nt:", anchor="nw")
e_nt = tk.Entry(frame_inputs, width=10, borderwidth=3)
e_nt.insert(0,'100')

l_co = tk.Label(frame_inputs, text="Enter target Coarant number, Co:", anchor="nw")
e_co = tk.Entry(frame_inputs, width=10, borderwidth=3)
e_co.insert(0,'0.9')

l_re = tk.Label(frame_inputs, text="Enter Reynolds number:", anchor="nw")
e_re = tk.Entry(frame_inputs, width=10, borderwidth=3)
e_re.insert(0,'300')

buttun_sub = tk.Button(frame_inputs, text="Submit", command=submit)
l_sub = tk.Label(frame_inputs, text="All inputs are ok.", anchor="nw")

# Put stuff in the frame:
l_nx.pack(side="top", padx=5, fill='x')
e_nx.pack(side="top", padx=5, fill="both")

l_ny.pack(side="top", fill='x', padx=5, pady=(15,0))
e_ny.pack(side="top", padx=5, fill="both")

l_lx.pack(side="top", fill='x', padx=5, pady=(15,0))
e_lx.pack(side="top", padx=5, fill="both")

l_ly.pack(side="top", fill='x', padx=5, pady=(15,0))
e_ly.pack(side="top", padx=5, fill="both")

l_nt.pack(side="top", fill='x', padx=5, pady=(15,0))
e_nt.pack(side="top", padx=5, fill="both")

l_co.pack(side="top", fill='x', padx=5, pady=(15,0))
e_co.pack(side="top", padx=5, fill="both")

l_re.pack(side="top", fill='x', padx=5, pady=(15,0))
e_re.pack(side="top", padx=5, fill="both")

buttun_sub.pack(anchor="e", side="left", padx=5, pady=5)

#=================================================================
# Run frame:
#=================================================================

# Show currently selected directory:
e_dir = tk.Entry(frame_run, borderwidth=3, width=60, fg='#adadad')
e_dir.insert(0,"Select directory to store solution files:")

# Show currently selected directory:
buttun_dir = tk.Button(frame_run, text="Select", command=select_dir)
button_run = tk.Button(frame_run, text="Run", command=run, state=DISABLED)

# Insert stuff in the frame:
buttun_dir.pack(anchor="e", side="left", padx=5, pady=5)
e_dir.pack(side="left", padx=5, pady=5, fill="x")
button_run.pack(anchor="e", side="right", padx=5, pady=5)

#=================================================================
# Plot frame:
#=================================================================
# Create figure with background matching software's background:
fig, ax = plt.subplots(figsize=(4, 4) )
fig.patch.set_facecolor(my_colour)
ax.set_facecolor(my_colour)

canvas = FigureCanvasTkAgg(fig, master=frame_visual)  # A tk.DrawingArea.
canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
toolbar = NavigationToolbar2Tk(canvas, frame_visual)


root.mainloop()