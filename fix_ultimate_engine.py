import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Clean out any previous engine injections
html = re.sub(r'<script id="tenaspecial-master-engine">[\s\S]*?</script>', '', html)
html = re.sub(r'<script id="tenaspecial-core">[\s\S]*?</script>', '', html)

engine_script = r'''
<script id="tenaspecial-master-engine">
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

    // 1. Ensure Admin Panel Drawer/Modal Toggles Work
    document.addEventListener('click', function(e) {
        const toggleBtn = e.target.closest('[data-admin-toggle], #admin-toggle, .admin-btn, [href="#admin"]');
        if (toggleBtn) {
            e.preventDefault();
            const panel = document.querySelector('#admin-panel, #admin-modal, .admin-drawer, [data-admin-panel]');
            if (panel) {
                panel.classList.toggle('hidden');
                panel.style.display = panel.style.display === 'none' || !panel.style.display ? 'block' : 'none';
            }
        }
    });

    async function pushToCloud(payload) {
        try {
            const res = await fetch(SUPA_URL, { 
                method: "POST", 
                headers: HEADERS, 
                body: JSON.stringify(payload) 
            });
            if (res.ok) {
                alert("☁️ Entry saved successfully!");
                await syncFromCloud();
                return true;
            } else {
                const err = await res.text();
                alert("❌ Cloud Error: " + err);
            }
        } catch(e) {
            alert("❌ Connection Error.");
        }
        return false;
    }

    // 2. Intercept Form Submissions via Explicit Form Type Matching
    document.addEventListener('submit', async function(e) {
        const form = e.target;
        const inputs = Array.from(form.querySelectorAll('input, select, textarea'));
        const formText = (form.innerText + ' ' + form.action + ' ' + (form.id||'')).toLowerCase();

        // Check form type based on input placeholders and content
        const hasDoctor = inputs.some(i => (i.placeholder||'').toLowerCase().includes('doctor') || (i.name||'').toLowerCase().includes('doctor'));
        const hasProduct = inputs.some(i => (i.placeholder||'').toLowerCase().includes('product') || (i.placeholder||'').toLowerCase().includes('price'));
        const hasChannel = inputs.some(i => (i.placeholder||'').toLowerCase().includes('channel') || (i.placeholder||'').toLowerCase().includes('telegram'));

        if (hasDoctor || formText.includes('specialist') || formText.includes('doctor')) {
            e.preventDefault(); e.stopPropagation();
            const nameInput = inputs.find(i => (i.placeholder||'').toLowerCase().includes('doctor')) || inputs[0];
            const specInput = inputs.find(i => (i.placeholder||'').toLowerCase().includes('speciality')) || inputs[1];
            const catInput = inputs.find(i => (i.placeholder||'').toLowerCase().includes('category') || i.tagName === 'SELECT') || inputs[2];

            const docName = nameInput ? nameInput.value.trim() : '';
            const speciality = specInput ? specInput.value.trim() : 'Specialist';
            const category = catInput ? (catInput.value.trim() || 'General') : 'General';

            if (!docName) return alert("Please enter Doctor Name");

            const payload = {
                title: docName,
                description: `[TYPE:specialist][CAT:${category}][SPEC:${speciality}]`,
                link: BOT_URL,
                is_paid: false
            };
            if (await pushToCloud(payload)) inputs.forEach(i => { if (i.tagName !== 'SELECT') i.value = ''; });
            return;
        }

        if (hasProduct || formText.includes('product') || formText.includes('store')) {
            e.preventDefault(); e.stopPropagation();
            const nameInput = inputs.find(i => (i.placeholder||'').toLowerCase().includes('product')) || inputs[0];
            const descInput = inputs.find(i => (i.placeholder||'').toLowerCase().includes('description')) || inputs[1];
            const priceInput = inputs.find(i => (i.placeholder||'').toLowerCase().includes('price')) || inputs[2];

            const prodName = nameInput ? nameInput.value.trim() : '';
            const desc = descInput ? descInput.value.trim() : '';
            const price = priceInput ? priceInput.value.trim() : '';

            if (!prodName) return alert("Please enter Product Name");

            const payload = {
                title: prodName,
                description: `[TYPE:product][PRICE:${price}] ${desc}`.trim(),
                link: BOT_URL,
                is_paid: true
            };
            if (await pushToCloud(payload)) inputs.forEach(i => { if (i.tagName !== 'SELECT') i.value = ''; });
            return;
        }

        if (hasChannel || formText.includes('channel') || formText.includes('group')) {
            e.preventDefault(); e.stopPropagation();
            const nameInput = inputs.find(i => (i.placeholder||'').toLowerCase().includes('name')) || inputs[0];
            const linkInput = inputs.find(i => (i.placeholder||'').toLowerCase().includes('link')) || inputs[1];

            const title = nameInput ? nameInput.value.trim() : '';
            const link = linkInput ? linkInput.value.trim() : '';

            let isPremium = false;
            let kind = "Channel";

            inputs.filter(i => i.tagName === 'SELECT').forEach(s => {
                const val = s.value.toUpperCase();
                if (val.includes('PREMIUM')) isPremium = true;
                if (val.includes('GROUP')) kind = "Group";
            });

            if (!title) return alert("Please enter Channel/Group Name");

            const payload = {
                title: title,
                description: `[TYPE:channel][KIND:${kind}]`,
                link: isPremium ? BOT_URL : (link || BOT_URL),
                is_paid: isPremium
            };
            if (await pushToCloud(payload)) inputs.forEach(i => { if (i.tagName !== 'SELECT') i.value = ''; });
            return;
        }
    }, true);

    // 3. Robust DOM Section Container Finder
    function getSectionBox(keywords) {
        const elements = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, div, section'));
        for (const kw of keywords) {
            const match = elements.find(el => el.children.length === 0 && el.textContent.toLowerCase().includes(kw.toLowerCase()));
            if (match) {
                const parent = match.closest('section, div.bg-gray-900, div.p-6, div.rounded-xl, div.shadow-lg') || match.parentElement;
                let box = parent.querySelector('.ts-dynamic-box');
                if (!box) {
                    box = document.createElement('div');
                    box.className = 'ts-dynamic-box w-full mt-4 space-y-3';
                    parent.appendChild(box);
                }
                // Hide static placeholder elements
                Array.from(parent.children).forEach(child => {
                    if (child !== box && child !== match && !child.contains(match)) {
                        const txt = child.textContent.toLowerCase();
                        if (txt.includes('no ') || txt.includes('registered') || txt.includes('join free') || child.querySelector('button')) {
                            child.style.display = 'none';
                        }
                    }
                });
                return box;
            }
        }
        return null;
    }

    // 4. Live Multi-Section Cloud Synchronizer
    window.syncFromCloud = async function() {
        try {
            const res = await fetch(SUPA_URL, { headers: HEADERS });
            if (!res.ok) return;
            const data = await res.json();

            const specs = data.filter(d => (d.description || '').includes('[TYPE:specialist]'));
            const prods = data.filter(d => (d.description || '').includes('[TYPE:product]'));
            const chans = data.filter(d => (d.description || '').includes('[TYPE:channel]'));

            renderSpecialists(specs);
            renderProducts(prods);
            renderChannels(chans);
        } catch(e) {}
    };

    function renderSpecialists(items) {
        const container = getSectionBox(['Speciality Categories', 'Specialist', 'Doctors']);
        if (!container) return;

        if (items.length === 0) {
            container.innerHTML = `<div style="padding:16px; background:#0f172a; border:1px dashed #334155; border-radius:12px; color:#64748b; font-size:13px; text-align:center;">No doctor categories registered yet.</div>`;
            return;
        }

        const groups = {};
        items.forEach(item => {
            const catMatch = (item.description || '').match(/\[CAT:(.*?)\]/);
            const cat = catMatch ? catMatch[1].trim() : 'General';
            if (!groups[cat]) groups[cat] = [];
            groups[cat].push(item);
        });

        let html = '';
        for (const [catName, docs] of Object.entries(groups)) {
            const docsList = docs.map(doc => {
                const specMatch = (doc.description || '').match(/\[SPEC:(.*?)\]/);
                const spec = specMatch ? specMatch[1].trim() : 'Specialist';
                return `
                <div style="display:flex; justify-content:space-between; align-items:center; padding: 12px 0; border-bottom: 1px solid #1e293b;">
                    <div style="display:flex; align-items:center; gap:12px;">
                        <div style="font-size:22px;">👨‍⚕️</div>
                        <div>
                            <div style="color:#ffffff; font-size:14px; font-weight:600;">${doc.title}</div>
                            <div style="color:#94a3b8; font-size:12px;">${spec}</div>
                        </div>
                    </div>
                    <a href="${BOT_URL}" target="_blank" style="background:#0284c7; color:#ffffff; padding:6px 16px; border-radius:8px; font-size:12px; font-weight:bold; text-decoration:none;">Book Now</a>
                </div>`;
            }).join('');

            html += `
            <details style="background:#0f172a; border:1px solid #1e293b; border-radius:12px; margin-bottom:12px; overflow:hidden;" open>
                <summary style="padding:16px; cursor:pointer; font-weight:bold; color:#ffffff; display:flex; align-items:center; gap:12px; outline:none; background:#1e293b;">
                    <span style="font-size:18px;">📂</span>
                    <span style="flex-grow:1; font-size:15px;">${catName}</span>
                    <span style="background:#0284c7; color:#ffffff; padding:2px 10px; border-radius:12px; font-size:11px;">${docs.length} Doctors</span>
                </summary>
                <div style="padding: 0 16px 8px 16px; background:#0b1120;">${docsList}</div>
            </details>`;
        }
        container.innerHTML = html;
    }

    function renderProducts(items) {
        const container = getSectionBox(['Digital Medical Store', 'Medical Store', 'Products']);
        if (!container) return;

        if (items.length === 0) {
            container.innerHTML = `<div style="padding:16px; background:#0f172a; border:1px dashed #334155; border-radius:12px; color:#64748b; font-size:13px; text-align:center;">No store products added yet.</div>`;
            return;
        }

        container.innerHTML = items.map(item => {
            const priceMatch = (item.description || '').match(/\[PRICE:(.*?)\]/);
            const price = priceMatch ? priceMatch[1].trim() : '';
            const desc = (item.description || '').replace(/\[.*?\]/g, '').trim();

            return `
            <div style="display:flex; justify-content:space-between; align-items:center; padding:16px; background:#0f172a; border:1px solid #1e293b; border-radius:12px; margin-bottom:12px;">
                <div style="display:flex; gap:14px; align-items:center;">
                    <div style="width:48px; height:48px; background:rgba(147,51,234,0.15); border:1px solid rgba(147,51,234,0.3); border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px;">🛒</div>
                    <div>
                        <div style="color:#ffffff; font-size:15px; font-weight:bold;">${item.title}</div>
                        ${desc ? `<div style="color:#94a3b8; font-size:12px; margin-top:2px;">${desc}</div>` : ''}
                        ${price ? `<div style="color:#10b981; font-weight:bold; font-size:13px; margin-top:4px;">${price} ETB</div>` : ''}
                    </div>
                </div>
                <a href="${BOT_URL}" target="_blank" style="background:#9333ea; color:#ffffff; padding:10px 18px; border-radius:8px; font-weight:bold; font-size:13px; text-decoration:none;">Buy Now</a>
            </div>`;
        }).join('');
    }

    function renderChannels(items) {
        const container = getSectionBox(['Channels & Groups', 'Channels', 'Groups']);
        if (!container) return;

        if (items.length === 0) {
            container.innerHTML = `<div style="padding:16px; background:#0f172a; border:1px dashed #334155; border-radius:12px; color:#64748b; font-size:13px; text-align:center;">No channels added yet.</div>`;
            return;
        }

        container.innerHTML = items.map(item => {
            const isPremium = item.is_paid === true;
            let kind = "Channel";
            if ((item.description || '').includes('[KIND:Group]')) kind = "Group";

            const badge = isPremium 
                ? `<span style="padding:3px 8px; font-size:10px; font-weight:bold; background:rgba(245,158,11,0.2); color:#fbbf24; border:1px solid rgba(245,158,11,0.3); border-radius:6px;">PREMIUM</span>`
                : `<span style="padding:3px 8px; font-size:10px; font-weight:bold; background:rgba(8,145,178,0.2); color:#22d3ee; border:1px solid rgba(8,145,178,0.3); border-radius:6px;">FREE</span>`;

            return `
            <div style="padding:16px; margin-bottom:12px; background:#0f172a; border:1px solid #1e293b; border-radius:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="background:#334155; color:#cbd5e1; font-size:10px; font-weight:bold; padding:2px 6px; border-radius:4px; text-transform:uppercase;">${kind}</span>
                    <span style="color:#ffffff; font-weight:bold; font-size:15px; flex-grow:1;">${item.title}</span>
                    ${badge}
                </div>
                <a href="${item.link || BOT_URL}" target="_blank" style="display:flex; justify-content:center; align-items:center; width:100%; padding:10px; background:#1e293b; color:#22d3ee; font-size:13px; font-weight:bold; border-radius:8px; text-decoration:none; border:1px solid #334155; margin-top:12px;">Join Now</a>
            </div>`;
        }).join('');
    }

    syncFromCloud();
    setInterval(syncFromCloud, 3000);
})();
</script>
'''

if '</body>' in html:
    final_html = html.replace('</body>', engine_script + '\n</body>')
else:
    final_html = html + engine_script

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Engine re-injected with Admin panel toggles and exact action buttons!")
