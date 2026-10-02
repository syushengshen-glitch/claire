# The exact prompt and response evidence for experiment 002

- Article: https://claire-mu.vercel.app/guides/chatgpt-vs-gemini-javascript-debugging-test.html
- Raw prompt: `content-lab/captures/002-prompt.txt`
- ChatGPT output: `content-lab/captures/002-chatgpt-response.txt`
- Gemini output: `content-lab/captures/002-gemini-response.txt`
- Screenshots: `content-lab/captures/002-chatgpt.png`, `content-lab/captures/002-gemini.png`
- Result: ChatGPT 10/10, Gemini 9/10
- Main difference: ChatGPT returned `null` when no valid amounts existed; Gemini returned `0`, which could conflate unknown data with a real zero.
