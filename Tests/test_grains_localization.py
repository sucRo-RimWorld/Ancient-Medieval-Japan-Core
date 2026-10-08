"""Static Grains JP localization source audit; not historical approval or a game loader test."""
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARED_THINGS = {
    'AMJC_BuckwheatFlour', 'AMJC_MilletFlour', 'AMJC_Houtou',
    'AMJC_Sobagaki', 'AMJC_MilletDumplings',
}
SHARED_RECIPES = {
    'AMJC_MillBuckwheat', 'AMJC_MillMillet', 'AMJC_CookHoutou',
    'AMJC_CookSobagaki', 'AMJC_CookMilletDumplings',
}
BASE_THINGS = {
    'AMJC_Plant_Wheat', 'AMJC_RawWheat',
    'AMJC_WheatFlour', 'AMJC_ManualMillstone',
}
BASE_RECIPES = {'AMJC_MillWheat'}


def labels(relative_path):
    return ET.parse(ROOT / relative_path).getroot()


def all_localizations(*bases):
    found = {}
    for base in bases:
        for path in sorted((ROOT / base).rglob('*.xml')):
            for node in ET.parse(path).getroot():
                assert node.tag not in found, 'Duplicate localized key: ' + node.tag
                found[node.tag] = node.text or ''
    return found


class JapaneseLocalizationAudit(unittest.TestCase):
    def test_labels_and_approved_description_inventory(self):
        audit = (ROOT / 'Docs/LocalizationHistoricalReview.md').read_text(encoding='utf-8')
        self.assertIn('作者承認済み', audit)
        shared = all_localizations('Languages/Japanese/DefInjected')
        vanilla = all_localizations('Languages/Japanese/DefInjected',
                                    'BaseWithoutMO/Languages/Japanese/DefInjected')
        medieval = all_localizations('Languages/Japanese/DefInjected',
                                     'Compatibility/MedievalOverhaul/Languages/Japanese/DefInjected')
        self.assertIn('Plant_Rice.label', shared)
        self.assertIn('Plant_Rice.description', shared)
        for name in sorted(SHARED_THINGS | SHARED_RECIPES):
            self.assertTrue(shared.get(name + '.label', '').strip(), name)
            self.assertIn('`' + name + '`', audit, name)
        for name in sorted(BASE_THINGS | BASE_RECIPES):
            self.assertTrue(vanilla.get(name + '.label', '').strip(), name)
            self.assertIn('`' + name + '`', audit, name)
        for name in BASE_THINGS | BASE_RECIPES:
            self.assertNotIn(name + '.label', medieval, 'Base-only label leaked into MO: ' + name)
        for name in ('AMJC_ThreshWheat', 'AMJC_ThreshWheatBulk'):
            self.assertIn(name + '.description', vanilla)
            self.assertIn(name + '.description', medieval)

    def test_base_facts_match_real_recipe_outputs(self):
        shared = labels('Languages/Japanese/DefInjected/RecipeDef/AMJC_StageA.xml')
        base = labels('BaseWithoutMO/Languages/Japanese/DefInjected/RecipeDef/AMJC_MOWheat.xml')
        mo = labels('Compatibility/MedievalOverhaul/Languages/Japanese/DefInjected/RecipeDef/AMJC_MOWheat.xml')
        for crop in ('Millet', 'Buckwheat', 'Barley'):
            for suffix in ('', 'Bulk'):
                key = 'AMJC_Thresh' + crop + suffix + '.description'
                node = shared.find(key)
                self.assertIsNotNone(node, key)
                self.assertNotIn('藁', node.text or '', key + ' cannot claim Base straw output')
                self.assertIn('殻付き', node.text or '', key)
        for suffix in ('', 'Bulk'):
            key = 'AMJC_ThreshWheat' + suffix + '.description'
            self.assertNotIn('藁', base.findtext(key), key)
            self.assertIn('藁', mo.findtext(key), key)
        for path in ('Defs/RecipeDefs/Recipes_GrainProcessing.xml',
                     'BaseWithoutMO/Defs/Recipes_Wheat.xml'):
            document = ET.parse(ROOT / path).getroot()
            for recipe in document.findall('RecipeDef'):
                if (recipe.findtext('defName') or '').startswith('AMJC_Thresh'):
                    self.assertIsNone(recipe.find('products/DankPyon_Straw'))
        mo_recipes = [
            recipe for recipe in ET.parse(
                ROOT / 'Compatibility/MedievalOverhaul/Defs/Recipes_MOWheat.xml').getroot().findall('RecipeDef')
            if (recipe.findtext('defName') or '') in ('AMJC_ThreshWheat', 'AMJC_ThreshWheatBulk')
        ]
        self.assertEqual(len(mo_recipes), 2)
        for recipe in mo_recipes:
            self.assertIsNotNone(recipe.find('products/DankPyon_Straw'))

    def test_shared_thing_explanations_do_not_claim_unimplemented_features(self):
        things = labels('Languages/Japanese/DefInjected/ThingDef/AMJC_StageA.xml')
        barley = things.findtext('AMJC_Plant_Barley.description')
        edible = things.findtext('AMJC_Barley.description')
        wheat = things.findtext('AMJC_Wheat.description')
        self.assertNotIn('基礎農業研究が必要', barley)
        self.assertNotIn('麦茶', edible)
        self.assertNotIn('麦味噌', edible)
        self.assertNotIn('Medieval Overhaul', wheat)
        self.assertIn('製粉', wheat)

    def test_approved_japanese_english_parity_and_recipe_work_strings(self):
        audit = (ROOT/'Docs/LocalizationHistoricalReview.md').read_text(encoding='utf-8')
        self.assertIn('作者承認済み', audit)
        self.assertIn('国土交通省', audit)
        self.assertIn('## 6. English localization', audit)

        def table(section):
            values = {}
            for line in section.splitlines():
                if not line.startswith('| `AMJC_'):
                    continue
                cells = [cell.strip() for cell in line.split('|')]
                if len(cells) < 4 or not cells[1].startswith('`AMJC_') or not cells[1].endswith('`'):
                    continue
                name = cells[1].strip('`')
                description = cells[2].replace('**', '').replace('。 ', '。')
                job = cells[3] if len(cells) >= 5 and cells[3] != '—' else ''
                self.assertNotIn(name, values, 'duplicate approval row')
                values[name] = (description, job)
            return values

        jp = table(audit.split('## 2.', 1)[1].split('## 3.', 1)[0])
        en = table(audit.split('## 6.', 1)[1])
        names = SHARED_THINGS | SHARED_RECIPES | BASE_THINGS | BASE_RECIPES
        self.assertEqual(set(jp), names)
        self.assertEqual(set(en), names)

        japanese = all_localizations('Languages/Japanese/DefInjected',
                                    'BaseWithoutMO/Languages/Japanese/DefInjected')
        source_groups = (
            ('Defs/ThingDefs_Items/Items_GrainsFlour.xml', SHARED_THINGS),
            ('Defs/ThingDefs_Items/Items_GrainsFood.xml', SHARED_THINGS),
            ('Defs/RecipeDefs/Recipes_GrainsMilling.xml', SHARED_RECIPES),
            ('Defs/RecipeDefs/Recipes_GrainsFood.xml', SHARED_RECIPES),
            ('BaseWithoutMO/Defs/Plants_Wheat.xml', BASE_THINGS),
            ('BaseWithoutMO/Defs/Items_Wheat.xml', BASE_THINGS),
            ('BaseWithoutMO/Defs/Items_Flour.xml', BASE_THINGS),
            ('BaseWithoutMO/Defs/Buildings_Millstone.xml', BASE_THINGS),
            ('BaseWithoutMO/Defs/Recipes_Milling.xml', BASE_RECIPES),
        )
        seen = set()
        for path, relevant in source_groups:
            for node in ET.parse(ROOT/path).getroot():
                name = node.findtext('defName')
                if name not in relevant:
                    continue
                self.assertNotIn(name, seen, 'duplicate Def across runtime scopes: ' + name)
                seen.add(name)
                self.assertEqual(japanese[name+'.description'], jp[name][0],
                                 'Japanese description drift: ' + name)
                self.assertEqual(node.findtext('description'), en[name][0],
                                 'English description drift: ' + name)
                if name in SHARED_RECIPES | BASE_RECIPES:
                    self.assertTrue(jp[name][1], 'missing Japanese jobString: ' + name)
                    self.assertTrue(en[name][1], 'missing English jobString: ' + name)
                    self.assertEqual(japanese[name+'.jobString'], jp[name][1])
                    self.assertEqual(node.findtext('jobString'), en[name][1])
                else:
                    self.assertEqual(jp[name][1], '')
                    self.assertEqual(en[name][1], '')
        self.assertEqual(seen, names)

        wheat = japanese['AMJC_Plant_Wheat.description']
        self.assertIn('小麦の穀粒は食事の材料に使え', wheat)
        self.assertNotIn('実は食材になる', wheat)
        for name in ('AMJC_MilletFlour', 'AMJC_Plant_Wheat',
                     'AMJC_WheatFlour', 'AMJC_ManualMillstone'):
            self.assertIn('AMJGrains', japanese[name+'.description'], name)
            self.assertIn('AMJGrains', en[name][0], name)
        self.assertIn('料理として同一だったとは断定できない',
                      japanese['AMJC_Houtou.description'])
        self.assertIn('cannot be assumed to be the same dish',
                      en['AMJC_Houtou'][0])


if __name__ == '__main__':
    unittest.main()
