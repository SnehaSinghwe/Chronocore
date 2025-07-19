## Chronocore
A real-time AI co-pilot for smart asset maintenance and decision intelligence.  ChronoCore is built from scratch, this system monitors assets in real time, detects anomalies, and suggests actionable recommendations through a simple Streamlit dashboard.

## Features
- Real-time sensor data simulation (fans, temperature)
- Smart AI Co-Pilot that:
  - Detects anomalies
  - Recommends actions (Generate Work Order, Send Alert)
  - Offers explainable logic based on system behavior
- Live feed updated every 5 seconds
- Built using Python + Streamlit, with modular architecture

## Why I Built This
I wanted to show how an intelligent system can go beyond prediction — and become a trusted, real-time assistant to engineers and technicians. ChronoCore reflects my passion for explainable, human-centered AI in real-world environments.

## Project Structure

ChronoCore/
├── app.py # Streamlit UI (AI co-pilot dashboard)
├── simulator.py # Real-time sensor simulator
├── data/
│ ├── live_feed.json 
│ └── history.json 
└── README.md 

## How to Run It

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ChronoCore.git
cd ChronoCore

2. Create a virtual environment and install dependencies
python -m venv .venv
.venv\Scripts\activate  # (Windows)

3. Run the simulator (in a separate terminal)
python simulator.py

4. Run the Streamlit dashboard
streamlit run app.py

Built With
Python 3.10+
Streamlit
Pandas
JSON

Author
Sneha Singh
Computer Science Engineer
LinkedIn: www.linkedin.com/in/sneha-singh246

🌀 License
This project is open-source and free to use for learning and demonstration purposes.
