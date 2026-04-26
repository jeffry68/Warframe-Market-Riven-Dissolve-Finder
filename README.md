# Warframe-Market-Riven-Dissolve-Finder
scrapes through most of Warframe Market's available rivens to either find rivens with the highest endo / plat ratio or the highest total endo amount


## 🧰 Setup Checklist

### ✅ 1. Install Python

* Download Python 3 from the official website
* During install:

  * ☑️ Check **“Add Python to PATH”**
  * Click **Install Now**

---

### ✅ 2. Verify Installation

Open Command Prompt and run:

```
python --version
```

* You should see something like `Python 3.x.x`

---

### ✅ 3. Clone / Download This Repo

```
git clone <your-repo-url>
cd <your-repo-folder>
```

*or download ZIP and extract*

---

### ✅ 4. Install Dependencies

```
pip install requests python-dotenv
```

---

### ✅ 5. Run the Program

```
python main.py
```

---

## 🎮 Usage

### Commands:

```
riven                # fetch all rivens
riven ingame         # filter by ingame users
riven online         # filter by online users
sort                 # sort last results
exit                 # quit program
```

---

### Example:

```
riven ingame
sort
1   # sort by endo/plat
```

---

## ⚠️ Troubleshooting

### ❌ Python not recognized

* Reinstall Python and enable **Add to PATH**

### ❌ Missing modules

```
pip install requests python-dotenv
```

### ❌ No output / errors

* Make sure these files exist in the same folder:

  * `main.py`
  * `RivenMod.py`
  * `Settings.py`

---

## 💡 Optional (Windows)

Create `run.bat`:

```
@echo off
python main.py
pause
```

(Double-click to run)
