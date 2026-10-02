# AdSense 審查對照表

更新日期：2026-10-02

## 目前狀態

- Publisher ID：`ca-pub-1837836558769995`
- `claire-mu.vercel.app`：正在接受審查
- `ads.txt`：已授權
- Auto Ads：已啟用
- Google CMP：已設定
- Consent Mode：廣告儲存、使用者資料、個人化預設為 denied
- 實際廣告：審查通過後才會開始放送

## 已符合或已處理

| 審查面向 | 目前做法 | 狀態 |
|---|---|---|
| 網站可瀏覽 | 桌面與手機版皆可正常使用 | 已符合 |
| 導覽 | 首頁、目錄、分類、工具頁與指南互相連結 | 已符合 |
| 原創內容 | 已有真實 ChatGPT vs Gemini 實測、完整提示詞、原始回答與截圖 | 部分符合 |
| 內容深度 | 主要指南約 900 到 1,070 英文詞，工具頁有 strengths、limits、pricing note | 部分符合 |
| 隱私權 | 有 Privacy and Cookies 頁，說明 Google Consent Mode 與外部連結 | 已符合基本要求 |
| Cookie 同意 | 使用 Google 認證 CMP，並設定三選項同意訊息 | 已符合 |
| 關於頁 | 有 About、編輯流程與 AI 協作說明 | 已符合基本要求 |
| 聯絡方式 | 有公開 Issue 與私密 Security Advisory 聯絡入口 | 已符合基本要求 |
| 社論政策 | 有 Editorial Policy、Disclosure 與更正流程 | 已符合 |
| 技術 SEO | canonical、robots.txt、sitemap.xml、404 noindex | 已符合 |
| 廣告標示 | 使用 Auto Ads；不再手動插入沒有 slot ID 的廣告 | 已符合 |
| 無效流量 | 沒有購買流量、互點、強制下載或誤導點擊 | 已符合目前狀態 |
| 網站擁有權 | AdSense Ads.txt 驗證成功 | 已符合 |

## 仍可能影響審查的風險

### 1. Google 尚未完整收錄

目前 Search Console 仍可能顯示 sitemap 初次擷取或首頁未收錄。AdSense 和 SEO 是不同系統，但 Google 無法正常辨識網站仍是需要優先處理的技術風險。

處理方式：

- 等 Google 重試 sitemap
- 修復 Search Console 的抓取問題
- 不對審查中的網站持續改動大量結構
- 不使用購買流量或流量交換

### 2. 工具頁原創深度不足

目前 32 個工具頁多數是根據官方資訊與編輯判斷整理，還不是完整的第一手測試。這不一定會直接退件，但大量相似頁面會增加「低價值或大量生成內容」的風險。

處理方式：

- 每週完成 2 到 3 個實測
- 每篇加入截圖、使用時間、修改時間、錯誤與限制
- 優先測已有流量或商業意圖的頁面
- 不以沒有證據的「I tested」描述內容

### 3. 網站還是 Vercel 子網域

`claire-mu.vercel.app` 可以運作，但自訂網域通常更適合長期品牌、廣告主信任與搜尋成長。

處理方式：

- 購買品牌網域
- 更新 canonical、sitemap、Search Console 與 AdSense 網站
- 設定品牌 email

### 4. 聯絡與營運身分較薄

目前沒有公開公司名稱、地址或品牌 email，只有 GitHub Issue 與 Security Advisory。

處理方式：

- 如果有公司或工作室，加入合法名稱
- 若沒有，至少使用網域 email
- 不要在網站公開個人住址或私人電話

### 5. Vercel Hobby 商用限制

Vercel 條款限制 Hobby 為 personal 或 non-commercial use。網站準備接受廣告收入時，應升級 Pro 或改用允許商業用途的主機。

### 6. AdSense 帳戶內有多個網站

目前帳戶中有 11 個網站，包括 10 個 `signalstack-*` 網站。若這些網站不是你建立或不是你控制的，應立即檢查 Google 帳號與 Vercel 專案安全。

## 審查通過前不要做

- 不要一直按「要求複查」
- 不要購買流量或加入互點群組
- 不要要求親友點擊廣告
- 不要把廣告按鈕做得像下載或主要操作
- 不要提交空白頁或只有廣告的頁面
- 不要大量複製其他網站的內容

## 建議的下一階段

1. 讓 Google 完成 sitemap 與首頁收錄
2. 每週新增 2 到 3 篇有截圖與實測的內容
3. 更新既有工具頁，補上第一手觀察
4. 接上自訂網域與品牌 email
5. 在廣告開始放送前處理 Vercel 商業方案
6. 審查結果出現後，再依 `需要處理` 的說明修正，不重複盲目提交
