import joblib
from sklearn.cluster import KMeans
from preprocessing import load_data, encode_data, scale_features

# Load and encode
df = load_data("data/data.csv")
df = encode_data(df)

X = df.drop("Osteoporosis", axis=1)

# Scale
X_scaled, scaler = scale_features(X)

# Train KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X_scaled)

# Save
joblib.dump(kmeans, "models/kmeans_model.pkl")