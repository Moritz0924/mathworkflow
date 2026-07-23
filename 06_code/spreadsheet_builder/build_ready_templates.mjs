import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const root = path.resolve(import.meta.dirname, "..", "..");
const readyRoot = path.join(root, "07_results", "ready_for_freeze");
const previewRoot = path.join(readyRoot, "template_previews");
const inputs = JSON.parse(await fs.readFile(path.join(readyRoot, "template_inputs.json"), "utf8"));

const number = (value) => (value === "" || value === null || value === undefined ? null : Number(value));
const used = (row) => String(row.is_used) === "1";

function matchCount(ndjson) {
  return ndjson.trim().split("\n").filter(Boolean).reduce((count, line) => {
    const payload = JSON.parse(line);
    if (Array.isArray(payload.matches)) return count + payload.matches.length;
    if (Array.isArray(payload.results)) return count + payload.results.length;
    return count + Number(payload.matchCount || 0);
  }, 0);
}

function setValues(sheet, address, values) {
  sheet.getRange(address).values = [values];
}

function clear(sheet, address) {
  sheet.getRange(address).clear({ applyTo: "contents" });
}

function populateQ3(sheet, rows) {
  for (const row of rows) {
    const targetRow = Number(row.bomb_id) + 1;
    if (!used(row)) {
      clear(sheet, `A${targetRow}:B${targetRow}`);
      clear(sheet, `D${targetRow}:J${targetRow}`);
      continue;
    }
    setValues(sheet, `A${targetRow}:J${targetRow}`, [
      number(row.heading_deg), number(row.speed_mps), Number(row.bomb_id),
      number(row.release_x_m), number(row.release_y_m), number(row.release_z_m),
      number(row.detonation_x_m), number(row.detonation_y_m), number(row.detonation_z_m),
      number(row.effective_duration_s),
    ]);
  }
}

function populateQ4(sheet, rows) {
  const rowByUav = { FY1: 2, FY2: 3, FY3: 4 };
  for (const row of rows) {
    const targetRow = rowByUav[row.uav_id];
    if (!used(row)) {
      clear(sheet, `B${targetRow}:J${targetRow}`);
      continue;
    }
    setValues(sheet, `B${targetRow}:J${targetRow}`, [
      number(row.heading_deg), number(row.speed_mps),
      number(row.release_x_m), number(row.release_y_m), number(row.release_z_m),
      number(row.detonation_x_m), number(row.detonation_y_m), number(row.detonation_z_m),
      number(row.effective_duration_s),
    ]);
  }
}

function populateQ5(sheet, rows) {
  for (const row of rows) {
    const targetRow = 2 + (Number(String(row.uav_id).replace("FY", "")) - 1) * 3 + Number(row.bomb_id) - 1;
    if (!used(row)) {
      clear(sheet, `B${targetRow}:C${targetRow}`);
      clear(sheet, `E${targetRow}:L${targetRow}`);
      continue;
    }
    setValues(sheet, `B${targetRow}:L${targetRow}`, [
      number(row.heading_deg), number(row.speed_mps), Number(row.bomb_id),
      number(row.release_x_m), number(row.release_y_m), number(row.release_z_m),
      number(row.detonation_x_m), number(row.detonation_y_m), number(row.detonation_z_m),
      number(row.effective_duration_s), row.missile_id,
    ]);
  }
}

const jobs = [
  { questionId: "Q3", input: "result1.xlsx", output: "result1.xlsx", range: "A1:J6", populate: populateQ3 },
  { questionId: "Q4", input: "result2.xlsx", output: "result2.xlsx", range: "A1:J6", populate: populateQ4 },
  { questionId: "Q5", input: "result3.xlsx", output: "result3.xlsx", range: "A1:L18", populate: populateQ5 },
];

await fs.mkdir(readyRoot, { recursive: true });
await fs.mkdir(previewRoot, { recursive: true });
const verification = [];
for (const job of jobs) {
  const source = path.join(root, "03_data", "raw", job.input);
  const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(source));
  const sheet = workbook.worksheets.getItem("Sheet1");
  job.populate(sheet, inputs[job.questionId]);

  const inspection = await workbook.inspect({
    kind: "table",
    range: `Sheet1!${job.range}`,
    include: "values,formulas",
    tableMaxRows: 20,
    tableMaxCols: 14,
  });
  const errors = await workbook.inspect({
    kind: "match",
    searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
    options: { useRegex: true, maxResults: 50 },
    summary: `${job.questionId} formula error scan`,
  });
  const preview = await workbook.render({ sheetName: "Sheet1", range: job.range, autoCrop: "all", scale: 2, format: "png" });
  await fs.writeFile(path.join(previewRoot, `${job.questionId.toLowerCase()}_ready.png`), new Uint8Array(await preview.arrayBuffer()));
  const output = await SpreadsheetFile.exportXlsx(workbook);
  await output.save(path.join(readyRoot, job.output));
  verification.push({
    question_id: job.questionId,
    template: job.output,
    range: job.range,
    inspection: JSON.parse(inspection.ndjson),
    formula_error_matches: errors.ndjson ? matchCount(errors.ndjson) : 0,
  });
}
await fs.writeFile(
  path.join(readyRoot, "template_mapping_verification.json"),
  JSON.stringify({ status: "ready", generated_by: "artifact-tool", verification }, null, 2) + "\n",
  "utf8",
);
