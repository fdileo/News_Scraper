from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from app.models import Articles
from app import db
from app.statistics import bar_chart
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/articles', methods = ['GET'])
def views_articles():
    
    q = request.args.get('q')
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    
    query = Articles.query.order_by(Articles.id.asc())
    
    if q:
        query = query.filter(
            Articles.topic.like(f"%{q}%") |
            Articles.abstract.like(f"%{q}%")
        )
    
    if date_from:
        
        try:
            date_from = datetime.strptime(date_from, '%d.%m.%Y')
            query = query.filter(
                Articles.date >= date_from
            )
        except:
            pass
    
    if date_to:
        
        try:
            date_to = datetime.strptime(date_to, '%d.%m.%Y')
            query = query.filter(
                Articles.date <= date_to
            )
        except:
            pass
       
    all_articles = query.all()
    
    return jsonify([
        
        {"id" : a.id,
         "topic" : a.topic,
         "abstract" : a.abstract,
         "link" : a.link,
         "date" : a.date.strftime('%d-%m-%Y')}
        
        for a in all_articles
    ])
    

@views.route('/articles/<int:id>', methods = ['GET'])
def views_article_id(id:int):
    a = Articles.query.get_or_404(id)
    
    return jsonify( {
         "topic" : a.topic,
         "abstract" : a.abstract,
         "link" : a.link,
         "date" : a.date.strftime('%d-%m-%Y')} )
    

@views.route('/filter', methods = ['GET', 'POST'])
def filter_articles():
    
    if request.method == 'POST':
        
        key = request.form['key']
        start = request.form['start']
        end = request.form['end']
        
        params = {'q': key}

        start_date = None
        end_date = None

        if start:
            try:
                start_date = datetime.strptime(start, '%Y-%m-%d')
                params['from'] = start_date.strftime('%d.%m.%Y') 
            except ValueError:
                flash("Formato data iniziale non valido", category="error")

        if end:
            try:
                end_date = datetime.strptime(end, '%Y-%m-%d')
                params['to'] = end_date.strftime('%d.%m.%Y')
            except ValueError:
                flash("Formato data finale non valido", category="error")

        if start_date and end_date and start_date > end_date:
            flash("La data iniziale non può essere successiva alla finale", category="error")
            return render_template("filter.html")

        return redirect(url_for('views.views_articles', **params))

    return render_template('filter.html')


@views.route('/stat', methods = ['GET', 'POST'])
def statistics():
    
    all_articles = Articles.query.order_by(Articles.date.asc()).all()
    
    # Conteggio articoli di giornale per topic
    total_topics = [a.topic for a in all_articles]
    count_topics = []
    
    for topic in total_topics:
        count_topics.append(
            Articles.query.filter_by(topic = topic).count()
        )
        
    bar_chart(values = count_topics,
              labels = total_topics,
              filename = "bar_chart_topic"
              )
    
    # Conteggio articoli di giornale per date
    total_dates = [a.date for a in all_articles]
    count_dates = []
    
    for date in total_dates:
        count_dates.append(
            Articles.query.filter_by(date = date).count()
        )
        
    bar_chart(values = count_dates,
              labels = [date.strftime("%d %b") for date in total_dates],
              filename = "bar_chart_date"
              )
    
    total_articles = Articles.query.count()
    articles_filter = None
    
    if request.method == 'POST':
        
        min = request.form['min']
        max = request.form['max']
        
        try:
            min = int(min)
            max = int(max) 
        except:
            print('Ci arrivo qui?')
            flash('Si prega di inserire numeri interi', category = "error")
            return redirect(url_for('views.statistics'))
            
        if min > max:
            flash('Parametri non inseriti correttamente', category = "error")
            return redirect(url_for('views.statistics'))
        
        articles_filter = Articles.query.filter(
            Articles.id.between(min, max)
        ).all()
        
        
    return render_template('stat.html', total = total_articles, filter = articles_filter)
        
        