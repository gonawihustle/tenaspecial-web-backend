import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 1. Clean out all previous channel scripts
content = re.sub(r'<!-- SUPABASE CLOUD ENGINE FOR CHANNELS -->[\s\S]*?</script>', '', content)

script = '''
<!-- SUPABASE CLOUD ENGINE FOR CHANNELS -->
<script>
(function() {
    const SUPABASE_URL = "https://xbuhtrxhzpjiiiqeluhh.supabase.co";
    const API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhidWh0cnhoenBqaWlpcWVsdWhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODg4ODE4ODgsImV4cCI6MjEwNDQ1Nzg4OH0.s0tBaDZJs5_RxVtgDf5M50owUbeEIcrCciLk4FTYXNc";

    if (!window.supabase) return;
    const db = window.supabase.createClient(SUPABASE_URL, API_KEY);

    // Global Sync Function
    window.syncCloudChannels = async function() {
        try {
            const { data, error } = await db.from('channels').select('*').order('created_at', { ascending: false });
            if (error) {
                console.error("Cloud fetch error:", error.message);
                return;
            }

            const items = data || [];

            // --- A. CLEAN LEGACY UNDEFINED ELEMENTS ---
            document.querySelectorAll('div, li, p, span').forEach(el => {
                if (el.children.length === 0 && el.innerText && el.innerText.includes('undefined')) {
                    const parent = el.closest('div.flex') || el.parentElement;
                    if (parent) parent.style.display = 'none';
                }
            });

            // --- B. UPDATE PUBLIC CHANNELS SECTION ---
            const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, div'));
            const publicHeader = headings.find(e => e.textContent && e.textContent.trim().toLowerCase().includes('channels & groups'));

            if (publicHeader && publicHeader.parentElement) {
                // Update Count Text
                const countBadge = publicHeader.parentElement.querySelector('span, div.text-cyan-400, div.text-xs');
                if (countBadge && countBadge !== publicHeader) {
                    countBadge.textContent = items.length + ' Items';
                }

                let publicContainer = document.getElementById('public-cloud-channels-list');
                if (!publicContainer) {
                    publicContainer = document.createElement('div');
                    publicContainer.id = 'public-cloud-channels-list';
                    publicContainer.className = 'space-y-3 my-3';
                    publicHeader.parentElement.appendChild(publicContainer);
                }

                // Hide default static cards
                Array.from(publicHeader.parentElement.children).forEach(child => {
                    if (child !== publicContainer && child !== publicHeader && !child.contains(publicHeader)) {
                        if (child.innerText && (child.innerText.includes('No channels') || child.innerText.includes('Join Channel') || child.innerText.includes('Continue in Bot') || child.innerText.includes('FREE') || child.innerText.includes('PAID'))) {
                            child.style.display = 'none';
                        }
                    }
                });

                if (items.length === 0) {
                    publicContainer.innerHTML = '<div class="p-4 text-slate-400 text-xs text-center border border-dashed border-slate-700 rounded-2xl">No channels added yet.</div>';
                } else {
                    publicContainer.innerHTML = items.map(c => {
                        const title = c.title || c.name || 'Untitled Item';
                        const sub = c.description || c.subtitle || c.nameAm || 'Tenaspecial Community';
                        const rawLink = c.link || c.url || '';
                        
                        const titleLower = title.toLowerCase();
                        const subLower = sub.toLowerCase();
                        const isPaid = c.is_paid === true || c.price > 0 || titleLower.includes('paid') || titleLower.includes('premium') || subLower.includes('paid') || subLower.includes('premium');
                        
                        if (isPaid) {
                            const botUrl = rawLink.includes('t.me/') ? rawLink : 'https://t.me/tenaspecial_bot';
                            return '<div class="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl flex items-center justify-between my-3">' +
                                '<div>' +
                                    '<div class="flex items-center gap-2 mb-1">' +
                                        '<h4 class="text-white font-bold text-sm sm:text-base">' + title + '</h4>' +
                                        '<span class="px-2 py-0.5 text-[10px] font-bold rounded-md bg-amber-500/20 text-amber-400 border border-amber-500/30">PAID</span>' +
                                    '</div>' +
                                    '<p class="text-xs text-slate-400">' + sub + '</p>' +
                                '</div>' +
                                '<a href="' + botUrl + '" target="_blank" class="px-4 py-2 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs rounded-xl no-underline flex items-center gap-1.5 transition-all shadow-md shrink-0">' +
                                    '<span>Continue in Bot</span>' +
                                    '<svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.2-.08-.06-.19-.04-.27-.02-.12.02-1.96 1.25-5.54 3.69-.52.36-1 .53-1.42.52-.47-.01-1.37-.26-2.03-.48-.82-.27-1.47-.42-1.42-.88.03-.25.38-.51 1.07-.78 4.18-1.82 6.97-3.02 8.37-3.6 3.98-1.65 4.81-1.94 5.35-1.95.12 0 .38.03.55.17.14.12.18.28.2.4.02.12.01.24 0 .33z"/></svg>' +
                                '</a>' +
                            '</div>';
                        } else {
                            const channelUrl = rawLink.startsWith('http') ? rawLink : 'https://' + rawLink;
                            return '<div class="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl flex items-center justify-between my-3">' +
                                '<div>' +
                                    '<div class="flex items-center gap-2 mb-1">' +
                                        '<h4 class="text-white font-bold text-sm sm:text-base">' + title + '</h4>' +
                                        '<span class="px-2 py-0.5 text-[10px] font-bold rounded-md bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">FREE</span>' +
                                    '</div>' +
                                    '<p class="text-xs text-slate-400">' + sub + '</p>' +
                                '</div>' +
                                '<a href="' + channelUrl + '" target="_blank" class="px-4 py-2 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs rounded-xl no-underline transition-all shadow-md shrink-0">Join Channel</a>' +
                            '</div>';
                        }
                    }).join('');
                }
            }

            # --- C. UPDATE SUPERADMIN "MANAGE SAVED ITEMS" SECTION ---
            const adminHeader = headings.find(e => e.textContent && e.textContent.includes('Manage Saved Items'));
            if (adminHeader && adminHeader.parentElement) {
                let adminContainer = document.getElementById('admin-cloud-channels-list');
                if (!adminContainer) {
                    adminContainer = document.createElement('div');
                    adminContainer.id = 'admin-cloud-channels-list';
                    adminContainer.className = 'space-y-3 mt-4';
                    adminHeader.parentElement.appendChild(adminContainer);
                }

                // Hide old static item cards inside Admin section
                Array.from(adminHeader.parentElement.children).forEach(child => {
                    if (child !== adminContainer && child !== adminHeader && !child.contains(adminHeader)) {
                        if (child.innerText && (child.innerText.includes('Delete') || child.innerText.includes('Edit') || child.innerText.includes('No saved items'))) {
                            child.style.display = 'none';
                        }
                    }
                });

                if (items.length === 0) {
                    adminContainer.innerHTML = '<div class="p-4 text-slate-400 text-xs text-center border border-dashed border-slate-700 rounded-2xl">No items stored in cloud database.</div>';
                } else {
                    adminContainer.innerHTML = items.map(item => {
                        const title = item.title || item.name || 'Untitled Item';
                        const link = item.link || item.url || '';
                        const typeLabel = (title.toLowerCase().includes('group') || (item.description && item.description.toLowerCase().includes('group'))) ? 'GROUP' : 'CHANNEL';
                        const itemId = item.id || '';

                        return '<div class="p-3 bg-slate-900/90 rounded-2xl border border-slate-800 flex items-center justify-between my-2">' +
                            '<div>' +
                                '<span class="text-[10px] font-bold text-cyan-400 uppercase tracking-wider block mb-0.5">' + typeLabel + '</span>' +
                                '<h5 class="text-white font-bold text-xs sm:text-sm">' + title + '</h5>' +
                                '<p class="text-[11px] text-slate-400 truncate max-w-[180px] sm:max-w-xs">' + link + '</p>' +
                            '</div>' +
                            '<div class="flex items-center gap-2">' +
                                '<button onclick="deleteCloudItem(\'' + itemId + '\', \'' + title.replace(/'/g, "\\'") + '\')" class="px-3 py-1.5 bg-rose-500/20 text-rose-400 hover:bg-rose-500 hover:text-white border border-rose-500/30 font-bold text-xs rounded-xl transition-all">Delete</button>' +
                            '</div>' +
                        '</div>';
                    }).join('');
                }
            }

        } catch (err) {
            console.error("Cloud Sync Exception:", err);
        }
    };

    // Delete Handler
    window.deleteCloudItem = async function(id, title) {
        if (!confirm('Are you sure you want to delete "' + title + '"?')) return;
        
        let res;
        if (id && id !== 'undefined' && id !== 'null') {
            res = await db.from('channels').delete().eq('id', id);
        } else {
            res = await db.from('channels').delete().eq('title', title);
        }

        if (res.error) {
            alert("❌ Delete failed: " + res.error.message);
        } else {
            alert("✅ Deleted successfully!");
            await window.syncCloudChannels();
        }
    };

    // Global Save Interceptor
    document.addEventListener('click', async function(e) {
        const btn = e.target.closest('button, input[type="submit"], a');
        if (!btn) return;

        const text = (btn.innerText || btn.value || '').toLowerCase();
        if (text.includes('save channel') || text.includes('add channel')) {
            const formBox = btn.closest('form') || btn.closest('div.bg-slate-900') || btn.closest('div.p-4') || btn.parentElement.parentElement;
            if (formBox) {
                const inputs = Array.from(formBox.querySelectorAll('input, select'));
                let titleVal = '', linkVal = '', descVal = '', isPaid = false;

                inputs.forEach(inp => {
                    const val = inp.value.trim();
                    if (!val) return;
                    const placeholder = (inp.placeholder || inp.name || '').toLowerCase();
                    
                    if (val.startsWith('http') || val.includes('t.me') || val.includes('.')) {
                        linkVal = val;
                    } else if (placeholder.includes('sub') || placeholder.includes('amharic') || placeholder.includes('desc')) {
                        descVal = val;
                    } else if (inp.type === 'checkbox' || inp.type === 'radio') {
                        if (inp.checked && (val.toLowerCase().includes('paid') || val === 'true')) isPaid = true;
                    } else if (inp.tagName === 'SELECT' && (val.toLowerCase().includes('paid') || val.toLowerCase().includes('premium'))) {
                        isPaid = true;
                    } else if (!titleVal) {
                        titleVal = val;
                    } else if (!descVal) {
                        descVal = val;
                    }
                });

                if (titleVal && linkVal) {
                    e.preventDefault();
                    e.stopPropagation();

                    if (titleVal.toLowerCase().includes('paid') || titleVal.toLowerCase().includes('premium')) {
                        isPaid = true;
                    }

                    const payload = {
                        title: titleVal,
                        link: linkVal,
                        description: descVal || 'Tenaspecial Community',
                        is_paid: isPaid,
                        item_type: titleVal.toLowerCase().includes('group') ? 'group' : 'channel'
                    };

                    let { error } = await db.from('channels').insert([payload]);

                    if (error && error.message && error.message.includes('column')) {
                        delete payload.is_paid;
                        delete payload.description;
                        const retry = await db.from('channels').insert([payload]);
                        error = retry.error;
                    }

                    if (error) {
                        alert("❌ Save Failed: " + error.message);
                    } else {
                        alert("✅ Saved to Cloud Database!");
                        inputs.forEach(inp => { if (inp.type !== 'submit' && inp.type !== 'button') inp.value = ''; });
                        await window.syncCloudChannels();
                    }
                }
            }
        }
    }, true);

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', window.syncCloudChannels);
    } else {
        window.syncCloudChannels();
    }
    setInterval(window.syncCloudChannels, 5000);
})();
</script>
'''

if '</body>' in content:
    content = content.replace('</body>', script + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Cloud sync and superadmin panel fix applied!")
