# laravel_dev_data

## What this is

**laravel_dev_data** is a simple internal tool for **collecting publicly available data of Laravel developers on GitHub**.

That’s it.

No research, no analytics, no complex processing — just **getting the data**.

---

## What the tool does

* Finds Laravel-related developers on GitHub
* Collects **public information only**, such as:

  * GitHub usernames
  * Profile links
  * Laravel-related repositories
  * Basic public metadata
* Saves the data in a usable format (CSV / JSON)

This tool does **not** access private data or bypass GitHub restrictions.

---

## Why it exists

The purpose of this tool is simply to:

* Build a list of Laravel developers
* Store their public GitHub data locally
* Use the data internally however you want

Nothing more.

---

## Scope

* Internal tool
* Straightforward data collection
* No analysis, scoring, or ranking

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/laravel_dev_data.git
cd laravel_dev_data
```

Install dependencies (adjust based on the stack used):

```bash
# example
pip install -r requirements.txt
# or
npm install
```

---

## Usage

Run the script:

```bash
# example
python main.py
```

After running, the collected data will be saved to the output files.

---

## Output

Typical output files:

* `laravel_devs.csv`
* `laravel_devs.json`

---

## Notes

* Uses **only public GitHub data**
* Respect GitHub rate limits and terms of service
* You are responsible for how you use the data

---

## License

MIT License — free to use, modify, and adapt.

---

## Disclaimer

This tool is provided as-is. It is meant for simple data collection and internal use.
