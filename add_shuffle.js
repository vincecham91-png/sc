const fs = require('fs');

const files = ["初二第3章复习.html", "初二第四章复习.html", "力与压强学习系统.html"];

for (const file of files) {
    let content = fs.readFileSync(file, 'utf8');

    // 1. Add shuffle function
    if (!content.includes('shuffleArray(array)')) {
        content = content.replace('let currentMCQIndex = 0;', `
        function shuffleArray(array) {
            for (let i = array.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [array[i], array[j]] = [array[j], array[i]];
            }
        }
        let currentMCQIndex = 0;`);
    }

    // 2. Add shuffle call in onload
    if (!content.includes('shuffleArray(mcqQuestions)')) {
        content = content.replace('window.onload = function() {\n            renderMCQ();', `window.onload = function() {
            shuffleArray(mcqQuestions);
            shuffleArray(saqQuestions);
            renderMCQ();`);
    }

    // 3. Add restart button in MCQ
    const mcqRegex = /document\.getElementById\('mcq-prev-btn'\)\.disabled\s*=\s*\(currentMCQIndex === 0\);\s*const nextBtn = document\.getElementById\('mcq-next-btn'\);\s*if\s*\(currentMCQIndex === mcqQuestions\.length - 1\)\s*\{([\s\S]*?)\}\s*else\s*\{([\s\S]*?)\}/;
    
    const mcqNew = `const prevBtn = document.getElementById('mcq-prev-btn');
            const nextBtn = document.getElementById('mcq-next-btn');
            if (currentMCQIndex === mcqQuestions.length - 1) {
                nextBtn.textContent = "🎁 玩个游戏提神！";
                nextBtn.disabled = false;
                nextBtn.style.background = "#f59e0b";
                nextBtn.onclick = function() { window.location.href = 'game.html'; };
                
                prevBtn.textContent = "🔄 重新开始";
                prevBtn.disabled = false;
                prevBtn.onclick = function() {
                    currentMCQIndex = 0;
                    shuffleArray(mcqQuestions);
                    renderMCQ();
                };
            } else {
                nextBtn.textContent = "下一题";
                nextBtn.disabled = false;
                nextBtn.style.background = "";
                nextBtn.onclick = nextMCQ;
                
                prevBtn.textContent = "上一题";
                prevBtn.disabled = (currentMCQIndex === 0);
                prevBtn.onclick = prevMCQ;
            }`;
    content = content.replace(mcqRegex, mcqNew);

    // 4. Add restart button in SAQ
    const saqRegex = /document\.getElementById\('saq-prev-btn'\)\.disabled\s*=\s*\(currentSAQIndex === 0\);\s*const nextBtn = document\.getElementById\('saq-next-btn'\);\s*if\s*\(currentSAQIndex === saqQuestions\.length - 1\)\s*\{([\s\S]*?)\}\s*else\s*\{([\s\S]*?)\}/;
    
    const saqNew = `const prevBtn = document.getElementById('saq-prev-btn');
            const nextBtn = document.getElementById('saq-next-btn');
            if (currentSAQIndex === saqQuestions.length - 1) {
                nextBtn.textContent = "🎁 玩个游戏提神！";
                nextBtn.disabled = false;
                nextBtn.style.background = "#f59e0b";
                nextBtn.onclick = function() { window.location.href = 'game.html'; };
                
                prevBtn.textContent = "🔄 重新开始";
                prevBtn.disabled = false;
                prevBtn.onclick = function() {
                    currentSAQIndex = 0;
                    shuffleArray(saqQuestions);
                    renderSAQ();
                };
            } else {
                nextBtn.textContent = "下一题";
                nextBtn.disabled = false;
                nextBtn.style.background = "";
                nextBtn.onclick = nextSAQ;
                
                prevBtn.textContent = "上一题";
                prevBtn.disabled = (currentSAQIndex === 0);
                prevBtn.onclick = prevSAQ;
            }`;
    content = content.replace(saqRegex, saqNew);

    fs.writeFileSync(file, content);
}
console.log("Updated all chapters");
