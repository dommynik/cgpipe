import os
import pathlib
import tarfile
import urllib.request

import numpy as np
import scipy.io as scio
import scipy.sparse as scsp


def load_npz(filename: str):
    loader = np.load(filename)
    return scsp.csr_matrix((loader['data'], loader['indices'], loader['indptr']), shape=loader['shape'])


def save_npz(filename: str, mtx_data):
    np.savez(filename, data=mtx_data.data, indices=mtx_data.indices, indptr=mtx_data.indptr, shape=mtx_data.shape)


def load_matrix(url: str, hint_filename: str = None):
    if not os.path.isdir('data'):
        os.mkdir('data')

    file_name = url.split('?')[0].split('/')[-1]
    mtx_name = file_name.replace('.tar.gz', '')

    if not os.path.isfile('data/' + file_name):
        urllib.request.urlretrieve(url, 'data/' + file_name)

    tar = tarfile.open('data/' + file_name)
    tar.extractall('data/')

    if hint_filename is not None and os.path.isfile('data/' + mtx_name + '/' + hint_filename):
        try:
            mtx_data = load_npz('data/' + mtx_name + '/' + hint_filename + '.npz')
            return mtx_data
        except IOError:
            mtx_data = scio.mmread('data/' + mtx_name + '/' + hint_filename).tocsr()
            save_npz('data/' + mtx_name + '/' + hint_filename, mtx_data)
            return mtx_data

    for mtx_file in pathlib.Path('data/' + mtx_name).glob('**/*.mtx'):
        try:
            mtx_data = load_npz(str(mtx_file) + '.npz')
            return mtx_data
        except IOError:
            mtx_data = scio.mmread(str(mtx_file)).tocsr()
            save_npz(mtx_file, mtx_data)
            return mtx_data
