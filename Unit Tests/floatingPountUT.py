import unittest
from floatingPoint import fp_bin


class FloatingPointUnitTest(unittest.TestCase):
    def test_example2(self):
        word = '011011110'
        res = fp_bin(word, mantissa_sign=0, exp_sign=1, mantissa_bits=(2, 6), exp_bits=(6, 10))
        self.assertEqual(res['decimal_value'], 0.0263671875)

    def test_example4(self):
        word = '0101101100'
        res = fp_bin(word, mantissa_sign=0, exp_sign=1, exp_bits=(2, 6), mantissa_bits=(6, 10))
        self.assertEqual(res['decimal_value'], 0.02734375)

    def test_qq1(self):
        word = '00010101'
        res = fp_bin(word, mantissa_sign=0, exp_sign=1, exp_bits=(2, 4), mantissa_bits=(4, 8))
        self.assertEqual(res['decimal_value'], 2.625)

    def test_qq(self):
        word = '00011001'
        res = fp_bin(word, mantissa_sign=0, exp_sign=1, exp_bits=(2, 4), mantissa_bits=(4, 8))
        self.assertEqual(res['decimal_value'], 3.125)


if __name__ == '__main__':
    unittest.main()
