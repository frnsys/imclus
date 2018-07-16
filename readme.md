super simple example of image clustering with image hashes ([wavelet hashing](https://fullstackml.com/wavelet-image-hash-in-python-3504fdd282b5) in particular) and DBSCAN.

this is an unrealistically simple example, but this clusters "brain expanding" memes from "political compass" memes pretty well.

install deps: `pip install -r requirements.txt`

to run: `python2 server.py`

went with wavelet hashing because of the results of my unscientific experimentation (see `tests.py`)
