def initializeGrid(nx,ny,lx,ly):

      import numpy as np

      # Grid size (Equispaced)
      dx = lx/nx
      dy = ly/ny

      # Coordinate of each cell corners:
      x = np.linspace(0,lx,nx)
      y = np.linspace(0,ly,ny)

      # Coordinate of cell centers
      #xcc = x+dx/2
      #ycc = x+dx/2

      return x, y, dx, dy

# =======================================================

def initializeFields(nx,ny):

      import numpy as np

      u = np.zeros((nx+1,ny+2)); # x-velocity
      v = np.zeros((nx+2,ny+1)); # y-velocity
      p = np.zeros((nx,ny));     # pressure

      ucc = ( u[0:-2,1:-2] + u[1:-1,1:-2] )/2; # u at cell center
      vcc = ( v[1:-2,0:-2] + v[1:-2,1:-1] )/2;  # v at cell center

      return u, v, ucc, vcc, p

# =======================================================

def bc(u,v,u_bot,v_bot,u_top,v_top,u_lef,v_lef,u_rig,v_rig):
      # Bottom:
      u[:,0] = 2*u_bot - u[:,1]
      v[:,0] = 0

      # Top:
      u[:,-1] = 2*u_top - u[:,-2]
      v[:,-1] = 0

      # Left:
      u[0,:] = 0
      v[0,:] = 2*v_lef - v[1,:]


      # Right:
      u[-1,:] = 0
      v[-1,:] = 2*v_rig - v[-2,:]

      return u, v


# =======================================================

def predictorStep(u,v,dx,dy,dt,Re):

      import numpy as np
      
      # Calculate viscous terms:
      Lux = ( u[0:-2,1:-1] - 2*u[1:-1,1:-1] + u[2:,1:-1] )/dx**2 # nx-1 * ny
      Luy = ( u[1:-1,0:-2] - 2*u[1:-1,1:-1] + u[1:-1,2:] )/dy**2 # nx-1 * ny
      Lvx = ( v[0:-2,1:-1] - 2*v[1:-1,1:-1] + v[2:,1:-1] )/dx**2 # nx   * ny-1
      Lvy = ( v[1:-1,0:-2] - 2*v[1:-1,1:-1] + v[1:-1,2:] )/dy**2 # nx   * ny-1

      # Calculate the convective terms:

      # 1. interpolate velocity at cell center/cell cornder
      uce = ( u[0:-1,1:-1] + u[1:,1:-1] )/2
      uco = ( u[:,0:-1]    + u[:,1:]    )/2
      vco = ( v[0:-1,:]    + v[1:,:]    )/2
      vce = ( v[1:-1,0:-1] + v[1:-1,1:] )/2
      
      # 2. multiply
      uuce = np.multiply(uce,uce)
      uvco = np.multiply(uco,vco)
      vvce = np.multiply(vce,vce)

      # 3-1. get derivative for u
      Nu = (uuce[1:,:] - uuce[0:-1,:] )/dx + (uvco[1:-1,1:] - uvco[1:-1,0:-1] )/dy
      
      # 3-2. get derivative for v
      Nv = (vvce[:,1:] - vvce[:,0:-1])/dy + (uvco[1:,1:-1] - uvco[0:-1,1:-1])/dx

      # 1st order Euler integration gives the intermediate velocity
      u[1:-1,1:-1] +=  dt*(-Nu + (Lux+Luy)/Re)
      v[1:-1,1:-1] +=  dt*(-Nv + (Lvx+Lvy)/Re)

      # RHS of pressure Poisson equation:
      b = (( u[1:,1:-1] - u[0:-1,1:-1] )/dx +  ( v[1:-1,1:] - v[1:-1,0:-1] )/dy)

      return b

# =======================================================


def solvePoissonEquation_2dDCT(b,nx,ny,dx,dy):

      import numpy as np

      # Import utilities:
      from solverLibs.utilities import my_dct2
      from solverLibs.utilities import my_idct2
      from solverLibs.utilities import my_divide
      
      # modified wavenumber
      kx = np.linspace(0,nx-1,nx)
      ky = np.linspace(0,ny-1,ny)

      mwx = 2*(np.cos(np.pi*kx[:]/nx)-1)/dx**2 
      mwy = 2*(np.cos(np.pi*ky[:]/ny)-1)/dy**2

      # 2D DCT of b (Right hand side)
      fhat = my_dct2(b)

      [MWX, MWY] = np.meshgrid(mwx,mwy)
      phat = my_divide(fhat,MWX+MWY)
      

      # Inverse 2D DCT
      p = my_idct2(phat)


      return p

# =======================================================

def CorretorStep(p,u,v,dx,dy):

      # Make the velocity field divergence free: nabla dot u = 0
      #v(2:end-1,2:end-1) = v(2:end-1,2:end-1) -  (p(:,2:end)-p(:,1:end-1))/dy;

      u[1:-1,1:-1] = u[1:-1,1:-1] -  ( p[1:,:]-p[0:-1,:] )/dx
      v[1:-1,1:-1] = v[1:-1,1:-1] -  ( p[:,1:]-p[:,0:-1] )/dy

      return u, v
