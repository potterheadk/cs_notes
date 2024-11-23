
1) import numpy as np
2) A= np.array([[[1,2,3,9],[4,5,6,7],[5,4,3,2]],[[7,8,9,0],[6,8,9,10],[1,2,3,4]]]) #declare array
3) A.ndim #returns dimension of array
4) A.shape #result (2,3,4)
5) # 2: how many 2D array are there
6) # 3: how many 1D array in that 2D
7) # 4: number of elements(int)in that 1D arrays
8) size in bytes : B.nbytes
9) size B.size 

------------------------------------------xx---xx---------------------------------------------
random functions

* np.arange
* np.random.permutation
* np.reshape


1)  A= np.arange(4,56,2) #start form 4 to 56 with jump of 2 print it then
2)  print(list(range(20))) #can-print-numbers-1-to-20-in-array
3) v = np.random.randint(20,50) #type(v) # = int
4) T = np.random.permutation(np.arange(10)) #arrange-integers-in-random-order-in-array 
5) A = np.random.rand(1000) #creates-random-numbers-for-hypothesis-in-statistics
6) C = np.random.rand(2,5,4,2) #4D-array
7) B = np.random.randn(100000) #creates-random-numbers-for-hypothesis-in-statistics 
8) D = np.arange(100).reshape(4,25) # 4 rows and 25 coloumns #0-to-100-numbers-print-in-4-rows-and-25-coloumns-in-array
9) T = np.arange(100).reshape(4,5,5) #4D-array-with-5-1D-arrays-consisting-5-elements-in-it

# Numpy (Slicing)

1) A = np.arange(100)
2) b = A[3:11].copy()
3) b[0]=121
4) A[::5] #it-will-start-from-0-index-till-end-and-will-pick-every-5th-element 
5) np.where(A == -1200) : #locate index number of element in np array

# linear algebra using numpy.linalg module

1) import numpy.linalg as la #linear-algebra-module-in-numpy
2) la.inv(np.random.rand(3,3))
3) A.sort(axis=0) #sorting an array as columns
4) A.sort(axis=1) #sorting an array as rows
5) more linear algebra related functions() like matrix-multi,add,substract,eigen-val etc.

# Numpy-masking(more indexing)

1) &(use for arrays),and(use for single objects)  
2) | (array) , or (single element)
3) ~ (array), not(single element)

# Numpy-Broadcasting


# Numpy(hstack-horizontal,vstack-vertical,sort(axis=0))

1) np.hstack #if-you-want-to-concate-2-different-arrays-horizontally 
2) np.vstack #vertically
3) np.sort

	* A+(np.arange(2).reshape(2,1))
	* C = np.hstack((A,B)) # give what you want to concatinate in tuple and 2 matrix will be concatinated into one horizontally

# Numpy vs normal array summing speed test

 * B = np.random.rand(10000)
 * %timeit np.sum(B) #27.2 µs ± 459 ns per loop (mean ± std. dev. of 7 runs, 10,000 loops each)
 * %timeit sum(B) #6.72 ms ± 265 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
 * #lets-define-own-function-and-see-time-difference
 * def mysum(B):
    s = 0
    for x in B:
        s=s+x
    return s
	* %timeit mysum(B) #8.11 ms ± 357 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)