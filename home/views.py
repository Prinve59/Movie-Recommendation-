from django.shortcuts import render,redirect
import pickle
import requests
# Create your views here.

movie_lst=pickle.load(open("movies.pkl",'rb'))
similarity=pickle.load(open("simil.pkl",'rb'))




def rec(movie):
    movie=(lambda x:x.lower())(movie)
    matches = movie_lst[movie_lst['title'] == movie]
    if matches.empty:
        return ["❌ Movie not found in database"]
    movies_idx= movie_lst[movie_lst['title']==movie].index[0]
    distances=similarity[movies_idx]
    mov_list=list(enumerate(distances))
    rec_m=[]
    for i,sim_sc in mov_list:
        if i==movies_idx:
            continue
        poster_path=movie_lst.iloc[i].posters
        title = movie_lst.iloc[i].title
        rating = movie_lst.iloc[i].rating
        final_sc=sim_sc*(0.7+0.3 * (rating / 10))
        rec_m.append((title,rating, final_sc,poster_path))
    rec_m = sorted(rec_m, key=lambda x: x[2], reverse=True)[:10]
    final_rec = []
    for title, rating, final_sc, poster_path in rec_m:
        final_rec.append((title,poster_path,rating, final_sc))

    return final_rec

def index(request):
    movie = None
    recommendations = []
    if request.method=='POST':
        movie=request.POST.get("movie")
        if movie:
            recommendations= rec(movie)
    if(len(recommendations)==1):
        movie_df=movie_lst['title'].values.tolist()
        return render(request,"index.html",{'movie':movie ,'movie_lst':movie_df}) 
        
    movie_df=movie_lst['title'].values.tolist()
    return render(request,"index.html",{'movie':movie ,'movie_lst':movie_df,'rec_m': recommendations}) 
