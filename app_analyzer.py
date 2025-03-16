import json
import functions

import seaborn as sea
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_cosine_similarity(ppaf_edata, gp_edata):

    # Create a TfidfVectorizer to vectorize the text
    vectorizer = TfidfVectorizer(stop_words='english')

    # Transform the texts into TF-IDF vectors
    tfidf_matrix = vectorizer.fit_transform([ppaf_edata, gp_edata])

    # Calculate the cosine similarity between the two vectors
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return cosine_sim[0][0]


def merge_sections(data): # specifically for the googleplay apps, data safety page had nested categories
    if isinstance(data, str):
        return data # return empty string is no key found

    finalstring = ""
    for key, value in data.items():
        if isinstance(value, dict): # since the 1k_apps_data.json has many nested dictionaries, recursively loop to
            # connect them all
            finalstring += merge_sections(value)
        else:
            finalstring += merge_sections(value) + " "
    # print(finalstring)
    return finalstring.strip()


def compare_apps(ppaf, gplay):
    with open(ppaf, 'r') as f1, open(gplay, 'r') as f2:
        ppaf_data = json.load(f1)
        gp_data = json.load(f2)
    # load both json files, data safety scraped and ppaf scarped

    app_sim = {}  # to store cosine similarity results
    count = 0;

    for app_id in ppaf_data:
        if app_id in gp_data:
            print(f"Finding similarities in {app_id}")
            count += 1
            cos_sim = {}

            ppaf_data_shared = ppaf_data[app_id].get('Data Shared', '')
            gp_data_shared = merge_sections(gp_data[app_id].get('Data shared', ''))

            ppaf_data_coll = ppaf_data[app_id].get('Data Collected', '')
            gp_data_coll = merge_sections(gp_data[app_id].get('Data collected', ''))

            ppaf_security = ppaf_data[app_id].get('Security Practices', '')
            gp_security = merge_sections(gp_data[app_id].get('Security practices', ''))

            cos_sim['Data shared'] = calculate_cosine_similarity(ppaf_data_shared, gp_data_shared)
            cos_sim['Data collected'] = calculate_cosine_similarity(ppaf_data_coll, gp_data_coll)
            cos_sim['Security practices'] = calculate_cosine_similarity(ppaf_security, gp_security)

            app_sim[app_id] = cos_sim

        else:
            app_sim[app_id] = "Not yet in file."
    print(count)
    functions.save_as_json(app_sim, 'data/policy_similarities.json')


def heatmap(simfile):
    with open(simfile, 'r') as f1:
        data = json.load(f1)

    cosine_data = {}

    for app_id, sections in data.items():
        print(f"getting data for {app_id}")
        cosine_data[app_id] = [
            sections.get("Data shared", 0.0),
            sections.get("Data collected", 0.0),
            sections.get("Security practices", 0.0)
        ]
    df = pd.DataFrame(cosine_data, index=["Data shared", "Data collected", "Security practices"])

    plt.figure(figsize=(27, 10))
    sea.heatmap(df, annot=False, cmap="Oranges", cbar=True)
    plt.title('Cosine Similarity Heatmap')
    plt.xlabel('Applications')
    plt.ylabel('Sections')
    plt.show()


def main():
    # create polciy_similarities to populate heat map
    # compare_apps('ppaf_data.json', '1k_apps_data_safety.json')

    # create heatmap
    heatmap('policy_similarities.json')


if __name__ == '__main__':
    main()
