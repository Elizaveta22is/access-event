import os

files = {}

files[".github/workflows/day5-check.yml"] = '''name: Day5 Check
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install deps
        run: pip install -r requirements.txt pytest
      - name: Check tests exist
        run: |
          test -f tests/test_models.py
          test -f tests/test_api.py
      - name: Check docs exist
        run: |
          test -f docs/test_cases.md
          test -f docs/bug_reports.md
          test -f docs/user_manual.md
          test -f docs/admin_manual.md
          test -f docs/api.md
          test -f docs/assessment.md
      - name: Run tests
        run: pytest -v
'''

files[".github/workflows/docker-publish.yml"] = '''name: Build and Publish Docker Image
on:
  push:
    branches: [main]
permissions:
  packages: write
  contents: read
jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository_owner }}/accessevent:latest
'''

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("OK: " + path)

print("")
print("Готово - YAML-файлы перезаписаны.")
