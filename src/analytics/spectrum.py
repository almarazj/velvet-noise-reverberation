import numpy as np
    
    
def smoothing(F,AMP,OCT):
    ampsmooth=AMP
    if OCT!=0:
        for n in range(1,len(F)):
            f_sup=F[n]*pow(2,1/(2*OCT))  # calcula el corte superior del promedio
            f_inf=F[n]*pow(2,1/(2*OCT))  # calcula el corte inferior del promedio

            if F[-1]<=f_sup:
                idxsup=len(F)-n
            else:
                idxsup=np.argmin(abs(F[n:]-f_sup))   # busca el índice de fsup
                
            if F[1]<=f_inf:
                idxinf=np.argmin(abs(F[0:n+1]-f_inf))    # busca el ínfice de finf
            else:
                idxinf=0
                
            if idxsup!=idxinf+n:
                temp=pow(10,AMP[idxinf:idxsup+n-1]*0.1)
                ampsmooth[n]=10*np.log10(sum(temp)/(idxsup+n-idxinf))
    return ampsmooth
