import pandas as pd
import sqlite3

data_list = ['sample_data/wa3i_sample_data - teacher.csv',
             'sample_data/wa3i_sample_data - assignment.csv',
             'sample_data/wa3i_sample_data - makequestion.csv',
             'sample_data/wa3i_sample_data - selfsolvedata.csv',
             'sample_data/wa3i_sample_data - mark.csv',
             'sample_data/wa3i_sample_data - category.csv',
             'sample_data/wa3i_sample_data - question.csv',
             'sample_data/wa3i_sample_data - studysolvedata.csv',
             'sample_data/wa3i_sample_data - keyword.csv',
             'sample_data/wa3i_sample_data - assignmentquestionrel.csv',
             'sample_data/wa3i_sample_data - solve.csv',
            ]

app_name = "mainpage"

with sqlite3.connect('../wa3i/db.sqlite3') as conn:
    cur = conn.cursor()
    for i in data_list:
        df = pd.read_csv(i, index_col=False)
        query = "insert into %s (%s) values (%s)" % (app_name+"_"+i[31:-4], ', '.join(df.columns), ', '.join(["?" for i in range(len(df.columns))]))
        cur.executemany(query, df.values.tolist())
        conn.commit()
        print(i[31:-4], "table insert를 완료하였습니다.")