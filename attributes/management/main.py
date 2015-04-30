import sys
import os
import mysql.connector
import json
import pandas as pd

"""
The management attribute measures the median number of commits per month
for each repository in the sample of GitHub repositories.

This module uses an init function to generate an in-memory table of medians.
The table is a pandas data frame, which is constructed via an SQL query over
the python MySQL connector. Before this can happen though, frequency tables
must be updated on the MySQL server. See the functions invoked by init() to
get an understanding of the logic that updates the frequency tables.

Author:
    Steven Kroh skk8768@rit.edu

Updated:
    29 April 2015
"""

# Permanent SQL table names
sample_tbl = 'reaper_sample'
freq_tbl_runs = 'reaper_issue_freq_runs'
freq_tbl = 'reaper_issue_freq'


def init(cursor, **options):
    """
    This function initializes the medians data for all projects in the sample
    via a chain of SQL statements and python pandas frame operations. This is
    done beforehand to optimise comunication with the MySQL server.
    """

    # Compute the range of months each sample repository has been active
    range_tbl = create_active_range(cursor)
    # Compute a table with rows representing months of activity in the sample
    calendar = create_calendar(cursor, range_tbl)

    # Create the permanent frequency tables on the server if necessary
    create_freq_tables(cursor)
    # Derive the freqency data for this run of the program
    run = update_freq_tables(cursor, range_tbl, calendar)

    # Compute the median number of issues created per month
    compute_medians(cursor, run)


def run(project_id, repo_path, cursor, **option):
    """
    Selects answers for the management attribute on individual repositories.
    This information comes from the medians data frame in memory. For this
    global table to exist, the init function must have been run first.
    """

    global medians
    median = medians.loc[project_id, 'count']

    attr_threshold = option['threshold']

    attr_pass = (median >= attr_threshold)
    return (attr_pass, median)


def create_calendar(cursor, range_tbl):
    """
    Creates a temporary calendar table by months. Months are included within
    the range of the first repository creation date to the date of last commit.
    Only projects within the sample are considered: this calendar does not
    necessarily apply to all of GitHub.

        That is: Calendar = [ Min(repo creation date) , Max(commit date) ]

    Todo:
        Refactor the stored procedure into python code

    Returns:
        The name of the temporary calendar table
    """

    calendar_tbl = 'reaper_calendar'  # Will be returned
    calendar_proc = 'reaper_fill_calendar'

    # Drop existing calendar table and recreate it
    cursor.execute('''
        DROP TABLE IF EXISTS {cal};
        '''.format(cal=calendar_tbl))

    cursor.execute('''
        CREATE TEMPORARY TABLE {cal}
          (
            id SMALLINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            dt DATETIME NOT NULL
          );
        '''.format(cal=calendar_tbl))

    # Drop existing fill procedure and recreate it
    cursor.execute('''
        DROP PROCEDURE IF EXISTS {proc};
        '''.format(proc=calendar_proc))

    cursor.execute('''
        CREATE PROCEDURE {proc} ()
          BEGIN
          DECLARE dt_cur, dt_last, temp DATETIME;

          -- temp is the minimum repo creation date timestamp
          -- dt_cur is a DATETIME set to the first day of temp's month

          SET temp = (SELECT MIN(first) FROM {range_tbl});
          SET dt_cur = MAKEDATE(YEAR(temp), MONTH(temp));

          -- temp is now the maximum commit date timestamp
          -- dt_cur is a DATETIME set to the first day of temp's month

          SET temp = (SELECT MAX(last) FROM {range_tbl});
          SET dt_last = MAKEDATE(YEAR(temp), MONTH(temp));

          -- Insert months into the calendar within the desired range
          SET dt_last = DATE_ADD(dt_last, INTERVAL 1 MONTH);
          -- SET dt_cur = DATE_SUB(dt_cur, INTERVAL 1 MONTH);
          WHILE dt_cur < dt_last DO
            INSERT INTO {cal} (dt) VALUES (dt_cur);
            SET dt_cur = DATE_ADD(dt_cur, INTERVAL 1 MONTH);
          END WHILE;
        END;
        '''.format(proc=calendar_proc, cal=calendar_tbl, range_tbl=range_tbl))

    # Fill the temporary calendar table
    cursor.execute('CALL {proc} ();'.format(proc=calendar_proc))

    return calendar_tbl


def create_freq_tables(cursor):
    """
    The management attribute requires two permanent tables alongside the
    GHTorrent tables. The first table, reaper_issue_freq_runs, tracks
    individual runs of the management program with timestamps. The second
    table, reaper_issue_freq, contains the actual issue creation data for
    all runs. You can select particular run sets out of this table on the
    'run' foreign key.

    Each row in reaper_isue_freq is associated with a unique row id and run
    number. Within a single run, issue creation counts are bucketed by month
    for each project_id. The month bucketing process supports sparse data, as
    months with no issues created will report a count of 0.

    This function simply creates these tables if they do not yet exist.
    """

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS {tbl_runs}
          (
            id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            timestamp DATETIME NOT NULL
          );
        '''.format(tbl_runs=freq_tbl_runs))

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
        '''.format(tbl=freq_tbl))


def update_freq_tables(cursor, range_tbl, calendar_tbl):
    """
    This function is responsible for selecting the sparse, month-wise, issue
    creation, frequency data into the two permanent management tables.

    First, a new row is added to the runs table. All frequency data to be
    generated at this time will be associated with that run.

    Next, the set of active months (between repo creation and last commit) is
    selected for each project in the sample. In this set, each month row
    represents one fake issue creation event. This is done so each month of
    project existence is reflected in the final result set. We union this data
    with the actual issue data.

    Then, we have to subtract out one issue creation event per month because we
    purposefuly added one fake issue creation event earlier in the process.

    Hack:
        You cannot use a temporary table twice in a single query. So, we
        could not use range_tbl twice. Instead, we use sample_tbl in the
        first part of the query. The tables sample_tbl and range_tbl contain
        duplicate project_id data, which makes this possible.

    Returns:
        The current run number
    """

    # Generate run timestamp. We get the run number via cursor.lastrowid
    cursor.execute(
        '''
        INSERT INTO {tbl_runs} (timestamp) SELECT NOW();
        '''.format(tbl_runs=freq_tbl_runs)
    )
    run = cursor.lastrowid

    cursor.execute(
        '''
        INSERT INTO {freq} (run, project_id, year, month, count)
        SELECT
          {run} AS run,                  -- Current run number
          u.repo_id AS project_id,
          YEAR(u.created_at) AS year,    -- Year as an int
          MONTH(u.created_at) AS month,  -- Month as an int
          COUNT(*) - 1 AS count          -- Decrement because of fake event
        FROM
          (
            (
              SELECT -- Does not include zero issue months

                {sample}.project_id AS repo_id, -- Use of {sample} is a hack
                issues.created_at AS created_at

              FROM {sample} JOIN issues
                ON {sample}.project_id=issues.repo_id
              ORDER BY repo_id, created_at
            )
            UNION ALL -- Include duplicates in union
            (
              SELECT -- One fake issue event per active month per repo

                {range}.project_id AS repo_id,
                {calendar}.dt AS created_at

              FROM {range} CROSS JOIN {calendar}
              WHERE
                (
                  {calendar}.dt > DATE_SUB({range}.first, INTERVAL 1 MONTH) AND
                  {calendar}.dt <= {range}.last
                  -- {calendar}.dt BETWEEN {range}.first AND {range}.last
                )
              ORDER BY repo_id, created_at
            )
          ) AS u
          GROUP BY u.repo_id, year, month
          ORDER BY u.repo_id, year, month;
        '''.format(
            calendar=calendar_tbl, range=range_tbl, sample=sample_tbl,
            freq=freq_tbl, run=run
        )
    )
    return run


def create_active_range(cursor):
    """
    The generation of issue month buckets, including buckets of zero issue
    months, requires us to know the range of project activity on GitHub. This
    function generates this range. The first date of the range is the date
    on which the repository was created on GitHub (inclusive). The second date
    of the range is the date on which the repository's latest commit was
    created (inclusive). Of course, since the GHTorrent data quickly grows
    stale, this commit data is only accurate to the capture date of the
    GHTorrent package.

    Returns:
        The name of the temporary range table
    """

    range_tbl = "reaper_sample_active_range"  # Name of the temp table

    cursor.execute('''
        CREATE TEMPORARY TABLE {range_tbl}
          (
            id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            project_id INT(11) NOT NULL,
            first DATETIME NOT NULL,
            last DATETIME NOT NULL
          );
        '''.format(range_tbl=range_tbl))

    cursor.execute('''
        INSERT INTO {range_tbl} (project_id, first, last)
        SELECT p.project_id, p.first,
          CASE
            WHEN MAX(c.created_at) >= p.first THEN MAX(c.created_at)
            ELSE p.first
          END AS last -- Some repos have last commit date BEFORE creation date
        FROM
          (
            SELECT projects.id AS project_id,
              projects.created_at AS first
            FROM
              {sample_tbl} JOIN projects ON {sample_tbl}.project_id=projects.id
          ) AS p
        JOIN commits as c
          ON p.project_id=c.project_id
        GROUP BY p.project_id;
        '''.format(range_tbl=range_tbl, sample_tbl=sample_tbl))

    return range_tbl


def compute_medians(cursor, run):
    """
    This function computes the median number of commits created per month
    for each repository in the sample. This is done by reading in the
    appropriate query for the most recent run into a python pandas data frame.

    A global variable is created to hold the medians table so that the run
    method may refer to the medians.
    """

    df = pd.read_sql('''
        SELECT project_id, count FROM {freq_tbl} WHERE run={run};
        '''.format(freq_tbl=freq_tbl, run=run), con=cursor._connection)

    global medians
    medians = df.groupby('project_id').median()

if __name__ == '__main__':
    with open('../../config.json', 'r') as file:
        config = json.load(file)

    mysql_config = config['options']['datasource']

    connection = mysql.connector.connect(**mysql_config)
    connection.connect()
    init(connection.cursor())

    global medians
    print(medians)

    attr_options = config['attributes'][6]['options']
    result = run(1536, None, None, threshold=1.0)

    print(result)
