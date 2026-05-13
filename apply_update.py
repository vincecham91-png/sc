import os
import shutil
import glob
import re

sc_dir = r"c:\Users\PC\Downloads\sc"
assets_dir = os.path.join(sc_dir, "assets")
os.makedirs(assets_dir, exist_ok=True)

brain_dir = r"C:\Users\PC\.gemini\antigravity\brain\f2fcb6e8-c787-4856-9010-de95c3895750"
for img in ["panda_scientist", "panda_doctor", "panda_astronaut", "panda_explorer"]:
    files = glob.glob(os.path.join(brain_dir, img + "*.png"))
    if files:
        shutil.copy(files[0], os.path.join(assets_dir, img + ".png"))

index_file = os.path.join(sc_dir, "index.html")
with open(index_file, "r", encoding="utf-8") as f:
    idx_content = f.read()

modal_and_leaderboard = '''
    <!-- REGISTRATION MODAL -->
    <div id="registration-modal" class="fixed inset-0 bg-slate-900/80 backdrop-blur-md z-50 flex items-center justify-center transition-opacity duration-300">
        <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full mx-4 transform transition-transform duration-300 scale-100">
            <h2 class="text-2xl font-black text-center mb-2 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">🌟 创建你的学习角色</h2>
            <p class="text-slate-500 text-center text-sm mb-6">请输入名字并选择你的专属熊猫吉祥物，准备开始挑战！</p>
            
            <div class="mb-5">
                <label class="block text-sm font-bold text-slate-700 mb-2">你的名字</label>
                <input type="text" id="student-name-input" class="w-full px-4 py-3 rounded-xl border border-slate-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all" placeholder="例如：张小明">
            </div>
            
            <label class="block text-sm font-bold text-slate-700 mb-2">选择吉祥物</label>
            <div class="grid grid-cols-4 gap-3 mb-8" id="avatar-selection">
                <div class="avatar-option cursor-pointer rounded-xl border-2 border-blue-500 bg-blue-50 p-2 text-center transition-all" onclick="selectAvatar('panda_scientist.png', this)">
                    <img src="assets/panda_scientist.png" class="w-16 h-16 rounded-full mx-auto shadow-sm" alt="Scientist">
                </div>
                <div class="avatar-option cursor-pointer rounded-xl border-2 border-transparent hover:border-pink-300 p-2 text-center transition-all" onclick="selectAvatar('panda_doctor.png', this)">
                    <img src="assets/panda_doctor.png" class="w-16 h-16 rounded-full mx-auto shadow-sm" alt="Doctor">
                </div>
                <div class="avatar-option cursor-pointer rounded-xl border-2 border-transparent hover:border-orange-300 p-2 text-center transition-all" onclick="selectAvatar('panda_astronaut.png', this)">
                    <img src="assets/panda_astronaut.png" class="w-16 h-16 rounded-full mx-auto shadow-sm" alt="Astronaut">
                </div>
                <div class="avatar-option cursor-pointer rounded-xl border-2 border-transparent hover:border-green-300 p-2 text-center transition-all" onclick="selectAvatar('panda_explorer.png', this)">
                    <img src="assets/panda_explorer.png" class="w-16 h-16 rounded-full mx-auto shadow-sm" alt="Explorer">
                </div>
            </div>
            
            <button onclick="submitRegistration()" class="w-full py-3.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold rounded-xl shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 hover:-translate-y-0.5 transition-all">
                🚀 开始学习之旅！
            </button>
        </div>
    </div>

    <!-- LEADERBOARD WIDGET -->
    <div id="leaderboard-widget" class="fixed bottom-6 right-6 z-40 bg-white/95 backdrop-blur-md border border-slate-200 shadow-2xl rounded-2xl w-72 overflow-hidden hidden transform transition-all duration-500 translate-y-4 opacity-0">
        <div class="bg-gradient-to-r from-indigo-600 to-blue-600 p-3 flex justify-between items-center cursor-pointer" onclick="toggleLeaderboard()">
            <h3 class="text-white font-bold text-sm"><i class="fa-solid fa-trophy text-yellow-300 mr-2"></i> 学霸风云榜</h3>
            <i id="lb-chevron" class="fa-solid fa-chevron-down text-white/80 text-xs transition-transform"></i>
        </div>
        <div id="lb-content" class="p-3 transition-all duration-300">
            <ul id="lb-list" class="space-y-2">
                <!-- Dynamically populated -->
            </ul>
        </div>
    </div>
'''

global_js = '''
    <script>
        // GLOBAL STATE
        window.studentName = "";
        window.studentAvatar = "";
        window.studentScore = 0;
        
        let leaderboardData = [
            { name: "李华", avatar: "assets/panda_scientist.png", score: 150 },
            { name: "王明", avatar: "assets/panda_explorer.png", score: 85 },
            { name: "张芳", avatar: "assets/panda_doctor.png", score: 45 }
        ];

        let selectedAvatarPath = "assets/panda_scientist.png";
        
        function selectAvatar(filename, el) {
            selectedAvatarPath = "assets/" + filename;
            document.querySelectorAll('.avatar-option').forEach(opt => {
                opt.classList.remove('border-blue-500', 'bg-blue-50');
                opt.classList.add('border-transparent');
            });
            el.classList.remove('border-transparent');
            el.classList.add('border-blue-500', 'bg-blue-50');
        }

        function submitRegistration() {
            const nameInput = document.getElementById('student-name-input').value.trim();
            if (!nameInput) {
                alert("请输入你的名字哦！");
                return;
            }
            window.studentName = nameInput;
            window.studentAvatar = selectedAvatarPath;
            window.studentScore = 0;
            
            const modal = document.getElementById('registration-modal');
            modal.style.opacity = '0';
            setTimeout(() => { modal.style.display = 'none'; }, 300);
            
            leaderboardData.push({ name: window.studentName, avatar: window.studentAvatar, score: window.studentScore, isMe: true });
            renderLeaderboard();
            
            const lbWidget = document.getElementById('leaderboard-widget');
            lbWidget.classList.remove('hidden');
            setTimeout(() => {
                lbWidget.classList.remove('translate-y-4', 'opacity-0');
            }, 100);
            
            const iframeWin = document.getElementById('content-frame').contentWindow;
            if(iframeWin && iframeWin.unlockQuiz) {
                iframeWin.unlockQuiz();
            }
        }

        function toggleLeaderboard() {
            const content = document.getElementById('lb-content');
            const icon = document.getElementById('lb-chevron');
            if (content.style.display === 'none') {
                content.style.display = 'block';
                icon.style.transform = 'rotate(0deg)';
            } else {
                content.style.display = 'none';
                icon.style.transform = 'rotate(180deg)';
            }
        }

        function renderLeaderboard() {
            leaderboardData.sort((a, b) => b.score - a.score);
            const list = document.getElementById('lb-list');
            list.innerHTML = '';
            
            leaderboardData.forEach((player, index) => {
                const isMe = player.isMe ? 'bg-blue-50 border border-blue-100' : '';
                const rankColor = index === 0 ? 'text-yellow-500' : index === 1 ? 'text-slate-400' : index === 2 ? 'text-amber-600' : 'text-slate-300';
                
                list.innerHTML += 
                    <li class="flex items-center justify-between p-2 rounded-lg  transition-all">
                        <div class="flex items-center">
                            <span class="w-5 font-bold  text-sm mr-1"></span>
                            <img src="" class="w-8 h-8 rounded-full shadow-sm mr-2 border border-slate-200 object-cover">
                            <span class="text-sm font-bold text-slate-700 "></span>
                        </div>
                        <span class="text-sm font-black "></span>
                    </li>
                ;
            });
        }

        window.updateScore = function(points) {
            window.studentScore += points;
            const myData = leaderboardData.find(p => p.isMe);
            if(myData) myData.score = window.studentScore;
            
            renderLeaderboard();
            
            const lbWidget = document.getElementById('leaderboard-widget');
            lbWidget.style.transform = 'scale(1.05)';
            setTimeout(() => { lbWidget.style.transform = 'scale(1)'; }, 200);
        };
'''
if "REGISTRATION MODAL" not in idx_content:
    idx_content = idx_content.replace('<!-- Main Content -->', modal_and_leaderboard + '\n    <!-- Main Content -->')
    idx_content = idx_content.replace('<script>', global_js)
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(idx_content)

chapters = ["初二第3章复习.html", "初二第四章复习.html", "力与压强学习系统.html"]
for chap in chapters:
    chap_file = os.path.join(sc_dir, chap)
    with open(chap_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "score-popup" not in content:
        css_inject = '''
        .score-popup {
            position: absolute;
            font-size: 2rem;
            font-weight: black;
            text-shadow: 0 2px 10px rgba(0,0,0,0.5);
            pointer-events: none;
            animation: floatUp 1s ease-out forwards;
            z-index: 1000;
        }
        @keyframes floatUp {
            0% { opacity: 0; transform: translateY(0) scale(0.5); }
            20% { opacity: 1; transform: translateY(-20px) scale(1.2); }
            100% { opacity: 0; transform: translateY(-60px) scale(1); }
        }
'''
        content = content.replace('</style>', css_inject + '\n    </style>')
    
    if "mcqStartTime" not in content:
        js_timer_logic = '''
        let mcqStartTime = 0;
        let isAnswered = false;
        
        window.unlockQuiz = function() {
            if(document.getElementById('mcq-slides').classList.contains('active')) {
                mcqStartTime = Date.now();
            }
        };

        function showScorePopup(points, text, element) {
            const popup = document.createElement('div');
            popup.className = 'score-popup';
            const color = points > 0 ? '#10b981' : '#ef4444';
            const sign = points > 0 ? '+' : '';
            popup.innerHTML = <span style="color:"></span><br><span style="font-size:1rem; color:#fff"></span>;
            
            const rect = element.getBoundingClientRect();
            popup.style.left = (rect.left + rect.width/2 - 40) + 'px';
            popup.style.top = (rect.top - 20) + 'px';
            
            document.body.appendChild(popup);
            setTimeout(() => popup.remove(), 1000);
            
            if(window.parent && window.parent.updateScore) {
                window.parent.updateScore(points);
            }
        }
'''
        content = content.replace('let currentMCQIndex = 0;', js_timer_logic + '\n        let currentMCQIndex = 0;')
    
    new_check_logic = '''
            const timeTaken = (Date.now() - mcqStartTime) / 1000;
            let points = 0;
            let msg = "";

            if (selectedIndex === data.correct) {
                element.classList.add('correct');
                if (timeTaken <= 3) { points = 20; msg = "⚡极速！"; }
                else if (timeTaken <= 5) { points = 10; msg = "⏱️快速！"; }
                else if (timeTaken <= 10) { points = 5; msg = "👍不错！"; }
                else { points = 0; msg = "🐌超时无分"; }
            } else {
                element.classList.add('wrong');
                optionsList[data.correct].classList.add('correct');
                points = -20;
                msg = "❌扣分";
            }
            
            showScorePopup(points, msg, element);
'''
    content = re.sub(
        r"if\s*\(\s*selectedIndex\s*===\s*data\.correct\s*\)\s*\{\s*element\.classList\.add\('correct'\);\s*\}\s*else\s*\{\s*element\.classList\.add\('wrong'\);\s*optionsList\[data\.correct\]\.classList\.add\('correct'\);\s*\}",
        new_check_logic,
        content
    )
    
    if "isAnswered = false;" not in content.replace("let isAnswered = false;", ""): # Just check if we added it to renderMCQ
        content = content.replace("document.getElementById('mcq-prev-btn').disabled", "mcqStartTime = Date.now();\n            document.getElementById('mcq-prev-btn').disabled")
    
    show_section_replace = '''
        function showSection(sectionId) {
            if ((sectionId === 'mcq-slides' || sectionId === 'saq-slides') && window.parent && window.parent.studentName === "") {
                alert("请先完成首页的角色创建才能答题哦！");
                return;
            }
            if (sectionId === 'mcq-slides') {
                mcqStartTime = Date.now();
            }
'''
    content = content.replace('function showSection(sectionId) {', show_section_replace)

    with open(chap_file, "w", encoding="utf-8") as f:
        f.write(content)
