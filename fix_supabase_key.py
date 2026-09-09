import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Valid Supabase Anon Key
NEW_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhidWh0cnhoenBqaWlpcWVsdWhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODg4ODE4ODgsImV4cCI6MjEwNDQ1Nzg4OH0.s0tBaDZJs5_RxVtgDf5M50owUbeEIcrCciLk4FTYXNc"

# Remove any older inline scripts
content = re.sub(r'<!-- SUPABASE CLOUD ENGINE FOR CHANNELS -->[\s\S]*?</script>', '', content)

script = f'''
<!-- SUPABASE CLOUD ENGINE FOR CHANNELS -->
<script>
(function() {{
    const SUPABASE_URL = "https://xbuhtrxhzpjiiiqeluhh.supabase.co";
    const API_KEY = "{NEW_KEY}";

    if (!window.supabase) return;
    const db = window.supabase.createClient(SUPABASE_URL, API_KEY);

    window.loadCloudChannels = async function() {{
        try {{
            const {{ data, error }} = await db.from('channels').select('*').order('created_at', {{ ascending: false }});
            if (error) return console.error("Cloud fetch error:", error.message);

            if (data) localStorage.setItem('ts_channels', JSON.stringify(data));

            const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, div'));
            const channelHeader = headings.find(e => e.textContent && e.textContent.trim().toLowerCase().includes('channels & groups'));

            if (channelHeader && channelHeader.parentElement) {{
                let container = document.getElementById('public-cloud-channels-list');
                if (!container) {{
                    container = document.createElement('div');
                    container.id = 'public-cloud-channels-list';
                    container.className = 'space-y-3 my-3';
                    channelHeader.parentElement.appendChild(container);
                }}

                Array.from(channelHeader.parentElement.children).forEach(child => {{
                    if (child !== container && child !== channelHeader && !child.contains(channelHeader)) {{
                        if (child.innerText && (child.innerText.includes('No channels') || child.innerText.includes('Join Channel') || child.innerText.includes('Continue in Bot') || child.innerText.includes('FREE') || child.innerText.includes('PAID'))) {{
                            child.style.display = 'none';
                        }}
                    }}
                }});

                if (!data || data.length === 0) {{
                    container.innerHTML = '<div class="p-4 text-slate-400 text-xs text-center border border-dashed border-slate-700 rounded-2xl">No channels added yet.</div>';
                }} else {{
                    container.innerHTML = data.map(c => {{
                        const title = c.title || 'Untitled Channel';
                        const sub = c.description || c.subtitle || c.nameAm || 'Tenaspecial Community';
                        const rawLink = c.link || '';
                        
                        const titleLower = title.toLowerCase();
                        const subLower = sub.toLowerCase();
                        const isPaid = c.is_paid === true || c.price > 0 || titleLower.includes('paid') || titleLower.includes('premium') || subLower.includes('paid') || subLower.includes('premium');
                        
                        if (isPaid) {{
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
                        }} else {{
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
                        }}
                    }}).join('');
                }}
            }}
        }} catch (e) {{
            console.error("Error loading channels:", e);
        }}
    }};

    document.addEventListener('click', async function(e) {{
        const btn = e.target.closest('button, input[type="submit"], a');
        if (!btn) return;

        const text = (btn.innerText || btn.value || '').toLowerCase();
        if (text.includes('save') || text.includes('add')) {{
            const formBox = btn.closest('form') || btn.closest('div.bg-slate-900') || btn.closest('div.p-4') || btn.parentElement.parentElement;
            if (formBox) {{
                const inputs = Array.from(formBox.querySelectorAll('input, select'));
                let titleVal = '', linkVal = '', descVal = '', isPaid = false;

                inputs.forEach(inp => {{
                    const val = inp.value.trim();
                    if (!val) return;
                    const placeholder = (inp.placeholder || inp.name || '').toLowerCase();
                    
                    if (val.startsWith('http') || val.includes('t.me') || val.includes('.')) {{
                        linkVal = val;
                    }} else if (placeholder.includes('sub') || placeholder.includes('amharic') || placeholder.includes('desc')) {{
                        descVal = val;
                    }} else if (inp.type === 'checkbox' || inp.type === 'radio') {{
                        if (inp.checked && (val.toLowerCase().includes('paid') || val === 'true')) isPaid = true;
                    }} else if (inp.tagName === 'SELECT' && (val.toLowerCase().includes('paid') || val.toLowerCase().includes('premium'))) {{
                        isPaid = true;
                    }} else if (!titleVal) {{
                        titleVal = val;
                    }} else if (!descVal) {{
                        descVal = val;
                    }}
                }});

                if (titleVal && linkVal) {{
                    e.preventDefault();
                    e.stopPropagation();

                    if (titleVal.toLowerCase().includes('paid') || titleVal.toLowerCase().includes('premium')) {{
                        isPaid = true;
                    }}

                    const payload = {{
                        title: titleVal,
                        link: linkVal,
                        description: descVal || 'Tenaspecial Community',
                        is_paid: isPaid,
                        item_type: 'channel'
                    }};

                    let {{ error }} = await db.from('channels').insert([payload]);

                    if (error && error.message && error.message.includes('column')) {{
                        delete payload.is_paid;
                        delete payload.description;
                        const retry = await db.from('channels').insert([payload]);
                        error = retry.error;
                    }}

                    if (error) {{
                        alert("❌ Save Failed: " + error.message);
                    }} else {{
                        alert("✅ Saved to Cloud Database successfully!");
                        inputs.forEach(inp => {{ if (inp.type !== 'submit' && inp.type !== 'button') inp.value = ''; }});
                        await window.loadCloudChannels();
                    }}
                }}
            }}
        }}
    }}, true);

    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', window.loadCloudChannels);
    }} else {{
        window.loadCloudChannels();
    }}
    setInterval(window.loadCloudChannels, 8000);
}})();
</script>
'''

if '</body>' in content:
    content = content.replace('</body>', script + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Supabase API key updated successfully!")
