import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Strip out the entire previous floating button and ugly UI injection
content = re.sub(r'<script id="tenaspecial-core">[\s\S]*?</script>', '', content)

script = '''
<!-- TENASPECIAL INVISIBLE CLOUD HOOK -->
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

    async function tsPush(payload) {
        try {
            const res = await fetch(SUPA_URL, { method: "POST", headers: HEADERS, body: JSON.stringify(payload) });
            if (res.ok) {
                tsFetchAndRender();
            } else {
                alert("Database Error: Could not save.");
            }
        } catch(e) { console.error("Network error"); }
    }

    // 1. HOOK DIRECTLY INTO YOUR SUPERADMIN PANEL BUTTONS
    document.addEventListener('click', async (e) => {
        const btn = e.target.closest('button');
        if (!btn) return;
        
        const text = btn.innerText.trim();
        
        // Listen for YOUR exact Channel Save button
        if (text === 'Save Channel / Group') {
            e.preventDefault();
            const inputs = Array.from(document.querySelectorAll('input, select, textarea'));
            
            const name = inputs.find(i => i.placeholder && i.placeholder.includes('Channel Name (EN)'))?.value 
                      || inputs.find(i => i.placeholder && i.placeholder.includes('Channel Name'))?.value;
            const desc = inputs.find(i => i.placeholder && i.placeholder.includes('Description (EN)'))?.value || '';
            const link = inputs.find(i => i.placeholder && i.placeholder.includes('Telegram Link'))?.value || '';
            const dropdown = inputs.find(i => i.tagName === 'SELECT' && i.options.length > 0 && i.options[0].text.includes('FREE'));
            
            const isPremium = dropdown && dropdown.value.toUpperCase().includes('PREMIUM');
            
            if (name) {
                await tsPush({ title: name, description: `[TYPE:channel] ${desc}`, link: link || BOT_URL, is_paid: isPremium });
                inputs.forEach(i => { if(i.tagName !== 'SELECT') i.value = ''; });
                alert("✅ Channel Saved to Cloud!");
            }
        }
        // Listen for YOUR exact Specialist Save button
        else if (text === 'Save Specialist to Category') {
            e.preventDefault();
            const inputs = Array.from(document.querySelectorAll('input, select, textarea'));
            
            const docName = inputs.find(i => i.placeholder && i.placeholder.includes('Doctor Name (EN)'))?.value 
                         || inputs.find(i => i.placeholder && i.placeholder.includes('Doctor Name'))?.value;
            const spec = inputs.find(i => i.placeholder && i.placeholder.includes('Speciality (EN)'))?.value || '';
            const customCat = inputs.find(i => i.placeholder && i.placeholder.includes('Category Name'))?.value;
            
            // Find category dropdown
            const catDropdown = inputs.find(i => i.tagName === 'SELECT' && i.options.length > 0 && i.options[0].text.includes('Select'));
            const finalCat = customCat || (catDropdown ? catDropdown.value : '') || 'Consultant';
            
            if (docName) {
                await tsPush({ title: docName, description: `[TYPE:specialist][CAT:${finalCat}] ${spec}`, link: BOT_URL, is_paid: false });
                inputs.forEach(i => { if(i.tagName !== 'SELECT') i.value = ''; });
                alert("✅ Specialist Saved to Cloud!");
            }
        }
        // Listen for YOUR Clear All button
        else if (text.includes('Clear All') && btn.closest('div') && btn.closest('div').innerText.includes('Manage Saved Items')) {
            e.preventDefault();
            if(confirm("Are you sure you want to completely wipe the cloud database?")) {
                await fetch(SUPA_URL + '?title=not.is.null', { method: 'DELETE', headers: HEADERS });
                alert('☁️ Cloud Cleared');
                tsFetchAndRender();
            }
        }
    });

    // 2. RENDER THE EXACT "COOL BUTTONS" WHERE THEY BELONG
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

        } catch(e) {}
    };

    function updateUISection(headerText, items, countLabel, renderFunc) {
        const headers = Array.from(document.querySelectorAll('h2, h3, h4, div'));
        const header = headers.find(el => el.children.length === 0 && el.textContent.trim().toLowerCase() === headerText.toLowerCase());
        if (!header) return;

        const parentRow = header.closest('div.flex') || header.parentElement;
        
        // Update the counts automatically
        if (parentRow) {
            const counter = Array.from(parentRow.querySelectorAll('span, div')).find(el => el.textContent.includes(countLabel));
            if (counter) counter.textContent = `${items.length} ${countLabel}`;
        }

        let container = document.getElementById('ts-cloud-box-' + countLabel);
        if (!container) {
            container = document.createElement('div');
            container.id = 'ts-cloud-box-' + countLabel;
            container.style.width = '100%';
            container.style.marginTop = '12px';
            if (parentRow && parentRow.nextSibling) {
                parentRow.parentElement.insertBefore(container, parentRow.nextSibling);
            } else if (parentRow) {
                parentRow.parentElement.appendChild(container);
            }
        }

        // Hide old empty state boxes
        if (parentRow && parentRow.parentElement) {
            Array.from(parentRow.parentElement.children).forEach(child => {
                if (child !== parentRow && child !== container && child.textContent.includes('No ') && child.tagName === 'DIV') {
                    child.style.display = 'none';
                }
            });
        }

        if (items.length === 0) {
            container.innerHTML = `<div style="padding:16px; background:#0f172a; border:1px dashed #1e293b; border-radius:16px; color:#64748b; font-size:12px; text-align:center;">No items added yet.</div>`;
            return;
        }

        container.innerHTML = items.map(renderFunc).join('');
    }

    // THE ORIGINAL "COOL BUTTON" DESIGN
    function renderChannelHTML(item) {
        const cleanDesc = (item.description || '').replace(/\[TYPE:.*?\]/g, '').trim();
        const isPremium = item.is_paid === true;
        
        const badge = isPremium 
            ? `<span style="padding: 2px 6px; font-size: 10px; font-weight: bold; background: rgba(245,158,11,0.2); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); border-radius: 4px;">PREMIUM</span>`
            : `<span style="padding: 2px 6px; font-size: 10px; font-weight: bold; background: rgba(8,145,178,0.2); color: #22d3ee; border: 1px solid rgba(8,145,178,0.3); border-radius: 4px;">FREE</span>`;

        const btn = isPremium
            ? `<a href="${BOT_URL}" target="_blank" style="display: flex; justify-content: center; align-items: center; width: 100%; padding: 10px; background: #f59e0b; color: #1e293b; font-size: 13px; font-weight: bold; border-radius: 8px; text-decoration: none; margin-top: 12px;">⭐ Get Premium Access →</a>`
            : `<a href="${item.link || BOT_URL}" target="_blank" style="display: flex; justify-content: center; align-items: center; width: 100%; padding: 10px; background: #1e293b; color: #22d3ee; font-size: 13px; font-weight: bold; border-radius: 8px; text-decoration: none; border: 1px solid #334155; margin-top: 12px; gap: 6px; transition: all 0.2s;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
                Join Free Channel →
               </a>`;

        return `
            <div style="padding: 16px; margin-bottom: 12px; background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; font-family: sans-serif;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span style="background: #334155; color: #cbd5e1; font-size: 10px; font-weight: bold; padding: 2px 6px; border-radius: 4px; text-transform: uppercase;">Channel</span>
                    <span style="color: white; font-weight: bold; font-size: 14px; flex-grow: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${item.title}</span>
                    ${badge}
                </div>
                ${cleanDesc ? `<div style="color: #94a3b8; font-size: 12px; margin-bottom: 4px; line-height: 1.4;">${cleanDesc}</div>` : ''}
                ${btn}
            </div>
        `;
    }

    // ORIGINAL STYLING FOR SPECIALISTS
    function renderSpecialistHTML(item) {
        let cat = "Specialist";
        if (item.description && item.description.includes('[CAT:')) {
            const match = item.description.match(/\[CAT:(.*?)\]/);
            if (match && match[1]) cat = match[1].trim();
        }
        const cleanDesc = (item.description || '').replace(/\[TYPE:.*?\]/g, '').replace(/\[CAT:.*?\]/g, '').trim();

        return `
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 16px; margin-bottom: 12px; background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; font-family: sans-serif;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 40px; height: 40px; background: rgba(2,132,199,0.2); border: 1px solid rgba(2,132,199,0.3); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px;">👨‍⚕️</div>
                    <div>
                        <div style="color: white; font-weight: bold; font-size: 14px;">${item.title}</div>
                        <div style="color: #38bdf8; font-size: 11px; margin-top:2px; font-weight: 600;">${cat} ${cleanDesc ? `• <span style="color:#94a3b8; font-weight:normal;">${cleanDesc}</span>` : ''}</div>
                    </div>
                </div>
                <a href="${BOT_URL}" target="_blank" style="padding: 6px 14px; background: #0284c7; color: white; font-size: 11px; font-weight: bold; border-radius: 8px; text-decoration: none;">Book</a>
            </div>
        `;
    }

    function renderProductHTML(item) {
        const cleanDesc = (item.description || '').replace(/\[TYPE:.*?\]/g, '').trim();
        return `
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 16px; margin-bottom: 12px; background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; font-family: sans-serif;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 40px; height: 40px; background: rgba(147,51,234,0.2); border: 1px solid rgba(147,51,234,0.3); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px;">🛒</div>
                    <div>
                        <div style="color: white; font-weight: bold; font-size: 14px;">${item.title}</div>
                        <div style="color: #c084fc; font-size: 11px; margin-top:2px;">${cleanDesc}</div>
                    </div>
                </div>
                <a href="${BOT_URL}" target="_blank" style="padding: 6px 14px; background: #9333ea; color: white; font-size: 11px; font-weight: bold; border-radius: 8px; text-decoration: none;">Buy</a>
            </div>
        `;
    }

    // Keep it continuously synced seamlessly 
    tsFetchAndRender();
    setInterval(tsFetchAndRender, 3000); 
})();
</script>
'''

if '</body>' in content:
    content = content.replace('</body>', script + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Invisible Superadmin Hook and Cool Buttons successfully restored!")
