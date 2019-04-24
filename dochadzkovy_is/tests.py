from django.test import TestCase
from functions import validator as v


class ValidatorTestCase(TestCase):

    def test_string_len(self):
        self.assertTrue(v.validate_length("a" * 10))
        self.assertTrue(v.validate_length("Peter"))
        self.assertTrue(v.validate_length("Frantisek"))
        self.assertTrue(v.validate_length("", min_length=0))
        self.assertTrue(v.validate_length("""Dobry den, dneska sa mi strasne nechce do prace, tak radsej by som
                                             nerobil nic uzitocne, ako Vajk na tomto projekte a ostal spinkat doma
                                             v tepluckej posteli. Toto je test na dlzku komentarov. PIS je top predmet,
                                             chcel by som ho mat aj o rok.""", max_length=500))
        self.assertFalse(v.validate_length("Vajk"))
        self.assertFalse(v.validate_length("a" * 101))
        self.assertFalse(v.validate_length("a" * 3))

    def test_date(self):
        self.assertTrue(v.validate_date("2019-04-01", "2019-04-03"))
        self.assertTrue(v.validate_date("2019-04-01", "2019-04-01"))
        self.assertFalse(v.validate_date("2019-04-03", "2019-04-01"))

