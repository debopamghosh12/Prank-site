from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# --- SERVER STATE ---
# True = Prank is Active (Admin wants to prank)
server_state = {"frozen": True}

# ==========================================
# 1. THE ULTIMATE PRANK PAGE
# ==========================================
prank_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>System Update 2.0</title>
    <style>
        /* Base Styles */
        body { margin: 0; background: #000; font-family: -apple-system, BlinkMacSystemFont, Roboto, sans-serif; overflow: hidden; user-select: none; -webkit-user-select: none; }
        
        /* SCREEN 1: The Start Button (Gets Audio Permission) */
        #start-screen {
            display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh;
            background: #000; color: white; text-align: center;
        }
        .install-btn {
            padding: 15px 40px; background: #2196F3; color: white; border: none; font-size: 18px; 
            border-radius: 25px; cursor: pointer; margin-top: 20px; font-weight: bold;
        }

        /* SCREEN 2: The Fake Update (Looks Legit) */
        #update-screen {
            display: none; flex-direction: column; justify-content: center; align-items: center;
            height: 100vh; color: white;
        }
        .loader {
            border: 4px solid #333; border-top: 4px solid #fff; border-radius: 50%;
            width: 50px; height: 50px; animation: spin 1s linear infinite; margin-bottom: 30px;
        }
        .progress-bar { width: 80%; height: 4px; background: #333; border-radius: 2px; margin-top: 20px; }
        .progress-fill { width: 0%; height: 100%; background: #4caf50; transition: width 0.5s; }
        
        /* SCREEN 3: The PANIC MODE (Red Flashing) */
        #panic-screen {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.98); flex-direction: column; justify-content: center; align-items: center;
            text-align: center; z-index: 99999;
        }
        .blink-red { animation: flash 0.1s infinite; }
        .warning-text { color: red; font-size: 2rem; font-weight: bold; text-shadow: 0 0 10px red; }
        
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @keyframes flash { 0% { background: #000; } 50% { background: #500; } 100% { background: #000; } }
    </style>
</head>
<body>

    <div id="start-screen" onclick="startUpdate()">
        <h2 style="font-weight: normal;">System Update 17.4</h2>
        <p style="color: #888; max-width: 80%;">Critical security patches available.</p>
        <button class="install-btn">INSTALL NOW</button>
    </div>

    <div id="update-screen" onclick="triggerPanic()">
        <div class="loader"></div>
        <h2 style="font-weight: normal;">Installing...</h2>
        <p style="color: #888; font-size: 12px;">Do not turn off device.</p>
        <div class="progress-bar"><div class="progress-fill" id="fill"></div></div>
        <p id="percent" style="margin-top: 10px; color: #888;">0%</p>
    </div>

    <div id="panic-screen" onclick="triggerPanic()">
        <div class="warning-text">⚠️ ERROR ⚠️</div>
        <p style="color: white; margin-top: 20px;">TOUCH DETECTED!</p>
        <p style="color: red; font-size: 12px;">SYSTEM CORRUPTED</p>
    </div>

    <script>
        let audioCtx;
        let oscillator;
        let progress = 0;
        let isPrankRunning = false;
        let inPanicMode = false;

        // --- PREVENT SCROLL & EXIT ---
        document.addEventListener('touchmove', function(e) { e.preventDefault(); }, { passive: false });
        window.onbeforeunload = function() { return "Update in progress!"; };

        // --- START FUNCTION ---
        function startUpdate() {
            // 1. UI Switch
            document.getElementById('start-screen').style.display = 'none';
            document.getElementById('update-screen').style.display = 'flex';
            
            // 2. Fullscreen & Back Trap
            if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
            history.pushState(null, null, location.href);
            window.onpopstate = function () {
                history.pushState(null, null, location.href);
                triggerPanic(); // Back button triggers panic too!
            };

            // 3. Init Audio (Silent first)
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            if (audioCtx.state === 'suspended') audioCtx.resume();
            
            isPrankRunning = true;
        }

        // --- THE PANIC TRIGGER (If touched) ---
        function triggerPanic() {
            if (!isPrankRunning) return;
            
            inPanicMode = true;
            document.getElementById('update-screen').style.display = 'none';
            document.getElementById('panic-screen').style.display = 'flex';
            document.getElementById('panic-screen').classList.add('blink-red');

            // Vibrate
            if(navigator.vibrate) navigator.vibrate([200, 50, 200, 50, 500]);
            
            // Play Siren
            playSiren();
            
            // Reset to "Normal Update" after 3 seconds (To confuse them)
            setTimeout(() => {
                inPanicMode = false;
                document.getElementById('panic-screen').style.display = 'none';
                document.getElementById('panic-screen').classList.remove('blink-red');
                document.getElementById('update-screen').style.display = 'flex';
                stopSiren();
            }, 3000);
        }

        // --- SOUND LOGIC ---
        function playSiren() {
            if (!audioCtx) return;
            oscillator = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            oscillator.connect(gain);
            gain.connect(audioCtx.destination);
            
            oscillator.type = 'sawtooth';
            oscillator.frequency.value = 800;
            oscillator.start();
            
            // Wee-Woo Effect
            window.sirenInterval = setInterval(() => {
                if(oscillator.frequency.value == 800) oscillator.frequency.value = 500;
                else oscillator.frequency.value = 800;
            }, 200);
        }

        function stopSiren() {
            if (oscillator) {
                oscillator.stop();
                clearInterval(window.sirenInterval);
                oscillator = null;
            }
        }

        // --- SERVER CONTROL LOOP ---
        setInterval(() => {
            fetch('/status')
                .then(res => res.json())
                .then(data => {
                    // Update Progress Bar if not in panic
                    if (isPrankRunning && !inPanicMode) {
                        if (data.frozen) {
                            if(progress < 95) progress += 0.5;
                        } else {
                            // Admin released it
                            document.body.innerHTML = "<h1 style='color:green;text-align:center;margin-top:50%'>Update Success ✅</h1>";
                            document.body.style.cursor = 'default';
                        }
                        document.getElementById('fill').style.width = progress + "%";
                        document.getElementById('percent').innerText = Math.floor(progress) + "%";
                    }
                });
        }, 1000);
    </script>
</body>
</html>
"""

# ==========================================
# 2. ADMIN PANEL
# ==========================================
admin_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #111; color: #0f0; font-family: monospace; text-align: center; padding-top: 50px; }
        button { padding: 20px; font-size: 20px; border: 2px solid #0f0; background: #000; color: #0f0; border-radius: 10px; cursor: pointer;}
    </style>
</head>
<body>
    <h1>CONTROL CENTER</h1>
    <h2 id="st">{{ state }}</h2>
    <button onclick="toggle()">TOGGLE PRANK</button>
    <script>
        function toggle() {
            fetch('/toggle', { method: 'POST' })
                .then(res => res.json())
                .then(data => document.getElementById('st').innerText = data.frozen ? "PRANK ACTIVE 😈" : "RELEASED ✅");
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(prank_html)

@app.route('/admin')
def admin():
    return render_template_string(admin_html, state="PRANK ACTIVE 😈" if server_state["frozen"] else "RELEASED ✅")

@app.route('/status')
def status():
    return jsonify(server_state)

@app.route('/toggle', methods=['POST'])
def toggle():
    server_state["frozen"] = not server_state["frozen"]
    return jsonify(server_state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)