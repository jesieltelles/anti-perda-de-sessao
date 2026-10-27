param(
  [Parameter(Mandatory=$true)][string]$Projeto,
  [Parameter(Mandatory=$true)][ValidateSet('INICIO','FEITO','ACHADO','DECISAO','PARADO','NOTA')][string]$Tipo,
  [Parameter(Mandatory=$true)][string]$Texto
)
# Acrescenta UMA linha ao DIARIO.md do projeto (append-only, nunca sobrescreve) e forca a gravacao em disco.
# Pasta dos projetos: variavel de ambiente ANTI_PERDA_VAULT, ou ~\ObsidianVault\Projetos por padrao.
$base = if ($env:ANTI_PERDA_VAULT) { $env:ANTI_PERDA_VAULT } else { Join-Path $HOME 'ObsidianVault\Projetos' }
$dir = Join-Path $base $Projeto
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force $dir | Out-Null }
$arq = Join-Path $dir 'DIARIO.md'
if (-not (Test-Path $arq)) { [IO.File]::WriteAllText($arq, "# Diario: $Projeto`r`nUma linha por acao, mais nova embaixo. Linha INICIO sem FEITO depois = pode ter sido cortada no meio.`r`n", (New-Object Text.UTF8Encoding($false))) }
$linha = '- {0} [{1}] {2}' -f (Get-Date -Format 'dd/MM HH:mm:ss'), $Tipo, ($Texto -replace "[\r\n]+", ' ')
$fs = [IO.File]::Open($arq, 'Append', 'Write', 'Read')
try {
  $b = (New-Object Text.UTF8Encoding($false)).GetBytes($linha + "`r`n")
  $fs.Write($b, 0, $b.Length)
  $fs.Flush($true)   # $true = descarrega o cache do Windows no disco (sobrevive a queda de luz)
} finally { $fs.Dispose() }
