# Issue #23: PR metadata credential lifetime review

Review date: 2026-10-14 (Asia/Shanghai).
Repository: canzheng/workflow-skills.
Inspected main: b0a1e53b5f1c72c0564610af0af59d38f448821d.
This document describes a local review-branch proposal, not deployed behavior.

## Finding and evidence limits

The current workflow uses pull_request_target, read-only contents/pull-requests
permissions, base-SHA checkout and persist-credentials:true. The checkout v4
source inspected at 11d5960a326750d5838078e36cf38b85af677262 writes a Basic
Authorization header into .git/config (git-auth-helper.ts configureToken and
replaceTokenPlaceholder). The Base64 payload contains x-access-token:TOKEN;
Base64 is reversible, not encryption. git-source-provider.ts removes auth before
returning only when persistCredentials is false; the normal persisted case is
cleaned up later during post-job cleanup, after checker execution.

Consequently credential readability is a concrete implementation property, not
merely a hypothetical ability to exploit a future defect. The regression probe
reproduces child-process readability and Base64 decoding using a synthetic token
in the same configuration format. No actual GITHUB_TOKEN was read, displayed or
exfiltrated during this review. No historical runner, outbound-traffic or secret
incident forensic audit was performed. There is no evidence here of unauthorized
access or a completed credential leak, and this review cannot rule one out.
The exact trusted-base pin and read-only permissions reduce current exploitability
and impact. A private-repository contents token still grants repository read access.

## Proposed YAML and rationale

The executable proposal is [pr-metadata.yml](../../.github/workflows/pr-metadata.yml).
The focused tests are [test_metadata_credentials.py](../../tests/v2/test_metadata_credentials.py).

1. Keep pull_request_target, base checkout, exact checker provenance and existing
   contents:read / pull-requests:read. Set persist-credentials:false.
2. Before loading any checker, use a dedicated Python step to parse the event as
   data, validate its base repository and a lowercase 40-character head SHA, and
   probe git cat-file -e SHA^{commit}.
3. Only when absent, fetch the exact SHA with --no-tags --depth=1
   --no-recurse-submodules from GITHUB_SERVER_URL/GITHUB_REPOSITORY.git. Do not
   use the PR head repository URL; the test also poisons origin to prove it is
   not selected for credential-bearing transport.
4. Supply Basic authentication with --config-env=http.URL.extraheader=WF2_FETCH_AUTH.
   This keeps the header out of argv and all persistent Git config files.
   Disable credential helpers for that command, interactive prompting and HTTP
   redirects. No token-bearing URL or temporary credential file is created.
5. Require successful fetch and a second commit-object probe. Any fetch failure
   stops the step/job before checker preparation, with no privilege escalation.
6. Run the existing pinned checker unchanged. It finds the local commit and reads
   git show SHA:path; the CLI's fallback fetch remains available outside this CI.

Git documents --config-env as command-scope configuration. The shorter alternative
`git -c http.extraheader="AUTHORIZATION: basic ..." fetch ...` also avoids writing
config but puts the secret value in process argv. This proposal avoids that
additional exposure. Neither approach prevents the fetch process or its children
from reading the header while authentication is required.

## Credential lifecycle

| Boundary | Credential availability | Persistent state |
| --- | --- | --- |
| checkout v4 | Action uses the job token for checkout | With false, action removes its temporary auth before returning |
| Dedicated fetch step shell/Python | Token is a step-only environment value; Python pops it before launching Git | Never written to Git config or GITHUB_ENV |
| cat-file probe | No WF2_FETCH_TOKEN or WF2_FETCH_AUTH inherited | No credential state written |
| Authenticated fetch process tree | Header supplied in its environment; raw step token is not inherited by Git | Object/FETCH_HEAD/shallow data may change; no auth config change |
| Checker preparation and checker steps | Neither custom token nor header variable is passed | Base checkout config contains no checkout/fetch token |
| Fetch failure | Step exits nonzero; later steps do not run | No credential cleanup file/trap is required |

Step isolation is a lifetime boundary, not secure memory erasure. The parent shell
and Python process have access to the token during the fetch step; Git transport
children can read the header. This is not isolation from a compromised runner or
concurrent same-user processes. Use the workflow's existing fresh ubuntu-latest
runner assumption. Do not move authentication to job-level env, GITHUB_ENV,
credential.store, local/global git config, or a wrapper that also runs the checker.

## Checker dependencies and preserved behavior

The current metadata-only path reads trusted-base .workflow/config.json, the event,
PR section text and head Git blobs. It does not need the branch checked out, a
merge commit, ancestor traversal, tags, submodules, configured application commands
or a modified index. A depth-one head fetch suffices for these current operations.
The tests validate a head-only Markdown link, preserving base HEAD, index and
worktree. Git object storage, FETCH_HEAD and shallow metadata are expected to change.
A deleted/unavailable head or denied repository access remains a failing check;
there is no silent success or permission expansion.

Consumer workflows are installed from the source workflow through the bundle asset
mapping. Existing consumers must adopt a reviewed new exact source revision with
normal setup preview/apply so their manifest hashes remain consistent. Do not
hand-edit the managed workflow in consumer repositories. Operations guidance and
the current quality spec are updated with this proposal.

## Local verification

The six focused tests execute the actual YAML fetch block, using Git 2.51.1 and a
local HTTP server backed by real git http-backend, gated on a synthetic Basic
credential. They cover:

- persisted-header readability and reversible decoding in a child process;
- missing head: an unauthenticated fetch first fails with HTTP 401, then the
  dedicated authenticated fetch succeeds and the checker validates a head-only
  link without any network call or authentication;
- process-boundary audit: only fetch receives the header, Git receives no raw
  step-token variable or header value in argv, and checker Git subprocesses
  receive neither token nor header;
- head already present: no HTTP request, even with an invalid token;
- denied authentication: nonzero exit, missing head remains missing, config/index/
  base HEAD/worktree unchanged and synthetic credentials absent from output;
- invalid SHA / mismatched repository: rejected before any HTTP request;
- base-repository selection despite a poisoned origin and attacker head URL;
- checkout persistence disabled and token injection limited to the fetch step.

Commands:

```sh
python3 -m unittest discover -s tests/v2 -p test_metadata_credentials.py -v
python3 -m unittest discover -s tests/v2 -p test_consumer_ci.py -v
python3 tools/workflow/verify.py
git diff --check
```

Focused credential tests: 6 passed. Consumer CI tests: 4 passed.
YAML parsed successfully and both embedded Python blocks compiled. The current
repository check and pinned OpenSpec 1.14.0 validation returned ok:true with no
findings. The first full run executed 210 tests: 206 passed, two OpenSpec tests were
skipped before npm ci completed, and two real-source installation tests rejected
the dirty source because its asset bytes differed from the HEAD pin. The proposal
was then committed locally to give those tests a valid exact revision, and the
full suite was rerun with the locked OpenSpec runtime installed. Final rerun on code commit cc9c6b6fc33eb84db628016c2120511e5f9e7a43:
all 210 tests passed, with no skips; the subsequent repository check also passed.
This result covers Python 3.12.14 and Git 2.51.1 locally, not the Actions runner
or its second Python 3.14 matrix leg. A documentation-only follow-up records
this evidence without changing executable assets.

## Required real GitHub Actions acceptance (pending)

No remote changes, PR publication or Actions dispatch were performed. A local
HTTP authentication gate is not a real private GitHub repository or GITHUB_TOKEN
policy test. After the reviewed change is active on a trusted base, run:

1. A private-repository PR whose new head SHA is absent from the depth-one base
   checkout. Include a PR-body link to a document existing only at head. Expect
   prefetch and metadata success while base HEAD/index/worktree stay unchanged.
2. At checker entry, assert absence (without printing values) of extraheader auth,
   credential-helper files, token-bearing remote URLs and the two custom credential
   env variables in checkout/config/global/worktree state. Verify GITHUB_ENV has
   no auth material. Never dump configuration values or process environments.
3. Exercise the supported fork-PR case, if enabled, and synchronize to a new head;
   verify the base-repository endpoint can retrieve that exact SHA with read-only
   GITHUB_TOKEN. Local tests do not prove GitHub fork object visibility.
4. Negative metadata control: remove Documentation text and expect metadata failure;
   retain it and break a head-only link and expect links.path. Restore and rerun.
5. Simulate denied authentication in a controlled test workflow and verify prefetch
   failure prevents checker preparation/execution. Keep the token scopes unchanged.

Because pull_request_target uses trusted-base workflow code, a PR proposing this
YAML may still run the old base workflow. A green premerge check is not evidence
that this new credential lifetime has executed. Record the actual workflow revision
and private-repository run URL before marking integration acceptance complete.

## Primary sources

- [Issue #23](https://github.com/canzheng/workflow-skills/issues/23)
- [Inspected workflow](https://github.com/canzheng/workflow-skills/blob/b0a1e53b5f1c72c0564610af0af59d38f448821d/.github/workflows/pr-metadata.yml)
- [Inspected checker](https://github.com/canzheng/workflow-skills/blob/b0a1e53b5f1c72c0564610af0af59d38f448821d/tools/workflow/checks.py)
- [checkout auth helper](https://github.com/actions/checkout/blob/11d5960a326750d5838078e36cf38b85af677262/src/git-auth-helper.ts)
- [checkout cleanup lifecycle](https://github.com/actions/checkout/blob/11d5960a326750d5838078e36cf38b85af677262/src/git-source-provider.ts)
- [Git command configuration](https://git-scm.com/docs/git)
- [Git configuration scopes](https://git-scm.com/docs/git-config)
