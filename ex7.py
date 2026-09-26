# 7. CLUSTERING COM K-MEANS
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

st.title("🎨 Clustering K-Means")

st.sidebar.header("Parâmetros")
n_samples = st.sidebar.slider("Amostras", 100, 1000, 300)
n_clusters = st.sidebar.slider("Número de Clusters", 2, 10, 3)
cluster_std = st.sidebar.slider("Dispersão", 0.5, 3.0, 1.0)

X, y_true = make_blobs(n_samples=n_samples, centers=n_clusters, 
                       cluster_std=cluster_std, random_state=42)

kmeans = KMeans(n_clusters=n_clusters, random_state=42)
y_pred = kmeans.fit_predict(X)
centroids = kmeans.cluster_centers_

fig = go.Figure()

colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

for i in range(n_clusters):
    mask = y_pred == i
    fig.add_trace(go.Scatter(x=X[mask, 0], y=X[mask, 1], mode='markers',
                            name=f'Cluster {i}',
                            marker=dict(size=8, color=colors[i], opacity=0.6)))

fig.add_trace(go.Scatter(x=centroids[:, 0], y=centroids[:, 1], mode='markers',
                        name='Centróides',
                        marker=dict(size=20, symbol='x', color='black', 
                                   line=dict(width=2, color='white'))))

fig.update_layout(title="Clustering K-Means", xaxis_title="Feature 1", yaxis_title="Feature 2")
st.plotly_chart(fig)

st.subheader("Métricas")
inertia = kmeans.inertia_
st.metric("Inércia (Within-cluster sum of squares)", f"{inertia:.2f}")

df_results = pd.DataFrame(X, columns=['Feature_1', 'Feature_2'])
df_results['Cluster'] = y_pred
st.dataframe(df_results.head(20))