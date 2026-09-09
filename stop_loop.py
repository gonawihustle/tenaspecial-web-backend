import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 1. Strip out all broken sync scripts causing the loop
content = re.sub(r'<!-- SUPABASE CLOUD SYNC -->[\s\S]*?</script>', '', content)

# 2. Add safe sync script with zero location.reload calls
safe_script = '''
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
                if (typeof window.loadAllData === 'function') {
                    window.loadAllData();
                }
            }
        } catch (err) {
            console.error("Fetch error:", err);
        }
    }

    document.addEventListener('submit', async function(e) {
        e.preventDefault();
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
                alert("Saved to cloud!");
                form.reset();
                await syncFromCloud();
            }
        }
    });

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', syncFromCloud);
    } else {
        syncFromCloud();
    }
})();
</script>
'''

if '</body>' in content:
    content = content.replace('</body>', safe_script + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Loop fix applied successfully!")
