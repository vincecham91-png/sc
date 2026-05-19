import os
import re

files = ["初二第3章复习.html", "初二第四章复习.html", "力与压强学习系统.html"]
base_dir = r"c:\Users\PC\Downloads\sc"

shuffle_func = """
        function shuffleArray(array) {
            for (let i = array.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [array[i], array[j]] = [array[j], array[i]];
            }
        }
        let currentMCQIndex = 0;"""

mcq_new = """const prevBtn = document.getElementById('mcq-prev-btn');
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
            }"""

saq_new = """const prevBtn = document.getElementById('saq-prev-btn');
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
            }"""

for f in files:
    filepath = os.path.join(base_dir, f)
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    # 1. Add shuffle function
    if "shuffleArray(array)" not in content:
        content = content.replace("let currentMCQIndex = 0;", shuffle_func)
    
    # 2. Call shuffle in onload
    if "shuffleArray(mcqQuestions)" not in content:
        content = re.sub(
            r"window\.onload\s*=\s*function\(\)\s*\{\s*renderMCQ\(\);",
            "window.onload = function() {\n            shuffleArray(mcqQuestions);\n            shuffleArray(saqQuestions);\n            renderMCQ();",
            content
        )

    # 3. Replace MCQ buttons
    mcq_pattern = r"document\.getElementById\('mcq-prev-btn'\)\.disabled\s*=\s*\(currentMCQIndex\s*===\s*0\);\s*const\s*nextBtn\s*=\s*document\.getElementById\('mcq-next-btn'\);\s*if\s*\(currentMCQIndex\s*===\s*mcqQuestions\.length\s*-\s*1\)\s*\{[\s\S]*?\}\s*else\s*\{[\s\S]*?\}"
    content = re.sub(mcq_pattern, mcq_new, content)

    # 4. Replace SAQ buttons
    saq_pattern = r"document\.getElementById\('saq-prev-btn'\)\.disabled\s*=\s*\(currentSAQIndex\s*===\s*0\);\s*const\s*nextBtn\s*=\s*document\.getElementById\('saq-next-btn'\);\s*if\s*\(currentSAQIndex\s*===\s*saqQuestions\.length\s*-\s*1\)\s*\{[\s\S]*?\}\s*else\s*\{[\s\S]*?\}"
    content = re.sub(saq_pattern, saq_new, content)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)

print("Updated all chapters with python")
