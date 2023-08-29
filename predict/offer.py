import pandas as pd
import requests

class Offer:
    def __init__(self, job_offer):
        job_offer_api = job_offer.replace("https://justjoin.it/offers/", "https://justjoin.it/api/offers/")
        response = requests.get(job_offer_api)
        job_data = response.json()

        with open('output.txt', 'r') as file:
            lines = file.readlines()
            self.top_20_skills = [line.strip() for line in lines]

        offer_data = []

        for skill in job_data['skills']:
            new_row = job_data.copy()
            new_row['skill_name'] = skill['name']
            new_row['skill_level'] = skill['level']
            offer_data.append(new_row)

        self.offer_df = pd.DataFrame(offer_data)

    def standardize_text(self, df, text_field):
        df[text_field] = df[text_field].str.lower()
        return df

    def remove_blanc(self, value):
        if value == '':
            value = 0
            return value

    def remove_mark(self, value):
        marks = ['>', '<', '-', '+', '_', ' ', '  ', ',']
        for mark in marks:
            if pd.notna(value) and mark in value:
                return value.replace(mark, '')
        return value

    def preprocess(self):
        self.offer_df = self.standardize_text(self.offer_df, "title")
        self.offer_df = self.standardize_text(self.offer_df, "skill_name")

        offer_dummies = pd.DataFrame()

        for col_name in sorted(self.top_20_skills):
            offer_dummies["skill_" + col_name] = 0

        offer_dummies.loc[0] = 0

        final = []
        for skill in self.offer_df['skill_name']:
            new_dummy = offer_dummies.copy()
            if skill in self.top_20_skills:
                new_dummy[f"skill_{skill}"] = 1
            final.append(new_dummy)

        all_dummies = pd.concat(final, ignore_index=True)

        for col in all_dummies.columns:
            all_dummies[col] *= self.offer_df['skill_level']

        aggregated_offer_df = pd.concat([self.offer_df, all_dummies], axis=1)

        def custom_agg(series):
            if series.name.startswith('skill'):
                return series.sum()
            else:
                return series.iat[0]

        aggregated_offer_df = aggregated_offer_df.drop('skill_name', axis=1)
        aggregated_offer_df = aggregated_offer_df.drop('skills', axis=1)

        aggregated_offer_df = aggregated_offer_df.groupby('id', as_index=False).agg(custom_agg)
        aggregated_offer_df = aggregated_offer_df.drop('skill_level', axis=1)

        level_mapping = {'junior': 0, 'mid': 1, 'senior': 2}
        workplace_mapping = {'remote': 0, 'partly_remote': 1, 'office': 2}
        country_mapping = {'PL': 0, 'SK': 1, 'CZ': 2, 'HU': 3, 'AT': 4, 'SI': 5, 'RO': 6, 'MT': 7, 'DE': 8, 'UA': 9, None: 10, 'EE': 11}

        aggregated_offer_df['experience_level'] = aggregated_offer_df['experience_level'].map(level_mapping)
        aggregated_offer_df['workplace_type'] = aggregated_offer_df['workplace_type'].map(workplace_mapping)
        aggregated_offer_df['country_code'] = aggregated_offer_df['country_code'].map(country_mapping)

        offer_employment_types = aggregated_offer_df['employment_types'].apply(pd.Series)
        offer_employment_type = offer_employment_types[0].apply(pd.Series)
        offer_employment_type = pd.concat([offer_employment_type.drop(['salary'], axis=1), offer_employment_type['salary'].apply(pd.Series)], axis=1)

        offer_no_employment = aggregated_offer_df.drop(columns='employment_types')
        offer_employment = pd.concat([offer_no_employment, offer_employment_type], axis=1)

        type_map = {'permanent': 0, 'b2b': 1, 'mandate_contract': 2}
        offer_employment['type'] = offer_employment['type'].map(type_map)

        def standardize_company_size(company_size_value):
            company_size_value = str(company_size_value)
            if (company_size_value == '-' or company_size_value == '' or company_size_value == ' ' or company_size_value == 'None'):
                size = 0.0
            elif '-' in company_size_value:
                min_value, max_value = company_size_value.split('-')
                size = 0.5 * (float(min_value) + float(max_value))
            elif '+' in company_size_value:
                size = float(company_size_value.replace('+', ''))
            elif ' ' in company_size_value:
                size = float(company_size_value.replace(' ', ''))
            else:
                size = float(company_size_value)

            return size

        offer_employment['avg_company_size'] = offer_employment['company_size'].apply(lambda x: standardize_company_size(x))

        self.offer = offer_employment.drop(columns=['id', 'from', 'to', 'currency', 'company_size', 'company_profile', 'apply_body', 'title', 'street', 'city', 'address_text', 'marker_icon', 'company_name', 'company_url', 'latitude', 'longitude', 'apply_url', 'published_at', 'remote_interview', 'video_key', 'video_provider', 'open_to_hire_ukrainians', 'future_consent_title', 'future_consent', 'information_clause', 'custom_consent_title', 'custom_consent', 'tags', 'body', 'company_logo_url', 'banner_url', 'multilocation'])

    def get_processed_offer(self):
        return self.offer


