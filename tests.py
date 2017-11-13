import unittest

import dispatch
import playground.api_daemon as api_daemon


class Backend_tests(unittest.TestCase):
    # NOTE: tests methods must begin with test_, otherwise

    def setUp(self):
        """
        shared vars that must be initialized prior to test
        :return:
        """
        dispatch.Tracker.append(
            data=dispatch.Case(index=42, client="client", platform='pc', cr=False, system="AL-quam"))

    def tearDown(self):
        # print("popping 42 from database...")
        dispatch.database.pop(42)
        # print(dispatch.database)

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
        # self.assertEqual(len(dispatch.database), 2)
        self.assertIsInstance(ret, dispatch.Case)
        self.assertEqual(ret.platform.lower(), 'xb')
        self.assertEqual(ret.client, expected_client)
        self.assertEqual(ret.system, " CRUCIS SECTOR BQ-P A5-1")  # not sure *why* this needed a space
        self.assertEqual(ret.index, -1)
        self.assertEqual(ret.rats, [])

    def test_rat_Signal(self):
        dispatch.on_message_received(dispatch.pc_rsig_message)
        data = dispatch.database.get(4)
        self.assertIsNotNone(data)

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
        data.Platform('XB')
        self.assertEqual(data.platform, 'XB')

    def test_change_system(self):
        """
        updates case 42's set_system and verifies the result
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
        # data: dispatch.Case
        expected_rat = "theunkn0wn1[pc]"
        data.Rats(expected_rat)
        self.assertEqual(data.rats, [expected_rat])
        # dispatch.database.pop(42)

    def test_add_multiple_rats(self):
        expected_rats = ["orion", "Neptunes_Beard[xb-nd]", "stack_overflow[xb]"]
        # these names are random, any rats that may exist by these names are purely coincidental
        data = dispatch.database.get(42)
        self.assertIsNotNone(data)
        # data: dispatch.Case
        data.Rats(expected_rats)
        self.assertEqual(expected_rats, data.rats)

    def test_delete_rats(self):
        expected_deleted = [["theunkn0wn1[pc]", "Orion[xb|nd]", "somerat"], ["theunknown1[xb]"],
                            [
                                'xray',
                                'november',
                                'mike',
                                'ratsignal',
                                'im_just_making_this_up'
                            ]]
        data = dispatch.database.get(42)
        # data: dispatch.Case
        for testCase in expected_deleted:
            with self.subTest(expected_deleted=testCase):
                data.Rats(testCase)  # add them to the case
                data.Rats(testCase, mode="remove")  # now remove them again
                # data.Rats(expected_deleted)
                # data.Rats(expected_deleted, mode='remove')
                self.assertEqual([], data.rats)  # the list should be empty
                self.assertNotEqual(expected_deleted, data.rats)  # and certainly not equal to the original


class CommandTesting(unittest.TestCase):
    """
    For the testing of / commands
    """

    @classmethod
    def setUpClass(cls):
        dispatch.init()
        super().setUpClass()

    def setUp(self):
        """
        shared vars that must be initialized prior to test
        :return:
        """
        dispatch.Tracker.append(
            data=dispatch.Case(index=64, client="PotatoClient", platform='ps', cr=False, system="Ki"))

    def tearDown(self):
        """
        clean up after each case
        :return:
        """
        # print("popping 64 from database...")
        dispatch.database.pop(64)
        # print(dispatch.database)

    def test_system(self):
        # ['sys', '2', 'overall', 'asd']  # word
        # (['sys 2 overall asd', '2 overall asd', 'overall asd', 'asd'], None)  # word_eol
        cmd = dispatch.CommandBase.getCommand('sys')
        cmd.func(
                ['set_system', '64', 'some_random_data'],["", "64 some_random_data", "some_random_data"])
        data = dispatch.database.get(64)
        # data: dispatch.Case
        self.assertEqual(data.system, "some_random_data")

    def test_cr(self):
        # dispatch.Commands.code_red(["cr", "64"], ([]), None)
        data = dispatch.database.get(64)
        command = dispatch.CommandBase.getCommand('cr')
        self.assertIsNotNone(data)
        self.assertFalse(data.cr)
        command.func(["cr", "64"],None,None)
        self.assertTrue(data.cr)

    def test_platform_valid(self):
        expected_platforms = ['XB', 'PC', 'PS']
        data = dispatch.database.get(64)
        # data: dispatch.Case
        for platform in expected_platforms:
            with self.subTest(platform=platform):
                    dispatch.Commands.platform(['platform', '64', platform], None, None)
                    self.assertEqual(data.platform, platform)

    def test_platform_invalid(self):
        bad_platforms = ['xbox', "pee-cee","ps3",""]
        data = dispatch.database.get(64)
        # data: dispatch.Case
        for platform in bad_platforms:
            with self.subTest(platform=platform):
                dispatch.Commands.platform(['platform', '64', platform], None, None)
        self.assertEqual(data.platform, 'ps')  # the platform should remain unchanged.

    def test_add_rats(self):
        """via command this time"""
        expected_rats = ["theunkn0wn1[pc]", "ninjaKiwi"]
        command = ["append", "64"] + expected_rats
        data = dispatch.database.get(64)
        cmd_func = dispatch.CommandBase.getCommand('append')
        cmd_func.func(command,None)
        # data: dispatch.Case
        self.assertEqual(data.rats, expected_rats)

    def test_say(self):
        # dispatch.StageManager.Say() # init
        self.assertNotEqual(dispatch.stageBase.registered_commands, {})
        command = dispatch.stageBase.getCommand("say")
        # command: dispatch.CommandBase
        self.assertIsNotNone(command)
        print(command)
        command.func(message="test")

    def test_cmd_new_case(self):
        """Test if one can register a command and invoke it"""

        cmd = dispatch.CommandBase.getCommand("new")
        self.assertIsNotNone(cmd)
        print("cmd = {}".format(cmd))
        cmd.func(['new', "2", "ki"], None, None)
        case = dispatch.Tracker.get_case(value=2)
        self.assertIsNotNone(case)
    # @unittest.expectedFailure
    def test_find_by_alias(self):
        commands = ['create', 'new', 'cr']
        for name in commands:
            with self.subTest(cmd = name):
                found = dispatch.CommandBase.getCommand(name=name)
                self.assertIsNotNone(found)




class ProxyServerParse(unittest.TestCase):
    output = None

    def setUp(self):
        global output
        test_inputs ='{"meta":{"event":"rescueCreated"},"data":{"id":"8e861212-c990-4ff9-b8e7-3c09da4adfb7","type":"rescues","attributes":{"notes":"","outcome":null,"title":null,"firstLimpetId":null,"client":"jkacina","set_system":"PENCIL SECTOR BV-O A6-4","codeRed":false,"unidentifiedRats":[],"status":"open","platform":"pc","quotes":[{"author":"Mecha","message":"RATSIGNAL - CMDR jkacina - System: PENCIL SECTOR BV-O A6-4 - Platform: PC - O2: OK - Language: English (en-CA)","createdAt":"2017-10-16T17:11:08.216278","updatedAt":"2017-10-16T17:11:08.216262","lastAuthor":"Mecha"}],"data":{"langID":"en","status":{},"IRCNick":"jkacina","boardIndex":5,"markedForDeletion":{"marked":false,"reason":"None.","reporter":"Noone."}},"updatedAt":"2017-10-16T17:11:07.794Z","createdAt":"2017-10-16T17:11:07.794Z","deletedAt":null},"relationships":{"rats":{"data":null},"firstLimpet":{"data":null},"epics":{"data":null}},"links":{"self":"/rescues/8e861212-c990-4ff9-b8e7-3c09da4adfb7"}}}'
        output = api_daemon.Parser.parse(test_inputs)
        expected_results = [
            dispatch.Case(client="jkacina", api_id="8e861212-c990-4ff9-b8e7-3c09da4adfb7",
                          platform='pc', system="PENCIL SECTOR BV-O A6-4")]
        # output: dispatch.Case

    def test_index(self):
        self.assertEqual(output.index, 5)

    def test_cr(self):
        self.assertFalse(output.cr)

    def test_client(self):
        self.assertEqual(output.client, "jkacina")

    def test_id(self):
        self.assertEqual(output.api_id, "8e861212-c990-4ff9-b8e7-3c09da4adfb7")

    def test_system(self):
        self.assertEqual(output.system, "PENCIL SECTOR BV-O A6-4")

    def test_platform(self):
        self.assertEqual(output.platform, 'pc')

    def test_parse(self):
        # test_inputs = ['{"meta":{"event":"rescueCreated"},"data":{"id":"8e861212-c990-4ff9-b8e7-3c09da4adfb7","type":"rescues","attributes":{"notes":"","outcome":null,"title":null,"firstLimpetId":null,"client":"jkacina","set_system":"PENCIL SECTOR BV-O A6-4","codeRed":false,"unidentifiedRats":[],"status":"open","platform":"pc","quotes":[{"author":"Mecha","message":"RATSIGNAL - CMDR jkacina - System: PENCIL SECTOR BV-O A6-4 - Platform: PC - O2: OK - Language: English (en-CA)","createdAt":"2017-10-16T17:11:08.216278","updatedAt":"2017-10-16T17:11:08.216262","lastAuthor":"Mecha"}],"data":{"langID":"en","status":{},"IRCNick":"jkacina","boardIndex":5,"markedForDeletion":{"marked":false,"reason":"None.","reporter":"Noone."}},"updatedAt":"2017-10-16T17:11:07.794Z","createdAt":"2017-10-16T17:11:07.794Z","deletedAt":null},"relationships":{"rats":{"data":null},"firstLimpet":{"data":null},"epics":{"data":null}},"links":{"self":"/rescues/8e861212-c990-4ff9-b8e7-3c09da4adfb7"}}}']
        # output = api_daemon.Parser.parse(test_inputs[0])
        self.assertIsNotNone(output)
        self.assertIsInstance(output, dispatch.Case)
        self.assertEqual(output.client, "jkacina")
        self.assertEqual(output.api_id, "8e861212-c990-4ff9-b8e7-3c09da4adfb7")
        self.assertEqual(output.platform, "pc")
        self.assertEqual(output.system, "PENCIL SECTOR BV-O A6-4")
        self.assertFalse(output.cr)
        self.assertEqual(output.index, 5)


if __name__ == '__main__':  # this prevents script code from being executed on import. (bad!)
    unittest.main()
