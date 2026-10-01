# 實驗 001：用相同任務比較 ChatGPT、Claude、Gemini

## 測試目標

比較三個通用 AI 工具，在「規劃 AI 工具網站內容」這個真實工作上的完成度。

這個測試不需要付費。使用免費方案即可，但要在結果中寫明實際使用的方案。

## 固定任務

請三個工具規劃 7 天內容，每一天都要有：

- primary keyword
- search intent
- article title
- 文章要回答的 3 個問題
- 3 個適合連到的內部頁面
- 需要查證的事實

## 要貼給三個工具的完全相同提示詞

```text
You are helping plan a 7-day editorial sprint for an English-language AI tools directory.

Audience: freelancers, small business owners, and remote teams.
Website pages available:
- ChatGPT, Claude, Gemini, Perplexity, Microsoft Copilot tool reviews
- Coding, Writing and SEO, Productivity, and Business category pages
- Guides about small business, freelancers, remote teams, and SEO writing

Create a 7-day content plan in a table with:
1. Day
2. Primary keyword
3. Search intent
4. Article title
5. Three questions the article must answer
6. Three relevant internal links
7. Facts that need verification

Rules:
- Do not invent search volume.
- Mark uncertain assumptions as [VERIFY].
- Prioritize long-tail topics over broad topics such as "best AI tools".
- Keep each article practical for the named audience.
- Return only the table and a short rationale.
```

## 操作步驟

1. 開啟三個工具的新對話。
2. 同時開始計時。
3. 貼上同一段提示詞。
4. 每個工具最多等待或修改 10 分鐘。
5. 儲存原始回答。
6. 擷取工具名稱、回答與重要限制。
7. 為三個回答評分。
8. 寫下 100 到 200 字的真人觀察。
9. 補上官方來源與測試日期。

## 需要截圖的畫面

- 提示詞輸入畫面
- 工具產生的 7 天表格
- 錯誤、缺漏或需要查證的地方
- 最終評分表

## 發布文章草案

標題：

> We gave ChatGPT, Claude, and Gemini the same AI content-planning task

結構：

1. Why we ran this test
2. The exact prompt
3. How we scored the results
4. ChatGPT result
5. Claude result
6. Gemini result
7. Comparison table
8. What surprised us
9. Which tool to choose
10. Limitations and sources

## 完成後回報格式

```text
實驗 001
ChatGPT：總分 X/10，第一次可用 X 分鐘
Claude：總分 X/10，第一次可用 X 分鐘
Gemini：總分 X/10，第一次可用 X 分鐘
最推薦：
最大缺點：
我的觀察：
截圖位置：
```

## 已完成結果

- 測試日期：2026-10-01
- ChatGPT：8/10，第一次可用時間約 37 秒
- Gemini Flash：6/10，第一次可用時間約 37 秒
- 勝出者：ChatGPT
- 主要原因：ChatGPT 的內部頁面名稱較接近網站實際結構；Gemini 產生多個不存在的路徑。
- 排除工具：Claude 需要登入、Arena AI 需要 reCAPTCHA，兩者都沒有列入分數。
- 發布文章：https://claire-mu.vercel.app/guides/chatgpt-vs-gemini-editorial-plan-test.html
- 原始輸出：content-lab/captures/001-chatgpt-response.txt、content-lab/captures/001-gemini-response.txt
