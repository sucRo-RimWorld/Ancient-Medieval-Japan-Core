"""Boundary regressions: reject unconditional MO and lost compatibility payload."""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import validate_grains_base as gate
from amj_profile_xml import ROOT, MO_FOLDER, profile_xml


class BaseBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ('Defs', 'Languages', 'Patches', 'Compatibility', 'BaseWithoutMO', 'LegacyStartingScenarios', 'Tests/Fixtures'):
            shutil.copytree(ROOT / name, self.root / name)
        shutil.copyfile(ROOT / 'loadFolders.xml', self.root / 'loadFolders.xml')

    def validate(self):
        with patch.object(gate, 'ROOT', self.root), patch.object(
            gate, 'profile_xml', lambda profile: profile_xml(profile, self.root)
        ), redirect_stdout(StringIO()):
            gate.validate()

    def test_current_payload(self):
        self.validate()

    def test_unconditional_mo_reference_rejected(self):
        path = self.root / 'Defs/ThingDefs_Items/Items_StageA_Grains.xml'
        xml = ET.parse(path)
        ET.SubElement(xml.getroot()[0], 'thingCategories').append(ET.fromstring('<li>DankPyon_Cereal</li>'))
        xml.write(path)
        with self.assertRaisesRegex(AssertionError, 'Base MO reference'):
            self.validate()

    def test_missing_mo_guard_rejected(self):
        path = self.root / 'loadFolders.xml'
        xml = ET.parse(path)
        del xml.find('v1.6/li[@IfModActive]').attrib['IfModActive']
        xml.write(path)
        with self.assertRaises(AssertionError):
            self.validate()

    def test_lost_mo_straw_rejected(self):
        path = self.root / MO_FOLDER / 'Patches/MedievalOverhaul_StageA_Base.xml'
        xml = ET.parse(path)
        output = xml.find('.//DankPyon_Straw')
        output.text = '2'
        xml.write(path)
        with self.assertRaisesRegex(AssertionError, 'pre-split snapshot'):
            self.validate()


if __name__ == '__main__':
    unittest.main()
