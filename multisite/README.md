# SignalStack 十站系統

`multisite/build_multisite.py` 會產生 `sites/` 下 10 個獨立靜態網站。每一站有自己的品牌、主題、工具頁、3 篇起始指南、sitemap、robots、ads.txt 與 AdSense publisher ID。

## 網站

| # | 主題 | Vercel 專案 | 品牌 |
|---|---|---|---|
| 1 | AI coding agents | `signalstack-coding-lab` | CodeSignal Lab |
| 2 | AI voice and dubbing | `signalstack-voice-lab` | VoiceSignal Lab |
| 3 | AI customer support | `signalstack-support-lab` | SupportSignal Lab |
| 4 | AI meeting notes | `signalstack-meeting-lab` | MeetingSignal Lab |
| 5 | AI website builders | `signalstack-website-lab` | WebSignal Lab |
| 6 | AI image editors | `signalstack-image-lab` | ImageSignal Lab |
| 7 | AI resume and career | `signalstack-career-lab` | CareerSignal Lab |
| 8 | AI visual generators | `signalstack-visual-lab` | VisualSignal Lab |
| 9 | AI SEO content tools | `signalstack-seo-lab` | SearchSignal Lab |
| 10 | AI chatbot builders | `signalstack-chatbot-lab` | BotSignal Lab |

## 重跑產生器

```powershell
& 'C:\Users\syush\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'C:\Users\syush\.codex\worktrees\1ea4\廣告收入設定\multisite\build_multisite.py'
```

## 檢查

```powershell
& 'C:\Users\syush\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'C:\Users\syush\.codex\worktrees\1ea4\廣告收入設定\multisite\check_multisite.py'

& 'C:\Users\syush\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' `
  'C:\Users\syush\.codex\worktrees\1ea4\廣告收入設定\multisite\test_multisite.js'
```

## AdSense

- Accounts are limited to one account per publisher.
- All sites use the same publisher ID: `ca-pub-1837836558769995`.
- Each site needs its own ownership verification, ads.txt check, and Google review.
- Auto Ads must be enabled separately for each site after it is added to AdSense.
- The starter content is not sufficient for approval by itself. Each site needs original tests, screenshots, and more content before review.


## Small Ops Lab

- 獨立站台：`sites/small-ops-lab`
- 主題：自由工作者與小型工作室的營運流程
- 5 個分類、15 篇原創指南、15 個模板或計算器頁面
- 產生器：`multisite/build_small_ops_lab.py`
- 內容資料：`multisite/small-ops-content.json`
- 樣式與工具：`multisite/themes/ops.css`、`multisite/themes/ops-tools.js`
- 使用同一個 AdSense publisher ID：`ca-pub-1837836558769995`
- 通過 AdSense 審查前，廣告位只顯示 Advertisement 標籤

重新建置：

```powershell
& 'C:\Users\syush\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'C:\Users\syush\.codex\worktrees\1ea4\廣告收入設定\multisite\build_small_ops_lab.py'
```

瀏覽器測試：

```powershell
& 'C:\Users\syush\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' `
  'C:\Users\syush\.codex\worktrees\1ea4\廣告收入設定\multisite\test_small_ops_lab.js'
```
