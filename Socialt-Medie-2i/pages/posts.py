from urllib.parse import quote
import dominate
from dominate.tags import *

from sanic import Sanic
from config import APP_NAME

import pages.userprofile as userprofile
from pages.menu import show_menu
import database.post as post

def show_posts(posts=[], user=None):
    app = Sanic.get_app(APP_NAME)
    doc = dominate.document(title=f'{APP_NAME} | Posts')

    with doc.head:
        link(rel='stylesheet', href=app.url_for('static',
                                                name='static',
                                                filename='style.css'))

    with doc:
        with div (id='top_border'):
            with ul():
                li(a(img(src=app.url_for('static', name='static', filename='images/Profile.png', title="Profil")), href="/profile"))
                input_(type='text', placeholder="  Søg...")
                li(a(img(src=app.url_for('static', name='static', filename='images/logo.png')), href="/"))
        with div (id= 'side_border'):
            img(src=app.url_for('static', name='static', filename='images/menu.png'))
            with ul():
                li(a(img(src=app.url_for('static', name='static', filename='images/main.png', title="Forside")), href="/"))
                li(a(img(src=app.url_for('static', name='static', filename='images/explore.png', title="Opdag")), href="/opdag"))
                li(a(img(src=app.url_for('static', name='static', filename='images/post.png'), title="Post"), href="/upload"))
                li(a(img(src=app.url_for('static', name='static', filename='images/messages.png', title="Beskeder")), href="/beskeder"))
                """img(src=app.url_for('static', name='static', filename='images/Logo.png'))"""
        with div (id= 'post_header'):
            p("")
        with div (id= 'posts'):
            p("")
        with div (cls="empty"):
            p("")
        with div (id= 'stories'):
            img(src=app.url_for('static', name='static', filename='images/stories.png'))
            p("profil")
            img(src=app.url_for('static', name='static', filename='images/stories.png'))
            p("profil")
            img(src=app.url_for('static', name='static', filename='images/stories.png'))
            p("profil")
            img(src=app.url_for('static', name='static', filename='images/stories.png'))
            p("profil")
            img(src=app.url_for('static', name='static', filename='images/stories.png'))
            p("profil")
            img(src=app.url_for('static', name='static', filename='images/stories.png'))
            p("profil")
        with div (id='stories_tag'):
            p("Stories")
            
        if user is not None:
            userprofile.user_profile(user)
        with div(id= "all_posts"):
            for display_post in posts:
                with div(cls="posts"):
                    #h1(display_post.post.title)
                    with div(cls='author'):
                        img(src=app.url_for('static',
                                        name='static',
                                        filename=display_post.author.get_img_path()))
                        a(f'{display_post.author.username}',
                            href=f'/u/{quote(display_post.author.username)}',
                            cls='author_link')
            
                    if isinstance(display_post.post, post.TextPost): # text post
                        with div():
                            lines = filter(bool, display_post.post.contents.splitlines())
                            for par in lines:
                                p(par)
                    else: # image post
                        with div():
                            img(src=app.url_for('static',
                                                name='static',
                                                filename=f'images/posts/{display_post.post.image_path}'))
                        img(src=app.url_for('static', name='static', filename='images/like.png'))
                        img(src=app.url_for('static', name='static', filename='images/comment.png'))
                        img(src=app.url_for('static', name='static', filename='images/save.png'))
                        img(src=app.url_for('static', name='static', filename='images/messages.png'))
                        with div(cls='empty'):
                            p("")
        
    return doc.render()

def create_image_page():
    app = Sanic.get_app(APP_NAME)
    doc = dominate.document(title=f'{APP_NAME} | Upload billede')

    with doc.head:
        link(rel='stylesheet', href=app.url_for('static',
                                                name='static',
                                                filename='style.css'))

    with doc:
        menu_items = [
            ('Forside', '/'),
            ('Log ud', '/logout'),
            ('Upload', '/upload'),
            ('Profil', '/profile')
        ]
        show_menu(menu_items)
        with form(cls='post-form', enctype='multipart/form-data', method='POST', action='/post/image'):
            with div(cls='posts'):
                input_(type='text', cls='title_inp',
                        name='title',
                        placeholder='Indtast titel...')
                input_(type='file', name='image', accept='image/*')
            input_(type='submit', value='Post', cls='button')

        """with form(cls='post-form', method='POST', action='/post/text'):
            with div(cls='post'):
                input_(type='text', cls='title_inp',
                        name='title',
                        placeholder='Indtast titel...')
                textarea(cls='contents_inp',
                            name='contents',
                            placeholder='Indtast tekst...')
            input_(type='submit', value='Post', cls='button')"""

    return doc.render()