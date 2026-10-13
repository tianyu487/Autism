"""游戏渲染层:把一个训练模块渲染成自成一体的 HTML5 小游戏合辑(可点击、可离线)。

与视频渲染并列的"另一个渲染器":读同一份 TrainingModule(结构化内容),
不依赖 TTS/ffmpeg,产出单个 .html 文件(内联 CSS/JS,无外部依赖,可直接打开/售卖)。

一个模块可自动派生多种玩法(首页让孩子选,哪些可玩由内容决定):
- story    听故事:社交选择分支 + "轮到你"练习(social_choice / practice_trials);
- sequence 排顺序:把示范步骤排成正确顺序(steps,≥3 步);
- match    配一配:图案 ↔ 文字/情绪配对(steps 或 visual_cards,≥3 项)。
画面低刺激、柔和配色,反馈温和无惩罚,契合自闭症儿童视觉支持原则。
"""

from __future__ import annotations

import json
from pathlib import Path

_GAME_TYPES = ("pack", "story", "sequence", "match")

_TEMPLATE = r"""<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  :root{ --bg:#f5f1e9; --card:#fffdf8; --accent:#7fa098; --accent-d:#5f857b; --zh:#333a40; --en:#6c7674; --foot:#a8a49c; }
  *{ box-sizing:border-box; }
  html,body{ margin:0; height:100%; }
  body{ background:var(--bg); color:var(--zh); font-family:"Microsoft YaHei","PingFang SC","Segoe UI",sans-serif; display:flex; flex-direction:column; min-height:100vh; }
  .topbar{ height:8px; background:var(--accent); }
  .wrap{ flex:1; display:flex; align-items:center; justify-content:center; padding:24px; }
  .stage{ width:100%; max-width:840px; background:var(--card); border-radius:28px; box-shadow:0 10px 40px rgba(90,110,100,.12); padding:36px 30px; text-align:center; animation:fade .35s ease; }
  @keyframes fade{ from{opacity:0; transform:translateY(8px);} to{opacity:1; transform:none;} }
  .tag{ color:var(--accent-d); font-size:16px; letter-spacing:1px; margin-bottom:8px; }
  .tag2{ width:100%; color:var(--en); font-size:15px; margin:10px 0 2px; }
  .emoji{ font-size:92px; line-height:1.1; margin:6px 0 14px; }
  .zh{ font-size:29px; font-weight:700; line-height:1.5; margin:6px 0; }
  .en{ font-size:18px; color:var(--en); font-weight:400; line-height:1.4; margin:4px 0 6px; }
  .hint{ color:var(--accent-d); font-size:22px; margin-top:12px; }
  .msg{ color:var(--accent-d); font-size:19px; margin-top:12px; min-height:26px; }
  .btns{ margin-top:22px; display:flex; gap:14px; flex-wrap:wrap; justify-content:center; }
  .btns.menu{ flex-direction:column; align-items:center; }
  .btns.menu button{ min-width:260px; }
  button{ font-family:inherit; font-size:20px; padding:14px 26px; border:none; border-radius:16px; background:var(--accent); color:#fff; cursor:pointer; transition:background .2s, transform .1s; }
  button:hover{ background:var(--accent-d); }
  button:active{ transform:scale(.97); }
  button.ghost{ background:#e9e3d7; color:var(--zh); }
  button.ghost:hover{ background:#ddd5c6; }
  .opt{ display:flex; align-items:center; gap:12px; width:100%; max-width:560px; margin:12px auto; text-align:left; background:#eef3f0; color:var(--zh); font-size:22px; }
  .opt:hover{ background:#e2ebe6; }
  .opt .oi{ font-size:34px; }
  .reveal{ margin-top:18px; background:#f0f5f2; border-radius:18px; padding:16px 18px; }
  .row{ display:flex; flex-wrap:wrap; gap:12px; justify-content:center; margin:8px 0; min-height:64px; }
  .chip{ display:flex; align-items:center; gap:8px; background:#eef3f0; border-radius:16px; padding:10px 16px; font-size:19px; cursor:pointer; }
  .chip:hover{ background:#e2ebe6; }
  .chip.placed{ background:#eef7f2; }
  .chip .ci{ font-size:28px; }
  .seqbox{ display:flex; flex-direction:column; align-items:center; gap:4px; }
  .seqnum{ font-size:14px; color:var(--accent-d); }
  .grid2{ display:flex; gap:26px; justify-content:center; align-items:flex-start; margin-top:8px; }
  .col{ display:flex; flex-direction:column; gap:12px; }
  .mbtn{ min-width:130px; font-size:22px; background:#eef3f0; color:var(--zh); }
  .mbtn:hover{ background:#e2ebe6; }
  .mbtn.sel{ background:#cfe3d9; outline:3px solid var(--accent); }
  .mbtn.done{ background:#dff0e6; color:#9ab5a8; cursor:default; }
  .cards{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:14px; margin-top:12px; }
  .cardx{ background:#f0f5f2; border-radius:18px; padding:16px; }
  .cardx .emoji{ font-size:54px; margin:0 0 6px; }
  .cardx .zh{ font-size:19px; }
  .cardx .en{ font-size:14px; }
  .cardx .cap{ font-size:15px; color:var(--accent-d); margin-top:6px; }
  .foot{ text-align:center; color:var(--foot); font-size:13px; padding:12px; line-height:1.5; }
</style>
</head>
<body>
  <div class="topbar"></div>
  <div class="wrap"><div class="stage" id="stage"></div></div>
  <div class="foot">示范 · 需专业审核&nbsp;&nbsp;|&nbsp;&nbsp;Draft · needs professional review<br>本内容为辅助 / 教育工具,不替代专业评估、诊断或治疗。</div>
  <script type="application/json" id="mod">__MODULE_JSON__</script>
  <script>
  const M = JSON.parse(document.getElementById('mod').textContent);
  const START = "__GAME_TYPE__";
  const stage = document.getElementById('stage');
  const L = 'ABCD';
  function el(tag, cls, text){ const e=document.createElement(tag); if(cls) e.className=cls; if(text!=null) e.textContent=text; return e; }
  function btn(label, cls, on){ const b=el('button', cls||'', label); b.onclick=on; return b; }
  function clear(){ stage.innerHTML=''; }
  function add(){ for(const n of arguments) if(n) stage.appendChild(n); }
  function ctrl(){ const b=el('div','btns'); for(const x of arguments) if(x) b.appendChild(x); stage.appendChild(b); return b; }
  function shuffle(a){ a=a.slice(); for(let k=a.length-1;k>0;k--){ const j=Math.floor(Math.random()*(k+1)); const tmp=a[k]; a[k]=a[j]; a[j]=tmp; } return a; }

  const has = {
    story: !!(M.intro_zh || (M.steps&&M.steps.length) || M.social_choice),
    sequence: (M.steps||[]).length >= 3,
    match: (M.steps||[]).length >= 3 || (M.visual_cards||[]).length >= 3,
  };

  // ---------------- 首页:选一个小游戏 ----------------
  function home(){
    clear();
    add(el('div','tag','选一个小游戏 · Choose a game'),
        el('div','emoji',(M.steps&&M.steps[0]&&M.steps[0].icon)||'🎮'),
        el('div','zh',M.title_zh), el('div','en',M.title_en));
    const bs=el('div','btns menu');
    if(has.story) bs.appendChild(btn('📖 听故事 · Story','',story));
    if(has.sequence) bs.appendChild(btn('🔢 排顺序 · Put in order','',sequence));
    if(has.match) bs.appendChild(btn('🧩 配一配 · Match','',match));
    stage.appendChild(bs);
  }

  // ---------------- 玩法一:听故事(社交选择分支)----------------
  function story(){
    const scenes=[];
    if(M.intro_zh) scenes.push({t:'page', zh:M.intro_zh, en:M.intro_en, icon:(M.social_choice&&M.social_choice.icon)||'🌈'});
    (M.steps||[]).forEach((s,idx)=>scenes.push({t:'page', zh:s.text_zh, en:s.text_en, icon:s.icon, tag:'示范 '+(idx+1)+'/'+M.steps.length+' · Watch'}));
    (M.practice_trials||[]).forEach(tr=>scenes.push({t:'trial', tr}));
    if(M.social_choice) scenes.push({t:'choice', sc:M.social_choice});
    scenes.push({t:'review'});
    if((M.visual_cards||[]).length) scenes.push({t:'cards'});
    let si=0;
    function sgo(n){ si=Math.max(0,Math.min(scenes.length-1,n)); sdraw(); }
    function snext(){ sgo(si+1); }
    function sOutcome(o,k){
      clear();
      add(el('div','tag','选 '+L[k]+':'+o.label_zh), el('div','emoji',o.icon||'🙂'),
          el('div','zh',o.outcome_zh), o.outcome_en&&el('div','en',o.outcome_en));
      ctrl(btn('↩ 再试试别的','ghost',sdraw), btn('继续 ▶','',snext));
    }
    function sdraw(){
      clear(); const s=scenes[si];
      if(s.t==='page'){
        add(s.tag&&el('div','tag',s.tag), el('div','emoji',s.icon||'🧩'),
            el('div','zh',s.zh), s.en&&el('div','en',s.en));
        ctrl(btn('下一步 ▶','',snext));
      } else if(s.t==='trial'){
        const tr=s.tr;
        add(el('div','tag','练习 · 轮到你 Your turn'), el('div','emoji',tr.icon||'🌟'),
            el('div','zh',tr.prompt_zh), tr.prompt_en&&el('div','en',tr.prompt_en),
            el('div','hint','⏳ 轮到你,试试看'));
        const cb=ctrl(btn('我来试试 👉','',()=>{
          const r=el('div','reveal');
          r.appendChild(el('div','tag','可以这样说 · Like this'));
          r.appendChild(el('div','zh',tr.answer_zh));
          if(tr.answer_en) r.appendChild(el('div','en',tr.answer_en));
          r.appendChild(el('div','zh','🌟 '+(tr.reinforce_zh||'')));
          if(tr.reinforce_en) r.appendChild(el('div','en',tr.reinforce_en));
          stage.insertBefore(r, cb); cb.innerHTML=''; cb.appendChild(btn('继续 ▶','',snext));
        }));
      } else if(s.t==='choice'){
        const sc=s.sc;
        add(el('div','tag','想一想 · Choose'), el('div','emoji',sc.icon||'🤝'),
            el('div','zh',sc.scenario_zh), sc.scenario_en&&el('div','en',sc.scenario_en));
        (sc.options||[]).forEach((o,k)=>{
          const b=el('button','opt'); b.onclick=()=>sOutcome(o,k);
          b.appendChild(el('span','oi',o.icon||'🙂'));
          b.appendChild(el('span',null,L[k]+'. '+o.label_zh+(o.label_en?('  '+o.label_en):'')));
          stage.appendChild(b);
        });
      } else if(s.t==='review'){
        add(el('div','tag','今天的故事 · Today'), el('div','emoji','🌈'),
            el('div','zh',M.review_zh), M.review_en&&el('div','en',M.review_en),
            el('div','hint','🎉 完成!'));
        const bs=[];
        if((M.visual_cards||[]).length) bs.push(btn('看看小卡片 ▶','',snext));
        bs.push(btn('↺ 再玩一遍','ghost',()=>sgo(0)));
        bs.push(btn('← 选择别的','ghost',home));
        ctrl.apply(null, bs);
      } else if(s.t==='cards'){
        add(el('div','tag','小卡片 · Cards'));
        const g=el('div','cards');
        (M.visual_cards||[]).forEach(c=>{
          const cx=el('div','cardx');
          cx.appendChild(el('div','emoji',c.icon||'🧩'));
          cx.appendChild(el('div','zh',c.title_zh));
          if(c.title_en) cx.appendChild(el('div','en',c.title_en));
          if(c.caption_zh) cx.appendChild(el('div','cap',c.caption_zh));
          g.appendChild(cx);
        });
        add(g);
        ctrl(btn('↺ 再玩一遍','ghost',()=>sgo(0)), btn('← 选择别的','ghost',home));
      }
    }
    sdraw();
  }

  // ---------------- 玩法二:排顺序(把步骤排成正确顺序)----------------
  function sequence(){
    clear();
    const steps=(M.steps||[]).map((s,idx)=>({idx, icon:s.icon||'🔹', label:(s.text_zh||'')}));
    let pool=shuffle(steps); let placed=[];
    const placedRow=el('div','row'); const poolRow=el('div','row'); const msg=el('div','msg','');
    function chip(item, where){
      const c=el('div','chip'+(where==='placed'?' placed':''));
      c.appendChild(el('span','ci', item.icon));
      const t=item.label.length>12?item.label.slice(0,12)+'…':item.label;
      c.appendChild(el('span',null,t));
      c.onclick=()=>{
        if(where==='pool'){ pool=pool.filter(x=>x!==item); placed.push(item); }
        else { placed=placed.filter(x=>x!==item); pool.push(item); }
        msg.textContent=''; draw();
      };
      return c;
    }
    function win(){
      clear();
      add(el('div','emoji','🎉'), el('div','zh','顺序排对了!'), el('div','en','Correct order!'));
      ctrl(btn('↺ 再来一次','ghost',sequence), btn('← 选择别的','ghost',home));
    }
    function draw(){
      placedRow.innerHTML=''; poolRow.innerHTML='';
      placed.forEach((it,k)=>{ const box=el('div','seqbox'); box.appendChild(el('div','seqnum',(k+1)+'')); box.appendChild(chip(it,'placed')); placedRow.appendChild(box); });
      pool.forEach(it=>poolRow.appendChild(chip(it,'pool')));
      if(pool.length===0){
        if(placed.every((it,k)=>it.idx===k)) win();
        else msg.textContent='顺序还没对,点一下卡片可以拿回来重新排 🙂';
      }
    }
    add(el('div','tag','排顺序 · Put in order'), el('div','zh','按正确的顺序,点一点下面的步骤'),
        el('div','tag2','正确顺序 →'), placedRow, el('div','tag2','可选步骤'), poolRow, msg);
    ctrl(btn('🏠 返回选择','ghost',home));
    draw();
  }

  // ---------------- 玩法三:配一配(图案 ↔ 文字/情绪)----------------
  function match(){
    clear();
    const src=(M.steps&&M.steps.length>=3)
      ? M.steps.map(s=>({icon:s.icon,label:s.text_zh}))
      : (M.visual_cards||[]).map(c=>({icon:c.icon,label:c.title_zh}));
    const pairs=src.slice(0,6).map((p,idx)=>({id:idx, icon:p.icon||'🧩', label:p.label||''}));
    const g=el('div','grid2'); const left=el('div','col'); const right=el('div','col'); const msg=el('div','msg','');
    let sel=null; const done=new Set(); const lmap={};
    function win(){
      clear();
      add(el('div','emoji','🎉'), el('div','zh','全部配对成功!'), el('div','en','All matched!'));
      ctrl(btn('↺ 再来一次','ghost',match), btn('← 选择别的','ghost',home));
    }
    function pickL(id,b){ if(done.has(id))return; sel=id; for(const k in lmap) lmap[k].classList.toggle('sel', (+k)===id); msg.textContent=''; }
    function pickR(id,b){
      if(done.has(id))return;
      if(sel==null){ msg.textContent='先点左边一个图案'; return; }
      if(id===sel){ done.add(id); lmap[id].classList.remove('sel'); lmap[id].classList.add('done'); b.classList.add('done'); const s=sel; sel=null; msg.textContent='配对成功!'; if(done.size===pairs.length) win(); }
      else { msg.textContent='再看看,不是这个'; if(lmap[sel]) lmap[sel].classList.remove('sel'); sel=null; }
    }
    shuffle(pairs).forEach(p=>{ const b=el('button','mbtn'); b.textContent=p.icon; b.style.fontSize='40px'; b.onclick=()=>pickL(p.id,b); left.appendChild(b); lmap[p.id]=b; });
    shuffle(pairs).forEach(p=>{ const b=el('button','mbtn'); b.textContent=(p.label.length>10?p.label.slice(0,10)+'…':p.label); b.onclick=()=>pickR(p.id,b); right.appendChild(b); });
    g.appendChild(left); g.appendChild(right);
    add(el('div','tag','配一配 · Match'), el('div','zh','把图案和文字配到一起'), g, msg);
    ctrl(btn('🏠 返回选择','ghost',home));
  }

  // ---------------- 启动 ----------------
  (function(){
    const one={story:story, sequence:sequence, match:match};
    if(START!=='pack' && has[START] && one[START]) one[START]();
    else home();
  })();
  </script>
</body>
</html>
"""


def render_game(module, out_path, game_type: str = "pack") -> Path:
    """把一个训练模块渲染成自成一体的 HTML5 小游戏合辑文件。

    game_type: pack(首页选玩法,默认)| story | sequence | match(直接进入某一玩法)。
    """
    gt = game_type if game_type in _GAME_TYPES else "pack"
    data = json.dumps(module.model_dump(), ensure_ascii=False)
    data = data.replace("</", "<\\/")            # 防止 </script> 破坏内嵌 JSON(保险)
    html = (_TEMPLATE
            .replace("__TITLE__", module.title_zh)
            .replace("__GAME_TYPE__", gt)
            .replace("__MODULE_JSON__", data))
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    return out_path
