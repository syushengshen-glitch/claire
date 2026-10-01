# 十站上線與 AdSense 計畫

## 已完成

- 建立 10 個獨立利基站的本機檔案。
- 每站有 5 個工具頁、3 篇指南、法務頁、sitemap、robots、ads.txt。
- 所有站共用 publisher ID：`ca-pub-1837836558769995`。
- 內部連結檢查共 3,430 條，沒有死連結。
- 10 站首頁、品牌、AdSense client 注入與行動版已通過瀏覽器測試。

## Google Trends 免費研究

Google Trends 提供的是一個地區與時間區間內的相對熱度，不是絕對搜尋量。已觀察到的 Rising/Breakout 訊號包括：

| 主題 | Rising signal | 使用站點 |
|---|---|---|
| AI coding agents | `opencode +90%`, `ollama +90%` | CodeSignal Lab |
| AI voice generators | `fish audio +1,400%`, `kokoro voices Breakout` | VoiceSignal Lab |
| AI customer support | `otter ai +750%` | SupportSignal Lab |
| AI meeting notes | `read ai meeting notes in teams +300%` | MeetingSignal Lab |
| AI website builders | `figma ai website builder +550%` | WebSignal Lab |
| AI image editors | `bg remover Breakout`, `fooocus Breakout`, `ai image describer Breakout` | ImageSignal Lab |
| AI resume builders | `ai resume builder based on job description +200%`, `rezi +110%` | CareerSignal Lab |
| AI visual generators | `nano banana +2,400%`, `kling ai +1,500%`, `sora ai +650%` | VisualSignal Lab |
| AI SEO tools | `uploadarticle.com Breakout` | SearchSignal Lab |
| AI chatbot builders | `chatbot +800%` | BotSignal Lab |

這些不是 Google Keyword Planner 的絕對月搜尋量。因為目前沒有 Keyword Planner、Ahrefs 或 Semrush，所有站點都把趨勢標記為 Google Trends 相對訊號。

## 部署順序

1. 推送到 GitHub。
2. 將 repository 匯入 Vercel 十次。
3. 每次把 Root Directory 設為 `sites/<slug>`。
4. 使用表中的 project name，取得對應的 `*.vercel.app`。
5. 驗證十個首頁、`ads.txt`、`sitemap.xml` 與 AdSense client。
6. 在 AdSense 逐一新增網站、驗證擁有權、設定 Auto Ads、送交審查。
7. 每一站通過審查前不預期有廣告收益。

## 重要限制

- Google AdSense 只能有一個帳戶。
- 每個網站都要獨立驗證與審查。
- 新站目前只有 starter 內容，應先補上原創實測，再提交審查。
- Vercel Hobby 條款限制為 personal 或 non-commercial；商業廣告應先升級 Pro 或改用允許商業用途的主機。
