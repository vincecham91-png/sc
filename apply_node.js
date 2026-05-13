const fs = require('fs');

const files = ['初二第3章复习.html', '初二第四章复习.html', '力与压强学习系统.html'];

for (const file of files) {
    if (!fs.existsSync(file)) continue;
    let content = fs.readFileSync(file, 'utf8');

    if (!content.includes('.score-popup')) {
        const cssInject = 
        .score-popup {
            position: absolute;
            font-size: 2rem;
            font-weight: 900;
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
    </style>;
        content = content.replace('</style>', cssInject);
    }

    if (!content.includes('mcqStartTime')) {
        const jsTimerLogic = 
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
            popup.innerHTML = \<span style="color:\">\\</span><br><span style="font-size:1rem; color:#fff">\</span>\;
            
            const rect = element.getBoundingClientRect();
            popup.style.left = (rect.left + rect.width/2 - 40) + 'px';
            popup.style.top = (rect.top - 20) + 'px';
            
            document.body.appendChild(popup);
            setTimeout(() => popup.remove(), 1000);
            
            if(window.parent && window.parent.updateScore) {
                window.parent.updateScore(points);
            }
        }
        let currentMCQIndex = 0;;
        content = content.replace('let currentMCQIndex = 0;', jsTimerLogic);
    }

    const checkRegex = /if\s*\(\s*selectedIndex\s*===\s*data\.correct\s*\)\s*\{\s*element\.classList\.add\('correct'\);\s*\}\s*else\s*\{\s*element\.classList\.add\('wrong'\);\s*optionsList\[data\.correct\]\.classList\.add\('correct'\);\s*\}/;
    if (checkRegex.test(content)) {
        const newCheckLogic = 
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
        ;
        content = content.replace(checkRegex, newCheckLogic);
    }

    if (!content.includes('mcqStartTime = Date.now();') && content.includes("document.getElementById('mcq-prev-btn').disabled =")) {
        content = content.replace(
            "document.getElementById('mcq-prev-btn').disabled =", 
            "mcqStartTime = Date.now();\n            document.getElementById('mcq-prev-btn').disabled ="
        );
    }

    if (content.includes('function showSection(sectionId) {') && !content.includes('window.parent.studentName === ""')) {
        const showSectionReplace = 
        function showSection(sectionId) {
            if ((sectionId === 'mcq-slides' || sectionId === 'saq-slides') && window.parent && window.parent.studentName === "") {
                alert("请先在首页创建熊猫角色才能答题哦！");
                return;
            }
            if (sectionId === 'mcq-slides') {
                mcqStartTime = Date.now();
            }
;
        content = content.replace('function showSection(sectionId) {', showSectionReplace);
    }

    fs.writeFileSync(file, content, 'utf8');
}
console.log('Update Complete');
