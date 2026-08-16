from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old='''  <div class="panel ai-eval-panel"><h2>AI 담당교사 평가서</h2>
    <div class="ai-eval-top">
      <button class="btn btn-save" id="generateAiComment" type="button">✨ AI 평가서 만들기</button>
      <span class="hint" id="aiStatus">시험 결과를 입력한 뒤 AI 평가서를 생성하세요.</span>
    </div>
    <div class="field" style="margin-top:12px"><label>담당교사 Comment · AI 초안 (수정 가능)</label><textarea id="aiComment" class="ai-comment-input" placeholder="AI 평가서가 여기에 생성됩니다."></textarea></div>
    <details class="teacher-memo-details"><summary>선생님 추가 메모</summary><div class="grid" style="grid-template-columns:1fr 1fr;margin-top:10px">
      <div class="field"><label>강점 추가 메모</label><textarea id="strengthMemo"></textarea></div>
      <div class="field"><label>보완점 추가 메모</label><textarea id="growthMemo"></textarea></div>
    </div></details>
  </div>'''

new='''  <div class="panel ai-eval-panel"><h2>AI 담당교사 평가서</h2>
    <div class="ai-eval-layout">
      <aside class="recent-tests-box">
        <div class="recent-tests-title">최근 Growth Test</div>
        <div class="recent-tests-sub">현재 학생의 최근 평가 기록</div>
        <div id="recentTestsList" class="recent-tests-list"><div class="recent-empty">저장된 평가가 없습니다.</div></div>
      </aside>
      <div class="ai-eval-main">
        <div class="ai-eval-top">
          <button class="btn btn-save" id="generateAiComment" type="button">✨ AI 평가서 만들기</button>
          <span class="hint" id="aiStatus">시험 결과를 입력한 뒤 AI 평가서를 생성하세요.</span>
        </div>
        <div class="field" style="margin-top:12px"><label>담당교사 Comment · AI 초안 (수정 가능)</label><textarea id="aiComment" class="ai-comment-input" placeholder="AI 평가서가 여기에 생성됩니다."></textarea></div>
        <details class="teacher-memo-details"><summary>선생님 추가 메모</summary><div class="grid" style="grid-template-columns:1fr 1fr;margin-top:10px">
          <div class="field"><label>강점 추가 메모</label><textarea id="strengthMemo"></textarea></div>
          <div class="field"><label>보완점 추가 메모</label><textarea id="growthMemo"></textarea></div>
        </div></details>
      </div>
    </div>
  </div>'''

if old not in s:
    raise SystemExit('AI panel block not found')
s=s.replace(old,new,1)

css='''
.ai-eval-layout{display:grid;grid-template-columns:230px minmax(0,1fr);gap:18px;align-items:start}
.recent-tests-box{background:#f7f9fc;border:1px solid var(--line);border-radius:13px;padding:14px}
.recent-tests-title{font-size:13px;font-weight:900;color:var(--navy)}
.recent-tests-sub{font-size:10.5px;color:var(--slate);margin-top:2px;margin-bottom:10px}
.recent-tests-list{display:flex;flex-direction:column;gap:8px}
.recent-test-item{background:#fff;border:1px solid #e3e9f2;border-radius:10px;padding:9px 10px}
.recent-test-top{display:flex;align-items:center;justify-content:space-between;gap:8px}
.recent-test-code{font-size:12px;font-weight:900;color:var(--navy)}
.recent-test-score{font-size:16px;font-weight:900;color:var(--blue)}
.recent-test-date{font-size:10px;color:var(--slate);margin-top:2px}
.recent-empty{font-size:11px;color:var(--slate);padding:12px 4px;text-align:center}
.ai-eval-main{min-width:0}
@media(max-width:760px){.ai-eval-layout{grid-template-columns:1fr}.recent-tests-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:480px){.recent-tests-list{grid-template-columns:1fr}}
'''
s=s.replace('</style>',css+'\n</style>',1)

marker='''function applyAiCommentToReport(){
  const text=(window.AI_COMMENT||'').trim();
  if(!text)return;
  const p=document.querySelector('#card .comment p');
  if(p)p.textContent=text;
}
const card=document.getElementById('card');
if(card)new MutationObserver(()=>applyAiCommentToReport()).observe(card,{childList:true,subtree:true});'''
replacement='''function applyAiCommentToReport(){
  const text=(window.AI_COMMENT||'').trim();
  if(!text)return;
  const p=document.querySelector('#card .comment p');
  if(p)p.textContent=text;
}
function renderRecentTests(){
  const list=document.getElementById('recentTestsList');
  if(!list)return;
  const name=$('name').value.trim();
  if(!name){list.innerHTML='<div class="recent-empty">학생명을 입력하면 최근 평가가 표시됩니다.</div>';return;}
  const rows=(REPORTS_CACHE||[])
    .filter(r=>String(r.name||'').trim()===name)
    .sort((a,b)=>String(b.date||'').localeCompare(String(a.date||'')))
    .slice(0,4);
  if(!rows.length){list.innerHTML='<div class="recent-empty">저장된 평가가 없습니다.</div>';return;}
  list.innerHTML=rows.map(r=>`<div class="recent-test-item"><div class="recent-test-top"><span class="recent-test-code">${esc(r.testCode||'-')}</span><span class="recent-test-score">${Number(r.score)||0}점</span></div><div class="recent-test-date">${esc(r.date||'-')}</div></div>`).join('');
}
window.renderRecentTests=renderRecentTests;
const card=document.getElementById('card');
if(card)new MutationObserver(()=>{applyAiCommentToReport();renderRecentTests();}).observe(card,{childList:true,subtree:true});'''
if marker not in s:
    raise SystemExit('AI observer block not found')
s=s.replace(marker,replacement,1)
p.write_text(s,encoding='utf-8')
