#!/usr/bin/env bash
# Checagens deste repositório. Sai com 0 só quando o ramo está pronto para revisão.
#
# O gate roda este arquivo a partir da cópia principal, com a pasta de trabalho
# no ramo do job. Regras em AGENTS.md e docs/criterios-de-aceite.md (seção 5).
#
# Cada bloco só roda se o script correspondente já existir, então o arquivo
# serve da issue 01 à 07 sem mudar. Os scripts rodam numa pasta temporária que
# contém só codigo/, config/ e dev.csv: os dados proibidos não existem ali.
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAMO="$PWD"
PERMITIDOS="preparar_sgc.py modelos.py avaliar.py decisao.py sensibilidade.py demo.py test_decisao.py baseline_logreg.py"
# Fora das buscas: o primeiro é o único que pode ler os dados brutos; o segundo
# é herdado e some na issue 01.
ISENTOS="preparar_sgc.py baseline_logreg.py"

falha() { echo "checks: FALHA: $*" >&2; exit 1; }
passo() { echo "checks: $*"; }

# 1. Dados intactos.
passo "hashes dos dados"
# shortcut: shasum é do macOS; em Linux trocar por sha256sum.
(cd dados/processados && shasum -a 256 -c SHA256SUMS >/dev/null) || falha "dados/processados não confere com SHA256SUMS"

# 2. Nada apagado, exceto o script herdado.
if git rev-parse -q --verify origin/main >/dev/null; then
  apagados="$(git diff --diff-filter=D --name-only origin/main...HEAD -- codigo config resultados | grep -vx 'codigo/baseline_logreg.py' || true)"
  [ -z "$apagados" ] || falha "arquivos apagados: $apagados"
fi

# 3. Só os scripts do plano.
passo "arquivos em codigo/"
for f in codigo/*; do
  nome="$(basename "$f")"
  [ "$nome" = "__pycache__" ] && continue
  case " $PERMITIDOS " in *" $nome "*) ;; *) falha "arquivo fora do plano: $f" ;; esac
done

alvos=()
for f in codigo/*.py; do
  case " $ISENTOS " in *" $(basename "$f") "*) ;; *) alvos+=("$f") ;; esac
done

if [ ${#alvos[@]} -gt 0 ]; then
  # 4. Dados proibidos e listagem de pastas. O nome de um arquivo de saída como
  #    predicoes_teste.csv não casa: a busca exige que "teste.csv" não venha depois de "_".
  passo "buscas no código"
  achado="$(grep -nE '(^|[^_a-zA-Z])(teste|sgc)\.csv|dados/brutos|\.asc\b|\bglob\b|listdir|iterdir|scandir|os\.walk' "${alvos[@]}" || true)"
  [ -z "$achado" ] || falha "referência a dado proibido ou listagem de pasta:
$achado"

  # 5. Padrões proibidos.
  achado="$(grep -nE 'fillna|nan_to_num|pickle|joblib|\bclip\(' "${alvos[@]}" || true)"
  [ -z "$achado" ] || falha "padrão proibido:
$achado"
  if [ -f codigo/avaliar.py ]; then
    achado="$(grep -nE 'pgmpy|import modelos|from modelos|\.fit\(' codigo/avaliar.py || true)"
    [ -z "$achado" ] || falha "avaliar.py não pode treinar:
$achado"
  fi

  # 6. Docstring com linha de uso.
  python3 - "${alvos[@]}" <<'PY' || falha "docstring ausente ou sem linha 'Uso:'"
import ast, sys
ruins = [f for f in sys.argv[1:] if "Uso:" not in (ast.get_docstring(ast.parse(open(f).read())) or "")]
print("\n".join(ruins), file=sys.stderr)
sys.exit(1 if ruins else 0)
PY
fi

# 7. Resultados do teste final: ou nenhum, ou exatamente os 6 esperados.
#    Desde 18/11/2026 (teste final rodado pelo autor) eles podem ser commitados.
if compgen -G "resultados/*_teste*" >/dev/null; then
  esperados="calibracao_teste.png diferenca_politicas_teste.csv metricas_teste.csv politicas_teste.csv predicoes_teste.csv resumo_politicas_teste.csv"
  for e in $esperados; do [ -f "resultados/$e" ] || falha "falta resultados/$e (resultados do teste final incompletos)"; done
  for f in resultados/*_teste*; do
    case " $esperados " in *" $(basename "$f") "*) ;; *) falha "sobra $f (não é um dos 6 resultados do teste final)" ;; esac
  done
fi

[ -f codigo/modelos.py ] || { passo "nenhum script do experimento ainda; fim"; exit 0; }

# 8. Ambiente.
passo "ambiente"
uv sync --frozen --quiet
PY="$RAMO/.venv/bin/python"

# 9. Pasta temporária sem os dados proibidos.
S="$(mktemp -d)"
trap 'rm -rf "$S"' EXIT
mkdir -p "$S/dados/processados" "$S/resultados"
cp -R codigo "$S/codigo"
[ -d config ] && cp -R config "$S/config"
cp dados/processados/dev.csv "$S/dados/processados/dev.csv"
find "$S" -name __pycache__ -prune -exec rm -rf {} +
antes="$(cd "$S" && find . -type f -not -path './resultados/*' -not -path '*/__pycache__/*' | sort)"

rodar() { passo "rodando $*"; (cd "$S" && MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 "$PY" "$@") || falha "falhou: $*"; }
tem() { grep -q -- "$1" "codigo/$2" 2>/dev/null; }

# 10. Autotestes e execução do zero, na ordem do plano.
rodar codigo/modelos.py --verificar
rodar codigo/modelos.py
if [ -f codigo/avaliar.py ]; then
  rodar codigo/avaliar.py --verificar
  rodar codigo/avaliar.py
fi
if tem '--ocultar' modelos.py; then
  rodar codigo/modelos.py --ocultar
  tem '--ocultar' avaliar.py && rodar codigo/avaliar.py --ocultar
fi
if tem '--selecao' modelos.py; then
  rodar codigo/modelos.py --selecao
  tem '--selecao' avaliar.py && rodar codigo/avaliar.py --selecao
fi
if [ -f codigo/decisao.py ]; then
  rodar codigo/test_decisao.py
  rodar codigo/decisao.py
fi
if [ -f codigo/sensibilidade.py ]; then
  rodar codigo/sensibilidade.py --verificar
  rodar codigo/sensibilidade.py
fi

# 11. Scripts só gravam em resultados/.
depois="$(cd "$S" && find . -type f -not -path './resultados/*' -not -path '*/__pycache__/*' | sort)"
[ "$antes" = "$depois" ] || falha "arquivo gravado fora de resultados/:
$(diff <(echo "$antes") <(echo "$depois") || true)"

# 12. O que foi gerado é o que está commitado (CSV e JSON byte a byte; PNG só existe).
passo "comparando com resultados/ do ramo"
for f in "$S"/resultados/*; do
  nome="$(basename "$f")"
  [ -f "resultados/$nome" ] || falha "resultados/$nome foi gerado mas não está no ramo"
  case "$nome" in *.csv|*.json) cmp -s "$f" "resultados/$nome" || falha "resultados/$nome difere do que o script gera" ;; esac
done
for f in resultados/*; do
  nome="$(basename "$f")"
  # Só o autor gera os *_teste* (com --final, à mão); a factory não os reproduz.
  case "$nome" in *_teste*) continue ;; esac
  [ -f "$S/resultados/$nome" ] || falha "resultados/$nome está no ramo mas nenhum script o gera"
done

# 13. Formato, consistência, demonstração e caminho do teste final.
passo "verificando saídas"
(cd "$S" && MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 "$PY" "$AQUI/verificar_saidas.py" "$S") || falha "verificar_saidas.py reprovou"

passo "tudo certo"
