import unittest
from golden.change import ChangeRun, GateError, validate_draft, canonical_hash

VALID = {'change_id':'TEST-1','system':'DEMO_METROLOGY','revision':'r1','parameter':'sample_count','value':22}
SYSTEMS = frozenset({'DEMO_METROLOGY'})

class ChangeTests(unittest.TestCase):
    def make_validated(self):
        r=ChangeRun('X'); r.evidence_ready(); r.set_draft(VALID); r.validate(SYSTEMS); return r

    def test_happy_path(self):
        r=self.make_validated(); r.review('independent',True)
        self.assertEqual(r.export(), VALID)
        self.assertEqual(r.status,'exported')

    def test_no_review_export(self):
        with self.assertRaises(GateError): self.make_validated().export()

    def test_invalid_draft_rejected(self):
        r=ChangeRun('X');r.evidence_ready(); r.set_draft({**VALID,'value':101})
        with self.assertRaises(GateError): r.validate(SYSTEMS)

    def test_bool_is_not_integer(self):
        self.assertTrue(validate_draft({**VALID,'value':True}, SYSTEMS))

    def test_unknown_field_rejected(self):
        self.assertTrue(validate_draft({**VALID,'other':'x'}, SYSTEMS))

    def test_unauthorized_system_rejected(self):
        self.assertTrue(validate_draft({**VALID,'system':'REAL_EQUIPMENT'}, SYSTEMS))

    def test_malformed_system_rejected_without_crashing(self):
        self.assertTrue(validate_draft({**VALID,'system':{'forged':'role'}},SYSTEMS))

    def test_duplicate_review_requires_state(self):
        r=self.make_validated(); r.review('independent',True)
        with self.assertRaises(GateError): r.review('other',True)

    def test_independent_review_required(self):
        r=self.make_validated()
        with self.assertRaises(GateError): r.review('self',False)

    def test_hash_tamper_blocked(self):
        r=self.make_validated();r.review('independent',True)
        r.draft['value']=99
        with self.assertRaises(GateError):r.export()

    def test_revalidation_invalidates_approval(self):
        r=self.make_validated();r.set_draft({**VALID,'value':23})
        with self.assertRaises(GateError):r.review('independent',True)

    def test_hash_is_key_order_independent(self):
        self.assertEqual(canonical_hash(VALID),canonical_hash(dict(reversed(list(VALID.items())))))

    def test_out_of_order(self):
        r=ChangeRun('X')
        with self.assertRaises(GateError):r.set_draft(VALID)

if __name__ == '__main__': unittest.main()
