from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "outputs" / "manual-roteiro-execucao" / "presentations" / "roteiro-execucao"
SLIDES_DIR = WORKSPACE / "slides"
PREVIEW_DIR = WORKSPACE / "preview"
LAYOUT_DIR = WORKSPACE / "layout"
QA_DIR = WORKSPACE / "qa"
OUTPUT_DIR = ROOT / "slides"


COMMON = r"""
export const C = {
  ink: "#1C2430",
  muted: "#5D6878",
  bg: "#F7F9FB",
  panel: "#FFFFFF",
  line: "#DCE4EC",
  teal: "#0E7C7B",
  blue: "#3563E9",
  amber: "#D98C1F",
  coral: "#D75A4A",
  green: "#2E7D32",
  dark: "#14213D",
};

export function base(slide, ctx, section, title) {
  ctx.addShape(slide, { x: 0, y: 0, w: ctx.W, h: ctx.H, fill: C.bg });
  ctx.addText(slide, {
    x: 56,
    y: 32,
    w: 720,
    h: 24,
    text: section.toUpperCase(),
    fontSize: 11,
    bold: true,
    color: C.teal,
  });
  ctx.addText(slide, {
    x: 56,
    y: 66,
    w: 970,
    h: 72,
    text: title,
    fontSize: 30,
    bold: true,
    color: C.ink,
    typeface: ctx.fonts.title,
  });
  ctx.addShape(slide, { x: 56, y: 148, w: 1168, h: 1.5, fill: C.line });
}

export function footer(slide, ctx, page) {
  ctx.addText(slide, {
    x: 56,
    y: 684,
    w: 720,
    h: 20,
    text: "Roteiro manual | Coffee Shop Sales DW + ML",
    fontSize: 9,
    color: C.muted,
  });
  ctx.addText(slide, {
    x: 1172,
    y: 684,
    w: 52,
    h: 20,
    text: String(page).padStart(2, "0"),
    fontSize: 9,
    color: C.muted,
    align: "right",
  });
}

export function metric(slide, ctx, x, y, w, value, label, color = C.teal) {
  ctx.addShape(slide, { x, y, w, h: 92, fill: C.panel, line: ctx.line(C.line, 1) });
  ctx.addText(slide, { x: x + 18, y: y + 15, w: w - 36, h: 34, text: value, fontSize: 25, bold: true, color, typeface: ctx.fonts.title });
  ctx.addText(slide, { x: x + 18, y: y + 54, w: w - 36, h: 26, text: label, fontSize: 12, color: C.muted });
}

export function card(slide, ctx, x, y, w, h, title, body, color = C.teal) {
  ctx.addShape(slide, { x, y, w, h, fill: C.panel, line: ctx.line(C.line, 1) });
  ctx.addShape(slide, { x, y, w: 5, h, fill: color });
  ctx.addText(slide, { x: x + 18, y: y + 14, w: w - 34, h: 25, text: title, fontSize: 15, bold: true, color: C.ink });
  ctx.addText(slide, { x: x + 18, y: y + 46, w: w - 34, h: h - 72, text: body, fontSize: 12, color: C.muted });
}

export function step(slide, ctx, x, y, n, title, body, color = C.teal) {
  ctx.addShape(slide, { x, y, w: 48, h: 48, geometry: "ellipse", fill: color });
  ctx.addText(slide, { x, y: y + 10, w: 48, h: 24, text: String(n).padStart(2, "0"), fontSize: 15, bold: true, color: "#FFFFFF", align: "center", valign: "mid" });
  ctx.addText(slide, { x: x + 62, y: y + 2, w: 270, h: 24, text: title, fontSize: 15, bold: true, color: C.ink });
  ctx.addText(slide, { x: x + 62, y: y + 30, w: 300, h: 44, text: body, fontSize: 12, color: C.muted });
}

export function check(slide, ctx, x, y, text, color = C.teal, w = 470) {
  ctx.addShape(slide, { x, y: y + 8, w: 9, h: 9, geometry: "ellipse", fill: color });
  ctx.addText(slide, { x: x + 20, y, w, h: 34, text, fontSize: 13, color: C.ink });
}

export function miniTable(slide, ctx, x, y, w, rows, colors = [C.teal, C.blue]) {
  const rowH = 34;
  rows.forEach((row, i) => {
    const fill = i === 0 ? C.dark : C.panel;
    const color = i === 0 ? "#FFFFFF" : C.ink;
    ctx.addShape(slide, { x, y: y + i * rowH, w, h: rowH, fill, line: ctx.line(C.line, 1) });
    ctx.addText(slide, { x: x + 12, y: y + i * rowH + 8, w: w * 0.46, h: 18, text: row[0], fontSize: 11, bold: i === 0, color });
    ctx.addText(slide, { x: x + w * 0.52, y: y + i * rowH + 8, w: w * 0.42, h: 18, text: row[1], fontSize: 11, bold: i === 0, color, align: "right" });
  });
}
"""


SLIDES = {
    "slide-01.mjs": r"""
import { C, footer, metric } from "./common.mjs";

export async function slide01(presentation, ctx) {
  const slide = presentation.slides.add();
  ctx.addShape(slide, { x: 0, y: 0, w: ctx.W, h: ctx.H, fill: C.bg });
  ctx.addShape(slide, { x: 0, y: 0, w: 430, h: ctx.H, fill: C.dark });
  ctx.addText(slide, { x: 60, y: 66, w: 300, h: 24, text: "ROTEIRO MANUAL", fontSize: 12, bold: true, color: "#8FD8D2" });
  ctx.addText(slide, { x: 60, y: 126, w: 300, h: 150, text: "Como fazer o projeto do início ao fim", fontSize: 40, bold: true, color: "#FFFFFF", typeface: ctx.fonts.title });
  ctx.addText(slide, { x: 60, y: 322, w: 300, h: 86, text: "Coffee Shop Sales\nData Warehouse + Machine Learning", fontSize: 18, color: "#E7EDF4" });
  ctx.addText(slide, { x: 500, y: 92, w: 660, h: 80, text: "Um guia de execução para fazer tudo na mão, entendendo cada etapa.", fontSize: 32, bold: true, color: C.ink, typeface: ctx.fonts.title });
  ctx.addText(slide, { x: 500, y: 194, w: 670, h: 50, text: "Use estes slides como checklist de trabalho e como base para dividir a fala entre as duas pessoas do grupo.", fontSize: 16, color: C.muted });
  metric(slide, ctx, 500, 312, 186, "26", "etapas no roteiro", C.teal);
  metric(slide, ctx, 714, 312, 186, "7", "dias sugeridos", C.blue);
  metric(slide, ctx, 928, 312, 186, "2", "pessoas no grupo", C.amber);
  ctx.addShape(slide, { x: 500, y: 470, w: 614, h: 1.5, fill: C.line });
  ctx.addText(slide, { x: 500, y: 504, w: 614, h: 44, text: "Meta: chegar à entrega com SQL, notebook, slides, relatório opcional e domínio da apresentação.", fontSize: 18, bold: true, color: C.ink, align: "center" });
  footer(slide, ctx, 1);
  return slide;
}
""",
    "slide-02.mjs": r"""
import { base, footer, card, C } from "./common.mjs";

export async function slide02(presentation, ctx) {
  const slide = presentation.slides.add();
  base(slide, ctx, "Mapa geral", "O projeto avança em sete blocos, do dataset à apresentação");
  const items = [
    ["01 Dataset", "Baixar, abrir e validar requisitos.", C.teal],
    ["02 Pergunta", "Definir a pergunta de negócio.", C.blue],
    ["03 DW", "Modelar fato, dimensões e chaves.", C.amber],
    ["04 SQL", "Criar banco, views e validações.", C.coral],
    ["05 EDA", "Gerar métricas e gráficos.", C.green],
    ["06 ML", "Treinar, avaliar e comparar modelos.", C.teal],
    ["07 Entrega", "Insights, slides e ensaio.", C.blue],
  ];
  items.forEach((item, i) => {
    const topRow = i < 4;
    const x = topRow ? 86 + i * 284 : 230 + (i - 4) * 284;
    const y = topRow ? 206 : 386;
    card(slide, ctx, x, y, 236, 112, item[0], item[1], item[2]);
  });
  ctx.addText(slide, { x: 120, y: 548, w: 1040, h: 44, text: "Regra de ouro: cada etapa precisa gerar uma evidência que vocês consigam mostrar ou explicar.", fontSize: 20, bold: true, color: C.ink, align: "center" });
  footer(slide, ctx, 2);
  return slide;
}
""",
    "slide-03.mjs": r"""
import { base, footer, card, check, C } from "./common.mjs";

export async function slide03(presentation, ctx) {
  const slide = presentation.slides.add();
  base(slide, ctx, "Requisitos", "Antes de começar, marquem o que o professor vai cobrar");
  card(slide, ctx, 72, 188, 334, 360, "Dados e DW", "Dataset público com no mínimo 10.000 registros; variáveis numéricas e categóricas; PostgreSQL; star schema; 1 fato; 3 a 5 dimensões; 2 views analíticas.", C.teal);
  card(slide, ctx, 472, 188, 334, 360, "Análise e ML", "EDA em Python; gráficos de distribuição, categorias e evolução temporal; KNN; Árvore de Decisão; Random Forest; Logistic Regression; Regressão Linear.", C.blue);
  card(slide, ctx, 872, 188, 334, 360, "Entrega e fala", "Comparar modelos; explicar melhor desempenho; apresentar 3 a 5 insights; sugerir decisões de negócio; slides; 10 a 15 minutos; todos participam.", C.amber);
  check(slide, ctx, 212, 594, "Tudo que não aparecer claramente pode virar pergunta na apresentação.", C.coral, 850);
  footer(slide, ctx, 3);
  return slide;
}
""",
    "slide-04.mjs": r"""
import { base, footer, metric, card, C } from "./common.mjs";

export async function slide04(presentation, ctx) {
  const slide = presentation.slides.add();
  base(slide, ctx, "Dataset", "Validem a base antes de criar qualquer tabela ou modelo");
  metric(slide, ctx, 80, 190, 182, "149.116", "registros", C.teal);
  metric(slide, ctx, 296, 190, 182, "11", "colunas originais", C.blue);
  metric(slide, ctx, 512, 190, 182, "3", "lojas", C.coral);
  metric(slide, ctx, 728, 190, 182, "80", "produtos", C.amber);
  metric(slide, ctx, 944, 190, 182, "9", "categorias", C.green);
  card(slide, ctx, 82, 344, 310, 148, "Conferir no Excel", "Arquivo abre, datas vão de 01/01/2023 a 30/06/2023, não há nulos críticos e as colunas têm tipos coerentes.", C.teal);
  card(slide, ctx, 456, 344, 310, 148, "Variáveis úteis", "Numéricas: quantidade e preço. Categóricas: loja, categoria, tipo e detalhe. Temporais: data e hora.", C.blue);
  card(slide, ctx, 830, 344, 310, 148, "Conclusão para falar", "A base atende aos requisitos e permite análise por tempo, loja, produto, categoria e demanda.", C.amber);
  footer(slide, ctx, 4);
  return slide;
}
""",
    "slide-05.mjs": r"""
import { base, footer, card, C } from "./common.mjs";

export async function slide05(presentation, ctx) {
  const slide = presentation.slides.add();
  base(slide, ctx, "Pergunta de negócio", "A pergunta central deve guiar DW, EDA, ML e insights");
  ctx.addShape(slide, { x: 116, y: 202, w: 1048, h: 118, fill: C.dark, line: ctx.line(C.dark, 0) });
  ctx.addText(slide, { x: 158, y: 224, w: 964, h: 74, text: "Quais fatores explicam maior receita e maior demanda por loja, produto, mês, dia da semana e horário?", fontSize: 26, bold: true, color: "#FFFFFF", align: "center", typeface: ctx.fonts.title });
  card(slide, ctx, 118, 374, 238, 142, "DW", "Organiza vendas por tempo, loja e produto.", C.teal);
  card(slide, ctx, 386, 374, 238, 142, "Views", "Respondem perguntas analíticas recorrentes.", C.blue);
  card(slide, ctx, 654, 374, 238, 142, "EDA", "Mostra padrões visuais de receita e demanda.", C.amber);
  card(slide, ctx, 922, 374, 238, 142, "ML", "Prevê alta demanda e quantidade vendida.", C.coral);
  ctx.addText(slide, { x: 146, y: 574, w: 988, h: 38, text: "Tudo que vocês fizerem deve voltar para essa pergunta.", fontSize: 21, bold: true, color: C.ink, align: "center" });
  footer(slide, ctx, 5);
  return slide;
}
""",
    "slide-06.mjs": r"""
import { base, footer, C } from "./common.mjs";

function box(slide, ctx, x, y, w, h, title, rows, color) {
  ctx.addShape(slide, { x, y, w, h, fill: "#FFFFFF", line: ctx.line(color, 2) });
  ctx.addShape(slide, { x, y, w, h: 34, fill: color });
  ctx.addText(slide, { x: x + 14, y: y + 8, w: w - 28, h: 18, text: title, fontSize: 12, bold: true, color: "#FFFFFF" });
  rows.forEach((row, i) => ctx.addText(slide, { x: x + 16, y: y + 52 + i * 27, w: w - 32, h: 22, text: row, fontSize: 12, color: C.ink }));
}

export async function slide06(presentation, ctx) {
  const slide = presentation.slides.add();
  base(slide, ctx, "Modelagem dimensional", "Desenhem o star schema antes de escrever SQL");
  box(slide, ctx, 442, 244, 352, 214, "fato_vendas", ["venda_key", "transacao_id", "tempo_key, loja_key, produto_key", "quantidade", "preco_unitario", "receita"], C.dark);
  box(slide, ctx, 82, 190, 260, 164, "dim_tempo", ["data e hora", "mês e dia da semana", "fim de semana", "período do dia"], C.teal);
  box(slide, ctx, 896, 190, 260, 164, "dim_loja", ["localização", "cidade e país", "rede", "tipo de loja"], C.blue);
  box(slide, ctx, 82, 466, 260, 142, "dim_produto", ["categoria", "tipo", "detalhe", "faixa de preço"], C.amber);
  ctx.addShape(slide, { x: 342, y: 270, w: 100, h: 3, fill: C.line });
  ctx.addShape(slide, { x: 794, y: 270, w: 102, h: 3, fill: C.line });
  ctx.addShape(slide, { x: 342, y: 510, w: 100, h: 3, fill: C.line });
  ctx.addText(slide, { x: 858, y: 486, w: 300, h: 74, text: "Dimensão degenerada: transacao_id fica na fato porque identifica a venda, mas não exige tabela própria.", fontSize: 15, bold: true, color: C.ink });
  footer(slide, ctx, 6);
  return slide;
}
""",
    "slide-07.mjs": r"""
import { base, footer, step, C } from "./common.mjs";

export async function slide07(presentation, ctx) {
  const slide = presentation.slides.add();
  base(slide, ctx, "Preparação dos dados", "Façam a transformação entendendo cada coluna criada");
  step(slide, ctx, 82, 196, 1, "Abrir base", "Conferir linhas, colunas, tipos e nulos.", C.teal);
  step(slide, ctx, 82, 306, 2, "Criar receita", "receita = transaction_qty * unit_price.", C.blue);
  step(slide, ctx, 82, 416, 3, "Extrair tempo", "Separar data, hora, mês, dia e período.", C.amber);
  step(slide, ctx, 536, 196, 4, "Gerar dimensões", "Tempo, loja e produto com valores únicos.", C.coral);
  step(slide, ctx, 536, 306, 5, "Montar fato", "Chaves mais medidas e transacao_id.", C.green);
  step(slide, ctx, 536, 416, 6, "Validar", "A fato precisa ter 149.116 linhas.", C.teal);
  ctx.addText(slide, { x: 174, y: 574, w: 932, h: 34, text: "Só passem para o PostgreSQL depois que os CSVs finais estiverem coerentes.", fontSize: 18, bold: true, color: C.ink, align: "center" });
  footer(slide, ctx, 7);
  return slide;
}
""",
    "slide-08.mjs": r"""
import { base, footer, step, card, C } from "./common.mjs";

export async function slide08(presentation, ctx) {
  const slide = presentation.slides.add();
  base(slide, ctx, "PostgreSQL", "A ordem importa: dimensões entram antes da fato");
  step(slide, ctx, 76, 196, 1, "Criar banco", "coffee_shop_dw e schema coffee_dw.", C.teal);
  step(slide, ctx, 76, 296, 2, "Criar tabelas", "dimensões, fato, PKs, FKs e índices.", C.blue);
  step(slide, ctx, 76, 396, 3, "Carregar dados", "primeiro dimensões, depois fato_vendas.", C.amber);
  step(slide, ctx, 76, 496, 4, "Criar views", "receita mensal, demanda horária e ranking.", C.coral);
  card(slide, ctx, 690, 218, 410, 118, "View 1", "Receita mensal por loja e categoria: mostra receita, quantidade, preço médio e transações.", C.teal);
  card(slide, ctx, 690, 372, 410, 118, "View 2", "Demanda por hora e produto: mostra picos por dia, hora, loja, categoria e tipo de produto.", C.blue);
  footer(slide, ctx, 8);
  return slide;
}
""",
    "slide-09.mjs": r"""
import { base, footer, card, check, C } from "./common.mjs";

export async function slide09(presentation, ctx) {
  const slide = presentation.slides.add();
  base(slide, ctx, "Validações", "O projeto precisa provar que os dados carregaram certo");
  card(slide, ctx, 78, 196, 312, 126, "Linhas", "fato_vendas deve ter 149.116 registros, igual ao dataset original.", C.teal);
  card(slide, ctx, 462, 196, 312, 126, "Receita", "Toda linha deve obedecer: receita = quantidade * preco_unitario.", C.blue);
  card(slide, ctx, 846, 196, 312, 126, "Dimensões", "dim_loja deve ter 3 lojas e dim_produto deve ter 80 produtos.", C.amber);
  check(slide, ctx, 150, 402, "As views devem retornar resultados e não podem ficar vazias.", C.coral, 900);
  check(slide, ctx, 150, 456, "Não pode existir chave na fato sem correspondência nas dimensões.", C.teal, 900);
  check(slide, ctx, 150, 510, "Guardem prints ou resultados das consultas para justificar a implementação.", C.blue, 900);
  footer(slide, ctx, 9);
  return slide;
}
""",
    "slide-10.mjs": r"""
import { base, footer, card, C } from "./common.mjs";

export async function slide10(presentation, ctx) {
  const slide = presentation.slides.add();
  base(slide, ctx, "EDA", "A análise exploratória precisa cobrir métricas e gráficos obrigatórios");
  card(slide, ctx, 74, 190, 338, 146, "Métricas gerais", "Receita total, itens vendidos, número de lojas, produtos, categorias, loja líder, categoria líder e horário de pico.", C.teal);
  card(slide, ctx, 470, 190, 338, 146, "Distribuição", "Quantidade por transação, preço unitário, receita por transação ou distribuição por horário.", C.blue);
  card(slide, ctx, 866, 190, 338, 146, "Comparação", "Receita por loja, receita por categoria, quantidade por categoria ou receita por tipo de produto.", C.amber);
  card(slide, ctx, 272, 404, 338, 146, "Evolução temporal", "Receita mensal de janeiro a junho para mostrar crescimento, queda ou variação no tempo.", C.coral);
  card(slide, ctx, 670, 404, 338, 146, "Extra forte", "Demanda por hora e loja. Esse gráfico sustenta decisões de equipe e estoque.", C.green);
  footer(slide, ctx, 10);
  return slide;
}
""",
    "slide-11.mjs": r"""
import { base, footer, card, check, C } from "./common.mjs";

export async function slide11(presentation, ctx) {
  const slide = presentation.slides.add();
  base(slide, ctx, "Machine Learning", "Transformem transações em previsão de demanda");
  card(slide, ctx, 72, 190, 326, 160, "Base agregada", "Agrupar por data, hora, loja, categoria e tipo de produto. Criar quantidade_vendida, receita, preço médio e transações.", C.teal);
  card(slide, ctx, 476, 190, 326, 160, "Classificação", "Target: alta_demanda. Definir alta demanda como quantidade vendida acima ou igual ao quartil 75.", C.blue);
  card(slide, ctx, 880, 190, 326, 160, "Regressão", "Target: quantidade_vendida. Usar Regressão Linear para prever demanda numérica.", C.amber);
  check(slide, ctx, 142, 430, "Separar treino e teste antes de avaliar qualquer modelo.", C.coral, 950);
  check(slide, ctx, 142, 482, "Aplicar one-hot encoding nas variáveis categóricas.", C.teal, 950);
  check(slide, ctx, 142, 534, "Padronizar variáveis numéricas quando necessário, especialmente para KNN e regressão logística.", C.blue, 950);
  footer(slide, ctx, 11);
  return slide;
}
""",
    "slide-12.mjs": r"""
import { base, footer, miniTable, card, C } from "./common.mjs";

export async function slide12(presentation, ctx) {
  const slide = presentation.slides.add();
  base(slide, ctx, "Comparação de modelos", "Mostrem métricas, escolham o melhor e expliquem o motivo");
  miniTable(slide, ctx, 90, 198, 430, [
    ["Modelo", "F1-score"],
    ["KNN", "0.5329"],
    ["Árvore de Decisão", "0.7143"],
    ["Random Forest", "0.6548"],
    ["Logistic Regression", "0.4915"],
  ]);
  card(slide, ctx, 594, 198, 500, 118, "Melhor classificador", "Árvore de Decisão: melhor F1-score. Ela captura regras combinadas de horário, loja e produto.", C.teal);
  card(slide, ctx, 594, 356, 500, 118, "Regressão Linear", "MAE 1.6091, RMSE 2.2356 e R² 0.2464. O desempenho limitado indica relações não lineares e variáveis ausentes.", C.coral);
  ctx.addText(slide, { x: 156, y: 554, w: 968, h: 40, text: "Resposta obrigatória: qual modelo foi melhor, por quê, e como os dados influenciaram o resultado.", fontSize: 18, bold: true, color: C.ink, align: "center" });
  footer(slide, ctx, 12);
  return slide;
}
""",
    "slide-13.mjs": r"""
import { base, footer, card, C } from "./common.mjs";

export async function slide13(presentation, ctx) {
  const slide = presentation.slides.add();
  base(slide, ctx, "Insights", "Cada insight precisa virar uma decisão de negócio");
  card(slide, ctx, 72, 190, 320, 116, "Hell's Kitchen lidera", "Priorizar estoque, equipe e disponibilidade dos produtos mais vendidos nessa loja.", C.blue);
  card(slide, ctx, 480, 190, 320, 116, "Pico às 10h", "Reforçar equipe e pré-preparo no período da manhã.", C.coral);
  card(slide, ctx, 888, 190, 320, 116, "Coffee lidera receita", "Tratar Coffee como categoria âncora do mix.", C.teal);
  card(slide, ctx, 272, 380, 320, 116, "Barista Espresso", "Usar como produto de receita e destaque em combos premium.", C.amber);
  card(slide, ctx, 688, 380, 320, 116, "Brewed Chai tea", "Usar como produto de alto giro para venda cruzada.", C.green);
  ctx.addText(slide, { x: 180, y: 574, w: 920, h: 30, text: "Evitem insight descritivo demais: sempre terminem com uma ação recomendada.", fontSize: 18, bold: true, color: C.ink, align: "center" });
  footer(slide, ctx, 13);
  return slide;
}
""",
    "slide-14.mjs": r"""
import { base, footer, card, C } from "./common.mjs";

export async function slide14(presentation, ctx) {
  const slide = presentation.slides.add();
  base(slide, ctx, "Divisão da fala", "Duas pessoas, uma narrativa só");
  card(slide, ctx, 112, 196, 430, 250, "Pessoa 1", "Objetivo do projeto, dataset, requisitos atendidos, modelagem dimensional, PostgreSQL, tabela fato, dimensões e views.\n\nTempo sugerido: 5 a 7 minutos.", C.teal);
  card(slide, ctx, 738, 196, 430, 250, "Pessoa 2", "Análise exploratória, gráficos, Machine Learning, comparação dos modelos, insights e recomendações finais.\n\nTempo sugerido: 5 a 7 minutos.", C.blue);
  ctx.addShape(slide, { x: 590, y: 258, w: 98, h: 98, geometry: "ellipse", fill: C.amber });
  ctx.addText(slide, { x: 590, y: 282, w: 98, h: 34, text: "10-15", fontSize: 23, bold: true, color: "#FFFFFF", align: "center" });
  ctx.addText(slide, { x: 590, y: 320, w: 98, h: 22, text: "minutos", fontSize: 11, bold: true, color: "#FFFFFF", align: "center" });
  ctx.addText(slide, { x: 180, y: 540, w: 920, h: 38, text: "Ambos participam da abertura, conclusão e perguntas do professor.", fontSize: 20, bold: true, color: C.ink, align: "center" });
  footer(slide, ctx, 14);
  return slide;
}
""",
    "slide-15.mjs": r"""
import { base, footer, check, C } from "./common.mjs";

export async function slide15(presentation, ctx) {
  const slide = presentation.slides.add();
  base(slide, ctx, "Checklist final", "Antes de entregar, passem por esta lista sem pular item");
  check(slide, ctx, 92, 186, "Dataset na pasta, notebook abre e scripts SQL estão organizados.", C.teal, 520);
  check(slide, ctx, 92, 238, "Banco criado, tabelas carregadas, views funcionando e validações conferidas.", C.blue, 520);
  check(slide, ctx, 92, 290, "Gráficos de distribuição, comparação e evolução temporal aparecem no notebook.", C.amber, 520);
  check(slide, ctx, 92, 342, "Todos os modelos obrigatórios foram treinados e avaliados.", C.coral, 520);
  check(slide, ctx, 92, 394, "Matriz de confusão, comparação dos modelos e regressão linear estão explicadas.", C.green, 520);
  check(slide, ctx, 92, 446, "3 a 5 insights têm decisão de negócio associada.", C.teal, 520);
  check(slide, ctx, 92, 498, "Slides prontos, fala dividida e apresentação ensaiada em 10 a 15 minutos.", C.blue, 520);
  ctx.addShape(slide, { x: 766, y: 234, w: 326, h: 226, fill: C.dark, line: ctx.line(C.dark, 0) });
  ctx.addText(slide, { x: 804, y: 278, w: 250, h: 76, text: "Conclusão", fontSize: 30, bold: true, color: "#FFFFFF", align: "center", typeface: ctx.fonts.title });
  ctx.addText(slide, { x: 800, y: 360, w: 260, h: 62, text: "DW organiza o dado, EDA revela padrões e ML transforma padrões em previsão.", fontSize: 16, color: "#E7EDF4", align: "center" });
  footer(slide, ctx, 15);
  return slide;
}
""",
}


def main() -> None:
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    LAYOUT_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (WORKSPACE / "profile-plan.txt").write_text(
        "task mode: create\n"
        "primary deck-profile: engineering-platform\n"
        "required proof objects: manual roadmap, checklist, star schema, SQL flow, EDA/ML plan, final delivery checklist\n"
        "QA gates: rendered previews, contact sheet, no overlap or text overflow\n",
        encoding="utf-8",
    )
    (WORKSPACE / "contact-sheet-plan.txt").write_text(
        "01 cover\n02 phase map\n03 requirements\n04 dataset validation\n05 business question\n06 star schema\n07 data preparation\n08 postgres flow\n09 SQL validation\n10 EDA\n11 ML setup\n12 model comparison\n13 insights\n14 speaking split\n15 final checklist\n",
        encoding="utf-8",
    )
    (SLIDES_DIR / "common.mjs").write_text(COMMON.strip() + "\n", encoding="utf-8")
    for name, content in SLIDES.items():
        (SLIDES_DIR / name).write_text(content.strip() + "\n", encoding="utf-8")
    print(WORKSPACE)


if __name__ == "__main__":
    main()
