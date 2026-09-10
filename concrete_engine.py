import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Completely remove all previous injected scripts
content = re.sub(r'<script id="tenaspecial-core">[\s\S]*?</script>', '', content)

script = r'''
<!-- TENASPECIAL CONCRETE CLOUD ENGINE -->
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

    async function pushToCloud(payload) {
        try {
            const res = await fetch(SUPA_URL, { method: "POST", headers: HEADERS, body: JSON.stringify(payload) });
            if (res.ok) {
                alert("☁️ SAVED TO CLOUD SUCCESSFULLY!");
                syncFromCloud(); 
                return true;
            } else {
                const errText = await res.text();
                alert("❌ CLOUD REJECTED IT: " + errText); 
            }
        } catch(e) { alert("❌ NETWORK ERROR"); }
        return false;
    }

    // KILL DEFAULT FORM SUBMISSIONS
    window.addEventListener('submit', (e) => { e.preventDefault(); e.stopPropagation(); }, true);

    // EXACT BUTTON MATCHING (No Guesswork)
    window.addEventListener('click', async (e) => {
        const btn = e.target.closest('button, input[type="submit"], input[type="button"]');
        if (!btn) return;
        
        const btnText = (btn.innerText || btn.value || '').toLowerCase().trim();
        const container = btn.closest('form, div.p-4, div.card, div.flex-col, div.bg-gray-800, section, div');
        if (!container) return;

        const inputs = Array.from(container.querySelectorAll('input, select, textarea'));

        // 1. IS IT A SPECIALIST?
        if (btnText === 'save specialist to category' || btnText.includes('save specialist')) {
            e.preventDefault(); e.stopPropagation();
            
            const docName = inputs.find(i => (i.placeholder||'').toLowerCase().includes('doctor'))?.value;
            const spec = inputs.find(i => (i.placeholder||'').toLowerCase().includes('speciality'))?.value || 'Specialist';
            const customCat = inputs.find(i => (i.placeholder||'').toLowerCase().includes('category'))?.value;
            const catDropdown = inputs.find(i => i.tagName === 'SELECT' && Array.from(i.options).some(o => o.text.includes('Select')));
            const finalCat = customCat || (catDropdown ? catDropdown.value : '') || 'General';
            
            if (!docName) return alert("Missing Doctor Name");
            
            if (await pushToCloud({ title: docName, description: `[TYPE:specialist][CAT:${finalCat}][SPEC:${spec}]`, link: BOT_URL, is_paid: false })) {
                inputs.forEach(i => { if (i.tagName !== 'SELECT') i.value = ''; });
            }
        }
        
        // 2. IS IT A PRODUCT?
        else if (btnText === 'add product to store' || btnText.includes('add product')) {
            e.preventDefault(); e.stopPropagation();
            
            const name = inputs.find(i => (i.placeholder||'').toLowerCase().includes('product'))?.value;
            const desc = inputs.find(i => (i.placeholder||'').toLowerCase().includes('description'))?.value || '';
            const price = inputs.find(i => (i.placeholder||'').toLowerCase().includes('price'))?.value || '';
            
            if (!name) return alert("Missing Product Name");
            
            if (await pushToCloud({ title: name, description: `[TYPE:product][PRICE:${price}] ${desc}`, link: BOT_URL, is_paid: true })) {
                inputs.forEach(i => { if (i.tagName !== 'SELECT') i.value = ''; });
            }
        }
        
        // 3. IS IT A CHANNEL/GROUP?
        else if (btnText === 'save channel / group' || btnText.includes('save channel')) {
            e.preventDefault(); e.stopPropagation();
            
            const name = inputs.find(i => (i.placeholder||'').toLowerCase().includes('name'))?.value;
            const link = inputs.find(i => (i.placeholder||'').toLowerCase().includes('link'))?.value || '';
            
            let isPremium = false;
            let kind = "Channel";
            inputs.filter(i => i.tagName === 'SELECT').forEach(s => {
                const val = s.value.toUpperCase();
                if (val.includes('PREMIUM')) isPremium = true;
                if (val.includes('GROUP')) kind = "Group";
            });
            
            if (!name) return alert("Missing Name");
            
            if (await pushToCloud({ title: name, description: `[TYPE:channel][KIND:${kind}]`, link: isPremium ? BOT_URL : link, is_paid: isPremium })) {
                inputs.forEach(i => { if (i.tagName !== 'SELECT') i.value = ''; });
            }
        }
        
        // CLEAR DB
        else if (btnText.includes('clear all')) {
            e.preventDefault(); e.stopPropagation();
            if(confirm("DANGER: Wipe entire cloud?")) {
                await fetch(SUPA_URL + '?title=not.is.null', { method: 'DELETE', headers: HEADERS });
                alert("☁️ Cloud wiped."); 
                syncFromCloud();
            }
        }
    }, true);

    // ==========================================
    // RENDERING ENGINE
    // ==========================================
    window.syncFromCloud = async function() {
        try {
            const res = await fetch(SUPA_URL, { headers: HEADERS });
            if (!res.ok) return;
            const data = await res.json();
            
            const specs = data.filter(d => (d.description || '').includes('[TYPE:specialist]'));
            const prods = data.filter(d => (d.description || '').includes('[TYPE:product]'));
            const chans = data.filter(d => (d.description || '').includes('[TYPE:channel]'));

            updateSpecialistsUI(specs);
            updateProductsUI(prods);
            updateChannelsUI(chans);
        } catch(e) {}
    };

    function getContainer(headerText, countLabel) {
        const headers = Array.from(document.querySelectorAll('h2, h3, h4, div'));
        const header = headers.find(el => el.children.length === 0 && el.textContent.trim().toLowerCase() === headerText.toLowerCase());
        if (!header) return null;

        const parentRow = header.closest('div.flex') || header.parentElement;
        
        // Update local count tags
        if (parentRow) {
            const counter = Array.from(parentRow.querySelectorAll('span, div')).find(el => el.textContent.includes(countLabel) || el.textContent.includes('Products') || el.textContent.includes('Categories') || el.textContent.includes('Channels'));
            if (counter) counter.style.display = 'none'; // Hide the local counter to avoid confusion
        }

        let container = document.getElementById('ts-cloud-box-' + countLabel);
        
        if (!container) {
            container = document.createElement('div');
            container.id = 'ts-cloud-box-' + countLabel;
            container.style.width = '100%';
            container.style.marginTop = '16px';
            if (parentRow && parentRow.nextSibling) {
                parentRow.parentElement.insertBefore(container, parentRow.nextSibling);
            } else if (parentRow) {
                parentRow.parentElement.appendChild(container);
            }
        }
        
        // Hide ALL local placeholders
        if (parentRow && parentRow.parentElement) {
            Array.from(parentRow.parentElement.children).forEach(child => {
                if (child !== parentRow && child !== container && child.tagName === 'DIV' && (child.textContent.includes('No ') || child.querySelector('button') || child.textContent.includes('Join Free'))) {
                    if(!child.id.includes('ts-cloud-box')) child.style.display = 'none';
                }
            });
        }
        return container;
    }

    function updateSpecialistsUI(items) {
        const container = getContainer('Speciality Categories', 'Categories');
        if (!container) return;
        if (items.length === 0) return container.innerHTML = `<div style="padding:16px; background:#0f172a; border:1px dashed #1e293b; border-radius:12px; color:#64748b; font-size:12px; text-align:center;">No categories added yet.</div>`;

        const grouped = {};
        items.forEach(item => {
            let cat = "General";
            const catMatch = (item.description || '').match(/\[CAT:(.*?)\]/);
            if (catMatch && catMatch[1]) cat = catMatch[1].trim();
            if (!grouped[cat]) grouped[cat] = [];
            grouped[cat].push(item);
        });

        let html = '';
        for (const [catName, doctors] of Object.entries(grouped)) {
            let docsHtml = doctors.map(doc => {
                let spec = "Specialist";
                const specMatch = (doc.description || '').match(/\[SPEC:(.*?)\]/);
                if (specMatch && specMatch[1]) spec = specMatch[1].trim();
                return `
                <div style="display:flex; justify-content:space-between; align-items:center; padding: 12px 0; border-bottom: 1px solid #1e293b;">
                    <div style="display:flex; align-items:center; gap:12px;">
                        <div style="font-size:20px;">👨‍⚕️</div>
                        <div>
                            <div style="color:white; font-size:14px; font-weight:600;">${doc.title}</div>
                            <div style="color:#94a3b8; font-size:12px;">${spec}</div>
                        </div>
                    </div>
                    <a href="${BOT_URL}" target="_blank" style="background:#0284c7; color:white; padding:6px 16px; border-radius:8px; font-size:12px; font-weight:bold; text-decoration:none;">Book</a>
                </div>`;
            }).join('');
            
            html += `
            <details style="background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; margin-bottom: 12px; overflow:hidden;">
                <summary style="padding: 16px; cursor: pointer; font-weight: bold; color: white; display:flex; align-items:center; gap:12px; outline:none;">
                    <span style="font-size:18px;">📁</span> <span style="flex-grow:1;">${catName}</span>
                    <span style="background: #1e293b; color:#cbd5e1; padding: 2px 8px; border-radius: 12px; font-size: 11px;">${doctors.length} Doctors</span>
                </summary>
                <div style="padding: 0 16px 8px 16px; background: #0b1120;">${docsHtml}</div>
            </details>`;
        }
        container.innerHTML = html;
    }

    function updateProductsUI(items) {
        const container = getContainer('Digital Medical Store', 'Products');
        if (!container) return;
        if (items.length === 0) return container.innerHTML = `<div style="padding:16px; background:#0f172a; border:1px dashed #1e293b; border-radius:12px; color:#64748b; font-size:12px; text-align:center;">No products added yet.</div>`;

        container.innerHTML = items.map(item => {
            let price = "";
            const priceMatch = (item.description || '').match(/\[PRICE:(.*?)\]/);
            if (priceMatch && priceMatch[1]) price = priceMatch[1].trim();
            const desc = (item.description || '').replace(/\[.*?\]/g, '').trim();

            return `
            <div style="display:flex; justify-content:space-between; align-items:center; padding: 16px; background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; margin-bottom: 12px;">
                <div style="display:flex; gap:12px; align-items:center;">
                    <div style="width: 48px; height: 48px; background: rgba(147,51,234,0.15); border: 1px solid rgba(147,51,234,0.3); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 22px;">🛒</div>
                    <div>
                        <div style="color:white; font-size:15px; font-weight:bold;">${item.title}</div>
                        ${desc ? `<div style="color:#94a3b8; font-size:12px; margin-top:2px;">${desc}</div>` : ''}
                        ${price ? `<div style="color:#10b981; font-weight:bold; font-size:13px; margin-top:4px;">${price}</div>` : ''}
                    </div>
                </div>
                <a href="${BOT_URL}" target="_blank" style="background:#9333ea; color:white; padding:10px 16px; border-radius:8px; font-weight:bold; font-size:13px; text-decoration:none;">Buy Now</a>
            </div>`;
        }).join('');
    }

    function updateChannelsUI(items) {
        const container = getContainer('Channels & Groups', 'Channels');
        if (!container) return;
        if (items.length === 0) return container.innerHTML = `<div style="padding:16px; background:#0f172a; border:1px dashed #1e293b; border-radius:12px; color:#64748b; font-size:12px; text-align:center;">No channels added yet.</div>`;

        container.innerHTML = items.map(item => {
            const isPremium = item.is_paid === true;
            let kind = "Channel";
            if ((item.description || '').includes('[KIND:Group]')) kind = "Group";
            
            const badge = isPremium 
                ? `<span style="padding: 2px 6px; font-size: 10px; font-weight: bold; background: rgba(245,158,11,0.2); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); border-radius: 4px;">PREMIUM</span>`
                : `<span style="padding: 2px 6px; font-size: 10px; font-weight: bold; background: rgba(8,145,178,0.2); color: #22d3ee; border: 1px solid rgba(8,145,178,0.3); border-radius: 4px;">FREE</span>`;

            const btn = isPremium
                ? `<a href="${BOT_URL}" target="_blank" style="display: flex; justify-content: center; align-items: center; width: 100%; padding: 10px; background: #f59e0b; color: #1e293b; font-size: 13px; font-weight: bold; border-radius: 8px; text-decoration: none; margin-top: 12px;">⭐ Get Premium Access →</a>`
                : `<a href="${item.link || BOT_URL}" target="_blank" style="display: flex; justify-content: center; align-items: center; width: 100%; padding: 10px; background: #1e293b; color: #22d3ee; font-size: 13px; font-weight: bold; border-radius: 8px; text-decoration: none; border: 1px solid #334155; margin-top: 12px; gap: 6px;">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
                    Join Free ${kind} →
                   </a>`;

            return `
                <div style="padding: 16px; margin-bottom: 12px; background: #0f172a; border: 1px solid #1e293b; border-radius: 12px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="background: #334155; color: #cbd5e1; font-size: 10px; font-weight: bold; padding: 2px 6px; border-radius: 4px; text-transform: uppercase;">${kind}</span>
                        <span style="color: white; font-weight: bold; font-size: 15px; flex-grow: 1;">${item.title}</span>
                        ${badge}
                    </div>
                    ${btn}
                </div>`;
        }).join('');
    }

    syncFromCloud();
    setInterval(syncFromCloud, 3000);
})();
</script>
'''

if '</body>' in content:
    content = content.replace('</body>', script + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Concrete routing fix applied successfully!")
