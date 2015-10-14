
"""
Collection of SQL snippets used in lateral movement detection.
Oct-2015: Regunathan Radhakrishnan <rradhakrishnan@pivotal.io> - SQL snippets for lateral movement

"""

    


    

def extract_anomaly_list_for_weekid(input_schema,input_table,week_id):
    """
        Inputs:
        =======
        input_schema (str): The schema containing the input table
        input_table (str): The table in the input_schema containing data for list of anomalies per week
        Outputs:
        ========
        A sql code block        
    """
    sql = """
    select *,
           pca_score/(max(pca_score) over()) as pca_score1
    from
    (
        select 
             *
        from
            {input_schema}.{input_table}
        where
             week_id = {week_id}
        order by pca_score desc limit 25
    ) as foo order by pca_score1 desc
    """.format(input_schema=input_schema,
               input_table=input_table,
               week_id=week_id)
    return sql

def extract_anomaly_tseries_for_accid(input_schema,input_table,selected_accid):
    """
        Inputs:
        =======
        input_schema (str): The schema containing the input table
        input_table (str): The table in the input_schema containing data for list of anomalies per week
        Outputs:
        ========
        A sql code block        
    """
    sql = """
    
        select 
             week_id,
             pca_score,
             pca_recom_score,
             account_name
        from
            {input_schema}.{input_table}
        where
             account_name = {selected_accid}
        order by week_id
    
    """.format(input_schema=input_schema,
               input_table=input_table,
               selected_accid=selected_accid)
    return sql

def extract_heatmapdata_for_accid_weekid(input_schema,input_table,selected_accid,week_id):
    """
        Inputs:
        =======
        input_schema (str): The schema containing the input table
        input_table (str): The table in the input_schema containing data for heatmap data
        Outputs:
        ========
        A sql code block        
    """
    sql = """
        select
              t1.*,
              t2.server_id
        from
        (
            select 
                 week_id,
                 server_name::int,
                 num_days,
                 account_name
            from
                {input_schema}.{input_table}
            where
                 account_name = {selected_accid}
            and
                 week_id <= {week_id}
            order by week_id
        ) t1
        inner join
        (
            select
                   server_name,
                   row_number() over(order by server_name) as server_id
            from
            (
                select 
                     week_id,
                     server_name::int,
                     num_days,
                     account_name
                from
                    {input_schema}.{input_table}
                where
                     account_name = {selected_accid}
                and
                     week_id <= {week_id}
                order by week_id
            ) as foo group by server_name order by 1
        ) t2
        on (t1.server_name=t2.server_name)
        order by server_name
    """.format(input_schema=input_schema,
               input_table=input_table,
               selected_accid=selected_accid,
               week_id=week_id)
    return sql

    
    
    
    
    
    
    
    
    
    
    
    