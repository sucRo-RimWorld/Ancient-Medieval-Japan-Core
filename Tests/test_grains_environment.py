"""Environmental regressions include crop roles and the in-place upland-rice patch."""
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from amj_profile_xml import ROOT
from validate_grains_environment import validate, output


def copy_runtime_xml(root):
    for folder in ('Defs','Patches','BaseWithoutMO','Compatibility','LegacyStartingScenarios'):
        shutil.copytree(ROOT/folder,root/folder)
    shutil.copyfile(ROOT/'loadFolders.xml',root/'loadFolders.xml')
    (root/'Tests/Fixtures').mkdir(parents=True)
    shutil.copyfile(ROOT/'Tests/Fixtures/Grains_Environment.json',
                    root/'Tests/Fixtures/Grains_Environment.json')


class EnvironmentTests(unittest.TestCase):
    def test_current_matrix(self):
        self.assertTrue(validate())

    def test_no_growth_outside_temperature_range_or_below_fertility(self):
        crop = (6,13,0.5,0.4,8,18,32,42)
        for fertility,temperature in ((0.4,20),(1,8),(1,42),(1,0),(1,50)):
            self.assertEqual(output(crop,fertility,temperature,20),0)

    def test_incomplete_season_has_no_mature_harvest(self):
        self.assertEqual(output((6,13,0.5,0.4,8,18,32,42),1,20,5),0)

    def test_balance_changes_cannot_silently_change_the_matrix(self):
        for crop,field,value in ((0,'fertilityMin','0.6'),(2,'growDays','1'),
                                  (3,'maxOptimalGrowthTemperature','32'),
                                  (4,'harvestYield','200')):
            with self.subTest(field=field,crop=crop), tempfile.TemporaryDirectory() as temp:
                root=Path(temp);copy_runtime_xml(root)
                path=root/'Defs/ThingDefs_Plants/Plants_StageA.xml'
                doc=ET.parse(path);node=doc.findall('ThingDef')[crop].find('plant/'+field)
                node.text=value;doc.write(path)
                with self.assertRaises(AssertionError):validate(root)

    def test_upland_rice_balance_cannot_silently_change(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);copy_runtime_xml(root)
            path=root/'Patches/UplandRice.xml'
            doc=ET.parse(path)
            doc.find('.//value/harvestYield').text='200'
            doc.write(path)
            with self.assertRaises(AssertionError):validate(root)

    def test_upland_rice_hydroponic_sowing_cannot_return(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);copy_runtime_xml(root)
            path=root/'Patches/UplandRice.xml'
            doc=ET.parse(path)
            tags=doc.find('.//value/sowTags')
            ET.SubElement(tags,'li').text='Hydroponic'
            doc.write(path)
            with self.assertRaises(AssertionError):validate(root)


if __name__ == '__main__':unittest.main()
