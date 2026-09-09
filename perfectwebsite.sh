mkdir -p tenaspecial-web && cd tenaspecial-web

# 1. Generate updated HTML
cat << 'EOF' > index.html
<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tena Special | Modern Healthcare Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        brand: {
                            50: '#f0f9ff',
                            100: '#e0f2fe',
                            500: '#0284c7',
                            600: '#0369a1',
                            700: '#075985',
                            800: '#0c4a6e',
                        }
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans pb-20 md:pb-0">

    <!-- TOP ANNOUNCEMENT BAR WITH UPDATED EMERGENCY NUMBERS -->
    <div class="bg-brand-800 text-white text-xs py-2 px-4 text-center flex flex-wrap justify-between items-center gap-2">
        <span class="truncate"><i class="fa-solid fa-hospital-user mr-1 text-sky-300"></i> 24/7 Virtual Consultation & Emergency Dispatch</span>
        <div class="flex items-center space-x-2">
            <a href="tel:+251967449552" class="bg-red-600 hover:bg-red-700 text-white font-bold px-3 py-0.5 rounded-full text-xs transition">
                <i class="fa-solid fa-phone-volume mr-1"></i> +251967449552
            </a>
            <a href="tel:+251908343267" class="bg-red-600 hover:bg-red-700 text-white font-bold px-3 py-0.5 rounded-full text-xs transition">
                <i class="fa-solid fa-phone-volume mr-1"></i> +251908343267
            </a>
        </div>
    </div>

    <!-- MAIN NAVBAR -->
    <nav class="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16 items-center">
                <div class="flex items-center space-x-3 cursor-pointer" onclick="showSection('hero')">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-sky-400 flex items-center justify-center text-white shadow-md">
                        <i class="fa-solid fa-heart-pulse text-xl"></i>
                    </div>
                    <div>
                        <span class="text-xl font-extrabold tracking-tight text-slate-900">Tena<span class="text-brand-600">Special</span></span>
                        <span class="block text-[10px] text-slate-500 font-medium tracking-widest uppercase">Healthcare Hub</span>
                    </div>
                </div>

                <div class="hidden md:flex space-x-8 text-sm font-semibold text-slate-600">
                    <button onclick="showSection('specialists')" class="hover:text-brand-600 transition py-2">Specialists</button>
                    <button onclick="showSection('communities')" class="hover:text-brand-600 transition py-2">Channels & Groups</button>
                    <button onclick="showSection('store')" class="hover:text-brand-600 transition py-2">Digital Store</button>
                    <button onclick="showSection('homecare')" class="hover:text-brand-600 transition py-2">Home Care</button>
                    <button onclick="showSection('emergency')" class="hover:text-brand-600 transition py-2 text-rose-600">Emergency</button>
                </div>

                <div class="hidden md:flex items-center space-x-3">
                    <a href="https://t.me/tenaspecial" target="_blank" class="text-slate-500 hover:text-brand-600 text-xs font-bold px-3 py-2 border rounded-xl flex items-center">
                        <i class="fa-brands fa-telegram mr-1.5 text-sky-500 text-sm"></i> Help: @tenaspecial
                    </a>
                    <button onclick="openBookingModal()" class="bg-brand-600 hover:bg-brand-700 text-white px-5 py-2.5 rounded-xl font-semibold shadow-md transition text-sm flex items-center">
                        <i class="fa-regular fa-calendar-check mr-2"></i> Book Service
                    </button>
                </div>

                <button onclick="toggleMobileMenu()" class="md:hidden text-slate-600 text-2xl focus:outline-none">
                    <i class="fa-solid fa-bars-staggered"></i>
                </button>
            </div>
        </div>

        <div id="mobileMenu" class="hidden md:hidden bg-white border-b border-slate-200 px-4 pt-2 pb-6 space-y-3 shadow-xl">
            <button onclick="showSection('specialists'); toggleMobileMenu()" class="block w-full text-left py-2 text-slate-700 font-medium border-b border-slate-100">🩺 Specialists Directory</button>
            <button onclick="showSection('communities'); toggleMobileMenu()" class="block w-full text-left py-2 text-slate-700 font-medium border-b border-slate-100">💬 Telegram Channels & Groups</button>
            <button onclick="showSection('store'); toggleMobileMenu()" class="block w-full text-left py-2 text-slate-700 font-medium border-b border-slate-100">🛍️ Digital Store & eBooks</button>
            <button onclick="showSection('homecare'); toggleMobileMenu()" class="block w-full text-left py-2 text-slate-700 font-medium border-b border-slate-100">🏠 የቤት ለቤት ህክምና (Home Care)</button>
            <button onclick="showSection('emergency'); toggleMobileMenu()" class="block w-full text-left py-2 text-rose-600 font-semibold border-b border-slate-100">🚨 Emergency Ambulance</button>
            <a href="https://t.me/tenaspecial" target="_blank" class="block w-full text-center py-2 bg-sky-50 text-sky-700 font-bold rounded-xl border border-sky-100">
                <i class="fa-brands fa-telegram mr-1"></i> Telegram Support: @tenaspecial
            </a>
            <button onclick="openBookingModal(); toggleMobileMenu()" class="w-full mt-2 bg-brand-600 text-white py-3 rounded-xl font-bold shadow-md">Book Appointment Now</button>
        </div>
    </nav>

    <!-- HERO SECTION -->
    <section id="hero" class="relative bg-gradient-to-b from-sky-50/80 via-white to-slate-50 py-12 md:py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid md:grid-cols-2 gap-12 items-center">
                <div class="space-y-6 text-center md:text-left">
                    <div class="inline-flex items-center space-x-2 bg-sky-100/80 text-brand-700 px-3 py-1 rounded-full text-xs font-semibold">
                        <span class="w-2 h-2 rounded-full bg-brand-500 animate-pulse"></span>
                        <span>Superadmin Approval Protection Active</span>
                    </div>
                    <h1 class="text-3xl sm:text-4xl md:text-5xl font-black text-slate-900 leading-tight">
                        Expert Healthcare <br><span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-600 to-sky-500">At Your Service</span>
                    </h1>
                    <p class="text-slate-600 text-base sm:text-lg leading-relaxed max-w-xl">
                        Connect with top medical specialists, join our public & premium Telegram communities, request home care visits, and dispatch emergency support.
                    </p>
                    <div class="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
                        <button onclick="showSection('communities')" class="bg-brand-600 hover:bg-brand-700 text-white font-bold px-6 py-3.5 rounded-xl shadow-lg transition flex items-center justify-center">
                            <i class="fa-brands fa-telegram mr-2"></i> Channels & Groups
                        </button>
                        <button onclick="openBookingModal()" class="bg-white border-2 border-slate-200 hover:border-brand-500 text-slate-700 font-bold px-6 py-3.5 rounded-xl transition flex items-center justify-center">
                            <i class="fa-regular fa-clock mr-2"></i> Book Quick Visit
                        </button>
                    </div>
                </div>

                <!-- Admin & Support Quick Contact Box -->
                <div class="bg-white p-6 sm:p-8 rounded-3xl shadow-xl border border-slate-100 space-y-4">
                    <h3 class="text-lg font-bold text-slate-900 flex items-center">
                        <i class="fa-solid fa-user-shield text-brand-600 mr-2"></i> Superadmin & Support Desk
                    </h3>
                    <p class="text-xs text-slate-500">All paid services on the website and bot are reviewed & verified directly by Superadmins.</p>
                    <div class="space-y-2">
                        <a href="https://t.me/tenaspecial" target="_blank" class="p-3 bg-sky-50 hover:bg-sky-100 rounded-xl flex items-center justify-between transition border border-sky-100">
                            <div class="flex items-center space-x-3">
                                <i class="fa-brands fa-telegram text-2xl text-sky-600"></i>
                                <div>
                                    <p class="text-xs font-bold text-slate-800">Help Username</p>
                                    <p class="text-xs text-brand-600 font-semibold">@tenaspecial</p>
                                </div>
                            </div>
                            <span class="text-xs font-bold text-sky-700 bg-sky-200 px-2.5 py-1 rounded-lg">Chat Now</span>
                        </a>
                        <a href="tel:+251908343267" class="p-3 bg-slate-50 hover:bg-slate-100 rounded-xl flex items-center justify-between transition border border-slate-200">
                            <div class="flex items-center space-x-3">
                                <i class="fa-solid fa-phone text-emerald-600 text-lg"></i>
                                <div>
                                    <p class="text-xs font-bold text-slate-800">Admin Line 1</p>
                                    <p class="text-xs text-slate-600 font-mono">+251908343267</p>
                                </div>
                            </div>
                            <i class="fa-solid fa-chevron-right text-xs text-slate-400"></i>
                        </a>
                        <a href="tel:+251967449552" class="p-3 bg-slate-50 hover:bg-slate-100 rounded-xl flex items-center justify-between transition border border-slate-200">
                            <div class="flex items-center space-x-3">
                                <i class="fa-solid fa-phone text-emerald-600 text-lg"></i>
                                <div>
                                    <p class="text-xs font-bold text-slate-800">Admin Line 2 & የቤት ለቤት</p>
                                    <p class="text-xs text-slate-600 font-mono">+251967449552</p>
                                </div>
                            </div>
                            <i class="fa-solid fa-chevron-right text-xs text-slate-400"></i>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- TELEGRAM CHANNELS & GROUPS SECTION -->
    <section id="communities" class="py-16 bg-slate-100 border-t border-b border-slate-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center max-w-2xl mx-auto mb-10">
                <span class="text-xs font-bold uppercase tracking-wider text-brand-600">Community Access</span>
                <h2 class="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1">Telegram Channels & Groups</h2>
                <p class="text-slate-500 text-sm mt-2">Join our free open communities or request superadmin-approved access to premium channels.</p>
            </div>

            <div class="grid md:grid-cols-2 gap-8">
                <!-- FREE CHANNELS & GROUPS -->
                <div class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-3">
                            <div class="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold">
                                <i class="fa-solid fa-unlock"></i>
                            </div>
                            <div>
                                <h3 class="font-extrabold text-slate-900 text-lg">Free Public Access</h3>
                                <p class="text-xs text-slate-500">Open for everyone to join immediately</p>
                            </div>
                        </div>
                        <span class="bg-emerald-100 text-emerald-800 text-xs font-bold px-3 py-1 rounded-full">FREE</span>
                    </div>

                    <div class="space-y-4">
                        <div class="p-4 bg-slate-50 rounded-2xl border border-slate-100 flex items-center justify-between">
                            <div>
                                <h4 class="font-bold text-slate-800 text-sm">Free Channel</h4>
                                <p class="text-xs text-slate-500">Public health tips & updates</p>
                            </div>
                            <a href="https://t.me/tenaspecialfreec" target="_blank" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-4 py-2 rounded-xl text-xs transition">
                                Join Channel
                            </a>
                        </div>
                        <div class="p-4 bg-slate-50 rounded-2xl border border-slate-100 flex items-center justify-between">
                            <div>
                                <h4 class="font-bold text-slate-800 text-sm">Free Group</h4>
                                <p class="text-xs text-slate-500">Community discussions & advice</p>
                            </div>
                            <a href="https://t.me/tenaspecialfreeg" target="_blank" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-4 py-2 rounded-xl text-xs transition">
                                Join Group
                            </a>
                        </div>
                    </div>
                </div>

                <!-- PREMIUM CHANNELS & GROUPS (REQUIRES SUPERADMIN APPROVAL) -->
                <div class="bg-white rounded-3xl p-6 sm:p-8 border border-amber-200 shadow-md space-y-6 relative overflow-hidden">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-3">
                            <div class="w-10 h-10 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center font-bold">
                                <i class="fa-solid fa-crown"></i>
                            </div>
                            <div>
                                <h3 class="font-extrabold text-slate-900 text-lg">Premium VIP Access</h3>
                                <p class="text-xs text-amber-600 font-semibold">Superadmin Verification Required</p>
                            </div>
                        </div>
                        <span class="bg-amber-500 text-white text-xs font-bold px-3 py-1 rounded-full">PAID</span>
                    </div>

                    <div class="space-y-4">
                        <div class="p-4 bg-amber-50/50 rounded-2xl border border-amber-100 flex items-center justify-between">
                            <div>
                                <h4 class="font-bold text-slate-800 text-sm">Premium Channel</h4>
                                <p class="text-xs text-slate-500">Exclusive doctor consultations & research</p>
                            </div>
                            <button onclick="requestPremiumAccess('Premium Channel', 'https://t.me/tenaspecialpremc')" class="bg-amber-600 hover:bg-amber-700 text-white font-bold px-4 py-2 rounded-xl text-xs transition">
                                Request Access
                            </button>
                        </div>
                        <div class="p-4 bg-amber-50/50 rounded-2xl border border-amber-100 flex items-center justify-between">
                            <div>
                                <h4 class="font-bold text-slate-800 text-sm">Premium Group</h4>
                                <p class="text-xs text-slate-500">Priority direct Q&A with specialists</p>
                            </div>
                            <button onclick="requestPremiumAccess('Premium Group', 'https://t.me/tenaspecialpremiumgroup')" class="bg-amber-600 hover:bg-amber-700 text-white font-bold px-4 py-2 rounded-xl text-xs transition">
                                Request Access
                            </button>
                        </div>
                    </div>
                    <p class="text-[11px] text-slate-400 italic text-center">Once payment screenshot is verified by Superadmin (@tenaspecial), direct access link will be granted.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- SPECIALISTS SECTION -->
    <section id="specialists" class="py-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-2xl mx-auto mb-10">
            <h2 class="text-2xl sm:text-3xl font-extrabold text-slate-900">Find & Book Medical Specialists</h2>
            <p class="text-slate-500 text-sm mt-2">Filter doctors by category and reserve direct consultation slots.</p>
        </div>

        <div class="flex overflow-x-auto pb-4 gap-2 no-scrollbar mb-8 justify-start md:justify-center">
            <button onclick="filterCategory('All')" class="cat-btn active bg-brand-600 text-white px-4 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition shadow-sm">All Specialists</button>
            <button onclick="filterCategory('General Medicine')" class="cat-btn bg-white border border-slate-200 hover:bg-slate-100 text-slate-700 px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition">General Medicine</button>
            <button onclick="filterCategory('Cardiology')" class="cat-btn bg-white border border-slate-200 hover:bg-slate-100 text-slate-700 px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition">Cardiology</button>
            <button onclick="filterCategory('Pediatrics')" class="cat-btn bg-white border border-slate-200 hover:bg-slate-100 text-slate-700 px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition">Pediatrics</button>
            <button onclick="filterCategory('Neurology')" class="cat-btn bg-white border border-slate-200 hover:bg-slate-100 text-slate-700 px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition">Neurology</button>
            <button onclick="filterCategory('Gynecology')" class="cat-btn bg-white border border-slate-200 hover:bg-slate-100 text-slate-700 px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition">Gynecology</button>
        </div>

        <div id="doctorsGrid" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6"></div>
    </section>

    <!-- DIGITAL STORE SECTION -->
    <section id="store" class="py-16 bg-slate-100 border-t border-b border-slate-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-end mb-10">
                <div>
                    <span class="text-xs font-bold uppercase tracking-wider text-brand-600">Digital Library</span>
                    <h2 class="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1">Medical Store & e-Books</h2>
                </div>
                <p class="text-slate-500 text-sm max-w-md mt-2 md:mt-0">Download clinical guidelines, medical textbooks, and health guides following superadmin approval.</p>
            </div>
            <div id="productsGrid" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6"></div>
        </div>
    </section>

    <!-- HOME CARE SECTION (የቤት ለቤት ህክምና) -->
    <section id="homecare" class="py-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-gradient-to-br from-emerald-600 to-teal-800 rounded-3xl p-8 sm:p-12 text-white shadow-2xl relative overflow-hidden">
            <div class="grid md:grid-cols-2 gap-8 items-center relative z-10">
                <div class="space-y-4">
                    <span class="bg-emerald-500/30 text-emerald-100 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">የቤት ለቤት ህክምና</span>
                    <h2 class="text-3xl font-black leading-tight">Home Medical Visit Dispatch</h2>
                    <p class="text-emerald-100 text-sm leading-relaxed">
                        Our licensed general practitioners and nurses bring clinical assessments, wound care, and health monitoring directly to your home.
                    </p>
                    <div class="pt-2 flex flex-col space-y-2">
                        <div class="flex items-center space-x-4">
                            <span class="text-2xl font-black text-amber-300">800 ETB</span>
                            <span class="text-xs text-emerald-200">/ Home Visit Consultation</span>
                        </div>
                        <p class="text-xs font-bold text-emerald-100"><i class="fa-solid fa-phone mr-1"></i> Direct Call: +251967449552</p>
                    </div>
                    <button onclick="openBookingModal('Home Care')" class="mt-4 bg-white text-emerald-900 font-bold px-6 py-3 rounded-xl shadow-lg hover:bg-emerald-50 transition">
                        Book Home Visit Online
                    </button>
                </div>
                <div class="bg-white/10 backdrop-blur-md p-6 rounded-2xl border border-white/20 space-y-3">
                    <h3 class="font-bold text-lg mb-2"><i class="fa-solid fa-square-check text-emerald-300 mr-2"></i> What's Included:</h3>
                    <p class="text-xs text-emerald-100 flex items-center"><i class="fa-solid fa-check text-xs mr-2"></i> Vital signs & comprehensive physical exam</p>
                    <p class="text-xs text-emerald-100 flex items-center"><i class="fa-solid fa-check text-xs mr-2"></i> On-site diagnostic testing & blood sampling</p>
                    <p class="text-xs text-emerald-100 flex items-center"><i class="fa-solid fa-check text-xs mr-2"></i> Prescription issuing & home treatment plans</p>
                </div>
            </div>
        </div>
    </section>

    <!-- EMERGENCY DISPATCH SECTION -->
    <section id="emergency" class="py-16 bg-rose-50 border-t border-rose-100">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div class="max-w-2xl mx-auto space-y-4">
                <div class="w-16 h-16 bg-rose-600 text-white rounded-full flex items-center justify-center mx-auto text-2xl shadow-lg animate-bounce">
                    <i class="fa-solid fa-truck-medical"></i>
                </div>
                <h2 class="text-3xl font-black text-slate-900">Emergency Ambulance Dispatch</h2>
                <p class="text-slate-600 text-sm">
                    Instant ambulance dispatch unit equipped with life-support tools and medical technicians.
                </p>
                <div class="p-6 bg-white rounded-2xl border border-rose-200 shadow-md inline-block text-center max-w-md w-full">
                    <p class="text-xs text-slate-500 uppercase font-bold tracking-wider">Emergency Hotline Numbers</p>
                    <div class="my-3 space-y-1">
                        <a href="tel:+251967449552" class="block text-2xl font-black text-rose-600 hover:underline">+251967449552</a>
                        <a href="tel:+251908343267" class="block text-2xl font-black text-rose-600 hover:underline">+251908343267</a>
                    </div>
                    <button onclick="openBookingModal('Emergency Ambulance')" class="w-full mt-3 bg-rose-600 hover:bg-rose-700 text-white font-bold py-3 rounded-xl shadow-md transition">
                        Dispatch Ambulance Request Online
                    </button>
                </div>
            </div>
        </div>
    </section>

    <!-- INTERACTIVE BOOKING & PAYMENT APPROVAL MODAL -->
    <div id="bookingModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl relative border border-slate-100 max-h-[90vh] overflow-y-auto">
            <button onclick="closeBookingModal()" class="absolute top-5 right-5 text-slate-400 hover:text-slate-600 text-xl">
                <i class="fa-solid fa-xmark"></i>
            </button>
            <div class="mb-6">
                <span id="modalServiceTag" class="text-xs font-bold text-brand-600 bg-sky-50 px-2.5 py-1 rounded-full uppercase tracking-wider">Superadmin Approval Workflow</span>
                <h3 id="modalTitle" class="text-2xl font-extrabold text-slate-900 mt-2">Service Booking & Verification</h3>
            </div>
            <form id="bookingForm" onsubmit="handleBookingSubmit(event)" class="space-y-4">
                <div>
                    <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Select Service / Product</label>
                    <select id="serviceSelect" onchange="updateModalFee()" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-brand-500 focus:outline-none"></select>
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Full Name</label>
                        <input type="text" required id="patientName" placeholder="Abebe Bikila" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-brand-500 focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Phone Number</label>
                        <input type="tel" required id="patientPhone" placeholder="0911223344" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-brand-500 focus:outline-none">
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Preferred Date</label>
                        <input type="date" required id="appointmentDate" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-brand-500 focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Time / Support Slot</label>
                        <select id="appointmentTime" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-brand-500 focus:outline-none">
                            <option>Morning (09:00 AM - 12:00 PM)</option>
                            <option>Afternoon (02:00 PM - 05:00 PM)</option>
                            <option>Evening (06:00 PM - 08:00 PM)</option>
                        </select>
                    </div>
                </div>
                <div class="p-4 bg-amber-50 rounded-2xl border border-amber-200 text-xs space-y-1.5 text-slate-700">
                    <div class="flex justify-between font-bold text-slate-900 text-sm">
                        <span>Required Payment:</span>
                        <span id="calculatedFeeDisplay" class="text-amber-700 font-extrabold">200 ETB</span>
                    </div>
                    <p class="text-slate-600">Telebirr / CBE Account: <code class="bg-white px-1.5 py-0.5 rounded font-mono text-slate-900 font-bold border">1000123456789</code></p>
                    <p class="text-[11px] text-amber-800 font-medium pt-1">⚠️ Notice: All payment submissions are routed directly to Superadmin (<span class="font-bold">@tenaspecial</span>) for mandatory verification before approval.</p>
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Upload Receipt Screenshot</label>
                    <input type="file" required accept="image/*" class="w-full text-xs text-slate-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100">
                </div>
                <button type="submit" class="w-full bg-brand-600 hover:bg-brand-700 text-white font-bold py-3.5 rounded-xl shadow-lg transition text-sm">
                    Submit Payment for Superadmin Approval
                </button>
            </form>
        </div>
    </div>

    <!-- MOBILE STICKY BOTTOM NAVIGATION -->
    <div class="md:hidden fixed bottom-0 left-0 right-0 bg-white/95 backdrop-blur-lg border-t border-slate-200 py-2 px-6 flex justify-between items-center z-40 text-slate-600">
        <button onclick="showSection('hero')" class="flex flex-col items-center text-xs font-medium focus:text-brand-600">
            <i class="fa-solid fa-house text-lg"></i>
            <span>Home</span>
        </button>
        <button onclick="showSection('communities')" class="flex flex-col items-center text-xs font-medium focus:text-brand-600">
            <i class="fa-brands fa-telegram text-lg"></i>
            <span>Groups</span>
        </button>
        <button onclick="openBookingModal()" class="flex flex-col items-center text-xs font-bold text-brand-600 -mt-5 bg-brand-50 p-2.5 rounded-full border-2 border-brand-600 shadow-md">
            <i class="fa-solid fa-calendar-plus text-xl"></i>
        </button>
        <button onclick="showSection('store')" class="flex flex-col items-center text-xs font-medium focus:text-brand-600">
            <i class="fa-solid fa-store text-lg"></i>
            <span>Store</span>
        </button>
        <button onclick="showSection('emergency')" class="flex flex-col items-center text-xs font-medium text-rose-600">
            <i class="fa-solid fa-truck-medical text-lg"></i>
            <span>Call</span>
        </button>
    </div>

    <script src="app.js"></script>
</body>
</html>
EOF

# 2. Generate updated JavaScript logic
cat << 'EOF' > app.js
const SPECIALISTS = [
    { id: 1, name: "Tazebachew Wudie", category: "General Medicine", qual: "MD, Senior Consultant", hospital: "Central Hospital", fee: 200, exp: "12 Years", rating: "4.9" },
    { id: 2, name: "Abebe Kebede", category: "Cardiology", qual: "MD, Interventional Cardiologist", hospital: "Heart Center", fee: 350, exp: "15 Years", rating: "5.0" },
    { id: 3, name: "Tigist Alemu", category: "Pediatrics", qual: "Pediatric Specialist", hospital: "Children's Clinic", fee: 250, exp: "8 Years", rating: "4.8" },
    { id: 4, name: "Mulugeta Tadesse", category: "Neurology", qual: "Neuro Consultant", hospital: "Specialized Hospital", fee: 400, exp: "10 Years", rating: "4.9" },
    { id: 5, name: "Bethlehem Haile", category: "Gynecology", qual: "OB-GYN Consultant", hospital: "Women Care Center", fee: 300, exp: "11 Years", rating: "4.9" }
];

const PRODUCTS = [
    { id: 101, title: "Clinical Assessment Guide 2026", price: 0, file: "clinical_guide.pdf", desc: "Essential medical reference for general practitioners." },
    { id: 102, title: "Pediatric Care Protocols PDF", price: 150, file: "pediatric_care.pdf", desc: "Comprehensive treatment manual for infant and child health." },
    { id: 103, title: "Cardiovascular Health eBook", price: 200, file: "cardio_ebook.pdf", desc: "In-depth guide on cardiac prevention and clinical management." }
];

document.addEventListener("DOMContentLoaded", () => {
    renderSpecialists(SPECIALISTS);
    renderProducts(PRODUCTS);
    populateServiceDropdown();
});

function renderSpecialists(list) {
    const grid = document.getElementById("doctorsGrid");
    grid.innerHTML = list.map(doc => `
        <div class="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm hover:shadow-md transition relative flex flex-col justify-between">
            <div>
                <div class="flex justify-between items-start mb-4">
                    <div class="w-12 h-12 rounded-xl bg-brand-50 text-brand-600 flex items-center justify-center font-bold text-xl">
                        👨‍⚕️
                    </div>
                    <span class="bg-amber-50 text-amber-700 text-xs font-bold px-2 py-1 rounded-lg flex items-center">
                        <i class="fa-solid fa-star text-amber-400 mr-1"></i> ${doc.rating}
                    </span>
                </div>
                <h3 class="font-bold text-slate-900 text-lg">Dr. ${doc.name}</h3>
                <p class="text-xs font-semibold text-brand-600">${doc.category}</p>
                <p class="text-xs text-slate-500 mt-1">${doc.qual} • ${doc.hospital}</p>
            </div>
            <div class="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
                <div>
                    <span class="text-xs text-slate-400 block">Fee</span>
                    <span class="text-lg font-black text-slate-900">${doc.fee} ETB</span>
                </div>
                <button onclick="openBookingModal('Doctor:${doc.id}')" class="bg-brand-600 hover:bg-brand-700 text-white text-xs font-bold px-4 py-2.5 rounded-xl transition">
                    Book Now
                </button>
            </div>
        </div>
    `).join('');
}

function renderProducts(list) {
    const grid = document.getElementById("productsGrid");
    grid.innerHTML = list.map(prod => `
        <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between">
            <div>
                <div class="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold text-lg mb-3">
                    📄
                </div>
                <h3 class="font-bold text-slate-900 text-base">${prod.title}</h3>
                <p class="text-xs text-slate-500 mt-2">${prod.desc}</p>
            </div>
            <div class="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
                <span class="text-sm font-bold ${prod.price === 0 ? 'text-emerald-600' : 'text-slate-900'}">
                    ${prod.price === 0 ? 'FREE' : prod.price + ' ETB'}
                </span>
                <button onclick="handleProductAction(${prod.id}, ${prod.price})" class="bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold px-4 py-2 rounded-xl transition">
                    ${prod.price === 0 ? 'Download PDF' : 'Request Access'}
                </button>
            </div>
        </div>
    `).join('');
}

function filterCategory(cat) {
    document.querySelectorAll('.cat-btn').forEach(btn => btn.classList.remove('active', 'bg-brand-600', 'text-white'));
    event.target.classList.add('active', 'bg-brand-600', 'text-white');
    
    if (cat === 'All') {
        renderSpecialists(SPECIALISTS);
    } else {
        const filtered = SPECIALISTS.filter(d => d.category.includes(cat));
        renderSpecialists(filtered);
    }
}

function populateServiceDropdown() {
    const select = document.getElementById("serviceSelect");
    let options = `<option value="general" data-fee="200">General Medical Visit (200 ETB)</option>`;
    SPECIALISTS.forEach(d => {
        options += `<option value="doc_${d.id}" data-fee="${d.fee}">Dr. ${d.name} - ${d.category} (${d.fee} ETB)</option>`;
    });
    options += `<option value="prem_chanel" data-fee="300">Premium Telegram Channel Access (300 ETB)</option>`;
    options += `<option value="prem_group" data-fee="300">Premium Telegram Group Access (300 ETB)</option>`;
    options += `<option value="homecare" data-fee="800">የቤት ለቤት ህክምና - Home Care Visit (800 ETB)</option>`;
    options += `<option value="emergency" data-fee="500">Emergency Ambulance Dispatch (500 ETB)</option>`;
    select.innerHTML = options;
}

function updateModalFee() {
    const select = document.getElementById("serviceSelect");
    const selectedOption = select.options[select.selectedIndex];
    const fee = selectedOption.getAttribute("data-fee") || 200;
    document.getElementById("calculatedFeeDisplay").innerText = `${fee} ETB`;
}

function requestPremiumAccess(type, link) {
    openBookingModal();
    if (type === 'Premium Channel') {
        document.getElementById("serviceSelect").value = "prem_chanel";
    } else {
        document.getElementById("serviceSelect").value = "prem_group";
    }
    updateModalFee();
}

function openBookingModal(preset = '') {
    const modal = document.getElementById("bookingModal");
    modal.classList.remove("hidden");
    
    if (preset.startsWith('Doctor:')) {
        const id = preset.split(':')[1];
        document.getElementById("serviceSelect").value = `doc_${id}`;
    } else if (preset === 'Home Care') {
        document.getElementById("serviceSelect").value = `homecare`;
    } else if (preset === 'Emergency Ambulance') {
        document.getElementById("serviceSelect").value = `emergency`;
    }
    updateModalFee();
}

function closeBookingModal() {
    document.getElementById("bookingModal").classList.add("hidden");
}

function toggleMobileMenu() {
    document.getElementById("mobileMenu").classList.toggle("hidden");
}

function showSection(id) {
    document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
}

function handleBookingSubmit(e) {
    e.preventDefault();
    alert("✅ Payment submission received! Request sent to Superadmin (@tenaspecial) for verification. Once confirmed, your service access link will be activated.");
    closeBookingModal();
}

function handleProductAction(id, price) {
    if (price === 0) {
        alert("📥 Free PDF download started.");
    } else {
        openBookingModal();
    }
}
EOF

# 3. Deploy directly to Surge
echo "🚀 Publishing website to tenaspecial.surge.sh..."
npx surge . tenaspecial.surge.sh