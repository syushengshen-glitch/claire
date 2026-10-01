# 從零到上線 SOP

## 第一階段：先驗證方向

在寫網站之前，先選一個可被搜尋、可自然連到 20 篇以上文章的方向。這個 starter 使用英文 AI 工具目錄，原因是英文市場通常有較高的廣告單價，但競爭也更高。

每個候選方向要記錄：

| 檢查項目 | 合格條件 |
|---|---|
| 搜尋需求 | 有明確長尾關鍵字，而不是只有品牌字 |
| 競爭程度 | 首頁不是全由大型媒體、官方網站佔滿 |
| 差異化 | 你有實測、專業背景、資料整理或更窄的使用者 |
| 商業意圖 | 可以自然連到工具評測、比較與教學 |
| 內容深度 | 至少能規劃 30 篇不重複主題 |
| 廣告風險 | 不會違反 AdSense 內容政策 |

先把 `docs/02-content-plan.csv` 的 P1 主題拿去 Google Keyword Planner、Search Console 或 Ahrefs 驗證。沒有需求的題目不要寫。

## 第二階段：建立網站

目前專案已經包含：

- `site/index.html`：首頁
- `site/directory.html`：可搜尋、可篩選的工具目錄
- `site/tools/`：32 個工具頁
- `site/category/`：7 個分類頁
- `site/guides/`：6 個工作流指南骨架
- `site/privacy.html`、`site/terms.html`、`site/contact.html`：法務與信任頁
- `site/sitemap.xml`、`site/robots.txt`、`site/ads.txt`
- `docs/02-content-plan.csv`：100 篇 SEO 主題規劃

建置指令：

```powershell
& 'C:\Users\syush\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'C:\Users\syush\Documents\ChatGPT\廣告收入設定\scripts\build_site.py' `
  --base-url 'https://你的網域.com'
```

等 AdSense 通過後再填 publisher ID：

```powershell
& 'C:\Users\syush\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'C:\Users\syush\Documents\ChatGPT\廣告收入設定\scripts\build_site.py' `
  --base-url 'https://你的網域.com' `
  --adsense-publisher 'ca-pub-你的ID'
```

## 第三階段：補內容，不要直接發 100 篇

網站模式成立與否，核心不是頁面數，而是頁面是否能解決搜尋問題。

建議先做 10 篇：

1. 從 `docs/02-content-plan.csv` 選 P1 題目。
2. 每篇先做 SERP 與關鍵字意圖檢查。
3. 實際試用至少 3 個工具，留下截圖與日期。
4. 用 AI 協助整理大綱與比較表。
5. 自己補上觀察、限制、適合誰、不適合誰。
6. 加入 3 到 5 個內部連結。
7. 讓另一位真人做事實與語氣檢查。
8. 每週更新 2 到 3 篇，而不是一次上線 100 篇。

這個流程比較慢，但比較接近影片裡「不要讓 AI 直接寫完整內容」的修正方向。

## 第四階段：部署

1. 建立 GitHub repository。
2. 將整個專案推到 repository。
3. 到 Vercel 匯入 GitHub repository。
4. 如果使用根目錄的 `vercel.json`，Vercel 會把 `site/` 當成靜態輸出目錄。
5. 設定正式網域並確認 HTTPS。
6. 用 Google Search Console 驗證網域。
7. 提交 `https://你的網域.com/sitemap.xml`。
8. 用 `site/robots.txt` 確認爬蟲沒有被封鎖。

## 第五階段：先做流量，再申請廣告

AdSense 申請前至少完成：

- 可正常瀏覽的桌面與手機頁面
- 隱私權、Cookie、聯絡、關於、條款頁
- 原創且有差異化的內容
- 沒有大量空白、重複或無審核 AI 內容
- 沒有誤導性下載、彈窗或假按鈕
- `ads.txt` 與 publisher ID 設定正確
- 有可持續更新的網站

申請後不要購買流量、加入互點群組、要求朋友點廣告，或使用任何「流量交換」服務。這些會造成無效流量與帳號風險。

## 第六階段：廣告版位與收入

上線後至少觀察 2 到 4 週，再決定廣告版位。可以測：

- 文章第一個二級標題後
- 工具列表第 8 到 12 個項目後
- 桌面版側欄
- 長篇文章中段

不要測：

- 蓋住主要按鈕
- 與下載按鈕長得像
- 使用者還沒看到內容就出現的蓋版廣告
- 誤導點擊或自動重新導向

收入要看 RPM、CTR、可見曝光、流量來源與內容主題。短期的 $1 到 $5 不能推論成穩定收入；真正要做的是保留有效內容、刪掉沒有需求的頁面，並每月更新高流量文章。

## 30 天建議節奏

| 時間 | 要做的事 |
|---|---|
| 第 1 天 | 選方向、完成關鍵字驗證、替換 placeholder |
| 第 2 天 | 建立 GitHub 與 Vercel、檢查手機版 |
| 第 3 到 7 天 | 發佈 5 篇真正測過的文章 |
| 第 8 到 14 天 | 發佈到 10 篇，提交 sitemap，修正索引問題 |
| 第 15 到 21 天 | 檢查 Search Console，保留有效主題，刪除重複內容 |
| 第 22 到 30 天 | 申請 AdSense 或補強合規頁，先累積自然流量 |
