import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 1. Clean out all previous sync script attempts
content = re.sub(r'<!-- SUPABASE CLOUD ENGINE -->[\s\S]*?</script>', '', content)
content = re.sub(r'<!-- SUPABASE CLOUD SYNC -->[\s\S]*?</script>', '', content)
content = re.sub(r'<!-- SUPABASE ROOT ENGINE -->[\s\S]*?</script>', '', content)
content = re.sub(r'<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>', '', content)

# 2. Ensure SDK in head
if '</head>' in content:
    content = content.replace('</head>', '  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n</head>')

# 3. Direct Root Engine Script
root_script = '''
<!-- SUPABASE ROOT ENGINE -->
<script>
(function() {
    const SUPABASE_URL = "https://xbuhtrxhzpjiiiqeluhh.supabase.co";
    const SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzIsInJlZiI6InhidWh0cnhoenBqaWlpcWVsdWhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODg4ODE4ODgsImV4cCI6MjEwNDQ1Nzg4OH0.s0tBaDZJs5_RxVtgDf5M50owUbeEIcrCciLk4FTYXNc";

    if (!window.supabase) return;
    const db = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

    window.loadCloudChannels = async function() {
        try {
            const { data, error } = await db.from('channels').select('*').order('created_at', { ascending: false });
            if (error) return console.error("Supabase load error:", error.message);

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
        const { error } = await db.from('channels').insert([{ title: title, link: link, item_type: 'channel' }]);
        if (error) {
            alert("❌ Cloud Save Failed: " + error.message);
        } else {
            alert("✅ Saved to Cloud Database! Syncing live across all browsers...");
            await window.loadCloudChannels();
        }
    }

    // Intercept all save clicks directly at the root
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
    setInterval(window.loadCloudChannels, 10000); // Live sync polling every 10 seconds
})();
</script>
'''

if '</body>' in content:
    content = content.replace('</body>', root_script + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Root fix applied successfully!")
