import unittest

from .get_bots import MalformedBotfile, parse_botline


class TestBotfile(unittest.TestCase):
    def test_rejects_only_name(self):
        with self.assertRaises(MalformedBotfile):
            parse_botline('just_a_name')

    def test_rejects_if_missing_address(self):
        with self.assertRaises(MalformedBotfile):
            parse_botline('just_a_name and_a_password')

    def test_accepts_proper_line(self):
        name = 'just_a_name'
        pw = 'and_a_password'
        addr = 'and           an     address'
        self.assertEqual((name, pw, 'and an address'),
                         parse_botline(f'{name}     {pw}  {addr}'))
