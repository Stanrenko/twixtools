import os
import numpy as np
import tempfile
import unittest
from twixtools import twixzip, read_twix
from twixtools.mdh_def import is_flag_set
from twixtools.twixzip import suppress_stdout_stderr

def md5(fname):
    import hashlib
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.digest()


class test_lossless(unittest.TestCase):

    def test(self):
        infile = 'test/singlechannel.dat'
        md5_orig = md5(infile)

        with tempfile.NamedTemporaryFile(suffix='.dat') as out_dat:
            with tempfile.NamedTemporaryFile(suffix='.h5') as out_h5:
                twixzip.compress_twix(infile=infile, outfile=out_h5.name)
                twixzip.reconstruct_twix(infile=out_h5.name, outfile=out_dat.name)
            md5_new = md5(out_dat.name)

        self.assertEqual(md5_orig, md5_new, 'lossless compression: md5 hash does not match with original')


class test_zfp(unittest.TestCase):

    def test(self):
        infile = 'test/singlechannel.dat'
        sz_orig = os.path.getsize(infile)

        zfp_tol = 1e-5
        with tempfile.NamedTemporaryFile(suffix='.dat') as out_dat:
            with tempfile.NamedTemporaryFile(suffix='.h5') as out_h5:
                twixzip.compress_twix(infile=infile, outfile=out_h5.name, zfp=True, zfp_tol=zfp_tol)
                twixzip.reconstruct_twix(infile=out_h5.name, outfile=out_dat.name)

            self.assertEqual(sz_orig, os.path.getsize(out_dat.name), 'zfp: file size not equal to original')
            
            with suppress_stdout_stderr():
                twix_orig = read_twix(infile)[-1]
                twix_new = read_twix(out_dat.name)[-1]

            self.assertTrue((np.all(twix_orig['hdr_str']==twix_new['hdr_str'])), 'zfp: headers do not match')

            for mdb_orig, mdb_new in zip(twix_orig['mdb'], twix_new['mdb']):
                if mdb_orig.is_flag_set('ACQEND'):
                    continue
                elif mdb_orig.is_flag_set('SYNCDATA'):
                    continue

                self.assertTrue(mdb_orig.mdh == mdb_new.mdh, 'zfp: mdhs do not match')
                self.assertTrue(np.allclose(mdb_orig.data, mdb_new.data, atol=zfp_tol), 'zfp: mdb data not within zfp tolerance')


class test_remove_os(unittest.TestCase):

    def test(self):
        infile = 'test/singlechannel.dat'
        sz_orig = os.path.getsize(infile)

        with tempfile.NamedTemporaryFile(suffix='.dat') as out_dat:
            with tempfile.NamedTemporaryFile(suffix='.h5') as out_h5:
                twixzip.compress_twix(infile=infile, outfile=out_h5.name, remove_os=True)
                twixzip.reconstruct_twix(infile=out_h5.name, outfile=out_dat.name)
            sz_new = os.path.getsize(out_dat.name)

        self.assertEqual(sz_orig, sz_new, 'remove_os: file size not equal to original')


class test_scc(unittest.TestCase):

    def test(self):
        infile = 'test/multichannel.dat'

        with suppress_stdout_stderr():
            twix_orig = read_twix(infile)[-1]
        
        nc = twix_orig['mdb'][1].mdh['ushUsedChannels']

        with tempfile.NamedTemporaryFile(suffix='.dat') as out_python:
            with tempfile.NamedTemporaryFile(suffix='.h5') as out_h5:
                twixzip.compress_twix(infile=infile, outfile=out_h5.name, cc_mode='scc', ncc=nc)
                twixzip.reconstruct_twix(infile=out_h5.name, outfile=out_python.name)
            
            with suppress_stdout_stderr():
                twix_orig = read_twix(infile)[-1]
                twix_python = read_twix(out_python.name)[-1]

            for mdb_orig, mdb_python in zip(twix_orig['mdb'], twix_python['mdb']):
                if mdb_orig.is_flag_set('ACQEND'):
                    continue
                elif mdb_orig.is_flag_set('SYNCDATA'):
                    continue

                self.assertTrue(mdb_orig.mdh == mdb_python.mdh, 'scc: mdhs do not match')
                self.assertTrue(np.allclose(mdb_orig.data, mdb_python.data), 'scc: mdb data not within tolerance')


class test_gcc(unittest.TestCase):

    def test(self):
        infile = 'test/multichannel.dat'

        with suppress_stdout_stderr():
            twix_orig = read_twix(infile)[-1]
        
        nc = twix_orig['mdb'][1].mdh['ushUsedChannels']

        with tempfile.NamedTemporaryFile(suffix='.dat') as out_python:
            with tempfile.NamedTemporaryFile(suffix='.h5') as out_h5:
                twixzip.compress_twix(infile=infile, outfile=out_h5.name, cc_mode='gcc', ncc=nc)
                twixzip.reconstruct_twix(infile=out_h5.name, outfile=out_python.name)
            
            with suppress_stdout_stderr():
                twix_orig = read_twix(infile)[-1]
                twix_python = read_twix(out_python.name)[-1]

            for mdb_orig, mdb_python in zip(twix_orig['mdb'], twix_python['mdb']):
                if mdb_orig.is_flag_set('ACQEND'):
                    continue
                elif mdb_orig.is_flag_set('SYNCDATA'):
                    continue

                self.assertTrue(mdb_orig.mdh == mdb_python.mdh, 'gcc: mdhs do not match')
                self.assertTrue(np.allclose(mdb_orig.data, mdb_python.data), 'gcc: mdb data not within tolerance')
