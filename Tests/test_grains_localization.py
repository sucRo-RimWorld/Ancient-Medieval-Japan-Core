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


RICE_ITEMS = {'AMJC_RiceSheaf', 'AMJC_RiceInHull'}
RICE_RECIPES = {'AMJC_ThreshRice', 'AMJC_ThreshRiceBulk',
                'AMJC_HullRice', 'AMJC_HullRiceBulk'}


def validate_rice_localizations(root):
    """Reject drift from the approved JP-first rice processing copy in §10.

    Checks live JP labels/descriptions/jobStrings and English XML defaults.
    It does not claim runtime UI language-switching or historical provenance.
    """
    import re
    source = (root / 'Docs/LocalizationHistoricalReview.md').read_text(encoding='utf-8')
    assert '## 10. 陸稲の新加工語彙' in source
    chapter = source.split('## 10. 陸稲の新加工語彙', 1)[1]
    entries, jobs = {}, {}
    for line in chapter.splitlines():
        matched = re.fullmatch(r'- `(AMJC_[A-Za-z]+)`：(.+?)。(.+?)English: \*\*([^*]+)\*\* — (.+)', line)
        if matched:
            name, jp_label, jp_desc, en_label, en_desc = matched.groups()
            assert name not in entries, 'Duplicate approved rice description: ' + name
            entries[name] = (jp_label.strip(' *'), jp_desc.strip(), en_label.strip(), en_desc.strip())
        matched_job = re.fullmatch(r'- `(AMJC_[A-Za-z]+)\.jobString`：(.+?) / (.+)', line)
        if matched_job:
            name, jp, en = matched_job.groups()
            assert name not in jobs, 'Duplicate approved rice jobString: ' + name
            jobs[name] = (jp.strip(), en.strip())
    assert set(entries) == RICE_ITEMS | RICE_RECIPES, 'Rice approved description inventory changed'
    assert set(jobs) == RICE_RECIPES, 'Rice approved jobString inventory changed'

    thing_source = ET.parse(root / 'Defs/ThingDefs_Items/Items_StageA_Grains.xml').getroot()
    recipe_source = ET.parse(root / 'Defs/RecipeDefs/Recipes_GrainProcessing.xml').getroot()
    jp_items = ET.parse(root / 'Languages/Japanese/DefInjected/ThingDef/AMJC_RiceProcessing.xml').getroot()
    jp_recipes = ET.parse(root / 'Languages/Japanese/DefInjected/RecipeDef/AMJC_RiceProcessing.xml').getroot()
    for name, (ja_label, ja_desc, en_label, en_desc) in entries.items():
        source_group = thing_source if name in RICE_ITEMS else recipe_source
        jp_group = jp_items if name in RICE_ITEMS else jp_recipes
        nodes = [node for node in source_group if node.findtext('defName') == name]
        assert len(nodes) == 1, 'Missing or duplicate rice Def: ' + name
        node = nodes[0]
        assert node.findtext('label') == en_label, 'English rice label drift: ' + name
        assert node.findtext('description') == en_desc, 'English rice description drift: ' + name
        assert jp_group.findtext(name + '.label') == ja_label, 'Japanese rice label drift: ' + name
        assert jp_group.findtext(name + '.description') == ja_desc, 'Japanese rice description drift: ' + name
        if name in RICE_RECIPES:
            assert node.findtext('jobString') == jobs[name][1], 'English rice jobString drift: ' + name
            assert jp_group.findtext(name + '.jobString') == jobs[name][0], 'Japanese rice jobString drift: ' + name


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

    def test_approved_rice_processing_copy_matches_source(self):
        validate_rice_localizations(ROOT)

    def test_rice_copy_mutations_are_rejected(self):
        import shutil
        import tempfile
        relative = (
            'Docs/LocalizationHistoricalReview.md',
            'Defs/ThingDefs_Items/Items_StageA_Grains.xml',
            'Defs/RecipeDefs/Recipes_GrainProcessing.xml',
            'Languages/Japanese/DefInjected/ThingDef/AMJC_RiceProcessing.xml',
            'Languages/Japanese/DefInjected/RecipeDef/AMJC_RiceProcessing.xml',
        )
        for target, old, new in (
            (relative[1], '<label>rice sheaf</label>', '<label>unreviewed sheaf</label>'),
            (relative[3], '収穫した稲を束ねたもの。', '収穫した稲を乾燥させたもの。'),
            (relative[2], '<jobString>Hulling rice in bulk.</jobString>',
             '<jobString>Milling rice in bulk.</jobString>'),
            (relative[0], '籾10個をまとめて籾摺りし', '籾100個をまとめて籾摺りし'),
        ):
            with self.subTest(file=target), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for name in relative:
                    destination = root / name
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(ROOT / name, destination)
                original = (root / target).read_text(encoding='utf-8')
                self.assertIn(old, original)
                (root / target).write_text(original.replace(old, new), encoding='utf-8')
                with self.assertRaises(AssertionError):
                    validate_rice_localizations(root)

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

    def test_six_approved_crop_descriptions_match_live_japanese_and_english(self):
        review = (ROOT/'Docs/LocalizationHistoricalReview.md').read_text(encoding='utf-8')
        self.assertIn('## 7. 既存六作物の承認済み歴史説明', review)
        self.assertIn('## 8. English descriptions translated', review)
        japanese_section = review.split('## 7.', 1)[1].split('## 8.', 1)[0]
        english_section = review.split('## 8.', 1)[1]
        self.assertIn('日本語説明を作者承認済み', japanese_section)

        def approved_table(section):
            rows = {}
            for line in section.splitlines():
                if not line.startswith('| `'):
                    continue
                cells = [cell.strip() for cell in line.split('|')]
                name = cells[1].strip('`')
                self.assertNotIn(name, rows, 'duplicate approved crop: ' + name)
                rows[name] = cells[2].replace('**', '').replace('。 ', '。')
            return rows

        japanese = approved_table(japanese_section)
        english = approved_table(english_section)
        names = {
            'AMJC_Plant_FoxtailMillet_Awa': '粟（あわ）',
            'AMJC_Plant_BarnyardMillet_Hie': '稗（ひえ）',
            'AMJC_Plant_ProsoMillet_Kibi': '黍（きび）',
            'AMJC_Plant_Buckwheat_Soba': '蕎麦（そば）',
            'AMJC_Plant_Barley': '大麦（おおむぎ）',
            'Plant_Rice': '陸稲（おかぼ・りくとう）',
        }
        self.assertEqual(set(japanese), set(names))
        self.assertEqual(set(english), set(names))
        localizations = all_localizations('Languages/Japanese/DefInjected')
        plants = {
            item.findtext('defName'): item
            for item in ET.parse(ROOT/'Defs/ThingDefs_Plants/Plants_StageA.xml').getroot()
            if item.tag == 'ThingDef'
        }
        for name, name_form in names.items():
            self.assertTrue(japanese[name].startswith(name_form), name)
            self.assertIn('AMJGrains', japanese[name], name)
            self.assertIn('AMJGrains', english[name], name)
            self.assertIn(name + '.label', localizations)
            self.assertEqual(localizations[name + '.description'], japanese[name],
                             'Japanese crop description drift: ' + name)
            if name != 'Plant_Rice':
                self.assertIn(name, plants)
                self.assertEqual(plants[name].findtext('description'), english[name],
                                 'English PlantDef description drift: ' + name)

        patches = ET.parse(ROOT/'Patches/UplandRice.xml').getroot()
        rice_target = '/Defs/ThingDef[defName="Plant_Rice"]/description'
        matched = [node.findtext('value/description') for node in patches.findall('.//li')
                   if node.findtext('xpath') == rice_target]
        self.assertEqual(matched, [english['Plant_Rice']],
                         'English upland rice Patch description drift')
        self.assertIn('霜への強さまで保証するものではない',
                      japanese['AMJC_Plant_BarnyardMillet_Hie'])
        self.assertIn('does not guarantee greater resistance to frost',
                      english['AMJC_Plant_BarnyardMillet_Hie'])
        self.assertIn('古い蕎麦の食べ方と', japanese['AMJC_Plant_Buckwheat_Soba'])
        self.assertIn('Edo period', english['AMJC_Plant_Buckwheat_Soba'])

        properties = {name: node.find('plant') for name, node in plants.items()}
        self.assertLess(float(properties['AMJC_Plant_BarnyardMillet_Hie'].findtext('minGrowthTemperature')),
                        float(properties['AMJC_Plant_FoxtailMillet_Awa'].findtext('minGrowthTemperature')))
        self.assertLess(float(properties['AMJC_Plant_ProsoMillet_Kibi'].findtext('growDays')),
                        float(properties['AMJC_Plant_FoxtailMillet_Awa'].findtext('growDays')))
        self.assertLess(float(properties['AMJC_Plant_Buckwheat_Soba'].findtext('growDays')),
                        float(properties['AMJC_Plant_Barley'].findtext('growDays')))
        upland = (ROOT/'Patches/UplandRice.xml').read_text(encoding='utf-8')
        self.assertIn('<fertilityMin>0.7</fertilityMin>', upland)
        self.assertIn('<minGrowthTemperature>10</minGrowthTemperature>', upland)
        self.assertIn('<maxGrowthTemperature>42</maxGrowthTemperature>', upland)

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
        en = table(audit.split('## 6.', 1)[1].split('## 7.', 1)[0])
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
