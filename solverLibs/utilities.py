def my_dct2(A):
      import numpy as np
      from scipy.fftpack import idct, dct

      # Perform the 2-dimensional direct cosine transform with orthonormal normalization:
      B = np.transpose(  dct(  np.transpose(dct(A,norm='ortho')), norm='ortho'  )  )

      return B

def my_idct2(A):
      import numpy as np
      from scipy.fftpack import idct, dct

      # Perform the inverse 2-dimensional direct cosine transform with 
      # orthonormal normalization:
      B = np.transpose( idct( np.transpose(  idct(A,norm='ortho') ), norm='ortho' ) )
      
      return B

def my_divide(A,B):
      import numpy as np
      from scipy.fftpack import idct, dct

      # Perform element wise division of matrix A by B, Aij/Bij, such that matrix B is a 
      # numpy meshgrid 2-dimensional array
      B = B.transpose()
      C = np.divide(A, B, out=np.zeros_like(A), where=B!=0) # prevent division by zero!

      return C