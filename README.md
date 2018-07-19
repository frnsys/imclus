super simple example of image clustering with image hashes ([wavelet hashing](https://fullstackml.com/wavelet-image-hash-in-python-3504fdd282b5) in particular) and DBSCAN.

install deps: `pip3 install -r requirements.txt`

to run:
 - store all images in `static/img/` directory
 - empty `data` directory if u wish to do a re-run of clustering
 - run `python3 server.py --server` to do an interactive run and decide the cluster distance and min-samples count.
 - run without `--server` argument to move the images to `clusters` directory

```
usage: server.py [-h] [-s] [--cluster distance] [--min-samples count]

Image Cluster

optional arguments:
  -h, --help           show this help message and exit
  -s, --server         run flask server (default: False)
  --cluster distance   cluster distance (default: 1)
  --min-samples count  minimum number of samples in a cluster (default: 1)
```
