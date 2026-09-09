import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Remove previous injected core scripts
content = re.sub(r'<!-- SUPABASE [^>]*-->[\s\S]*?</script>', '', content)
content = re.sub(r'<script id="tenaspecial-core">[\s\S]*?</script>', '', content)

script = '''
<!-- SUPABASE SAFE SCHEMA ENGINE -->
<script id="tenaspecial-core">
(function() {
    try { localStorage.clear(); sessionStorage.clear(); } catch(e){}

    const SUPABASE_URL = "https://xbuhtrxhzpjiiiqeluhh.supabase.co";
    const API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhidWh0cnhoenBqaWlpcWVsdWhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODg4ODE4ODgsImV4cCI6MjEwNDQ1Nzg4OH0.s0tBaDZJs5_RxVtgDf5M50owUbeEIcrCciLk4FTYXNc";
    const BOT_URL = "https://t.me/tenaspecial_bot";

    if (!window.supabase) return;
    const db = window.supabase.createClient(SUPABASE_URL, API_KEY);

    // Inject Tabbed UI Modal
    function injectProModalUI() {
        let proForm = document.getElementById('ts-pro-admin-forms');
        if (!proForm) {
            proForm = document.createElement('div');
            proForm.id = 'ts-pro-admin-forms';
            proForm.className = 'p-4 bg-slate-900 border border-slate-800 rounded-2xl my-4 text-white font-sans';
            
            proForm.innerHTML = `
                <div class="flex gap-2 mb-4 border-b border-slate-800 pb-2">
                    <button id="tab-btn-spec" onclick="switchTsTab('spec')" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-cyan-500 text-slate-950">Add Specialist</button>
                    <button id="tab-btn-store" onclick="switchTsTab('store')" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800 text-slate-300">Digital Store</button>
                    <button id="tab-btn-chan" onclick="switchTsTab('chan')" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800 text-slate-300">Channels & Groups</button>
                </div>

                <!-- SPECIALIST FORM -->
                <div id="ts-form-spec" class="space-y-3">
                    <div>
                        <label class="block text-[11px] font-bold text-slate-400 mb-1">Doctor / Specialist Name</label>
                        <input id="ts-spec-name" type="text" placeholder="e.g. Dr. Abebe Bikila" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500" />
                    </div>
                    <div>
                        <label class="block text-[11px] font-bold text-slate-400 mb-1">Speciality</label>
                        <input id="ts-spec-detail" type="text" placeholder="e.g. Senior Cardiologist" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500" />
                    </div>
                    <div>
                        <label class="block text-[11px] font-bold text-slate-400 mb-1">Speciality Category</label>
                        <input id="ts-spec-cat" type="text" placeholder="e.g. Cardiology, Pediatrics" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500" />
                    </div>
                    <button onclick="window.submitSpecialist()" class="w-full py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black text-xs rounded-xl transition-all shadow-lg shadow-cyan-500/20">
                        + Add Specialist
                    </button>
                </div>

                <!-- STORE PRODUCT FORM -->
                <div id="ts-form-store" class="space-y-3 hidden">
                    <div>
                        <label class="block text-[11px] font-bold text-slate-400 mb-1">Product Name</label>
                        <input id="ts-prod-name" type="text" placeholder="e.g. Pediatric Medical Guide" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-purple-500" />
                    </div>
                    <div>
                        <label class="block text-[11px] font-bold text-slate-400 mb-1">Description</label>
                        <input id="ts-prod-desc" type="text" placeholder="Brief details about the product" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-purple-500" />
                    </div>
                    <div>
                        <label class="block text-[11px] font-bold text-slate-400 mb-1">Price (ETB)</label>
                        <input id="ts-prod-price" type="number" placeholder="e.g. 250" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-purple-500" />
                    </div>
                    <button onclick="window.submitProduct()" class="w-full py-2.5 bg-purple-600 hover:bg-purple-500 text-white font-black text-xs rounded-xl transition-all shadow-lg shadow-purple-500/20">
                        + Add Store Product
                    </button>
                </div>

                <!-- CHANNELS & GROUPS FORM -->
                <div id="ts-form-chan" class="space-y-3 hidden">
                    <div>
                        <label class="block text-[11px] font-bold text-slate-400 mb-1">Channel or Group Name</label>
                        <input id="ts-chan-name" type="text" placeholder="e.g. Health Tips Community" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500" />
                    </div>
                    <div>
                        <label class="block text-[11px] font-bold text-slate-400 mb-1">Description</label>
                        <input id="ts-chan-desc" type="text" placeholder="e.g. Daily medical updates" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500" />
                    </div>
                    <div class="grid grid-cols-2 gap-2">
                        <div>
                            <label class="block text-[11px] font-bold text-slate-400 mb-1">Access Type</label>
                            <select id="ts-chan-access" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-2 py-2 text-xs text-white focus:outline-none">
                                <option value="free">FREE</option>
                                <option value="premium">PREMIUM</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-[11px] font-bold text-slate-400 mb-1">Community Type</label>
                            <select id="ts-chan-kind" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-2 py-2 text-xs text-white focus:outline-none">
                                <option value="channel">Channel</option>
                                <option value="group">Group</option>
                            </select>
                        </div>
                    </div>
                    <div>
                        <label class="block text-[11px] font-bold text-slate-400 mb-1">Telegram Link (For Free Access)</label>
                        <input id="ts-chan-link" type="text" placeholder="https://t.me/yourchannel" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500" />
                    </div>
                    <button onclick="window.submitChannel()" class="w-full py-2.5 bg-blue-600 hover:bg-blue-500 text-white font-black text-xs rounded-xl transition-all shadow-lg shadow-blue-500/20">
                        + Add Channel / Group
                    </button>
                </div>

                <!-- DATABASE CONTROL -->
                <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between items-center">
                    <span class="text-[11px] text-slate-400">Cloud Sync Control</span>
                    <button onclick="window.cloudResetAll()" class="px-3 py-1.5 bg-red-500/20 hover:bg-red-500/40 text-red-400 font-bold text-xs rounded-xl border border-red-500/30">
                        🔥 Clear All Items
                    </button>
                </div>
            `;
            
            const target = document.querySelector('div:has(> input), div[class*="Superadmin"]') || document.body;
            target.prepend(proForm);
        }
    }

    window.switchTsTab = function(tab) {
        ['spec', 'store', 'chan'].forEach(t => {
            const form = document.getElementById('ts-form-' + t);
            const btn = document.getElementById('tab-btn-' + t);
            if (form) form.classList.toggle('hidden', t !== tab);
            if (btn) {
                btn.className = (t === tab)
                    ? "px-3 py-1.5 rounded-lg text-xs font-bold bg-cyan-500 text-slate-950"
                    : "px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800 text-slate-300";
            }
        });
    };

    // Form Submissions (Only standard Supabase columns used)
    window.submitSpecialist = async function() {
        const name = document.getElementById('ts-spec-name')?.value.trim();
        const spec = document.getElementById('ts-spec-detail')?.value.trim();
        const cat = document.getElementById('ts-spec-cat')?.value.trim() || 'General Medicine';

        if (!name || !spec) return alert("Please enter Specialist Name and Speciality!");

        const payload = {
            title: name,
            description: `[TYPE:specialist] [CAT:${cat}] ${spec}`,
            link: BOT_URL,
            is_paid: false
        };

        const { error } = await db.from('channels').insert([payload]);
        if (error) alert("Save Error: " + error.message);
        else {
            alert("Specialist saved successfully!");
            document.getElementById('ts-spec-name').value = '';
            document.getElementById('ts-spec-detail').value = '';
            window.syncProCloud();
        }
    };

    window.submitProduct = async function() {
        const name = document.getElementById('ts-prod-name')?.value.trim();
        const desc = document.getElementById('ts-prod-desc')?.value.trim() || 'Digital Medical Product';
        const price = document.getElementById('ts-prod-price')?.value.trim();

        if (!name) return alert("Please enter Product Name!");

        const payload = {
            title: name,
            description: `[TYPE:product] ${desc}${price ? ' - ' + price + ' ETB' : ''}`,
            link: BOT_URL,
            is_paid: true
        };

        const { error } = await db.from('channels').insert([payload]);
        if (error) alert("Save Error: " + error.message);
        else {
            alert("Digital Product saved successfully!");
            document.getElementById('ts-prod-name').value = '';
            document.getElementById('ts-prod-price').value = '';
            window.syncProCloud();
        }
    };

    window.submitChannel = async function() {
        const name = document.getElementById('ts-chan-name')?.value.trim();
        const desc = document.getElementById('ts-chan-desc')?.value.trim() || 'Community';
        const access = document.getElementById('ts-chan-access')?.value || 'free';
        const kind = document.getElementById('ts-chan-kind')?.value || 'channel';
        const link = document.getElementById('ts-chan-link')?.value.trim();

        if (!name) return alert("Please enter Channel/Group Name!");

        const isPremium = access === 'premium';
        let finalLink = BOT_URL;
        if (!isPremium && link) {
            finalLink = link.startsWith('http') ? link : ('https://' + link.replace(/^@/, 't.me/'));
        }

        const payload = {
            title: name,
            description: `[TYPE:${kind}] ${desc}`,
            link: finalLink,
            is_paid: isPremium
        };

        const { error } = await db.from('channels').insert([payload]);
        if (error) alert("Save Error: " + error.message);
        else {
            alert("Saved successfully!");
            document.getElementById('ts-chan-name').value = '';
            document.getElementById('ts-chan-link').value = '';
            window.syncProCloud();
        }
    };

    window.cloudDeleteItem = async function(id) {
        if (!confirm("Delete item?")) return;
        const { error } = await db.from('channels').delete().eq('id', id);
        if (error) alert("Delete Error: " + error.message);
        else window.syncProCloud();
    };

    window.cloudResetAll = async function() {
        if (!confirm("Reset database completely across all browsers?")) return;
        const { error } = await db.from('channels').delete().neq('id', '00000000-0000-0000-0000-000000000000');
        if (error) alert("Reset Error: " + error.message);
        else {
            alert("Database reset!");
            window.syncProCloud();
        }
    };

    // Rendering Engine
    window.syncProCloud = async function() {
        try {
            await db.from('channels').delete().is('title', null);
            await db.from('channels').delete().eq('title', 'undefined');

            const { data, error } = await db.from('channels').select('*').order('created_at', { ascending: false });
            if (error) return;

            const items = (data || []).filter(i => i && i.title && i.title !== 'undefined');

            renderSpecialistsModule(items.filter(i => (i.description && i.description.includes('[TYPE:specialist]')) || i.type === 'specialist'));
            renderStoreModule(items.filter(i => (i.description && i.description.includes('[TYPE:product]')) || i.type === 'product'));
            renderChannelsModule(items.filter(i => (i.description && (i.description.includes('[TYPE:channel]') || i.description.includes('[TYPE:group]'))) || i.type === 'channel' || i.type === 'group' || (!i.description || !i.description.includes('[TYPE:'))));
            renderAdminManageList(items);

        } catch (e) {}
    };

    function renderSpecialistsModule(specs) {
        const header = findHeader('specialities') || findHeader('specialist') || findHeader('categories');
        if (!header || !header.parentElement) return;
        const parent = header.parentElement;
        let container = getOrCreateContainer(parent, 'ts-pro-specialists-list');

        if (specs.length === 0) {
            container.innerHTML = '<div class="p-4 text-slate-400 text-xs text-center border border-dashed border-slate-800 rounded-2xl">No specialists registered yet.</div>';
            return;
        }

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
                <div class="mb-4 p-4 rounded-2xl bg-slate-900/80 border border-slate-800">
                    <h3 class="text-cyan-400 font-bold text-sm mb-3 flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-cyan-400"></span> ${catName}
                    </h3>
                    <div class="space-y-2">
                        ${doctors.map(d => {
                            const cleanDesc = (d.description || '').replace(/\[TYPE:.*?\]/g, '').replace(/\[CAT:.*?\]/g, '').trim();
                            return `
                                <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                                    <div>
                                        <h4 class="text-white font-bold text-sm">${d.title}</h4>
                                        <p class="text-xs text-slate-400">${cleanDesc}</p>
                                    </div>
                                    <a href="${BOT_URL}" target="_blank" class="px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 text-slate-950 font-extrabold text-xs rounded-xl no-underline shadow-lg shadow-cyan-500/20">
                                        Book Now ➔
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

    function renderStoreModule(prods) {
        const header = findHeader('store') || findHeader('products');
        if (!header || !header.parentElement) return;
        const parent = header.parentElement;
        let container = getOrCreateContainer(parent, 'ts-pro-store-list');

        if (prods.length === 0) {
            container.innerHTML = '<div class="p-4 text-slate-400 text-xs text-center border border-dashed border-slate-800 rounded-2xl">No products registered yet.</div>';
            return;
        }

        container.innerHTML = prods.map(p => {
            const cleanDesc = (p.description || '').replace(/\[TYPE:.*?\]/g, '').trim();
            return `
                <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-between my-2">
                    <div>
                        <h4 class="text-white font-bold text-sm">${p.title}</h4>
                        <p class="text-xs text-slate-400">${cleanDesc || 'Medical Resource'}</p>
                    </div>
                    <a href="${BOT_URL}" target="_blank" class="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs rounded-xl no-underline shadow-lg shadow-purple-500/20">
                        Buy Now ➔
                    </a>
                </div>
            `;
        }).join('');
    }

    function renderChannelsModule(chans) {
        const header = findHeader('channels') || findHeader('groups');
        if (!header || !header.parentElement) return;
        const parent = header.parentElement;
        let container = getOrCreateContainer(parent, 'ts-pro-channels-list');

        if (chans.length === 0) {
            container.innerHTML = '<div class="p-4 text-slate-400 text-xs text-center border border-dashed border-slate-800 rounded-2xl">No channels or groups registered yet.</div>';
            return;
        }

        container.innerHTML = chans.map(c => {
            const isPremium = c.is_paid === true;
            const linkUrl = isPremium ? BOT_URL : (c.link || BOT_URL);
            const cleanDesc = (c.description || '').replace(/\[TYPE:.*?\]/g, '').trim();
            const badge = isPremium 
                ? '<span class="px-2 py-0.5 text-[10px] font-bold rounded-md bg-amber-500/20 text-amber-400 border border-amber-500/30">PREMIUM</span>'
                : '<span class="px-2 py-0.5 text-[10px] font-bold rounded-md bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">FREE</span>';

            return `
                <div class="p-4 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-between my-2">
                    <div>
                        <div class="flex items-center gap-2 mb-1">
                            <h4 class="text-white font-bold text-sm">${c.title}</h4>
                            ${badge}
                        </div>
                        <p class="text-xs text-slate-400">${cleanDesc || 'Community'}</p>
                    </div>
                    <a href="${linkUrl}" target="_blank" class="px-4 py-2 ${isPremium ? 'bg-amber-500 text-slate-950' : 'bg-cyan-500 text-slate-950'} font-bold text-xs rounded-xl no-underline">
                        Join Now
                    </a>
                </div>
            `;
        }).join('');
    }

    function renderAdminManageList(items) {
        let listElem = document.getElementById('ts-admin-cloud-items');
        if (!listElem) {
            listElem = document.createElement('div');
            listElem.id = 'ts-admin-cloud-items';
            listElem.className = 'mt-3 space-y-2 max-h-48 overflow-y-auto p-2 bg-slate-950 rounded-xl border border-slate-800';
            const form = document.getElementById('ts-pro-admin-forms');
            if (form) form.appendChild(listElem);
        }

        if (items.length === 0) {
            listElem.innerHTML = '<div class="text-xs text-slate-500 text-center py-2">No saved items in database.</div>';
            return;
        }

        listElem.innerHTML = items.map(i => {
            const cleanDesc = (i.description || '').replace(/\[TYPE:.*?\]/g, '').replace(/\[CAT:.*?\]/g, '').trim();
            return `
                <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-between gap-2">
                    <div class="truncate">
                        <div class="text-xs font-bold text-white truncate">${i.title}</div>
                        <div class="text-[10px] text-slate-400 truncate">${cleanDesc || 'Item'}</div>
                    </div>
                    <button onclick="window.cloudDeleteItem('${i.id}')" class="px-2 py-1 bg-red-500/20 text-red-400 font-bold text-[10px] rounded-lg border border-red-500/30">
                        Remove
                    </button>
                </div>
            `;
        }).join('');
    }

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
        return container;
    }

    setInterval(injectProModalUI, 1000);
    setInterval(window.syncProCloud, 3000);
    window.syncProCloud();
})();
</script>
'''

if '</body>' in content:
    content = content.replace('</body>', script + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Schema fix successfully applied!")
