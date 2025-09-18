from flask import Blueprint, render_template, redirect, url_for, flash
from app.models import Articles
from app.scraping.scrap_euronews import euronews_scrap
from app.scraping.scrap_repubblica import repubblica_scrap
from datetime import datetime
from app import db
import numpy as np
import pandas as pd

main = Blueprint('main', __name__)

@main.route('/')
def home():
    
    all_articles = Articles.query.order_by(Articles.date.desc()).limit(50).all()
    total_articles = Articles.query.count()
    
    return render_template('home.html', history = all_articles, total = total_articles)


@main.route('/scrape', methods = ['POST'])
def scrape():
    
    repubblica_topic = ['politica', 'economia', 'cronaca', 'scuola', 'sport', 'cultura', 
                        'spettacoli', 'motori', 'design']
    
    df1 = euronews_scrap()
    df2 = repubblica_scrap(np.random.choice(repubblica_topic))
    
    
    df = pd.concat([df1, df2], ignore_index = True)
     
    for i in range(df.shape[0]):
        
        if any(df.loc[i,:] == ''):
            continue
        
        article_id = df.loc[i, 'id']
        
        # salta articoli già presenti
        if Articles.query.filter_by(article_id=article_id).first():
            continue
        
        
        article = Articles(article_id = article_id,
                           topic = df.loc[i, 'topic'],
                           abstract = df.loc[i, 'abstract'],
                           link = df.loc[i, 'link'],
                           date = datetime.strptime(df.loc[i, 'day_published'], "%d.%m.%Y"))
        
        db.session.add(article)
    
    db.session.commit()
    
    flash("News aggiornate con successo", category="success")
    
    return redirect(url_for('main.home'))
            
        
        