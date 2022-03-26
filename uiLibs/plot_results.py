def plot_velocity_field(backup_file):

      import numpy as np
      import matplotlib.pyplot as plt

      # Load results:
      data = np.load(backup_file)
      xcc, ycc, ucc, vcc = data['x'], data['y'], data['ucc'], data['vcc']
      nx, Axis, uslices, t, nt = data['nx'], data['Axis'], data['uslices'], data['t'], data['nt']

      # Clean solution:
      plt.cla()

      # Calculate x-indexes to slice the data at
      nslices = np.size(uslices,axis=0)
      idx     = np.zeros((nslices,))
      for i in range(nslices):
            idx[i] = int(nx*(uslices[i] - Axis[0])/(Axis[1]-Axis[0]))

      # =============================================================
      # Plot results: u-velocity contours
      # =============================================================
      ucc = ucc.transpose()
      vcc = vcc.transpose()

      # contours of velocity magnitude:
      #[X,Y] = np.meshgrid(xcc,ycc)
      plt.contourf(xcc,ycc,ucc, 20, cmap='turbo')

      # Plot vector field:
      npoints = np.size(ucc,axis=1)
      plt.quiver(xcc[0:npoints:1],ycc[0:npoints:1],ucc[0:npoints:1],vcc[0:npoints:1],scale=10)

      # Plot velocity contours at selected locations:
      uscale = 0.7 # 0.03 # scale velocity 
      for s in range(nslices):
            i = int(idx[s])

            yline = ycc[:]
            xline = xcc[i]*np.ones((nx,))
            uline = ucc[:,i]*uscale

            plt.plot(xline, yline, '--', color='white') 
            plt.plot(uline+xline, yline, color='white') 


      # Save figure:
      plt.axis('scaled')
      plt.xlim(Axis[0],Axis[1])
      plt.ylim(Axis[2],Axis[3])
      plt.xlabel("$x/c$")
      plt.ylabel("$y/c$")
      plt.text(0.05,0.05,'Complete: ' + str(100*t/nt) + '%', bbox = dict(alpha = 0.9))

      backup_file
      
      # In case the user wants to save results automatally:
      #plt.savefig(my_dir + "/u_" + str(time) + ".png", bbox_inches='tight', dpi=450)