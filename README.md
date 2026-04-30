# Warframe-Market-Riven-Dissolve-Finder

Scrapes Warframe Market rivens and identifies mods with either:

- high **Endo / Plat ratio**
- high **total Endo value**

Useful for finding rivens worth buying and dissolving for profit.

---

## 🧰 Setup Checklist

### ✅ 1. Install Python

Download Python 3 from the official website.

During installation:

- ☑️ Check **Add Python to PATH**
- Click **Install Now**

---

### ✅ 2. Verify Installation

Open Command Prompt and run:

```bash
python --version
```

You should see:

```bash
Python 3.x.x
```

---

### ✅ 3. Clone / Download Repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

Or download ZIP and extract manually.

---

### ✅ 4. Install Dependencies

```bash
pip install requests
```

---

### ✅ 5. Run Program

```bash
python standalone.py
```

---

# 🎮 Usage

## Main Commands

```text
1. ping
2. riven
3. sort
4. settings
5. exit
```

---

## Settings Menu

The settings menu controls all filters and saves them permanently to `settings.json`.

### Available Settings

### Preferred Status
Choose which sellers to include:

- ALL
- online
- ingame
- offline

---

### Randomize Stat List
Randomizes attribute search order to reduce consistent rate-limiting.

```text
True / False
```

---

### Minimum Endo/Plat
Only shows rivens above your chosen ratio.

Example:

```text
500
```

Only shows rivens with:

```text
Endo/Plat >= 500
```

---

### Request Mode

Controls API speed.

### fast
- 0.3–0.35 sec delay
- Faster
- May trigger rate limits

### safe
- 6–8 sec delay
- Much slower
- More complete results / fewer rate limits

Recommended:

- everyday scanning → `fast`
- full scan → `safe`

---

## Sorting

After running `riven`, you can sort results:

### Option 1: Endo / Plat
Best efficiency

### Option 2: Endo
Highest raw endo value

---

## Example Workflow

```text
settings
→ set status = ingame
→ set min endo/plat = 500
→ set request mode = safe

riven
sort
1
```

---

## Example settings.json

```json
{
    "prefered_status": "ingame",
    "min_endo_per_plat": 500.0,
    "randomize_stats": true,
    "request_mode": "safe"
}
```

---

## 📁 Required Files

Make sure these files are in the same folder:

```text
standalone.py
RivenMod.py
Settings.py
settings.json
scraped.txt
```

---

## ⚠️ Troubleshooting

### Error 429
You are being rate-limited by Warframe Market.

Solutions:
- enable randomize stat list
- switch request mode to `safe`

---

### Python not recognized

Reinstall Python and enable:

```text
Add Python to PATH
```

---

### Missing modules

Install dependencies:

```bash
pip install requests
```

---

### No results found

Your filters may be too strict.

Try lowering:

- minimum Endo/Plat
- seller status restrictions

---

## 💡 Optional (Windows)

Create `run.bat`

```bat
@echo off
python standalone.py
pause
```

Double-click to run.

---
