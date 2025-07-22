
# 📑 pyBookmark-Link-Checker

A Python script that scans an exported bookmarks HTML file, checks the availability of each link, and outputs the results in a CSV file. It also logs the process and displays a progress bar.

## 🚀 What it does

✅ Parses a `Bookmarks.html` export file.  
✅ Checks each bookmarked URL for availability.  
✅ Detects:  
- `Alive`  
- `Dead`  
- `Login Required` (HTTP 401/403)  
- `Redirected`  
- `SSL Error`  

✅ Outputs:  
- `bookmark_check_results.csv` — summary of all bookmarks and their status.  
- `bookmark_check.log` — detailed log of the checking process.

## 🧰 Requirements

- Python **3.7+**
- Python packages:
  - `beautifulsoup4`
  - `requests`
  - `tqdm`

### Install requirements

Run:
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install beautifulsoup4 requests tqdm
```

## 📂 How to run

1️⃣ Place your `Bookmarks.html` export file somewhere accessible.  
2️⃣ Run the script:
```bash
python main.py
```
3️⃣ When prompted:
```
Enter path to Bookmarks.html:
```
Enter the full path to your bookmarks file.

4️⃣ Wait for the progress bar to complete.  
5️⃣ Check the output files in the same folder where you ran the script.

## 📄 Output files

✅ **bookmark_check_results.csv**  
✅ **bookmark_check.log**  

## 📝 Example: `bookmark_check_results.csv`

| Bookmark Name | URL | Status |
|---------------|-----|--------|
| Google | https://www.google.com | Alive |
| SomeSite | http://somesite.local | Dead |
| Internal Dashboard | http://intranet.company.local | Login Required |
| Redirect Example | http://oldsite.com | Redirected |
| Secure Site | https://badssl.com | SSL Error |

## 📝 Example: `bookmark_check.log`

```
2025-07-22 16:42:01 Starting bookmark check
2025-07-22 16:42:02 Checked: Google (https://www.google.com) - Alive
2025-07-22 16:42:03 Checked: SomeSite (http://somesite.local) - Dead
...
```

## 📌 Notes

- The script does not attempt to log in to protected sites — it just detects login prompts.
