import json
import shutil
import numpy as np
from glob import glob
from cluster import compute_hashes, compute_dists, cluster, create_directory

import argparse
parser = argparse.ArgumentParser(description='Image Cluster')

# begin arguments
parser.add_argument('-s', '--server', action='store_true',
                    help='run flask server (default: %(default)s)\n\n')
parser.add_argument('--cluster', metavar='distance', default=1,
                    type=float, help='cluster distance (default: %(default)s)')
parser.add_argument('--min-samples', metavar='count', default=1,
                    type=int, help='minimum number of samples in a cluster (default: %(default)s)')

args = parser.parse_args()


if __name__ == '__main__':

    if not create_directory('static/img/'):
        print('Couldn\'t create static images directory!')
        raise SystemExit

    try:
        mat = np.load('data/dist_mat.npy')
        fnames = json.load(open('data/fnames.json', 'r'))
    except FileNotFoundError:
        if not create_directory('data'):
            print('Couldn\'t create data directory!')
            raise SystemExit

        print('Computing hashes & distance matrix...')
        hashes, fnames = compute_hashes(glob('static/img/*'))
        mat = compute_dists(hashes)

        np.save('data/hashes.npy', hashes)
        with open('data/fnames.json', 'w') as f:
            json.dump(fnames, f)
        np.save('data/dist_mat.npy', mat)


    if not args.server:
        eps = args.cluster
        min_samples = args.min_samples
        clusters = cluster(mat, fnames, eps, min_samples)

        print('Generated {} clusters!'.format(len(clusters)))
        print('Moving images to "clusters" directory..')
        for cluster in clusters:
            create_directory('clusters/{}'.format(cluster))
            for image in clusters[cluster]:
                shutil.move(image, 'clusters/{}/'.format(cluster))
        print('Created {} clusters and stored the images in "clusters" directory!'.format(len(clusters)))

    else:
        from flask import Flask, request, render_template, abort
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

        app.run(host='0.0.0.0', port=5002)
