"""
   IoT demo: Server side components for the Pivotal Data Science Marketplace prototype app for IoT
   Author: Srivatsan Ramanujam <sramanujam@pivotal.io>, 28-May-2015
"""
import os
import json
from flask import Flask, render_template, jsonify, request
from flask.ext.assets import Bundle, Environment
import logging
from dbconnector import DBConnect
from sql.queries import *

#init app
app = Flask(__name__)

#init logger
logging.basicConfig(level= logging.DEBUG if not os.getenv('VCAP_APP_PORT') else logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#init flask assets
bundles = {
    'user_js': Bundle(
           'js/tabulate.js',
           'js/barplot.js',
           'js/lineplot.js',
           'js/selected_acc_Heatmap.js',
           'js/grouped_barplot.js',
           filters='jsmin' if os.getenv('VCAP_APP_PORT') else None, #minify if deploying on CF
           output='gen/user.js',
        ),
    'user_css': Bundle(
           'css/custom.css',
           filters='jsmin' if os.getenv('VCAP_APP_PORT') else None, #minify if deploying on CF
           output='gen/user.css'
        )   
}
assets = Environment(app)
assets.register(bundles)

#Initialize database connection objects
conn = DBConnect(logger)
week_id = 28
selected_acc_id = 7454

def index():
    """
       Render homepage
    """
    return render_template('index.html', title='Lateral Movement demo')

@app.route('/')
@app.route('/home')
def home():
    """
       Homepage
    """
    logger.debug('In home()')
    return render_template('home.html')

@app.route('/about')
def about():
    """
       About page, listing background information about the app
    """
    logger.debug('In about()')
    return render_template('about.html')

@app.route('/contact')
def contact():
    """
       Contact page
    """
    logger.debug('In contact()')
    return render_template('contact.html')
    
@app.route('/settings')
def settings():
    """
       Settings page (for model building)
    """
    logger.debug('In settings()')
    return render_template('settings.html')    

@app.route('/<path:path>')
def static_proxy(path):
    """
       Serving static files
    """
    logger.debug('In static_proxy()')
    return app.send_static_file(path)

@app.route('/_anomalies_weekid/<int:val>')    
def anomalies_weekid(val):
    """
        Select weekid for list of anomalies
    """
    global week_id 
    week_id = val
    print "week_id = ", week_id
    return jsonify(week_id=[{'week_id':week_id}])

@app.route('/_selected_accid/<int:val>')    
def selected_accid(val):
    """
        Select accid for drill down
    """
    global selected_acc_id 
    selected_acc_id = val
    print "week_id = ", selected_acc_id
    return jsonify(selected_acc_id=[{'selected_acc_id':selected_acc_id}])
    
@app.route('/_get_anomalies_weekid')    
def get_anomalies_weekid():
    """
        Return the week_id value
    """
    global week_id 
    print "week_id = ", week_id
    return jsonify(week_id=[{'week_id':week_id}])

@app.route('/_get_selected_accid')    
def get_selected_accid():
    """
        Return the selected_accid value
    """
    global selected_acc_id 
    print "selected_acc_id = ", selected_acc_id
    return jsonify(selected_acc_id=[{'selected_acc_id':selected_acc_id}])
    
@app.route('/_weekid_anomalylist')    
def weekid_anomalylist():
    """
        Populate the table with list of anomalies for a week
    """
    global conn
    global week_id
    print "week_id = ", week_id
    
    INPUT_SCHEMA = 'public'
    INPUT_TABLE = 'anomaly_det_results_table'
    sql = extract_anomaly_list_for_weekid(INPUT_SCHEMA, INPUT_TABLE, week_id)
    logger.info(sql)
    df = conn.fetchDataFrame(sql)
    logger.info('weekid_anomalylist: {0} rows'.format(len(df)))
    return jsonify(hmap=[{'account_name':r['account_name'],'week_id':r['week_id'], 'pca_score':r['pca_score'], 'anomaly_flag':r['anomaly_flag'], 'pca_recom_score':r['pca_recom_score'], 'diff':r['diff'],'pca_score1':r['pca_score1']} for indx, r in df.iterrows()])
    

@app.route('/_anomalytseries_accid')    
def anomalytseries_accid():
    """
        Populate the table with anomaly score tseries for selected acc
    """
    global conn
    global selected_acc_id
    print "selected_acc_id = ", selected_acc_id
    
    INPUT_SCHEMA = 'public'
    INPUT_TABLE = 'anomaly_det_results_table'
    sql = extract_anomaly_tseries_for_accid(INPUT_SCHEMA, INPUT_TABLE, selected_acc_id)
    logger.info(sql)
    df = conn.fetchDataFrame(sql)
    logger.info('anomalytseries_accid: {0} rows'.format(len(df)))
    return jsonify(hmap=[{'week_id':r['week_id'], 'pca_score':r['pca_score'],  'pca_recom_score':r['pca_recom_score'],'account_name':r['account_name']} for indx, r in df.iterrows()])

@app.route('/_heatmap_accid_weekid')    
def heatmap_accid_weekid():
    """
        Populate the table with heatmap data for selected acc and weekid
    """
    global conn
    global selected_acc_id
    print "selected_acc_id = ", selected_acc_id
    global week_id
    print "week_id = ", week_id
    
    INPUT_SCHEMA = 'public'
    INPUT_TABLE = 'syn_dataset_genmodel_3_grp'
    sql = extract_heatmapdata_for_accid_weekid(INPUT_SCHEMA, INPUT_TABLE, selected_acc_id,week_id)
    logger.info(sql)
    df = conn.fetchDataFrame(sql)
    logger.info('heatmap_accid_weekid: {0} rows'.format(len(df)))
    return jsonify(hmap=[{'week_id':r['week_id'], 'server_name':r['server_name'],  'num_days':r['num_days'],'account_name':r['account_name'],'server_id':r['server_id']} for indx, r in df.iterrows()])

def main():
    """
       Start the application
    """
    app_port = int(os.getenv('VCAP_APP_PORT')) if os.getenv('VCAP_APP_PORT') else 9090
    app.run(host='0.0.0.0', debug= True if not os.getenv('VCAP_APP_PORT') else False, port = app_port)
