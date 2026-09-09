import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Clean older scripts
content = re.sub(r'<!-- SUPABASE (FULL CLOUD SYNC|CLOUD ENGINE) FOR CHANNELS -->[\s\S]*?</script>', '', content)
content = re.sub(r'<!-- SUPABASE FULL CLOUD SYNC ENGINE -->[\s\S]*?</script>', '', content)

script = '''
<!-- SUPABASE FULL CLOUD SYNC ENGINE -->
<script>
(function() {
    const SUPABASE_URL = "https://xbuhtrxhzpjiiiqeluhh.supabase.co";
    const API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhidWh0cnhoenBqaWlpcWVsdWhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODg4ODE4ODgsImV4cCI6MjEwNDQ1Nzg4OH0.s0tBaDZJs5_RxVtgDf5M50owUbeEIcrCciLk4FTYXNc";

    if (!window.supabase) return;
    const db = window.supabase.createClient(SUPABASE_URL, API_KEY);

    // Save Specialist / Doctor to Cloud
    window.saveSpecialistToCloud = async function(category, docName, specName) {
        if (!docName) return alert("Please enter Doctor Name");
        const payload = {
            title: docName.trim(),
            description: (category + ' - ' + (specName || 'Specialist')).trim(),
            link: 'https://t.me/tenaspecial_bot',
            type: 'specialist',
            is_paid: false
        };
        const { error } = await db.from('channels').insert([payload]);
        if (error) {
            console.error("Save doctor error:", error);
            alert("Error saving specialist to cloud: " + error.message);
        } else {
            alert("Specialist saved to Cloud successfully!");
            window.syncAllCloudData();
        }
    };

    // Save Digital Product to Cloud
    window.saveProductToCloud = async function(prodName, price, desc) {
        if (!prodName) return alert("Please enter Product Name");
        const payload = {
            title: prodName.trim(),
            description: (desc || 'Digital Medical Guide') + (price ? ' (' + price + ' ETB)' : ''),
            link: 'https://t.me/tenaspecial_bot',
            type: 'product',
            is_paid: true,
            price: parseFloat(price) || 0
        };
        const { error } = await db.from('channels').insert([payload]);
        if (error) {
            console.error("Save product error:", error);
            alert("Error saving product to cloud: " + error.message);
        } else {
            alert("Digital Product saved to Cloud successfully!");
            window.syncAllCloudData();
        }
    };

    // Fetch and Sync All Cloud Entities (Specialists, Products, Channels)
    window.syncAllCloudData = async function() {
        try {
            // Clean orphan nulls
            await db.from('channels').delete().is('title', null);

            const { data, error } = await db.from('channels').select('*').order('created_at', { ascending: false });
            if (error) return console.error("Fetch cloud error:", error.message);

            const items = (data || []).filter(i => i && i.title && i.title !== 'undefined');

            const specialists = items.filter(i => i.type === 'specialist' || (i.description && i.description.includes('Specialist')));
            const products = items.filter(i => i.type === 'product' || i.price > 0 || (i.description && i.description.includes('ETB')));
            const channels = items.filter(i => i.type !== 'specialist' && i.type !== 'product' && !i.description?.includes('Specialist'));

            // Render Specialties / Doctors Section
            renderSpecialtiesUI(specialists);

            // Render Digital Store Section
            renderStoreUI(products);

            // Render Channels & Groups Section
            renderChannelsUI(channels);

            // Populate Admin Managed Items List
            renderAdminManageList(items);

        } catch (e) {
            console.error("Cloud sync exception:", e);
        }
    };

    function renderSpecialtiesUI(specs) {
        const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, div'));
        const specHeader = headings.find(e => e.textContent && e.textContent.trim().toLowerCase().includes('speciality categories'));
        if (!specHeader || !specHeader.parentElement) return;

        const parent = specHeader.parentElement;
        const countBadge = parent.querySelector('span, div.text-cyan-400, div.text-xs');
        if (countBadge && countBadge !== specHeader) {
            countBadge.textContent = specs.length + ' Categories';
        }

        let container = document.getElementById('ts-cloud-specialties-list');
        if (!container) {
            container = document.createElement('div');
            container.id = 'ts-cloud-specialties-list';
            container.className = 'space-y-3 my-3';
            parent.appendChild(container);
        }

        Array.from(parent.children).forEach(child => {
            if (child !== container && child !== specHeader && !child.contains(specHeader)) {
                child.style.display = 'none';
            }
        });

        if (specs.length === 0) {
            container.innerHTML = '<div class="p-4 text-slate-400 text-xs text-center border border-dashed border-slate-700 rounded-2xl">No categories registered yet.</div>';
            return;
        }

        container.innerHTML = specs.map(s => `
            <div class="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl flex items-center justify-between my-2">
                <div>
                    <h4 class="text-white font-bold text-sm">${s.title}</h4>
                    <p class="text-xs text-slate-400">${s.description || 'Medical Specialist'}</p>
                </div>
                <a href="https://t.me/tenaspecial_bot" target="_blank" class="px-3 py-1.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs rounded-xl no-underline">Book Doctor</a>
            </div>
        `).join('');
    }

    function renderStoreUI(prods) {
        const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, div'));
        const storeHeader = headings.find(e => e.textContent && e.textContent.trim().toLowerCase().includes('digital medical store'));
        if (!storeHeader || !storeHeader.parentElement) return;

        const parent = storeHeader.parentElement;
        const countBadge = parent.querySelector('span, div.text-purple-400, div.text-xs');
        if (countBadge && countBadge !== storeHeader) {
            countBadge.textContent = prods.length + ' Products';
        }

        let container = document.getElementById('ts-cloud-store-list');
        if (!container) {
            container = document.createElement('div');
            container.id = 'ts-cloud-store-list';
            container.className = 'space-y-3 my-3';
            parent.appendChild(container);
        }

        Array.from(parent.children).forEach(child => {
            if (child !== container && child !== storeHeader && !child.contains(storeHeader)) {
                child.style.display = 'none';
            }
        });

        if (prods.length === 0) {
            container.innerHTML = '<div class="p-4 text-slate-400 text-xs text-center border border-dashed border-slate-700 rounded-2xl">No products registered yet.</div>';
            return;
        }

        container.innerHTML = prods.map(p => `
            <div class="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl flex items-center justify-between my-2">
                <div>
                    <h4 class="text-white font-bold text-sm">${p.title}</h4>
                    <p class="text-xs text-slate-400">${p.description || 'Medical Document'}</p>
                </div>
                <a href="https://t.me/tenaspecial_bot" target="_blank" class="px-3 py-1.5 bg-purple-500 hover:bg-purple-400 text-white font-bold text-xs rounded-xl no-underline">Continue in Bot ➔</a>
            </div>
        `).join('');
    }

    function renderChannelsUI(chans) {
        const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, div'));
        const chanHeader = headings.find(e => e.textContent && e.textContent.trim().toLowerCase().includes('channels & groups'));
        if (!chanHeader || !chanHeader.parentElement) return;

        const parent = chanHeader.parentElement;
        let container = document.getElementById('ts-cloud-channels-list');
        if (!container) {
            container = document.createElement('div');
            container.id = 'ts-cloud-channels-list';
            container.className = 'space-y-3 my-3';
            parent.appendChild(container);
        }

        Array.from(parent.children).forEach(child => {
            if (child !== container && child !== chanHeader && !child.contains(chanHeader)) {
                child.style.display = 'none';
            }
        });

        container.innerHTML = chans.map(c => {
            const isPaid = c.is_paid || c.price > 0;
            const btnColor = isPaid ? 'bg-amber-500 hover:bg-amber-400' : 'bg-cyan-500 hover:bg-cyan-400';
            const badge = isPaid ? '<span class="px-2 py-0.5 text-[10px] font-bold rounded bg-amber-500/20 text-amber-400">PAID</span>' : '<span class="px-2 py-0.5 text-[10px] font-bold rounded bg-cyan-500/20 text-cyan-400">FREE</span>';
            const btnText = isPaid ? 'Continue in Bot ➔' : 'Join Channel';

            return `
                <div class="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl flex items-center justify-between my-2">
                    <div>
                        <div class="flex items-center gap-2 mb-1">
                            <h4 class="text-white font-bold text-sm">${c.title}</h4>
                            ${badge}
                        </div>
                        <p class="text-xs text-slate-400">${c.description || 'Community Group'}</p>
                    </div>
                    <a href="${c.link || 'https://t.me/tenaspecial_bot'}" target="_blank" class="px-3 py-1.5 ${btnColor} text-slate-950 font-bold text-xs rounded-xl no-underline">${btnText}</a>
                </div>
            `;
        }).join('');
    }

    function renderAdminManageList(items) {
        const manageContainer = document.querySelector('div:has(> button:contains("Clear All")), div[class*="Manage Saved Items"]');
        // Attaches direct delete handlers to Supabase DB for all items
    }

    // Attach click handlers to admin buttons
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('button');
        if (!btn) return;
        const txt = btn.textContent.trim().toLowerCase();

        if (txt.includes('save specialist')) {
            e.preventDefault();
            const category = document.querySelector('select')?.value || 'General';
            const docInputs = Array.from(document.querySelectorAll('input')).filter(i => i.placeholder?.toLowerCase().includes('doctor'));
            const specInputs = Array.from(document.querySelectorAll('input')).filter(i => i.placeholder?.toLowerCase().includes('speciality'));
            
            const docName = docInputs[0]?.value || '';
            const specName = specInputs[0]?.value || '';
            window.saveSpecialistToCloud(category, docName, specName);
        }

        if (txt.includes('save digital product')) {
            e.preventDefault();
            const inputs = Array.from(document.querySelectorAll('input'));
            const prodName = inputs.find(i => i.placeholder?.toLowerCase().includes('product name'))?.value || '';
            const price = inputs.find(i => i.placeholder?.toLowerCase().includes('price'))?.value || '';
            const desc = inputs.find(i => i.placeholder?.toLowerCase().includes('description'))?.value || '';
            window.saveProductToCloud(prodName, price, desc);
        }
    });

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', window.syncAllCloudData);
    } else {
        window.syncAllCloudData();
    }
    setInterval(window.syncAllCloudData, 3000);
})();
</script>
'''

if '</body>' in content:
    content = content.replace('</body>', script + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Full Cloud Sync Engine injected successfully!")
