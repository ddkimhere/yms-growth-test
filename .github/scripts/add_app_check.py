from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = '''import { initializeApp as initializeModularApp } from "https://www.gstatic.com/firebasejs/12.16.0/firebase-app.js";
import { getAI, getGenerativeModel, GoogleAIBackend } from "https://www.gstatic.com/firebasejs/12.16.0/firebase-ai.js";'''
new = '''import { initializeApp as initializeModularApp } from "https://www.gstatic.com/firebasejs/12.16.0/firebase-app.js";
import { initializeAppCheck, ReCaptchaEnterpriseProvider } from "https://www.gstatic.com/firebasejs/12.16.0/firebase-app-check.js";
import { getAI, getGenerativeModel, GoogleAIBackend } from "https://www.gstatic.com/firebasejs/12.16.0/firebase-ai.js";'''

if old not in s:
    raise SystemExit('AI module imports not found')
s = s.replace(old, new, 1)

old2 = '''      const app=initializeModularApp(firebaseConfig,'yms-ai-evaluation');
      const ai=getAI(app,{backend:new GoogleAIBackend()});'''
new2 = '''      const app=initializeModularApp(firebaseConfig,'yms-ai-evaluation');
      initializeAppCheck(app,{
        provider:new ReCaptchaEnterpriseProvider('6Ldq4YgtAAAAALQVJCU0XqmKGBR-cedGh77SBCEC'),
        isTokenAutoRefreshEnabled:true
      });
      const ai=getAI(app,{backend:new GoogleAIBackend()});'''

if old2 not in s:
    raise SystemExit('AI app initialization block not found')
s = s.replace(old2, new2, 1)

p.write_text(s, encoding='utf-8')
