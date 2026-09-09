with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Ensure Supabase SDK is present
if 'supabase-js' not in content:
    content = content.replace('</head>', '  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n</head>')

# Remove any old broken sync scripts
import re
content = re.sub(r'<!-- SUPABASE CLOUD SYNC -->[\s\S]*?</script>', '', content)

cloud_script = '''
<!-- SUPABASE CLOUD SYNC -->
<script>
(function() {
    const SUPABASE_URL = "https://xbuhtrxhzpjiiiqeluhh.supabase.co";
    const SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhidWh0cnhoenBqaWlpcWVsdWhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODg4ODE4ODgsImV4cCI6MjEwNDQ1Nzg4OH0.s0tBaDZJs5_RxVtgDf5M50owUbeEIcrCciLk4FTYXNc";

    if (!window.supabase) return;
    const db = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

    async function syncFromCloud() {
        try {
            const { data, error } = await db.from('channels').select('*').order('created_at', { ascending: false });
            if (!error && data) {
                localStorage.setItem('ts_channels', JSON.stringify(data));
                if (typeof window.loadAllData === 'function') window.loadAllData();
                else location.reload();
            }
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    document.addEventListener('submit', async function(e) {
        e.preventDefault(); // Stop page from refreshing before cloud write finishes
        
        const form = e.target;
        const titleInput = form.querySelector('input[placeholder*="Title"], input[placeholder*="Name"], input[name*="title"]');
        const linkInput = form.querySelector('input[placeholder*="http"], input[placeholder*="Link"], input[name*="link"]');
        
        if (titleInput && linkInput && titleInput.value && linkInput.value) {
            const title = titleInput.value.trim();
            const link = linkInput.value.trim();
            
            const { error } = await db.from('channels').insert([{ title: title, link: link, item_type: 'channel' }]);
            if (error) {
                alert("Cloud save failed: " + error.message);
            } else {
                alert("Saved to cloud! Syncing across all browsers...");
                form.reset();
                await syncFromCloud();
            }
        }
    });

    // Auto-sync from cloud on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', syncFromCloud);
    } else {
        syncFromCloud();
    }
})();
</script>
'''

if '</body>' in content:
    content = content.replace('</body>', cloud_script + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed cloud sync successfully!")
