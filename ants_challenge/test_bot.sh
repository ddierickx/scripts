#!/usr/bin/env sh
./playgame.py --player_seed 42 --end_wait=0.25 --verbose --log_dir game_logs --turns 1000 --map_file maps/maze/maze_08p_01.map "python ../MyBot.py" "python sample_bots/python/GreedyBot.py"
