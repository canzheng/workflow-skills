"""S33 consumer installation and native snapshot operations; no live remote claims."""
import json
import pathlib
import re
import subprocess
import tempfile
import unittest

from test_setup import ROOT, init, commit, run
from core import Conflict
from checks import links
from records import source_match, phase_labels, managed_update

CASE = ROOT / 'tests/v2/scenarios/initial-backlog'


class InitialBacklogTests(unittest.TestCase):
    def setUp(self):
        self.artifact = json.loads((CASE / 'output.json').read_text())
        self.items = self.artifact['items']

    def test_fresh_real_bundle_preserves_design_without_starting_application_work(self):
        sha = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
        with tempfile.TemporaryDirectory() as td:
            target = pathlib.Path(td) / 'fresh project'
            init(target)
            design = target / 'docs/design.md'
            design.parent.mkdir()
            design.write_bytes((CASE / 'design.md').read_bytes())
            starting = commit(target)
            branch = subprocess.check_output(['git', '-C', str(target), 'branch', '--show-current'])
            run('setup', '--target', target, '--source', ROOT, '--revision', sha, '--repository', 'fixture/pantry', '--apply')
            run('doctor', '--repo', target)
            run('check', '--repo', target)
            self.assertEqual(design.read_bytes(), (CASE / 'design.md').read_bytes())
            self.assertEqual(subprocess.check_output(['git', '-C', str(target), 'rev-parse', 'HEAD'], text=True).strip(), starting)
            self.assertEqual(subprocess.check_output(['git', '-C', str(target), 'branch', '--show-current']), branch)
            self.assertFalse((target / 'app').exists())
            self.assertFalse((target / 'docs/planning').exists())
            self.assertFalse(self.artifact['implementation_authorized'])
            for item in self.items:
                self.assertEqual(links(target, item['body'], 'ISSUE.md'), [])
            broken = self.items[0]['body'].replace('#ingredient-catalog', '#missing-design-section')
            self.assertTrue(any(x['code'] == 'links.anchor' for x in links(target, broken, 'ISSUE.md')))

    def test_one_batch_approval_and_confirmed_dependency_links_do_not_dispatch(self):
        # Explicit fixture remote snapshots, not invented real GitHub numbers.
        snapshots = []
        for number, item in enumerate(self.items, 801):
            self.assertIsNone(source_match(snapshots, item['source_id']))
            snapshots.append(dict(number=number, body=item['body'], state='open', labels=['project:pantry', 'wf:backlog']))
        self.assertEqual(len(snapshots), 5)
        self.assertTrue(all(x['labels'] == ['project:pantry', 'wf:backlog'] for x in snapshots))
        confirmed = {item['source_id']: f'https://github.com/fixture/pantry/issues/{snapshots[i]["number"]}' for i, item in enumerate(self.items)}
        # One approval covers the whole batch; availability is independently assessed.
        ready = {'pantry-planner:ingredients', 'pantry-planner:recipes'}
        for item, snapshot in zip(self.items, snapshots):
            dependencies = [confirmed[x] for x in item['requires']]
            old_marker = '<!-- workflow-requires: ' + json.dumps(item['requires']) + ' -->'
            snapshot['body'] = snapshot['body'].replace(old_marker, '<!-- workflow-requires: ' + json.dumps(dependencies) + ' -->')
            parsed = json.loads(re.search(r'<!-- workflow-requires: (.+?) -->', snapshot['body']).group(1))
            self.assertEqual(parsed, dependencies)
            snapshot['labels'] = phase_labels(snapshot['labels'], 'wf:ready' if item['source_id'] in ready else 'wf:backlog', [] if item['source_id'] in ready else ['wf:blocked'])
        self.assertEqual(sum('wf:ready' in x['labels'] for x in snapshots), 2)
        self.assertTrue(all('project:pantry' in x['labels'] for x in snapshots))
        self.assertFalse(any('wf:in-progress' in x['labels'] for x in snapshots))
        self.assertEqual({x['source_id'] for x in self.items}, {'pantry-planner:ingredients', 'pantry-planner:recipes', 'pantry-planner:dietary-policy', 'pantry-planner:meal-plan', 'pantry-planner:shopping-list'})

    def test_evolved_design_rerun_reuses_identity_and_preserves_human_acceptance(self):
        item = self.items[0]
        body = item['body'] + '\nHuman acceptance amendment: preserve identifier case.\n'
        remote = [dict(number=801, state='closed', title='Old section title', body=body)]
        match = source_match(remote, item['source_id'])
        self.assertEqual(match['number'], 801)
        self.assertEqual(match['state'], 'closed')
        replacement = item['body'].split('<!-- workflow-shaping:start -->')[1].split('<!-- workflow-shaping:end -->')[0]
        updated = managed_update(body, body, replacement, '<!-- workflow-shaping:start -->', '<!-- workflow-shaping:end -->')
        self.assertIn('Human acceptance amendment: preserve identifier case.', updated)
        conflicting = body + '\nHuman correction contradicting proposed case normalization.\n'
        with self.assertRaises(Conflict):
            managed_update(body, conflicting, replacement, '<!-- workflow-shaping:start -->', '<!-- workflow-shaping:end -->')
        with self.assertRaises(Conflict):
            source_match(remote + [dict(match, number=802)], item['source_id'])
        self.assertIsNone(source_match(remote, 'pantry-planner:explicit-new-outcome'))
        self.assertEqual(remote[0]['body'], body)
        self.assertEqual(len(remote), 1)
