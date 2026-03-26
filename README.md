# State Plane to KML Converter

A simple Python tool that converts survey CSV files from any **NAD83 State Plane Coordinate System** zone into a **KML file** for viewing in Google Earth.

Supports 97 State Plane zones across the US.

---

## πΈ Demo

Drop in your CSV, pick your zone, and open the resulting `Survey_Points.kml` in Google Earth.

---

## π Requirements

- Python 3.8+
- pip

Install all dependencies with:

```bash
pip install pandas pyproj simplekml
```

---

## π How to Use

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/state-plane-to-kml.git
cd state-plane-to-kml
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Format your CSV**

Your CSV file should have **no header row** and five columns in this exact order:

| Column | Description |
|---|---|
| `point_name` | Name or ID of the survey point |
| `northing` | Northing value in US Survey Feet |
| `easting` | Easting value in US Survey Feet |
| `elevation` | Elevation in feet |
| `description` | Any notes or description |

Example row:
```
101,702345.123,2345678.456,125.50,Iron Pin Found
```

An example CSV is included in the `example/` folder.

**4. Run the script**
```bash
python survey_to_kml.py
```

**5. Pick your State Plane zone**

The script will display a numbered list of all available zones. Type the number for your zone and press Enter.

```
============================================================
  NAD83 State Plane Zone Selection
============================================================
    1. AR: Arkansas North          2. AR: Arkansas South
    3. AZ: Arizona Central (ft)    4. AZ: Arizona East (ft)
  ...
============================================================

Enter zone number (1β97):
```

**6. Grab your output files**

Two files will be saved in the same folder as the script:

- `Survey_Points.kml` β open this in Google Earth
- `Plotted_Data.csv` β your original data with latitude/longitude columns added

---

## π Project Structure

```
state-plane-to-kml/
βββ survey_to_kml.py      # Main script
βββ requirements.txt      # Python dependencies
βββ .gitignore
βββ README.md
βββ example/
    βββ example.csv       # Sample survey data to test with
```

---

## πΊοΈ Supported Zones

Zones are sourced from [proj.org](https://proj.org/en/stable/) and cover:

AR, AZ, CA, CO, CT, DE, FL, GA, IA, ID, IL, IN, KS, KY, LA, MA, MD, ME, MI, MN, MS, MT, NC, ND, NE, NH, NJ, NM, NV, NY, OH, OK, OR, PA, RI, SC, TN, TX, UT, VA, WA, WI, WY

---

## π License

MIT License β free to use, modify, and share.
