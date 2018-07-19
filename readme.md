super simple example of image clustering with image hashes ([wavelet hashing](https://fullstackml.com/wavelet-image-hash-in-python-3504fdd282b5) in particular) and DBSCAN.

this is an unrealistically simple example, but this clusters "brain expanding" memes from "political compass" memes pretty well.

install deps: `pip3 install -r requirements.txt`

went with wavelet hashing because of the results of my unscientific experimentation (see `tests.py`)

to run: `python3 server.py`

```
usage: server.py [-h] [-s] [--cluster distance] [--min-samples count]

Image Cluster

optional arguments:
  -h, --help           show this help message and exit
  -s, --server         run flask server (default: False)
  --cluster distance   cluster distance (default: 1)
  --min-samples count  minimum number of samples in a cluster (default: 1)
```
