import os

TOKEN = ''  # bot token
project_dir = r'/root/telegram_bot/'  # project directory
db_path = os.path.join(project_dir, 'database.db')
DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"

admin_username = ""
admins_id = 
group_id = 

start_status = 0
first_app_qst_status = 1
second_app_qst_status = 2
third_app_qst_status = 3
fourth_app_qst_status = 4
fifth_app_qst_status = 5
sixth_app_qst_status = 6
feed_back_input_status = 7
completed_app_status = 10
examination_app_status = 11
finalized_app_status = 12

broadcast_msg_status = 20
broadcast_msg_zero_status = 0

zoom_zero_status = 0
zoom_date_status = 30
zoom_time_status = 31
zoom_url_status = 32
zoom_topic_status = 33
