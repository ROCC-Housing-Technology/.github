# Shared issue templates

The public `.github` repository is the source of truth for ROCC product issue templates.
Do not add a local `.github/ISSUE_TEMPLATE` directory to a product repository: even
a local configuration file suppresses **all** organisation defaults.

## Bug reports

`bug_report.yml` sets native issue type **Bug**. It collects Product, Interested
customers, Version, Environment, Actual result, Expected result, Steps to reproduce,
Impact, Severity and optional Evidence. Unknown information can be stated honestly.

The required **Report format** dropdown defaults to **ROCC bug report v1**. This is
a real submitted field, not a markdown-only block. The bot must detect this exact
heading/value before parsing the form. Keep headings and options coordinated with
the issue-field parser. The form itself does not populate arbitrary issue fields:
the bot maps validated answers to Product and Other Interested. No private customer
roster belongs in this public repository. Customer names must not be submitted to
public issues; use the private reporting channel instead.

Native Bug type does not depend on repository labels. Severity is the reporter's
proposal for triage, not a priority or a release decision.

## Other work

Feature, Task, Decision and Risk templates remain available. The Feature and Task
templates set their native issue types. Blank issues remain available so the bot can
flag unstructured or incomplete bug reports. This changes Attend and Resolve's
previous repository-local blank-issue restriction. The separate
backport request template is retired; no replacement backport category is introduced.

## Rollout order

1. Review and deploy the companion bug-field automation, including its failure/
   missing-information handling, before relying on automatic fields.
2. Merge this shared-template change into this repository's default branch.
3. Verify the new-issue chooser on a product with no local templates.
4. Merge the dependent removal PRs for Attend, Resolve and Mobile Legacy.
5. Verify their choosers contain Bug, Feature, Task, Decision and Risk, with no
   local/backport duplicates and a working blank-issue route. Preview a bug and verify
   the format marker and supplied version are in the submitted body.

Customer Funded's specialised request forms are intentionally retained; that
repository is not a product-template inheritance target.

GitHub reads templates from default branches. Draft PRs cannot change the live
chooser; end-to-end inheritance/creation verification must follow merge.
Validation here checks schema and the submitted-body contract without creating
test issues or claiming a pre-merge live inheritance test.

## Validation

`python -m pip install PyYAML==6.0.3`
`python scripts/validate_issue_templates.py`

GitHub documentation:
- https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
- https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file
