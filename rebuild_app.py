import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Clear out any existing custom injection scripts
content = re.sub(r'<!-- SUPABASE [^>]*-->[\s\S]*?</script>', '', content)
content = re.sub(r'<script id="tenaspecial-core">[\s\S]*?</script>', '', content)

script = '''
<!-- SUPABASE PROFESSIONAL ENGINE -->
<script id="tenaspecial-core">
(function() {
    // 1. Purge legacy stuck local storage items
    try {
        localStorage.clear();
        sessionStorage.clear();
    } catch(e){}

    const SUPABASE_URL = "https://xbuhtrxhzpjiiiqeluhh.supabase.co";
    const API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhidWh0cnhoenBqaWlpcWVsdWhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODg4ODE4ODgsImV4cCI6MjEwNDQ1Nzg4OH0.s0tBaDZJs5_RxVtgDf5M50owUbeEIcrCciLk4FTYXNc";

    if (!window.supabase) return;
    const db = window.supabase.createClient(SUPABASE_URL, API_KEY);

    const BOT_URL = "https://t.me/tenaspecial_bot";

    // --- CLOUD DATABASE ACTIONS ---

    // 1. Add Specialist
    window.cloudAddSpecialist = async function(name, speciality, category) {
        if (!name || !speciality) return alert("Please fill in Doctor Name and Speciality");
        const catName = category.trim() || "General Medicine";
        const payload = {
            title: name.trim(),
            description: speciality.trim() + " [CAT:" + catName + "]",
            link: BOT_URL,
            type: 'specialist',
            is_paid: false
        };
        const { error } = await db.from('channels').insert([payload]);
        if (error) alert("Error adding specialist: " + error.message);
        else {
            alert("Specialist registered successfully!");
            window.syncProCloud();
        }
    };

    // 2. Add Digital Store Product
    window.cloudAddProduct = async function(name, desc, price) {
        if (!name) return alert("Please enter Product Name");
        const payload = {
            title: name.trim(),
            description: (desc.trim() || "Digital Medical Resource") + (price ? " - " + price + " ETB" : ""),
            link: BOT_URL,
            type: 'product',
            is_paid: true,
            price: parseFloat(price) || 0
        };
        const { error } = await db.from('channels').insert([payload]);
        if (error) alert("Error adding product: " + error.message);
        else {
            alert("Digital Product added successfully!");
            window.syncProCloud();
        }
    };

    // 3. Add Channel or Group
    window.cloudAddChannelGroup = async function(name, desc, link, isPremium, isGroup) {
        if (!name) return alert("Please enter Channel/Group Name");
        const rawLink = link.trim();
        const finalLink = isPremium ? BOT_URL : (rawLink.startsWith('http') ? rawLink : ('https://' + rawLink.replace(/^@/, 't.me/')));
        
        const payload = {
            title: name.trim(),
            description: desc.trim() || (isGroup ? "Telegram Group" : "Telegram Channel"),
            link: finalLink,
            type: isGroup ? 'group' : 'channel',
            is_paid: isPremium
        };
        const { error } = await db.from('channels').insert([payload]);
        if (error) alert("Error adding item: " + error.message);
        else {
            alert((isGroup ? "Group" : "Channel") + " added successfully!");
            window.syncProCloud();
        }
    };

    // 4. Delete Single Record from DB
    window.cloudDeleteItem = async function(id) {
        if (!confirm("Are you sure you want to permanently delete this item?")) return;
        const { error } = await db.from('channels').delete().eq('id', id);
        if (error) alert("Delete failed: " + error.message);
        else window.syncProCloud();
    };

    // 5. Reset / Clear All Records from DB
    window.cloudResetAll = async function() {
        if (!confirm("WARNING: This will purge ALL saved items across all browsers. Continue?")) return;
        const { error } = await db.from('channels').delete().neq('id', '00000000-0000-0000-0000-000000000000');
        if (error) alert("Reset error: " + error.message);
        else {
            alert("Database reset completely!");
            window.syncProCloud();
        }
    };

    // --- RENDERING ENGINE ---
    window.syncProCloud = async function() {
        try {
            // Delete corrupt rows automatically
            await db.from('channels').delete().is('title', null);
            await db.from('channels').delete().eq('title', 'undefined');

            const { data, error } = await db.from('channels').select('*').order('created_at', { ascending: false });
            if (error) return console.error("Cloud fetch error:", error.message);

            const items = (data || []).filter(i => i && i.title && i.title !== 'undefined');

            // Render Modules
            renderSpecialistsModule(items.filter(i => i.type === 'specialist'));
            renderStoreModule(items.filter(i => i.type === 'product'));
            renderChannelsModule(items.filter(i => i.type === 'channel' || i.type === 'group'));
            renderAdminManageList(items);

        } catch (e) {
            console.error("Sync exception:", e);
        }
    };

    // Specialist Renderer (Grouped by Category)
    function renderSpecialistsModule(specs) {
        const specHeader = findHeader('speciality categories');
        if (!specHeader || !specHeader.parentElement) return;

        const parent = specHeader.parentElement;
        let container = getOrCreateContainer(parent, 'ts-pro-specialists-list');

        if (specs.length === 0) {
            container.innerHTML = '<div class="p-4 text-slate-400 text-xs text-center border border-dashed border-slate-800 rounded-2xl">No specialists registered yet.</div>';
            return;
        }

        // Group specialists by category
        const groups = {};
        specs.forEach(s => {
            let cat = "General Medicine";
            if (s.description && s.description.includes('[CAT:')) {
                const match = s.description.match(/\[CAT:(.*?)\]/);
                if (match && match[1]) cat = match[1].trim();
            }
            if (!groups[cat]) groups[cat] = [];
            groups[cat].push(s);
        });

        let html = '';
        for (const [catName, doctors] of Object.entries(groups)) {
            html += `
                <div class="mb-4 p-4 rounded-2xl bg-slate-900/80 border border-slate-800/80">
                    <h3 class="text-cyan-400 font-bold text-sm mb-3 flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
                        ${catName}
                    </h3>
                    <div class="space-y-2">
                        ${doctors.map(d => {
                            const specText = d.description ? d.description.replace(/\[CAT:.*?\]/, '').trim() : 'Medical Specialist';
                            return `
                                <div class="p-3 rounded-xl bg-slate-950/70 border border-slate-800 flex items-center justify-between">
                                    <div>
                                        <h4 class="text-white font-bold text-sm">${d.title}</h4>
                                        <p class="text-xs text-slate-400">${specText}</p>
                                    </div>
                                    <a href="${BOT_URL}" target="_blank" class="px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-extrabold text-xs rounded-xl no-underline shadow-lg shadow-cyan-500/20 transition-all flex items-center gap-1">
                                        <span>Book Now</span> ➔
                                    </a>
                                </div>
                            `;
                        }).join('')}
                    </div>
                </div>
            `;
        }
        container.innerHTML = html;
    }

    // Digital Store Renderer
    function renderStoreModule(prods) {
        const storeHeader = findHeader('digital medical store');
        if (!storeHeader || !storeHeader.parentElement) return;

        const parent = storeHeader.parentElement;
        let container = getOrCreateContainer(parent, 'ts-pro-store-list');

        if (prods.length === 0) {
            container.innerHTML = '<div class="p-4 text-slate-400 text-xs text-center border border-dashed border-slate-800 rounded-2xl">No store products registered yet.</div>';
            return;
        }

        container.innerHTML = prods.map(p => `
            <div class="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl flex items-center justify-between my-2">
                <div>
                    <h4 class="text-white font-bold text-sm">${p.title}</h4>
                    <p class="text-xs text-slate-400">${p.description || 'Medical Resource'}</p>
                </div>
                <a href="${BOT_URL}" target="_blank" class="px-4 py-2 bg-gradient-to-r from-purple-500 to-indigo-600 hover:from-purple-400 hover:to-indigo-500 text-white font-extrabold text-xs rounded-xl no-underline shadow-lg shadow-purple-500/20 transition-all">
                    Buy Now ➔
                </a>
            </div>
        `).join('');
    }

    // Channels and Groups Renderer
    function renderChannelsModule(chans) {
        const chanHeader = findHeader('channels & groups');
        if (!chanHeader || !chanHeader.parentElement) return;

        const parent = chanHeader.parentElement;
        let container = getOrCreateContainer(parent, 'ts-pro-channels-list');

        if (chans.length === 0) {
            container.innerHTML = '<div class="p-4 text-slate-400 text-xs text-center border border-dashed border-slate-800 rounded-2xl">No channels or groups registered yet.</div>';
            return;
        }

        container.innerHTML = chans.map(c => {
            const isPremium = c.is_paid === true;
            const linkUrl = isPremium ? BOT_URL : (c.link || BOT_URL);
            const badge = isPremium 
                ? '<span class="px-2 py-0.5 text-[10px] font-bold rounded-md bg-amber-500/20 text-amber-400 border border-amber-500/30">PREMIUM</span>'
                : '<span class="px-2 py-0.5 text-[10px] font-bold rounded-md bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">FREE</span>';
            const btnColor = isPremium 
                ? 'bg-amber-500 hover:bg-amber-400 text-slate-950' 
                : 'bg-cyan-500 hover:bg-cyan-400 text-slate-950';

            return `
                <div class="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl flex items-center justify-between my-2">
                    <div>
                        <div class="flex items-center gap-2 mb-1">
                            <h4 class="text-white font-bold text-sm">${c.title}</h4>
                            ${badge}
                        </div>
                        <p class="text-xs text-slate-400">${c.description || (c.type === 'group' ? 'Community Group' : 'Official Channel')}</p>
                    </div>
                    <a href="${linkUrl}" target="_blank" class="px-4 py-2 ${btnColor} font-bold text-xs rounded-xl no-underline transition-all shadow-md shrink-0">
                        Join Now
                    </a>
                </div>
            `;
        }).join('');
    }

    // Admin Manage Items List Renderer
    function renderAdminManageList(items) {
        const manageContainer = document.querySelector('div:has(> button:contains("Clear All")), div[class*="Manage Saved Items"]');
        let listElem = document.getElementById('ts-admin-cloud-items');
        
        if (!listElem) {
            const targetParent = manageContainer || document.body;
            listElem = document.createElement('div');
            listElem.id = 'ts-admin-cloud-items';
            listElem.className = 'mt-4 space-y-2 max-h-60 overflow-y-auto p-2 bg-slate-950/80 rounded-xl border border-slate-800';
            targetParent.appendChild(listElem);
        }

        if (items.length === 0) {
            listElem.innerHTML = '<div class="text-xs text-slate-500 text-center py-2">No saved items in database.</div>';
            return;
        }

        listElem.innerHTML = items.map(i => `
            <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-between gap-2">
                <div class="truncate">
                    <div class="text-xs font-bold text-white truncate">${i.title} <span class="text-[10px] text-cyan-400">(${i.type})</span></div>
                    <div class="text-[10px] text-slate-400 truncate">${i.description || 'No description'}</div>
                </div>
                <button onclick="window.cloudDeleteItem('${i.id}')" class="px-2.5 py-1 bg-red-500/20 hover:bg-red-500/40 text-red-400 font-bold text-[10px] rounded-lg border border-red-500/30 shrink-0">
                    Remove
                </button>
            </div>
        `).join('');
    }

    // Helper functions
    function findHeader(text) {
        return Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, div')).find(e => e.textContent && e.textContent.trim().toLowerCase().includes(text));
    }

    function getOrCreateContainer(parent, id) {
        let container = document.getElementById(id);
        if (!container) {
            container = document.createElement('div');
            container.id = id;
            container.className = 'space-y-3 my-3';
            parent.appendChild(container);
        }
        Array.from(parent.children).forEach(child => {
            if (child !== container && !child.contains(document.querySelector('h1, h2, h3, h4, h5'))) {
                child.style.display = 'none';
            }
        });
        return container;
    }

    // Intercept Form Buttons
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('button, a');
        if (!btn) return;
        const txt = btn.textContent.trim().toLowerCase();

        // Clear All / Reset Button
        if (txt.includes('clear all') || txt.includes('reset database')) {
            e.preventDefault();
            window.cloudResetAll();
            return;
        }

        // Save Specialist
        if (txt.includes('save specialist')) {
            e.preventDefault();
            const docInputs = Array.from(document.querySelectorAll('input')).filter(i => i.placeholder?.toLowerCase().includes('doctor') || i.placeholder?.toLowerCase().includes('name'));
            const specInputs = Array.from(document.querySelectorAll('input')).filter(i => i.placeholder?.toLowerCase().includes('speciality') || i.placeholder?.toLowerCase().includes('specialty'));
            const catSelect = document.querySelector('select');
            const catInput = Array.from(document.querySelectorAll('input')).find(i => i.placeholder?.toLowerCase().includes('category'));

            const name = docInputs[0]?.value || '';
            const spec = specInputs[0]?.value || '';
            const cat = catInput?.value || catSelect?.value || 'General Medicine';

            window.cloudAddSpecialist(name, spec, cat);
            return;
        }

        // Save Digital Product
        if (txt.includes('save digital product') || txt.includes('save product')) {
            e.preventDefault();
            const inputs = Array.from(document.querySelectorAll('input'));
            const name = inputs.find(i => i.placeholder?.toLowerCase().includes('product name'))?.value || '';
            const price = inputs.find(i => i.placeholder?.toLowerCase().includes('price'))?.value || '';
            const desc = inputs.find(i => i.placeholder?.toLowerCase().includes('description'))?.value || '';

            window.cloudAddProduct(name, desc, price);
            return;
        }

        // Save Channel / Group
        if (txt.includes('save channel')) {
            e.preventDefault();
            const inputs = Array.from(document.querySelectorAll('input'));
            const selects = Array.from(document.querySelectorAll('select'));

            const name = inputs.find(i => i.placeholder?.toLowerCase().includes('channel name') || i.placeholder?.toLowerCase().includes('name'))?.value || '';
            const desc = inputs.find(i => i.placeholder?.toLowerCase().includes('description'))?.value || '';
            const link = inputs.find(i => i.placeholder?.toLowerCase().includes('link') || i.placeholder?.toLowerCase().includes('telegram'))?.value || '';

            const accessVal = selects[0]?.value?.toLowerCase() || '';
            const isPremium = accessVal.includes('premium') || accessVal.includes('paid');
            const isGroup = accessVal.includes('group');

            window.cloudAddChannelGroup(name, desc, link, isPremium, isGroup);
            return;
        }
    });

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', window.syncProCloud);
    } else {
        window.syncProCloud();
    }
    setInterval(window.syncProCloud, 3000);
})();
</script>
'''

if '</body>' in content:
    content = content.replace('</body>', script + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Professional Cloud System script successfully created!")
