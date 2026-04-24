import os

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VIBE SPACIEE</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #fcfbf9;
            --container-bg: #ffffff;
            --text-main: #2d2a26;
            --text-muted: #757067;
            --primary: #d65a31;
            --primary-dark: #b54925;
            --border: #e8e6e1;
            --card-bg: #f5f3ef;
            --chip-bg: #f0ece3;
            --chip-hover: #e3dccf;
            --shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
            padding: 3rem 1rem;
        }

        .container {
            background: var(--container-bg);
            border-radius: 16px;
            padding: 3rem;
            width: 100%;
            max-width: 600px;
            box-shadow: var(--shadow);
            border: 1px solid var(--border);
        }

        h1 { font-family: 'Playfair Display', serif; font-size: 2.2rem; margin-bottom: 0.5rem; }
        p.subtitle { color: var(--text-muted); margin-bottom: 2.5rem; line-height: 1.5; }

        .step-num {
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--primary);
            letter-spacing: 0.1em;
            margin-bottom: 0.3rem;
            display: block;
        }

        .step-title {
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .step-desc {
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-bottom: 1.2rem;
            line-height: 1.4;
        }

        .section {
            margin-bottom: 2.5rem;
            padding-bottom: 2.5rem;
            border-bottom: 1px solid var(--border);
        }
        .section:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }

        /* Chips & Toggles */
        .chip-group { display: flex; flex-wrap: wrap; gap: 0.6rem; }
        .chip {
            padding: 0.6rem 1.2rem;
            border-radius: 20px;
            background: var(--chip-bg);
            color: var(--text-main);
            font-size: 0.9rem;
            font-weight: 500;
            cursor: pointer;
            border: 1px solid transparent;
            transition: all 0.2s;
        }
        .chip:hover { background: var(--chip-hover); }
        .chip.active { background: var(--text-main); color: #fff; }

        /* Toggle switches */
        .toggle-group {
            display: inline-flex;
            background: var(--chip-bg);
            border-radius: 8px;
            padding: 4px;
            margin-bottom: 1rem;
        }
        .toggle-btn {
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            border: none;
            background: transparent;
            color: var(--text-muted);
        }
        .toggle-btn.active { background: var(--text-main); color: #fff; }

        /* Inputs */
        .input-row { display: flex; gap: 1rem; }
        .input-col { flex: 1; }
        .input-label { display: block; font-size: 0.75rem; font-weight: 600; color: var(--text-muted); margin-bottom: 0.4rem; letter-spacing: 0.05em; text-transform: uppercase; }
        input[type="number"], input[type="text"] {
            width: 100%;
            padding: 0.8rem;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--card-bg);
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            outline: none;
        }
        input:focus { border-color: var(--text-main); }

        .sqft-calc {
            margin-top: 1rem;
            padding: 0.8rem;
            background: var(--card-bg);
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--text-main);
        }
        .sqft-calc span { font-weight: 400; color: var(--text-muted); }

        /* Theme Cards */
        .theme-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }
        .theme-card {
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            cursor: pointer;
            transition: all 0.2s;
            background: var(--card-bg);
        }
        .theme-card:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
        .theme-card.active { border: 2px solid var(--primary); }
        .theme-img {
            height: 120px;
            background-color: #ddd;
            background-size: cover;
            background-position: center;
            position: relative;
        }
        .theme-name {
            position: absolute;
            bottom: 10px;
            left: 10px;
            color: #fff;
            font-weight: 700;
            font-size: 1.1rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.8);
        }
        .theme-desc {
            padding: 0.8rem;
            font-size: 0.8rem;
            color: var(--text-muted);
            line-height: 1.4;
        }

        /* Drop Zone */
        .drop-zone {
            width: 100%;
            height: 160px;
            border: 2px dashed #ccc;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            background: var(--card-bg);
            text-align: center;
            flex-direction: column;
            gap: 10px;
            position: relative;
            transition: all 0.2s;
        }
        .drop-zone:hover { border-color: var(--primary); background: #fdf5f2; }
        .drop-zone.valid-room { border-color: #22c55e; background: #f0fdf4; }
        #preview-img { max-height: 120px; border-radius: 8px; display: none; }
        
        .btn-primary {
            background: var(--text-main);
            color: #fff;
            border: none;
            padding: 1rem 2rem;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            margin-top: 1rem;
            transition: all 0.2s;
        }
        .btn-primary:hover { background: #000; }
        .btn-primary:disabled { background: #ccc; cursor: not-allowed; }

        /* Loader & Results */
        .loading { display: none; text-align: center; margin: 2rem 0; font-weight: 500; color: var(--text-muted); }
        .results { display: none; }
        .result-images { display: flex; flex-direction: column; gap: 1.5rem; margin-top: 1.5rem; }
        .comparison { border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
        .comp-header { padding: 0.8rem 1rem; background: var(--card-bg); font-weight: 600; border-bottom: 1px solid var(--border); }
        .comp-body { display: flex; height: 250px; }
        .comp-half { flex: 1; background-size: cover; background-position: center; position: relative; }
        .comp-half::after { content: attr(data-label); position: absolute; bottom: 8px; left: 8px; background: rgba(0,0,0,0.6); color: #fff; font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; }
        .comp-divider { width: 2px; background: var(--primary); }

        .budget-table { width: 100%; border-collapse: collapse; margin-top: 1rem; font-size: 0.9rem; }
        .budget-table td { padding: 0.8rem 0; border-bottom: 1px solid var(--border); }
        .budget-table td:last-child { text-align: right; font-weight: 600; }
        .budget-total { font-weight: 700 !important; font-size: 1.1rem; color: var(--primary); border-bottom: none !important;}

    </style>
</head>
<body>

    <div class="container" id="app-container">
        <h1>Design your space</h1>
        <p class="subtitle">Upload a photo of your room, tell us what you have and what you want, and our AI will architect the perfect layout and aesthetic.</p>

        <div id="setup-form">
            <!-- STEP 1 -->
            <div class="section">
                <span class="step-num">01</span>
                <h2 class="step-title">Upload your room</h2>
                <div id="drop-zone" class="drop-zone">
                    <img id="preview-img" src="" alt="Preview" />
                    <span id="drop-text">Drag &amp; drop interior photo here<br/><span style="font-size: 0.8rem; opacity: 0.7; margin-top: 4px; display:inline-block;">or click to browse</span></span>
                    <input type="file" id="fileInput" accept="image/*" style="display: none;" />
                </div>
                <p id="validation-msg" style="font-size:0.85rem; margin-top:0.5rem; color:#d65a31; display:none;"></p>
            </div>

            <!-- STEP 2 -->
            <div class="section">
                <span class="step-num">02</span>
                <h2 class="step-title">What kind of room?</h2>
                <div class="chip-group" id="room-types">
                    <div class="chip active">Living Room</div>
                    <div class="chip">Bedroom</div>
                    <div class="chip">Home Office</div>
                    <div class="chip">Dining</div>
                    <div class="chip">Kitchen</div>
                    <div class="chip">Kids</div>
                    <div class="chip">Studio</div>
                    <div class="chip">Bathroom</div>
                </div>
            </div>

            <!-- STEP 3 -->
            <div class="section">
                <span class="step-num">03</span>
                <h2 class="step-title">How big is it?</h2>
                <div class="toggle-group" id="unit-toggle">
                    <button class="toggle-btn active" data-unit="feet">Feet</button>
                    <button class="toggle-btn" data-unit="meters">Meters</button>
                </div>
                <div class="input-row">
                    <div class="input-col"><span class="input-label">Length</span><input type="number" id="dim-l" value="14"></div>
                    <div class="input-col"><span class="input-label">Width</span><input type="number" id="dim-w" value="12"></div>
                    <div class="input-col"><span class="input-label">Height</span><input type="number" id="dim-h" value="9"></div>
                </div>
                <div class="sqft-calc">
                    &#x2197; <strong id="area-val">168 sq ft</strong> <span>of floor space</span>
                </div>
            </div>

            <!-- STEP 4 -->
            <div class="section">
                <span class="step-num">04</span>
                <h2 class="step-title">What's already in there?</h2>
                <p class="step-desc">Select items you want to keep. We'll include them in the new design.</p>
                <div class="chip-group" id="existing-items">
                    <div class="chip">Sofa</div>
                    <div class="chip">Bed</div>
                    <div class="chip">Dining Table</div>
                    <div class="chip">Desk</div>
                    <div class="chip">Wardrobe</div>
                    <div class="chip">TV Unit</div>
                    <div class="chip">Bookshelf</div>
                    <div class="chip">Coffee Table</div>
                    <div class="chip">Rug</div>
                </div>
                <input type="text" id="custom-items" placeholder="Anything else? e.g. Vintage mirror" style="margin-top:1rem;">
            </div>

            <!-- STEP 5 -->
            <div class="section">
                <span class="step-num">05</span>
                <h2 class="step-title">Pick a feeling</h2>
                <p class="step-desc">Choose a design direction for the AI to follow.</p>
                <div class="theme-grid" id="themes">
                    <div class="theme-card active" data-theme="Minimalist">
                        <div class="theme-img" style="background-image:url('https://images.unsplash.com/photo-1600607686527-6fb886090705?w=500&q=80')"><span class="theme-name">Minimalist</span></div>
                        <div class="theme-desc">Clean, calm, only what matters.</div>
                    </div>
                    <div class="theme-card" data-theme="Scandinavian">
                        <div class="theme-img" style="background-image:url('https://images.unsplash.com/photo-1593696140826-c58b021acf8b?w=500&q=80')"><span class="theme-name">Scandinavian</span></div>
                        <div class="theme-desc">Light woods, soft textiles, hygge.</div>
                    </div>
                    <div class="theme-card" data-theme="Boho">
                        <div class="theme-img" style="background-image:url('https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=500&q=80')"><span class="theme-name">Boho</span></div>
                        <div class="theme-desc">Layered textures, plants, lived-in soul.</div>
                    </div>
                    <div class="theme-card" data-theme="Industrial">
                        <div class="theme-img" style="background-image:url('https://images.unsplash.com/photo-1513694203232-719a280e022f?w=500&q=80')"><span class="theme-name">Industrial</span></div>
                        <div class="theme-desc">Raw materials and confident lines.</div>
                    </div>
                    <div class="theme-card" data-theme="Mid-Century">
                        <div class="theme-img" style="background-image:url('https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500&q=80')"><span class="theme-name">Mid-Century</span></div>
                        <div class="theme-desc">Walnut warmth and sculptural shapes.</div>
                    </div>
                    <div class="theme-card" data-theme="Japandi">
                        <div class="theme-img" style="background-image:url('https://images.unsplash.com/photo-1616486029423-aaa4789e8c9a?w=500&q=80')"><span class="theme-name">Japandi</span></div>
                        <div class="theme-desc">Quiet, intentional, breathing space.</div>
                    </div>
                    <div class="theme-card" data-theme="Coastal">
                        <div class="theme-img" style="background-image:url('https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=500&q=80')"><span class="theme-name">Coastal</span></div>
                        <div class="theme-desc">Bleached woods and breezy linens.</div>
                    </div>
                    <div class="theme-card" data-theme="Farmhouse">
                        <div class="theme-img" style="background-image:url('https://images.unsplash.com/photo-1582582621959-48d27397dc69?w=500&q=80')"><span class="theme-name">Farmhouse</span></div>
                        <div class="theme-desc">Honest woods with worn-in welcome.</div>
                    </div>
                </div>
            </div>

            <!-- STEP 6 -->
            <div class="section">
                <span class="step-num">06</span>
                <h2 class="step-title">What can you spend?</h2>
                <div class="toggle-group" id="currency-toggle">
                    <button class="toggle-btn active" data-curr="USD">$ USD</button>
                    <button class="toggle-btn" data-curr="EUR">€ EUR</button>
                    <button class="toggle-btn" data-curr="GBP">£ GBP</button>
                    <button class="toggle-btn" data-curr="INR">₹ INR</button>
                </div>
                <input type="number" id="budgetLimit" value="2000" style="font-size: 1.5rem; font-weight:700; text-align:center;">
            </div>

            <button class="btn-primary" id="generateBtn" onclick="startGeneration()">Generate Design</button>
        </div>

        <div class="loading" id="loading">
            <h2 style="font-family:'Playfair Display',serif; color:var(--text-main); margin-bottom:1rem;">Architecting your space...</h2>
            <p id="loading-text">Analyzing spatial constraints and generating renders.</p>
        </div>

        <div class="results" id="results">
            <h2 style="font-family: 'Playfair Display', serif; font-size: 2rem; margin-bottom: 1rem;">Your Redesign</h2>
            <p id="explanation-text" style="line-height: 1.6; color: var(--text-muted); margin-bottom: 2rem;"></p>

            <div class="result-images" id="resultImageBox"></div>

            <h3 style="margin-top: 3rem; margin-bottom:1rem; font-family:'Playfair Display',serif;">Estimated Budget</h3>
            <div id="extra-results"></div>

            <button class="btn-primary" style="margin-top: 3rem; background: var(--chip-bg); color: var(--text-main);" onclick="location.reload()">Design Another Room</button>
        </div>

    </div>

    <script>
        const API_BASE = window.location.origin + "/api/v1";
        let selectedFile = null;
        let roomValidated = false;
        let selectedRoomType = "Living Room";
        let selectedTheme = "Minimalist";
        let selectedCurrency = "USD";

        // Chip selection logic
        document.querySelectorAll('#room-types .chip').forEach(chip => {
            chip.addEventListener('click', function() {
                document.querySelectorAll('#room-types .chip').forEach(c => c.classList.remove('active'));
                this.classList.add('active');
                selectedRoomType = this.innerText;
            });
        });

        document.querySelectorAll('#existing-items .chip').forEach(chip => {
            chip.addEventListener('click', function() {
                this.classList.toggle('active');
            });
        });

        // Toggle logic
        document.querySelectorAll('#currency-toggle .toggle-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('#currency-toggle .toggle-btn').forEach(c => c.classList.remove('active'));
                this.classList.add('active');
                selectedCurrency = this.dataset.curr;
            });
        });

        // Theme selection
        document.querySelectorAll('.theme-card').forEach(card => {
            card.addEventListener('click', function() {
                document.querySelectorAll('.theme-card').forEach(c => c.classList.remove('active'));
                this.classList.add('active');
                selectedTheme = this.dataset.theme;
            });
        });

        // Area Calc
        const inputs = ['dim-l', 'dim-w'];
        inputs.forEach(id => {
            document.getElementById(id).addEventListener('input', () => {
                let l = parseFloat(document.getElementById('dim-l').value) || 0;
                let w = parseFloat(document.getElementById('dim-w').value) || 0;
                let unit = document.querySelector('#unit-toggle .active').dataset.unit;
                document.getElementById('area-val').innerText = (l * w).toFixed(0) + (unit === 'feet' ? ' sq ft' : ' sq m');
            });
        });

        // File handling
        const dropZone = document.getElementById('drop-zone');
        const fileInput = document.getElementById('fileInput');
        const previewImg = document.getElementById('preview-img');
        const dropText = document.getElementById('drop-text');

        dropZone.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', (e) => { if (e.target.files.length) handleFile(e.target.files[0]); });
        dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.style.borderColor = "var(--primary)"; });
        dropZone.addEventListener('dragleave', () => dropZone.style.borderColor = "#ccc");
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.style.borderColor = "#ccc";
            if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
        });

        async function handleFile(file) {
            const reader = new FileReader();
            reader.onload = (ev) => { previewImg.src = ev.target.result; };
            reader.readAsDataURL(file);
            previewImg.style.display = 'block';
            dropText.style.display = 'none';

            document.getElementById('validation-msg').style.display = 'block';
            document.getElementById('validation-msg').innerText = 'Validating image...';
            document.getElementById('validation-msg').style.color = 'var(--text-muted)';
            
            const fd = new FormData();
            fd.append('file', file);
            try {
                const res = await fetch(`${API_BASE}/validate-room`, { method: 'POST', body: fd });
                const data = await res.json();
                if (data.is_room) {
                    selectedFile = file;
                    roomValidated = true;
                    dropZone.classList.add('valid-room');
                    document.getElementById('validation-msg').innerText = '✓ Valid interior room detected.';
                    document.getElementById('validation-msg').style.color = '#22c55e';
                } else {
                    document.getElementById('validation-msg').innerText = '✕ Does not appear to be a room. Please try another photo.';
                    document.getElementById('validation-msg').style.color = '#d65a31';
                    roomValidated = false;
                }
            } catch(e) {
                // If backend offline, just accept
                selectedFile = file;
                roomValidated = true;
                dropZone.classList.add('valid-room');
                document.getElementById('validation-msg').innerText = '✓ Image ready (Backend offline).';
                document.getElementById('validation-msg').style.color = '#22c55e';
            }
        }

        async function startGeneration() {
            if (!selectedFile || !roomValidated) {
                alert('Please upload a valid room image first.');
                return;
            }

            document.getElementById('setup-form').style.display = 'none';
            document.getElementById('loading').style.display = 'block';
            
            // Get selected items
            let existingItems = Array.from(document.querySelectorAll('#existing-items .chip.active')).map(c => c.innerText);
            let customItems = document.getElementById('custom-items').value;
            let suggestions = existingItems;
            if (customItems) suggestions.push(customItems);

            const formData = new FormData();
            formData.append('file', selectedFile);
            
            let imageUrl = "http://127.0.0.1:8001/static/generic_room.png";
            try {
                const uploadRes = await fetch(`${API_BASE}/upload`, { method: 'POST', body: formData });
                const uploadData = await uploadRes.json();
                if (uploadData.success) imageUrl = uploadData.image_url;
            } catch(e) { console.warn("Upload failed"); }

            const payload = {
                image_url: imageUrl,
                room_type: selectedRoomType,
                design_style: selectedTheme,
                ai_suggestions: suggestions,
                design_preferences: {
                    budget: document.getElementById('budgetLimit').value,
                    country: selectedCurrency === 'INR' ? 'IN' : selectedCurrency === 'GBP' ? 'UK' : 'US'
                }
            };

            try {
                const res = await fetch(`${API_BASE}/generate`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if(data.success) {
                    pollStatus(data.generation_id, previewImg.src);
                } else {
                    alert('Generation error.'); location.reload();
                }
            } catch(e) {
                alert('API Offline.'); location.reload();
            }
        }

        async function pollStatus(jobId, uploadedSrc) {
            const interval = setInterval(async () => {
                try {
                    const res = await fetch(`${API_BASE}/generations/${jobId}`);
                    const data = await res.json();
                    if(data.status === 'completed') {
                        clearInterval(interval);
                        showResults(data.data, uploadedSrc);
                    }
                } catch(e) {}
            }, 1000); 
        }

        function showResults(resultData, uploadedSrc) {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('results').style.display = 'block';

            document.getElementById('explanation-text').innerText = resultData.explanation;

            const imgBox = document.getElementById('resultImageBox');
            imgBox.innerHTML = '';

            resultData.result_image_urls.forEach((url, i) => {
                imgBox.innerHTML += `
                    <div class="comparison">
                        <div class="comp-header">Variant ${i+1}</div>
                        <div class="comp-body">
                            <div class="comp-half" style="background-image:url('${uploadedSrc}')" data-label="Original"></div>
                            <div class="comp-divider"></div>
                            <div class="comp-half" style="background-image:url('${url}')" data-label="AI Generated"></div>
                        </div>
                    </div>
                `;
            });

            if (resultData.budget_estimates) {
                let html = '<table class="budget-table">';
                let total = 0;
                let sym = "$";
                resultData.budget_estimates.forEach(item => {
                    sym = item.currency_symbol;
                    html += `<tr><td>${item.item_name}</td><td>${sym}${item.estimated_cost.toLocaleString()}</td></tr>`;
                    total += item.estimated_cost;
                });
                html += `<tr><td><strong>Total Estimate</strong></td><td class="budget-total">${sym}${total.toLocaleString()}</td></tr></table>`;
                
                if (resultData.recommendations) {
                    html += '<h3 style="margin-top: 2rem; margin-bottom:1rem; font-family:\'Playfair Display\',serif;">Designer Notes</h3><ul style="padding-left:1.5rem; color:var(--text-muted); line-height:1.6;">';
                    resultData.recommendations.forEach(r => { html += `<li style="margin-bottom:0.5rem;">${r}</li>`; });
                    html += '</ul>';
                }
                
                document.getElementById('extra-results').innerHTML = html;
            }
        }
    </script>
</body>
</html>
"""

with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)
    
with open("../demo.html", "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print("Frontend HTML generated successfully!")
