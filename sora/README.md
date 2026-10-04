# Sora Video Generation API

Sora AI video generation service with text and image input.

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-AI%20API-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

![Sora Video Generation](https://cdn.acedata.cloud/820jy0.jpg)

API home page: [Ace Data Cloud - Sora Video Generation](https://platform.acedata.cloud/service/sora)

Keywords: sora-api, ai-video, video-generation, openai-sora, rest-api, ai-api, aivideo, AI API, REST API, Developer API, Ace Data Cloud

## Why Use Sora Video Generation on Ace Data Cloud

- Unified developer platform with one API key, billing system, and usage tracking
- Production-ready AI API endpoints served from [https://api.acedata.cloud](https://api.acedata.cloud)
- English integration guides, API references, and service documentation
- Global-ready workflow for developers building chat, image, video, music, and search products

## Overview

<style>
.sora-page * { box-sizing: border-box; }
.sora-page h1, .sora-page h2, .sora-page h3, .sora-page h4, .sora-page h5, .sora-page h6, .sora-page p, .sora-page ul, .sora-page ol, .sora-page li, .sora-page pre, .sora-page blockquote, .sora-page table, .sora-page td, .sora-page th { margin: 0; padding: 0; }
.sora-page {
-webkit-font-smoothing: antialiased;
-moz-osx-font-smoothing: grayscale;
color: var(--el-text-color-primary);
background: var(--el-bg-color);
line-height: 1.6;
}
.sora-page a { text-decoration: none; color: inherit; }
.sora-page a:hover { text-decoration: none; }
.sora-page ul { list-style: none; }
.markdown-body .sora-page a { color: inherit !important; text-decoration: none !important; }
.markdown-body .sora-page a:hover { text-decoration: none !important; }
.markdown-body .sora-page a.s-btn-primary,
.markdown-body .sora-page a.price-btn-fill,
.markdown-body .sora-page a.btn-cta-light { color: #ffffff !important; }
.markdown-body .sora-page a.s-btn-secondary { color: var(--el-text-color-primary) !important; }
.markdown-body .sora-page a.price-btn-out { color: var(--el-text-color-primary) !important; }
.markdown-body .sora-page a.btn-cta-ghost { color: #94a3b8 !important; }
.markdown-body .sora-page a.btn-cta-ghost:hover { color: #e2e8f0 !important; }
.markdown-body .sora-page h1, .markdown-body .sora-page h2 { border-bottom: none !important; padding-bottom: 0 !important; }
.s-container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.s-container-narrow { max-width: 800px; margin: 0 auto; padding: 0 24px; }
.s-container-wide { max-width: 1100px; margin: 0 auto; padding: 0 32px; }
.s-section { padding: 80px 0; }
.s-section-lg { padding: 100px 0; }
.s-section-sm { padding: 48px 0; }
.s-bg-white { background: var(--el-bg-color); }
.s-bg-gray { background: var(--el-bg-color-page); }
.s-bg-dark { background: #0f172a; color: #f8fafc; }
.s-header { text-align: center; margin-bottom: 64px; }
.s-header h2 {
font-size: clamp(28px, 4vw, 40px);
font-weight: 700;
color: var(--el-text-color-primary);
letter-spacing: normal;
margin-bottom: 20px;
line-height: 1.15;
}
.s-header p {
font-size: clamp(16px, 2vw, 18px);
color: var(--el-text-color-regular);
max-width: 640px;
margin: 0 auto;
line-height: 1.6;
}
.s-bg-dark .s-header h2 { color: #f8fafc; }
.s-bg-dark .s-header p { color: var(--el-text-color-secondary); }
.sora-page .s-btn-primary {
display: inline-flex; align-items: center; gap: 6px;
padding: 14px 28px;
background: #277186; color: #ffffff !important;
border-radius: 9999px; font-size: 15px; font-weight: 600;
transition: background 0.2s, transform 0.15s;
border: none; cursor: pointer;
text-decoration: none !important;
}
.sora-page .s-btn-primary:hover { background: #1f5a6b; transform: translateY(-1px); text-decoration: none !important; }
.sora-page .s-btn-secondary {
display: inline-flex; align-items: center; gap: 6px;
padding: 14px 28px;
background: var(--el-bg-color); color: var(--el-text-color-primary) !important;
border: 1px solid var(--el-border-color-light);
border-radius: 9999px; font-size: 15px; font-weight: 600;
transition: border-color 0.2s, background 0.2s;
cursor: pointer;
text-decoration: none !important;
}
.sora-page .s-btn-secondary:hover { background: var(--el-bg-color-page); text-decoration: none !important; }
.sora-hero {
padding: 100px 0 80px;
text-align: center;
background: var(--el-bg-color);
position: relative;
overflow: hidden;
}
.sora-hero::before {
content: '';
position: absolute;
top: -200px; left: 50%;
transform: translateX(-50%);
width: 900px; height: 500px;
background: radial-gradient(ellipse, rgba(39, 113, 134, 0.06) 0%, transparent 70%);
pointer-events: none;
}
.hero-badge {
display: inline-flex; align-items: center; gap: 8px;
padding: 6px 16px;
background: var(--el-bg-color-page); border: 1px solid var(--el-border-color-light);
border-radius: 9999px; font-size: 13px; font-weight: 600; color: var(--el-text-color-regular);
margin-bottom: 28px;
}
.hero-badge .badge-dot {
width: 6px; height: 6px; background: #10b981; border-radius: 50%;
display: inline-block;
}
.sora-hero h1 {
font-size: clamp(36px, 5vw, 60px);
font-weight: 700; line-height: 1.05;
letter-spacing: normal; color: var(--el-text-color-primary);
margin-bottom: 20px;
position: relative;
}
.sora-hero h1 span { color: #277186; }
.sora-page .hero-subtitle {
font-size: clamp(16px, 2vw, 20px);
color: var(--el-text-color-regular); line-height: 1.6;
max-width: 620px; margin: 0 auto 56px;
position: relative;
}
.hero-actions {
display: flex; gap: 12px; justify-content: center;
flex-wrap: wrap; margin-bottom: 56px; position: relative;
}
.hero-highlights {
display: flex; align-items: center; justify-content: center;
gap: 16px; flex-wrap: wrap; position: relative;
}
.hero-highlights .h-item { font-size: 14px; color: var(--el-text-color-regular); font-weight: 500; }
.hero-highlights .h-div { width: 1px; height: 16px; background: var(--el-border-color-light); }
@media (max-width: 640px) {
.hero-highlights .h-div { display: none; }
.hero-highlights { gap: 8px 16px; }
.hero-actions { flex-direction: column; align-items: center; }
.hero-actions a { width: 100%; max-width: 280px; justify-content: center; }
}
.sora-stats {
padding: 48px 0;
background: var(--el-bg-color-page);
border-top: 1px solid var(--el-border-color-lighter);
border-bottom: 1px solid var(--el-border-color-lighter);
}
.stats-grid {
display: grid; grid-template-columns: repeat(4, 1fr);
gap: 32px; text-align: center;
}
.stat-icon { font-size: 28px; margin-bottom: 12px; }
.stat-val {
font-size: clamp(28px, 4vw, 40px);
font-weight: 700; color: var(--el-text-color-primary);
letter-spacing: normal; margin-bottom: 4px;
}
.stat-lbl { font-size: 14px; color: var(--el-text-color-secondary); font-weight: 500; }
@media (max-width: 768px) { .stats-grid { grid-template-columns: repeat(2, 1fr); gap: 24px; } } @media (max-width: 480px) { .stats-grid { grid-template-columns: 1fr; gap: 20px; } }
.features-grid {
display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px;
}
.feat-card {
padding: 32px 28px;
border: none; border-radius: 20px; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.08);
background: var(--el-bg-color);
transition: border-color 0.2s, box-shadow 0.2s, transform 0.15s;
}
.feat-card:hover { box-shadow: 0 8px 24px 0 rgba(0,0,0,0.12);
transform: translateY(-2px);
}
.feat-icon { font-size: 32px; margin-bottom: 16px; }
.feat-card h3 { font-size: 18px; font-weight: 700; color: var(--el-text-color-primary); margin-bottom: 8px; }
.feat-card p { font-size: 15px; color: var(--el-text-color-regular); line-height: 1.6; }
@media (max-width: 1024px) { .features-grid { grid-template-columns: repeat(2, 1fr); } } @media (max-width: 640px) { .features-grid { grid-template-columns: 1fr; } } .code-split {
display: flex; gap: 48px; align-items: center;
}
.code-left { flex: 1; min-width: 0; }
.code-right { flex: 1; }
.code-wrap {
border-radius: 16px !important; overflow: hidden !important;
border: 1px solid #334155 !important; background: #0f172a !important;
}
.markdown-body .sora-page .code-wrap {
border-radius: 16px !important; overflow: hidden !important;
border: 1px solid #334155 !important; background: #0f172a !important;
}
.code-bar {
display: flex !important; align-items: center !important; justify-content: space-between !important;
padding: 12px 20px !important; background: #1e293b !important;
border-bottom: 1px solid #334155 !important;
}
.code-dots { display: flex; gap: 6px; }
.code-dots i {
width: 10px; height: 10px; border-radius: 50%;
display: inline-block;
}
.code-dots .r { background: #ef4444; }
.code-dots .y { background: #f59e0b; }
.code-dots .g { background: #10b981; }
.code-lang {
font-size: 12px; color: var(--el-text-color-secondary); font-weight: 600;
text-transform: uppercase; letter-spacing: 0.05em;
}
.code-block {
padding: 24px !important; margin: 0 !important; overflow-x: auto !important;
font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', monospace !important;
font-size: 13.5px !important; line-height: 1.7 !important; color: #e2e8f0 !important;
white-space: pre !important; background: transparent !important;
border: none !important; border-radius: 0 !important;
}
.markdown-body .sora-page .code-block {
padding: 24px !important; margin: 0 !important; overflow-x: auto !important;
font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', monospace !important;
font-size: 13.5px !important; line-height: 1.7 !important; color: #e2e8f0 !important;
white-space: pre !important; background: transparent !important;
border: none !important; border-radius: 0 !important;
}
.code-right h2 {
font-size: clamp(24px, 3vw, 32px);
font-weight: 700; color: var(--el-text-color-primary); margin-bottom: 12px;
letter-spacing: normal;
}
.code-right > p { font-size: 16px; color: var(--el-text-color-regular); line-height: 1.6; margin-bottom: 32px; }
.explain-steps { display: flex; flex-direction: column; gap: 20px; }
.explain-step { display: flex; gap: 16px; align-items: flex-start; }
.step-num {
width: 32px; height: 32px; border-radius: 50%;
background: var(--el-bg-color-page); border: 1px solid var(--el-border-color-light);
display: flex; align-items: center; justify-content: center;
font-size: 14px; font-weight: 700; color: var(--el-text-color-regular);
flex-shrink: 0;
}
.step-text h4 { font-size: 15px; font-weight: 700; color: var(--el-text-color-primary); margin-bottom: 2px; }
.step-text p { font-size: 14px; color: var(--el-text-color-secondary); line-height: 1.5; }
@media (max-width: 768px) {
.code-split { flex-direction: column; }
.code-left { order: 2; }
.code-right { order: 1; }
} .usecases-grid {
display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;
}
.uc-card {
padding: 28px 24px; background: var(--el-bg-color);
border: none; border-radius: 20px; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.08);
text-align: center;
transition: border-color 0.2s, box-shadow 0.2s, transform 0.15s;
}
.uc-card:hover { box-shadow: 0 8px 24px 0 rgba(0,0,0,0.12);
transform: translateY(-2px);
}
.uc-icon { font-size: 36px; margin-bottom: 16px; }
.uc-card h3 { font-size: 17px; font-weight: 700; color: var(--el-text-color-primary); margin-bottom: 8px; }
.uc-card p { font-size: 14px; color: var(--el-text-color-regular); line-height: 1.6; }
@media (max-width: 1024px) { .usecases-grid { grid-template-columns: repeat(2, 1fr); } } @media (max-width: 480px) { .usecases-grid { grid-template-columns: 1fr; } } .steps-row {
display: flex; align-items: flex-start; justify-content: center;
margin-bottom: 48px;
}
.stp-card { flex: 1; max-width: 320px; text-align: center; padding: 0 24px; }
.stp-num {
font-size: clamp(48px, 6vw, 72px);
font-weight: 700; color: #e2e8f0;
letter-spacing: -0.04em; line-height: 1;
margin-bottom: 20px;
}
.stp-card h3 { font-size: 18px; font-weight: 700; color: var(--el-text-color-primary); margin-bottom: 10px; }
.stp-card p { font-size: 15px; color: var(--el-text-color-regular); line-height: 1.6; }
.stp-conn {
width: 60px; height: 2px; background: var(--el-border-color-light);
margin-top: 36px; flex-shrink: 0;
}
.steps-cta { text-align: center; }
@media (max-width: 768px) {
.steps-row { flex-direction: column; align-items: center; gap: 32px; }
.stp-conn { width: 2px; height: 32px; margin: 0; }
.stp-card { max-width: 100%; }
}
.cmp-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.sora-page .cmp-table {
display: table !important;
width: 100%; max-width: 860px; margin: 0 auto;
border-collapse: collapse; font-size: 15px;
}
.sora-page .cmp-table th, .cmp-table td {
padding: 16px 20px; text-align: center;
border-bottom: 1px solid var(--el-border-color-light);
}
.sora-page .cmp-table th {
font-weight: 700; color: var(--el-text-color-regular); font-size: 14px;
text-transform: uppercase; letter-spacing: 0.04em;
background: var(--el-bg-color-page);
}
.sora-page .cmp-table td:first-child, .cmp-table th:first-child {
text-align: left; font-weight: 600; color: var(--el-text-color-primary);
}
.cmp-us { font-weight: 700; }
.cmp-brand { font-weight: 700; color: var(--el-text-color-primary); }
.ck { color: #10b981; font-weight: 700; font-size: 18px; }
.cx { color: #d1d5db; font-weight: 700; font-size: 18px; }
@media (max-width: 640px) {
.cmp-table th, .cmp-table td { padding: 12px 10px; font-size: 13px; }
} .models-grid {
display: grid; grid-template-columns: repeat(2, 1fr);
gap: 24px; max-width: 720px; margin: 0 auto;
}
.mdl-card {
padding: 32px 28px;
border: none; border-radius: 20px; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.08);
background: var(--el-bg-color); position: relative;
}
.mdl-card.mdl-rec { border-color: #277186; border-width: 2px; }
.mdl-rec-badge {
position: absolute; top: -12px; left: 50%;
transform: translateX(-50%);
padding: 4px 14px; background: #277186; color: #ffffff;
border-radius: 9999px; font-size: 12px; font-weight: 700;
text-transform: uppercase; letter-spacing: 0.04em;
}
.mdl-head { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.mdl-head h3 { font-size: 20px; font-weight: 700; color: var(--el-text-color-primary); }
.mdl-tag {
padding: 3px 10px; background: var(--el-bg-color-page); border-radius: 9999px;
font-size: 11px; font-weight: 700; color: var(--el-text-color-regular);
text-transform: uppercase; letter-spacing: 0.04em;
}
.mdl-tag-blue { background: #eff6ff; color: #2563eb; }
.mdl-tag-purple { background: #e9f1f3; color: #277186; }
.sora-page .mdl-desc { font-size: 15px; color: var(--el-text-color-regular); line-height: 1.6; margin-bottom: 20px; }
.mdl-feats { display: flex; flex-direction: column; gap: 8px; }
.mdl-feats li { font-size: 14px; color: var(--el-text-color-regular); line-height: 1.4; }
@media (max-width: 768px) { .models-grid { grid-template-columns: 1fr; } } .price-grid {
display: grid !important; grid-template-columns: repeat(2, 1fr) !important;
gap: 24px !important; max-width: 720px !important; margin: 0 auto !important;
align-items: start;
}
.price-card {
padding: 36px 32px;
border: 1px solid var(--el-border-color-light); border-radius: 20px;
background: var(--el-bg-color); position: relative;
}
.price-card-feat {
border: 2px solid #277186;
box-shadow: 0 8px 32px rgba(0,0,0,0.08);
transform: scale(1.03);
}
.price-feat-badge {
position: absolute; top: -13px; left: 50%;
transform: translateX(-50%);
padding: 5px 18px; background: #277186; color: #ffffff;
border-radius: 9999px; font-size: 12px; font-weight: 700;
text-transform: uppercase; letter-spacing: 0.04em;
white-space: nowrap;
}
.price-tier {
font-size: 16px; font-weight: 700; color: var(--el-text-color-regular);
text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 12px;
}
.price-amt {
font-size: clamp(36px, 5vw, 48px);
font-weight: 700; color: var(--el-text-color-primary); letter-spacing: normal;
}
.price-per { font-size: 16px; color: var(--el-text-color-secondary); font-weight: 500; }
.sora-page .price-desc { font-size: 14px; color: var(--el-text-color-secondary); margin-bottom: 24px; margin-top: 8px; }
.sora-page .price-feats { display: flex; flex-direction: column; gap: 10px; margin-bottom: 36px; }
.sora-page .price-feats li { font-size: 14px; color: var(--el-text-color-regular); line-height: 1.4; display: flex; align-items: center; gap: 8px; }
.price-ck { color: #10b981; font-weight: 700; font-size: 14px; flex-shrink: 0; }
.price-btn {
display: block; text-align: center; padding: 14px 0;
border-radius: 9999px; font-size: 15px; font-weight: 600;
transition: background 0.2s, border-color 0.2s, transform 0.15s;
width: 100%; cursor: pointer;
}
.sora-page .price-btn-fill { background: #277186; color: #ffffff !important; border: none; text-decoration: none !important; }
.sora-page .price-btn-fill:hover { background: #1f5a6b; transform: translateY(-1px); text-decoration: none !important; }
.sora-page .price-btn-out { background: var(--el-bg-color); color: var(--el-text-color-primary) !important; border: 1px solid var(--el-border-color-light); text-decoration: none !important; }
.sora-page .price-btn-out:hover { background: var(--el-bg-color-page); text-decoration: none !important; }
@media (max-width: 768px) {
.price-grid { grid-template-columns: 1fr !important; }
.price-card-feat { transform: none; }
} .faq-list { display: flex; flex-direction: column; }
.faq-item { border-bottom: 1px solid var(--el-border-color-light); }
.faq-item:first-child { border-top: 1px solid #e5e7eb; }
.faq-q {
display: flex; justify-content: space-between; align-items: center;
padding: 20px 0; cursor: pointer;
font-size: 16px; font-weight: 600; color: var(--el-text-color-primary);
list-style: none; user-select: none;
transition: color 0.2s;
}
.faq-q::-webkit-details-marker { display: none; }
.faq-q:hover { color: var(--el-text-color-primary); }
.faq-chev { font-size: 18px; color: var(--el-text-color-secondary); transition: transform 0.2s; flex-shrink: 0; }
.faq-item[open] .faq-chev { transform: rotate(180deg); }
.faq-a { padding: 0 0 20px; }
.faq-a p { font-size: 15px; color: var(--el-text-color-regular); line-height: 1.7; }
.rel-grid {
display: grid; grid-template-columns: repeat(2, 1fr);
gap: 16px; max-width: 800px; margin: 0 auto;
}
.rel-card
{
display: flex; align-items: center; gap: 16px;
padding: 20px 24px; background: var(--el-bg-color);
border: none; border-radius: 20px; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.08);
transition: border-color 0.2s, box-shadow 0.2s;
}
.rel-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.rel-icon { font-size: 28px; flex-shrink: 0; }
.rel-info { flex: 1; min-width: 0; }
.rel-info h3 { font-size: 15px; font-weight: 700; color: var(--el-text-color-primary); margin-bottom: 2px; }
.rel-info p { font-size: 13px; color: var(--el-text-color-secondary); line-height: 1.4; }
.rel-arrow {
font-size: 18px; color: #cbd5e1; flex-shrink: 0;
transition: color 0.2s, transform 0.2s;
}
.rel-card:hover .rel-arrow { color: var(--el-text-color-regular); transform: translateX(3px); }
@media (max-width: 640px) { .rel-grid { grid-template-columns: 1fr; } } .sora-cta {
padding: 100px 0; background: #0f172a;
text-align: center; position: relative; overflow: hidden;
}
.sora-cta::before {
content: '';
position: absolute; top: -100px; left: 50%;
transform: translateX(-50%);
width: 700px; height: 400px;
background: radial-gradient(ellipse, rgba(39, 113, 134, 0.12) 0%, transparent 70%);
pointer-events: none;
}
.sora-cta h2 {
font-size: clamp(28px, 4vw, 44px);
font-weight: 700; color: #f8fafc;
letter-spacing: normal; margin-bottom: 28px;
position: relative;
}
.sora-cta > div > p {
font-size: clamp(16px, 2vw, 18px);
color: var(--el-text-color-secondary); max-width: 520px;
margin: 0 auto 56px; line-height: 1.6;
position: relative;
}
.cta-actions {
display: flex; gap: 12px; justify-content: center;
flex-wrap: wrap; position: relative;
}
.sora-page .btn-cta-light {
display: inline-flex; align-items: center; gap: 6px;
padding: 14px 32px; background: #277186; color: #ffffff !important;
border-radius: 9999px; font-size: 15px; font-weight: 700;
transition: background 0.2s, transform 0.15s;
text-decoration: none !important;
}
.sora-page .btn-cta-light:hover { background: #1f5a6b; transform: translateY(-1px); text-decoration: none !important; }
.sora-page .btn-cta-ghost {
display: inline-flex; align-items: center;
padding: 14px 32px; background: transparent; color: #94a3b8 !important;
border: 1px solid #334155; border-radius: 9999px;
font-size: 15px; font-weight: 600;
transition: border-color 0.2s, color 0.2s;
text-decoration: none !important;
}
.sora-page .btn-cta-ghost:hover { border-color: var(--el-text-color-regular); color: #e2e8f0 !important; text-decoration: none !important; }
.sora-page code
```css
{
background: #dbeafe !important;
padding: 2px 8px !important;
border-radius: 5px !important;
font-size: 13px !important;
font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', monospace !important;
color: #1e40af !important;
border: 1px solid #bfdbfe !important;
}
.s-text-dark { color: var(--el-text-color-primary); }
.s-text-brand { color: #277186; }
.s-section-body { font-size: 16px; color: var(--el-text-color-regular); line-height: 1.8; text-align: center; max-width: 680px; margin: 0 auto; }
.s-section-body p + p { margin-top: 16px; }
.s-text-muted { color: var(--el-text-color-secondary); }
html.dark .sora-page { background: var(--el-bg-color); color: var(--el-text-color-primary); }
html.dark .sora-page a { color: inherit; }
html.dark .markdown-body .sora-page a { color: inherit !important; }
html.dark .markdown-body .sora-page a.s-btn-primary,
html.dark .markdown-body .sora-page a.price-btn-fill,
html.dark .markdown-body .sora-page a.btn-cta-light { color: #ffffff !important; }
html.dark .markdown-body .sora-page a.s-btn-secondary { color: var(--el-text-color-primary) !important; }
html.dark .markdown-body .sora-page a.price-btn-out { color: var(--el-text-color-primary) !important; }
html.dark .markdown-body .sora-page a.btn-cta-ghost { color: #94a3b8 !important; }
html.dark .markdown-body .sora-page a.btn-cta-ghost:hover { color: var(--el-text-color-primary) !important; }
html.dark .s-bg-white { background: var(--el-bg-color); }
html.dark .s-bg-gray { background: var(--el-bg-color-page); }
html.dark .s-bg-dark { background: var(--el-bg-color); }
html.dark .s-header h2 { color: var(--el-text-color-primary); }
html.dark .s-header p { color: var(--el-text-color-secondary); }
html.dark .sora-page .s-btn-primary { background: #277186; color: #ffffff !important; }
html.dark .sora-page .s-btn-primary:hover { background: #1f5a6b; }
html.dark .sora-page .s-btn-secondary {
background: #1e293b; color: var(--el-text-color-primary) !important;
border-color: #475569;
}
html.dark .sora-page .s-btn-secondary:hover { background: var(--el-border-color); border-color: var(--el-text-color-regular); }
html.dark .sora-hero { background: var(--el-bg-color); }
html.dark .sora-hero::before {
background: radial-gradient(ellipse, rgba(39, 113, 134, 0.15) 0%, transparent 70%);
}
html.dark .hero-badge { background: var(--el-bg-color-page); border-color: var(--el-border-color); color: var(--el-text-color-secondary); }
html.dark .sora-hero h1 { color: var(--el-text-color-primary); }
html.dark .sora-hero h1 span { color: #3b9ab5; }
html.dark .sora-page .hero-subtitle { color: var(--el-text-color-secondary); }
html.dark .hero-highlights .h-item { color: var(--el-text-color-secondary); }
html.dark .hero-highlights .h-div { background: var(--el-border-color); }
html.dark .sora-stats { background: var(--el-bg-color-page); border-color: var(--el-border-color); }
html.dark .stat-val { color: var(--el-text-color-primary); }
html.dark .stat-lbl { color: var(--el-text-color-regular); }
html.dark .feat-card {
background: var(--el-bg-color-page); border-color: var(--el-border-color);
}
html.dark .feat-card:hover { border-color: var(--el-text-color-regular); box-shadow: 0 4px 16px rgba(0,0,0,0.3); }
html.dark .feat-card h3 { color: var(--el-text-color-primary); }
html.dark .feat-card p { color: var(--el-text-color-secondary); }
html.dark .code-right h2 { color: var(--el-text-color-primary); }
html.dark .code-right > p { color: var(--el-text-color-secondary); }
html.dark .step-num { background: var(--el-border-color); border-color: var(--el-text-color-regular); color: var(--el-text-color-secondary); }
html.dark .step-text h4 { color: var(--el-text-color-primary); }
html.dark .step-text p { color: var(--el-text-color-regular); }
html.dark .sora-page code {
background: #1e3a5f !important; color: #93c5fd !important; border-color: #2563eb !important;
}
html.dark .s-text-dark { color: var(--el-text-color-primary); }
html.dark .s-text-brand { color: #3b9ab5; }
html.dark .s-section-body { color: var(--el-text-color-secondary); }
html.dark .uc-card { background: var(--el-bg-color-page); border-color: var(--el-border-color); }
html.dark .uc-card:hover { border-color: var(--el-text-color-regular); box-shadow: 0 4px 16px rgba(0,0,0,0.3); }
html.dark .uc-card h3 { color: var(--el-text-color-primary); }
html.dark .uc-card p { color: var(--el-text-color-secondary); }
html.dark .stp-num { color: #334155; }
html.dark .stp-card h3 { color: var(--el-text-color-primary); }
html.dark .stp-card p { color: var(--el-text-color-secondary); }
html.dark .stp-conn { background: var(--el-border-color); }
html.dark .cmp-table th { background: var(--el-bg-color-page); color: var(--el-text-color-secondary); }
html.dark .cmp-table td { border-color: var(--el-border-color); }
html.dark .cmp-table th { border-color: var(--el-border-color); }
html.dark .cmp-table td:first-child { color: var(--el-text-color-primary); }
html.dark .cmp-brand { color: var(--el-text-color-primary); }
html.dark .cx { color: var(--el-text-color-regular); }
html.dark .mdl-card { background: var(--el-bg-color-page); border-color: var(--el-border-color); }
html.dark .mdl-card.mdl-rec { border-color: #277186; }
html.dark .mdl-head h3 { color: var(--el-text-color-primary); }
html.dark .mdl-tag { background: var(--el-border-color); color: var(--el-text-color-secondary); }
html.dark .mdl-tag-blue { background: #1e3a5f; color: #60a5fa; }
html.dark .mdl-tag-purple { background: rgba(39, 113, 134, 0.2); color: #3b9ab5; }
html.dark .mdl-desc { color: var(--el-text-color-secondary); }
html.dark .mdl-feats li { color: var(--el-text-color-secondary); }
html.dark .price-card { background: var(--el-bg-color-page); border-color: var(--el-border-color); }
html.dark .price-card-feat { border-color: #277186; box-shadow: 0 8px 32px rgba(0,0,0,0.3); }
html.dark .price-tier { color: var(--el-text-color-secondary); }
html.dark .price-amt { color: var(--el-text-color-primary); }
html.dark .price-desc { color: var(--el-text-color-regular); }
html.dark .price-feats li { color: var(--el-text-color-secondary); }
html.dark .sora-page .price-btn-out {
background: #1e293b; color: var(--el-text-color-primary) !important; border-color: #334155;
}
html.dark .sora-page .price-btn-out:hover { background: var(--el-border-color); border-color: var(--el-text-color-regular); }
html.dark .faq-item { border-color: var(--el-border-color); }
html.dark .faq-q { color: var(--el-text-color-primary); }
html.dark .faq-q:hover { color: #ffffff; }
html.dark .faq-chev { color: var(--el-text-color-regular); }
html.dark .faq-a p { color: var(--el-text-color-secondary); }
html.dark .rel-card { background: var(--el-bg-color-page); border-color: var(--el-border-color); }
html.dark .rel-card:hover { border-color: var(--el-text-color-regular); box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
html.dark .rel-info h3 { color: var(--el-text-color-primary); }
html.dark .rel-info p { color: var(--el-text-color-regular); }
html.dark .rel-arrow { color: var(--el-text-color-regular); }
html.dark .rel-card:hover .rel-arrow { color: var(--el-text-color-secondary); }
html.dark .sora-cta { background: #020617; }
html.dark .sora-cta::before {
background: radial-gradient(ellipse, rgba(39, 113, 134, 0.2) 0%, transparent 70%);
}
html.dark .sora-page .btn-cta-light { color: #ffffff !important; }
html.dark .sora-page .btn-cta-ghost { color: #94a3b8 !important; }
html.dark .sora-page .btn-cta-ghost:hover { color: var(--el-text-color-primary) !important; }
html.dark .sora-page .price-btn-fill { color: #ffffff !important; }
</style>
<div class="sora-page">
<section class="sora-hero">
<div class="s-container-narrow">
<div class="hero-badge">
<span class="badge-dot"></span>
Sora API · Ace Data Cloud
</div>
<h1>
Sora API:<br/>
Generate <span>AI Videos</span>
</h1>
<p class="hero-subtitle">
Integrate OpenAI Sora video generation capabilities into your application through a stable and comprehensive REST API. Text-to-video, image-to-video, character-driven video—all accomplished through a unified interface.
```
</p>
<div class="hero-actions">
<a href="https://platform.acedata.cloud/documents/sora-videos" class="s-btn-primary">📄 View Documentation</a>
</div>
<div class="hero-highlights">
<span class="h-item">🎬 2 Model Versions</span>
<span class="h-div"></span>
<span class="h-item">🖼️ Image to Video</span>
<span class="h-div"></span>
<span class="h-item">📄 OpenAPI 3.0 Specification</span>
<span class="h-div"></span>
<span class="h-item">🔑 Bearer Token Authentication</span>
</div>
</div>
</section>
<section class="sora-stats s-section-sm s-bg-gray">
<div class="s-container">
<div class="stats-grid">
<div>
<div class="stat-icon">🎬</div>
<div class="stat-val">2</div>
<div class="stat-lbl">Model Versions</div>
</div>
<div>
<div class="stat-icon">⏱️</div>
<div class="stat-val">25s</div>
<div class="stat-lbl">Longest Video Duration</div>
</div>
<div>
<div class="stat-icon">📐</div>
<div class="stat-val">3</div>
<div class="stat-lbl">Orientation</div>
</div>
<div>
<div class="stat-icon">📡</div>
<div class="stat-val">2</div>
<div class="stat-lbl">API Endpoints</div>
</div>
</div>
</div>
</section>
<section class="s-section s-bg-white">
<div class="s-container-narrow">
<div class="s-header">
<h2>Does Sora have an official API?</h2>
</div>
<div class="s-section-body">
<p>OpenAI's Sora video generation model is currently only available through ChatGPT Plus/Pro subscriptions and limited enterprise partnerships, and a standalone public REST API has not yet been opened.</p>
<p>Ace Data Cloud fills this gap by providing a <strong class="s-text-dark">stable, production-ready API</strong> that allows you to programmatically access Sora's video generation capabilities in full—including the latest <strong class="s-text-brand">sora-2</strong> and <strong class="s-text-brand">sora-2-pro</strong> models—through a simple REST interface, equipped with OpenAPI specifications, Webhook support, streaming, and pay-as-you-go pricing.</p>
</div>
</div>
</section>
<section class="s-section s-bg-gray">
<div class="s-container">
<div class="s-header">
<h2>All Features of Sora API</h2>
<p>A comprehensive API suite covering the complete workflow of Sora video generation</p>
</div>
<div class="features-grid">
<div class="feat-card">
<div class="feat-icon">🎬</div>
<h3>Text to Video Generation</h3>
<p>Generate high-quality AI videos from text prompts. Describe the scenes, characters, and actions you want, and Sora will create realistic video content.</p>
</div>
<div class="feat-card">
<div class="feat-icon">🖼️</div>
<h3>Image to Video</h3>
<p>Upload reference images and let Sora convert static images into dynamic videos. Use the <code>image_urls</code> parameter to pass in image links.</p>
</div>
<div class="feat-card">
<div class="feat-icon">🎭</div>
<h3>Character-Driven Video</h3>
<p>Upload character reference videos using <code>character_url</code> to maintain consistent character appearance and action style in the generated video.</p>
</div>
<div class="feat-card">
<div class="feat-icon">📐</div>
<h3>Flexible Screen Settings</h3>
<p>Supports three orientations: landscape, portrait, and square, as well as two resolution options: small and large.</p>
</div>
<div class="feat-card">
<div class="feat-icon">⏱️</div>
<h3>Flexible Video Duration</h3>
<p>Supports video durations of 10 seconds, 15 seconds, and 25 seconds. 25 seconds is limited to the sora-2-pro model—satisfying various needs from short to long videos.</p>
</div>
<div class="feat-card">
<div class="feat-icon">⚡</div>
<h3>Streaming and Webhook</h3>
<p>Supports NDJSON real-time streaming to get generation progress updates, or set a <code>callback_url</code> to asynchronously receive results. No polling required.</p>
</div>
</div>
</div>
</section>
<section class="s-section s-bg-white">
<div class="s-container">
<div class="code-split">
<div class="code-left">
<div class="code-wrap">
<div class="code-bar">
<div class="code-dots"><i class="r"></i><i class="y"></i><i class="g"></i></div>
<div class="code-lang">cURL</div>
</div>
<pre class="code-block">curl -X POST https://api.acedata.cloud/sora/videos \
-H "Authorization: Bearer YOUR_API_KEY" \
-H "Content-Type: application/json" \
-d '{
"prompt": "A cat running through a sunlit meadow",
"model": "sora-2",
"duration": 10,
"orientation": "landscape",
"size": "large",
"callback_url": "https://your-app.com/webhook"
}'</pre>
</div>
<div style="margin-top: 16px;">
<div class="code-wrap">
<div class="code-bar">
<div class="code-dots"><i class="r"></i><i class="y"></i><i class="g"></i></div>
<div class="code-lang">Response</div>
</div>
<pre class="code-block">{
"success": true,
"task_id": "c7e3a1...",
"data":
{
"id": "f9d2b4...",
"video_url": "https://cdn.acedata.cloud/f9d2b4.mp4",
"state": "succeeded",
"prompt": "A cat running through a sunlit meadow",
"model": "sora-2",
"duration": 10
}
}</pre>
</div>
</div>
</div>
<div class="code-right">
<h2>Quick Start - Get Started in 5 Minutes</h2>
<p>A concise REST API that uses Bearer Token authentication. One request is enough to generate your first AI video.</p>
<div class="explain-steps">
<div class="explain-step">
<div class="step-num">1</div>
<div class="step-text">
<h4>Get API Key</h4>
<p>Register on Ace Data Cloud and obtain your Bearer Token from the console</p>
</div>
</div>
<div class="explain-step">
<div class="step-num">2</div>
<div class="step-text">
<h4>Send POST Request</h4>
<p>Send a request to <code>/sora/videos</code> with your prompt and model preferences</p>
</div>
</div>
<div class="explain-step">
<div class="step-num">3</div>
<div class="step-text">
<h4>Get Your Video</h4>
<p>Obtain the video URL - which can be downloaded, embedded, or shared directly</p>
</div>
</div>
</div>
</div>
</div>
</div>
</section>
<section class="s-section s-bg-gray">
<div class="s-container">
<div class="s-header">
<h2>What Can You Build with the Sora API?</h2>
<p>From content creation to enterprise applications - developers are building these projects</p>
</div>
<div class="usecases-grid">
<div class="uc-card">
<div class="uc-icon">🎬</div>
<h3>Video Content Platforms</h3>
<p>Build AI video generation applications that allow users to quickly create short video content through text descriptions</p>
</div>
<div class="uc-card">
<div class="uc-icon">📱</div>
<h3>Social Media Tools</h3>
<p>Provide AI video generation features for social media creators to quickly produce eye-catching short videos</p>
</div>
<div class="uc-card">
<div class="uc-icon">🤖</div>
<h3>AI Agents and MCP</h3>
<p>Integrate with Claude, ChatGPT, or any AI Agent through our MCP Server for natural language video creation</p>
</div>
<div class="uc-card">
<div class="uc-icon">🏢</div>
<h3>Enterprise Marketing</h3>
<p>Generate product demo videos, advertising materials, and brand promotional content in bulk</p>
</div>
</div>
</div>
</section>
<section class="s-section s-bg-white">
<div class="s-container">
<div class="s-header">
<h2>3 Steps to Get Started Quickly</h2>
<p>From registration to generating your first AI video, it takes less than 5 minutes</p>
</div>
<div class="steps-row">
<div class="stp-card">
<div class="stp-num">01</div>
<h3>Register and Get API Key</h3>
<p>Create a free account on Ace Data Cloud. Generate your Bearer Token from the API management console.</p>
</div>
<div class="stp-conn"></div>
<div class="stp-card">
<div class="stp-num">02</div>
<h3>Initiate Your First API Call</h3>
<p>Send a POST request with a text prompt to <code>/sora/videos</code>. You can use SDK, cURL, or any HTTP client.</p>
</div>
<div class="stp-conn"></div>
<div class="stp-card">
<div class="stp-num">03</div>
<h3>Integration and Expansion</h3>
<p>Embed the API into your application. Use Webhook for asynchronous processing and confidently scale to production.</p>
</div>
</div>
<div class="steps-cta">
<a href="https://platform.acedata.cloud/documents/sora-videos" class="s-btn-primary">View Documentation →</a>
</div>
</div>
</section>
<section class="s-section s-bg-gray">
<div class="s-container">
<div class="s-header">
<h2>Why Choose Ace Data Cloud Over Other Sora APIs?</h2>
<p>Check out our comparative advantages on the features that matter most to developers</p>
</div>
<div class="cmp-wrap">
<table class="cmp-table">
<thead>
<tr>
<th>Feature</th>
<th class="cmp-us"><span class="cmp-brand">Ace Data Cloud</span></th>
<th>Other Platforms</th>
</tr>
</thead>
<tbody>
<tr>
<td>sora-2 + sora-2-pro models</td>
<td class="cmp-us"><span class="ck">✓</span></td>
<td>Partial support</td>
</tr>
<tr>
<td>Text to Video</td>
<td class="cmp-us"><span class="ck">✓</span></td>
<td><span class="ck">✓</span></td>
</tr>
<tr>
<td>Image to Video</td>
<td class="cmp-us"><span class="ck">✓</span></td>
<td>Partial support</td>
</tr>
<tr>
<td>Character-driven Video</td>
<td class="cmp-us"><span class="ck">✓</span></td>
<td><span class="cx">✗</span></td>
</tr>
<tr>
<td>OpenAPI 3.0 Specification</td>
<td class="cmp-us"><span class="ck">✓</span></td>
<td><span class="cx">✗</span></td>
</tr>
<tr>
<td>Webhook Callback</td>
<td class="cmp-us"><span class="ck">✓</span></td>
<td>Partial support</td>
</tr>
<tr>
<td>NDJSON Streaming</td>
<td class="cmp-us"><span class="ck">✓</span></td>
<td><span class="cx">✗</span></td>
</tr>
<tr>
<td>Pay-as-you-go</td>
<td class="cmp-us"><span class="ck">✓</span></td>
<td>Partial support</td>
</tr>
<tr>
<td>MCP Server (AI Agent Integration)</td>
<td class="cmp-us"><span class="ck">✓</span></td>
<td><span class="cx">✗</span></td>
</tr>
</tbody>
</table>
</div>
</div>
</section>
<section class="s-section s-bg-white">
<div class="s-container">
<div class="s-header">
<h2>Comparison of Sora with Other AI Video Models</h2>
<p>Hesitating between Sora, Luma, Veo, and other AI video platforms? Check out their comparisons.</p>
</div>
<div class="cmp-wrap">
<table class="cmp-table">
<thead>
<tr>
<th>Capability</th>
<th class="cmp-us"><span class="cmp-brand">Sora (via Ace Data)</span></th>
<th>Luma</th>
<th>Veo</th>
</tr>
</thead>
<tbody>
<tr>
<td>Text to Video</td>
<td class="cmp-us"><span class="ck">✓</span></td>
<td><span class="ck">✓</span></td>
<td><span class="ck">✓</span></td>
</tr>
<tr>
<td>Image to Video</td>
<td class="cmp-us"><span class="ck">✓</span></td>
<td><span class="ck">✓</span></td>
<td><span class="ck">✓</span></td>
</tr>
<tr>
<td>Character-driven Video</td>
<td class="cmp-us"><span class="ck">✓</span></td>
<td><span class="cx">✗</span></td>
<td><span class="cx">✗</span></td>
</tr>
<tr>
<td>Up to 25 Seconds Video</td>
<td class="cmp-us"><span class="ck">✓</span></td>
<td><span class="cx">✗</span></td>
<td><span class="ck">✓</span></td>
</tr>
<tr>
<td>Multiple Aspect Ratios</td>
<td class="cmp-us"><span class="ck">✓</span></td>
<td><span class="ck">✓</span></td>
<td><span class="ck">✓</span></td>
</tr>
<tr>
<td>API Access</td>
<td class="cmp-us"><span class="ck">✓</span></td>
<td><span class="ck">✓</span></td>
<td><span class="ck">✓</span></td>
</tr>
</tbody>
</table>
</div>
</div>
</section>
<section class="s-section s-bg-gray">
<div class="s-container">
<div class="s-header">
<h2>Which Model is Right for You?</h2>
<p>Choose the right Sora model based on your needs for quality, duration, and budget</p>
</div>
<div class="models-grid">
<div class="mdl-card mdl-rec">
<div class="mdl-rec-badge">Recommended</div>
<div class="mdl-head">
<h3>sora-2</h3>
<span class="mdl-tag-blue mdl-tag">Standard</span>
</div>
<p class="mdl-desc">The best value choice, suitable for most video generation scenarios. Fast, stable, and low-cost.</p>
<ul class="mdl-feats">
<li>✓ Text to Video + Image to Video</li>
<li>✓ Character-driven Video</li>
<li>✓ 10 seconds / 15 seconds video</li>
<li>✓ Landscape / Portrait / Square</li>
<li>✓ As low as $0.053 / call</li>
</ul>
</div>
<div class="mdl-card">
<div class="mdl-head">
<h3>sora-2-pro</h3>
<span class="mdl-tag-purple mdl-tag">Professional</span>
</div>
<p class="mdl-desc">Highest quality output, supports 25 seconds long videos. Suitable for professional content creation and commercial use.</p>
<ul class="mdl-feats">
<li>✓ All features of sora-2</li>
<li>✓ Higher video quality</li>
<li>✓ Supports 25 seconds long videos</li>
<li>✓ Suitable for commercial output</li>
<li>✓ As low as $0.53 / call</li>
</ul>
</div>
</div>
</div>
</section>
<section class="s-section s-bg-white">
<div class="s-container">
<div class="s-header">
<h2>Sora API Pricing</h2>
<p>Transparent pay-as-you-go pricing. No subscription fees. No hidden costs. Pay only for usage.</p>
<p style="font-size:14px;color:#94a3b8;margin-top:8px;">Bulk packages up to 27% discount</p>
</div>
<div class="price-grid">
<div class="price-card price-card-feat">
<div class="price-feat-badge">Pay-as-you-go</div>
<div class="price-tier">Video Generation</div>
<div>
<span class="price-amt">$0.053</span>
<span class="price-per"> / call</span>
</div>
<p class="price-desc">Charged by model - generating 1 video per call</p>
<ul class="price-feats">
<li><span class="price-ck">✓</span> sora-2: as low as $0.053 / call</li>
<li><span class="price-ck">✓</span> sora-2-pro: as low as $0.53 / call</li>
<li><span class="price-ck">✓</span> Text to Video + Image to Video</li>
<li><span class="price-ck">✓</span> Character-driven Video</li>
<li><span class="price-ck">✓</span> Webhook + Streaming</li>
<li><span class="price-ck">✓</span> Task polling - <strong>free</strong></li>
</ul>
<a href="https://platform.acedata.cloud/services/sora?tab=pricing" class="price-btn price-btn-fill">View Pricing Details</a>
<a href="https://platform.acedata.cloud/documents/sora-videos" class="price-btn price-btn-out" style="margin-top:8px">View API Documentation</a>
</div>
<div class="price-card">
<div class="price-tier">Enterprise Edition</div>
<div>
<span class="price-amt">Custom</span>
</div>
<p class="price-desc">Bulk discounts for high-usage teams</p>
<ul class="price-feats">
<li><span class="price-ck">✓</span> Usage-based discounts</li>
<li><span class="price-ck">✓</span> Priority support</li>
<li><span class="price-ck">✓</span> Dedicated account manager</li>
<li><span class="price-ck">✓</span> Custom rate limits</li>
<li><span class="price-ck">✓</span> SLA guarantees</li>
</ul>
<a href="https://platform.acedata.cloud/support" class="price-btn price-btn-out">Contact Sales</a>
</div>
</div>
</div>
</section>
<section class="s-section s-bg-gray">
<div class="s-container-narrow">
<div class="s-header">
<h2>Frequently Asked Questions</h2>
<p>Everything you need to know about using the Sora API</p>
</div>
<div class="faq-list">
<details class="faq-item">
<summary class="faq-q">
<span>Does Sora have an official API?</span>
<span class="faq-chev">▾</span>
</summary>
<div class="faq-a">
<p>OpenAI currently does not provide a standalone public Sora REST API. Sora is only available to ChatGPT Plus/Pro users through the web interface. Ace Data Cloud offers a stable, production-ready API that gives you full access to Sora's video generation capabilities, including the sora-2 and sora-2-pro models.</p>
</div>
</details>
<details class="faq-item">
<summary class="faq-q">
<span>What is the pricing model?</span>
<span class="faq-chev">▾</span>
</summary>
<div class="faq-a">
<p>We use a pay-as-you-go model with no subscription or monthly fees. The sora-2 model starts at $0.053/call, and the sora-2-pro model starts at $0.53/call. Bulk packages can enjoy up to a 27% discount. Task polling is free forever.</p>
</div>
</details>
<details class="faq-item">
<summary class="faq-q">
<span>Which models are supported?</span>
<span class="faq-chev">▾</span>
</summary>
<div class="faq-a">
<p>We support two versions of the Sora model: sora-2 (standard version, best value) and sora-2-pro (professional version, higher quality, supports 25 seconds long videos). We will support new models released by OpenAI as soon as possible.</p>
</div>
</details>
<details class="faq-item">
<summary class="faq-q">
<span>How to handle longer generation times?</span>
<span class="faq-chev">▾</span>
</summary>
<div class="faq-a">
<p>Three ways: (1) Use <code>callback_url</code> - set a Webhook URL, and we will POST the results once completed. (2) Use NDJSON streaming - set the <code>Accept: application/x-ndjson</code> request header to get real-time progress. (3) Poll through <code>/sora/tasks</code> - this endpoint is free and allows you to check the status at any time.</p>
</div>
</details>
<details class="faq-item">
<summary class="faq-q">
<span>Is image to video supported?</span>
<span class="faq-chev">▾</span>
</summary>
<div class="faq-a">
<p>Yes. Pass the reference image links through the <code>image_urls</code> parameter in the request, and Sora will generate a video based on the image content and your text prompt. You can also achieve character-driven video generation through <code>character_url</code>.</p>
</div>
</details>
<details class="faq-item">
<summary class="faq-q">
<span>What video specifications are supported?</span>
<span class="faq-chev">▾</span>
</summary>
<div class="faq-a">
<p>Video durations supported are 10 seconds, 15 seconds, and 25 seconds (25 seconds only for sora-2-pro). Aspect ratios supported are landscape, portrait, and square. Resolutions supported are small and large.</p>
</div>
</details>
<details class="faq-item">
<summary class="faq-q">
<span>Can it be used with AI Agents like Claude or ChatGPT?</span>
<span class="faq-chev">▾</span>
</summary>
<div class="faq-a">
<p>Yes! We provide an official MCP Server (<code>mcp-sora</code>) that can be directly integrated with Claude Desktop, VS Code, and other MCP-compatible AI tools. Your AI Agent can generate videos through natural language conversations. We also provide standard REST API + OpenAPI specification to support any other integration methods.</p>
</div>
</details>
<details class="faq-item">
<summary class="faq-q">
<span>What is "character-driven video"?</span>
<span class="faq-chev">▾</span>
</summary>
<div class="faq-a">
<p>Character-driven video allows you to upload a reference video through <code>character_url</code>, and Sora will maintain the appearance and motion style of that character in the generated video. Note: Real people cannot appear in the reference video, or it will fail to generate. You can specify the time range for the character's appearance in the video using <code>character_start</code> and <code>character_end</code>.</p>
</div>
</details>
</div>
</div>
</section>
<section class="s-section s-bg-white">
<div class="s-container">
<div class="s-header">
<h2>Other AI Models</h2>
<p>Explore our complete suite of AI APIs covering video, image, music, and more</p>
</div>
<div class="rel-grid">
<a

## Quick Start

- Base URL: [https://api.acedata.cloud](https://api.acedata.cloud)
- Service page: [Sora Video Generation on Ace Data Cloud](https://platform.acedata.cloud/service/sora)
- Docs: [Developer documentation](https://docs.acedata.cloud)

```bash
curl --request POST "https://api.acedata.cloud/sora/tasks" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{}'
```

## APIs and Guides

Explore the supported endpoints and integration guides for Sora Video Generation.

| API | Path | Integration Guidance |
| ---- | ---- | ------------ |
| [Sora Tasks API](https://platform.acedata.cloud/documents/c9d81bad-9064-4796-86b6-4fb43cc93a16) | `/sora/tasks` | [Sora Tasks API Integration Guide](https://platform.acedata.cloud/documents/a90964ff-27e4-4645-8d77-80755c8e731b) |
| [Sora Videos Generation API](https://platform.acedata.cloud/documents/99a24421-2e22-4028-8201-e19cb834b67e) | `/sora/videos` | [Sora Videos Generation API Integration Guide](https://platform.acedata.cloud/documents/ac9a395e-9306-460f-b22e-9edda07514fc) |

## Related Resources

- [Ace Data Cloud Developer Platform](https://platform.acedata.cloud)
- [Ace Data Cloud Docs](https://docs.acedata.cloud)
- [Status Page](https://status.acedata.cloud)
- [Ace Data Cloud GitHub Organization](https://github.com/AceDataCloud)

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud).