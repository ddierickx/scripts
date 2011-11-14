@echo off
playgame.py --engine_seed 42 --player_seed 42 --food random --end_wait=0.25 --verbose --log_dir game_logs --turns 30 --map_file maps\maze\maze_1.map  %1 "python ..\MyBot.py" %2 "python ..\MyBot.py"  -e --nolaunch --strict --capture_errors
