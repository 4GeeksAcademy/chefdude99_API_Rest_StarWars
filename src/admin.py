import os
from flask_admin import Admin
from models import db, User, Characters, Starships, Planets, Fav_character, Fav_starship, Fav_planet
from flask_admin.contrib.sqla import ModelView

class UserModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list = ['id', 'name', 'lastname', 'email', 'characters_favorites', 'starships_favorites', 'planets_favorites']

class CharactersModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list = ['id', 'name', 'height', 'favorites']

class StarshipsModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list = ['id', 'name', 'size', 'seats', 'favorites']

class PlanetsModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list = ['id', 'name', 'number', 'favorites']

class Fav_characterModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list = ['id', 'user_id', 'character_id', 'user', 'character']

class Fav_starshipModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list = ['id', 'user_id', 'starship_id', 'user', 'starship']

class Fav_planetModelView(ModelView):
    column_auto_select_related = True  # Carga automáticamente las relaciones
    # Columnas y relationships de mi tabla PeopleFavorites
    column_list = ['id', 'user_id', 'planet_id', 'user', 'planet']


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='API StarWars', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(CharactersModelView(Characters, db.session))
    admin.add_view(StarshipsModelView(Starships, db.session))
    admin.add_view(PlanetsModelView(Planets, db.session))
    admin.add_view(Fav_characterModelView(Fav_character, db.session))
    admin.add_view(Fav_starshipModelView(Fav_starship, db.session))
    admin.add_view(Fav_planetModelView(Fav_planet, db.session))

# You can duplicate that line to add mew models
# admin.add_view(ModelView(YourModelName, db.session))
