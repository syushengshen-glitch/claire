# Small Ops Lab 上線與 AdSense 計畫

更新日期：2026-10-12

## 定位

Small Ops Lab 是給自由工作者與小型工作室的營運刊物，處理客戶開發、報價與合約、收款、專案交付、自動化與 SOP。

選擇這個題材的原因：

- 廣告主友善，不是醫療、投資或高風險 YMYL 主題。
- 可以產出真正的工具與模板，不只是產品介紹。
- 內容有清楚的搜尋意圖與商業需求。
- 可以逐步累積原創案例、計算器與可下載資源。

## 目前內容

- 5 個分類
- 15 篇原創指南
- 15 個模板或計算器頁面
- 其中 5 個是瀏覽器端互動工具
- 分類頁、指南索引、工具索引、About、Contact、Privacy、Terms、Disclosure、Editorial Policy
- sitemap、robots、ads.txt、vercel.json、404

## 廣告位

- 每篇文章與工具頁都有 inline 與 rail 廣告位。
- 分類與索引頁有 wide 廣告位。
- 廣告位目前只顯示 Advertisement 標籤。
- AdSense 核准後可維持 Auto Ads，或把預留位置換成正式廣告單元。
- 使用同一個 publisher ID：`ca-pub-1837836558769995`。

## 部署

- 網站目錄：`sites/small-ops-lab`
- Vercel Root Directory：`sites/small-ops-lab`
- 目標網域：`https://small-ops-lab.vercel.app/`

## 驗證

- 內部連結：1,082 條，0 條死連結
- 桌面與手機版瀏覽器測試通過
- 互動工具測試：quote builder、SOP builder 通過
- 所有頁面沒有 console error 或水平溢出

## 發布前仍需確認

- Vercel 專案建立與部署狀態
- AdSense 網站擁有權與 ads.txt
- Auto Ads 開啟
- Google Search Console 收錄與 sitemap
- 後續每週新增真實案例、截圖或使用者回饋
