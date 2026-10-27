# anti-perda-de-sessao

Skill do Claude Code que grava, em tempo real, cada passo da sessão num diário (`DIARIO.md`) dentro de um vault do Obsidian. Se a luz cair, o PC travar ou o limite de uso estourar, a próxima sessão sabe de onde parou e se alguma ação ficou cortada no meio.

## Como funciona

- Antes de uma ação que muda algo fora do arquivo local (deploy, SQL, envio), grava uma linha `INICIO`.
- Depois, grava `FEITO` com o resultado.
- Ao abrir uma sessão, procura `INICIO` sem `FEITO` depois: é ação possivelmente cortada. Confere o estado real antes de refazer.
- O script força a gravação no disco a cada linha.

## Arquivos

- `SKILL.md`: a skill. Copie a pasta para `~/.claude/skills/anti-perda-de-sessao/`.
- `diario.ps1`: acrescenta uma linha ao diário (PowerShell, Windows).
- `hooks/diario_inicio.py`: hook de `SessionStart` que mostra o fim do diário na abertura.

## Instalação

1. Copie `SKILL.md` e `diario.ps1` para `~/.claude/skills/anti-perda-de-sessao/`.
2. Copie `hooks/diario_inicio.py` para `~/.claude/hooks/`.
3. Em `~/.claude/settings.json`, dentro de `hooks.SessionStart`, acrescente:

```json
{ "type": "command", "command": "python \"C:/Users/SEU_USUARIO/.claude/hooks/diario_inicio.py\"", "timeout": 10 }
```

4. Defina a variável de ambiente `ANTI_PERDA_VAULT` com a pasta onde ficam os projetos. Sem ela, o padrão é `~/ObsidianVault/Projetos`.

Numa sessão já aberta, digite `/anti-perda-de-sessao`.
