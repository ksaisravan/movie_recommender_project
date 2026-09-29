# 🎬 Movie Recommender System

A content-based movie recommendation web app built with Python and Streamlit. Pick a movie, get five similar suggestions with posters, and give 👍 / 👎 feedback so movies you dislike stop showing up.

<!-- Add a screenshot or GIF here: ![Demo](demo.png) -->
<!-- Add your live link here: **Live demo:** https://your-app.streamlit.app -->

## ✨ Features

- **Content-based recommendations:** finds movies similar to your selection using cosine similarity over movie metadata
- **Movie posters:** fetched live from the TMDB API, with a placeholder when no poster exists
- **Like / Dislike feedback:** saved to a CSV file; disliked movies are excluded from future recommendations
- **Feedback counter:** shows total likes and dislikes, with a one-click reset
- **Fast lookups:** poster requests are cached to avoid repeat API calls

## 🛠️ Tech Stack

| Area | Tools |
|---|---|
| Language | Python |
| Web app | Streamlit |
| Data handling | Pandas, NumPy |
| ML / NLP | Scikit-learn, NLTK |
| External API | TMDB (The Movie Database) |
| Storage | CSV (feedback), Pickle (model data) |

## ⚙️ How It Works

1. Movie metadata (e.g. genres, keywords, cast, overview) is cleaned and combined into a single text "tag" per movie.
2. The tags are converted to vectors, and a **cosine similarity** matrix is computed between all movies (see the notebook).
3. The matrix and movie list are saved as `similarity.pkl` and `movie_dict.pkl`.
4. When you select a movie, the app looks up its row in the similarity matrix, sorts by score, skips movies you've disliked, and returns the top 5.
5. Posters are fetched from TMDB using each movie's ID.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ksaisravan/movie_recommender_project.git
cd movie_recommender_project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your TMDB API key

Get a free key at [themoviedb.org](https://www.themoviedb.org/settings/api), then create `.streamlit/secrets.toml`:

```toml
TMDB_API_KEY = "your_api_key_here"
```

> ⚠️ Never commit your API key. `.streamlit/secrets.toml` is listed in `.gitignore`.

### 4. Run the app

```bash
streamlit run app.py
```

## 📁 Project Structure

```
movie_recommender_project/
├── app.py              # Streamlit web app
├── movie_dict.pkl      # Movie titles and IDs
├── similarity.pkl      # Precomputed similarity matrix
├── user_feedback.csv   # Created automatically when you like/dislike
├── *.ipynb             # Notebook: data cleaning + similarity computation
├── requirements.txt    # Python dependencies
└── README.md
```

> If `similarity.pkl` is too large for GitHub (100 MB limit), host it via Git LFS or a release and add download instructions here.

## 🔮 Future Improvements

- Per-user feedback instead of one shared CSV
- Recommendations that learn from likes, not only dislikes
- Filters by genre, year, or rating
- Deploy on Streamlit Community Cloud

## 👤 Author

**Killamsetty Sai Sravan**
[GitHub](https://github.com/ksaisravan) 

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
