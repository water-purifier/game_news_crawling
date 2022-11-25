import os

# 폴더로 이동
# command_line = "ssh funcode@iqiafan.com -p 20022 'cd ~/iqiafan.v2/game_news_next_js/ ; npm run build; pm2 stop 0'"
command_line = "ssh funcode@iqiafan.com -p 20022 'cd ~/iqiafan.v2/game_news_next_js/; source ~/.nvm/nvm.sh ;npm run build; pm2 restart 0'"
os.system(command_line)

# next 명령어 실행