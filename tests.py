import imagehash
from PIL import Image
from glob import glob
from itertools import combinations

imgs = [(Image.open(fname), fname) for fname in glob('example/*.jpg')]

for name, hashfunc in [
    ('phash', imagehash.phash),
    ('ahash', imagehash.average_hash),
    ('dhash', imagehash.dhash),
    ('whash', imagehash.whash),
    ('whash-db4', lambda img: imagehash.whash(img, mode='db4'))
]:
    print('hashfunc:', name)
    hashes = [(hashfunc(im), fname) for im, fname in imgs]
    pairs = combinations(hashes, 2)
    true_sim_dists = []
    true_dif_dists = []
    for (a, a_n), (b, b_n) in pairs:
        # pc=political compass
        if 'pc' in a_n or 'pc' in b_n:
            true_dif_dists.append(a - b)
        else:
            true_sim_dists.append(a - b)
        print(a_n, b_n, ':', a - b)

    # want the `max sim dist` to be less than
    # the `min dif dist`. the bigger the gap, the better
    print('min dif dist:', min(true_dif_dists))
    print('max sim dist:', max(true_sim_dists))
    print('clean split?:', max(true_sim_dists) < min(true_dif_dists))
    print('---')