import pickle
import pickletools
from test import support
from test.pickletester import AbstractPickleTests
import doctest
import unittest

class OptimizedPickleTests(AbstractPickleTests, unittest.TestCase):

    # TODO: RUSTPYTHON, AttributeError: module 'pickle' has no attribute 'PickleBuffer'
    @unittest.expectedFailure
    def test_buffer_callback_error(self): # TODO: RUSTPYTHON, remove when this passes
        super().test_buffer_callback_error()

    # TODO: RUSTPYTHON, AttributeError: module 'pickle' has no attribute 'PickleBuffer'
    @unittest.expectedFailure
    def test_buffers_error(self): # TODO: RUSTPYTHON, remove when this passes
        super().test_buffers_error()

    # TODO: RUSTPYTHON, TypeError: cannot pickle 'method' object
    @unittest.expectedFailure
    def test_c_methods(self): # TODO: RUSTPYTHON, remove when this passes
        super().test_c_methods()

    def test_compat_pickle(self): # TODO: RUSTPYTHON, remove when this passes
        super().test_compat_pickle()

    # TODO: RUSTPYTHON
    @unittest.expectedFailure
    def test_complex_newobj_ex(self): # TODO: RUSTPYTHON, remove when this passes
        super().test_complex_newobj_ex()

    # TODO: RUSTPYTHON, TypeError: cannot pickle 'method' object
    @unittest.expectedFailure
    def test_in_band_buffers(self): # TODO: RUSTPYTHON, remove when this passes
        super().test_in_band_buffers()

    # TODO: RUSTPYTHON, pickle.PicklingError
    @unittest.expectedFailure
    def test_nested_names(self): # TODO: RUSTPYTHON, remove when this passes
        super().test_nested_names()

    # TODO: RUSTPYTHON
    @unittest.expectedFailure
    def test_newobj_generic(self): # TODO: RUSTPYTHON, remove when this passes
        super().test_newobj_generic()

    # TODO: RUSTPYTHON, TypeError: cannot pickle 'weakproxy' object
    @unittest.expectedFailure
    def test_newobj_proxies(self): # TODO: RUSTPYTHON, remove when this passes
        super().test_newobj_proxies()

    def test_notimplemented(self): # TODO: RUSTPYTHON, remove when this passes
        super().test_notimplemented()

    # TODO: RUSTPYTHON, AttributeError: module 'pickle' has no attribute 'PickleBuffer'
    @unittest.expectedFailure
    def test_oob_buffers(self): # TODO: RUSTPYTHON, remove when this passes
        super().test_oob_buffers()

    # TODO: RUSTPYTHON, AttributeError: module 'pickle' has no attribute 'PickleBuffer'
    @unittest.expectedFailure
    def test_oob_buffers_writable_to_readonly(self): # TODO: RUSTPYTHON, remove when this passes
        super().test_oob_buffers_writable_to_readonly()

    # TODO: RUSTPYTHON, TypeError: Expected type 'bytes', not 'bytearray'
    @unittest.expectedFailure
    def test_optional_frames(self): # TODO: RUSTPYTHON, remove when this passes
        super().test_optional_frames()

    # TODO: RUSTPYTHON, AttributeError: module 'pickle' has no attribute 'PickleBuffer'
    @unittest.expectedFailure
    def test_picklebuffer_error(self): # TODO: RUSTPYTHON, remove when this passes
        super().test_picklebuffer_error()

    # TODO: RUSTPYTHON, pickle.PicklingError
    @unittest.expectedFailure
    def test_py_methods(self): # TODO: RUSTPYTHON, remove when this passes
        super().test_py_methods()

    # TODO: RUSTPYTHON, AttributeError: attribute '__qualname__' of 'type' objects is not writable
    @unittest.expectedFailure
    def test_recursive_nested_names(self): # TODO: RUSTPYTHON, remove when this passes
        super().test_recursive_nested_names()

    def test_singleton_types(self): # TODO: RUSTPYTHON, remove when this passes
        super().test_singleton_types()

    def dumps(self, arg, proto=None, **kwargs):
        return pickletools.optimize(pickle.dumps(arg, proto, **kwargs))

    def loads(self, buf, **kwds):
        return pickle.loads(buf, **kwds)

    # Test relies on precise output of dumps()
    test_pickle_to_2x = None

    # Test relies on writing by chunks into a file object.
    test_framed_write_sizes_with_delayed_writer = None

    # TODO: RUSTPYTHON
    @unittest.expectedFailure
    def test_optimize_long_binget(self):
        data = [str(i) for i in range(257)]
        data.append(data[-1])
        for proto in range(pickle.HIGHEST_PROTOCOL + 1):
            pickled = pickle.dumps(data, proto)
            unpickled = pickle.loads(pickled)
            self.assertEqual(unpickled, data)
            self.assertIs(unpickled[-1], unpickled[-2])

            pickled2 = pickletools.optimize(pickled)
            unpickled2 = pickle.loads(pickled2)
            self.assertEqual(unpickled2, data)
            self.assertIs(unpickled2[-1], unpickled2[-2])
            self.assertNotIn(pickle.LONG_BINGET, pickled2)
            self.assertNotIn(pickle.LONG_BINPUT, pickled2)

    def test_optimize_binput_and_memoize(self):
        pickled = (b'\x80\x04\x95\x15\x00\x00\x00\x00\x00\x00\x00'
                   b']\x94(\x8c\x04spamq\x01\x8c\x03ham\x94h\x02e.')
        #    0: \x80 PROTO      4
        #    2: \x95 FRAME      21
        #   11: ]    EMPTY_LIST
        #   12: \x94 MEMOIZE
        #   13: (    MARK
        #   14: \x8c     SHORT_BINUNICODE 'spam'
        #   20: q        BINPUT     1
        #   22: \x8c     SHORT_BINUNICODE 'ham'
        #   27: \x94     MEMOIZE
        #   28: h        BINGET     2
        #   30: e        APPENDS    (MARK at 13)
        #   31: .    STOP
        self.assertIn(pickle.BINPUT, pickled)
        unpickled = pickle.loads(pickled)
        self.assertEqual(unpickled, ['spam', 'ham', 'ham'])
        self.assertIs(unpickled[1], unpickled[2])

        pickled2 = pickletools.optimize(pickled)
        unpickled2 = pickle.loads(pickled2)
        self.assertEqual(unpickled2, ['spam', 'ham', 'ham'])
        self.assertIs(unpickled2[1], unpickled2[2])
        self.assertNotIn(pickle.BINPUT, pickled2)


class MiscTestCase(unittest.TestCase):
    def test__all__(self):
        blacklist = {'bytes_types',
                     'UP_TO_NEWLINE', 'TAKEN_FROM_ARGUMENT1',
                     'TAKEN_FROM_ARGUMENT4', 'TAKEN_FROM_ARGUMENT4U',
                     'TAKEN_FROM_ARGUMENT8U', 'ArgumentDescriptor',
                     'read_uint1', 'read_uint2', 'read_int4', 'read_uint4',
                     'read_uint8', 'read_stringnl', 'read_stringnl_noescape',
                     'read_stringnl_noescape_pair', 'read_string1',
                     'read_string4', 'read_bytes1', 'read_bytes4',
                     'read_bytes8', 'read_bytearray8', 'read_unicodestringnl',
                     'read_unicodestring1', 'read_unicodestring4',
                     'read_unicodestring8', 'read_decimalnl_short',
                     'read_decimalnl_long', 'read_floatnl', 'read_float8',
                     'read_long1', 'read_long4',
                     'uint1', 'uint2', 'int4', 'uint4', 'uint8', 'stringnl',
                     'stringnl_noescape', 'stringnl_noescape_pair', 'string1',
                     'string4', 'bytes1', 'bytes4', 'bytes8', 'bytearray8',
                     'unicodestringnl', 'unicodestring1', 'unicodestring4',
                     'unicodestring8', 'decimalnl_short', 'decimalnl_long',
                     'floatnl', 'float8', 'long1', 'long4',
                     'StackObject',
                     'pyint', 'pylong', 'pyinteger_or_bool', 'pybool', 'pyfloat',
                     'pybytes_or_str', 'pystring', 'pybytes', 'pybytearray',
                     'pyunicode', 'pynone', 'pytuple', 'pylist', 'pydict',
                     'pyset', 'pyfrozenset', 'pybuffer', 'anyobject',
                     'markobject', 'stackslice', 'OpcodeInfo', 'opcodes',
                     'code2op',
                     }
        support.check__all__(self, pickletools, not_exported=blacklist)


def load_tests(loader, tests, pattern):
    # TODO: RUSTPYTHON
    # tests.addTest(doctest.DocTestSuite(pickletools))
    return tests


if __name__ == "__main__":
    unittest.main()
