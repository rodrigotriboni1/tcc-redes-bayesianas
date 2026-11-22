// Gera o deck da defesa a partir de monografia/roteiro-defesa.md e dos CSVs de resultados/ (só leitura).
// Uso: NODE_PATH=$HOME/.local/node_modules node build.js
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const REPO = path.join(__dirname, "..", "..");
const OUT = path.join(__dirname, "Defesa_TCC_Rodrigo_rascunho.pptx");
const RES = (f) => path.join(REPO, "resultados", f);
const ROT = fs.readFileSync(path.join(REPO, "monografia/roteiro-defesa.md"), "utf8");

const C = { navy: "1F4E79", azul: "2E75B6", alerta: "C00000", corpo: "2D2D2D", cinza: "777777", amarelo: "FFF2CC", branco: "FFFFFF" };
const F = "Arial";
const W = 13.333, M = 0.5, UW = 12.333;
const erros = [];
const relat = { palavras: {}, sowhat: {} };

// ---------- dados ----------
function csv(f, key) {
  const [h, ...ls] = fs.readFileSync(RES(f), "utf8").trim().split("\n");
  const cols = h.split(",");
  const out = {};
  for (const l of ls) {
    const v = l.split(","), o = {};
    cols.forEach((c, i) => (o[c] = isNaN(+v[i]) || v[i] === "" ? v[i] : +v[i]));
    out[key(o)] = o;
  }
  return out;
}
const dev = csv("metricas_dev.csv", (o) => o.modelo);
const tst = csv("metricas_teste.csv", (o) => o.modelo);
const dif = csv("diferenca_politicas_teste.csv", (o) => o.modelo);
const res = csv("resumo_politicas_teste.csv", (o) => o.modelo + "/" + o.regra);
const sen = csv("sensibilidade.csv", (o) => o.perda + "/" + o.custo_analise);
const sel = csv("selecao_dev.csv", (o) => o.modelo);
const esc = csv("selecao_escolha.csv", (o) => o.fold_externo + "/" + o.config);
const U = JSON.parse(fs.readFileSync(path.join(REPO, "config/utilidade.json"), "utf8")).acoes;
const G = U.aprovar.bom, L = -U.aprovar.ruim, cA = G - U.analise_manual.bom;
if (-U.analise_manual.ruim !== cA) erros.push("matriz: custo da análise inconsistente");
const lim = [cA / L, 1 - cA / G];
const fmt = (x, d) => x.toFixed(d).replace(".", ",");
const escolhidas = Object.values(esc).filter((o) => o.escolhida === "True").map((o) => o.config);
if (escolhidas.length !== 6 || escolhidas.some((c) => c !== "nb_ess50")) erros.push("selecao_escolha: nb_ess50 não é a escolhida em todas");

// Texto tem de existir literalmente no roteiro; devolve sem marcação Markdown.
function R(s) {
  if (!ROT.includes(s)) erros.push("texto não encontrado no roteiro: " + s.slice(0, 70));
  return s.replace(/\*\*/g, "").replace(/\*/g, "").replace(/`/g, "");
}
// Cada número exibido tem de bater com o CSV (formatado como no roteiro).
function chk(onde, texto, pares) {
  for (const [v, d] of pares) if (!texto.includes(fmt(v, d))) erros.push(`${onde}: CSV dá ${fmt(v, d)}, roteiro diverge`);
}

// ---------- medida de texto ----------
const cpl = (pt, w, bold) => Math.floor(w / ((pt / 72) * (bold ? 0.52 : 0.5)));
function linhas(par, n) {
  let k = 1, cur = 0;
  for (const wd of par.split(/\s+/).filter(Boolean)) {
    if (cur === 0) cur = wd.length;
    else if (cur + 1 + wd.length <= n) cur += 1 + wd.length;
    else { k++; cur = wd.length; }
  }
  return k;
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "Defesa de TCC";
let nSlide = 0;
const slides = [];

// Caixa de texto com verificação de capacidade. paras: string ou array de strings.
function T(s, paras, o) {
  paras = Array.isArray(paras) ? paras : [paras];
  const pt = o.pt, ins = o.fill ? 0.1 : 0;
  const wIn = o.w - 2 * ins - (o.bullet ? 0.35 : 0), hIn = o.h - 2 * ins;
  const n = cpl(pt, wIn, o.bold);
  const avail = Math.floor(hIn / ((pt * 1.2) / 72) + 1e-9);
  const used = paras.reduce((a, p) => a + linhas(p, n), 0) + (o.gap ? (paras.length - 1) * 0.5 : 0);
  const chars = paras.reduce((a, p) => a + p.length, 0);
  const onde = `slide ${nSlide} [${paras[0].slice(0, 40)}]`;
  if (o.kind === "title") {
    if (used > 2) erros.push(`${onde}: título com ${used} linhas estimadas`);
    if (chars > 150) erros.push(`${onde}: título com ${chars} caracteres`);
  } else if (used > avail || chars > 0.9 * avail * n) erros.push(`${onde}: excede 90% da caixa (${used}/${avail} linhas, ${chars}/${avail * n} car.)`);
  if (o.x < M - 1e-9 || o.y < 0.3 || o.x + o.w > W - M + 1e-9 || o.y + o.h > 7.5 - 0.2) erros.push(`${onde}: fora das margens`);
  if (o.kind === "body") s._palavras += paras.join(" ").split(/\s+/).filter(Boolean).length;
  const runs = paras.map((p, i) => ({
    text: p,
    options: { breakLine: i < paras.length - 1, bullet: o.bullet ? { indent: 22 } : false, paraSpaceAfter: o.gap ? 6 : 0 },
  }));
  s.addText(runs, {
    x: o.x, y: o.y, w: o.w, h: o.h, fontFace: F, fontSize: pt, bold: !!o.bold, italic: !!o.italic,
    color: o.color || C.corpo, align: o.align || "left", valign: o.valign || "top",
    margin: o.fill ? 7 : 0, fill: o.fill ? { color: o.fill } : undefined,
    line: o.line ? { color: o.line, width: 1.5 } : undefined, fit: "none",
  });
}
const placeholder = (s, txt, x, y, w) => T(s, txt, { x, y, w, h: 0.55, pt: 20, fill: C.amarelo, line: "BF9000", color: C.corpo, kind: "ph" });

function novo({ titulo, notas, escuro, sowhat }) {
  nSlide++;
  const s = pres.addSlide();
  s._palavras = 0;
  s.background = { color: escuro ? C.navy : C.branco };
  const rod = escuro ? "BDD7EE" : C.cinza;
  s.addText("UFU · Engenharia de Controle e Automação", { x: M, y: 7.0, w: 6, h: 0.3, fontFace: F, fontSize: 12, color: rod, margin: 0 });
  s.addText(String(nSlide), { x: W - M - 1, y: 7.0, w: 1, h: 0.3, fontFace: F, fontSize: 12, color: rod, align: "right", margin: 0 });
  if (titulo) T(s, titulo, { x: M, y: 0.4, w: UW, h: 1.0, pt: 24, bold: true, color: escuro ? C.branco : C.navy, kind: "title" });
  s._notas = notas || "";
  s._sowhat = sowhat;
  s._n = nSlide;
  slides.push(s);
  return s;
}
// "So what" vai no slide se couber no limite de palavras; senão, abre as notas.
function fechar(s, corpo, area) {
  if (s._sowhat) {
    const n = s._sowhat.split(/\s+/).length;
    if (corpo && s._palavras + n <= 45 && area) {
      T(s, s._sowhat, { ...area, pt: 20, italic: true, color: C.azul, kind: "body" });
      relat.sowhat[s._n] = "slide";
    } else {
      s._notas = "Mensagem do slide: " + s._sowhat + "\n\n" + s._notas;
      relat.sowhat[s._n] = "notas";
    }
  }
  if (corpo) { relat.palavras[s._n] = s._palavras; if (s._palavras > 45) erros.push(`slide ${s._n}: ${s._palavras} palavras`); }
  if (s._notas) s.addNotes(s._notas);
}
const cite = (s, txt, y = 6.55) => T(s, txt, { x: M, y, w: UW, h: 0.3, pt: 12, color: C.cinza, kind: "cite" });

function img(s, f, a) {
  const b = fs.readFileSync(RES(f));
  const pw = b.readUInt32BE(16), ph = b.readUInt32BE(20);
  const k = Math.min(a.w / pw, a.h / ph), w = pw * k, h = ph * k;
  s.addImage({ path: RES(f), x: a.x + (a.w - w) / 2, y: a.y + (a.h - h) / 2, w, h });
}

// Intervalos (IC ou ±desvio) como barras horizontais empilhadas: base invisível + trecho visível.
function faixas(s, cats, lo, hi, dest, a, eixo) {
  const z = (f) => cats.map((_, i) => (f(i) ? hi[i] - lo[i] : 0));
  s.addChart(pres.charts.BAR, [
    { name: "base", labels: cats, values: lo },
    { name: "destaque", labels: cats, values: z((i) => dest[i]) },
    { name: "demais", labels: cats, values: z((i) => !dest[i]) },
  ], {
    ...a, barDir: "bar", barGrouping: "stacked", barGapWidthPct: 70, chartColors: [C.branco, C.azul, C.navy],
    showLegend: false, catAxisOrientation: "maxMin", valGridLine: { style: "none" }, catGridLine: { style: "none" },
    valAxisMinVal: eixo.min, valAxisMaxVal: eixo.max, valAxisMajorUnit: eixo.passo, valAxisLabelFormatCode: eixo.fmt || "0.00",
    catAxisLabelFontSize: 14, valAxisLabelFontSize: 14, catAxisLabelFontFace: F, valAxisLabelFontFace: F,
    showValAxisTitle: true, valAxisTitle: eixo.titulo, valAxisTitleFontSize: 14, valAxisTitleColor: C.corpo,
  });
}

function retasUE(s, a, destaqueAnalise) {
  const ps = Array.from({ length: 21 }, (_, i) => i / 20);
  const lab = ps.map((p) => fmt(p, 2));
  const ue = (u) => ps.map((p) => (1 - p) * u.bom + p * u.ruim);
  s.addChart(pres.charts.LINE, [
    { name: "Aprovar", labels: lab, values: ue(U.aprovar) },
    { name: "Rejeitar", labels: lab, values: ue(U.rejeitar) },
    { name: "Análise manual", labels: lab, values: ue(U.analise_manual) },
  ], {
    ...a, lineSize: 3, lineDataSymbol: "none",
    chartColors: destaqueAnalise ? ["BFBFBF", "BFBFBF", C.azul] : [C.navy, C.cinza, C.azul],
    showLegend: true, legendPos: "b", legendFontSize: 14, legendFontFace: F,
    catAxisLabelFrequency: 4, catAxisLabelFontSize: 14, valAxisLabelFontSize: 14, catAxisLabelFontFace: F, valAxisLabelFontFace: F,
    valAxisMinVal: -400, valAxisMaxVal: 100, valAxisMajorUnit: 100,
    showCatAxisTitle: true, catAxisTitle: "P(ruim)", showValAxisTitle: true, valAxisTitle: "utilidade esperada",
    catAxisTitleFontSize: 14, valAxisTitleFontSize: 14, valGridLine: { color: "E5E5E5", size: 0.5 },
  });
}

const ESQ = { x: M, y: 1.6, w: 7.2, h: 4.8 };          // área do exibidor
const DIR = { x: 8.0, y: 1.6, w: W - M - 8.0 };       // coluna de texto

// =================== CORPO ===================
// 1 — Título
{
  const s = novo({ escuro: true, notas: R("Bom dia. Sou Rodrigo Mialichi Triboni, orientado pelo professor Fabio Vincenzi. Este trabalho separa duas tarefas que a decisão de crédito costuma misturar: estimar o risco e escolher a ação. Vou mostrar que essa separação deixa os limiares explícitos, e qual efeito ela teve num conjunto de teste, com as ressalvas que acompanham esse número.") });
  T(s, R("Redes bayesianas e utilidade esperada aplicadas à seleção de *next best action* em sistemas automatizados de decisão"), { x: M, y: 1.0, w: UW, h: 1.1, pt: 28, bold: true, color: C.branco, kind: "title" });
  T(s, R("Separar o risco da ação torna os limiares explícitos; o efeito medido vem com ressalvas"), { x: M, y: 2.35, w: UW, h: 0.9, pt: 24, color: "BDD7EE", kind: "sub" });
  T(s, ["Rodrigo Mialichi Triboni", "Orientador: Fabio Vincenzi", "Universidade Federal de Uberlândia (UFU) · Faculdade de Engenharia Elétrica (FEELT) · Engenharia de Controle e Automação"], { x: M, y: 3.6, w: UW, h: 1.6, pt: 20, color: C.branco, kind: "meta" });
  placeholder(s, "[titulação do orientador]", M, 5.35, 6.0);
  placeholder(s, "[data e local da defesa]", 6.8, 5.35, 6.03);
  fechar(s, false);
}

// 2 — Problema
{
  const s = novo({
    titulo: R("Na regra de escore com ponto de corte, estimar o risco e escolher a ação ficam fundidos, e os custos ficam implícitos"),
    sowhat: R("o problema é de arquitetura da decisão, não de acurácia."),
    notas: R("Na concessão de crédito, um modelo dá um escore e o escore é comparado com um corte; é a prática descrita por Thomas e por Siddiqi. Nessa regra, duas coisas diferentes viram uma: a probabilidade de o crédito ser ruim e a escolha do que fazer. O corte carrega os custos de errar, mas não os mostra. Redes bayesianas, no sentido de Pearl, servem para a primeira tarefa; para a segunda, uso a utilidade esperada. O trabalho testa essa separação num estudo de caso."),
  });
  const bx = (t, x, y, w, h, cor) => T(s, t, { x, y, w, h, pt: 20, fill: C.branco, line: cor || C.navy, color: C.corpo, align: "center", valign: "middle", kind: "body" });
  T(s, "Hoje", { x: M, y: 1.6, w: 7.2, h: 0.4, pt: 20, bold: true, color: C.navy, kind: "body" });
  bx("caso → escore → corte → aprovar/rejeitar", M, 2.05, 7.2, 0.75);
  T(s, "Proposta", { x: M, y: 3.1, w: 7.2, h: 0.4, pt: 20, bold: true, color: C.navy, kind: "body" });
  bx("camada de risco: P(ruim)", M, 3.55, 2.6, 1.25);
  s.addShape(pres.shapes.RIGHT_ARROW, { x: 3.15, y: 3.95, w: 0.6, h: 0.45, fill: { color: C.azul }, line: { color: C.azul } });
  bx("camada de decisão: custos", 3.8, 3.55, 2.6, 1.25, C.azul);
  s.addShape(pres.shapes.RIGHT_ARROW, { x: 6.45, y: 4.05, w: 0.4, h: 0.3, fill: { color: C.navy }, line: { color: C.navy } });
  T(s, "ação", { x: 6.9, y: 3.95, w: 0.8, h: 0.45, pt: 20, color: C.corpo, kind: "body" });
  T(s, R("Escore + corte: prática da indústria, interpretável. / Custos não aparecem na regra. / Proposta: risco por rede bayesiana; ação por utilidade esperada.").split(" / "), { ...DIR, h: 3.4, pt: 20, bullet: true, gap: true, kind: "body" });
  cite(s, R("(THOMAS, 2000; SIDDIQI, 2006; PEARL, 1988)"));
  fechar(s, true, { x: DIR.x, y: 5.15, w: DIR.w, h: 1.1 });
}

// 3 — Pergunta
{
  const s = novo({
    titulo: R("A pergunta tem duas partes: uma propriedade da política e um efeito medido contra o corte 0,5"),
    sowhat: R("a banca sabe o que cada resultado responde."),
    notas: R("Esta é a pergunta, como está no plano e no capítulo 1. A parte 1 é uma propriedade da política: vale para qualquer escore de probabilidade, inclusive a regressão logística, e não depende do experimento. A parte 2 é o que medi: ações e utilidade média, contra um corte fixo de 0,5. A pergunta e a forma de ler cada desfecho foram escritas no plano de 15/11, antes dos resultados; duas decisões complementares vieram em 18/11, depois da abertura do teste, e o estudo de seleção foi desenhado depois de ver o desenvolvimento [docs/plano-de-analise.md §1]."),
  });
  // A pergunta é o exibidor (citação literal do plano); não entra na contagem de palavras do corpo.
  T(s, R("Uma política que separa a estimativa do risco (rede bayesiana, com calibração medida) da escolha da ação (utilidade esperada) tem (1) limiares explícitos, que qualquer pessoa reproduz a partir da matriz de utilidade e de `p`, e (2) que efeito medido sobre as ações e a utilidade média, em comparação com um limiar fixo de 0,5?"),
    { x: M, y: 1.6, w: UW, h: 2.35, pt: 20, fill: "EAF1FB", line: C.azul, color: C.corpo, kind: "quote" });
  T(s, R("(1) vale por construção, para qualquer escore. (2) é o que o experimento mede. Leitura definida no plano de análise.").split(/(?<=\.) (?=\()|(?<=mede\.) /), { x: M, y: 4.2, w: UW, h: 1.4, pt: 20, bullet: true, kind: "body" });
  fechar(s, true, { x: M, y: 5.75, w: UW, h: 0.45 });
}

// 4 — Dados e protocolo
{
  const s = novo({
    titulo: R("1.000 casos da South German Credit: 800 para desenvolver em 5 partições e 200 de teste, abertos uma única vez"),
    sowhat: R("o teste não influenciou nenhuma escolha."),
    notas: R("A base é a South German Credit, a versão corrigida por Grömping da base alemã citada na proposta. São 1.000 casos; separei 800 para desenvolvimento, com 240 ruins, e 200 para teste, com 60 ruins [resultados/predicoes_teste.csv, kredit: 60 zeros em 200 linhas]. No desenvolvimento usei validação cruzada estratificada em 5 partições, semente 2026. As três variáveis contínuas viram três faixas por tercis, com cortes aprendidos só no treino; no teste, os cortes vêm do desenvolvimento inteiro [resultados/cortes.json]. O teste foi aberto uma única vez, em 17/11/2026, depois do *commit* de congelamento."),
  });
  const k = UW / 1000;
  for (let i = 0; i < 5; i++) T(s, "P" + (i + 1), { x: M + i * 160 * k, y: 1.65, w: 160 * k - 0.04, h: 0.7, pt: 20, fill: C.navy, color: C.branco, align: "center", valign: "middle", kind: "body" });
  T(s, "Teste", { x: M + 800 * k + 0.1, y: 1.65, w: 200 * k - 0.1, h: 0.7, pt: 20, fill: C.branco, line: C.azul, color: C.azul, bold: true, align: "center", valign: "middle", kind: "body" });
  T(s, "Dev: 800 (240 ruins)", { x: M, y: 2.45, w: 800 * k, h: 0.4, pt: 20, color: C.navy, kind: "body" });
  T(s, "Teste: 200 (60 ruins), aberto 1× em 17/11/2026 (49d77ff)", { x: M, y: 2.9, w: UW, h: 0.45, align: "right", pt: 20, color: C.azul, kind: "body" });
  T(s, R("Divisão estratificada, semente 2026. / Validação cruzada estratificada, 5 partições. / 3 contínuas em 3 faixas por tercis, cortes só no treino. / Classe positiva: ruim (30%).").split(" / "), { x: M, y: 3.6, w: 9.0, h: 2.1, pt: 20, bullet: true, kind: "body" });
  chk("slide 4", "30%", [[tst.taxa_base.pr_auc * 100, 0]]);
  cite(s, R("(GRÖMPING, 2019)"));
  fechar(s, true, { x: M, y: 5.85, w: UW, h: 0.45 });
}

// 5 — Modelos
{
  const s = novo({
    titulo: R("Três modelos estimam P(ruim): Naive Bayes e TAN com prior BDeu 5, e a regressão logística como referência"),
    sowhat: R("modelo e representação variam juntos; a comparação entre famílias não isola o modelo."),
    notas: R("Comparo três modelos. O Naive Bayes trata as preditoras como independentes dada a classe; o TAN, de Friedman e colegas, acrescenta uma árvore de dependências entre elas. Os parâmetros das redes usam prior BDeu com tamanho equivalente 5, como em Heckerman, para evitar probabilidade zero. A regressão logística é a referência e recebe as contínuas sem discretizar; por isso a diferença entre redes e logística mistura modelo e representação. A calibração é só medida: corrigir exigiria escolher o método depois de ver as métricas."),
  });
  const grafo = (x0, tan) => {
    const cx = x0 + 1.15, top = 1.7, kids = [x0 + 0.1, x0 + 0.65, x0 + 1.2, x0 + 1.75];
    s.addShape(pres.shapes.OVAL, { x: cx - 0.3, y: top, w: 0.6, h: 0.45, fill: { color: C.navy }, line: { color: C.navy } });
    kids.forEach((kx, i) => {
      s.addShape(pres.shapes.LINE, { x: Math.min(cx, kx + 0.2), y: top + 0.45, w: Math.abs(kx + 0.2 - cx) || 0.001, h: 0.85, line: { color: C.cinza, width: 1.25 }, flipH: kx + 0.2 < cx });
      const v = tan && i === 1;
      s.addShape(pres.shapes.OVAL, { x: kx, y: top + 1.3, w: 0.4, h: 0.4, fill: { color: v ? C.azul : C.branco }, line: { color: v ? C.azul : C.navy, width: 1.25 } });
      if (tan && i < 3) s.addShape(pres.shapes.LINE, { x: kx + 0.4, y: top + 1.5, w: 0.15, h: 0, line: { color: C.azul, width: 2 } });
    });
  };
  grafo(M, false);
  grafo(M + 2.45, true);
  T(s, ["sem grafo", "contínuas originais"], { x: M + 4.9, y: 1.8, w: 2.3, h: 1.35, pt: 20, fill: C.branco, line: C.navy, align: "center", valign: "middle", kind: "body" });
  const leg = [["NB: kredit pai de todas"], ["TAN: + árvore entre preditoras; azul: verw"], ["Regressão logística"]];
  leg.forEach((t, i) => T(s, t, { x: M + i * 2.45, y: 3.6, w: 2.3, h: 1.4, pt: 20, color: C.navy, kind: "body" }));
  T(s, R("Parâmetros: prior BDeu, tamanho equivalente 5. / Inferência exata (pgmpy 1.1.2). / Logística: `max_iter=1000`. / Calibração só medida, não corrigida.").split(" / "), { ...DIR, h: 3.4, pt: 20, bullet: true, gap: true, kind: "body" });
  cite(s, R("(FRIEDMAN; GEIGER; GOLDSZMIDT, 1997; HECKERMAN; GEIGER; CHICKERING, 1995; ANKAN; TEXTOR, 2024; PEDREGOSA et al., 2011)"));
  fechar(s, true, { x: M, y: 5.2, w: 7.2, h: 1.1 });
}

// 6 — Utilidade esperada
{
  const t = R("Com a matriz demonstrativa, a utilidade esperada vira dois limiares: aprovar abaixo de 0,10, análise manual até 0,60, rejeitar acima");
  chk("slide 6", t, [[lim[0], 2], [lim[1], 2]]);
  const s = novo({
    titulo: t,
    sowhat: R("responde à parte 1: qualquer pessoa reproduz as fronteiras a partir da matriz e de *p*."),
    notas: R("A camada de decisão escolhe a ação de maior utilidade esperada. A matriz é demonstrativa: aprovar um bom vale 100, aprovar um ruim custa 400, rejeitar vale zero, e a análise manual custa c = 40 [config/utilidade.json]. Como cada utilidade esperada é uma reta em p, a escolha vira limiares, como Elkan mostra: análise manual entre c/400 e 1 − c/100, ou seja, de 0,10 a 0,60. Isso responde à primeira parte da pergunta, por construção, para qualquer escore. A contribuição não é uma regra nova, é derivar os limiares dos custos de forma explícita."),
  });
  retasUE(s, { x: M, y: 1.55, w: 7.2, h: 4.2 }, false);
  const lt = "Limiares: 0,10 (c/L = 40/400) e 0,60 (1 − c/G = 1 − 40/100)";
  chk("slide 6 limiares", lt, [[lim[0], 2], [lim[1], 2], [cA, 0], [L, 0], [G, 0]]);
  if (Math.abs(sen["400/40"].limiar_inferior - lim[0]) > 1e-9 || Math.abs(sen["400/40"].limiar_superior - lim[1]) > 1e-9) erros.push("slide 6: limiares ≠ sensibilidade.csv 400/40");
  T(s, lt, { x: M, y: 5.8, w: 7.2, h: 0.7, pt: 20, color: C.azul, kind: "body" });
  const body = R("UE(a) = (1−p)·U(a,bom) + p·U(a,ruim). / Matriz: G = 100, L = 400, c = 40. / Demonstrativa, aprovada pelo orientador, não calibrada com dados reais.");
  chk("slide 6", body, [[G, 0], [L, 0], [cA, 0]]);
  T(s, body.split(" / "), { ...DIR, h: 3.6, pt: 20, bullet: true, gap: true, kind: "body" });
  cite(s, R("(ELKAN, 2001)"));
  fechar(s, true, { x: DIR.x, y: 5.3, w: DIR.w, h: 1.1 });
}

// 7 — Sensibilidade
{
  const s = novo({
    titulo: R("Os limiares se movem com a perda e o custo da análise; com custo alto, a análise manual desaparece"),
    sowhat: R("a política mostra para onde vai com outros custos; a escolha do custo é do negócio, não do trabalho."),
    notas: R("Variei a perda por inadimplência em 200, 400, 600 e 800 e o custo da análise de 0 a 100, de 5 em 5 [resultados/sensibilidade.csv, 84 linhas]. Com custo zero, a análise manual cobre todo o intervalo [sensibilidade.csv, linha 400/0: 0,000 e 1,000]. Quando os dois limiares coincidem a faixa some: com perda 200 a partir de c = 70, ambos 0,333; com perda 400 a partir de c = 80, ambos 0,200 [sensibilidade.csv, limiar_inferior e limiar_superior]. Essa figura não depende de modelo, e o trabalho não escolhe valor de custo."),
  });
  if (Object.keys(sen).length !== 84) erros.push("slide 7: sensibilidade.csv não tem 84 linhas");
  chk("slide 7 notas", s._notas, [[sen["200/70"].limiar_inferior, 3], [sen["400/80"].limiar_superior, 3], [sen["400/0"].limiar_superior, 3]]);
  img(s, "sensibilidade.png", { x: M, y: 1.5, w: UW, h: 3.5 });
  const b = R("Grade: perda 200–800; custo 0–100. / c = 0: análise manual cobre 0 a 1. / Limiares coincidem → volta a duas ações. / Nenhum valor escolhido.").split(" / ");
  T(s, b.slice(0, 2), { x: M, y: 5.1, w: 6.0, h: 1.4, pt: 20, bullet: true, kind: "body" });
  T(s, b.slice(2), { x: 6.83, y: 5.1, w: 6.0, h: 1.4, pt: 20, bullet: true, kind: "body" });
  fechar(s, true, null);
}

// 8 — Desenvolvimento
{
  const t = R("No desenvolvimento, o TAN ficou abaixo do Naive Bayes nas cinco métricas; NB e logística ficaram a 0,001 de ROC-AUC");
  chk("slide 8", t, [[dev.nb.roc_auc_media - dev.logreg.roc_auc_media, 3]]);
  const s = novo({
    titulo: t,
    sowhat: R("o TAN, estrutura mais rica, não trouxe ganho aqui; o resultado entra como saiu."),
    notas: R("No desenvolvimento, a ROC-AUC média foi 0,789 no Naive Bayes, 0,788 na logística e 0,742 no TAN [resultados/metricas_dev.csv, roc_auc_media]. NB e logística diferem em 0,001, abaixo de 0,03, e pela regra descritiva do plano é tratada como ruído. O TAN ficou abaixo do NB nas cinco métricas; o erro de calibração do TAN foi 0,152, contra 0,093 do NB e 0,095 da logística [metricas_dev.csv, ece_media]. O desvio do TAN entre partições foi 0,049 [roc_auc_desvio]. Não ajustei nada por causa disso: o resultado vai como saiu."),
  });
  // "abaixo nas cinco métricas": AUCs menores, Brier/log loss/ECE maiores
  const d = dev;
  if (!(d.tan.roc_auc_media < d.nb.roc_auc_media && d.tan.pr_auc_media < d.nb.pr_auc_media && d.tan.brier_media > d.nb.brier_media && d.tan.log_loss_media > d.nb.log_loss_media && d.tan.ece_media > d.nb.ece_media)) erros.push("slide 8: TAN não fica abaixo do NB nas cinco métricas");
  const ms = ["nb", "tan", "logreg", "taxa_base"], nm = { nb: "NB", tan: "TAN", logreg: "Logística", taxa_base: "Taxa base", sel: "sel" };
  faixas(s, ms.map((m) => `${nm[m]} ${fmt(d[m].roc_auc_media, 3)}`), ms.map((m) => d[m].roc_auc_media - d[m].roc_auc_desvio), ms.map((m) => d[m].roc_auc_media + d[m].roc_auc_desvio), ms.map((m) => m === "tan"), { x: M, y: 1.55, w: 7.2, h: 4.3 }, { min: 0.4, max: 0.9, passo: 0.1, titulo: "ROC-AUC média ± 1 desvio (5 partições)" });
  T(s, "NB − logística: 0,001 → abaixo de 0,03", { x: M, y: 5.9, w: 7.2, h: 0.45, pt: 20, color: C.azul, kind: "body" });
  const body = R("ROC-AUC: NB 0,789; logística 0,788; TAN 0,742 (desvio 0,049). / ECE do TAN 0,152 (NB 0,093). / Média de 5 partições, sem intervalo.");
  chk("slide 8", body, [[d.nb.roc_auc_media, 3], [d.logreg.roc_auc_media, 3], [d.tan.roc_auc_media, 3], [d.tan.roc_auc_desvio, 3], [d.tan.ece_media, 3], [d.nb.ece_media, 3]]);
  chk("slide 8 notas", s._notas, [[d.logreg.ece_media, 3]]);
  T(s, body.split(" / "), { ...DIR, h: 3.4, pt: 20, bullet: true, gap: true, kind: "body" });
  fechar(s, true, { x: DIR.x, y: 5.1, w: DIR.w, h: 1.3 });
}

// 9 — Teste: discriminação
{
  const t = R("No teste, as diferenças de ROC-AUC entre os três modelos ficaram entre 0,001 e 0,022, abaixo de 0,03: pela regra, são tratadas como ruído");
  const a = tst.nb.roc_auc, b = tst.tan.roc_auc, c = tst.logreg.roc_auc;
  const difs = [Math.abs(a - c), Math.abs(a - b), Math.abs(c - b)];
  chk("slide 9", t, [[Math.min(...difs), 3], [Math.max(...difs), 3]]);
  if (Math.max(...difs) >= 0.03) erros.push("slide 9: diferença ≥ 0,03");
  const s = novo({
    titulo: t,
    sowhat: R("o teste não distingue os modelos pela discriminação."),
    notas: R("No teste, a ROC-AUC foi 0,728 no NB, 0,706 no TAN e 0,729 na logística [resultados/metricas_teste.csv, roc_auc]. As diferenças são 0,001, 0,021 e 0,022; todas abaixo de 0,03 e, pela regra descritiva do plano, tratadas como ruído, sem apontar qual modelo é melhor. Os intervalos de 95% por *bootstrap* são largos; o do TAN vai de 0,623 a 0,789 [roc_auc_ic_inf, roc_auc_ic_sup]. A PR-AUC foi 0,490, 0,480 e 0,500, contra 0,300 da taxa base [pr_auc]; para ela não fixei regra de ruído, então só descrevo. Também registro que todos caíram em relação ao desenvolvimento; não testei a causa."),
  });
  chk("slide 9 notas", s._notas, [...difs.map((x) => [x, 3]), [tst.tan.roc_auc_ic_inf, 3], [tst.tan.roc_auc_ic_sup, 3]]);
  const ms = ["nb", "tan", "logreg"], nm = { nb: "NB", tan: "TAN", logreg: "Logística" };
  faixas(s, ms.map((m) => `${nm[m]} ${fmt(tst[m].roc_auc, 3)}`), ms.map((m) => tst[m].roc_auc_ic_inf), ms.map((m) => tst[m].roc_auc_ic_sup), ms.map((m) => m === "tan"), { x: M, y: 1.55, w: 7.2, h: 4.3 }, { min: 0.5, max: 0.85, passo: 0.05, titulo: "ROC-AUC no teste, IC 95% (bootstrap); eixo começa na taxa base, 0,5" });
  const body = R("n = 200; 60 ruins. / NB 0,728; TAN 0,706; logística 0,729. / IC 95% por *bootstrap*, largos e sobrepostos. / PR-AUC: 0,490; 0,480; 0,500 (taxa base 0,300), só descrita.");
  chk("slide 9", body, [[a, 3], [b, 3], [c, 3], [tst.nb.pr_auc, 3], [tst.tan.pr_auc, 3], [tst.logreg.pr_auc, 3], [tst.taxa_base.pr_auc, 3], [tst.taxa_base.pr_auc * 200, 0]]);
  T(s, body.split(" / "), { ...DIR, h: 4.0, pt: 20, bullet: true, gap: true, kind: "body" });
  cite(s, R("(EFRON; TIBSHIRANI, 1993)"));
  fechar(s, true, { x: DIR.x, y: 5.7, w: DIR.w, h: 0.75 });
}

// 10 — Brier
{
  const t = R("No teste, o Brier do TAN (0,215) ficou acima do da taxa base (0,210): o TAN não foi melhor que prever a taxa base");
  chk("slide 10", t, [[tst.tan.brier, 3], [tst.taxa_base.brier, 3]]);
  if (!(tst.tan.brier >= tst.taxa_base.brier)) erros.push("slide 10: Brier do TAN não ≥ taxa base");
  const s = novo({
    titulo: t,
    sowhat: R("a probabilidade do TAN, que alimenta a decisão principal, não supera a taxa base no teste."),
    notas: R("O Brier mede o erro da probabilidade. No teste, o do TAN foi 0,215, acima dos 0,210 de quem prevê a taxa base para todo caso [resultados/metricas_teste.csv, brier, linhas tan e taxa_base]. Pelo critério do plano, digo: o TAN não foi melhor que prever a taxa base; é uma comparação pontual, sem inferência. NB, com 0,199, e logística, com 0,191, ficaram abaixo [brier]. O erro de calibração foi 0,115, 0,157 e 0,078 [ece]. A calibração foi só medida; não corrigi."),
  });
  const ms = ["nb", "tan", "logreg", "taxa_base"], nm = { nb: "NB", tan: "TAN", logreg: "Logística", taxa_base: "Taxa base" };
  faixas(s, ms.map((m) => `${nm[m]} ${fmt(tst[m].brier, 3)}`), ms.map((m) => tst[m].brier_ic_inf), ms.map((m) => tst[m].brier_ic_sup), ms.map((m) => m === "tan"), { x: M, y: 1.55, w: 7.2, h: 4.3 }, { min: 0.14, max: 0.28, passo: 0.02, titulo: "Brier no teste, IC 95% (bootstrap); menor é melhor" });
  T(s, "Taxa base: 0,210", { x: M, y: 5.9, w: 7.2, h: 0.45, pt: 20, color: C.alerta, kind: "body" });
  const body = R("Brier: NB 0,199; logística 0,191; TAN 0,215. / ECE: NB 0,115; TAN 0,157; logística 0,078. / Calibração só medida, sem correção.");
  chk("slide 10", body, [[tst.nb.brier, 3], [tst.logreg.brier, 3], [tst.tan.brier, 3], [tst.nb.ece, 3], [tst.tan.ece, 3], [tst.logreg.ece, 3]]);
  T(s, body.split(" / "), { ...DIR, h: 3.4, pt: 20, bullet: true, gap: true, kind: "body" });
  cite(s, R("(BRIER, 1950; NAEINI; COOPER; HAUSKRECHT, 2015)"));
  fechar(s, true, { x: DIR.x, y: 5.1, w: DIR.w, h: 1.3 });
}

// 11 — Política de três ações
{
  const ori = R("Com o TAN, a política de três ações teve utilidade média 22,5 maior que o corte 0,5 (IC 95% de 9,2 a 37,2), uma vantagem prevista pela matriz, restrita à simulação");
  // Encurtado: o original passa de 150 caracteres. Mantém número, IC e "prevista pela matriz".
  const t = "Com o TAN, as três ações tiveram utilidade média 22,5 maior que o corte 0,5 (IC 95%: 9,2 a 37,2), vantagem prevista pela matriz (simulação)";
  relat.encurtado = { ori, novo: t };
  const D = dif.tan;
  chk("slide 11", ori + t, [[D.dif_utilidade_media, 1], [D.dif_ic_inf, 1], [D.dif_ic_sup, 1]]);
  if (Math.abs(res["tan/ue"].utilidade_media - res["tan/limiar"].utilidade_media - D.dif_utilidade_media) > 1e-9) erros.push("slide 11: resumo e diferença não batem");
  const s = novo({
    titulo: t,
    sowhat: R("responde à parte 2: há efeito medido, mas ele vem da ação extra e da matriz, não da rede."),
    notas: R("Esta é a comparação principal, fixada antes: TAN, política de três ações contra corte 0,5 de duas ações. A diferença pareada de utilidade média foi 22,5, com intervalo de 95% de 9,2 a 37,2 [resultados/diferenca_politicas_teste.csv, linha tan]. O intervalo exclui zero, então leio: diferença a favor da política de três ações, sem afirmar causa. A política aprovou 92, rejeitou 48 e mandou 60 para análise manual; o corte aprovou 145 e rejeitou 55; os 60 que mudaram são exatamente os da análise manual [resumo_politicas_teste.csv]. E a ressalva principal: com analista infalível, a análise manual quase não tem risco, então a matriz prevê vantagem para a política de três ações na utilidade esperada do modelo; a utilidade realizada depende da calibração, e o corte de 0,5 nem é o ótimo de duas ações, que é 0,2. A vantagem é consequência da matriz e do conjunto de ações, não evidência sobre a rede."),
  });
  const ue = res["tan/ue"], li = res["tan/limiar"];
  chk("slide 11 notas", s._notas, [[ue.n_aprovar, 0], [ue.n_rejeitar, 0], [ue.n_analise_manual, 0], [ue.n_mudam_vs_outra_regra, 0], [li.n_aprovar, 0], [li.n_rejeitar, 0]]);
  if (D.dif_ic_inf <= 0) erros.push("slide 11: IC não exclui zero");
  const ms = ["tan", "nb", "logreg", "sel"], nm = { nb: "NB", tan: "TAN (principal)", logreg: "Logística", sel: "sel" };
  faixas(s, ms.map((m) => `${nm[m]} ${fmt(dif[m].dif_utilidade_media, 1)}`), ms.map((m) => dif[m].dif_ic_inf), ms.map((m) => dif[m].dif_ic_sup), ms.map((m) => m === "tan"), { x: M, y: 1.5, w: 7.2, h: 2.9 }, { min: 0, max: 60, passo: 10, fmt: "0", titulo: "Diferença pareada de utilidade média (três ações − corte 0,5), IC 95%; eixo começa em zero" });
  const cats = ["TAN: três ações", "TAN: corte 0,5"];
  s.addChart(pres.charts.BAR, [
    { name: "Aprovar", labels: cats, values: [ue.n_aprovar, li.n_aprovar] },
    { name: "Rejeitar", labels: cats, values: [ue.n_rejeitar, li.n_rejeitar] },
    { name: "Análise manual", labels: cats, values: [ue.n_analise_manual, li.n_analise_manual] },
  ], {
    x: M, y: 4.45, w: 7.2, h: 2.0, barDir: "bar", barGrouping: "stacked", chartColors: [C.navy, C.cinza, C.azul], catAxisOrientation: "maxMin",
    showValue: true, dataLabelFontSize: 14, dataLabelColor: C.branco, showLegend: true, legendPos: "b", legendFontSize: 14,
    catAxisLabelFontSize: 14, valAxisHidden: true, valGridLine: { style: "none" }, valAxisMaxVal: 200, valAxisMinVal: 0,
  });
  T(s, R("IC exclui zero → diferença a favor das três ações; sem causa. / Os 60 que mudam = os 60 em análise manual.").split(" / "), { ...DIR, h: 2.6, pt: 20, bullet: true, gap: true, kind: "body" });
  T(s, R("Ressalvas: matriz demonstrativa; analista infalível; simulação, não política real."), { x: DIR.x, y: 4.3, w: DIR.w, h: 1.4, pt: 20, color: C.alerta, line: C.alerta, fill: C.branco, kind: "body" });
  fechar(s, true, { x: DIR.x, y: 5.8, w: DIR.w, h: 0.6 });
}

// 12 — Seleção
{
  const ori12 = R("O estudo de seleção secundário escolheu NB com BDeu 50, a 0,001 de ROC-AUC da referência; a grade foi desenhada depois de ver o desenvolvimento");
  // Encurtado: 3 linhas estimadas a 24 pt.
  const t = "O estudo de seleção secundário escolheu NB com BDeu 50, a 0,001 de ROC-AUC da referência; a grade veio depois de ver o desenvolvimento";
  relat.encurtado12 = { ori: ori12, novo: t };
  chk("slide 12", t, [[sel.nb_ess5.roc_auc_media - sel.aninhado.roc_auc_media, 3]]);
  const s = novo({
    titulo: t,
    sowhat: R("a seleção não muda a leitura; serve para mostrar que o viés foi declarado, não escondido."),
    notas: R("Depois de ver o TAN abaixo do NB, desenhei um estudo secundário: 8 configurações, NB e TAN com tamanho equivalente 1, 5, 10 e 50, em validação cruzada aninhada. A regra escolheu nb_ess50 nas cinco partições externas e no desenvolvimento inteiro [resultados/selecao_escolha.csv, escolhida]. A ROC-AUC do aninhado, 0,788, difere em 0,001 da referência nb_ess5, 0,789: abaixo de 0,03, tratada como ruído pela regra do plano [selecao_dev.csv, roc_auc_media]. O aninhamento corrige a escolha entre as 8, mas não o fato de a grade ter sido desenhada olhando o desenvolvimento; esse viés está declarado. A análise primária continua com NB e TAN de BDeu 5."),
  });
  chk("slide 12 notas", s._notas, [[sel.aninhado.roc_auc_media, 3], [sel.nb_ess5.roc_auc_media, 3]]);
  const ms = Object.keys(sel);
  faixas(s, ms.map((m) => `${m} ${fmt(sel[m].log_loss_media, 3)}${m === "nb_ess50" ? " (5/5)" : ""}`), ms.map((m) => sel[m].log_loss_media - sel[m].log_loss_desvio), ms.map((m) => sel[m].log_loss_media + sel[m].log_loss_desvio), ms.map((m) => m === "nb_ess50" || m === "aninhado"), { x: M, y: 1.55, w: 7.2, h: 4.85 }, { min: 0.4, max: 1.1, passo: 0.1, titulo: "log loss médio ± 1 desvio; azul: escolhida em 5/5 partições e aninhado" });
  T(s, R("8 comparações; regra: menor *log loss* interno. / Escolhida: nb_ess50 em todas as partições. / **Viés declarado:** grade motivada pelas métricas do desenvolvimento. / Análise primária não muda.").split(" / "), { ...DIR, h: 4.85, pt: 20, bullet: true, gap: true, kind: "body" });
  fechar(s, true, null);
}

// 13 — Limitações
{
  const s = novo({
    titulo: R("Os resultados valem para esta base, esta matriz demonstrativa e um analista infalível: é simulação, não política real"),
    sowhat: R("antecipa as objeções da banca antes da arguição."),
    notas: R("Seis limites acompanham tudo o que mostrei. A matriz é demonstrativa e supõe um analista que sempre acerta. A base não registra o que teria acontecido com as ações não tomadas, então a camada de decisão é simulação. O teste tem 200 casos e 60 ruins, e os intervalos são largos; no TAN, a diferença vai de 9,2 a 37,2 [diferenca_politicas_teste.csv]. Modelo e representação das variáveis variam juntos, o intervalo reamostra só o teste e não o treino, e a calibração foi só medida. Por isso não generalizo para outras bases nem recomendo um modelo."),
  });
  chk("slide 13 notas", s._notas, [[dif.tan.dif_ic_inf, 1], [dif.tan.dif_ic_sup, 1]]);
  const b = R("Matriz demonstrativa; analista infalível. / Sem desfecho das ações não tomadas → simulação. / Teste: 200 casos, 60 ruins → IC largos. / Modelo e representação variam juntos. / IC não cobre variação do treino. / Calibração só medida.").split(" / ");
  T(s, b.slice(0, 3), { x: M, y: 1.7, w: 5.9, h: 4.0, pt: 20, bullet: true, gap: true, kind: "body" });
  T(s, b.slice(3), { x: 6.93, y: 1.7, w: 5.9, h: 4.0, pt: 20, bullet: true, gap: true, kind: "body" });
  fechar(s, true, { x: M, y: 5.85, w: UW, h: 0.5 });
}

// 14 — Conclusões
{
  const t = R("Separar risco e ação dá limiares explícitos por construção; o efeito medido favorece as três ações, sem causa e sem modelo recomendado");
  const s = novo({
    titulo: t, escuro: true,
    sowhat: R("as duas partes da pergunta respondidas numa tela."),
    notas: R("Concluindo. Parte 1: separar risco e ação dá limiares explícitos, 0,10 e 0,60 com esta matriz, que qualquer pessoa reproduz; isso vale por construção e não distingue a rede da logística. Parte 2: com o TAN, a política de três ações teve utilidade média 22,5 maior que o corte 0,5, com intervalo de 9,2 a 37,2, uma vantagem prevista pela matriz, restrita à simulação. No risco, as diferenças de ROC-AUC ficaram abaixo de 0,03, sem apontar qual modelo é melhor, e o TAN não foi melhor que a taxa base no Brier. Fico à disposição para perguntas e comentários da banca."),
  });
  const body = R("1. Limiares 0,10 e 0,60 saem da matriz; valem para qualquer escore. / 2. TAN: +22,5 de utilidade média [9,2; 37,2], prevista pela matriz. / 3. ROC-AUC: diferenças < 0,03, sem apontar qual modelo é melhor; Brier do TAN não melhor que taxa base.");
  chk("slide 14", body, [[lim[0], 2], [lim[1], 2], [dif.tan.dif_utilidade_media, 1], [dif.tan.dif_ic_inf, 1], [dif.tan.dif_ic_sup, 1]]);
  T(s, body.split(" / "), { x: M, y: 1.75, w: UW, h: 3.6, pt: 22, color: C.branco, gap: true, kind: "body" });
  placeholder(s, "[e-mail]", M, 5.85, 4.0);
  placeholder(s, "[link do repositório]", 4.8, 5.85, 5.0);
  fechar(s, true, null);
}

// =================== APÊNDICE ===================
{
  const s = novo({ titulo: "Referências" });
  const refs = [
    "ANKAN, A.; TEXTOR, J. pgmpy: A Python Toolkit for Bayesian Networks. *JMLR*, v. 25, n. 265, 2024.",
    "BRIER, G. W. Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, v. 78, n. 1, 1950.",
    "EFRON, B.; TIBSHIRANI, R. J. *An Introduction to the Bootstrap*. Chapman & Hall, 1993.",
    "ELKAN, C. The foundations of cost-sensitive learning. In: IJCAI, 17., 2001. p. 973–978.",
    "FRIEDMAN, N.; GEIGER, D.; GOLDSZMIDT, M. Bayesian network classifiers. *Machine Learning*, v. 29, 1997.",
    "GRÖMPING, U. *South German Credit Data*: Correcting a Widely Used Data Set. Beuth Univ., 2019.",
    "HECKERMAN, D.; GEIGER, D.; CHICKERING, D. M. Learning Bayesian networks. *Machine Learning*, v. 20, 1995.",
    "NAEINI, M. P.; COOPER, G. F.; HAUSKRECHT, M. Obtaining well calibrated probabilities using Bayesian binning. AAAI, 2015.",
    "PEARL, J. *Probabilistic Reasoning in Intelligent Systems*. Morgan Kaufmann, 1988.",
    "PEDREGOSA, F. et al. Scikit-learn. *JMLR*, v. 12, 2011.",
    "SIDDIQI, N. *Credit Risk Scorecards*. Wiley, 2012.",
    "THOMAS, L. C. A survey of credit and behavioural scoring. *Int. J. Forecasting*, v. 16, n. 2, 2000.",
    "ZADROZNY, B.; ELKAN, C. Obtaining calibrated probability estimates from decision trees and naive Bayesian classifiers. ICML, 2001.",
  ].map(R);
  T(s, refs.slice(0, 7), { x: M, y: 1.5, w: 6.0, h: 4.6, pt: 13, gap: true, kind: "ref" });
  T(s, refs.slice(7), { x: 6.83, y: 1.5, w: 6.0, h: 4.6, pt: 13, gap: true, kind: "ref" });
  T(s, "A conferir pelo autor: ELKAN (2001) “a conferir no original”; GRÖMPING (2019) “verificar série/instituição”.", { x: M, y: 6.2, w: UW, h: 0.5, pt: 13, color: C.alerta, kind: "ref" });
  fechar(s, false);
}

function apendice(titulo, resp, exib, nums, abaixo) {
  const s = novo({ titulo: R(titulo) });
  const r = R(resp);
  if (nums) chk("apêndice " + titulo.slice(0, 20), r, nums);
  if (abaixo) { T(s, r, { x: M, y: 1.6, w: UW, h: 2.6, pt: 20, kind: "app" }); abaixo(s); }
  else if (exib) { exib(s); T(s, r, { x: 6.2, y: 1.6, w: W - M - 6.2, h: 4.9, pt: 20, kind: "app" }); }
  else T(s, r, { x: M, y: 1.7, w: UW, h: 4.6, pt: 20, kind: "app" });
  fechar(s, false);
}
const IMG_ESQ = { x: M, y: 1.55, w: 5.5, h: 5.0 };
apendice("O TAN ficou abaixo do NB, e a hipótese sobre `verw` é registrada, mas não foi testada",
  "Não sei a causa e não afirmo. Em todas as partições `verw` é, fora `kredit`, a variável com mais arestas de saída, 7 a 9 [resultados/tan_arestas.csv, origem]; tabelas esparsas e excesso de confiança seriam coerentes com o *log loss* 0,704 e o ECE 0,152 do TAN [metricas_dev.csv], mas nenhuma análise testou isso. No estudo de seleção, o *log loss* do TAN cai de 0,825 (ess 1) para 0,583 (ess 50) [selecao_dev.csv], o que também não testa a hipótese.",
  (s) => img(s, "calibracao_dev.png", IMG_ESQ),
  [[dev.tan.log_loss_media, 3], [dev.tan.ece_media, 3], [sel.tan_ess1.log_loss_media, 3], [sel.tan_ess50.log_loss_media, 3]]);
{ // arestas de verw por partição, lidas do CSV
  const [, ...ls] = fs.readFileSync(RES("tan_arestas.csv"), "utf8").trim().split("\n");
  const n = {}; ls.forEach((l) => { const [f, o] = l.split(","); if (o === "verw") n[f] = (n[f] || 0) + 1; });
  const v = Object.values(n);
  if (Math.min(...v) !== 7 || Math.max(...v) !== 9) erros.push("A1: arestas de verw fora de 7 a 9: " + v);
}
apendice("Calibrar exigiria escolher o método depois de ver as métricas, o que quebraria a pré-especificação",
  "Decisão P1: corrigir pediria escolher entre métodos olhando o desenvolvimento. A exigência de probabilidade calibrada para decidir por custos vem da literatura (ZADROZNY; ELKAN, 2001), não do experimento. Medi: ECE no teste 0,115 (NB), 0,157 (TAN), 0,078 (logística) [metricas_teste.csv, ece]. Calibrar é direção futura.",
  (s) => img(s, "calibracao_teste.png", IMG_ESQ), [[tst.nb.ece, 3], [tst.tan.ece, 3], [tst.logreg.ece, 3]]);
apendice("O corte 0,5 foi fixado na pergunta antes dos resultados; não é o limiar de duas ações da matriz, que seria 0,2",
  "O corte 0,5 representa a regra fixa sem referência a custos e está no texto da pergunta [PLANO.md §1]. Com esta matriz, o limiar de duas ações seria G/(G+L) = 100/500 = 0,2; a comparação não o inclui, e isso decorre da Seção 2.7, não de uma métrica. A comparação, portanto, não testa 'utilidade esperada contra qualquer limiar'.",
  null, [[G / (G + L), 1], [G + L, 0]]);
apendice("Mudar perda ou custo desloca os limiares de forma previsível; acima de certo custo a análise manual some",
  "A fórmula dá a resposta sem rodar nada: análise manual entre c/L e 1 − c/G. Na grade, perda 400 e c = 80 já zeram a faixa (0,200 e 0,200); perda 800 e c = 50 dão 0,063 e 0,5 [sensibilidade.csv]. A diferença de utilidade no teste só foi medida com a matriz aprovada; com outra matriz, ela teria de ser recalculada.",
  null, [[sen["400/80"].limiar_inferior, 3], [sen["400/80"].limiar_superior, 3], [sen["800/50"].limiar_inferior, 3], [sen["800/50"].limiar_superior, 1]],
  (s) => img(s, "sensibilidade.png", { x: M, y: 4.3, w: UW, h: 2.5 }));
apendice("5 partições é convenção fixada antes dos resultados, não escolhida por desempenho",
  "Constante congelada, como as 3 faixas e o BDeu 5 [docs/decisoes.md §2; monografia §3.3]. Com 800 casos, cada partição tem 160 casos de validação e 48 ruins (estratificada). Não testei outros valores para não escolher pelo resultado.", null);
apendice("O teste ficou fechado até o congelamento; o único vazamento é brando e está declarado",
  "Cortes das faixas aprendidos só no treino de cada partição; teste aberto uma vez, em 17/11/2026, sobre o *commit* 49d77ff. O espaço de estados de cada variável usa todos os valores do desenvolvimento inteiro, para uma categoria rara não quebrar a inferência; não usa o rótulo, mas é um vazamento brando, declarado [decisões P10; plano-de-análise §6, item 6]. A divisão com semente 42 foi descartada porque seu teste já tinha sido usado antes.", null);
apendice("Com analista infalível, o modelo prevê vantagem para a análise manual; o ganho realizado depende da calibração e do corte de comparação",
  "Na análise manual o analista acerta sempre: ganha 60 num bom e perde 40 num ruim. Entre 0,10 e 0,60 essa reta fica acima de aprovar e de rejeitar. Pelo modelo, a política de três ações nunca tem utilidade esperada menor que a de duas. Isso não garante ganho realizado: depende da calibração (ECE do TAN no teste: 0,157, o maior dos três), e o corte 0,5 nem é o ótimo de duas ações (0,2). No teste, as quatro diferenças foram positivas, de 22,5 a 38,3 [diferenca_politicas_teste.csv]. Por isso a diferença não é evidência sobre a rede nem sobre o critério da utilidade esperada.",
  (s) => retasUE(s, { x: M, y: 1.55, w: 5.5, h: 5.0 }, true),
  [[U.analise_manual.bom, 0], [cA, 0], [lim[0], 2], [lim[1], 2], [Math.min(...Object.values(dif).map((o) => o.dif_utilidade_media)), 1], [Math.max(...Object.values(dif).map((o) => o.dif_utilidade_media)), 1]]);
if (Object.values(dif).some((o) => o.dif_utilidade_media <= 0)) erros.push("A7: nem todas as diferenças são positivas");
apendice("Com 60 ruins, diferenças pequenas dificilmente se separam de ruído, e por isso o plano definiu antes o limite descritivo de 0,03",
  "O plano já previa que, com 60 ruins, diferença de AUC de 0,02 a 0,03 dificilmente se separa de ruído (limite descritivo, não teste de equivalência) [PLANO.md §6]. Os intervalos confirmam: ROC-AUC do TAN de 0,623 a 0,789; diferença de utilidade de 9,2 a 37,2 [metricas_teste.csv; diferenca_politicas_teste.csv]. E o intervalo reamostra só o teste, não o treino, então a incerteza total é maior.",
  null, [[tst.tan.roc_auc_ic_inf, 3], [tst.tan.roc_auc_ic_sup, 3], [dif.tan.dif_ic_inf, 1], [dif.tan.dif_ic_sup, 1]]);
apendice("Nenhuma regra do plano separou os modelos no teste, e escolher um seria decidir pelo resultado",
  "As diferenças de ROC-AUC no teste foram até 0,022, tratadas como ruído pela regra descritiva do plano [metricas_teste.csv]. PR-AUC só descrita. No Brier, só o TAN foi não melhor que a taxa base. A comparação principal usa o TAN porque foi fixada antes (P5), não por desempenho. O estudo de seleção diz o que a regra escolheu, não o que adotar.",
  null, [[tst.logreg.roc_auc - tst.tan.roc_auc, 3]]);

if (erros.length) { console.error("BUILD FALHOU:\n- " + erros.join("\n- ")); process.exit(1); }
pres.writeFile({ fileName: OUT }).then(() => console.log(JSON.stringify({ ok: OUT, slides: nSlide, ...relat }, null, 1)));
