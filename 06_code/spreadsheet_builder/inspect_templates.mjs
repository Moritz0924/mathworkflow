import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const root = path.resolve(import.meta.dirname, "..", "..");
const outputDir = path.join(root, "07_results", "result_freeze_validation", "template_previews");
const templates = [
  ["result1", path.join(root, "03_data", "raw", "result1.xlsx"), "A1:J6"],
  ["result2", path.join(root, "03_data", "raw", "result2.xlsx"), "A1:J6"],
  ["result3", path.join(root, "03_data", "raw", "result3.xlsx"), "A1:L18"],
];

await fs.mkdir(outputDir, { recursive: true });
for (const [name, source, range] of templates) {
  const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(source));
  const inspection = await workbook.inspect({
    kind: "table",
    range: `Sheet1!${range}`,
    include: "values,formulas",
    tableMaxRows: 20,
    tableMaxCols: 14,
  });
  console.log(`## ${name}`);
  console.log(inspection.ndjson);
  const preview = await workbook.render({ sheetName: "Sheet1", range, autoCrop: "all", scale: 2, format: "png" });
  await fs.writeFile(path.join(outputDir, `${name}.png`), new Uint8Array(await preview.arrayBuffer()));
}
