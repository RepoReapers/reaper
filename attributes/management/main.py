import sys
import os
import mysql.connector
import json
import pprint
from numpy import *
import pandas as pd

def create_calendar(cursor, range_tbl):
    cal_tbl = 'reaper_calendar'
    cal_prc = 'reaper_fill_calendar'

    query = '''
      DROP TABLE IF EXISTS {cal};
      CREATE TEMPORARY TABLE {cal}    
        (    
          id SMALLINT NOT NULL PRIMARY KEY AUTO_INCREMENT,    
          dt DATETIME NOT NULL    
        ); 
      DROP PROCEDURE IF EXISTS {prc};    
      CREATE PROCEDURE {prc} ()    
        BEGIN    
        DECLARE dt_cur, dt_last, temp DATETIME;

        SET temp = (SELECT MIN(first) FROM {rng});  
        SET dt_cur = MAKEDATE(YEAR(temp), MONTH(temp));      
  
        SET temp = (SELECT MAX(last) FROM {rng});    
        SET dt_last = MAKEDATE(YEAR(temp), MONTH(temp));

        SET dt_cur = DATE_SUB(dt_cur, INTERVAL 1 MONTH);    
        WHILE dt_cur <= dt_last DO    
          INSERT INTO {cal} (dt) VALUES (dt_cur);    
          SET dt_cur = DATE_ADD(dt_cur, INTERVAL 1 MONTH);    
        END WHILE;
      END;   

      CALL {prc} ();
    '''.format(prc=cal_prc, cal=cal_tbl, rng=range_tbl) 
     
    for result in cursor.execute(query, multi=True):
        if result.with_rows:
            pass

    return cal_tbl

def create_freq_tables(cursor):
    freq_tbl_runs = 'reaper_issue_freq_runs'
    freq_tbl = 'reaper_issue_freq'

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS {tbl_runs}
          (
            id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            timestamp DATETIME NOT NULL
          );
        '''.format(tbl_runs=freq_tbl_runs)
    )
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS {tbl}
          (
            id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            run INT NOT NULL,
            project_id INT(11) NOT NULL,
            year SMALLINT,
            month TINYINT,
            count SMALLINT
          );
        '''.format(tbl=freq_tbl)
    )

def update_freq_tables(cursor, range_tbl, cal_tbl):
    freq_tbl_runs = 'reaper_issue_freq_runs'
    freq_tbl = 'reaper_issue_freq'

    sample_tbl = 'reaper_insample'

    cursor.execute('''
        INSERT INTO {tbl_runs} (timestamp) SELECT NOW();
        '''.format(tbl_runs=freq_tbl_runs)
    )
    run = cursor.lastrowid 

    cursor.execute('''
        INSERT INTO {tbl} (run, project_id, year, month, count)
        SELECT 
          {run} AS run,
          u.repo_id AS project_id,
          YEAR(u.created_at) AS year,
          MONTH(u.created_at) AS month,
          COUNT(*) - 1 AS count
        FROM
          (
            (
              SELECT 
                {smp}.project_id AS repo_id,
                issues.created_at AS created_at
              FROM {smp} JOIN issues
                ON {smp}.project_id=issues.repo_id
              ORDER BY repo_id, created_at
            )
            UNION ALL
            (
              SELECT
                {rng}.project_id AS repo_id,
                {cal}.dt AS created_at
              FROM {rng} CROSS JOIN {cal}
              WHERE
                ( 
                  {cal}.dt BETWEEN {rng}.first AND {rng}.last
                )
              ORDER BY repo_id, created_at 
            )
          ) AS u
          GROUP BY u.repo_id, year, month
          ORDER BY u.repo_id, year, month;
        '''.format(cal=cal_tbl, rng=range_tbl, smp=sample_tbl, tbl=freq_tbl, run=run)

    )
    return run

def init(cursor, **options):
    sample_tbl = 'reaper_insample'
    range_tbl = 'reaper_sample_active_range'
    schema = '''
      ( 
        id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        project_id INT(11) NOT NULL,
        first DATETIME,
        last DATETIME
      )
    '''
    query = 'CREATE TEMPORARY TABLE {} {};'.format(range_tbl, schema)
    cursor.execute(query)
    query = '''
      INSERT INTO {0} (project_id, first, last)
        SELECT p.project_id,
          p.first,
          MAX(c.created_at) AS last
        FROM 
          (
            SELECT projects.id AS project_id,
              projects.created_at AS first
            FROM
              {1} JOIN projects
              ON {1}.project_id=projects.id
          ) AS p
        JOIN commits as c
          ON p.project_id=c.project_id
        GROUP BY p.project_id;
    '''.format(range_tbl, sample_tbl)
    cursor.execute(query)

    cal_tbl = create_calendar(cursor, range_tbl)

    create_freq_tables(cursor)
    run = update_freq_tables(cursor, range_tbl, cal_tbl)

    df = pd.read_sql('''
        SELECT project_id, count
        FROM {} WHERE run={};
        '''.format("reaper_issue_freq", run),
        con=cursor._connection) 

    global medians
    medians = df.groupby('project_id').median()

def run(project_id, repo_path, cursor, **option):
    global medians
    return df.loc[project_id, 'count']

if __name__ == '__main__':
    #print("Attribute plugins are not meant to be executed directly.")

    with open('../../config.json', 'r') as file:
        config = json.load(file)['options']['datasource']

    connection = mysql.connector.connect(**config)
    connection.connect()                           
    init(connection.cursor())
