# 1. 下載程式碼
```shell
git clone https://github.com/richarddwang/Langchain-Tutorial.git && cd Langchain-Tutorial
```
# 2. 啟動或創建虛擬環境
通常可以用 venv 或其他 package manager，但推薦使用 micromamba
```
micromamba create -n tutorial python=3.10
micromamba activate turorial
```

# 3. 安裝所需套件
```shell
pip install -e ".[tutorial]"
```
`-e` ：editable install。不是從 PyPi 上下載安裝，而是安裝寫在本地目錄的套件，且改動本地目錄的套件的程式碼後就會立即生效，不需重新安裝。在本教學會安裝 `langchain_setup` 這個我寫的輔助套件，並借此套件的 requirements 安裝需要的其他套件。

`.[tutorial]`: 安裝在此目錄下的套件 (`langchain_setup`)，並且額外安裝代號`tutorail`的額外 requirements。詳細可參閱`./setup.py`

# 4. 設定並編輯環境變數檔

在 `Langchain-Tutorial/langchain_setup` 下新增 `.env` 檔如下
```
OPENAI_API_KEY="<請填寫>" # 註冊 OpenAI AP，必須
DEFAULT_OPENAI_LLM_MODEL="text-davinci-003"
DEFAULT_OPENAI_CHAT_MODEL="gpt-3.5-turbo-0613"
LANGCHAIN_ENDPOINT="https://api.langchain.plus"
LANGCHAIN_API_KEY="" # 註冊 LangSmith，可要可不要
```

# 5.  設置完成。

建議可先從 `Modules/1. Chain/1.Models.ipynb` 來測試設置是否成功