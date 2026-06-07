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
const FRAME_DIR = path.join(ROOT, "assets", "gifs", "static_platform_frames");
const OUT_GIF = path.join(ROOT, "assets", "gifs", "static_platform_dashboard.gif");
const CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe";
const EDGE = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe";
const ML_PYTHON = "E:/workspace/tools/ml-stack/.venv/Scripts/python.exe";

async function main() {
  fs.rmSync(FRAME_DIR, { recursive: true, force: true });
  fs.mkdirSync(FRAME_DIR, { recursive: true });

  const executablePath = fs.existsSync(CHROME) ? CHROME : EDGE;
  const browser = await chromium.launch({ executablePath, headless: true });
  const page = await browser.newPage({ viewport: { width: 1365, height: 768 }, deviceScaleFactor: 1 });
  await page.goto(`file:///${DASHBOARD.replace(/\\/g, "/")}`, { waitUntil: "networkidle" });
  await page.waitForTimeout(1200);

  const tabs = ["Discover", "Explain", "Predict", "Simulate", "Recommend"];
  const frames = [];
  for (const [index, tab] of tabs.entries()) {
    await page.getByRole("button", { name: tab }).click();
    await page.waitForTimeout(900);
    const framePath = path.join(FRAME_DIR, `${String(index + 1).padStart(2, "0")}_${tab.toLowerCase()}.png`);
    await page.screenshot({ path: framePath, fullPage: false });
    frames.push(framePath);
  }
  await browser.close();

  const py = [
    "from PIL import Image",
    "from pathlib import Path",
    `frames = [Path(r'''${frames.join("'''), Path(r'''")}''')]`,
    `out = Path(r'''${OUT_GIF}''')`,
    "images = []",
    "for frame in frames:",
    "    img = Image.open(frame).convert('RGB')",
    "    img.thumbnail((960, 540), Image.Resampling.LANCZOS)",
    "    canvas = Image.new('RGB', (960, 540), 'white')",
    "    canvas.paste(img, ((960 - img.width) // 2, 0))",
    "    images.append(canvas.convert('P', palette=Image.Palette.ADAPTIVE, colors=128))",
    "images[0].save(out, save_all=True, append_images=images[1:], duration=1250, loop=0, optimize=True)",
    "print(out)",
  ].join("\n");
  const pyPath = path.join(FRAME_DIR, "_build_static_platform_gif.py");
  fs.writeFileSync(pyPath, py, "utf-8");
  execFileSync(ML_PYTHON, [pyPath], { stdio: "inherit", cwd: ROOT });
  fs.rmSync(FRAME_DIR, { recursive: true, force: true });
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
