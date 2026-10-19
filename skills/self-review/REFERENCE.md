# Self Review GitHub API Reference

Read the section for the current step. Replace `<pr-number>` and IDs. `gh api` supports the `{owner}/{repo}` placeholders.

## Read the PR

```bash
git status --short --branch
gh pr view <pr-number> --json number,title,url,author,baseRefName,headRefName,headRefOid,reviewDecision,statusCheckRollup
gh pr diff <pr-number>
```

For focused context, fetch refs as needed and use local Git:

```bash
git diff --unified=20 origin/<base-ref>...origin/<head-ref> -- path/to/file
```

Line comments must anchor to lines represented in the PR diff. `RIGHT` means the new side; `LEFT` means the old side.

## Find the current user's draft

```bash
ME=$(gh api user --jq .login)
gh api --paginate repos/{owner}/{repo}/pulls/<pr-number>/reviews \
  | jq --arg me "$ME" '[.[] | select(.state == "PENDING" and .user.login == $me) | {id,node_id,body,commit_id,user:.user.login,state}]'
gh api --paginate repos/{owner}/{repo}/pulls/<pr-number>/comments
```

Use GraphQL for thread state, diff ranges, and comment node IDs:

```bash
gh api graphql --paginate -f owner='{owner}' -f repo='{repo}' -F number=<pr-number> -f query='
query($owner:String!, $repo:String!, $number:Int!, $endCursor:String) {
  repository(owner:$owner, name:$repo) {
    pullRequest(number:$number) {
      reviewThreads(first:100, after:$endCursor) {
        nodes { id isResolved path diffSide line startDiffSide startLine comments(first:100) { nodes { id fullDatabaseId body path line startLine originalLine state author { login } pullRequestReview { id fullDatabaseId state author { login } } } pageInfo { hasNextPage endCursor } } }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}'
```

Filter comments by review ID, not only by author. If a thread's comments have another page, fetch it with that connection's cursor; outer pagination covers threads only.

## Create a new pending review

Use only after inventory confirms no current-user pending review. Omit `event`:

```bash
cat <<'EOF' | gh api repos/{owner}/{repo}/pulls/<pr-number>/reviews --method POST --input -
{
  "body": "Review summary",
  "comments": [
    {"path":"path/to/file.js", "line":42, "side":"RIGHT", "body":"Actionable comment"}
  ]
}
EOF
```

For suggestions, create an empty review, save `.node_id`, then add threads with the GraphQL mutation below.

## Reconcile in place

Add, update, or delete comments within the existing pending review. Preserve the review ID. Re-read before writing as required by [self-review](SKILL.md#2-compare-findings-and-saved-comments).

### Update the review summary

```bash
gh api repos/{owner}/{repo}/pulls/<pr-number>/reviews/<numeric-review-id> \
  --method PUT -f body='Updated pending review summary'
```

### Add a pending line-anchored thread

Use this for ordinary comments and suggestions. `startLine`/`startSide` are optional and only for multi-line anchors.

````bash
body=$(cat <<'EOF'
**Functional regression:** concise behavior and impact.

Please retain the required check.

<details>
<summary>Suggested fix</summary>

```suggestion
replacement code
```

</details>
EOF
)

gh api graphql \
  -f query='mutation($review:ID!, $path:String!, $line:Int!, $side:DiffSide!, $body:String!) { addPullRequestReviewThread(input:{pullRequestReviewId:$review,path:$path,line:$line,side:$side,body:$body}) { thread { comments(first:1) { nodes { id fullDatabaseId body pullRequestReview { fullDatabaseId state } } } } } }' \
  -f review='<pending-review-node-id>' \
  -f path='path/to/file.js' \
  -F line=42 \
  -f side='RIGHT' \
  -f body="$body"
````

Multi-line form adds `$startLine:Int!` and `$startSide:DiffSide!` variables and `startLine:$startLine,startSide:$startSide` to the input.

### Update a pending review comment

```bash
gh api graphql \
  -f query='mutation($id:ID!, $body:String!) { updatePullRequestReviewComment(input:{pullRequestReviewCommentId:$id,body:$body}) { pullRequestReviewComment { id fullDatabaseId body } } }' \
  -f id='<comment-node-id>' \
  -f body='Reconciled comment body'
```

### Delete a pending review comment, not the review

Removing a stale comment is an in-place reconciliation. First prove the comment belongs to the preserved current-user `PENDING` review.

```bash
gh api graphql \
  -f query='mutation($id:ID!) { deletePullRequestReviewComment(input:{id:$id}) { clientMutationId } }' \
  -f id='<comment-node-id>'
```

If a node ID is unavailable, a mutation fails, or exact state cannot be verified, stop. Follow [self-review's deletion boundary](SKILL.md#3-save-in-place); do not replace the review.

## Parameters

| Parameter | Meaning |
| --- | --- |
| `body` | Review summary or inline Markdown |
| `comments` | Inline comments included only when creating a review |
| `path` | Repository-relative changed file path |
| `line` / `side` | End line and diff side (`RIGHT` new, `LEFT` old) |
| `startLine` / `startSide` | Optional start of a multi-line diff range |
| `event` | Submission action; omit for a pending draft |
| review numeric ID | REST review identifier |
| review/comment node ID | GraphQL global identifier |

## Comment and suggestion mechanics

Use [team-review's content requirements](../team-review/SKILL.md#2-write-author-facing-findings). Anchor each suggestion to the range it replaces and include only replacement text inside the fence.

## Submit only when explicitly instructed

Only after [explicit submission authorization](SKILL.md#explicit-submission-boundary), submit the existing numeric review ID:

```bash
cat <<'EOF' | gh api repos/{owner}/{repo}/pulls/<pr-number>/reviews/<numeric-review-id>/events --method POST --input -
{"event":"REQUEST_CHANGES","body":"Requesting changes because …"}
EOF
```

Read the review again to verify the submitted state and visibility. Submission is not needed to save suggestions.
