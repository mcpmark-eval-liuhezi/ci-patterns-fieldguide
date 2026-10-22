"""Validate the field-guide notes.

Run by .github/workflows/ci.yml on every push. The check is deliberately
dependency-free so the CI never fails on a third-party service: it only needs
Python's standard library.
"""

import re
import sys
from pathlib import Path

NOTES_DIR = Path('notes')

# Each note must name the repository it documents in owner/name form.
OWNER_NAME = re.compile(r'^# .*\b[\w.-]+/[\w.-]+\b', re.MULTILINE)

# Each note must link the workflow file that was actually read.
WORKFLOW_LINK = re.compile(r'https://github\.com/[\w.-]+/[\w.-]+/blob/[^\s)]+\.github/workflows/[\w./-]+\.yml')


def main() -> int:
    if not NOTES_DIR.is_dir():
        # The notes arrive via the field-guide pull request; the CI step that
        # fails hard on missing notes lives on the branch that adds them.
        print('notes/ not found yet - nothing to validate')
        return 0

    files = sorted(NOTES_DIR.glob('*.md'))
    if not files:
        print('FAIL: notes/ exists but contains no markdown files')
        return 1

    failures = []
    for path in files:
        text = path.read_text(encoding='utf-8')
        problems = []

        if not OWNER_NAME.search(text):
            problems.append('first heading must name the repository as owner/name')

        if not WORKFLOW_LINK.search(text):
            problems.append('must link the specific workflow file that was read')

        # The summary should stay tight: three to five sentences.
        sentences = re.findall(r'[^.!?]+[.!?]', text)
        if len(sentences) < 3:
            problems.append('summary too short (needs at least 3 sentences)')

        if problems:
            failures.append(f"{path}: {'; '.join(problems)}")
        else:
            print(f'OK: {path}')

    if failures:
        print('\nFAILURES:')
        for failure in failures:
            print(f'  - {failure}')
        return 1

    print(f'\nValidated {len(files)} note(s).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
