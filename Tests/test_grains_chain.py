"""Reject nutrition multiplication, bread-like storage and new research gates."""
import shutil
import tempfile
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from amj_profile_xml import ROOT
from validate_grains_chain import validate


class ChainRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ('Defs','BaseWithoutMO','Compatibility'):
            shutil.copytree(ROOT/folder,self.root/folder)
        shutil.copyfile(ROOT/'loadFolders.xml',self.root/'loadFolders.xml')

    def mutate(self,path,xpath,text=None,new_element=None):
        f=self.root/path;xml=ET.parse(f);n=xml.find(xpath);assert n is not None
        if new_element is not None:n.append(ET.fromstring(new_element))
        else:n.text=text
        xml.write(f)
        with self.assertRaises(AssertionError):validate(self.root)

    def test_current_chain(self):validate(self.root)
    def test_flour_does_not_multiply_nutrition(self):
        self.mutate('BaseWithoutMO/Defs/Items_Flour.xml','ThingDef/statBases/Nutrition','0.1')
    def test_milling_does_not_create_straw(self):
        self.mutate('Defs/RecipeDefs/Recipes_GrainsMilling.xml','RecipeDef/products',new_element='<AMJC_Millet>1</AMJC_Millet>')
    def test_powder_food_not_bread_storage(self):
        self.mutate('Defs/ThingDefs_Items/Items_GrainsFood.xml','ThingDef/comps/li/daysToRotStart','8')
    def test_cooking_remains_research_free(self):
        self.mutate('Defs/RecipeDefs/Recipes_GrainsFood.xml','RecipeDef',new_element='<researchPrerequisite>Cooking</researchPrerequisite>')
    def test_mo_food_uses_mo_flour(self):
        self.mutate('Compatibility/MedievalOverhaul/Patches/MedievalOverhaul_GrainsFlour.xml','Operation[3]/value/li','AMJC_WheatFlour')
    def test_no_duplicate_fallback_in_mo(self):
        self.mutate('Defs/ThingDefs_Items/Items_GrainsFlour.xml','.',new_element='<ThingDef><defName>AMJC_WheatFlour</defName></ThingDef>')


if __name__ == '__main__':unittest.main()
