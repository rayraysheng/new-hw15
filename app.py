# Import Dependencies
from flask import (Flask, render_template, jsonify, request)
import pandas as pd

app = Flask(__name__)

# Flask routes
@app.route("/")
def home():
    return render_template('index.html')

@app.route('/names')
def get_name_list():
    # Read from the metadata csv file
    bb_metadata_df = pd.read_csv('DataSets/Belly_Button_Biodiversity_Metadata.csv')
    # Make a list out of the sample ids
    names_list = [
        'BB_' + str(bb_metadata_df['SAMPLEID'][i]) \
        for i in range(0, len(bb_metadata_df))
    ]
    return jsonify(names_list)

@app.route('/otu')
def get_otu_list():
    # Read from the otu csv file
    bb_otu_df = pd.read_csv('DataSets/belly_button_biodiversity_otu_id.csv')

    # Make a list out of the otu names
    otu_list = [
        bb_otu_df['lowest_taxonomic_unit_found'][i] \
        for i in range(0, len(bb_otu_df))
    ]
    return jsonify(otu_list)

@app.route('/metadata/<sample>')
def get_metadata(sample):
    # The sample name will be in 'BB_xxx' format
    # Parse sample name to get sample id to match the metadata file
    sample_id = int(sample.strip('BB_'))

    # Load the metadata file and find row by matching sample id
    bb_metadata_df = pd.read_csv('DataSets/Belly_Button_Biodiversity_Metadata.csv')
    target_row = bb_metadata_df.loc[bb_metadata_df['SAMPLEID'] == sample_id]

    metadata_dict = {
        'AGE': int(target_row['AGE'].values[0]),
        'BBTYPE': target_row['BBTYPE'].values[0],
        'ETHNICITY': target_row['ETHNICITY'].values[0],
        'GENDER': target_row['GENDER'].values[0],
        'LOCATION': target_row['LOCATION'].values[0],
        'SAMPLEID': int(target_row['SAMPLEID'].values[0])
    }

    return jsonify(metadata_dict)

@app.route('/wfreq/<sample>')
def get_wfreq(sample):
    # The sample name will be in 'BB_xxx' format
    # Parse sample name to get sample id to match the metadata file
    sample_id = int(sample.strip('BB_'))

    # Load the metadata file and find row by matching sample id
    bb_metadata_df = pd.read_csv('DataSets/Belly_Button_Biodiversity_Metadata.csv')
    target_row = bb_metadata_df.loc[bb_metadata_df['SAMPLEID'] == sample_id]

    wfreq = int(target_row['WFREQ'][0])

    return jsonify(wfreq)

@app.route('/samples/<sample>')
def get_sample_data(sample):
    # Load samples data and narrow down to the target sample
    all_samples_data_df = pd.read_csv('DataSets/belly_button_biodiversity_samples.csv')
    target_sample_df = all_samples_data_df[['otu_id', sample]]

    # Sort the target sample dataframe and reformat
    sorted_target_sample_df = target_sample_df.sort_values(by=[sample], ascending=False)
    sorted_target_sample_df.reset_index(inplace=True, drop=True)
    # Get rid of NaNs
    sorted_target_sample_df.dropna(axis=0, how = 'any', inplace=True)


    # Create the two lists from the dataframe
    otu_ids_list = [
        int(sorted_target_sample_df['otu_id'][i]) \
        for i in range(0, len(sorted_target_sample_df))
    ]

    sample_values_list = [
        int(sorted_target_sample_df[sample][i]) \
        for i in range(0, len(sorted_target_sample_df))
    ]

    return jsonify([
        {
            'otu_ids': otu_ids_list,
            'sample_values': sample_values_list
        }
    ])

if __name__ == "__main__":
    app.run(debug=True)