"""Structural studies are not evidence of natural contact or production activation."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'Docs/References/AMJ_Masu_Template.json'
spec = importlib.util.spec_from_file_location('fixed_template', ROOT / 'Scripts/Art/fixed_template.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class MasuTemplateTest(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(MANIFEST.read_text(encoding='utf-8'))
        self.master, self.masks, self.required = module.load_contact_contract(MANIFEST)

    def filled_context(self):
        context = self.master.copy()
        context.paste((180, 150, 105, 255), (0, 0, 256, 256), self.required)
        return context

    def test_production_and_scaffold_fail_closed(self):
        self.assertEqual(self.data['production_status'], 'blocked_pending_occlusion_validation')
        self.assertEqual(self.data['new_resource_production_status'], 'blocked_pending_occlusion_validation')
        self.assertEqual(self.data['layer_model'], module.CONTACT_MODEL)
        self.assertNotIn('front_occluder_regions', self.data)
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp) / 'context.png', Path(tmp) / 'final.png'
            self.filled_context().save(source)
            with self.assertRaisesRegex(ValueError, 'production is blocked'):
                module.compose(MANIFEST, source, output)
            with self.assertRaisesRegex(ValueError, 'production is blocked'):
                module.scaffold(MANIFEST, output)
            self.assertFalse(output.exists())

    def test_exact_identity_evidence_is_preserved(self):
        legacy = self.data['legacy_identity_exemplar']
        source = MANIFEST.parent / legacy['variable_layer_path']
        expected = MANIFEST.parent / legacy['expected_final_path']
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), legacy['variable_layer_sha256'])
        self.assertEqual(hashlib.sha256(expected.read_bytes()).hexdigest(), legacy['expected_final_sha256'])
        _, mask = module.load_template(MANIFEST)
        with Image.open(source) as layer, Image.open(expected) as exemplar:
            identity = Image.composite(layer.convert('RGBA'), self.master, mask)
            self.assertEqual(list(identity.get_flattened_data()), list(exemplar.convert('RGBA').get_flattened_data()))
            # Exemplar passes structure, but is not a contrasting-shape test.
            module.validate_contact_final(MANIFEST, exemplar)

    def test_empty_scaffold_is_intact_but_cannot_pass_fill(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'context.png'
            module.scaffold(MANIFEST, output, study=True)
            with Image.open(output) as context:
                self.assertEqual(list(context.get_flattened_data()), list(self.master.get_flattened_data()))
        module.validate_contact_final(MANIFEST, self.master, require_fill=False)
        with self.assertRaisesRegex(ValueError, 'under-fills'):
            module.validate_contact_final(MANIFEST, self.master)
        with self.assertRaisesRegex(ValueError, 'object-only'):
            module.validate_variable_layer(MANIFEST, Image.new('RGBA', (256, 256)))

    def test_same_masks_allow_contrasting_synthetic_shapes_without_clipping(self):
        # Only structural fixtures: these are deliberately not production art.
        before = {k: im.tobytes() for k, im in self.masks.items()}
        contexts = [self.filled_context() for _ in range(3)]
        ImageDraw.Draw(contexts[1]).ellipse((95, 12, 155, 80), fill=(105, 120, 60, 255))
        ImageDraw.Draw(contexts[2]).line([(70, 75), (150, 186)], fill=(195, 110, 65, 255), width=12)
        # Strong front-wall overlap survives; broad foreground restore would cut it.
        self.assertEqual(self.masks['contact_zone'].getpixel((150, 186)), 255)
        for context in contexts:
            with tempfile.TemporaryDirectory() as tmp:
                source, output = Path(tmp) / 'context.png', Path(tmp) / 'study.png'
                context.save(source)
                module.compose(MANIFEST, source, output, study=True)
                with Image.open(output) as result:
                    self.assertEqual(list(result.get_flattened_data()), list(context.get_flattened_data()))
        self.assertEqual(before, {k: im.tobytes() for k, im in self.masks.items()})
        self.assertEqual(self.data['production_status'], 'blocked_pending_occlusion_validation')

    def test_hard_fixed_restoration_copies_all_rgba_including_antialias(self):
        context = self.filled_context()
        for y in range(256):
            for x in range(256):
                if self.masks['hard_fixed'].getpixel((x, y)):
                    context.putpixel((x, y), (255, 0, 255, 0))
        with self.assertRaisesRegex(ValueError, 'HardFixed'):
            module.validate_contact_final(MANIFEST, context)
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp) / 'context.png', Path(tmp) / 'study.png'
            context.save(source)
            module.compose(MANIFEST, source, output, study=True)
            with Image.open(output) as result:
                for a, b, h in zip(result.get_flattened_data(), self.master.get_flattened_data(), self.masks['hard_fixed'].get_flattened_data()):
                    if h:
                        self.assertEqual(a, b)

    def test_forbidden_rgba_leaks_are_rejected_not_clipped(self):
        for color in [(255, 0, 0, 255), (1, 2, 3, 0), (1, 2, 3, 1)]:
            context = self.filled_context()
            context.putpixel((0, 0), color)
            with self.assertRaisesRegex(ValueError, 'forbidden'):
                module.validate_contact_final(MANIFEST, context)
            with tempfile.TemporaryDirectory() as tmp:
                source, output = Path(tmp) / 'context.png', Path(tmp) / 'study.png'
                context.save(source)
                with self.assertRaisesRegex(ValueError, 'forbidden'):
                    module.compose(MANIFEST, source, output, study=True)
                self.assertFalse(output.exists())

    def test_transparent_erasure_does_not_count_as_fill(self):
        context = self.master.copy()
        context.paste((0, 0, 0, 0), (0, 0, 256, 256), self.required)
        with self.assertRaises(ValueError):
            module.validate_contact_final(MANIFEST, context)

    def test_registered_mask_hash_binary_and_disjoint_guards(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'manifest.json'
            data = json.loads(MANIFEST.read_text(encoding='utf-8'))
            for entry in [data[k] for k in ('master', 'editable_mask', 'required_fill', 'representative_final')] + [data['region_contract'][k] for k in self.masks]:
                entry['path'] = str((MANIFEST.parent / entry['path']).resolve())
            mask = self.masks['extension_allowed'].copy()
            hard_point = next((x, y) for y in range(256) for x in range(256) if self.masks['hard_fixed'].getpixel((x, y)))
            mask.putpixel(hard_point, 255)  # overlaps HardFixed
            altered = Path(tmp) / 'altered.png'
            for value, error in [(255, 'overlap'), (128, 'binary')]:
                mask.putpixel(hard_point, value)
                mask.save(altered)
                data['region_contract']['extension_allowed'] = {'path': str(altered), 'sha256': hashlib.sha256(altered.read_bytes()).hexdigest()}
                path.write_text(json.dumps(data), encoding='utf-8')
                with self.assertRaisesRegex(ValueError, error):
                    module.load_contact_contract(path)
            altered.write_bytes(b'corrupt')
            with self.assertRaisesRegex(ValueError, 'SHA-256'):
                module.load_contact_contract(path)

    def test_studies_cannot_overwrite_sources_or_production(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'context.png'
            self.filled_context().save(source)
            for target in [source, MANIFEST.parent / self.data['representative_final']['path'], MANIFEST.parent / self.data['legacy_identity_exemplar']['variable_layer_path']]:
                with self.assertRaisesRegex(ValueError, 'overwrite'):
                    module.compose(MANIFEST, source, target, study=True)
                if target != source:
                    with self.assertRaisesRegex(ValueError, 'overwrite'):
                        module.scaffold(MANIFEST, target, study=True)
            for folder in ['Textures', 'Docs/References']:
                with self.assertRaisesRegex(ValueError, 'Study output'):
                    module.compose(MANIFEST, source, ROOT / folder / 'forbidden-study.png', study=True)


if __name__ == '__main__':
    unittest.main()
