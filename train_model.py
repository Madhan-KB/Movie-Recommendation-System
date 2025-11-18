
import ast
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def parse_names(x, key='name', top_n=None):
	"""Parse a stringified list of dicts and return joined names."""
	if pd.isna(x):
		return ''
	try:
		items = ast.literal_eval(x)
	except Exception:
		return ''

	names = []
	for i, it in enumerate(items):
		if top_n is not None and i >= top_n:
			break
		name = it.get(key, '') if isinstance(it, dict) else ''
		if isinstance(name, str):
			names.append(name.replace(' ', ''))

	return ' '.join(names)


def get_director(x):
	if pd.isna(x):
		return ''
	try:
		items = ast.literal_eval(x)
	except Exception:
		return ''

	for it in items:
		if isinstance(it, dict) and it.get('job', '').lower() == 'director':
			return it.get('name', '').replace(' ', '')
	return ''


def create_soup(df):
	# combine useful textual features into a single string
	df['genres_parsed'] = df['genres'].apply(lambda x: parse_names(x, key='name'))
	df['keywords_parsed'] = df['keywords'].apply(lambda x: parse_names(x, key='name'))
	df['cast_parsed'] = df['cast'].apply(lambda x: parse_names(x, key='name', top_n=3))
	df['director'] = df['crew'].apply(get_director)

	# overview might be NaN
	df['overview'] = df['overview'].fillna('')

	df['soup'] = (
		df['overview'].astype(str) + ' ' +
		df['genres_parsed'].astype(str) + ' ' +
		df['keywords_parsed'].astype(str) + ' ' +
		df['cast_parsed'].astype(str) + ' ' +
		df['director'].astype(str)
	)

	return df


def build_and_save_model(data_path: Path, credits_path: Path, out_path: Path):
	print(f"Loading movie data from {data_path} and credits from {credits_path}...")
	movies = pd.read_csv(data_path)
	credits = pd.read_csv(credits_path)

	# credits has movie_id column, movies has id
	credits = credits.rename(columns={'movie_id': 'id'})

	# merge
	df = movies.merge(credits, on='id')

	# make sure 'title' present
	if 'title' not in df.columns:
		df['title'] = df['original_title'] if 'original_title' in df.columns else ''

	# create combined text
	df = create_soup(df)

	# Vectorize
	print('Vectorizing text with TF-IDF...')
	tfidf = TfidfVectorizer(stop_words='english')
	tfidf_matrix = tfidf.fit_transform(df['soup'])

	print('Computing cosine similarity... (this may take a while)')
	cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

	# reset index for consistent lookups
	df = df.reset_index(drop=True)

	model_data = {
		'data': df[['id', 'title'] + [c for c in df.columns if c in ('soup', 'overview')]],
		'similarity': cosine_sim
	}

	print(f"Saving model to {out_path}...")
	with open(out_path, 'wb') as f:
		pickle.dump(model_data, f)

	print('Model saved successfully.')


if __name__ == '__main__':
	BASE = Path(__file__).resolve().parent
	movies_csv = BASE / 'tmdb_5000_movies.csv'
	credits_csv = BASE / 'tmdb_5000_credits.csv'
	out_file = BASE / 'model.pkl'

	# basic checks
	if not movies_csv.exists() or not credits_csv.exists():
		print('Required CSV files not found in backend/. Please ensure tmdb_5000_movies.csv and tmdb_5000_credits.csv are present.')
	else:
		build_and_save_model(movies_csv, credits_csv, out_file)
