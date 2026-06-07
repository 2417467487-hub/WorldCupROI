const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");

function loadPlaywright() {
  try {
    return require("playwright");
  } catch (error) {
    return require("E:/workspace/tools/npm-global/node_modules/@playwright/mcp/node_modules/playwright");
  }
}

const { chromium } = loadPlaywright();

const ROOT = path.resolve(__dirname, "..");
const DASHBOARD = path.join(ROOT, "dashboard", "panel_dashboard.html");
const FRAME_DIR = path.join(ROOT, "assets", "gifs", "static_preview_frames");
const CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe";
const EDGE = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe";
const ML_PYTHON = "E:/workspace/tools/ml-stack/.venv/Scripts/python.exe";

const PREVIEWS = [
  { tab: "Simulate", output: "scenario_simulation.gif" },
  { tab: "Predict", output: "risk_uncertainty.gif" },
  { tab: "Explain", output: "network_graph.gif" },
];

async function captureTab(page, preview) {
  await page.getByRole("button", { name: preview.tab }).click();
  await page.waitForFunction(
    () => document.querySelectorAll(".js-plotly-plot").length >= 2,
    null,
    { timeout: 20000 }
  );
  await page.evaluate(() => window.scrollTo(0, 240));
  await page.waitForTimeout(900);
  const frames = [];
  for (let i = 0; i < 3; i += 1) {
    await page.waitForTimeout(350);
    const framePath = path.join(FRAME_DIR, `${preview.output.replace(".gif", "")}_${i + 1}.png`);
    await page.screenshot({ path: framePath, fullPage: false });
    frames.push(framePath);
  }
  return frames;
}

function writeGif(frames, output) {
  const outGif = path.join(ROOT, "assets", "gifs", output);
  const py = [
    "from PIL import Image, ImageEnhance",
    "from pathlib import Path",
    `frames = [Path(r'''${frames.join("'''), Path(r'''")}''')]`,
    `out = Path(r'''${outGif}''')`,
    "images = []",
    "for idx, frame in enumerate(frames):",
    "    img = Image.open(frame).convert('RGB')",
    "    img.thumbnail((960, 540), Image.Resampling.LANCZOS)",
    "    canvas = Image.new('RGB', (960, 540), 'white')",
    "    canvas.paste(img, ((960 - img.width) // 2, 0))",
    "    images.append(canvas.convert('P', palette=Image.Palette.ADAPTIVE, colors=128))",
    "images[0].save(out, save_all=True, append_images=images[1:], duration=900, loop=0, optimize=True)",
    "print(out)",
  ].join("\n");
  const pyPath = path.join(FRAME_DIR, `_build_${output}.py`);
  fs.writeFileSync(pyPath, py, "utf-8");
  execFileSync(ML_PYTHON, [pyPath], { stdio: "inherit", cwd: ROOT });
}

async function main() {
  fs.rmSync(FRAME_DIR, { recursive: true, force: true });
  fs.mkdirSync(FRAME_DIR, { recursive: true });

  const executablePath = fs.existsSync(CHROME) ? CHROME : EDGE;
  const browser = await chromium.launch({ executablePath, headless: true });
  const page = await browser.newPage({ viewport: { width: 1365, height: 768 }, deviceScaleFactor: 1 });
  await page.goto(`file:///${DASHBOARD.replace(/\\/g, "/")}`, { waitUntil: "networkidle" });
  await page.waitForTimeout(1200);

  for (const preview of PREVIEWS) {
    const frames = await captureTab(page, preview);
    writeGif(frames, preview.output);
  }

  await browser.close();
  fs.rmSync(FRAME_DIR, { recursive: true, force: true });
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
