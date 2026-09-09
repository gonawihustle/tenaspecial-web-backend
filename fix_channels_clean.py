import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 1. Clean out all previous channel injection scripts
content = re.sub(r'<!-- SUPABASE CLOUD ENGINE FOR CHANNELS -->[\s\S]*?</script>', '', content)

# 2. Complete unified channel rendering engine
script = '''
<!-- SUPABASE CLOUD ENGINE FOR CHANNELS -->
<script>
(function() {
    const SUPABASE_URL = "https://xbuhtrxhzpjiiiqeluhh.supabase.co";
    const API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhidWh0cnhoenBqaWlpcWVsdWhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODg4ODE4ODgsImV4cCI6MjEwNDQ1Nzg4OH0.s0tBaDZJs5_RxVtgDf5M50owUbeEIcrCciLk4FTYXNc";

    if (!window.supabase) return;
    const db = window.supabase.createClient(SUPABASE_URL, API_KEY);

    window.renderCleanChannels = async function() {
        try {
            // Delete corrupt/empty rows from cloud DB automatically
            await db.from('channels').delete().is('title', null);

            const { data, error } = await db.from('channels').select('*').order('created_at', { ascending: false });
            if (error) return console.error("Cloud fetch error:", error.message);

            // Filter out invalid items to eliminate "undefined" cards
            const items = (data || []).filter(i => i && (i.title || i.name) && (i.title !== 'undefined') && (i.name !== 'undefined'));

            const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, div'));
            const headerElem = headings.find(e => e.textContent && e.textContent.trim().toLowerCase().includes('channels & groups'));

            if (!headerElem || !headerElem.parentElement) return;

            const parent = headerElem.parentElement;

            // Update item count badge
            const countBadge = parent.querySelector('span, div.text-cyan-400, div.text-xs');
            if (countBadge && countBadge !== headerElem) {
                countBadge.textContent = items.length + ' Items';
            }

            // Target or create dedicated container
            let listContainer = document.getElementById('ts-clean-channels-list');
            if (!listContainer) {
                listContainer = document.createElement('div');
                listContainer.id = 'ts-clean-channels-list';
                listContainer.className = 'space-y-3 my-3';
                parent.appendChild(listContainer);
            }

            // Hide all hardcoded static cards & legacy duplicates
            Array.from(parent.children).forEach(child => {
                if (child !== listContainer && child !== headerElem && !child.contains(headerElem)) {
                    child.style.display = 'none';
                }
            });

            if (items.length === 0) {
                listContainer.innerHTML = '<div class="p-4 text-slate-400 text-xs text-center border border-dashed border-slate-700 rounded-2xl">No channels registered yet.</div>';
                return;
            }

            listContainer.innerHTML = items.map(c => {
                const title = (c.title || c.name || 'Channel').trim();
                const sub = (c.description || c.subtitle || c.nameAm || 'Tenaspecial Community').trim();
                const rawLink = (c.link || c.url || '').trim();

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
                    let channelUrl = rawLink.startsWith('http') ? rawLink : ('https://' + rawLink.replace(/^@/, 't.me/'));
                    const btnLabel = titleLower.includes('group') ? 'Join Group' : 'Join Channel';
                    return '<div class="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl flex items-center justify-between my-3">' +
                        '<div>' +
                            '<div class="flex items-center gap-2 mb-1">' +
                                '<h4 class="text-white font-bold text-sm sm:text-base">' + title + '</h4>' +
                                '<span class="px-2 py-0.5 text-[10px] font-bold rounded-md bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">FREE</span>' +
                            '</div>' +
                            '<p class="text-xs text-slate-400">' + sub + '</p>' +
                        '</div>' +
                        '<a href="' + channelUrl + '" target="_blank" class="px-4 py-2 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs rounded-xl no-underline transition-all shadow-md shrink-0">' + btnLabel + '</a>' +
                    '</div>';
                }
            }).join('');

        } catch (err) {
            console.error("Render error:", err);
        }
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', window.renderCleanChannels);
    } else {
        window.renderCleanChannels();
    }
    setInterval(window.renderCleanChannels, 4000);
})();
</script>
'''

if '</body>' in content:
    content = content.replace('</body>', script + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Channel rendering engine fixed successfully!")
