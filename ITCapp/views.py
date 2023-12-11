import pickle
import pandas as pd
import requests

from django.shortcuts import render
from .forms import MyForms

# Create your views here.
from .models import *


def login(request):
    form = MyForms(request.POST)
    if request.method == "POST":
        if request.POST['login']:
            un = request.POST['username']
            pw = request.POST['password']
            if form.is_valid():
                try:
                    record = AppUser.objects.get(username=un)
                    record_pw = record.password
                    print("DB password:", record_pw)
                    print("Given password:", pw)

                    if record_pw == pw:
                        print("passwords match")
                        return render(request, "home.html")

                    else:
                        print("Incorrect Password")
                        incorrect_password = 'Incorrect Password!!'
                        context = {
                            'incorrect_password': incorrect_password,
                            'form': form
                        }
                        return render(request, "login.html", context)

                except:
                    print("User not found")
                    user_not_found = 'User not found!!'
                    context = {
                        'user_not_found': user_not_found,
                        'form': form
                    }
                    return render(request, "login.html", context)

            else:
                print("Invalid captcha!!")
                incorrect_captcha = 'Incorrect Captcha!!'
                context = {
                    'un': un,
                    'pw': pw,
                    'incorrect_captcha': incorrect_captcha,
                    'form': form
                }
                return render(request, "login.html", context)
    else:
        context = {
            'form': form
        }
        return render(request, 'login.html', context)


def register(request):
    if request.method == "POST":
        if request.POST['register']:
            nm = request.POST['name']
            email = request.POST['email']
            un = request.POST['username']
            pw = request.POST['password']
            cty = request.POST['country']
            age = request.POST['age']

            try:
                newuser = AppUser(name=nm, email=email, username=un, password=pw, country=cty, age=age)
                newuser.save()
                form = MyForms(request.POST)
                context = {
                    'form': form
                }
                return render(request, "login.html", context)

            except:
                err = "Username already taken! Please enter another username"
                context = {
                    'err': err,
                    'nm': nm,
                    'email': email,
                    'pw': pw,
                    'cty': cty,
                    'age': age
                }
                return render(request, 'register.html', context)

    return render(request, "register.html")


def home(request):
    return render(request, 'home.html')


main_dict = pickle.load(open('main.pkl', 'rb'))
main = pd.DataFrame(main_dict)
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


def search(request):
    if request.method == "POST":
        if request.POST['search']:
            try:
                print("Entered try")
                searched_movie = request.POST['search_mov']
                print(searched_movie)
                genre, movie_id, keywords, summary, name, cast, director = search_movies(searched_movie)
                print("Got movie")
                context = {
                    'genre': genre, 'keywords': keywords, 'summary': summary, 'name': name, 'cast': cast, 'director': director,
                    'searched_movie': searched_movie
                }
                return render(request, "search.html", context)

            except:
                print("Movie Not Found")
                error = "Movie Not Found"
                context = {
                    'error': error
                }
                return render(request, "search.html", context)
    return render(request, "search.html")


def search_movies(movie):
    if not main[main['title'] == movie].empty:
        info = []
        movie_index = main[main['title'] == movie].index[0]
        for x in range(7):
            info.append(main.iloc[movie_index][x])
        return info


def about(request):
    return render(request, "about.html")


def update(request):
    return -1


def recommend(request):
    if request.method == "POST":
        if request.POST["recommend"]:
            print("recommend")
            searched_movie = request.POST['movie_name']
            try:
                names, posters = rec_movie(searched_movie)
                print("Names: ", type(names))
                print("Posters: ", type(posters))
                movie_data = [{'name': movie, 'poster': poster} for movie, poster in zip(names, posters)]

                return render(request, 'recommend.html', {'movie_data': movie_data, 'movie': searched_movie})

            except:
                error = "Movie not found!! Search for another movie"
                return render(request, 'recommend.html', {'error': error})
    return render(request, 'recommend.html')


def rec_movie(movie):
    if movies[movies['title'] == movie].index[0]:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:7]

        recommended_movies = []
        recommended_movies_posters = []

        for i in movies_list:
            movie_id = movies.iloc[i[0]].id

            recommended_movies.append(movies.iloc[i[0]].title)
            # fetch poster from API
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters
    else:
        return "Search for another movie!!"


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=e4e0607c358028b0453af0285f1ad46f&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
