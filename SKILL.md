---
name: anti-perda-de-sessao
description: Grava em tempo real, a cada passo, tudo o que a sessão faz num diário (DIARIO.md do projeto), para retomar do ponto exato se acabar a luz, o PC travar, a internet cair ou o limite de uso estourar. Carregar no começo de toda sessão, em todo projeto.
---

# Anti-perda de sessão

O resumo do estado (um BASTAO.md, por exemplo) é sobrescrito e gravado nos marcos. Este é o
**diário linha a linha**: uma linha por ação, gravada na hora, que sobrevive a queda de luz.

## Por que existe

Queda de luz corta a sessão no meio de uma ação. O resumo só diz o que estava pronto, não diz "estava no meio de
publicar X". Sem isso a próxima sessão repete a ação (dobra estoque, reenvia mensagem, recria registro) ou
dá a ação por feita sem ter sido.

## Onde fica

`<pasta dos projetos>\<Nome>\DIARIO.md`. A pasta vem da variável de ambiente `ANTI_PERDA_VAULT`
(padrão: `~\ObsidianVault\Projetos`). Só acrescenta no fim, nunca reescreve.

## Como gravar (um comando, sem pensar)

```powershell
& "$HOME\.claude\skills\anti-perda-de-sessao\diario.ps1" -Projeto 'MeuProjeto' -Tipo INICIO -Texto 'subindo arquivo X para o servidor (md5 ...)'
```

O script cria o arquivo se faltar, acrescenta uma linha com data e hora e força a gravação no disco. Não use
heredoc nem Write para o diário (Write sobrescreve; heredoc come barra invertida).

Tipos: `INICIO`, `FEITO`, `ACHADO`, `DECISAO`, `PARADO`, `NOTA`.

## Quando gravar (obrigatório, sem esperar pedido)

1. **Antes** de toda ação que muda algo fora do arquivo local ou que não se desfaz com facilidade: deploy, upload,
   UPDATE/DELETE/INSERT, cron, migration, envio de mensagem ou e-mail, publicação, ação em sistema externo, comando
   que roda em segundo plano. Linha `INICIO` com o que vai fazer, o alvo e o identificador (arquivo, md5, id, hash).
2. **Logo depois**, linha `FEITO` com o resultado e a conferência (HTTP, contagem, md5). Se falhou, `FEITO` com o erro.
3. `ACHADO` quando descobrir algo relevante (causa, risco, número). `DECISAO` quando o dono decidir ou autorizar,
   com as palavras dele. `PARADO` quando uma frente parar e por quê.
4. Edição normal de arquivo local com backup não precisa de INICIO/FEITO; vale uma linha `FEITO` por entrega.
5. Comando de fundo (fila, import, loop de espera): gravar o id da tarefa e o arquivo de log para achar depois.

Nunca gravar senha, token, chave ou linha de `.env`. Escrever "trocado em <data>" no lugar.

## No começo da sessão

1. Ler o resumo do projeto e as **últimas 40 linhas** do `DIARIO.md`.
2. Procurar `INICIO` sem `FEITO` correspondente depois dele: é ação **possivelmente cortada no meio**.
3. Para cada uma: **conferir o estado real** (ler o servidor, o banco, o md5, a API) antes de refazer ou de
   dar por feita. Nunca repetir cegamente. Dizer ao dono em uma frase: "A sessão anterior parou no meio de X;
   conferi e Y".
4. Se nada ficou pendente, dizer só de onde retoma.

## Manutenção

- Quando o `DIARIO.md` passar de umas 400 linhas, mover as mais antigas para `DIARIO_<aaaamm>.md` na mesma pasta
  (copiar primeiro, conferir, só então cortar). O diário nunca é apagado.
- O que for decisão ou lição duradoura vai também para o resumo do projeto.

## Regra de ouro

Gravar custa 1 segundo. Refazer ação cortada custa estoque dobrado ou mensagem repetida ao cliente. Na dúvida, grave.
