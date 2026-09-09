import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Clean up existing scripts
content = re.sub(r'<!-- SUPABASE ROOT ENGINE -->[\s\S]*?</script>', '', content)
content = re.sub(r'<!-- SUPABASE CLOUD ENGINE -->[\s\S]*?</script>', '', content)
content = re.sub(r'<!-- SUPABASE CLOUD SYNC -->[\s\S]*?</script>', '', content)

script = '''
<!-- SUPABASE ROOT ENGINE -->
<script>
(function() {
    const SUPABASE_URL = "https://xbuhtrxhzpjiiiqeluhh.supabase.co";
    const SUPABASE_KEY = "sb_publishable_sCHzLpXNcpoTnKjKkv5kZg_-WZ5yB04";
    const SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzIsInJlZiI6InhidWh0cnhoenBqaWlpcWVsdWhoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4ODg4MTg4OCwiZXhwIjoyMTA0NDU3ODg4fQ.M2SWpbd0fiuSHkqXXjDRIfcupXQksWI3v0cHgo82F9o";

    if (!window.supabase) return;
    let db = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

    window.loadCloudChannels = async function() {
        try {
            let res = await db.from('channels').select('*').order('created_at', { ascending: false });
            if (res.error && (res.error.message.includes('API key') || res.error.message.includes('JWT'))) {
                db = window.supabase.createClient(SUPABASE_URL, SERVICE_KEY);
                res = await db.from('channels').select('*').order('created_at', { ascending: false });
            }
            const data = res.data;

            if (data) localStorage.setItem('ts_channels', JSON.stringify(data));

            const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, div'));
            const channelHeader = headings.find(e => e.textContent && e.textContent.trim().toLowerCase().includes('channels & groups'));

            if (channelHeader && channelHeader.parentElement) {
                let container = document.getElementById('public-cloud-channels-list');
                if (!container) {
                    container = document.createElement('div');
                    container.id = 'public-cloud-channels-list';
                    container.className = 'space-y-3 my-3';
                    channelHeader.parentElement.appendChild(container);
                }

                Array.from(channelHeader.parentElement.children).forEach(child => {
                    if (child !== container && child !== channelHeader && !child.contains(channelHeader) && child.tagName !== 'H1' && child.tagName !== 'H2' && child.tagName !== 'H3') {
                        if (child.innerText && (child.innerText.includes('No channels') || child.innerText.includes('Join Free'))) {
                            child.style.display = 'none';
                        }
                    }
                });

                if (!data || data.length === 0) {
                    container.innerHTML = '<div class="p-4 text-slate-400 text-xs text-center border border-dashed border-slate-700 rounded-2xl">No channels added yet.</div>';
                } else {
                    container.innerHTML = data.map(c => {
                        const redirectUrl = c.link && c.link.startsWith('http') ? c.link : 'https://' + (c.link || '');
                        return '<div class="p-4 rounded-2xl bg-slate-800/80 border border-slate-700/60 shadow-lg my-3">' +
                            '<div class="flex items-center justify-between mb-1">' +
                            '<h4 class="text-white font-bold text-sm">' + (c.title || 'Untitled Channel') + '</h4>' +
                            '<span class="px-2.5 py-0.5 border text-[10px] font-bold rounded-md bg-cyan-500/20 text-cyan-400 border-cyan-500/30">FREE</span></div>' +
                            '<div class="flex items-center justify-between pt-2 border-t border-slate-700/40 mt-2">' +
                            '<a href="' + redirectUrl + '" target="_blank" class="text-xs font-medium text-cyan-400 hover:text-cyan-300 no-underline">🔗 Join Free →</a>' +
                            '</div></div>';
                    }).join('');
                }
            }
        } catch (err) {
            console.error("Cloud load error:", err);
        }
    };

    async function saveToSupabase(title, link) {
        if (!title || !link) return;
        let res = await db.from('channels').insert([{ title: title, link: link, item_type: 'channel' }]);
        if (res.error) {
            db = window.supabase.createClient(SUPABASE_URL, SERVICE_KEY);
            res = await db.from('channels').insert([{ title: title, link: link, item_type: 'channel' }]);
        }

        if (res.error) {
            alert("❌ Cloud Save Failed: " + res.error.message);
        } else {
            alert("✅ Saved to Cloud Database! Syncing live across all browsers...");
            await window.loadCloudChannels();
        }
    }

    document.addEventListener('click', async function(e) {
        const btn = e.target.closest('button, input[type="submit"], a');
        if (!btn) return;

        const text = (btn.innerText || btn.value || '').toLowerCase();
        if (text.includes('save') || text.includes('add')) {
            const parent = btn.closest('form') || btn.closest('div.bg-slate-900') || btn.closest('div.p-4') || btn.parentElement.parentElement;
            if (parent) {
                const inputs = Array.from(parent.querySelectorAll('input[type="text"], input:not([type])'));
                let titleVal = '', linkVal = '';

                inputs.forEach(inp => {
                    const val = inp.value.trim();
                    if (!val) return;
                    if (val.startsWith('http') || val.includes('t.me') || val.includes('.')) linkVal = val;
                    else titleVal = val;
                });

                if (titleVal && linkVal) {
                    e.preventDefault();
                    e.stopPropagation();
                    await saveToSupabase(titleVal, linkVal);
                    inputs.forEach(inp => inp.value = '');
                }
            }
        }
    }, true);

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', window.loadCloudChannels);
    } else {
        window.loadCloudChannels();
    }
    setInterval(window.loadCloudChannels, 10000);
})();
</script>
'''

if '</body>' in content:
    content = content.replace('</body>', script + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("API Key fix applied successfully!")
