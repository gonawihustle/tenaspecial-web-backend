import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Strip any previous injection scripts
content = re.sub(r'<!-- SUPABASE [^>]*-->[\s\S]*?</script>', '', content)
content = re.sub(r'<script id="tenaspecial-core">[\s\S]*?</script>', '', content)

script = '''
<!-- TENASPECIAL NATIVE ROUTING ENGINE -->
<script id="tenaspecial-core">
(function() {
    try { localStorage.clear(); sessionStorage.clear(); } catch(e){}

    const SUPABASE_URL = "https://xbuhtrxhzpjiiiqeluhh.supabase.co";
    const API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhidWh0cnhoenBqaWlpcWVsdWhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODg4ODE4ODgsImV4cCI6MjEwNDQ1Nzg4OH0.s0tBaDZJs5_RxVtgDf5M50owUbeEIcrCciLk4FTYXNc";
    const BOT_URL = "https://t.me/tenaspecial_bot";

    if (!window.supabase) return;
    const db = window.supabase.createClient(SUPABASE_URL, API_KEY);

    // Form Submission Handlers
    window.submitSpecialist = async function() {
        const nameInput = document.getElementById('ts-spec-name') || document.querySelector('input[placeholder*="Abebe"], input[placeholder*="Doctor"], input[placeholder*="Name"]');
        const specInput = document.getElementById('ts-spec-detail') || document.querySelectorAll('input[type="text"]')[1];
        const catInput = document.getElementById('ts-spec-cat');

        const name = nameInput ? nameInput.value.trim() : '';
        const spec = specInput ? specInput.value.trim() : '';
        const cat = (catInput && catInput.value.trim()) ? catInput.value.trim() : 'OBGYN';

        if (!name) return alert("Please enter Specialist Name!");

        const payload = {
            title: name,
            description: `[TYPE:specialist][CAT:${cat}] ${spec || 'Specialist Doctor'}`,
            link: BOT_URL,
            is_paid: false
        };

        const { error } = await db.from('channels').insert([payload]);
        if (error) alert("Error saving specialist: " + error.message);
        else {
            alert("Specialist saved successfully!");
            if (nameInput) nameInput.value = '';
            if (specInput) specInput.value = '';
            if (catInput) catInput.value = '';
            window.syncTenaspecialHub();
        }
    };

    window.submitProduct = async function() {
        const nameInput = document.getElementById('ts-prod-name');
        const descInput = document.getElementById('ts-prod-desc');
        const priceInput = document.getElementById('ts-prod-price');

        const name = nameInput ? nameInput.value.trim() : '';
        const desc = descInput ? descInput.value.trim() : 'Medical Resource';
        const price = priceInput ? priceInput.value.trim() : '';

        if (!name) return alert("Please enter Product Name!");

        const payload = {
            title: name,
            description: `[TYPE:product] ${desc}${price ? ' - ' + price + ' ETB' : ''}`,
            link: BOT_URL,
            is_paid: true
        };

        const { error } = await db.from('channels').insert([payload]);
        if (error) alert("Error saving product: " + error.message);
        else {
            alert("Product saved successfully!");
            if (nameInput) nameInput.value = '';
            if (descInput) descInput.value = '';
            if (priceInput) priceInput.value = '';
            window.syncTenaspecialHub();
        }
    };

    window.submitChannel = async function() {
        const nameInput = document.getElementById('ts-chan-name');
        const descInput = document.getElementById('ts-chan-desc');
        const accessSelect = document.getElementById('ts-chan-access');
        const kindSelect = document.getElementById('ts-chan-kind');
        const linkInput = document.getElementById('ts-chan-link');

        const name = nameInput ? nameInput.value.trim() : '';
        const desc = descInput ? descInput.value.trim() : 'Community Channel';
        const access = accessSelect ? accessSelect.value : 'free';
        const kind = kindSelect ? kindSelect.value : 'channel';
        const link = linkInput ? linkInput.value.trim() : '';

        if (!name) return alert("Please enter Channel / Group Name!");

        const isPremium = access.toLowerCase() === 'premium';
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
        if (error) alert("Error saving channel: " + error.message);
        else {
            alert("Channel saved successfully!");
            if (nameInput) nameInput.value = '';
            if (descInput) descInput.value = '';
            if (linkInput) linkInput.value = '';
            window.syncTenaspecialHub();
        }
    };

    window.cloudDeleteItem = async function(id) {
        if (!confirm("Remove this item?")) return;
        const { error } = await db.from('channels').delete().eq('id', id);
        if (error) alert("Delete Error: " + error.message);
        else window.syncTenaspecialHub();
    };

    // Main Renderer and Section Router
    window.syncTenaspecialHub = async function() {
        try {
            // Clean empty entries
            await db.from('channels').delete().is('title', null);

            const { data, error } = await db.from('channels').select('*').order('created_at', { ascending: false });
            if (error) return;

            const items = data || [];

            // Classify Items
            const specialists = [];
            const products = [];
            const channels = [];

            items.forEach(item => {
                const desc = item.description || '';
                if (desc.includes('[TYPE:specialist]') || item.type === 'specialist') {
                    specialists.push(item);
                } else if (desc.includes('[TYPE:product]') || item.type === 'product') {
                    products.push(item);
                } else {
                    channels.push(item);
                }
            });

            renderSpecialistsSection(specialists);
            renderStoreSection(products);
            renderChannelsSection(channels);
            renderAdminManageList(items);

        } catch (e) {
            console.error("Hub Sync Error:", e);
        }
    };

    function renderSpecialistsSection(specs) {
        const sectionHeader = findSectionHeader('speciality categories');
        if (!sectionHeader) return;

        updateCounterBadge(sectionHeader, specs.length, 'Categories');

        let container = getOrCreateSectionContainer(sectionHeader, 'ts-native-specialists-box');

        if (specs.length === 0) {
            container.innerHTML = `<div class="p-4 text-slate-500 text-xs text-center border border-dashed border-slate-800 rounded-2xl my-2">No categories or doctors registered yet.</div>`;
            return;
        }

        // Group doctors by Category
        const categories = {};
        specs.forEach(s => {
            let cat = "OBGYN";
            if (s.description && s.description.includes('[CAT:')) {
                const match = s.description.match(/\[CAT:(.*?)\]/);
                if (match && match[1]) cat = match[1].trim();
            }
            if (!categories[cat]) categories[cat] = [];
            categories[cat].push(s);
        });

        let html = '';
        for (const [catName, doctors] of Object.entries(categories)) {
            html += `
                <div class="my-3 p-4 rounded-2xl bg-slate-900/90 border border-slate-800/80 shadow-xl">
                    <div class="flex items-center justify-between mb-3 border-b border-slate-800 pb-2">
                        <h3 class="text-cyan-400 font-bold text-sm flex items-center gap-2">
                            <span class="w-2.5 h-2.5 rounded-full bg-cyan-400"></span> ${catName}
                        </h3>
                        <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-300 border border-cyan-500/20">${doctors.length} Specialist${doctors.length > 1 ? 's' : ''}</span>
                    </div>
                    <div class="space-y-2">
                        ${doctors.map(d => {
                            const cleanDesc = (d.description || '').replace(/\[TYPE:.*?\]/g, '').replace(/\[CAT:.*?\]/g, '').trim();
                            return `
                                <div class="p-3 rounded-xl bg-slate-950/80 border border-slate-800 flex items-center justify-between gap-3">
                                    <div>
                                        <div class="text-white font-bold text-sm">${d.title}</div>
                                        <div class="text-xs text-slate-400">${cleanDesc || 'Consultant Doctor'}</div>
                                    </div>
                                    <a href="${BOT_URL}" target="_blank" class="px-3.5 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-black text-xs rounded-xl no-underline transition-all shadow-md shadow-cyan-500/20 whitespace-nowrap">
                                        Book Specialist 🩺
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

    function renderStoreSection(prods) {
        const sectionHeader = findSectionHeader('digital medical store');
        if (!sectionHeader) return;

        updateCounterBadge(sectionHeader, prods.length, 'Products');

        let container = getOrCreateSectionContainer(sectionHeader, 'ts-native-store-box');

        if (prods.length === 0) {
            container.innerHTML = `<div class="p-4 text-slate-500 text-xs text-center border border-dashed border-slate-800 rounded-2xl my-2">No store products added yet.</div>`;
            return;
        }

        container.innerHTML = prods.map(p => {
            const cleanDesc = (p.description || '').replace(/\[TYPE:.*?\]/g, '').trim();
            return `
                <div class="my-2 p-4 rounded-2xl bg-slate-900/90 border border-slate-800 flex items-center justify-between gap-3 shadow-xl">
                    <div>
                        <div class="text-white font-bold text-sm">${p.title}</div>
                        <div class="text-xs text-slate-400 mt-0.5">${cleanDesc || 'Medical Resource'}</div>
                    </div>
                    <a href="${BOT_URL}" target="_blank" class="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs rounded-xl no-underline transition-all shadow-md shadow-purple-500/20 whitespace-nowrap">
                        Buy Product 🛍️
                    </a>
                </div>
            `;
        }).join('');
    }

    function renderChannelsSection(chans) {
        const sectionHeader = findSectionHeader('channels & groups');
        if (!sectionHeader) return;

        updateCounterBadge(sectionHeader, chans.length, 'Channels');

        let container = getOrCreateSectionContainer(sectionHeader, 'ts-native-channels-box');

        // Hide old static or unrouted elements under this section
        const parent = sectionHeader.parentElement;
        if (parent) {
            Array.from(parent.children).forEach(child => {
                if (child !== container && child !== sectionHeader && !child.contains(sectionHeader)) {
                    if (child.className && (child.className.includes('border') || child.className.includes('p-4') || child.className.includes('rounded'))) {
                        child.style.display = 'none';
                    }
                }
            });
        }

        if (chans.length === 0) {
            container.innerHTML = `<div class="p-4 text-slate-500 text-xs text-center border border-dashed border-slate-800 rounded-2xl my-2">No channels or groups added yet.</div>`;
            return;
        }

        container.innerHTML = chans.map(c => {
            const desc = c.description || '';
            const isPremium = c.is_paid === true || desc.toLowerCase().includes('premium');
            const cleanDesc = desc.replace(/\[TYPE:.*?\]/g, '').trim();
            
            const badgeHtml = isPremium 
                ? `<span class="px-2 py-0.5 text-[10px] font-black rounded-md bg-amber-500/20 text-amber-400 border border-amber-500/30">PREMIUM</span>`
                : `<span class="px-2 py-0.5 text-[10px] font-black rounded-md bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">FREE</span>`;

            const actionBtn = isPremium
                ? `<a href="${BOT_URL}" target="_blank" class="px-4 py-2 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-black text-xs rounded-xl no-underline transition-all shadow-md shadow-amber-500/20 whitespace-nowrap">
                        Unlock Premium Access 🔒
                   </a>`
                : `<a href="${c.link || BOT_URL}" target="_blank" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-cyan-400 font-bold text-xs rounded-xl no-underline transition-all border border-cyan-500/20 whitespace-nowrap">
                        Join Free Channel →
                   </a>`;

            return `
                <div class="my-2 p-4 rounded-2xl bg-slate-900/90 border border-slate-800 flex items-center justify-between gap-3 shadow-xl">
                    <div>
                        <div class="flex items-center gap-2 mb-1">
                            <span class="text-white font-bold text-sm">${c.title}</span>
                            ${badgeHtml}
                        </div>
                        <div class="text-xs text-slate-400">${cleanDesc || 'Telegram Community'}</div>
                    </div>
                    ${actionBtn}
                </div>
            `;
        }).join('');
    }

    function renderAdminManageList(items) {
        let listContainer = document.getElementById('ts-cloud-admin-list');
        if (!listContainer) {
            listContainer = document.createElement('div');
            listContainer.id = 'ts-cloud-admin-list';
            listContainer.className = 'mt-4 p-3 bg-slate-950 border border-slate-800 rounded-xl space-y-2 max-h-52 overflow-y-auto';
            const adminModal = document.querySelector('div:has(> input), form, [class*="Admin"], [class*="admin"]');
            if (adminModal) adminModal.appendChild(listContainer);
        }

        if (items.length === 0) {
            listContainer.innerHTML = '<div class="text-xs text-slate-500 text-center py-2">No database items found.</div>';
            return;
        }

        listContainer.innerHTML = `
            <div class="text-[11px] font-bold text-slate-400 border-b border-slate-800 pb-1 mb-2">Database Items (${items.length})</div>
            ${items.map(i => {
                const cleanDesc = (i.description || '').replace(/\[TYPE:.*?\]/g, '').replace(/\[CAT:.*?\]/g, '').trim();
                return `
                    <div class="p-2 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-between text-xs gap-2">
                        <div class="truncate">
                            <div class="font-bold text-white truncate">${i.title}</div>
                            <div class="text-[10px] text-slate-400 truncate">${cleanDesc || 'Item'}</div>
                        </div>
                        <button onclick="window.cloudDeleteItem('${i.id}')" class="px-2 py-1 bg-red-500/20 hover:bg-red-500/40 text-red-400 text-[10px] font-bold rounded-lg border border-red-500/30 whitespace-nowrap">
                            Remove
                        </button>
                    </div>
                `;
            }).join('')}
        `;
    }

    function findSectionHeader(titleText) {
        const allElements = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, div'));
        return allElements.find(el => el.children.length === 0 && el.textContent.trim().toLowerCase().includes(titleText));
    }

    function updateCounterBadge(headerEl, count, labelSingular) {
        const row = headerEl.parentElement;
        if (!row) return;
        const counterEl = Array.from(row.querySelectorAll('span, div')).find(e => e !== headerEl && e.textContent.toLowerCase().includes(labelSingular.toLowerCase()));
        if (counterEl) {
            counterEl.textContent = `${count} ${labelSingular}`;
        }
    }

    function getOrCreateSectionContainer(headerEl, id) {
        let container = document.getElementById(id);
        if (!container) {
            container = document.createElement('div');
            container.id = id;
            container.className = 'w-full my-2 space-y-2';
            
            // Insert after section header row
            const targetParent = headerEl.closest('div.flex') || headerEl.parentElement;
            if (targetParent && targetParent.parentElement) {
                targetParent.parentElement.insertBefore(container, targetParent.nextSibling);
            } else {
                headerEl.insertAdjacentElement('afterend', container);
            }
        }
        return container;
    }

    // Sync on Load and Interval
    setInterval(window.syncTenaspecialHub, 2500);
    window.syncTenaspecialHub();
})();
</script>
'''

if '</body>' in content:
    content = content.replace('</body>', script + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print(" Native section router script applied!")
