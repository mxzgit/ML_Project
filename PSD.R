A = matrix(, nrow = 8, ncol = 8)
range = x <- c(1,2,3,4,5,6,7,8)
 
for (ii in x)
{
	for (jj in x) 
	{
		i <- ii-1
		j <- jj-1
		if (ii==jj){
			A[ii,jj] = 0
		}else if (i < j) {
			A[ii,jj] = (min(abs(i - j), min(i, j) + 8 - max(i, j))) * 0.25 + runif(1, 0.000001, 0.00001)
		} else {
			A[ii,jj] = A[jj,ii]
		}
		
	}
}
A
library(matrixcalc)
is.positive.semi.definite(A, tol=0.01)
