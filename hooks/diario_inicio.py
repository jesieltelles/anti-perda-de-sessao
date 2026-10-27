import glob, json, os, re, sys

# SessionStart: mostra o fim do DIARIO.md do projeto e avisa de INICIO sem FEITO (acao cortada, ex.: queda de luz).
# Pasta dos projetos: variavel de ambiente ANTI_PERDA_VAULT, ou ~/ObsidianVault/Projetos por padrao.
VAULT = os.environ.get("ANTI_PERDA_VAULT") or os.path.join(os.path.expanduser("~"), "ObsidianVault", "Projetos")

def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())

try:
    cwd = json.load(sys.stdin).get("cwd", "")
except Exception:
    cwd = ""

arquivos = glob.glob(os.path.join(VAULT, "*", "DIARIO.md"))
if not arquivos:
    sys.exit(0)

base = norm(os.path.basename(cwd.rstrip("\\/")))
por_nome = [a for a in arquivos if base and base in norm(os.path.basename(os.path.dirname(a)))]
# shortcut: sem casar o nome da pasta, usa o diario mexido mais recentemente; upgrade: mapa pasta->projeto
alvo = (por_nome or [max(arquivos, key=os.path.getmtime)])[0]

with open(alvo, encoding="utf-8") as f:
    linhas = [l.rstrip("\n") for l in f if l.startswith("- ")]

# INICIO sem FEITO depois dele: ainda nao fechado
abertos = []
for i, l in enumerate(linhas):
    if "[INICIO]" in l and not any("[FEITO]" in x for x in linhas[i + 1:]):
        abertos.append(l)

print("DIARIO ANTI-PERDA (%s), ultimas linhas:" % alvo)
print("\n".join(linhas[-25:]))
if abertos:
    print("\nATENCAO: acao INICIO sem FEITO depois (pode ter sido cortada no meio). CONFERIR o estado real antes de refazer:")
    print("\n".join(abertos[-5:]))
print("\nCarregue a skill anti-perda-de-sessao e continue gravando no diario.")
