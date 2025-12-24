from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# --- SERVER STATE (Memory) ---
# True = Freeze Mode ON
# False = Normal Mode
# Restart hole default 'True' thakbe
server_state = {"frozen": True}

# ==========================================
# 1. THE PRANK PAGE (For Friend/Victim)
# ==========================================
prank_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>System Critical Update</title>
    <style>
        /* General Styles */
        body { margin: 0; overflow: hidden; background: #000; font-family: 'Courier New', monospace; user-select: none; -webkit-user-select: none; }
        
        /* The Trap Button Screen (Safe Mode) */
        #safe { display: flex; height: 100vh; flex-direction: column; justify-content: center; align-items: center; color: white; text-align: center; background: #111; transition: opacity 0.2s;}
        .btn { padding: 15px 40px; background: #00ff00; color: black; border: none; font-size: 18px; font-weight: bold; border-radius: 5px; cursor: pointer; margin-top: 20px; box-shadow: 0 0 15px #00ff00; animation: pulse 1s infinite;}
        
        /* The SCARY Overlay (Panic Mode) */
        #overlay {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.98); color: red; flex-direction: column;
            justify-content: center; align-items: center; text-align: center; z-index: 99999;
            cursor: none; /* Mouse Gayeb for Laptop */
        }
        
        .blink { animation: b 0.1s infinite; font-size: 3rem; font-weight: bold; text-shadow: 0 0 20px red; }
        .virus-text { font-size: 1.2rem; color: white; margin-top: 20px; letter-spacing: 2px; }
        
        @keyframes b { 0% {opacity:1} 50% {opacity:0.2} 100% {opacity:1} }
        @keyframes pulse { 0% {transform: scale(1);} 50% {transform: scale(1.05);} 100% {transform: scale(1);} }
    </style>
</head>
<body>

    <div id="safe" onclick="startPrank()">
        <h1 style="color: #00ff00;">Security Check</h1>
        <p style="color: #ccc; max-width: 80%;">Please verify your device connection.</p>
        <button class="btn">CLICK TO VERIFY</button>
    </div>

    <div id="overlay">
        <div class="blink">⚠️ HACKED ⚠️</div>
        <div class="virus-text">SYSTEM FAILURE</div>
        <p style="color: red; font-size: 14px; margin-top: 30px;">DELETING ALL PHOTOS...</p>
        <p id="counter" style="color: white; font-size: 20px;">0%</p>
        <p style="color: grey; font-size: 10px; margin-top: 50px;">Device ID: LOCKED</p>
    </div>

    <script>
        let audioCtx;
        let oscillator;
        let isPlaying = false;
        let hasInteracted = false;

        // --- 1. PREVENT SCROLL & SWIPE GESTURES ---
        // Eta 'Pull to Refresh' ar 'Scroll' bondho korbe
        document.addEventListener('touchmove', function(e) {
            e.preventDefault();
        }, { passive: false });

        // --- 2. EXIT TRAP (Show Popup on Close) ---
        // Keu tab close ba swipe up korle browser warning debe
        window.onbeforeunload = function() {
            return "System Error: Cannot Close!";
        };

        // --- 3. ACTIVATION ---
        function startPrank() {
            if(hasInteracted) return;
            hasInteracted = true;

            // Go Fullscreen
            if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
            
            // Trap Back Button (History Loop)
            history.pushState(null, null, location.href);
            window.onpopstate = function () {
                history.pushState(null, null, location.href);
            };

            // Initialize Audio Context
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            
            document.getElementById('safe').innerHTML = "<h1 style='color:white'>Verifying...</h1>";
        }

        // --- 4. SOUND GENERATOR (Siren) ---
        function playAlarm() {
            if (isPlaying || !audioCtx) return;
            oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            
            oscillator.type = 'sawtooth'; 
            oscillator.frequency.value = 800; 
            
            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            
            oscillator.start();
            isPlaying = true;

            // Modulate pitch (Siren Effect)
            window.sirenInterval = setInterval(() => {
                if(oscillator.frequency.value == 800) oscillator.frequency.value = 500;
                else oscillator.frequency.value = 800;
            }, 300);
        }

        function stopAlarm() {
            if (oscillator) {
                oscillator.stop();
                clearInterval(window.sirenInterval);
                oscillator = null;
                isPlaying = false;
            }
        }

        // --- 5. SERVER POLLING (The Brain) ---
        setInterval(() => {
            fetch('/status')
                .then(res => res.json())
                .then(data => {
                    const overlay = document.getElementById('overlay');
                    const safeScreen = document.getElementById('safe');
                    
                    if (data.frozen && hasInteracted) {
                        // SHOW PRANK
                        safeScreen.style.display = 'none';
                        overlay.style.display = 'flex';
                        
                        // Laptop: Hide Cursor
                        document.body.style.cursor = 'none';

                        // Mobile: Vibrate (Strong)
                        if(navigator.vibrate) navigator.vibrate([400, 100, 400, 100]); 
                        
                        // Sound: Play
                        if(audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
                        playAlarm();

                        // Fake Progress Counter
                        document.getElementById('counter').innerText = Math.floor(Math.random() * 99) + "%";
                        
                    } else {
                        // HIDE PRANK / RESET
                        if(hasInteracted) {
                            overlay.style.display = 'none';
                            safeScreen.style.display = 'flex';
                            safeScreen.innerHTML = "<h1 style='color:#00ff00'>VERIFIED ✅</h1><p>System Safe.</p>";
                            document.body.style.cursor = 'default';
                            stopAlarm();
                        }
                    }
                });
        }, 1000); // Checks every 1 second
    </script>
</body>
</html>
"""

# ==========================================
# 2. THE ADMIN PAGE (For You)
# ==========================================
admin_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terminator Control</title>
    <style>
        body { background: #111; color: #0f0; font-family: monospace; text-align: center; padding-top: 50px; }
        button { 
            padding: 20px 40px; font-size: 20px; border: 2px solid #0f0; 
            background: #000; color: #0f0; cursor: pointer; border-radius: 10px; 
            text-transform: uppercase; letter-spacing: 2px;
            transition: 0.2s;
        }
        button:active { background: #0f0; color: #000; transform: scale(0.95); }
        .status { margin-bottom: 30px; font-size: 24px; border: 1px solid #333; padding: 10px; display: inline-block; }
    </style>
</head>
<body>
    <h1>TERMINATOR CONTROL 💀</h1>
    
    <div class="status">
        Current State: <span id="st">{{ state }}</span>
    </div>
    <br>
    
    <button onclick="toggle()">🔴 TOGGLE ATTACK</button>

    <script>
        function toggle() {
            fetch('/toggle', { method: 'POST' })
                .then(res => res.json())
                .then(data => {
                    const st = document.getElementById('st');
                    if(data.frozen) {
                        st.innerText = "ATTACKING... 🔥";
                        st.style.color = "red";
                    } else {
                        st.innerText = "SAFE ✅";
                        st.style.color = "#0f0";
                    }
                });
        }
    </script>
</body>
</html>
"""

# ==========================================
# 3. FLASK ROUTES
# ==========================================
@app.route('/')
def index():
    return render_template_string(prank_html)

@app.route('/admin')
def admin():
    status_text = "ATTACKING... 🔥" if server_state["frozen"] else "SAFE ✅"
    return render_template_string(admin_html, state=status_text)

@app.route('/status')
def status():
    return jsonify(server_state)

@app.route('/toggle', methods=['POST'])
def toggle():
    server_state["frozen"] = not server_state["frozen"]
    return jsonify(server_state)

if __name__ == '__main__':
    # Running on 0.0.0.0
    app.run(host='0.0.0.0', port=5000)