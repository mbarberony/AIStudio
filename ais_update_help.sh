#!/usr/bin/env bash
# ais_update_help.sh — AIStudio Help Corpus Updater
# Version: 1.0.0
#
# Reads help_manifest.yaml, regenerates stale PDFs, copies to help corpus uploads/
# Usage:
#   ais_update_help              — update all subjects
#   ais_update_help <subject>    — update one subject (e.g. ais_update_help howto)
#   ais_update_help --help       — show this help

VERSION="1.0.0"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="$REPO_ROOT/data/corpora/help/help_manifest.yaml"
UPLOADS_DIR="$REPO_ROOT/data/corpora/help/uploads"
VENV="$REPO_ROOT/.venv/bin/python3"
TODAY=$(date +%Y-%m-%d)

if [[ "$1" == "--help" ]]; then
    echo "ais_update_help v$VERSION"
    echo ""
    echo "Usage:"
    echo "  ais_update_help              Update all help corpus subjects"
    echo "  ais_update_help <subject>    Update one subject (e.g. howto, readme, quickstart)"
    echo "  ais_update_help --help       Show this help"
    echo ""
    echo "What it does:"
    echo "  1. Reads data/corpora/help/help_manifest.yaml"
    echo "  2. For each subject: generates PDF from source .md"
    echo "  3. Copies PDF to data/corpora/help/uploads/"
    echo "  4. Updates last_updated in manifest"
    echo ""
    echo "After running, re-ingest the help corpus:"
    echo "  AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \\"
    echo "    --corpus help --root data/corpora/help/uploads --force"
    exit 0
fi

echo "+============================================================+"
echo "|        AIStudio Help Corpus Updater v$VERSION              |"
echo "+============================================================+"
echo ""

# Check dependencies
if [[ ! -f "$MANIFEST" ]]; then
    echo "❌ Manifest not found: $MANIFEST"
    echo "   Run: cp ~/Downloads/help_manifest.yaml $MANIFEST"
    exit 1
fi

if [[ ! -f "$VENV" ]]; then
    echo "❌ Python venv not found. Run: source $REPO_ROOT/.venv/bin/activate"
    exit 1
fi

# Check weasyprint
if ! "$VENV" -c "import weasyprint" 2>/dev/null; then
    echo "⚠ weasyprint not installed. Installing..."
    "$VENV" -m pip install weasyprint --quiet
fi

# Create uploads dir if needed
mkdir -p "$UPLOADS_DIR"

SUBJECT_FILTER="$1"

# Generate PDF for a single subject
generate_pdf() {
    local subject="$1"
    local source_md="$2"
    local pdf_path="$3"
    local corpus_path="$4"

    local abs_source="$REPO_ROOT/$source_md"
    local abs_pdf="$REPO_ROOT/$pdf_path"
    local pdf_name=$(basename "$pdf_path")

    if [[ ! -f "$abs_source" ]]; then
        echo "  ⚠ Source not found: $source_md — skipping"
        return 1
    fi

    echo "  Generating $pdf_name from $source_md..."

    "$VENV" - <<PYEOF
import markdown, re
from datetime import date
from pathlib import Path
from weasyprint import HTML

today = date.today().strftime("%B %d, %Y")
repo_root = Path("$REPO_ROOT")
source = Path("$abs_source")
output = Path("$abs_pdf")
pdf_name = "$pdf_name"

md_text = source.read_text()

# Strip mermaid blocks
md_text = re.sub(r'\`\`\`mermaid.*?\`\`\`',
    '<div class="mermaid-placeholder"><em>[Architecture diagram]</em></div>',
    md_text, flags=re.DOTALL)
md_text = re.sub(r'\[!\[CI\].*?\]\(.*?\)\n?', '', md_text)

# Fix links: .md → .pdf if exists, broken → plain text
def fix_links(text, repo_root):
    def rewrite(m):
        label, href = m.group(1), m.group(2)
        if href.startswith(('http', 'mailto', '#', 'file://')):
            return m.group(0)
        anchor = ''
        if '#' in href:
            href, anchor = href.split('#', 1)
            anchor = f'#{anchor}'
        pdf_href = href.replace('.md', '.pdf')
        if (repo_root / pdf_href).exists():
            return f'[{label}](file://{repo_root}/{pdf_href}{anchor})'
        if (repo_root / href).exists():
            return f'[{label}](file://{repo_root}/{href}{anchor})'
        return label
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', rewrite, text)

md_text = fix_links(md_text, repo_root)

import markdown as md_lib
md = md_lib.Markdown(extensions=['tables', 'fenced_code', 'toc'])
body = md.convert(md_text)

html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
  @page {{ margin: 2cm 2cm 2.8cm 2cm; @bottom-center {{ content: "{pdf_name}    |    AIStudio    |    {today}"; font-family: Arial, Helvetica, sans-serif; font-size: 9pt; color: #999999; }} }}
  body {{ font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.6; color: #1a1a1a; }}
  h1 {{ font-size: 22pt; color: #1a1a2e; border-bottom: 2px solid #4a90d9; padding-bottom: 6px; margin-top: 24px; }}
  h2 {{ font-size: 16pt; color: #16213e; border-bottom: 1px solid #ddd; padding-bottom: 4px; margin-top: 20px; }}
  h3 {{ font-size: 13pt; color: #333; margin-top: 16px; }}
  p {{ margin: 6px 0; }}
  strong em, em strong {{ color: #4a90d9; font-style: italic; font-weight: bold; }}
  a {{ color: #4a90d9; text-decoration: none; }}
  code {{ background: #f4f4f4; padding: 1px 4px; border-radius: 3px; font-family: 'Courier New', monospace; font-size: 9.5pt; }}
  pre {{ background: #1a1a2e; color: #e0e0e0; padding: 12px 16px; border-radius: 6px; font-size: 9pt; line-height: 1.4; }}
  pre code {{ background: none; color: inherit; padding: 0; }}
  table {{ border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 10pt; }}
  th {{ background: #1a1a2e; color: white; padding: 8px 12px; text-align: left; }}
  td {{ border: 1px solid #ddd; padding: 7px 12px; }}
  tr:nth-child(even) td {{ background: #f9f9f9; }}
  blockquote {{ border-left: 4px solid #4a90d9; margin: 12px 0; padding: 8px 16px; background: #f0f6ff; font-style: italic; }}
  hr {{ border: none; border-top: 1px solid #ddd; margin: 24px 0; }}
  .mermaid-placeholder {{ background: #f0f6ff; border: 1px solid #4a90d9; border-radius: 6px; padding: 12px 16px; color: #555; font-style: italic; margin: 12px 0; }}
  .doc-header {{ text-align: center; margin-bottom: 32px; padding-bottom: 16px; border-bottom: 2px solid #4a90d9; }}
  .logo {{ font-size: 26pt; font-weight: bold; letter-spacing: -1px; font-family: Arial, sans-serif; }}
  .logo-ai {{ color: #1a1a1a; }}
  .logo-studio {{ color: #4a90d9; }}
</style></head>
<body>
<div class="doc-header">
  <div class="logo"><span class="logo-ai">AI</span><span class="logo-studio">Studio</span></div>
</div>
{body}
</body></html>"""

output.parent.mkdir(parents=True, exist_ok=True)
html_path = output.with_suffix('.html')
html_path.write_text(html)
HTML(filename=str(html_path)).write_pdf(str(output))
html_path.unlink()
print(f"✓ {output}")
PYEOF

    if [[ $? -eq 0 ]]; then
        # Copy to corpus uploads
        cp "$abs_pdf" "$UPLOADS_DIR/$(basename "$abs_pdf")"
        echo "  ✓ Copied to $UPLOADS_DIR/$(basename "$abs_pdf")"
        return 0
    else
        echo "  ❌ PDF generation failed for $subject"
        return 1
    fi
}

# Parse manifest and process subjects
GENERATED=0
SKIPPED=0
FAILED=0

# Use python to parse YAML manifest
"$VENV" - <<PYEOF
import yaml, sys, subprocess, os

manifest_path = "$MANIFEST"
subject_filter = "$SUBJECT_FILTER"

with open(manifest_path) as f:
    manifest = yaml.safe_load(f)

subjects = manifest.get('subjects', [])
updated = []

for s in subjects:
    subj = s['subject']
    if subject_filter and subj != subject_filter:
        continue

    print(f"\n── {subj} ──────────────────────────────────")
    result = subprocess.run(
        ['bash', '-c', f'source "$BASH_SOURCE" 2>/dev/null; generate_pdf "{subj}" "{s["source_md"]}" "{s["pdf"]}" "{s["corpus_path"]}"'],
        capture_output=False
    )

    # Call generate_pdf directly via sourced function won't work cleanly in subprocess
    # Instead we'll handle it inline here
    import re
    from pathlib import Path
    from datetime import date

    repo_root = Path("$REPO_ROOT")
    source = repo_root / s['source_md']
    pdf_path = repo_root / s['pdf']
    corpus_dest = Path("$UPLOADS_DIR") / Path(s['pdf']).name
    pdf_name = Path(s['pdf']).name
    today = date.today().strftime("%B %d, %Y")

    if not source.exists():
        print(f"  ⚠ Source not found: {s['source_md']} — skipping")
        continue

    print(f"  Generating {pdf_name} from {s['source_md']}...")

    try:
        import markdown
        from weasyprint import HTML

        md_text = source.read_text()
        md_text = re.sub(r'\`\`\`mermaid.*?\`\`\`',
            '<div class="mermaid-placeholder"><em>[Architecture diagram]</em></div>',
            md_text, flags=re.DOTALL)
        md_text = re.sub(r'\[!\[CI\].*?\]\(.*?\)\n?', '', md_text)

        def fix_links(text):
            def rewrite(m):
                label, href = m.group(1), m.group(2)
                if href.startswith(('http', 'mailto', '#', 'file://')):
                    return m.group(0)
                anchor = ''
                if '#' in href:
                    href, anchor = href.split('#', 1)
                    anchor = f'#{anchor}'
                pdf_href = href.replace('.md', '.pdf')
                if (repo_root / pdf_href).exists():
                    return f'[{label}](file://{repo_root}/{pdf_href}{anchor})'
                if (repo_root / href).exists():
                    return f'[{label}](file://{repo_root}/{href}{anchor})'
                return label
            return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', rewrite, text)

        md_text = fix_links(md_text)

        md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])
        body = md.convert(md_text)

        html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
  @page {{ margin: 2cm 2cm 2.8cm 2cm; @bottom-center {{ content: "{pdf_name}    |    AIStudio    |    {today}"; font-family: Arial, Helvetica, sans-serif; font-size: 9pt; color: #999999; }} }}
  body {{ font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.6; color: #1a1a1a; }}
  h1 {{ font-size: 22pt; color: #1a1a2e; border-bottom: 2px solid #4a90d9; padding-bottom: 6px; margin-top: 24px; }}
  h2 {{ font-size: 16pt; color: #16213e; border-bottom: 1px solid #ddd; padding-bottom: 4px; margin-top: 20px; }}
  h3 {{ font-size: 13pt; color: #333; margin-top: 16px; }}
  p {{ margin: 6px 0; }}
  strong em, em strong {{ color: #4a90d9; font-style: italic; font-weight: bold; }}
  a {{ color: #4a90d9; text-decoration: none; }}
  code {{ background: #f4f4f4; padding: 1px 4px; border-radius: 3px; font-family: 'Courier New', monospace; font-size: 9.5pt; }}
  pre {{ background: #1a1a2e; color: #e0e0e0; padding: 12px 16px; border-radius: 6px; font-size: 9pt; line-height: 1.4; }}
  pre code {{ background: none; color: inherit; padding: 0; }}
  table {{ border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 10pt; }}
  th {{ background: #1a1a2e; color: white; padding: 8px 12px; text-align: left; }}
  td {{ border: 1px solid #ddd; padding: 7px 12px; }}
  tr:nth-child(even) td {{ background: #f9f9f9; }}
  blockquote {{ border-left: 4px solid #4a90d9; margin: 12px 0; padding: 8px 16px; background: #f0f6ff; font-style: italic; }}
  hr {{ border: none; border-top: 1px solid #ddd; margin: 24px 0; }}
  .mermaid-placeholder {{ background: #f0f6ff; border: 1px solid #4a90d9; border-radius: 6px; padding: 12px 16px; color: #555; font-style: italic; margin: 12px 0; }}
  .doc-header {{ text-align: center; margin-bottom: 32px; padding-bottom: 16px; border-bottom: 2px solid #4a90d9; }}
  .logo {{ font-size: 26pt; font-weight: bold; letter-spacing: -1px; font-family: Arial, sans-serif; }}
  .logo-ai {{ color: #1a1a1a; }}
  .logo-studio {{ color: #4a90d9; }}
</style></head>
<body>
<div class="doc-header">
  <div class="logo"><span class="logo-ai">AI</span><span class="logo-studio">Studio</span></div>
</div>
{body}
</body></html>"""

        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        html_tmp = pdf_path.with_suffix('.gen.html')
        html_tmp.write_text(html)
        HTML(filename=str(html_tmp)).write_pdf(str(pdf_path))
        html_tmp.unlink()

        corpus_dest.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy2(str(pdf_path), str(corpus_dest))
        print(f"  ✓ {pdf_name} → {corpus_dest}")
        updated.append(subj)

    except Exception as e:
        print(f"  ❌ Failed: {e}")
        continue

# Update last_updated in manifest
if updated:
    with open(manifest_path) as f:
        raw = f.read()
    for subj in updated:
        # Update last_updated for this subject
        import re as _re
        # Simple approach: find the subject block and update last_updated
        raw = _re.sub(
            rf'(subject: {subj}.*?last_updated: ")[^"]*(")',
            rf'\g<1>{date.today().isoformat()}\g<2>',
            raw, flags=_re.DOTALL
        )
    with open(manifest_path, 'w') as f:
        f.write(raw)
    print(f"\n✓ Manifest updated — {len(updated)} subject(s) refreshed")

print(f"\n── Summary ──────────────────────────────────")
print(f"  Updated: {len(updated)}")
if updated:
    for s in updated:
        print(f"    ✓ {s}")
print(f"\n  Next step — re-ingest help corpus:")
print(f"  AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \\")
print(f"    --corpus help --root data/corpora/help/uploads --force")
PYEOF

