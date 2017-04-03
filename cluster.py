import imagehash
import numpy as np
from PIL import Image
from glob import glob
from itertools import combinations
from sklearn.cluster import DBSCAN
from collections import defaultdict


hashfunc = imagehash.whash

hashes, fnames = [], []
for i, fname in enumerate(glob('example/*.jpg')):
    img = Image.open(fname)
    hash = hashfunc(img)
    hashes.append(hash)
    fnames.append(fname)

# precompute distance matrix
mat = np.zeros((len(hashes), len(hashes)))
for i, j in combinations(range(len(hashes)), 2):
    dist = hashes[i] - hashes[j]
    mat[i, j] = mat[j,i] = dist

m = DBSCAN(eps=20, min_samples=1, metric='precomputed')
labels = m.fit_predict(mat)

print(mat)
print(labels)

clusters = defaultdict(list)
for i, lbl in enumerate(labels):
    clusters[lbl].append(fnames[i])
print(clusters)