from flask import Flask, render_template, request, redirect, session, flash# import the class from friend.py
from flask_app.models.order import Order
from flask_app.models.user import User
from flask_app import app
from werkzeug.datastructures import ImmutableMultiDict
from datetime import *

import socket

@app.route('/add_order',methods=['POST'])
def report_sighting():
    stop_hack(request.form['user_id'],session['id'])
    # end of code block identifying and logging out the hacker
    
    if not validate_order( request.form):
        return render_template("/user/new_order.html")

    data = {
        'method':request.form['method'],
        'size':request.form['size'],
        'crust':request.form['crust'],
        'toppings': request.form['toppings'],
        'user_id': int(session['id'])
    }
    
    Order.save_order(data)    
    
    return redirect("/user/dashboard")

@app.route('/update_order',methods=['POST'])
def update_sighting():
    stop_hack(request.form['user_id'],session['id'])
    
    if not validate_order(request.form):
        
        return redirect(f"/user/edit_order/{request.form['order_id']}")
    
    data = {
        'id': request.form['order_id'],
        'method':request.form['method'],
        'size':request.form['size'],
        'crust':request.form['crust'],
        'toppings': request.form['toppings']
    }
    Order.update_order(data)
    
    return redirect("/user/dashboard")

@app.route('/delete_order',methods=['POST'])
def delete_sighting():
    stop_hack(request.form['user_id'],session['id'])
    
    data = {'id': request.form['order_id']}
    Order.delete_order(data)
    
    return redirect("/user/dashboard")

def stop_hack(sender_info, session_info):
    if int(sender_info) != int(session_info):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        log_data = {
            'hostname': hostname,
            'ip_address': ip_address,
            'id':session['id']
        }
        
        results = User.get_by_id(log_data)
        session.clear()
        
        print("Your hostname:",log_data['hostname'])
        print("Your IP Address is:",log_data['ip_address'])
        
        return render_template("final_warning.html",log_info=log_data,user_info=results)
    else:
        return False
    

def validate_order ( order ):
    is_valid = True
    
    if len(order['method']) < 1 or order['method'].isspace():
        flash("Method is blank","order")
        is_valid = False
            
    if len(order['size']) < 1 or order['size'].isspace():
        flash("Size is blank","order")
        is_valid = False
            
    if len(order['crust']) < 1 or order['crust'].isspace():
        flash("Crust is blank","order")
        is_valid = False
        
    if len(order['qty']) < 1 or order['qty'].isspace():
        flash("Quantity is less than 1","order")
        is_valid = False

    return is_valid