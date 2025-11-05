Discord音樂機器人
一個簡單的 discord.py 音樂機器人。

命令：
目前命令前綴為正斜線字元（$）。

指令:
加入 $join
撥放音樂 $play
加入音樂清單 $queue
暫停 $pause
繼續 $resume
跳過 $skip
離開 $leave

如何克隆並運行它：
該機器人依賴 FFmpeg、、dotenv、PyNaCl 和 discord.py。

這個倉庫包含了運行一個（幾乎）完美運行的 Discord 音樂機器人的原始程式碼。要運行它，需要以下步驟：

下載並安裝 FFmpeg。

根據你使用的作業系統，實現方式會有所不同。
在Windows 系統上
在Linux 系統上
在Mac OS X上
將此倉庫複製到本機資料夾，然後開啟您喜歡的 Python 程式設計 IDE。

設定虛擬環境並使用 pip 安裝以下庫：

python-dotenv
PyNaCl
discord.py
建立一個名為 .env 的檔案並貼上discordToken = 'YOUR_DISCORD_TOKEN_HERE'。

若要取得 Discord 令牌，您需要：
進入Discord 開發者門戶
創建應用程式。
在「機器人」標籤中新增機器人。
請確保選取“伺服器成員意圖”選項。
仍然在“機器人”選項卡上，在機器人圖標的右側，單擊“複製”將令牌複製到剪貼簿。
將其貼到 .env 檔案中。
將機器人加入伺服器：
在您最近建立的應用程式中，開啟「OAuth2」選項卡，向下捲動至「範圍」。
勾選“bot”選項，並複製作用域表下方產生的連結。
將連結貼到瀏覽器中，然後選擇要新增機器人的伺服器。你需要是公會管理員才能執行此操作。
