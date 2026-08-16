from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

old='''<div class="auth-overlay" id="authOverlay">
  <div class="login-card">
    <div class="login-logo"><div class="login-mark">YMS</div><div><div class="login-title">Growth Test 로그인</div><div class="login-sub">등록된 선생님 계정으로 로그인하세요.</div></div></div>
    <div class="field"><label>이메일</label><input id="loginEmail" type="email" autocomplete="username" placeholder="teacher@example.com"></div>
    <div class="field"><label>비밀번호</label><input id="loginPassword" type="password" autocomplete="current-password" placeholder="비밀번호"></div>
    <button class="btn btn-save" id="loginBtn" type="button">로그인</button>
    <div class="login-error" id="loginError"></div>
  </div>
</div>'''
new='''<div class="auth-overlay" id="authOverlay">
  <div class="login-card">
    <div class="login-logo"><div class="login-mark">YMS</div><div><div class="login-title">Growth Test 로그인</div><div class="login-sub">승인된 선생님만 이용할 수 있습니다.</div></div></div>
    <div id="teacherLoginBox">
      <div class="field"><label>핸드폰 번호 뒷자리 4자리</label><input id="teacherPin" type="password" inputmode="numeric" maxlength="4" autocomplete="off" placeholder="••••" style="text-align:center;font-size:22px;letter-spacing:.28em"></div>
      <button class="btn btn-save" id="teacherPinBtn" type="button">선생님 로그인</button>
      <div class="login-error" id="teacherPinError"></div>
      <button class="admin-login-link" id="showAdminLogin" type="button">운영자 로그인</button>
    </div>
    <div id="adminLoginBox" style="display:none">
      <div class="field"><label>운영자 이메일</label><input id="loginEmail" type="email" autocomplete="username" placeholder="운영자 이메일"></div>
      <div class="field"><label>비밀번호</label><input id="loginPassword" type="password" autocomplete="current-password" placeholder="비밀번호"></div>
      <button class="btn btn-save" id="loginBtn" type="button">운영자 로그인</button>
      <div class="login-error" id="loginError"></div>
      <button class="admin-login-link" id="backTeacherLogin" type="button">← 선생님 로그인으로</button>
    </div>
  </div>
</div>
<div class="pin-admin-modal" id="pinAdminModal">
  <div class="pin-admin-card">
    <div class="pin-admin-head"><div><b>승인번호 관리</b><span>선생님 핸드폰 뒷자리 4자리</span></div><button id="closePinAdmin" type="button">×</button></div>
    <div class="pin-add-row"><input id="newAllowedPin" inputmode="numeric" maxlength="4" placeholder="예: 1234"><button id="addAllowedPinBtn" type="button">추가</button></div>
    <div id="pinAdminStatus" class="pin-admin-status"></div>
    <div id="allowedPinList" class="allowed-pin-list"></div>
  </div>
</div>'''
if old not in s:
    raise SystemExit('login overlay marker not found')
s=s.replace(old,new,1)

css='''
.admin-login-link{width:100%;border:0;background:transparent;color:var(--slate);font-size:11.5px;font-weight:700;margin-top:12px;cursor:pointer;text-decoration:underline;text-underline-offset:3px}
.pin-admin-modal{position:fixed;inset:0;z-index:260;background:rgba(18,31,58,.38);display:none;align-items:center;justify-content:center;padding:20px}.pin-admin-modal.on{display:flex}
.pin-admin-card{width:min(430px,100%);max-height:78vh;overflow:auto;background:#fff;border-radius:18px;border:1px solid #dfe5ef;box-shadow:0 22px 70px rgba(22,38,74,.22);padding:22px}
.pin-admin-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:16px}.pin-admin-head b{display:block;color:var(--navy);font-size:17px}.pin-admin-head span{display:block;color:var(--slate);font-size:11px;margin-top:2px}.pin-admin-head button{border:0;background:var(--soft);width:30px;height:30px;border-radius:9px;color:var(--navy);font-size:20px;cursor:pointer}
.pin-add-row{display:grid;grid-template-columns:1fr 86px;gap:8px}.pin-add-row input{border:1px solid var(--line);border-radius:9px;padding:10px 12px;font-size:17px;text-align:center;letter-spacing:.15em}.pin-add-row button{border:0;border-radius:9px;background:var(--green);color:#fff;font-weight:800;cursor:pointer}
.pin-admin-status{min-height:20px;font-size:11px;color:var(--slate);margin:8px 0}.allowed-pin-list{display:flex;flex-direction:column;gap:7px}.pin-item{display:flex;align-items:center;justify-content:space-between;background:var(--soft);border:1px solid var(--line);padding:9px 11px;border-radius:10px}.pin-item b{color:var(--navy);letter-spacing:.12em}.pin-item button{border:0;background:#fff;color:var(--red);font-weight:800;font-size:11px;padding:5px 8px;border-radius:7px;cursor:pointer}
#managePinsBtn{display:none}
'''
if '.admin-login-link{' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

toolbar_marker='<button class="btn btn-ghost" id="logoutBtn" type="button" style="display:none">로그아웃</button>'
if 'id="managePinsBtn"' not in s:
    s=s.replace(toolbar_marker,'<button class="btn btn-ghost" id="managePinsBtn" type="button">승인번호 관리</button>'+toolbar_marker,1)

oldjs="""function authMessage(e){const m={'auth/invalid-credential':'이메일 또는 비밀번호를 확인해 주세요.','auth/invalid-email':'이메일 형식을 확인해 주세요.','auth/too-many-requests':'로그인 시도가 너무 많습니다. 잠시 후 다시 시도해 주세요.','auth/user-disabled':'비활성화된 계정입니다.'};return m[e?.code]||e?.message||'로그인에 실패했습니다.'}
async function doLogin(){$('loginError').textContent='';try{await auth.signInWithEmailAndPassword($('loginEmail').value.trim(),$('loginPassword').value)}catch(e){$('loginError').textContent=authMessage(e)}}
$('loginBtn').onclick=doLogin;$('loginPassword').addEventListener('keydown',e=>{if(e.key==='Enter')doLogin()});$('logoutBtn').onclick=()=>auth.signOut();
auth.onAuthStateChanged(async user=>{CURRENT_USER=user||null;if(user){$('authOverlay').classList.add('hidden');$('userChip').classList.add('on');$('userChip').textContent=user.email||'로그인됨';$('logoutBtn').style.display='inline-block';try{await loadCloudData();refreshStudentPick();buildRows();render()}catch(e){alert('로그인은 되었지만 Firestore 데이터를 읽지 못했습니다.')}}else{REPORTS_CACHE=[];META_CACHE={};$('authOverlay').classList.remove('hidden');$('userChip').classList.remove('on');$('logoutBtn').style.display='none';$('cloudStatus').textContent='로그인 필요'}});"""
newjs="""function authMessage(e){const m={'auth/invalid-credential':'이메일 또는 비밀번호를 확인해 주세요.','auth/invalid-email':'이메일 형식을 확인해 주세요.','auth/too-many-requests':'로그인 시도가 너무 많습니다. 잠시 후 다시 시도해 주세요.','auth/user-disabled':'비활성화된 계정입니다.','auth/operation-not-allowed':'Firebase Authentication에서 익명 로그인을 사용 설정해 주세요.'};return m[e?.code]||e?.message||'로그인에 실패했습니다.'}
let ACCESS_MODE='';
let PIN_LOGIN_BUSY=false;
async function enterGrowthApp(user,mode,label){CURRENT_USER=user;ACCESS_MODE=mode;$('authOverlay').classList.add('hidden');$('userChip').classList.add('on');$('userChip').textContent=label;$('logoutBtn').style.display='inline-block';$('managePinsBtn').style.display=mode==='admin'?'inline-block':'none';try{await loadCloudData();refreshStudentPick();buildRows();render()}catch(e){alert('로그인은 되었지만 Firestore 데이터를 읽지 못했습니다.')}}
async function doTeacherPinLogin(){const pin=$('teacherPin').value.trim(),err=$('teacherPinError');err.textContent='';if(!/^\\d{4}$/.test(pin)){err.textContent='핸드폰 번호 뒷자리 4자리를 입력해 주세요.';return}PIN_LOGIN_BUSY=true;try{let user=auth.currentUser;if(!user||!user.isAnonymous){if(user)await auth.signOut();const cred=await auth.signInAnonymously();user=cred.user}const doc=await db.collection('allowed_users').doc(pin).get();if(!doc.exists){sessionStorage.removeItem('ymsGrowthTeacherPin');await auth.signOut();err.textContent='승인되지 않은 번호입니다.';return}sessionStorage.setItem('ymsGrowthTeacherPin',pin);await enterGrowthApp(user,'teacher','선생님 · '+pin)}catch(e){err.textContent=authMessage(e)}finally{PIN_LOGIN_BUSY=false}}
async function doLogin(){$('loginError').textContent='';try{const c=await auth.signInWithEmailAndPassword($('loginEmail').value.trim(),$('loginPassword').value);sessionStorage.removeItem('ymsGrowthTeacherPin');await enterGrowthApp(c.user,'admin',c.user.email||'운영자')}catch(e){$('loginError').textContent=authMessage(e)}}
async function loadAllowedPins(){if(ACCESS_MODE!=='admin')return;const list=$('allowedPinList'),status=$('pinAdminStatus');list.innerHTML='';status.textContent='불러오는 중...';try{const snap=await db.collection('allowed_users').get();const pins=snap.docs.map(d=>d.id).filter(x=>/^\\d{4}$/.test(x)).sort();status.textContent='승인번호 '+pins.length+'개';pins.forEach(pin=>{const row=document.createElement('div');row.className='pin-item';row.innerHTML='<b>'+pin+'</b><button type="button">삭제</button>';row.querySelector('button').onclick=()=>deleteAllowedPin(pin);list.appendChild(row)})}catch(e){status.textContent='목록 불러오기 실패: '+e.message}}
async function addAllowedPin(){const pin=$('newAllowedPin').value.trim(),status=$('pinAdminStatus');if(!/^\\d{4}$/.test(pin)){status.textContent='4자리 숫자를 입력해 주세요.';return}try{await db.collection('allowed_users').doc(pin).set({createdAt:firebase.firestore.FieldValue.serverTimestamp(),createdBy:CURRENT_USER?.email||''},{merge:true});$('newAllowedPin').value='';await loadAllowedPins()}catch(e){status.textContent='추가 실패: '+e.message}}
async function deleteAllowedPin(pin){if(!confirm(pin+' 번호의 승인을 삭제할까요?'))return;try{await db.collection('allowed_users').doc(pin).delete();await loadAllowedPins()}catch(e){$('pinAdminStatus').textContent='삭제 실패: '+e.message}}
$('showAdminLogin').onclick=()=>{$('teacherLoginBox').style.display='none';$('adminLoginBox').style.display='block';$('loginError').textContent=''};$('backTeacherLogin').onclick=()=>{$('adminLoginBox').style.display='none';$('teacherLoginBox').style.display='block';$('teacherPinError').textContent=''};
$('teacherPinBtn').onclick=doTeacherPinLogin;$('teacherPin').addEventListener('keydown',e=>{if(e.key==='Enter')doTeacherPinLogin()});$('loginBtn').onclick=doLogin;$('loginPassword').addEventListener('keydown',e=>{if(e.key==='Enter')doLogin()});
$('managePinsBtn').onclick=()=>{$('pinAdminModal').classList.add('on');loadAllowedPins()};$('closePinAdmin').onclick=()=>$('pinAdminModal').classList.remove('on');$('addAllowedPinBtn').onclick=addAllowedPin;$('newAllowedPin').addEventListener('keydown',e=>{if(e.key==='Enter')addAllowedPin()});
$('logoutBtn').onclick=async()=>{sessionStorage.removeItem('ymsGrowthTeacherPin');ACCESS_MODE='';await auth.signOut()};
auth.onAuthStateChanged(async user=>{if(!user){CURRENT_USER=null;REPORTS_CACHE=[];META_CACHE={};ACCESS_MODE='';$('authOverlay').classList.remove('hidden');$('userChip').classList.remove('on');$('logoutBtn').style.display='none';$('managePinsBtn').style.display='none';$('cloudStatus').textContent='로그인 필요';return}if(PIN_LOGIN_BUSY)return;if(user.isAnonymous){const pin=sessionStorage.getItem('ymsGrowthTeacherPin');if(!pin){await auth.signOut();return}try{const doc=await db.collection('allowed_users').doc(pin).get();if(doc.exists)await enterGrowthApp(user,'teacher','선생님 · '+pin);else{sessionStorage.removeItem('ymsGrowthTeacherPin');await auth.signOut()}}catch(e){$('teacherPinError').textContent='승인 확인 실패: '+e.message}}else{await enterGrowthApp(user,'admin',user.email||'운영자')}});"""
if oldjs not in s:
    raise SystemExit('auth js marker not found')
s=s.replace(oldjs,newjs,1)
p.write_text(s,encoding='utf-8')
