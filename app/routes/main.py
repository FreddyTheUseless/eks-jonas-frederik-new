import random
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from requests import Session, session
from sqlalchemy import null
from ..models.TeamsModel import Teams
from ..models.UsersModel import Users
from ..models.TournamentsModel import Tournaments
from ..models.TeamsUsersModel import teamsusers
from ..models.EventsModel import Events
from ..models.RegistrationsModel import Registrations
from ..models.MatchupsModel import Matchups
from .. import db
import numpy as np

main = Blueprint('main', __name__, template_folder='templates', static_folder='public')

def join_team(jt, ju):

    db.session.add(teamsusers(team_id=jt, user_id=ju))
    db.session.commit()    
        
def leave_team(lu):

    db.session.delete(teamsusers.query.filter_by(user_id=lu).first())
    db.session.commit()

def create_team(tn, td, to):    
    db.session.add(Teams(teamname=tn, teamdescription=td, teamowner=to))
    db.session.commit()
    
    current_id = Teams.query.filter_by(teamowner=current_user.id).first().id

    join_team(current_id, to)

def delete_team(oi):
    db.session.delete(Teams.query.filter_by(teamowner=oi).one())
    db.session.commit()

    leave_team(oi)

def create_event(en,s):
    db.session.add(Events(eventname=en, sponsor=s))
    db.session.commit()

def delete_event(ei):
    for n in Tournaments.query.filter_by(event_id=ei).all():
        for i in Registrations.query.filter_by(tournament_id=n.id).all():
            db.session.delete(i)
        for x in Matchups.query.filter_by(tournament_id=n.id).all():
            db.session.delete(x)
        db.session.delete(n)
    db.session.delete(Events.query.filter_by(id=ei).first())
    db.session.commit()


def create_tournament(ei,tn,v,g,s):
    db.session.add(Tournaments(event_id=ei,tournamentname=tn,venue=v,game=g,size=s))
    db.session.commit()

def delete_tournament(di):

    for i in Registrations.query.filter_by(tournament_id=di).all():
        db.session.delete(i)
    for n in Matchups.query.filter_by(tournament_id=di).all():
        db.session.delete(n)


    db.session.delete(Tournaments.query.filter_by(id=di).first())
    db.session.commit()
    

def join_tournament(ji, ui):
    db.session.add(Registrations(tournament_id=ji, user_id=ui))
    db.session.commit()   

def leave_tournament(li, ui):

    Registrations.query.filter_by(tournament_id=li, user_id=ui).delete()
    db.session.commit() 

def create_matchup(p, ti):
    
    mid_index = len(p) // 2

    players1 = p[:mid_index]
    players2 = p[mid_index:]

    for i, n in zip(players1, players2):

        print(i,n)
        db.session.add(Matchups(tournament_id=ti, user_id1=i, user_id2=n, winner=0))
        
    db.session.commit() 

 

    


# Landing

@main.route('/')

@login_required
def index():

    title = tournament
    events = Events.query.all()
    tournaments = Tournaments.query.all()

    return render_template('frontpage/frontpage.html', title=title, username=current_user.username, events=events, tournaments=tournaments)


# Profile

@main.route('/profile')
@login_required
def profile():
    title = "Profile"
    return render_template('profile/profile.html', title=title, username=current_user.username, email=current_user.email)


# Team Browse

@main.route('/browse')
@login_required
def browse():

    joinable = 1

    if teamsusers.query.filter_by(user_id=current_user.id).first() is not None:
        joinable = 0

    title = "Browse"

    teams = Teams.query.all()
    users = Users.query.all()
    tUsers = teamsusers.query.all()

    return render_template('team/browse.html', title=title, username=current_user.username, teams=teams, joinable=joinable, users=users, tUsers=tUsers)

@main.route('/browse', methods=['POST'])
def browse_post():
    team_id = request.form.get('team_id')

    join_team(team_id, current_user.id)

    return redirect(url_for('main.browse'))


# Team Create

@main.route('/manage')
@login_required
def manage():
    title = "Manage"

    teams = Teams.query.all()
    users = Users.query.all()
    tUsers = teamsusers.query.all()

    Team = null

    if teamsusers.query.filter_by(user_id=current_user.id).first() is not None: # User is in a team but does NOT own the team
        if Teams.query.filter_by(teamowner=current_user.id).first() is not None: # User is a team owner
            team_status = 1
            Team = Teams.query.filter_by(teamowner=current_user.id).first()
        else:
            Team_id = teamsusers.query.filter_by(user_id=current_user.id).first().team_id
            Team = Teams.query.filter_by(id=Team_id).first()
            team_status = 0
    else: 
        team_status = 2 # User is not in a team and does NOT own a team either


    return render_template('team/manage.html', title=title, username=current_user.username, team_status=team_status, Team=Team, teams=teams, users=users, tUsers=tUsers)

@main.route('/manage', methods=['POST'])
def manage_post():
    
    if request.form['button'] == 'CREATE':
        teamname = request.form.get('teamname')
        teamdescription = request.form.get('teamdescription')

        create_team(teamname, teamdescription, current_user.id)
    
        return redirect(url_for('main.manage'))
     
    elif request.form['button'] == 'DELETE':
        owner_id = request.form.get('owner_id')

        delete_team(owner_id)
        
        return redirect(url_for('main.manage'))

    elif request.form['button'] == 'LEAVE':
        leave_team(current_user.id)

        return redirect(url_for('main.manage'))

# Frontpage

@main.route('/frontpage')
@login_required
def frontpage():

    title= "Frontpage"

    return render_template('frontpage/frontpage.html', title=title, username=current_user.username)


# Terms

@main.route('/terms')
@login_required
def terms():
    title = "Terms of Use"
    return render_template('terms.html', title=title)


# Event

@main.route('/event')
@login_required
def event():
    title = "Event"

    
    tournaments = Tournaments.query.all()

    events = Events.query.all()

    event_status = 0

    if events:
        event_status = 1

    return render_template('event/event.html', title=title, username=current_user.username, events=events, event_status=event_status, tournaments=tournaments)

@main.route('/event', methods=['POST'])
def event_post():
    
    if request.form['button'] == 'CREATEEVENT':

        eventname = request.form.get('eventname')
        sponsor = request.form.get('sponsor')

        if eventname == '' or sponsor == None:
            flash('Please fill out the entire form!')            
            return redirect(url_for('main.event'))

        elif Events.query.filter_by(eventname=eventname).first() is not None:
            flash('This tournament does already exist')
            return redirect(url_for('main.event'))

        else:
            create_event(eventname,sponsor)
            return redirect(url_for('main.event'))

    elif request.form['button'] == 'CREATETOURNAMENT':
        event_id = request.form.get('event_id')
        tournamentname = request.form.get('tournamentname')
        venue = request.form.get('venue')
        game = request.form.get('game')
        size = request.form.get('size')

        if event_id == None or tournamentname == '' or venue == None or game == None or size == None:
            flash('Please fill out the entire form!')
            return redirect(url_for('main.event'))
        else:
            create_tournament(event_id,tournamentname,venue,game,size)
            return redirect(url_for('main.event'))
        
    elif request.form['button'] == 'DELETETOURNAMENT':

       

        t_delete_id = request.form.get('t_delete_id')

        delete_tournament(t_delete_id)
        return redirect(url_for('main.event'))


    elif request.form['button'] == 'DELETEEVENT':
        e_delete_id = request.form.get('e_delete_id')
        delete_event(e_delete_id)

        return redirect(url_for('main.event'))

        
# Tournament

@main.route('/tournament')
@login_required
def tournament():
    title = "Tournament"

    events = []
    ongoing_events = []
    tournaments = []
    ongoing_tournaments = []

    users = Users.query.all()
    registrations = Registrations.query.all()
    matchups = Matchups.query.all()


    for i in Tournaments.query.all():

        tournament_regs = []

        for x in Registrations.query.filter_by(tournament_id=i.id):
            tournament_regs.append(x)

        if len(tournament_regs) != i.size:
            tournaments.append(i)
        else:
            ongoing_tournaments.append(i)

            if Matchups.query.filter_by(tournament_id=i.id).first() is None:
            
                participants = []

                for n in tournament_regs:
                    participants.append(n.user_id)

                random.shuffle(participants)     
                create_matchup(participants, i.id)


        event_value = Events.query.filter_by(id=i.event_id).first()

        if event_value not in events and i in tournaments:
            events.append(event_value)

        if event_value not in events and i in ongoing_tournaments:
            ongoing_events.append(event_value)

    ongoing_events = list(dict.fromkeys(ongoing_events))


    return render_template('tournament/tournament.html', title=title, username=current_user.username, events=events, tournaments=tournaments, registrations=registrations, matchups=matchups, user_id=current_user.id, ongoing_tournaments=ongoing_tournaments, ongoing_events=ongoing_events, users=users)

  

@main.route('/tournament', methods=['POST'])
@login_required
def tournament_post():


    if request.form['button'] == 'JOINTOURNAMENT':

        join_id = request.form.get('join_id')
        join_tournament(join_id, current_user.id)

        

    elif request.form['button'] == 'LEAVETOURNAMENT':

        leave_id = request.form.get('leave_id')
        leave_tournament(leave_id, current_user.id)


    return redirect(url_for('main.tournament'))