# cython: boundscheck=False, wraparound=False, cdivision=True
import numpy as np
cimport numpy as np
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def pairwise_cosine(np.ndarray[np.double_t, ndim=2] X):
    cdef int n_samples = X.shape[0]
    cdef int n_features = X.shape[1]
    cdef np.ndarray[np.double_t, ndim=2] sims = np.zeros((n_samples, n_samples), dtype=np.double)
    cdef int i, j, k
    cdef double norm_i, norm_j, dot
    cdef double[:] xi, xj

    cdef np.ndarray[np.double_t, ndim=1] norms = np.zeros(n_samples, dtype=np.double)
    for i in range(n_samples):
        xi = X[i]
        norm_i = 0.0
        for k in range(n_features):
            norm_i += xi[k] * xi[k]
        if norm_i > 0:
            norms[i] = (norm_i ** 0.5)
        else:
            norms[i] = 0.0

    for i in range(n_samples):
        xi = X[i]
        for j in range(i, n_samples):
            xj = X[j]
            dot = 0.0
            for k in range(n_features):
                dot += xi[k] * xj[k]
            if norms[i] == 0 or norms[j] == 0:
                sims[i, j] = 0.0
            else:
                sims[i, j] = dot / (norms[i] * norms[j])
            sims[j, i] = sims[i, j]
    return sims
