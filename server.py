import json
import numpy as np
from glob import glob
from flask import Flask, request, render_template, abort
from cluster import compute_hashes, compute_dists, cluster


if __name__ == '__main__':
    print('computing hashes & distance matrix...')
    hashes, fnames = compute_hashes(glob('static/img/*'))
    mat = compute_dists(hashes)

    np.save('data/hashes.npy', hashes)
    with open('data/fnames.json', 'w') as f:
        json.dump(fnames, f)
    np.save('data/dist_mat.npy', mat)

    clusters = {}
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        global clusters
        if request.method == 'POST':
            eps = float(request.form.get('eps', 20))
            min_samples = int(request.form.get('min_samples', 2))
            clusters = cluster(mat, fnames, eps, min_samples)
            print(clusters)
        return render_template('index.html', clusters=clusters)

    @app.route('/cluster/<int:id>', methods=['GET', 'POST'])
    def view_cluster(id):
        try:
            print(clusters[id])
            return render_template('cluster.html', cluster=clusters[id])
        except KeyError:
            abort(404)

    app.run(host='0.0.0.0', port=5001)
