from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def display_table():
    # Read the Excel file
    file_path = 'main_data/influencer_avg_data/clean_data.xlsx'
    df = pd.read_excel(file_path)

    # Set the image column and base path
    image_column = 'image_path'  # Replace with your column name
    df['image'] = df[image_column].apply(lambda x: os.path.join('static/unique_faces', os.path.basename(x)))

    # Create HTML for images
    df['Image'] = df['image'].apply(lambda x: f'<img src="{x}" width="100" height="100">')
    
    df.drop(columns = ['image'] , inplace = True)
    
    # Convert DataFrame to HTML
    table_html = df.to_html(escape=False, index=False)
    
    # Render the table
    return render_template('table.html', table_html=table_html)

if __name__ == '__main__':
    app.run(debug=True)
