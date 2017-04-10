import imagehash
import numpy as np
from PIL import Image
from itertools import combinations
from sklearn.cluster import DBSCAN
from collections import defaultdict

EXTS = ['.jpg', '.png', '.jpeg', '.gif']


def compute_hashes(files, hashfunc=imagehash.whash):
    hashes, fnames = [], []
    for i, fname in enumerate(files):
        if any(fname.endswith(ext) for ext in EXTS):
            try:
                img = Image.open(fname)
                hash = hashfunc(img)
                hashes.append(hash)
                fnames.append(fname)
            except:
                pass

    return hashes, fnames


def compute_dists(hashes):
    # precompute distance matrix
    mat = np.zeros((len(hashes), len(hashes)))
    for i, j in combinations(range(len(hashes)), 2):
        dist = hashes[i] - hashes[j]
        mat[i, j] = mat[j,i] = dist
    return mat


def cluster(mat, fnames, eps, min_samples):
    m = DBSCAN(eps=eps, min_samples=min_samples, metric='precomputed')
    labels = m.fit_predict(mat)
    clusters = defaultdict(list)
    for i, lbl in enumerate(labels):
        clusters[lbl].append(fnames[i])
    return clusters