import sqlite3


def create(conn):
    sql_create = '''
    CREATE TABLE `sv_battle_data` (
        `id` INTEGER NOT NULL PRIMARY KEY UNIQUE,       
        `date`  TEXT UNIQUE,
        `forest_play` TEXT,
        `forest_win` TEXT,      
        `sword_play` TEXT,
        `sword_win` TEXT,                
        `dragon_play` TEXT,      
        `dragon_win` TEXT,    
        `shadow_play` TEXT,      
        `shadow_win` TEXT,                                
        `rune_play` TEXT,      
        `rune_win` TEXT,           
        `blood_play` TEXT,      
        `blood_win` TEXT,       
        `haven_play` TEXT,      
        `haven_win` TEXT                           
    )
    '''
    conn.execute(sql_create)
    print('创建成功')

def save_data(conn, data_lists, date,):
    sql_insert = '''
    INSERT INTO
        `sv_battle_data`(`date`, 
                         `forest_play`, `forest_win`, 
                         `sword_play`, `sword_win`, 
                         `dragon_play`, `dragon_win`,
                         `shadow_play`, `shadow_win`, 
                         `rune_play`,  `rune_win`,           
                         `blood_play`, `blood_win`,     
                         `haven_play`, `haven_win`)
    VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''
    conn.execute(sql_insert, (date,
                              data_lists[0][0], data_lists[0][1],
                              data_lists[1][0], data_lists[1][1],
                              data_lists[2][0], data_lists[2][1],
                              data_lists[3][0], data_lists[3][1],
                              data_lists[4][0], data_lists[4][1],
                              data_lists[5][0], data_lists[5][1],
                              data_lists[6][0], data_lists[6][1]))