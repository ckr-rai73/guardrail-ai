import re
import os
from pathlib import Path

FILES = [
    "backend/app/agents/shadow_model.py",
    "backend/app/reporting/board_report.py",
    "backend/app/learning/continuous_learning_pipeline.py",
    "backend/adversarial_test_latency_5000ms.py",
    "backend/adversarial_test_multi_region_500.py",
    "backend/adversarial_test_multi_region.py",
    "backend/adversarial_test_asi06_recursive.py",
    "backend/adversarial_test_at_scale.py",
]

def migrate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace import
    content = re.sub(
        r'import google\.generativeai\s+as\s+genai',
        'import google.genai as genai',
        content
    )

    # 2. Replace genai.configure(...) with client creation
    #    We'll insert a client creation line right after the import block.
    #    First, remove any existing configure line.
    content = re.sub(
        r'genai\.configure\([^)]*\)',
        '',  # remove it
        content
    )

    # 3. Add client = genai.Client() at the top (after imports)
    #    We'll look for the last import line and insert after it.
    lines = content.splitlines()
    new_lines = []
    inserted_client = False
    for line in lines:
        new_lines.append(line)
        # If we haven't inserted client yet and this line is an import line (or after imports)
        # Simple heuristic: after any import and not a comment/blank line
        if not inserted_client and line.startswith('import ') or line.startswith('from '):
            # We'll insert after a blank line following imports, but for simplicity
            pass  # we'll do a separate pass

    # Simpler: add client creation right after the import block
    # We'll find the end of imports by locating the first non-import line
    import_end = 0
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            import_end = i
        else:
            break
    # Insert after import_end
    lines.insert(import_end + 1, 'client = genai.Client()  # uses GOOGLE_API_KEY env var')
    content = '\n'.join(lines)

    # 4. Replace genai.GenerativeModel(...) with a constant model name
    #    We'll capture the model name and store it as MODEL_NAME.
    #    Then remove the model instantiation line.
    model_pattern = r'(\w+)\s*=\s*genai\.GenerativeModel\([\'"]([^\'"]+)[\'"]\)'
    model_matches = list(re.finditer(model_pattern, content))
    if model_matches:
        # Assume the last one is the primary model
        var_name, model_name = model_matches[-1].groups()
        # Replace the line with MODEL_NAME constant
        content = re.sub(
            model_pattern,
            f'MODEL_NAME = "models/{model_name}"',  # add prefix
            content,
            count=1  # replace only the last one? We'll replace all occurrences of model instantiation
        )
        # Also replace any remaining occurrences of the same variable with client calls
        # We'll replace `var_name.generate_content(` with client call
        content = re.sub(
            rf'{var_name}\.generate_content\(([^)]+)\)',
            f'client.models.generate_content(model=MODEL_NAME, contents=\\1)',
            content
        )
        # Similarly for count_tokens, start_chat, etc.
        content = re.sub(
            rf'{var_name}\.count_tokens\(([^)]+)\)',
            f'client.models.count_tokens(model=MODEL_NAME, contents=\\1)',
            content
        )
        # start_chat is more complex; maybe leave for manual

    # 5. If any standalone genai calls (like genai.embed_content), replace
    content = re.sub(
        r'genai\.embed_content\(([^)]+)\)',
        r'client.models.embed_content(\1)',
        content
    )

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Migrated: {filepath}")

if __name__ == "__main__":
    for f in FILES:
        if Path(f).exists():
            migrate_file(f)
        else:
            print(f"File not found: {f}")
