#!/usr/bin/env python3
"""Read-only by default; --write creates and deletes one marked test card."""
import argparse
import json
import subprocess
import uuid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', default='fizzy')
    parser.add_argument('--board', required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    passed = []

    def call(*argv, missing=False):
        result = subprocess.run([args.binary, *map(str, argv), '--json'],
                                capture_output=True, text=True)
        try:
            envelope = json.loads(result.stdout)
        except ValueError:
            raise RuntimeError(f'{argv[:2]} returned non-JSON (exit {result.returncode})')
        if missing:
            assert result.returncode == 2 and envelope.get('ok') is False, envelope.get('code')
        elif result.returncode or envelope.get('ok') is not True:
            raise RuntimeError(f'{argv[:2]} failed: exit={result.returncode}, code={envelope.get("code")}')
        return envelope.get('data')

    identity = call('identity', 'show')
    assert identity['accounts']
    passed.append('identity')
    board = call('board', 'show', args.board)
    assert board['id'] == args.board
    passed.append('board read')
    cards = call('card', 'list', '--board', args.board, '--all')
    assert isinstance(cards, list)
    passed.append('paginated open-card list')
    for lane in ('closed', 'not_now'):
        assert isinstance(call('card', 'list', '--board', args.board, '--indexed-by', lane, '--all'), list)
        passed.append(f'{lane} list')
    if cards:
        assert call('card', 'show', cards[0]['number'])['number'] == cards[0]['number']
        passed.append('existing card read')
    number = None
    marker = 'fizzy-cli-smoke-' + uuid.uuid4().hex[:12]
    try:
        if args.write:
            card = call('card', 'create', '--board', args.board, '--title', marker,
                        '--description', '## CLI upgrade test\n\n**Temporary** verification card.')
            number = card['number']
            print(json.dumps({'fixture_card': number, 'marker': marker}), flush=True)
            shown = call('card', 'show', number)
            assert '<h2>' in shown['description_html'] and '<strong>' in shown['description_html']
            passed.append('create and native Markdown rendering')
            link = board['url']
            html = f'<h2>HTML verification</h2><p><a href="{link}">Board</a></p>'
            call('card', 'update', number, '--description', html)
            shown = call('card', 'show', number)
            assert '<h2>' in shown['description_html'] and link in shown['description_html']
            passed.append('HTML update and link preservation')
            comment = call('comment', 'create', '--card', number, '--body', '**Smoke test**')
            comments = call('comment', 'list', '--card', number, '--all')
            assert any(c['id'] == comment['id'] and 'Smoke test' in c['body']['plain_text'] for c in comments)
            passed.append('comment create/read')
            step = call('step', 'create', '--card', number, '--content', 'Verify CLI')
            call('step', 'update', step['id'], '--card', number, '--completed')
            assert call('step', 'show', step['id'], '--card', number)['completed'] is True
            passed.append('step create/update/read')
            call('card', 'close', number)
            assert call('card', 'show', number)['closed'] is True
            call('card', 'reopen', number)
            assert call('card', 'show', number)['closed'] is False
            passed.append('close/reopen read-back')
            filtered = call('card', 'list', '--search', marker, '--board', args.board, '--all')
            assert any(c['number'] == number for c in filtered)
            passed.append('filtered search')
    finally:
        if number is not None:
            # Only delete the resource created by this invocation, after checking its marker.
            assert call('card', 'show', number)['title'] == marker
            call('card', 'delete', number)
            call('card', 'show', number, missing=True)
            passed.append('fixture deletion and not-found verification')
    print(json.dumps({'passed': passed, 'count': len(passed), 'write_test': args.write}, indent=2))


if __name__ == '__main__':
    main()
