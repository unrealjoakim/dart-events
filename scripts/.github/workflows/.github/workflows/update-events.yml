name: Update Swedish Dart Events

on:
  schedule:
    - cron: "0 3 * * *"   # kör varje natt kl 03:00
  workflow_dispatch:       # så du kan köra manuellt

jobs:
  update:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repo
      uses: actions/checkout@v3

    - name: Install Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"

    - name: Install dependencies
      run: pip install requests beautifulsoup4

    - name: Run update script
      run: python scripts/update_events.py

    - name: Commit and push changes
      run: |
        git config --global user.name "DartBot"
        git config --global user.email "bot@dart.se"
        git add Dart-event.json
        git commit -m "Auto-update Swedish dart events"
        git push
