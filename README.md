# 🧠 Distraction Monitor – AI-Powered Screen Activity Tracker

> **Detect YouTube Shorts & Instagram Reels automatically. Track your screen time and take control of your focus!**

A distraction monitoring tool built using AI + screen capture. Works on your local machine. Alerts you when you cross a limit!

---

## 🚀 Features

- ✅ Real-time screen monitoring using AI
- 🎯 Detects "Short", "Reel", or "Non-Short" screens
- ⏱️ Customizable threshold & scan interval
- 🔊 Sound + Notification alerts when threshold is reached
- 💡 Web dashboard with live counter
- 🔐 Runs entirely locally – no data leaves your machine

---

## 🧠 Tech Stack

- `TensorFlow` / `Keras` – AI Model
- `Flask` – Backend server
- `mss`, `PIL`, `NumPy` – Screen capture + preprocessing
- `HTML`, `CSS`, `JavaScript` – Frontend
- 📦 Folder-based deployment with no heavy dependencies

---

## 📁 Project Structure

See `file_structure.txt` for full layout.

---

## 🛠️ Setup Instructions

```bash
# 1. Clone the repo
git clone https://github.com/PRABHUSIDDARTH/distraction-monitor-v1.git
cd distraction-monitor-v1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place the model
# Download or train the file: 'distraction_meter_model.keras'
# And place it inside: model/distraction_meter_model.keras

# 4. Run the app
cd backend
python app.py



⚙️ How It Works
You set a threshold (number of shorts/reels you're allowed).

The app monitors your screen every few seconds.

If it detects YouTube Shorts or Reels, it counts them.

Once the count crosses your threshold, you get an alert!




⚠️ Notes
Works best on a single monitor setup.

for dual monitor change the monitor vale , value will be shown in detect monitor on windows.  #default primary monitor[1]

Model file (.keras) is excluded from this repo due to GitHub size limits.

you can get it in the assets

Model was trained on custom screenshots labeled as short, reel, and non_short.

🧾 License
This project is licensed under the MIT License.
You may use, modify, and distribute freely.

🙌 Credits
Built by Prabhu Siddarth during internship phase.
Feel free to ⭐ star this repo and share your feedback!


