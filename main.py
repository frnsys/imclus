import os
import json
import shutil
import imagehash
import numpy as np
from PIL import Image
from glob import glob
from tqdm import tqdm
from itertools import combinations
from sklearn.cluster import DBSCAN
from collections import defaultdict


hashfunc = imagehash.whash
hashes, fnames = [], []

print('hashing...')
for fname in tqdm(glob('posts/*')):
    if any(fname.endswith(ext) for ext in ['.jpg', '.png', '.jpeg', '.gif']):
        try:
            img = Image.open(fname)
            hash = hashfunc(img)
            hashes.append(hash)
            fnames.append(fname)
        except:
          pass

# precompute distance matrix
print('computing dist matrix...')
mat = np.zeros((len(hashes), len(hashes)))
for i, j in tqdm(combinations(range(len(hashes)), 2)):
    dist = hashes[i] - hashes[j]
    mat[i, j] = mat[j,i] = dist

print('clustering...')
m = DBSCAN(eps=10, min_samples=1, metric='precomputed')
labels = m.fit_predict(mat)

clusters = defaultdict(list)
for i, lbl in enumerate(labels):
    clusters[str(lbl)].append(fnames[i])

print('clusters:', len(clusters))

# save clusters to json
with open('clusters.json', 'w') as f:
    json.dump(clusters, f)

# generate directory structure/html
# so clusters can be browsed in the browser
html_list = []
for id, members in clusters.items():
    dir = 'clusters/{}'.format(id)
    html_list.append('<li><a href="{0}">{0}</a> ({1})</li>'.format(id, len(members)))
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)
    html = []
    for path in members:
        fname = os.path.basename(path)
        shutil.copy(path, os.path.join(dir, fname))
        html.append('<img src="{}">'.format(fname))
    with open(os.path.join(dir, 'index.html'), 'w') as f:
        f.write(''.join(html))
with open('clusters/index.html', 'w') as f:
    f.write('<ul>{}</ul>'.format(''.join(html_list)))