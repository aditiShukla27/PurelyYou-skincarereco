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

cleanser_df = read_skincare_data(cleanser_path)
toner_df = read_skincare_data(toners_path)
serums_df = read_skincare_data(serums_path)
moisturizers_df = read_skincare_data(moisturizers_path)

def filter_by_feature(df, feature):
    return df[df['Features'].apply(lambda x: feature in x)]

def filter_out_features(df, features_to_exclude):
    return df[df['Features'].apply(lambda x: not any(feature in x for feature in features_to_exclude))]

@app.route('/')
def right_sidebar():
    return render_template('right-sidebar.html')

@app.route('/filter', methods=['GET','POST'])
def filter():
    if request.method == "POST":
        skin_type = request.form.get('skin-type')
        weather = request.form.get('weather')
        skin_goals = request.form.getlist('skin-goals')
        sensitivity = request.form.get('sensitivity')
        acne = request.form.get('acne')
        uv_protection = request.form.get('uv')
        parabens = request.form.get('paraben')
        allergies = request.form.get('allergies')

        include = []
        exclude = []

        if skin_type and skin_type == 'Good for Dry Skin':
            include.append('Good for Dry Skin')
            exclude.append('Bad for Dry Skin')
        if skin_type and skin_type == 'Good for Oily Skin':
            include.append('Good for Oily Skin')
            exclude.append('Bad for Oily Skin')

        if acne and acne == 'severe':
            include.append('Promotes Wound Healing')
            include.append('Acne-Fighting')
        if acne and acne == 'Fungal Acne Trigger':
            exclude.append('Fungal Acne Trigger')

        if uv_protection and uv_protection == 'UV Protection':
            include.append('UV Protection')

        if parabens and parabens == 'no paraben':
            exclude.append('Paraben')

        if allergies and allergies == 'Allergens':
            exclude.append('Allergens')

        if skin_goals:
            include.append(skin_goals)
        
        filter_by_clean = filter_by_feature(cleanser_df, include)
        filter_out_clean = filter_out_features(cleanser_df, exclude)

        filter_by_toner = filter_by_feature(toner_df, include)
        filter_out_toner = filter_out_features(toner_df, exclude)

        filter_by_serum = filter_by_feature(serums_df, include)
        filter_out_serum = filter_out_features(serums_df, exclude)

        filter_by_cream = filter_by_feature(moisturizers_df, include)
        filter_out_cream = filter_out_features(moisturizers_df, exclude)

        

        


if(__name__ == 'main'):
    app.run()