import unittest

import dispatch


class Tests(unittest.TestCase):
    # NOTE: tests methods must begin with test_, otherwise

    def setUp(self):
        """
        shared vars that must be initialized prior to test
        :return:
        """
        dispatch.Tracker.append(
            data=dispatch.Case(index=42, client="client", platform='pc', cr=False, system="AL-quam"))

    def tearDown(self):
        dispatch.database.pop(42)

    def test_inject_a(self):
        ret = dispatch.Parser.parse(data=dispatch.debug_constant_B)
        self.assertIsInstance(ret, dispatch.Case)
        self.assertEqual(ret.client, "Potato", "client did not match expected client")
        self.assertEqual(ret.system, "ki")

    def test_inject_b(self):
        ret = dispatch.Parser.parse(data=dispatch.debug_constant_a)
        self.assertIsInstance(ret, dispatch.Case)
        self.assertEqual(ret.client, "ClientName")
        self.assertEqual(ret.system, "sol")

    def test_case_generation(self):
        expected_client = "potatoBot"
        expected_platform = "ps"
        expected_system = "Droju CB-X d1-4"
        expected_cr = True
        expected_index = 43
        case = dispatch.Case(client=expected_client, index=expected_index, cr=expected_cr, system=expected_system,
                             platform=expected_platform)
        self.assertIsNotNone(case)
        self.assertEqual(case.client, expected_client)
        self.assertEqual(case.platform, expected_platform)
        self.assertEqual(case.system, expected_system)
        self.assertEqual(case.index, expected_index)
        self.assertEqual(case.cr, expected_cr)

    def test_xb_rat_signal(self):
        # ret = dispatch.Parser.parse(data=dispatch.xb_rsig_message)
        expected_client = "XX_SAM_JR_XX"
        db = dispatch.database
        dispatch.on_message_received(dispatch.xb_rsig_message)
        ret = dispatch.Tracker.get_case(value=expected_client)
        self.assertEqual(len(dispatch.database), 2)
        self.assertIsInstance(ret, dispatch.Case)
        self.assertEqual(ret.platform.lower(), 'xb')
        self.assertEqual(ret.client, expected_client)
        self.assertEqual(ret.system, " CRUCIS SECTOR BQ-P A5-1")  # not sure *why* this needed a space
        self.assertEqual(ret.index, -1)
        self.assertEqual(ret.rats, [None] * 3)

    def test_clear(self):
        ret = dispatch.Parser.parse(data=dispatch.clear_msg)
        self.assertIsInstance(ret, str)
        self.assertEqual(ret, "Potato")
        # dispatch.on_message_received(dispatch.xb_rsig_message)
        # dispatch.on_message_received(dispatch.clear_msg)

    # @unittest.expectedFailure
    def test_change_platform(self):
        """
        depends on test_a_get_case
        updates case 42's platform and verifies the result
        """
        data = dispatch.Tracker.get_case(value="client")
        self.assertIsNotNone(data)
        data.Platform('xb')
        self.assertEqual(data.platform, 'xb')

    def test_change_system(self):
        """
        depends on test_a_get_case
        updates case 42's system and verifies the result
        """
        data = dispatch.Tracker.get_case(value="client")
        dispatch.log("test_change_system", "data is {}".format(data), True)
        dispatch.log("test_change_system", "database itself is {}".format(dispatch.database), True)
        self.assertIsNotNone(data)
        data.System("al-qaum")
        self.assertEqual(data.system, "al-qaum")

    def test_change_client_name(self):
        """
        depends on test_a_get_case
        updates case 42's client name and verifies the result
        :return:
        """
        expected_name = "new_client_name"
        data = dispatch.Tracker.get_case(value=42)
        self.assertIsNotNone(data)
        # data: dispatch.Case
        data.Client(expected_name)
        self.assertEqual(data.client, expected_name)

    def test_b_get_case(self):
        """
        I needed to prefix this with A because its alphabetically loaded and other tests depend on it...
        generates a case, adds it to the database, and verifies it was generated correctly
        """
        self.assertTrue(dispatch.Tracker.append(data=dispatch.Case(client="client", index=42, cr=False, platform='pc',
                                                                   system="ki")))
        data = dispatch.Tracker.get_case(value=42)
        # data: dispatch.Case
        self.assertIsNotNone(data)
        self.assertEqual(data.client, "client")
        self.assertEqual(data.index, 42)
        self.assertEqual(data.platform, 'pc')

    def test_add_single_rat(self):
        data = dispatch.database.get(42)
        self.assertIsNotNone(data, None)  # if data is None then we can just stop here
        data: dispatch.Case



if __name__ == '__main__':  # this prevents script code from being executed on import. (bad!)
    unittest.main()
