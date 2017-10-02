import unittest

import dispatch


class Tests(unittest.TestCase):
    @unittest.expectedFailure
    def test_inject(self):
        ret = dispatch.Parser.parse(data=dispatch.debug_constant_B)
        self.assertIsInstance(ret, dispatch.Case)
        self.assertEqual(ret.client, "Potato", "client did not match expected client")
        self.assertEqual(ret.system, "ki")

    def test_xb_rat_signal(self):
        ret = dispatch.Parser.parse(data=dispatch.xb_rsig_message)
        self.assertIsInstance(ret, dispatch.Case)
        self.assertEqual(ret.platform.lower(), 'xb')
        self.assertEqual(ret.client, "XX_SAM_JR_XX")
        self.assertEqual(ret.system, " CRUCIS SECTOR BQ-P A5-1")
        self.assertEqual(ret.index, -1)
        self.assertIsNone(ret.rats)


if __name__ == '__main__':  # this prevents script code from being executed on import. (bad!)
    unittest.main()
