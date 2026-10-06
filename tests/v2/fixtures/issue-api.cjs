// Execute the actual installed github-script body against a native-shaped API fixture.
const fs = require('node:fs');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const issue = structuredClone(input.issue);
const labels = new Set(input.repository_labels ?? ['wf:backlog', 'wf:done']);
const calls = [];
let transitioned = false;
const error = (status, message) => Object.assign(new Error(message), {status});
const record = (method, args) => {
  calls.push({method, args});
  if (input.fail === method) throw error(input.fail_status ?? 403, 'Denied fixture operation');
};
const methods = {
  get: async args => {
    record('get', args);
    return {data: structuredClone(issue)};
  },
  getLabel: async args => {
    record('getLabel', args);
    if (!labels.has(args.name)) throw error(404, 'Label missing');
    return {data: {name: args.name}};
  },
  createLabel: async args => {
    record('createLabel', args);
    if (input.label_creation_race) {
      labels.add(args.name);
      throw error(422, 'Already created by another job');
    }
    if (labels.has(args.name)) throw error(422, 'Label exists');
    labels.add(args.name);
    return {data: args};
  },
  addLabels: async args => {
    record('addLabels', args);
    for (const name of args.labels) {
      if (!labels.has(name)) throw error(422, 'Undefined repository label');
      if (!issue.labels.some(label => (typeof label === 'string' ? label : label.name) === name)) {
        issue.labels.push({name});
      }
    }
    if (input.add_custom_label) issue.labels.push({name: 'human-added-during-run'});
    if (input.reopen_after_add && !transitioned) {
      transitioned = true;
      issue.state = 'open';
      issue.state_reason = 'reopened';
    }
    return {data: structuredClone(issue.labels)};
  },
  removeLabel: async args => {
    record('removeLabel', args);
    if (input.remove_404) {
      issue.labels = issue.labels.filter(label => (typeof label === 'string' ? label : label.name) !== args.name);
      throw error(404, 'Concurrently removed label');
    }
    issue.labels = issue.labels.filter(label => (typeof label === 'string' ? label : label.name) !== args.name);
    if (input.close_after_remove && !transitioned) {
      transitioned = true;
      issue.state = 'closed';
      issue.state_reason = 'completed';
    }
    if (input.continuous_edit) issue.labels.push({name: 'wf:review'});
    return {data: {name: args.name}};
  }
};
// No update/setLabels endpoint: a broad replacement cannot pass this fixture.
const github = {rest: {issues: methods}};
const logs = [];
const core = {info: value => logs.push(value)};
const payload = input.dispatch ? {inputs: {issue_number: input.number ?? '17'}} : {
  issue: {...structuredClone(issue), labels: input.event_labels ?? structuredClone(issue.labels)}
};
if (input.number !== undefined && !input.dispatch) payload.issue.number = input.number;
const context = {repo: {owner: 'fixture', repo: 'consumer'}, payload};
(async () => {
  let failure = null;
  try {
    const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
    await new AsyncFunction('github', 'context', 'core', input.script)(github, context, core);
  } catch (err) {
    failure = err.message;
  }
  process.stdout.write(JSON.stringify({issue, calls, logs, failure, repository_labels: [...labels]}));
})();
