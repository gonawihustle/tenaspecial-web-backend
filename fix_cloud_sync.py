import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Strip out all previous broken injections
content = re.sub(r'<script id="tenaspecial-core">[\s\S]*?</script>', '', content)

script = '''
<!-- TENASPECIAL NATIVE CLOUD REST API ENGINE -->
<script id="tenaspecial-core">
(function() {
    const SUPA_URL = "https://xbuhtrxhzpjiiiqeluhh.supabase.co/rest/v1/channels";
    const SUPA_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhidWh0cnhoenBqaWlpcWVsdWhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODg4ODE4ODgsImV4cCI6MjEwNDQ1Nzg4OH0.s0tBaDZJs5_RxVtgDf5M50owUbeEIcrCciLk4FTYXNc";
    const BOT_URL = "https://t.me/tenaspecial_bot";

    const HEADERS = {
        "apikey": SUPA_KEY,
        "Authorization": "Bearer " + SUPA_KEY,
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    };

    // 1. INJECT GUARANTEED CLOUD ADMIN UI
    function injectCloudAdmin() {
        if (document.getElementById('ts-cloud-admin-btn')) return;
        
        // Floating Button
        const btn = document.createElement('div');
        btn.id = 'ts-cloud-admin-btn';
        btn.innerHTML = `
            <button onclick="document.getElementById('ts-cloud-modal').style.display='flex'" style="position:fixed; bottom:24px; right:24px; z-index:9999; background:#0284c7; color:white; padding:14px 24px; border-radius:50px; font-weight:900; font-size:14px; box-shadow:0 10px 25px rgba(2,132,199,0.4); border:none; cursor:pointer; font-family:sans-serif;">
                ☁️ Cloud Database Manager
            </button>
        `;
        document.body.appendChild(btn);

        // Modal Overlay
        const modal = document.createElement('div');
        modal.id = 'ts-cloud-modal';
        modal.style = "display:none; position:fixed; inset:0; background:rgba(0,0,0,0.8); z-index:10000; align-items:center; justify-content:center; padding:20px; font-family:sans-serif;";
        
        modal.innerHTML = `
            <div style="background:#0f172a; border:1px solid #1e293b; width:100%; max-width:400px; border-radius:24px; overflow:hidden; box-shadow:0 25px 50px rgba(0,0,0,0.5);">
                <div style="padding:20px; border-bottom:1px solid #1e293b; display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="color:white; margin:0; font-size:16px;">☁️ Secure Cloud Sync</h3>
                    <button onclick="document.getElementById('ts-cloud-modal').style.display='none'" style="background:transparent; color:#94a3b8; border:none; font-size:20px; cursor:pointer;">&times;</button>
                </div>
                
                <div style="display:flex; padding:10px; background:#1e293b; gap:5px;">
                    <button onclick="tsSwitchTab('spec')" id="ts-tab-spec" style="flex:1; padding:10px; border-radius:12px; font-weight:bold; font-size:12px; background:#0284c7; color:white; border:none;">Specialist</button>
                    <button onclick="tsSwitchTab('prod')" id="ts-tab-prod" style="flex:1; padding:10px; border-radius:12px; font-weight:bold; font-size:12px; background:transparent; color:#94a3b8; border:none;">Store</button>
                    <button onclick="tsSwitchTab('chan')" id="ts-tab-chan" style="flex:1; padding:10px; border-radius:12px; font-weight:bold; font-size:12px; background:transparent; color:#94a3b8; border:none;">Channel</button>
                </div>

                <div style="padding:20px;">
                    <!-- Specialist Form -->
                    <div id="ts-form-spec" style="display:flex; flex-direction:column; gap:12px;">
                        <input id="ts-val-spec-name" placeholder="Doctor Name (e.g. Dr. Abebe)" style="padding:12px; border-radius:12px; background:#020617; border:1px solid #1e293b; color:white;" />
                        <input id="ts-val-spec-cat" placeholder="Category (e.g. OBGYN, Pediatrics)" style="padding:12px; border-radius:12px; background:#020617; border:1px solid #1e293b; color:white;" />
                        <button onclick="tsSaveData('specialist')" style="padding:14px; border-radius:12px; background:#0284c7; color:white; font-weight:bold; border:none; margin-top:10px;">Save to Cloud</button>
                    </div>

                    <!-- Store Form -->
                    <div id="ts-form-prod" style="display:none; flex-direction:column; gap:12px;">
                        <input id="ts-val-prod-name" placeholder="Product Name" style="padding:12px; border-radius:12px; background:#020617; border:1px solid #1e293b; color:white;" />
                        <input id="ts-val-prod-desc" placeholder="Description / Price" style="padding:12px; border-radius:12px; background:#020617; border:1px solid #1e293b; color:white;" />
                        <button onclick="tsSaveData('product')" style="padding:14px; border-radius:12px; background:#9333ea; color:white; font-weight:bold; border:none; margin-top:10px;">Save to Cloud</button>
                    </div>

                    <!-- Channel Form -->
                    <div id="ts-form-chan" style="display:none; flex-direction:column; gap:12px;">
                        <input id="ts-val-chan-name" placeholder="Channel / Group Name" style="padding:12px; border-radius:12px; background:#020617; border:1px solid #1e293b; color:white;" />
                        <select id="ts-val-chan-type" style="padding:12px; border-radius:12px; background:#020617; border:1px solid #1e293b; color:white;">
                            <option value="FREE">FREE Channel (Public)</option>
                            <option value="PREMIUM">PREMIUM Channel (Paid)</option>
                        </select>
                        <input id="ts-val-chan-link" placeholder="Telegram Link (For Free Channels)" style="padding:12px; border-radius:12px; background:#020617; border:1px solid #1e293b; color:white;" />
                        <button onclick="tsSaveData('channel')" style="padding:14px; border-radius:12px; background:#0284c7; color:white; font-weight:bold; border:none; margin-top:10px;">Save to Cloud</button>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    window.tsSwitchTab = function(tab) {
        ['spec', 'prod', 'chan'].forEach(t => {
            document.getElementById('ts-form-' + t).style.display = (t === tab) ? 'flex' : 'none';
            document.getElementById('ts-tab-' + t).style.background = (t === tab) ? (t === 'prod' ? '#9333ea' : '#0284c7') : 'transparent';
            document.getElementById('ts-tab-' + t).style.color = (t === tab) ? 'white' : '#94a3b8';
        });
    }

    // 2. DIRECT REST API POST (No libraries required)
    window.tsSaveData = async function(type) {
        let payload = {};
        
        if (type === 'specialist') {
            const name = document.getElementById('ts-val-spec-name').value;
            const cat = document.getElementById('ts-val-spec-cat').value || 'Consultant';
            if (!name) return alert("Enter doctor name");
            payload = { title: name, description: `[TYPE:specialist][CAT:${cat}]`, link: BOT_URL, is_paid: false };
        } 
        else if (type === 'product') {
            const name = document.getElementById('ts-val-prod-name').value;
            const desc = document.getElementById('ts-val-prod-desc').value;
            if (!name) return alert("Enter product name");
            payload = { title: name, description: `[TYPE:product] ${desc}`, link: BOT_URL, is_paid: true };
        } 
        else if (type === 'channel') {
            const name = document.getElementById('ts-val-chan-name').value;
            const access = document.getElementById('ts-val-chan-type').value;
            let link = document.getElementById('ts-val-chan-link').value;
            if (!name) return alert("Enter channel name");
            
            const isPremium = access === 'PREMIUM';
            if (isPremium) link = BOT_URL;
            else if (link && !link.startsWith('http')) link = 'https://t.me/' + link.replace('@', '');
            
            payload = { title: name, description: `[TYPE:channel] ${isPremium ? 'Premium Access' : 'Free Community'}`, link: link || BOT_URL, is_paid: isPremium };
        }

        try {
            const res = await fetch(SUPA_URL, { method: "POST", headers: HEADERS, body: JSON.stringify(payload) });
            if (res.ok) {
                alert("Successfully saved to Supabase Cloud!");
                document.getElementById('ts-cloud-modal').style.display = 'none';
                document.querySelectorAll('input').forEach(i => i.value = '');
                tsFetchAndRender(); // Refresh UI instantly
            } else {
                alert("Database Error: Check connection.");
            }
        } catch(e) { alert("Network error: " + e.message); }
    };

    // 3. DIRECT REST API GET & UI RENDERER
    window.tsFetchAndRender = async function() {
        try {
            const res = await fetch(SUPA_URL, { headers: HEADERS });
            if (!res.ok) return;
            const data = await res.json();
            
            const specs = data.filter(d => (d.description || '').includes('[TYPE:specialist]'));
            const prods = data.filter(d => (d.description || '').includes('[TYPE:product]'));
            const chans = data.filter(d => !(d.description || '').includes('[TYPE:specialist]') && !(d.description || '').includes('[TYPE:product]'));

            updateUISection('Speciality Categories', specs, 'Categories', renderSpecialistHTML);
            updateUISection('Digital Medical Store', prods, 'Products', renderProductHTML);
            updateUISection('Channels & Groups', chans, 'Channels', renderChannelHTML);

        } catch(e) { console.error("Render error:", e); }
    };

    function updateUISection(headerText, items, countLabel, renderFunc) {
        // Find the native header
        const headers = Array.from(document.querySelectorAll('h2, h3, h4, div'));
        const header = headers.find(el => el.children.length === 0 && el.textContent.trim().toLowerCase() === headerText.toLowerCase());
        
        if (!header) return;

        // Update Counter
        const parentRow = header.closest('div.flex');
        if (parentRow) {
            const counter = Array.from(parentRow.querySelectorAll('span, div')).find(el => el.textContent.includes(countLabel));
            if (counter) counter.textContent = `${items.length} ${countLabel}`;
        }

        // Target Container
        let container = document.getElementById('ts-cloud-box-' + countLabel);
        if (!container) {
            container = document.createElement('div');
            container.id = 'ts-cloud-box-' + countLabel;
            container.className = 'w-full my-3 space-y-3';
            if (parentRow && parentRow.parentElement) {
                parentRow.parentElement.insertBefore(container, parentRow.nextSibling);
            }
        }

        // Hide old placeholder boxes under this section
        if (parentRow && parentRow.parentElement) {
            Array.from(parentRow.parentElement.children).forEach(child => {
                if (child !== parentRow && child !== container && child.tagName === 'DIV' && child.textContent.includes('No ')) {
                    child.style.display = 'none';
                }
            });
        }

        if (items.length === 0) {
            container.innerHTML = `<div style="padding:16px; background:#0f172a; border:1px dashed #1e293b; border-radius:16px; color:#64748b; font-size:12px; text-align:center;">No items found in database.</div>`;
            return;
        }

        container.innerHTML = items.map(renderFunc).join('');
    }

    // NATIVE MATCHING STYLES (From your screenshots)
    function renderSpecialistHTML(item) {
        let cat = "Specialist";
        if (item.description && item.description.includes('[CAT:')) {
            const match = item.description.match(/\[CAT:(.*?)\]/);
            if (match && match[1]) cat = match[1].trim();
        }
        return `
            <div style="display:flex; align-items:center; justify-content:space-between; padding:16px; margin-bottom:12px; background:#0f172a; border:1px solid #1e293b; border-radius:16px;">
                <div>
                    <div style="color:white; font-weight:bold; font-size:15px; font-family:sans-serif;">${item.title}</div>
                    <div style="color:#94a3b8; font-size:12px; margin-top:2px; font-family:sans-serif;">Category: ${cat}</div>
                </div>
                <a href="${BOT_URL}" target="_blank" style="padding:8px 16px; background:#0284c7; color:white; font-size:12px; font-weight:bold; border-radius:12px; text-decoration:none; font-family:sans-serif;">Book Specialist</a>
            </div>
        `;
    }

    function renderProductHTML(item) {
        const cleanDesc = (item.description || '').replace(/\[TYPE:.*?\]/g, '').trim();
        return `
            <div style="display:flex; align-items:center; justify-content:space-between; padding:16px; margin-bottom:12px; background:#0f172a; border:1px solid #1e293b; border-radius:16px;">
                <div>
                    <div style="color:white; font-weight:bold; font-size:15px; font-family:sans-serif;">${item.title}</div>
                    <div style="color:#94a3b8; font-size:12px; margin-top:2px; font-family:sans-serif;">${cleanDesc}</div>
                </div>
                <a href="${BOT_URL}" target="_blank" style="padding:8px 16px; background:#9333ea; color:white; font-size:12px; font-weight:bold; border-radius:12px; text-decoration:none; font-family:sans-serif;">Buy Product</a>
            </div>
        `;
    }

    function renderChannelHTML(item) {
        const cleanDesc = (item.description || '').replace(/\[TYPE:.*?\]/g, '').trim();
        const isPremium = item.is_paid === true;
        
        const badge = isPremium 
            ? `<span style="padding:2px 8px; font-size:10px; font-weight:bold; background:rgba(245,158,11,0.2); color:#fbbf24; border:1px solid rgba(245,158,11,0.3); border-radius:6px;">PREMIUM</span>`
            : `<span style="padding:2px 8px; font-size:10px; font-weight:bold; background:rgba(8,145,178,0.2); color:#22d3ee; border:1px solid rgba(8,145,178,0.3); border-radius:6px;">FREE</span>`;
            
        const btn = isPremium
            ? `<a href="${BOT_URL}" target="_blank" style="padding:8px 16px; background:#f59e0b; color:#1e293b; font-size:12px; font-weight:bold; border-radius:12px; text-decoration:none; white-space:nowrap; font-family:sans-serif;">Unlock Premium</a>`
            : `<a href="${item.link || BOT_URL}" target="_blank" style="padding:8px 16px; background:#0284c7; color:white; font-size:12px; font-weight:bold; border-radius:12px; text-decoration:none; white-space:nowrap; font-family:sans-serif;">Join Channel</a>`;

        return `
            <div style="display:flex; align-items:center; justify-content:space-between; padding:16px; margin-bottom:12px; background:#0f172a; border:1px solid #1e293b; border-radius:16px; gap:12px;">
                <div style="flex:1;">
                    <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                        <span style="color:white; font-weight:bold; font-size:15px; font-family:sans-serif; line-height:1.2;">${item.title}</span>
                        ${badge}
                    </div>
                    <div style="color:#94a3b8; font-size:12px; font-family:sans-serif;">${cleanDesc}</div>
                </div>
                ${btn}
            </div>
        `;
    }

    // Init Engine
    injectCloudAdmin();
    tsFetchAndRender();
    setInterval(tsFetchAndRender, 3000); // Keep everything continuously synced with cloud
})();
</script>
'''

if '</body>' in content:
    content = content.replace('</body>', script + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Native Fetch Engine and Cloud Admin applied successfully!")
