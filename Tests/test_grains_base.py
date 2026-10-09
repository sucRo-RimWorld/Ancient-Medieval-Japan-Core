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
        for name in ('Defs', 'Languages', 'Patches', 'Compatibility', 'BaseWithoutMO', 'LegacyStartingScenarios', 'Tests/Fixtures', 'Textures'):
            shutil.copytree(ROOT / name, self.root / name)
        shutil.copyfile(ROOT / 'loadFolders.xml', self.root / 'loadFolders.xml')
        (self.root / 'Docs').mkdir(exist_ok=True)
        shutil.copyfile(ROOT / 'Docs/LocalizationHistoricalReview.md',
                        self.root / 'Docs/LocalizationHistoricalReview.md')

    def validate(self):
        with patch.object(gate, 'ROOT', self.root), patch.object(
            gate, 'profile_xml', lambda profile: profile_xml(profile, self.root)
        ), redirect_stdout(StringIO()):
            gate.validate()

    def test_current_payload(self):
        self.validate()

    def test_unapproved_plant_description_rejected(self):
        path = self.root / 'Defs/ThingDefs_Plants/Plants_StageA.xml'
        tree = ET.parse(path)
        tree.find('ThingDef[defName="AMJC_Plant_Barley"]/description').text = (
            'Unexpected historical narrative')
        tree.write(path)
        with self.assertRaisesRegex(AssertionError, 'Approved English crop description changed'):
            self.validate()

    def test_approved_crop_review_drift_rejected(self):
        path = self.root / 'Docs/LocalizationHistoricalReview.md'
        text = path.read_text(encoding='utf-8')
        original = 'Barley (omugi). A cereal introduced to Japan in the Yayoi period'
        self.assertIn(original, text)
        path.write_text(text.replace(original, 'Barley (omugi). A cereal found in another era'),
                        encoding='utf-8')
        with self.assertRaisesRegex(AssertionError, 'Approved English crop description changed'):
            self.validate()

    def test_unapproved_common_recipe_translation_rejected(self):
        path = self.root / 'Languages/Japanese/DefInjected/RecipeDef/AMJC_StageA.xml'
        xml = ET.parse(path)
        xml.find('AMJC_HullMillet.description').text = '意図しない翻訳変更'
        xml.write(path)
        with self.assertRaisesRegex(AssertionError, 'MO recipe translations changed during split'):
            self.validate()

    def test_unapproved_thresh_wording_regression_rejected(self):
        path = self.root / 'Languages/Japanese/DefInjected/RecipeDef/AMJC_StageA.xml'
        xml = ET.parse(path)
        xml.find('AMJC_ThreshMillet.description').text = '藁と殻付き雑穀を得る'
        xml.write(path)
        with self.assertRaisesRegex(AssertionError, 'Approved neutral processing text changed'):
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

    def test_base_mo_texture_rejected(self):
        path = self.root / 'Defs/ThingDefs_Plants/Plants_StageA.xml'
        xml = ET.parse(path)
        xml.find('ThingDef[defName="AMJC_Plant_Barley"]/plant/immatureGraphicPath').text = 'Things/Plants/Immature/WheatPlant'
        xml.write(path)
        with self.assertRaisesRegex(AssertionError, 'AMJ graphics priority lost'):
            self.validate()

    def test_mo_graphics_override_rejected(self):
        path = self.root / MO_FOLDER / 'Patches/MedievalOverhaul_StageA_Base.xml'
        xml = ET.parse(path)
        xml.getroot().append(ET.fromstring('''<Operation Class="PatchOperationReplace">
          <xpath>/Defs/ThingDef[defName="AMJC_Plant_Barley"]/plant/immatureGraphicPath</xpath>
          <value><immatureGraphicPath>Things/Plants/Immature/WheatPlant</immatureGraphicPath></value>
        </Operation>'''))
        xml.write(path)
        with self.assertRaisesRegex(AssertionError, 'AMJ graphics priority lost'):
            self.validate()

    def test_mo_barley_research_override_rejected(self):
        path = self.root / MO_FOLDER / 'Patches/MedievalOverhaul_StageA_Base.xml'
        xml = ET.parse(path)
        xml.getroot().append(ET.fromstring('''<Operation Class="PatchOperationAdd">
          <xpath>/Defs/ThingDef[defName="AMJC_Plant_Barley"]/plant</xpath>
          <value><sowResearchPrerequisites><li>DankPyon_BasicAgriculture</li></sowResearchPrerequisites></value>
        </Operation>'''))
        xml.write(path)
        with self.assertRaisesRegex(AssertionError, 'AMJ MO field priority lost'):
            self.validate()

    def test_mo_processing_table_cost_override_rejected(self):
        path = self.root / MO_FOLDER / 'Patches/MedievalOverhaul_StageA_Base.xml'
        xml = ET.parse(path)
        xml.getroot().append(ET.fromstring('''<Operation Class="PatchOperationReplace">
          <xpath>/Defs/ThingDef[defName="AMJC_GrainProcessingTable"]/costList</xpath>
          <value><costList><DankPyon_IronIngot>30</DankPyon_IronIngot></costList></value>
        </Operation>'''))
        xml.write(path)
        with self.assertRaisesRegex(AssertionError, 'AMJ MO field priority lost'):
            self.validate()

    def test_mo_processing_table_research_override_rejected(self):
        path = self.root / MO_FOLDER / 'Patches/MedievalOverhaul_StageA_Base.xml'
        xml = ET.parse(path)
        xml.getroot().append(ET.fromstring('''<Operation Class="PatchOperationAdd">
          <xpath>/Defs/ThingDef[defName="AMJC_GrainProcessingTable"]</xpath>
          <value><researchPrerequisites><li>DankPyon_BasicAgriculture</li></researchPrerequisites></value>
        </Operation>'''))
        xml.write(path)
        with self.assertRaisesRegex(AssertionError, 'AMJ MO field priority lost'):
            self.validate()

    def test_visual_exception_does_not_hide_gameplay_change(self):
        path = self.root / 'Defs/ThingDefs_Buildings/Buildings_GrainProcessing.xml'
        xml = ET.parse(path)
        xml.find('ThingDef[defName="AMJC_GrainProcessingSpot"]/statBases/MaxHitPoints').text = '999'
        xml.write(path)
        with self.assertRaisesRegex(AssertionError, 'pre-split snapshot'):
            self.validate()


if __name__ == '__main__':
    unittest.main()
