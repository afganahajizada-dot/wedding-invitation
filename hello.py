import base64
from pathlib import Path
from datetime import datetime
from email.message import EmailMessage
import smtplib

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

BRIDE = "Əfqanə"
GROOM = "Cavid"
WEDDING_DATE_TEXT = "19 Dekabr 2026"
VENUE = "Elux Event Hall"
WEDDING_DATETIME = "2026-12-19T19:00:00+04:00"

st.set_page_config(
    page_title="J & A Wedding Invitation",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "invitation_opened" not in st.session_state:
    st.session_state.invitation_opened = False

castle_path = Path(__file__).parent / "castle.png"
if not castle_path.exists():
    st.error("castle.png faylı hello.py ilə eyni qovluqda olmalıdır.")
    st.stop()

@st.cache_data(show_spinner=False)
def cached_image_b64(path_string: str) -> str:
    return base64.b64encode(Path(path_string).read_bytes()).decode("utf-8")

castle_b64 = cached_image_b64(str(castle_path))
reveal_path = Path(__file__).parent / "castle_reveal.jpg"
if not reveal_path.exists():
    st.error("castle_reveal.jpg faylı hello.py ilə eyni qovluqda olmalıdır.")
    st.stop()
reveal_b64 = cached_image_b64(str(reveal_path))

tuxedo_path = Path(__file__).parent / "tuxedo_reference.png"
tuxedo_b64 = cached_image_b64(str(tuxedo_path)) if tuxedo_path.exists() else ""
tuxedo_img_html = (
    f'<img class="tuxedo-silhouette" src="data:image/png;base64,{tuxedo_b64}" '
    'alt="Qara smoking, papyon və şalvar">'
    if tuxedo_b64 else
    '<div class="section-text">tuxedo_reference.png faylını hello.py ilə eyni qovluğa əlavə edin.</div>'
)

snowflakes = []
for i in range(34):
    left = (i * 37 + 11) % 100
    size = 10 + (i * 7 % 15)
    duration = 8 + (i * 5 % 11)
    delay = -((i * 3) % 17)
    drift = ((i * 13) % 61) - 30
    opacity = 0.35 + ((i * 17) % 55) / 100
    snowflakes.append(
        f'<span class="snowflake" style="left:{left}%;font-size:{size}px;'
        f'animation-duration:{duration}s;animation-delay:{delay}s;'
        f'--drift:{drift}px;opacity:{opacity:.2f}">❄</span>'
    )
snow_html = '<div class="snow-layer" aria-hidden="true">' + ''.join(snowflakes) + '</div>' 

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Great+Vibes&family=Montserrat:wght@300;400;500&display=swap');

    html, body, [data-testid="stAppViewContainer"] {{
        background: #081426 !important;
        color: #f2f3f6 !important;
    }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    [data-testid="stHeader"] {{ display:none; }}
    .block-container {{
        max-width: 100% !important;
        padding: 0 0 2rem 0 !important;
    }}
    .gate {{
        position: relative;
        width: 100vw;
        height: 100vh;
        min-height: 560px;
        margin-left: calc(50% - 50vw);
        overflow: hidden;
        perspective: 1800px;
        background: #081426;
    }}
    .door-panel {{
        position: absolute;
        top: 0;
        width: 50%;
        height: 100%;
        background-image: url("data:image/png;base64,{castle_b64}");
        background-repeat: no-repeat;
        background-size: 200% 100%;
        z-index: 2;
        backface-visibility: hidden;
    }}
    .door-left {{
        left: 0;
        background-position: left center;
        transform-origin: left center;
    }}
    .door-right {{
        right: 0;
        background-position: right center;
        transform-origin: right center;
    }}

    .snow-layer {{
        position:absolute; inset:0; z-index:4; overflow:hidden;
        pointer-events:none;
    }}
    .global-snow {{
        position:fixed; inset:0; z-index:9999; overflow:hidden;
        pointer-events:none;
    }}
    .global-snow .snowflake {{ position:absolute; top:-12%; color:#fff;
        text-shadow:0 0 7px rgba(255,255,255,.85);
        animation-name:snowFall; animation-timing-function:linear;
        animation-iteration-count:infinite; will-change:transform;
    }}
    .snowflake {{
        position:absolute; top:-12%; color:#fff;
        text-shadow:0 0 7px rgba(255,255,255,.8);
        animation-name:snowFall; animation-timing-function:linear;
        animation-iteration-count:infinite;
        will-change:transform;
    }}
    @keyframes snowFall {{
        0% {{ transform:translate3d(0,-5vh,0) rotate(0deg); }}
        100% {{ transform:translate3d(var(--drift),115vh,0) rotate(300deg); }}
    }}

    .gate-hint {{
        position: absolute;
        z-index: 5;
        bottom: 8%;
        left: 0;
        width: 100%;
        text-align: center;
        color: #d9e4ef;
        font: 10px Montserrat, sans-serif;
        letter-spacing: 3px;
        text-shadow: 0 2px 12px #000;
        pointer-events: none;
    }}
    .gate.opening .door-left {{ animation: openLeft 3.2s cubic-bezier(.72,0,.22,1) forwards; }}
    .gate.opening .door-right {{ animation: openRight 3.2s cubic-bezier(.72,0,.22,1) forwards; }}
    .gate.opening {{ animation: fadeGate 1s ease 3.1s forwards; }}
    @keyframes openLeft {{ to {{ transform: rotateY(-108deg); }} }}
    @keyframes openRight {{ to {{ transform: rotateY(108deg); }} }}
    @keyframes fadeGate {{ to {{ opacity:0; visibility:hidden; height:0; min-height:0; margin-bottom:0; }} }}

    /* Full-screen click target is only rendered before the invitation opens. */
    div[data-testid="stButton"]:has(button[kind="secondary"]) {{
        position: fixed;
        inset: 0;
        z-index: 20;
        margin: 0 !important;
        padding: 0 !important;
        display: flex;
        align-items: flex-end;
        justify-content: center;
        pointer-events: none;
    }}
    div[data-testid="stButton"]:has(button[kind="secondary"]) button {{
        pointer-events: auto;
        width: 100vw;
        height: 100vh;
        border: 0 !important;
        border-radius: 0 !important;
        background: transparent !important;
        color: transparent !important;
        box-shadow: none !important;
        cursor: pointer;
    }}
    div[data-testid="stButton"]:has(button[kind="secondary"]) button:hover {{
        border: 0 !important;
        background: transparent !important;
        color: transparent !important;
    }}
    .invitation-content {{
        opacity: 0;
        animation: revealInvite 1.7s ease 3.0s forwards;
    }}
    @keyframes revealInvite {{ to {{ opacity:1; }} }}

    .hero {{
        min-height: 720px;
        padding: 70px 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        position: relative;
        overflow: hidden;
        background:
          radial-gradient(ellipse at 50% 35%, rgba(151,185,216,.22), transparent 58%),
          linear-gradient(145deg, #081426, #173454 48%, #0b1426 100%);
    }}
    .hero:before {{
        content:""; position:absolute; inset:18px;
        border:1px solid rgba(220,190,125,.88); pointer-events:none;
    }}
    .eyebrow {{
        font: 11px Montserrat,sans-serif; letter-spacing:4px;
        line-height:2; color:#d9e4ef;
    }}
    .names {{
        display:flex; flex-direction:column; align-items:center; gap:0;
        font: clamp(58px,9vw,104px) 'Great Vibes',cursive;
        line-height:1.08; color:#f1e5ca; margin:28px 0 20px;
        text-shadow:0 0 25px rgba(230,201,150,.25);
    }}
    .name-groom, .name-bride {{
        display:block; width:0; overflow:hidden; white-space:nowrap;
        border-right:2px solid #d7bd8d; opacity:0;
        padding-right:5px; line-height:1.2;
    }}
    .name-groom {{ animation: typeGroom 1.35s steps(5,end) .35s forwards, cursorBlink .7s step-end 2.0s 4; }}
    .name-bride {{ animation: typeBride 1.45s steps(6,end) 2.65s forwards, cursorBlink .7s step-end 4.2s 4; }}
    .amp {{
        font: .48em 'Cormorant Garamond',serif; color:#fff;
        display:block; opacity:0; margin:1px 0 5px;
        animation: ampEnter .7s ease 2.05s forwards;
    }}
    @keyframes typeGroom {{ 0% {{width:0;opacity:1;}} 100% {{width:5.2ch;opacity:1;}} }}
    @keyframes typeBride {{ 0% {{width:0;opacity:1;}} 100% {{width:6.1ch;opacity:1;}} }}
    @keyframes cursorBlink {{ 50% {{border-color:transparent;}} }}
    @keyframes ampEnter {{ from {{opacity:0;transform:scale(.4);}} to {{opacity:1;transform:scale(1);}} }}
    .tuxedo-silhouette {{ width:170px; height:auto; max-height:390px; object-fit:contain; display:block; margin:18px auto 0; filter:drop-shadow(0 8px 12px rgba(0,0,0,.28)); }}
    .gold-line {{ width:85px; height:1px; background:#c6b58f; margin:26px auto; }}
    .date {{
        font-size:clamp(22px,4vw,30px); letter-spacing:5px;
        color:#fff4e3; margin-top:18px;
    }}
    .section {{
        text-align:center; padding:78px 22px;
        background:#10233d; border-top:1px solid rgba(190,205,220,.20);
    }}
    .section.alt {{ background:#0a172b; }}
    .section-title {{
        font:clamp(42px,7vw,58px) 'Great Vibes',cursive;
        color:#d7bd8d; margin-bottom:12px;
    }}
    .section-text {{
        max-width:680px; margin:18px auto; font-size:23px;
        line-height:1.65; color:#e4e9f0;
    }}
    .detail-card {{
        max-width:480px; margin:18px auto; padding:28px 18px;
        border:1px solid #b8c7d8; background:rgba(195,215,235,.045);
    }}
    .detail-label {{
        font:10px Montserrat,sans-serif; letter-spacing:4px; color:#d7bd8d;
    }}
    .detail-value {{ font-size:30px; margin-top:12px; color:#fff4e3; }}
    .map-preview {{
        width:min(720px,100%); margin:28px auto 0;
        border:1px solid #c6b58f; padding:5px; background:#10233d; line-height:0;
    }}
    .map-preview iframe {{ display:block; width:100%; height:280px; border:0; }}
    .countdown {{
        display:flex; justify-content:center; flex-wrap:wrap;
        gap:18px; margin-top:30px;
    }}
    .time-box {{ min-width:105px; padding:18px 12px; border:1px solid rgba(190,205,220,.85); }}
    .time-number {{ font-size:42px; color:#f1e5ca; }}
    .time-label {{ font:9px Montserrat,sans-serif; letter-spacing:2px; color:#d7bd8d; }}
    .dress-grid {{
        display:grid; grid-template-columns:repeat(2,minmax(0,1fr));
        gap:22px; max-width:800px; margin:32px auto 0;
    }}
    .dress-card {{
        border:1px solid #c6b58f; padding:26px 18px;
        background:rgba(255,255,255,.035);
    }}
    .dress-heading {{
        color:#d7bd8d; font:12px Montserrat,sans-serif;
        letter-spacing:3px; margin-bottom:15px;
    }}
    .dress-main {{ font-size:29px; color:#fff4e3; }}
    .palette {{
        display:flex; justify-content:center; flex-wrap:wrap;
        gap:12px; margin:22px auto 8px;
    }}
    .swatch {{
        width:43px; height:43px; border-radius:50%;
        border:2px solid rgba(255,255,255,.72);
        box-shadow:0 2px 9px rgba(0,0,0,.3);
    }}
    .footer {{
        text-align:center; padding:55px 20px; color:#e2e8f0;
        background:#071225; font-size:21px;
    }}
    .footer-script {{ font:48px 'Great Vibes',cursive; color:#d7bd8d; }}

    [data-testid="stForm"] {{
        max-width:650px; margin:0 auto 3rem auto; padding:28px;
        background:#10233d; border:1px solid #b8c7d8; border-radius:4px;
    }}
    [data-testid="stForm"] label {{ color:#f5f0e7 !important; }}
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {{
        background:#f8f5ef; color:#142541;
    }}
    [data-testid="stFormSubmitButton"] button {{
        background:#d7bd8d; color:#101b30; border:1px solid #e4d6bb;
        border-radius:2px; letter-spacing:1.5px; font-weight:600; min-height:46px;
    }}
    @media(max-width:600px) {{
        .hero {{ min-height:660px; padding:55px 16px; }}
        .section {{ padding:60px 17px; }}
        .section-text {{ font-size:20px; }}
        .time-box {{ min-width:72px; padding:13px 7px; }}
        .time-number {{ font-size:32px; }}
        .dress-grid {{ grid-template-columns:1fr; max-width:420px; }}
        .gate-hint {{ font-size:8px; letter-spacing:2px; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

if not st.session_state.invitation_opened:
    st.markdown(
        f"""
        <div class="gate">
          <div class="door-panel door-left"></div>
          <div class="door-panel door-right"></div>
          {snow_html}
          <div class="gate-hint">✧ DƏVƏTNAMƏNİ AÇMAQ ÜÇÜN EKRANIN İSTƏNİLƏN YERİNƏ TOXUNUN ✧</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Dəvətnaməni aç", key="open_invitation", type="secondary"):
        st.session_state.invitation_opened = True
    st.stop()

# Keep snowfall visible over the entire invitation after the doors open.
st.markdown(
    '<div class="global-snow" aria-hidden="true">' + ''.join(snowflakes) + '</div>',
    unsafe_allow_html=True,
)

# After the guest taps the closed doors, play the full cinematic reveal.
components.html(
    f"""
    <!doctype html>
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Montserrat:wght@300;400;500&display=swap');
        * {{ box-sizing:border-box; }}
        html,body {{ margin:0; width:100%; height:100%; overflow:hidden; background:#071225; }}
        .scene {{ position:relative; width:100%; height:760px; min-height:620px; overflow:hidden; background:#071225; }}
        .castle-bg {{
          position:absolute; inset:0; width:100%; height:100%; object-fit:cover;
          opacity:0; transform:translateY(-25%) scale(1.12);
          filter:saturate(1.12);
          object-position:center 50%;
          animation: castleReveal 7.2s cubic-bezier(.18,.68,.22,1) 3.25s forwards;
          will-change:transform,opacity;
        }}
        /* The full castle image glides DOWN from above; no top crop is needed. */
        @keyframes castleReveal {{
          0% {{ opacity:0; transform:translateY(-25%) scale(1.12); }}
          18% {{ opacity:1; }}
          100% {{ opacity:1; transform:translateY(0%) scale(1.12); }}
        }}
        .door {{
          position:absolute; top:0; height:100%; width:50%; z-index:4;
          background-image:url("data:image/png;base64,{castle_b64}");
          background-repeat:no-repeat; background-size:200% 100%;
          backface-visibility:hidden; border:0;
        }}
        .left {{ left:0; background-position:left center; transform-origin:left center;
          animation: doorLeft 2.5s cubic-bezier(.72,0,.22,1) .25s forwards; }}
        .right {{ right:0; background-position:right center; transform-origin:right center;
          animation: doorRight 2.5s cubic-bezier(.72,0,.22,1) .25s forwards; }}
        @keyframes doorLeft {{ to {{ transform:perspective(1400px) rotateY(-112deg); opacity:.12; }} }}
        @keyframes doorRight {{ to {{ transform:perspective(1400px) rotateY(112deg); opacity:.12; }} }}
        .top-shade {{
          position:absolute; z-index:1; inset:0 0 auto; height:39%;
          background:linear-gradient(180deg,#061329 0%,#081a34 100%);
          opacity:0; animation:shadeIn 1.1s ease 4.35s forwards;
        }}
        @keyframes shadeIn {{ to {{ opacity:1; }} }}
        #fireworks {{ position:absolute; inset:0; width:100%; height:100%; z-index:2; pointer-events:none; }}
        .snow {{
          position:absolute; inset:0; z-index:3; pointer-events:none;
          background-image:
            radial-gradient(2px 2px at 10% 20%,rgba(255,255,255,.85) 50%,transparent 60%),
            radial-gradient(2px 2px at 35% 65%,rgba(255,255,255,.75) 50%,transparent 60%),
            radial-gradient(3px 3px at 78% 30%,rgba(255,255,255,.7) 50%,transparent 60%),
            radial-gradient(2px 2px at 90% 80%,rgba(255,255,255,.7) 50%,transparent 60%);
          background-size:190px 210px,240px 260px,280px 230px,220px 250px;
          animation:snowMove 8s linear infinite;
        }}
        @keyframes snowMove {{ to {{ background-position:40px 210px,-60px 260px,30px 230px,-45px 250px; }} }}
        .titles {{
          position:absolute; z-index:5; top:4%; left:4%; width:92%; text-align:center;
          color:#f5e5c5; opacity:0; text-shadow:0 2px 18px rgba(0,0,0,.85);
          animation:titleAppear 1.15s ease 5.05s forwards;
        }}
        @keyframes titleAppear {{ to {{ opacity:1; }} }}
        .ornament {{ color:#d8b875; font:25px Georgia,serif; letter-spacing:8px; }}
        .wedding-day {{
          margin-top:3px; font:600 clamp(17px,3vw,25px) Montserrat,Arial,sans-serif;
          letter-spacing:8px; color:#fff1d3; opacity:0;
          animation:fadeText 1s ease 5.35s forwards;
        }}
        .couple {{
          margin:8px auto 3px; min-height:52px;
          font:600 clamp(23px,4.5vw,38px) Montserrat,Arial,sans-serif;
          letter-spacing:4px; text-transform:uppercase;
          color:#f5d99e; line-height:1.2; white-space:nowrap;
        }}
        .typed {{ display:inline; }}
        .cursor {{ display:inline-block; width:2px; height:.8em; background:#e5c37e; margin-left:4px; animation:blink .7s step-end infinite; }}
        @keyframes blink {{ 50% {{ opacity:0; }} }}
        .date {{
          margin-top:5px; font:600 clamp(12px,2vw,16px) Montserrat,Arial,sans-serif;
          letter-spacing:7px; color:#fff1d3; opacity:0;
          animation:fadeText 1s ease 7.2s forwards;
        }}
        .divider {{ width:130px; height:1px; margin:9px auto 0; background:#d8b875; opacity:0; animation:fadeText 1s ease 6.8s forwards; }}
        @keyframes fadeText {{ to {{ opacity:1; }} }}
        @media(max-width:600px) {{
          .scene {{ height:680px; min-height:600px; }}
          .titles {{ top:4%; }}
          .top-shade {{ height:42%; }}
          .wedding-day {{ font-size:15px; letter-spacing:5px; }}
          .couple {{ font-size:clamp(20px,5vw,30px); letter-spacing:2px; }}
          .date {{ font-size:11px; letter-spacing:4px; }}
        }}
      </style>
    </head>
    <body>
      <div class="scene">
        <img class="castle-bg" src="data:image/jpeg;base64,{reveal_b64}" alt="Qarlı nağıl qalası">
        <div class="top-shade"></div>
        <canvas id="fireworks"></canvas>
        <div class="snow"></div>
        <div class="door left"></div>
        <div class="door right"></div>
        <div class="titles">
          <div class="ornament">✧ ❦ ✧</div>
          <div class="wedding-day">WEDDING DAY</div>
          <div class="couple"><span class="typed" id="typed"></span></div>
          <div class="divider"></div>
          <div class="date">19 DEKABR 2026</div>
        </div>
      </div>
      <script>
        const canvas = document.getElementById('fireworks');
        const ctx = canvas.getContext('2d');
        let W=0,H=0, rockets=[], particles=[];
        function resize(){{W=canvas.width=canvas.clientWidth;H=canvas.height=canvas.clientHeight;}}
        window.addEventListener('resize',resize); resize();

        function explode(x,y,hue) {{
          const count=115;
          for(let i=0;i<count;i++) {{
            const angle=(Math.PI*2*i/count)+(Math.random()*.08);
            const speed=1.1+Math.random()*4.4;
            particles.push({{x:x,y:y,vx:Math.cos(angle)*speed,vy:Math.sin(angle)*speed,
              life:65+Math.random()*35,max:100,hue:hue,light:62+Math.random()*22,
              size:1.2+Math.random()*2.2,drag:.986}});
          }}
          // A second, finer golden ring gives the burst a full sparkling-firework look.
          for(let i=0;i<42;i++) {{
            const angle=(Math.PI*2*i/42);
            const speed=2.3+Math.random()*1.4;
            particles.push({{x:x,y:y,vx:Math.cos(angle)*speed,vy:Math.sin(angle)*speed,
              life:85,max:85,hue:43,light:83,size:1.1+Math.random()*1.3,drag:.992}});
          }}
        }}

        function launchRocket() {{
          const x=W*(.14+Math.random()*.72);
          const targetY=H*(.16+Math.random()*.30);
          const hue=35+Math.random()*18;
          rockets.push({{x:x,y:H+8,vx:(Math.random()-.5)*1.1,
            vy:-(5.4+Math.random()*2.2),targetY:targetY,hue:hue,trail:[]}});
        }}

        let lastLaunch=-1400;
        function animate(t) {{
          ctx.clearRect(0,0,W,H);
          if(t-lastLaunch>720) {{ launchRocket(); lastLaunch=t; }}

          rockets=rockets.filter(r=>r.y>r.targetY);
          for(const r of rockets) {{
            r.trail.push({{x:r.x,y:r.y}});
            if(r.trail.length>13) r.trail.shift();
            r.x+=r.vx; r.y+=r.vy; r.vy*=.994;
            for(let j=0;j<r.trail.length;j++) {{
              const pt=r.trail[j];
              ctx.globalAlpha=(j/r.trail.length)*.85;
              ctx.fillStyle='#ffe5a6'; ctx.shadowBlur=14; ctx.shadowColor='#ffbd55';
              ctx.beginPath(); ctx.arc(pt.x,pt.y,1.5+(j/r.trail.length),0,Math.PI*2); ctx.fill();
            }}
            ctx.globalAlpha=1;
            if(r.y<=r.targetY) explode(r.x,r.y,r.hue);
          }}

          particles=particles.filter(p=>p.life>0);
          for(const p of particles) {{
            p.x+=p.vx; p.y+=p.vy; p.vy+=.022;
            p.vx*=p.drag; p.vy*=p.drag; p.life--;
            ctx.globalAlpha=Math.max(0,p.life/p.max);
            ctx.fillStyle='hsl('+p.hue+',98%,'+p.light+'%)';
            ctx.shadowBlur=16; ctx.shadowColor='#ffd27a';
            ctx.beginPath(); ctx.arc(p.x,p.y,p.size,0,Math.PI*2); ctx.fill();
          }}
          ctx.globalAlpha=1; ctx.shadowBlur=0;
          requestAnimationFrame(animate);
        }}
        requestAnimationFrame(animate);
        const text='Cavid & Əfqanə';
        const target=document.getElementById('typed');
        let i=0;
        setTimeout(function type(){{if(i<text.length){{target.textContent+=text.charAt(i).toUpperCase();i++;setTimeout(type,170);}}}},5900);
      </script>
    </body>
    </html>
    """,
    height=760,
    scrolling=False,
)


# Optional romantic Azerbaijani instrumental music.
# Add a legally obtained file named wedding_music.mp3 beside hello.py to show the player.
music_path = Path(__file__).parent / "wedding_music.mp3"
if music_path.exists():
    st.markdown(
        '<div style="text-align:center;color:#d7bd8d;letter-spacing:3px;'
        'font-size:12px;margin:10px 0 4px;">♫ MUSİQİ</div>',
        unsafe_allow_html=True,
    )
    st.audio(str(music_path), format="audio/mp3")


st.markdown(
    f"""
    <section class="section">
      <div class="section-title">Əziz qonaqlarımız...</div>
      <div class="gold-line"></div>
      <div class="section-text">
        Həyatımızın ən gözəl başlanğıcını sizinlə birlikdə qeyd etmək istəyirik.
        Sevincimizi, xoşbəxtliyimizi və sevgimizi bölüşəcəyimiz bu özəl gündə
        sizi aramızda görməkdən məmnun olarıq.
        <br><br>Bu sehrli günümüzdə bizimlə olun!
      </div>
      <div style="color:#d7bd8d;font-size:27px;">✧ ❦ ✧</div>
    </section>

""",
    unsafe_allow_html=True,
)


components.html(
    """
    <section style="background:#10233d;color:#f2f3f6;text-align:center;padding:45px 12px;font-family:Montserrat,Arial,sans-serif;">
      <div style="font-family:Georgia,serif;font-size:30px;color:#d7bd8d;margin-bottom:20px;">Böyük günə qalan vaxt</div>
      <div style="width:85px;height:1px;background:#c6b58f;margin:0 auto 28px;"></div>
      <div style="display:flex;justify-content:center;gap:14px;flex-wrap:wrap;">
        <div class="time-box" style="border-radius:10px;"><div class="time-number" id="days">00</div><div class="time-label">GÜN</div></div>
        <div class="time-box" style="border-radius:10px;"><div class="time-number" id="hours">00</div><div class="time-label">SAAT</div></div>
        <div class="time-box" style="border-radius:10px;"><div class="time-number" id="minutes">00</div><div class="time-label">DƏQİQƏ</div></div>
        <div class="time-box" style="border-radius:10px;"><div class="time-number" id="seconds">00</div><div class="time-label">SANİYƏ</div></div>
      </div>
    </section>
    <style>.time-box{min-width:90px;padding:17px 12px;border:1px solid rgba(190,205,220,.85)}.time-number{font-size:42px;color:#f1e5ca}.time-label{font-size:9px;letter-spacing:2px;color:#d7bd8d}</style>
    <script>
      const target = new Date("2026-12-19T19:00:00+04:00").getTime();
      function updateCountdown() {
        const diff = Math.max(0, target - Date.now());
        const values = {days:Math.floor(diff/86400000),hours:Math.floor(diff/3600000)%24,minutes:Math.floor(diff/60000)%60,seconds:Math.floor(diff/1000)%60};
        Object.entries(values).forEach(([id,value]) => {document.getElementById(id).textContent=String(value).padStart(2,"0");});
      }
      updateCountdown(); setInterval(updateCountdown,1000);
    </script>
    """,
    height=285,
    scrolling=False,
)

st.markdown(
    f"""

    <section class="section">
      <div class="section-title">Bu özəl günün detalları</div>
      <div class="gold-line"></div>
      <div class="detail-card">
        <div class="detail-label">MƏKAN</div>
        <div class="detail-value">{VENUE}</div>
      </div>
      <div class="map-preview">
        <iframe title="Elux Event Hall xəritəsi"
          src="https://www.google.com/maps?q=Elux%20Event%20Hall%20Baku&output=embed"
          loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
    </section>

    <section class="section alt">
      <div class="section-title">Dress Code</div>
      <div class="gold-line"></div>
      <div class="section-text">
        Qış gecəmizin zərif və eleqant ab-havasına uyğun geyim seçiminizi
        etməyinizi xahiş edirik.
      </div>
      <div class="dress-grid">
        <div class="dress-card">
          <div class="dress-heading">BƏYLƏR ÜÇÜN</div>
          {tuxedo_img_html}
          <div class="section-text" style="font-size:16px;margin:8px auto 0;">
            Klassik qara smoking və papyon.
          </div>
        </div>
        <div class="dress-card">
          <div class="dress-heading">XANIMLAR ÜÇÜN</div>
          <div class="palette">
            <span class="swatch" style="background:#741f32" title="Bordo"></span>
            <span class="swatch" style="background:#102b50" title="Tünd göy"></span>
            <span class="swatch" style="background:#5f89b0" title="Buz mavisi"></span>
            <span class="swatch" style="background:#9b315d" title="Moruq rəngi"></span>
            <span class="swatch" style="background:#654078" title="Bənövşəyi"></span>
            <span class="swatch" style="background:#7da6c9" title="Buz mavisi"></span>
            <span class="swatch" style="background:#050505" title="Qara"></span>
          </div>
          <div class="section-text" style="font-size:15px;margin:10px auto 0;">
            Zərif, uzun axşam libasları.
          </div>
        </div>
      </div>
    </section>

    <footer class="footer">
      <div class="footer-script">Sevgi ilə...</div>
      <div>Bir ömür, bir sevgi, bir hekayə.</div>
      <div style="font-family:Montserrat,sans-serif;font-size:11px;letter-spacing:3px;margin-top:22px;">19.12.2026</div>
      <div style="margin-top:20px;color:#d7bd8d;">✧ ♡ ✧</div>
    </footer>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="text-align:center;padding:65px 15px 20px;color:#d7bd8d;">
      <div style="font-family:Georgia,serif;font-size:clamp(34px,5vw,48px);">
        İştirakınızı təsdiqləyin
      </div>
      <div style="color:#fff4e3;font-size:18px;margin-top:12px;">
        19 dekabr 2026-cı il tarixində bizimlə olacağınızı bildirməyinizi xahiş edirik.
      </div>
      <div style="width:75px;height:1px;background:#c6b58f;margin:25px auto;"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("wedding_rsvp_form", clear_on_submit=True):
    guest_name = st.text_input("Adınız və soyadınız")
    attendance = st.selectbox(
        "İştirakınız",
        ["Bəli, iştirak edəcəyəm", "Xeyr, təəssüf ki, iştirak edə bilməyəcəyəm"],
    )
    guest_count = st.selectbox(
        "Neçə nəfər iştirak edəcəksiniz?",
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    )
    submitted = st.form_submit_button("CAVABI GÖNDƏR", use_container_width=True)

if submitted:
    if not guest_name.strip():
        st.warning("Zəhmət olmasa, adınızı və soyadınızı qeyd edin.")
    else:
        submitted_at = datetime.now().astimezone().strftime("%d.%m.%Y, %H:%M")
        subject = "J & A Wedding Invitation | RSVP"

        response = pd.DataFrame([{
            "Ad və soyad": guest_name.strip(),
            "İştirak": attendance,
            "Qonaq sayı": guest_count,
            "Tarix": submitted_at,
        }])
        csv_path = Path(__file__).parent / "wedding_rsvp.csv"
        if csv_path.exists():
            response.to_csv(
                csv_path, mode="a", header=False, index=False, encoding="utf-8-sig"
            )
        else:
            response.to_csv(csv_path, index=False, encoding="utf-8-sig")

        try:
            sender_email = st.secrets["gmail"]["sender_email"]
            app_password = st.secrets["gmail"]["app_password"]
            recipient_email = st.secrets["gmail"]["recipient_email"]

            message = EmailMessage()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.set_content(
                "Yeni toy dəvətnaməsi cavabı gəldi.\n\n"
                f"Ad və soyad: {guest_name.strip()}\n"
                f"İştirak: {attendance}\n"
                f"Qonaq sayı: {guest_count}\n"
                f"Göndərilmə vaxtı: {submitted_at}\n"
            )
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=20) as smtp:
                smtp.login(sender_email, app_password.replace(" ", ""))
                smtp.send_message(message)
            st.success("Cavabınız uğurla göndərildi. Təşəkkür edirik! ❤️")
        except KeyError:
            st.warning(
                "Cavabınız wedding_rsvp.csv faylında saxlanıldı. Email üçün "
                ".streamlit/secrets.toml ayarlarını tamamlamaq lazımdır."
            )
        except Exception as error:
            st.warning(
                "Cavabınız wedding_rsvp.csv faylında saxlanıldı, lakin email göndərilmədi. "
                "Gmail ayarlarını yoxlamaq lazımdır."
            )
            st.caption(f"Texniki məlumat: {error}")
