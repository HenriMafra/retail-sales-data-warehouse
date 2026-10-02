from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "outputs" / "manual-coffee-shop-sales" / "presentations" / "coffee-shop-sales"
SLIDES_DIR = WORKSPACE / "slides"
PREVIEW_DIR = WORKSPACE / "preview"
LAYOUT_DIR = WORKSPACE / "layout"
QA_DIR = WORKSPACE / "qa"
OUTPUT_DIR = ROOT / "slides"


COMMON = r"""
import fs from "node:fs";
import path from "node:path";

export const ROOT = path.resolve(process.cwd());
export const metrics = JSON.parse(fs.readFileSync(path.join(ROOT, "reports", "metrics.json"), "utf8"));

export const C = {
  ink: "#18212F",
  muted: "#5B6472",
  light: "#F7F9FB",
  panel: "#FFFFFF",
  line: "#DCE3EA",
  teal: "#0E7C7B",
  blue: "#3563E9",
  amber: "#D99028",
  coral: "#D75A4A",
  green: "#2E7D32",
  dark: "#14213D",
};

export function img(rel) {
  return path.join(ROOT, rel);
}

export function bg(slide, ctx, kicker, title) {
  ctx.addShape(slide, { x: 0, y: 0, w: ctx.W, h: ctx.H, fill: C.light });
  ctx.addText(slide, {
    x: 54,
    y: 28,
    w: 500,
    h: 24,
    text: kicker.toUpperCase(),
    fontSize: 12,
    bold: true,
    color: C.teal,
    typeface: ctx.fonts.body,
  });
  ctx.addText(slide, {
    x: 54,
    y: 58,
    w: 900,
    h: 88,
    text: title,
    fontSize: 30,
    bold: true,
    color: C.ink,
    typeface: ctx.fonts.title,
  });
  ctx.addShape(slide, { x: 54, y: 148, w: 1168, h: 1.5, fill: C.line });
}

export function footer(slide, ctx, page) {
  ctx.addText(slide, {
    x: 54,
    y: 684,
    w: 800,
    h: 22,
    text: "Coffee Shop Sales | Data Warehouse + Machine Learning",
    fontSize: 10,
    color: C.muted,
  });
  ctx.addText(slide, {
    x: 1170,
    y: 684,
    w: 52,
    h: 22,
    text: String(page).padStart(2, "0"),
    fontSize: 10,
    color: C.muted,
    align: "right",
  });
}

export function pill(slide, ctx, x, y, text, color = C.teal) {
  ctx.addShape(slide, {
    x,
    y,
    w: 118,
    h: 28,
    geometry: "roundRect",
    fill: color,
    line: ctx.line("#00000000", 0),
  });
  ctx.addText(slide, {
    x: x + 12,
    y: y + 5,
    w: 94,
    h: 18,
    text,
    fontSize: 10,
    bold: true,
    color: "#FFFFFF",
    align: "center",
    valign: "mid",
  });
}

export function metric(slide, ctx, x, y, w, value, label, color = C.teal) {
  ctx.addShape(slide, { x, y, w, h: 92, fill: C.panel, line: ctx.line(C.line, 1) });
  ctx.addText(slide, {
    x: x + 18,
    y: y + 16,
    w: w - 36,
    h: 36,
    text: value,
    fontSize: 25,
    bold: true,
    color,
    typeface: ctx.fonts.title,
  });
  ctx.addText(slide, {
    x: x + 18,
    y: y + 54,
    w: w - 36,
    h: 26,
    text: label,
    fontSize: 12,
    color: C.muted,
  });
}

export function note(slide, ctx, x, y, w, h, title, body, color = C.teal) {
  ctx.addShape(slide, { x, y, w, h, fill: C.panel, line: ctx.line(C.line, 1) });
  ctx.addShape(slide, { x, y, w: 5, h, fill: color });
  ctx.addText(slide, {
    x: x + 18,
    y: y + 14,
    w: w - 34,
    h: 24,
    text: title,
    fontSize: 15,
    bold: true,
    color: C.ink,
  });
  ctx.addText(slide, {
    x: x + 18,
    y: y + 42,
    w: w - 34,
    h: h - 52,
    text: body,
    fontSize: 12,
    color: C.muted,
  });
}

export function bullet(slide, ctx, x, y, text, color = C.teal) {
  ctx.addShape(slide, { x, y: y + 7, w: 7, h: 7, geometry: "ellipse", fill: color });
  ctx.addText(slide, { x: x + 18, y, w: 450, h: 34, text, fontSize: 14, color: C.ink });
}

export async function chart(slide, ctx, rel, x, y, w, h) {
  await ctx.addImage(slide, { path: img(rel), x, y, w, h, fit: "contain", alt: rel });
}
"""


SLIDES = {
    "slide-01.mjs": r"""
import { C, metric, footer, metrics } from "./common.mjs";

export async function slide01(presentation, ctx) {
  const slide = presentation.slides.add();
  ctx.addShape(slide, { x: 0, y: 0, w: ctx.W, h: ctx.H, fill: "#F7F9FB" });
  ctx.addShape(slide, { x: 0, y: 0, w: 402, h: ctx.H, fill: C.dark });
  ctx.addText(slide, { x: 54, y: 58, w: 286, h: 26, text: "PROJETO FINAL", fontSize: 12, bold: true, color: "#8FD8D2" });
  ctx.addText(slide, { x: 54, y: 104, w: 306, h: 124, text: "Coffee Shop Sales", fontSize: 44, bold: true, color: "#FFFFFF", typeface: ctx.fonts.title });
  ctx.addText(slide, { x: 54, y: 254, w: 286, h: 96, text: "Data Warehouse + Machine Learning aplicado a vendas de cafeteria.", fontSize: 18, color: "#DFE7EF" });
  ctx.addText(slide, { x: 452, y: 84, w: 650, h: 92, text: "Da modelagem dimensional ao insight de negócio", fontSize: 32, bold: true, color: C.ink, typeface: ctx.fonts.title });
  ctx.addText(slide, { x: 452, y: 184, w: 694, h: 50, text: "Dataset público Maven Analytics / Kaggle com transações de três lojas entre janeiro e junho de 2023.", fontSize: 16, color: C.muted });
  metric(slide, ctx, 452, 286, 172, "149.116", "registros", C.teal);
  metric(slide, ctx, 646, 286, 172, "$698,8k", "receita total", C.blue);
  metric(slide, ctx, 840, 286, 172, "214.470", "itens vendidos", C.amber);
  metric(slide, ctx, 1034, 286, 172, "3", "lojas", C.coral);
  ctx.addShape(slide, { x: 452, y: 444, w: 754, h: 1.5, fill: C.line });
  ctx.addText(slide, { x: 452, y: 472, w: 338, h: 82, text: `Loja lider: ${metrics.business.top_store.name}`, fontSize: 24, bold: true, color: C.ink, typeface: ctx.fonts.title });
  ctx.addText(slide, { x: 810, y: 472, w: 360, h: 82, text: `Pico de demanda: ${metrics.business.peak_hour.hour}h`, fontSize: 24, bold: true, color: C.ink, typeface: ctx.fonts.title });
  ctx.addText(slide, { x: 452, y: 562, w: 700, h: 46, text: "Pergunta central: quais fatores explicam maior receita e maior demanda por loja, produto, mês, dia da semana e horário?", fontSize: 15, color: C.muted });
  footer(slide, ctx, 1);
  return slide;
}
""",
    "slide-02.mjs": r"""
import { bg, C, footer, metric, note, metrics } from "./common.mjs";

export async function slide02(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, "Dataset", "A base atende aos requisitos e oferece boa leitura operacional");
  metric(slide, ctx, 62, 172, 190, "149.116", "mínimo exigido: 10.000", C.teal);
  metric(slide, ctx, 276, 172, 190, "11", "colunas originais", C.blue);
  metric(slide, ctx, 490, 172, 190, "80", "produtos", C.amber);
  metric(slide, ctx, 704, 172, 190, "9", "categorias", C.coral);
  metric(slide, ctx, 918, 172, 190, "181", "dias de operação", C.green);
  note(slide, ctx, 64, 318, 346, 168, "Variáveis numéricas", "transaction_qty, unit_price, store_id, product_id e transaction_id permitem medidas, chaves e validações.", C.blue);
  note(slide, ctx, 444, 318, 346, 168, "Variáveis categóricas", "store_location, product_category, product_type e product_detail sustentam dimensões e comparações.", C.teal);
  note(slide, ctx, 824, 318, 346, 168, "Variáveis temporais", "transaction_date e transaction_time permitem evolução mensal, dia da semana e análise por hora.", C.amber);
  ctx.addText(slide, { x: 64, y: 538, w: 990, h: 42, text: "Fonte: Maven Analytics Data Playground / Kaggle. A Maven Roasters é fictícia, mas o dataset é público e adequado para prática analítica.", fontSize: 14, color: C.muted });
  footer(slide, ctx, 2);
  return slide;
}
""",
    "slide-03.mjs": r"""
import { bg, C, footer } from "./common.mjs";

function box(slide, ctx, x, y, w, h, title, rows, color) {
  ctx.addShape(slide, { x, y, w, h, fill: "#FFFFFF", line: ctx.line(color, 2) });
  ctx.addShape(slide, { x, y, w, h: 34, fill: color });
  ctx.addText(slide, { x: x + 14, y: y + 8, w: w - 28, h: 20, text: title, fontSize: 13, bold: true, color: "#FFFFFF" });
  rows.forEach((row, i) => {
    ctx.addText(slide, { x: x + 16, y: y + 52 + i * 28, w: w - 32, h: 22, text: row, fontSize: 12, color: C.ink });
  });
}

export async function slide03(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, "Modelagem dimensional", "Star schema simples, explicável e aderente ao enunciado");
  box(slide, ctx, 430, 258, 360, 210, "fato_vendas", ["venda_key", "transacao_id (degenerada)", "tempo_key, loja_key, produto_key", "quantidade", "preco_unitario", "receita"], C.dark);
  box(slide, ctx, 72, 176, 275, 190, "dim_tempo", ["data e hora", "ano, mes, trimestre", "dia da semana", "periodo do dia"], C.teal);
  box(slide, ctx, 872, 176, 275, 190, "dim_loja", ["localizacao", "cidade e pais", "rede", "tipo_loja"], C.blue);
  box(slide, ctx, 72, 468, 275, 162, "dim_produto", ["categoria", "tipo_produto", "detalhe_produto", "faixa_preco"], C.amber);
  box(slide, ctx, 872, 468, 275, 162, "Views", ["receita mensal", "demanda horaria", "ranking produtos"], C.coral);
  ctx.addShape(slide, { x: 347, y: 268, w: 83, h: 3, fill: C.line });
  ctx.addShape(slide, { x: 790, y: 268, w: 82, h: 3, fill: C.line });
  ctx.addShape(slide, { x: 347, y: 548, w: 83, h: 3, fill: C.line });
  ctx.addShape(slide, { x: 790, y: 548, w: 82, h: 3, fill: C.line });
  ctx.addText(slide, { x: 424, y: 522, w: 378, h: 44, text: "Grão da fato: uma linha por item vendido em uma transação.", fontSize: 15, bold: true, color: C.ink, align: "center" });
  footer(slide, ctx, 3);
  return slide;
}
""",
    "slide-04.mjs": r"""
import { bg, C, footer, note } from "./common.mjs";

export async function slide04(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, "PostgreSQL", "Scripts organizados para criar banco, carregar DW e validar resultados");
  const steps = [
    ["00", "create_database", "Cria coffee_shop_dw"],
    ["01", "schema_dw", "Cria dimensões, fato, chaves e índices"],
    ["02", "load_dw", "Carrega CSVs processados via psql \\copy"],
    ["03", "views_analiticas", "Cria views de análise obrigatórias"],
    ["04", "quality_checks", "Confere linhas, receita e amostras"],
  ];
  steps.forEach((s, i) => {
    const x = 82 + i * 218;
    ctx.addShape(slide, { x, y: 190, w: 164, h: 164, geometry: "ellipse", fill: i % 2 ? C.blue : C.teal });
    ctx.addText(slide, { x: x + 38, y: 222, w: 88, h: 40, text: s[0], fontSize: 28, bold: true, color: "#FFFFFF", align: "center" });
    ctx.addText(slide, { x: x + 18, y: 270, w: 128, h: 36, text: s[1], fontSize: 12, bold: true, color: "#FFFFFF", align: "center" });
    ctx.addText(slide, { x: x - 20, y: 382, w: 204, h: 48, text: s[2], fontSize: 13, color: C.ink, align: "center" });
    if (i < steps.length - 1) ctx.addShape(slide, { x: x + 168, y: 270, w: 44, h: 3, fill: C.line });
  });
  note(slide, ctx, 84, 498, 500, 94, "Views obrigatórias", "Receita mensal por loja e categoria; demanda por dia, hora, loja e produto.", C.amber);
  note(slide, ctx, 650, 498, 500, 94, "Validações", "A fato mantém 149.116 linhas e a fórmula receita = quantidade * preço unitário é conferida.", C.coral);
  footer(slide, ctx, 4);
  return slide;
}
""",
    "slide-05.mjs": r"""
import { bg, C, footer, chart, note, metrics } from "./common.mjs";

export async function slide05(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, "EDA temporal", "A receita acelera no segundo trimestre, com junho como melhor mês");
  await chart(slide, ctx, metrics.figures.revenue_by_month, 78, 176, 720, 414);
  note(slide, ctx, 850, 182, 310, 104, "Junho lidera", "A receita total chega a $166,485.88, acima de todos os meses anteriores.", C.blue);
  note(slide, ctx, 850, 320, 310, 104, "Sazonalidade visível", "O crescimento entre abril, maio e junho sugere aumento de tráfego ou maturação operacional.", C.teal);
  note(slide, ctx, 850, 458, 310, 104, "Decisão", "Planejar estoque e escala usando mês, dia da semana e hora como chaves de previsão.", C.amber);
  footer(slide, ctx, 5);
  return slide;
}
""",
    "slide-06.mjs": r"""
import { bg, C, footer, chart, note, metrics } from "./common.mjs";

export async function slide06(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, "Lojas e categorias", "Receita se concentra em Hell's Kitchen e na categoria Coffee");
  await chart(slide, ctx, metrics.figures.revenue_by_store, 62, 172, 520, 390);
  await chart(slide, ctx, metrics.figures.revenue_by_category, 640, 172, 520, 390);
  note(slide, ctx, 86, 578, 450, 82, "Loja líder", "Hell's Kitchen soma $236,511.17 em receita.", C.blue);
  note(slide, ctx, 664, 578, 450, 82, "Categoria líder", "Coffee soma $269,952.45 e sustenta o mix.", C.teal);
  footer(slide, ctx, 6);
  return slide;
}
""",
    "slide-07.mjs": r"""
import { bg, C, footer, chart, note, metrics } from "./common.mjs";

export async function slide07(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, "Demanda horária", "O pico de operação acontece pela manhã, principalmente às 10h");
  await chart(slide, ctx, metrics.figures.hourly_demand_by_store, 70, 170, 760, 430);
  note(slide, ctx, 872, 184, 284, 106, "Pico", `${metrics.business.peak_hour.quantity.toLocaleString("pt-BR")} itens vendidos às ${metrics.business.peak_hour.hour}h.`, C.coral);
  note(slide, ctx, 872, 326, 284, 106, "Operação", "A escala de equipe deve priorizar abertura e meio da manhã.", C.teal);
  note(slide, ctx, 872, 468, 284, 106, "Estoque", "Produtos de alto giro precisam estar prontos antes do pico.", C.amber);
  footer(slide, ctx, 7);
  return slide;
}
""",
    "slide-08.mjs": r"""
import { bg, C, footer, note, metric } from "./common.mjs";

export async function slide08(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, "Machine Learning", "A formulação mais defensável é prever demanda, não adivinhar produto");
  metric(slide, ctx, 72, 180, 214, "68.469", "linhas agregadas para ML", C.teal);
  metric(slide, ctx, 316, 180, 214, "Q75", "limiar de alta demanda", C.blue);
  metric(slide, ctx, 560, 180, 214, "9", "variáveis preditoras", C.amber);
  metric(slide, ctx, 804, 180, 214, "5", "modelos avaliados", C.coral);
  note(slide, ctx, 84, 340, 316, 150, "Classificação", "Target: alta_demanda. A classe positiva representa combinações loja-produto-hora acima do quartil 75 de quantidade vendida.", C.teal);
  note(slide, ctx, 452, 340, 316, 150, "Regressão", "Target: quantidade_vendida. A Regressão Linear testa se relações simples explicam a demanda agregada.", C.blue);
  note(slide, ctx, 820, 340, 316, 150, "Features", "Hora, mês, dia, fim de semana, preço médio, loja, categoria e tipo de produto.", C.amber);
  ctx.addText(slide, { x: 86, y: 558, w: 1010, h: 36, text: "Modelos: KNN, Árvore de Decisão, Random Forest, Logistic Regression e Regressão Linear.", fontSize: 18, bold: true, color: C.ink, align: "center" });
  footer(slide, ctx, 8);
  return slide;
}
""",
    "slide-09.mjs": r"""
import { bg, C, footer, chart, note, metrics } from "./common.mjs";

export async function slide09(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, "Comparação de modelos", "Árvore de Decisão vence por F1-score no recorte testado");
  await chart(slide, ctx, metrics.figures.model_comparison, 58, 172, 520, 342);
  await chart(slide, ctx, metrics.figures.confusion_matrix, 628, 172, 460, 342);
  note(slide, ctx, 80, 552, 310, 80, "Melhor modelo", `Árvore de Decisão: accuracy ${metrics.best_classification_model.accuracy}, precision ${metrics.best_classification_model.precision}, recall ${metrics.best_classification_model.recall}, F1 ${metrics.best_classification_model.f1}.`, C.teal);
  note(slide, ctx, 456, 552, 310, 80, "Por quê?", "Regras não lineares de horário, loja e produto explicam melhor a demanda do que uma fronteira linear.", C.blue);
  note(slide, ctx, 832, 552, 310, 80, "Limite", `Regressão Linear teve R² ${metrics.regression.r2}; faltam clima, feriados, campanhas e clientes.`, C.coral);
  footer(slide, ctx, 9);
  return slide;
}
""",
    "slide-10.mjs": r"""
import { bg, C, footer, bullet, note, metrics } from "./common.mjs";

export async function slide10(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, "Insights e decisões", "A análise vira ação quando orienta estoque, equipe e mix de produtos");
  bullet(slide, ctx, 84, 182, "Priorizar estoque e escala em Hell's Kitchen, a loja de maior receita.", C.blue);
  bullet(slide, ctx, 84, 236, `Preparar operação para o pico das ${metrics.business.peak_hour.hour}h, com ${metrics.business.peak_hour.quantity.toLocaleString("pt-BR")} itens vendidos no período.`, C.coral);
  bullet(slide, ctx, 84, 290, "Manter Coffee como categoria âncora e proteger disponibilidade dos itens principais.", C.teal);
  bullet(slide, ctx, 84, 344, "Usar Barista Espresso como produto de receita e Brewed Chai tea como produto de tráfego.", C.amber);
  bullet(slide, ctx, 84, 398, "Criar combos e promoções para horários de menor movimento e produtos de menor giro.", C.green);
  note(slide, ctx, 720, 188, 366, 132, "Próximo passo analítico", "Adicionar clima, feriados, promoções e dados de cliente para melhorar a previsão de demanda.", C.teal);
  note(slide, ctx, 720, 356, 366, 132, "Mensagem final", "O DW organiza o dado; a EDA explica padrões; o ML transforma padrões em previsão operacional.", C.blue);
  ctx.addShape(slide, { x: 720, y: 542, w: 366, h: 2, fill: C.line });
  ctx.addText(slide, { x: 720, y: 558, w: 366, h: 58, text: "Entrega: SQL + Notebook + Slides + Relatório", fontSize: 20, bold: true, color: C.ink, align: "center" });
  footer(slide, ctx, 10);
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
        "required proof objects: dataset metrics, star schema, SQL pipeline, EDA charts, ML comparison, insights\n"
        "source requirements: reports/metrics.json and reports/figures/*.png\n"
        "QA gates: rendered previews, contact sheet, no text overflow, all slide modules export one slide\n",
        encoding="utf-8",
    )
    (WORKSPACE / "contact-sheet-plan.txt").write_text(
        "01 cover with metric rail\n"
        "02 dataset requirement proof\n"
        "03 star schema diagram\n"
        "04 SQL execution flow\n"
        "05 time-series chart with insight rail\n"
        "06 paired category/store proof\n"
        "07 hourly demand chart with decision rail\n"
        "08 ML framing cards\n"
        "09 model comparison proof\n"
        "10 recommendation close\n",
        encoding="utf-8",
    )
    (SLIDES_DIR / "common.mjs").write_text(COMMON.strip() + "\n", encoding="utf-8")
    for name, content in SLIDES.items():
        (SLIDES_DIR / name).write_text(content.strip() + "\n", encoding="utf-8")
    print(WORKSPACE)


if __name__ == "__main__":
    main()
