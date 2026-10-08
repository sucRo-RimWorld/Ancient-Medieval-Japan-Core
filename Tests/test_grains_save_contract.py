"""Synthetic XML contract regression; NEVER calls the game or certifies migrations."""
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'Scripts'))
from grains_save_contract import ContractError, inspect_bytes, compare, prepare, main

OLD = 'a'*40
NEW = 'b'*40


def save(rice='RawRice', millet=20, bill='AMJC_ThreshMilletBulk',
         core=True, mo=True, ticks='60000'):
    root = ET.Element('savegame')
    meta = ET.SubElement(root, 'meta')
    ET.SubElement(meta, 'gameVersion').text = '1.6.4622'
    ids = ET.SubElement(meta, 'modIds')
    for m in ('ludeon.rimworld', 'sucro.ancientmedievaljapan.core' if core else 'some.other',
              'dankpyon.medieval.overhaul' if mo else 'some.mod'):
        ET.SubElement(ids, 'li').text = m
    game = ET.SubElement(root, 'game')
    ET.SubElement(ET.SubElement(game, 'tickManager'), 'ticksGame').text = ticks
    maps = ET.SubElement(game, 'maps')
    map1 = ET.SubElement(maps, 'li')
    things = ET.SubElement(map1, 'things')
    for identity, kind, count in (('Thing_1', 'AMJC_RawMillet', str(millet)),
                                  ('Thing_2', rice, '15'),
                                  ('Thing_3', 'AMJC_GrainProcessingTable', '1')):
        node = ET.SubElement(things, 'li')
        ET.SubElement(node, 'def').text = kind
        ET.SubElement(node, 'id').text = identity
        ET.SubElement(node, 'stackCount').text = count
    table = things[-1]
    bills = ET.SubElement(table, 'bills')
    one = ET.SubElement(bills, 'li', Class='Bill_Production')
    ET.SubElement(one, 'recipe').text = bill
    ET.SubElement(one, 'repeatMode').text = 'RepeatCount'
    ET.SubElement(one, 'repeatCount').text = '5'
    return ET.tostring(root, encoding='utf-8', xml_declaration=True)


class SaveContracts(unittest.TestCase):
    def test_source_inventory_and_bill_contract(self):
        snap = inspect_bytes(save())
        self.assertEqual(snap['things']['Thing_1']['stackCount'], 20)
        self.assertEqual(snap['counts']['RawRice'], 15)
        self.assertEqual(len(snap['grainBills']), 1)
        self.assertEqual(compare(snap, inspect_bytes(save()))['runtimeVerified'], False)

    def test_reject_silent_inventory_loss(self):
        with self.assertRaisesRegex(ContractError, 'things'):
            compare(inspect_bytes(save()), inspect_bytes(save(millet=19)))

    def test_reject_legacy_rice_reinterpretation(self):
        with self.assertRaisesRegex(ContractError, 'RawRice/Plant_Rice'):
            compare(inspect_bytes(save()), inspect_bytes(save(rice='AMJC_RiceSheaf')))

    def test_reject_bill_reinterpretation(self):
        with self.assertRaisesRegex(ContractError, 'grainBills'):
            compare(inspect_bytes(save()), inspect_bytes(save(bill='AMJC_HullMilletBulk')))

    def test_reject_game_tick(self):
        with self.assertRaisesRegex(ContractError, 'ticksGame'):
            compare(inspect_bytes(save()), inspect_bytes(save(ticks='60001')))

    def test_reject_removed_mo_or_core(self):
        for data in (save(core=False), save(mo=False)):
            with self.subTest(data=data):
                with self.assertRaises(ContractError): inspect_bytes(data)

    def test_reject_missing_rice_fixture(self):
        with self.assertRaisesRegex(ContractError, 'RawRice/Plant_Rice'):
            inspect_bytes(save(rice='SomeOtherItem'))

    def test_reject_alias_and_malformed_xml(self):
        for data in (b'<invalid', b'<!DOCTYPE savegame><savegame/>',
                     save().replace(b'sucro.ancientmedievaljapan.core', b'sucro.ancientmedievaljapan.core.e2e')):
            with self.assertRaises(ContractError): inspect_bytes(data)

    def test_prepare_preserves_original_and_rejects_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td)/'old.rws'
            source.write_bytes(save())
            target = Path(td)/'results'
            prepared = prepare(source, target, OLD, NEW)
            self.assertFalse(prepared['runtimeVerified'])
            self.assertEqual(source.read_bytes(), (target/'baseline.rws').read_bytes())
            with self.assertRaisesRegex(ContractError, 'overwrite'):
                prepare(source, target, OLD, NEW)
            with self.assertRaisesRegex(ContractError, 'must differ'):
                prepare(source, Path(td)/'different', OLD, OLD)

    def test_cli_compare_exits_on_drift(self):
        with tempfile.TemporaryDirectory() as td:
            before, after = Path(td)/'before.rws', Path(td)/'after.rws'
            before.write_bytes(save()); after.write_bytes(save(millet=0))
            self.assertEqual(main(['compare','--before',str(before),'--after',str(after)]),2)


if __name__ == '__main__':
    unittest.main()
