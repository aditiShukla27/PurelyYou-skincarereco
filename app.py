from flask import Flask, request, render_template, jsonify
import pandas as pd

app = Flask(__name__)

def read_skincare_data(file_path):
    products = []
    features = []
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip().strip('[],')
            
            if '", [' in line:
                product, feature_list = line.split('", [', 1)
                
                product = product.strip('["')
                
                feature_list = feature_list.strip('[]')
                feature_list = feature_list.replace("'", "").split(', ')
                
                products.append(product)
                features.append(feature_list)
    df = pd.DataFrame({'Product': products, 'Features': features})
    
    return df

cleanser_path = "cleansers.txt"
serums_path = "serums.txt"
moisturizers_path = "moisturizers.txt"
toners_path = "toners.txt"

def filter_by_feature(df, feature):
    return df[df['Features'].apply(lambda x: feature in x)]

def filter_out_features(df, features_to_exclude):
    return df[df['Features'].apply(lambda x: not any(feature in x for feature in features_to_exclude))]

@app.route('/')
def index():
    return render_template('right-sidebar.html')

@app.route('/filter', methods=['POST'])
def filter_data():
    all_features = request.form.getlist('features')
    print(all_features)
    #file_path = 'cleansers.txt'
   # df = read_skincare_data(file_path)
    #filtered_df = filter_by_feature(all_features)
    #result_html = filtered_df.to_html()
    
    #return result_html
index()
filter_data()

