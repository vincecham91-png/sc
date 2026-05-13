import re

files = ["力与压强学习系统.html"]
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    mcq_target = "document.getElementById('mcq-next-btn').disabled = (currentMCQIndex === mcqQuestions.length - 1);"
    mcq_repl = """const nextBtn = document.getElementById('mcq-next-btn');
            if (currentMCQIndex === mcqQuestions.length - 1) {
                nextBtn.textContent = "🎁 玩个游戏提神！";
                nextBtn.disabled = false;
                nextBtn.style.background = "#f59e0b";
                nextBtn.onclick = function() { window.location.href = 'game.html'; };
            } else {
                nextBtn.textContent = "下一题";
                nextBtn.disabled = false;
                nextBtn.style.background = "";
                nextBtn.onclick = nextMCQ;
            }"""
            
    saq_target = "document.getElementById('saq-next-btn').disabled = (currentSAQIndex === saqQuestions.length - 1);"
    saq_repl = """const nextBtn = document.getElementById('saq-next-btn');
            if (currentSAQIndex === saqQuestions.length - 1) {
                nextBtn.textContent = "🎁 玩个游戏提神！";
                nextBtn.disabled = false;
                nextBtn.style.background = "#f59e0b";
                nextBtn.onclick = function() { window.location.href = 'game.html'; };
            } else {
                nextBtn.textContent = "下一题";
                nextBtn.disabled = false;
                nextBtn.style.background = "";
                nextBtn.onclick = nextSAQ;
            }"""
            
    content = content.replace(mcq_target, mcq_repl)
    content = content.replace(saq_target, saq_repl)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
