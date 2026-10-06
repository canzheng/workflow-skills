import pathlib
import sys
import unittest
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/workflow'))
from core import Conflict, Invalid
from records import render, source_match, phase_labels, managed_update, issue_findings


class RecordsTests(unittest.TestCase):
    def test_render_full_approved_catalog_without_live_state(self):
        items = render(ROOT / 'docs/v2/v2-feature-list.md')
        self.assertEqual(len(items), 14)
        self.assertIn('WF2-F14', items[-1]['body'])
        self.assertIn('**Acceptance**', items[0]['body'])
        self.assertNotIn('wf:ready', items[0]['body'])

    def test_closed_source_reused_duplicate_blocks_creation(self):
        item = dict(body='<!-- workflow-source: WF2-F04 -->', state='closed', number=7)
        self.assertEqual(source_match([item], 'WF2-F04')['number'], 7)
        self.assertIsNone(source_match([], 'WF2-F04'))
        with self.assertRaises(Conflict):
            source_match([item, dict(item, number=8)], 'WF2-F04')

    def test_phase_transition_block_defer_close_and_reopen(self):
        current = ['security', 'wf:ready', 'wf:blocked']
        self.assertEqual(phase_labels(current, 'wf:review'), ['security', 'wf:review'])
        self.assertEqual(phase_labels(current, closed=True), ['security'])
        with self.assertRaises(Invalid):
            phase_labels(current, 'wf:review', ['wf:deferred'])
        labels = phase_labels(current, 'wf:backlog', ['wf:deferred'])
        self.assertEqual(issue_findings(dict(state='open', labels=labels)), [])
        self.assertTrue(issue_findings(dict(state='open', labels=['wf:ready', 'wf:review'])))
        self.assertTrue(issue_findings(dict(state='closed', state_reason='completed', labels=[])))

    def test_remote_human_edits_are_not_overwritten(self):
        body = 'Human text\n<!-- start -->\nold\n<!-- end -->\nMore human'
        fresh = body + '\nHuman amendment'
        with self.assertRaises(Conflict):
            managed_update(body, fresh, 'new', '<!-- start -->', '<!-- end -->')
        updated = managed_update(fresh, fresh, 'new', '<!-- start -->', '<!-- end -->')
        self.assertIn('Human amendment', updated)
        self.assertIn('\nnew\n', updated)

    def test_completed_cancelled_and_reopened_label_projection(self):
        current = ['wf:review', 'wf:blocked', 'security', 'wf:custom']
        completed = phase_labels(current, closed=True, state_reason='completed')
        self.assertEqual(completed, ['security', 'wf:custom', 'wf:done'])
        cancelled = phase_labels(completed, closed=True, state_reason='not_planned')
        self.assertEqual(cancelled, ['security', 'wf:custom'])
        reopened = phase_labels(completed, 'wf:backlog')
        self.assertEqual(reopened, ['security', 'wf:backlog', 'wf:custom'])
        self.assertEqual(issue_findings(dict(state='closed', state_reason='completed',
                         labels=completed, delivery_evidence='PR and acceptance evidence')), [])
        self.assertTrue(issue_findings(dict(state='open', labels=completed + ['wf:backlog'])))
        self.assertTrue(issue_findings(dict(state='closed', state_reason='not_planned', labels=completed)))
        self.assertTrue(issue_findings(dict(state='closed', state_reason='completed', labels=completed)))
