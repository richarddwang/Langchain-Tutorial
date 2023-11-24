🚨 **LangChain 及其生態系正處於快速變化期，細節可能會與執筆時有所不同** 🚨

1. [運行環境設置](#1.-運行環境設置)
2. [Overview](#2.-Overview)
3. [參考學習順序](#3.-參考學習順序)
4. [觀看/執行說明](#4.-觀看/執行說明)
5. [langchain_setup 說明](#5.-langchain_setup-說明)
6. [本教學相對 Langchain 官方文件的價值](#6.-本教學相對-Langchain-官方文件的價值)
7. [參考資料](#7.-參考資料)

# 1. 運行環境設置

我司組內使用設置，請切換到 `business` branch 後，參閱 [在組內設置](SETUP_BUSINESS.md)

私人環境使用設置，請參閱 [在私人環境設置](SETUP_PUBLIC.md)

# 2. Overview
**Modules** 目錄：解釋構成 Langchain 的各個元件、概念、語法等等
```
Modules
├── 0. Utility
│   ├── LangSmith.ipynb
│   └── utilities.ipynb
├── 1. Chain
│   ├── 1. Models.ipynb
│   ├── 2. Input - Prompts.ipynb
│   ├── 3. Output - Formatting.ipynb
│   └── 4. Langchain Expression Language.ipynb
├── 2. Data
│   ├── 1. Data Loading.ipynb
│   ├── 2. Data Preprocessing.ipynb
│   ├── 3. Vector Store.ipynb
│   ├── 4. Retriever.ipynb
│   ├── 5. Advanced Retrieval.ipynb
│   └── 6. Multiple Documents Processing.ipynb
├── 3. Agent
│   └── ReAct.ipynb
├── 4. Evaluation（施工中）
│   └── Criterion Evaluators.ipynb
```
**Use cases** 目錄：實際展示如何利用 Langchain 快速做出應用
```
Use cases
├── 1. Chatbot.ipynb
├── 2. SQL QA.ipynb
├── 3. Summarization.ipynb
├── 4. Evaluation.ipynb
└── 5. AutoGPT.ipynb
```

# 3. 參考學習順序
`[1. Chain] -> [1. Chatbot] + [LangSmith#Tracking] -> [2. Data/1~4] -> [3. Agent/ReAct] -> [5. AutoGPT] -> [2. Data/6.Multiple Documents Processing] -> [3. Summarization] -> ...`

# 4. 觀看/執行說明

- 觀看說明：每個概念都會嘗試用以下的步驟說明
   1. 動機 (Motivation)
   2. 實際演示 (Demonstration)
   3. 解釋背後的原理 (Implementation)
   4. 如何客製化 (Customization)

- 程式碼執行說明：
   - 每次 `import` 到下一次 `import` 前是為可獨立執行的區塊
   - 每個區塊都建議需從區塊的開始一個個執行，❗跳著執行可能出錯❗。

# 5. langchain_setup 說明

langchain_setup 是我寫的小套件，發揮了以下的作用

❗必須要先 import 這個套件才能使用 OpenAI API 和 LangSmith❗，因為這個套件會幫你自動讀取需要的環境變數。當然你在其他地方可以自己設定需要的環境變數不一定要用這個套件。

在這裡使用 `from langchain_setup import ChatOpenAI, OpenAI` 的原因是，其會依自動依照環境變數的設置，選擇使用 `langchain.chat_models.AzureChatOpenAI` (公司用) 或 `langchain.chat_models.ChatOpenAI` (私人用)，對筆者來說很方便。

除此之外還有許多便利的小功能，如漂亮地秀出一連串的文件，檢視 vector store 內的資料等等。

除了在本教學內使用，有需要的話也可以在其他地方使用喔
```
cd Langchain-Tutorial
pip install -e .
```
或
```
pip install git+https://github.com/richarddwang/Langchain-Tutorial.git
```

# 6. 本教學相對 Langchain 官方文件的價值
雖然 Langchain 官方文件是最精準和最新的說明文件，但是範例都比較偏 API Reference，會展示如何做到但是不會詳細講背後的流程。本教學則旨在實際檢視運行的步驟，讓學習者由淺入深通徹地了解整體。

筆者花了心思將各種概念和工具分類整理成一個架構，讓學習者能透過比較系統性的觀點了解 Langchain 甚至是整個生態系

本教學是可以執行的教學，學習者可以實際動手操作，達成即學即可用的效果。

本教學以中文撰寫，對英文看沒有那麼快的學習者友善。

# 7. 參考資料

## 7.1 文件
[Langchain Python Documentation](https://python.langchain.com/docs)

[LangSmith Documentation](https://docs.smith.langchain.com/)

[Langsmith-cookbook](https://github.com/langchain-ai/langsmith-cookbook/tree/main)

## 7.2 新知
[Langchain Blogs](https://blog.langchain.dev/)：新應用/新技術、使用教學、Langchain 官方公告、其他公司刊登的應用心得分享或合作業配文。推薦訂閱。

[Langchain Discord](https://discord.gg/8ezkMXtR): #share_your_work 裡有時候可以看到一些很猛的應用

## 7.3 課程

[Deeplearning.ai - Short Courses](https://www.deeplearning.ai/short-courses/): 由大老 Andrew Ng 和 Langchain 創辦人 Harrison Chase 合作推出的入門課程，很多都是免費的






