"""angalia_faili.py - Kagua kama kila faili la .py linaloitwa na 'import' lipo kwenye git.

Matumizi (ndani ya folda ya repo, kwenye terminal):
    python angalia_faili.py
"""
import ast
import importlib.util
import pathlib
import subprocess
import sys

folda = pathlib.Path(".")
local = {p.stem: p.name for p in folda.glob("*.py")}
git = subprocess.run(["git", "ls-files"], capture_output=True, text=True)
tracked = set(git.stdout.split())
if git.returncode != 0:
    sys.exit("Hii si folda ya git, au git haijasakinishwa.")

matatizo = set()
for faili in local.values():
    try:
        mti = ast.parse(pathlib.Path(faili).read_text(encoding="utf-8"))
    except SyntaxError as e:
        matatizo.add(f"{faili}: kosa la sintaksia mstari {e.lineno}")
        continue
    for n in ast.walk(mti):
        if isinstance(n, ast.Import):
            majina = [a.name.split(".")[0] for a in n.names]
        elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module:
            majina = [n.module.split(".")[0]]
        else:
            continue
        for m in majina:
            if m in local and local[m] not in tracked:
                matatizo.add(f"{faili} -> {local[m]} lipo kwenye kompyuta lakini HALIJAINGIA git (git add + commit + push)")
            elif m not in local and m not in sys.stdlib_module_names and importlib.util.find_spec(m) is None:
                matatizo.add(f"{faili} -> '{m}' haipo kwenye folda wala kwenye pip (faili halipo, au ni pakiti ya requirements.txt)")

print("\n".join(sorted(matatizo)) if matatizo else "Hakuna tatizo la imports lililoonekana.")
