import glob, os, re

html_files = glob.glob('**/index.html', recursive=True) + glob.glob('*.html')
target_files = set([f for f in html_files if not any(x in f for x in ['node_modules', '.git', 'venv'])])

clean_script = '''
<!-- STRICT SEPARATION & CLEAN LAYOUT -->
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script>
(function() {
    const SUPABASE_URL = "https://xbuhtrxhzpjiiiqeluhh.supabase.co";
    const SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhidWh0cnhoenBqaWlpcWVsdWhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODg4ODE4ODgsImV4cCI6MjEwNDQ1Nzg4OH0.s0tBaDZJs5_RxVtgDf5M50owUbeEIcrCciLk4FTYXNc";

    if (!window.supabase) return;
    const db = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
    window.supabaseDb = db;

    window.deleteChannel = async function(id) {
        if (!confirm('Are you sure you want to delete this item?')) return;
        const { error } = await db.from('channels').delete().eq('id', id);
        if (error) alert('Error: ' + error.message);
        else { alert('Item deleted.'); loadAllData(); }
    };

    window.purgeAllChannels = async function() {
        if (!confirm('⚠️ Delete ALL saved channels and groups from the database?')) return;
        const { error } = await db.from('channels').delete().neq('id', 0);
        if (error) alert('Error purging: ' + error.message);
        else { alert('Database cleared successfully.'); loadAllData(); }
    };

    window.editChannel = async function(id) {
        const { data, error } = await db.from('channels').select('*').eq('id', id).single();
        if (error || !data) return alert('Item not found.');

        const title = prompt('Edit Title:', data.title);
        if (title === null) return;
        const link = prompt('Edit Link:', data.link);
        if (link === null) return;
        const type = prompt('Type (channel or group):', data.item_type || 'channel');
        if (type === null) return;

        const { error: err } = await db.from('channels').update({
            title: title, link: link, item_type: type.toLowerCase().includes('group') ? 'group' : 'channel'
        }).eq('id', id);

        if (err) alert('Update error: ' + err.message);
        else { alert('Updated successfully.'); loadAllData(); }
    };

    async function loadAllData() {
        const { data: channels } = await db.from('channels').select('*').order('created_at', { ascending: false });

        let saveBtn = Array.from(document.querySelectorAll('button')).find(b => b.textContent && b.textContent.includes('Save Channel'));
        if (saveBtn) {
            let adminContainer = document.getElementById('admin-channel-management');
            if (!adminContainer) {
                adminContainer = document.createElement('div');
                adminContainer.id = 'admin-channel-management';
                adminContainer.className = 'mt-6 p-4 bg-slate-900 border border-slate-700 rounded-2xl text-left shadow-2xl';
                if (saveBtn.parentElement) saveBtn.parentElement.after(adminContainer);
            }

            let adminHtml = '<div class="flex items-center justify-between mb-3 pb-2 border-b border-slate-700/80">' +
                '<div><h3 class="text-white font-bold text-sm">⚙️ Manage Saved Items (Admin Only)</h3>' +
                '<p class="text-[11px] text-slate-400">Edit or delete items stored in cloud</p></div>' +
                '<button onclick="window.purgeAllChannels()" class="px-2.5 py-1 bg-red-600/30 text-red-300 border border-red-500/40 rounded-lg text-xs font-bold hover:bg-red-600/50">🔥 Clear All</button>' +
                '</div>';

            if (!channels || channels.length === 0) {
                adminHtml += '<div class="text-slate-400 text-xs text-center py-3 border border-dashed border-slate-800 rounded-xl">No saved items in database.</div>';
            } else {
                adminHtml += '<div class="space-y-2 max-h-64 overflow-y-auto pr-1">';
                channels.forEach(c => {
                    const typeText = (c.item_type || 'channel').toUpperCase();
                    adminHtml += '<div class="p-2.5 bg-slate-800/90 rounded-xl border border-slate-700 flex items-center justify-between gap-2">' +
                        '<div class="min-w-0 flex-1"><div class="flex items-center gap-1 mb-0.5">' +
                        '<span class="text-[9px] px-1.5 py-0.5 rounded bg-slate-700 text-cyan-300 font-bold">' + typeText + '</span></div>' +
                        '<div class="text-white font-bold text-xs truncate">' + (c.title || 'Untitled') + '</div>' +
                        '<div class="text-slate-400 text-[10px] truncate">' + (c.link || '') + '</div></div>' +
                        '<div class="flex items-center gap-1 shrink-0">' +
                        '<button onclick="window.editChannel(' + c.id + ')" class="px-2 py-1 bg-amber-500/20 text-amber-300 border border-amber-500/30 rounded text-xs font-bold">Edit</button>' +
                        '<button onclick="window.deleteChannel(' + c.id + ')" class="px-2 py-1 bg-red-500/20 text-red-400 border border-red-500/30 rounded text-xs font-bold">Delete</button>' +
                        '</div></div>';
                });
                adminHtml += '</div>';
            }
            adminContainer.innerHTML = adminHtml;
        }

        const allHeadings = Array.from(document.querySelectorAll('h1, h2, h3, h4, div'));
        const storeHeader = allHeadings.find(e => e.textContent && e.textContent.trim().toLowerCase().includes('channels & groups') && e.children.length < 3);

        if (storeHeader && storeHeader.parentElement) {
            let publicContainer = storeHeader.parentElement.querySelector('#public-store-channel-list');
            if (!publicContainer) {
                publicContainer = document.createElement('div');
                publicContainer.id = 'public-store-channel-list';
                publicContainer.className = 'space-y-3 my-3';
                storeHeader.parentElement.appendChild(publicContainer);
            }

            const staticElements = storeHeader.parentElement.querySelectorAll('div');
            staticElements.forEach(el => {
                if (el.id !== 'public-store-channel-list' && !publicContainer.contains(el) && el.textContent.includes('Free channel for medical informations')) {
                    el.style.display = 'none';
                }
            });

            if (!channels || channels.length === 0) {
                publicContainer.innerHTML = '<div class="p-4 text-slate-400 text-xs text-center border border-dashed border-slate-700 rounded-2xl">No channels added yet.</div>';
            } else {
                publicContainer.innerHTML = channels.map(c => {
                    const itemType = (c.item_type || 'channel').toLowerCase() === 'group' ? 'Group' : 'Channel';
                    const redirectUrl = c.link.startsWith('http') ? c.link : 'https://' + c.link;
                    return '<div class="p-4 rounded-2xl bg-slate-800/80 border border-slate-700/60 shadow-lg my-3">' +
                        '<div class="flex items-center justify-between mb-1">' +
                        '<div class="flex items-center gap-2"><span class="text-xs px-2 py-0.5 rounded bg-slate-700 text-slate-300 font-semibold">' + itemType + '</span>' +
                        '<h4 class="text-white font-bold text-sm">' + (c.title || '') + '</h4></div>' +
                        '<span class="px-2.5 py-0.5 border text-[10px] font-bold rounded-md bg-cyan-500/20 text-cyan-400 border-cyan-500/30">FREE</span></div>' +
                        '<div class="flex items-center justify-between pt-2 border-t border-slate-700/40 mt-2">' +
                        '<a href="' + redirectUrl + '" target="_blank" class="text-xs font-medium text-cyan-400 hover:text-cyan-300 no-underline">🔗 Join Free ' + itemType + ' →</a>' +
                        '</div></div>';
                }).join('');
            }
        }
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', loadAllData);
    else loadAllData();
})();
</script>
'''

for fpath in target_files:
    try:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        content = re.sub(r'<!-- Bulletproof Superadmin[\s\S]*?</script>', '', content)
        content = re.sub(r'<!-- Admin Edit[\s\S]*?</script>', '', content)
        content = re.sub(r'<!-- STRICT SUPERADMIN[\s\S]*?</script>', '', content)
        content = re.sub(r'<!-- STRICT SEPARATION[\s\S]*?</script>', '', content)

        if '</body>' in content:
            content = content.replace('</body>', clean_script + '\n</body>')
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Cleaned & Updated: {fpath}')
    except Exception as e:
        pass
