# ⚡ EV Charge Simulator – Interaktiv laddtidsberäkning för elbil

![Preview](assets/demo-preview.png) <!-- Byt till din GIF eller MP4-länk -->

## 🚗 Beskrivning

EV Charge Simulator är en interaktiv webbaserad simulator som är byggt med **Python/Dash**, där användaren kan experimentera med:

- Batteristorlek (kWh)
- Körsträcka enligt tillverkare (km)
- Laddartyp & effekt (kW, AC/DC)
- Verkningsgrad och laddbegränsning (%)
- Dynamisk simulering av körsträcka och laddtid

👁 Med grafisk feedback, batteriikoner och realtidsuppdateringar visualiserar appen både **teoretisk och praktisk laddtid** samt **aktuell körsträcka**.

---

## 🖥 Demo

🔗 [Live demo på Render](https://ev-charge-simulator.onrender.com)

---

## 🧰 Teknisk stack

| Komponent                        | Beskrivning                            |
|----------------------------------|----------------------------------------|
| [Dash](https://dash.plotly.com/) | Web framework (byggt på Flask + React) |
| Plotly Graph Objects             | För animerade linjediagram             |
| Bootstrap Components             | UI med `dash-bootstrap-components`     |
| Python 3.10+                     | Backendlogik och simulering            |
| HTML/CSS                         | Stil och layout                        |

---

## 📊 Funktioner

✅ Batterislider: 5–80 kWh  
✅ Räckviddsinput: dynamisk energieffektivitet (Wh/km)  
✅ Välj laddartyp (AC/DC) och effekt (3.7–350 kW)  
✅ Visuell batteriikon som uppdateras efter körsträcka  
✅ Linjediagram över körsträcka mot batterinivå  
✅ Automatisk beräkning av laddtid för vald sträcka  
✅ Responsiv layout i flexgrid  

---

## 🔧 Kör lokalt

```bash
git clone https://github.com/<ditt-användarnamn>/ev-charge-simulator.git
cd ev-charge-simulator
pip install -r requirements.txt
python main.py
