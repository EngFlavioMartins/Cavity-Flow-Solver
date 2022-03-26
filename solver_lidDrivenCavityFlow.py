# =============================================================
# Lid-driven cavity problem
# 
# Inputs:
#     nx, ny - number of grid points in x and y-directions
#     lx, ly - lengh of the channel, in non-dimensional units
#     nt     - number of time-steps
#     Re     - flow Reynold's number
#     Co     - Coarant number for soluion (should be <1)
#     my_dir - where to store the solution
# Outputs: text files containing 
#     x, y, ucc, vcc - coordinates and velocities at cell centers
#     nx, ny, nt     - as user's input
#     Axis,          - axis limits to plot results
#     uslices        - velocity profile at x[i] = constant location
#     t              - flow time
# Algorithm written by Flavio Martins (flavio.martins@outlook.com)
# =============================================================

def solve_flow(lx,ly,nx,ny,nt,Re,Co,my_dir):

      global flag_too_much_time, flag_simulation_complete

      # Import necessary public libraries:
      import numpy as np
      import matplotlib.pyplot as plt
      import time
      #from matplotlib.animation import FuncAnimation # for a future implementation...

      # Import solver libraries:
      from solverLibs.functions import initializeGrid
      from solverLibs.functions import initializeFields
      from solverLibs.functions import bc
      from solverLibs.functions import predictorStep
      from solverLibs.functions import solvePoissonEquation_2dDCT
      from solverLibs.functions import CorretorStep

      # Import plotting libraries:
      from uiLibs.plot_results import plot_velocity_field

      # Boundary conditions: they are always the same for this flow

      # Bottom surface:
      u_bot = 0
      v_bot = 0
      # Top surface:
      u_top = 1
      v_top = 0
      # Left surface
      u_lef = 0
      v_lef = 0
      # Right surface
      u_rig = 0
      v_rig = 0

      # How to plot results: create velocity profile at x[i]=uslice[i]
      uslices = [0.5]
      fig = plt.figure( figsize=(5, 5) )
      Axis = [0,lx,0,ly] # figure axis

      # =============================================================
      # Create mesh:
      # =============================================================

      x, y, dx, dy = initializeGrid(nx,ny,lx,ly)
      dt = Co*dx/u_top

      # =============================================================
      # Run solver
      # =============================================================

      u, v, ucc, vcc, p = initializeFields(nx,ny)

      ii = 0
      for t in range(nt):
      
            # Enforce boundary conditions:
            u, v = bc(u,v,u_bot,v_bot,u_top,v_top,u_lef,v_lef,u_rig,v_rig)
                  
            # Velocity predictor step:
            RHS = predictorStep(u,v,dx,dy,dt,Re)

            # Solve the pressure equation using a cosine transform approach:
            p = solvePoissonEquation_2dDCT(RHS,nx,ny,dx,dy)

            # Make the velocity field divergence free:
            u, v = CorretorStep(p,u,v,dx,dy)

            # get velocity at the cell center (for visualization)
            ucc = ( u[0:-1,1:-1] + u[1:,1:-1] )/2
            vcc = ( v[1:-1,0:-1] + v[1:-1,1:] )/2

            # Save results every n-th number of time-steps (n=10):
            if t%10 == 0:
                  # Dump all results into a text file:
                  backup_file = my_dir+'/outputs_'+ str(ii) + '.npz'
                  np.savez(backup_file,x=x ,y=y, ucc=ucc, vcc=vcc, nx=nx, ny=ny, Axis=Axis, uslices=uslices, t=t, nt=nt)
                  
                  time.sleep(1) # give the code time to write down the outputs. This is inefficient, but it is ok for now.

                  # Plot results: I have to fix this function. I will ignore it for now
                  #plot_velocity_field(backup_file)
                  #plt.tight_layout()
                  #plt.show()
                  
                  ii += 1