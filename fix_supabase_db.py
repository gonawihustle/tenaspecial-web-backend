import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Remove all previous sync attempts
content = re.sub(r'<!-- SUPABASE CLOUD SYNC -->[\s\S]*?</script>', '', content)
content = re.sub(r'<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>', '', content)

# Inject SDK in head
if '</head>' in content:
    content = content.replace('</head>', '  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n</head>')

supabase_code = '''
<!-- SUPABASE CLOUD ENGINE -->
<script>
(function() {
    const SUPABASE_URL = "https://xbuhtrxhzpjiiiqeluhh.supabase.co";
    const SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzIsInJlZiI6InhidWh0cnhoenBqaWlpcWVsdWhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODg4ODE4ODgsImV4cCI6MjEwNDQ1Nzg4OH0.s0tBaDZJs5_RxVtgDf5M50owUbeEIcrCciLk4FTYXNc";

    if (!window.supabase) return;
    const db = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

    window.supabaseDb = db;

    async function loadCloudChannels() {
        const { data, error } = await db.from('channels').select('*').order('created_at', { ascending: false });
        if (error) {
            console.error("Supabase load error:", error.message);
            return;
        }

        // Render to public list
        const storeHeader = Array.from(document.querySelectorAll('div, h2, h3')).find(e => e.textContent && e.textContent.trim().toLowerCase() === 'channels & groups' && e.children.length < 3);
        if (storeHeader && storeHeader.parentElement) {
            let container = document.getElementById('public-cloud-channels');
            if (!container) {
                container = document.createElement('div');
                container.id = 'public-cloud-channels';
                container.className = 'space-y-3 my-3';
                storeHeader.parentElement.appendChild(container);
            }

            // Hide old local list container if present
            const oldList = storeHeader.parentElement.querySelector('.space-y-3:not(#public-cloud-channels)');
            if (oldList) oldList.style.display = 'none';

            if (!data || data.length === 0) {
                container.innerHTML = '<div class="p-4 text-slate-400 text-xs text-center border border-dashed border-slate-700 rounded-2xl">No channels added yet.</div>';
            } else {
                container.innerHTML = data.map(c => {
                    const redirectUrl = c.link.startsWith('http') ? c.link : 'https://' + c.link;
                    return '<div class="p-4 rounded-2xl bg-slate-800/80 border border-slate-700/60 shadow-lg my-3">' +
                        '<div class="flex items-center justify-between mb-1">' +
                        '<h4 class="text-white font-bold text-sm">' + (c.title || '') + '</h4>' +
                        '<span class="px-2.5 py-0.5 border text-[10px] font-bold rounded-md bg-cyan-500/20 text-cyan-400 border-cyan-500/30">FREE</span></div>' +
                        '<div class="flex items-center justify-between pt-2 border-t border-slate-700/40 mt-2">' +
                        '<a href="' + redirectUrl + '" target="_blank" class="text-xs font-medium text-cyan-400 hover:text-cyan-300 no-underline">🔗 Join Free →</a>' +
                        '</div></div>';
                }).join('');
            }
        }
    }

    document.addEventListener('submit', async function(e) {
        const form = e.target;
        const titleInput = form.querySelector('input[placeholder*="Title"], input[placeholder*="Name"], input[name*="title"]');
        const linkInput = form.querySelector('input[placeholder*="http"], input[placeholder*="Link"], input[name*="link"]');
        
        if (titleInput && linkInput && titleInput.value && linkInput.value) {
            e.preventDefault();
            const title = titleInput.value.trim();
            const link = linkInput.value.trim();

            const { error } = await db.from('channels').insert([{ title: title, link: link, item_type: 'channel' }]);
            if (error) {
                alert("Database Error: " + error.message);
            } else {
                alert("Successfully saved to Cloud!");
                form.reset();
                await loadCloudChannels();
            }
        }
    });

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadCloudChannels);
    } else {
        loadCloudChannels();
    }
})();
</script>
'''

if '</body>' in content:
    content = content.replace('</body>', supabase_code + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Supabase Engine installed successfully!")
