from flask import Flask, render_template, request, redirect, url_for, flash  # Added flash for notifications
from app.database import get_items, add_item, update_item, delete_item
from app.email_notification import send_email_notification
from app.scheduler import schedule_report

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

@app.route('/')
def index():
    items = get_items()  # Fetch items from the database
    return render_template('inventory.html', items=items)  # Render inventory page with items

@app.route('/add-item', methods=['GET', 'POST'])
def add_item_route():
    if request.method == 'POST':
        item_name = request.form.get('item_name')  # Use get to avoid KeyError
        quantity = request.form.get('item_quantity')  # Use get to avoid KeyError
        item_description = request.form.get('item_description')  # Use get to avoid KeyError
        
        # Input validation
        if not item_name or not quantity or not item_description:
            flash('All fields are required!', 'danger')  # Flash error if inputs are invalid
            return redirect(url_for('add_item_route'))  # Redirect to add item page

        # Add item to the database
        add_item(item_name, quantity, item_description)
        flash('Item added successfully!', 'success')  # Flash success message
        return redirect(url_for('index'))  # Redirect to index page

    return render_template('add_item.html')  # Render the add item form

@app.route('/edit-item/<int:item_id>', methods=['GET', 'POST'])
def edit_item_route(item_id):
    if request.method == 'POST':
        item_name = request.form.get('item_name')  # Use get to avoid KeyError
        quantity = request.form.get('item_quantity')  # Use get to avoid KeyError
        item_description = request.form.get('item_description')  # Use get to avoid KeyError

        # Input validation
        if not item_name or not quantity or not item_description:
            flash('All fields are required!', 'danger')  # Flash error if inputs are invalid
            return redirect(url_for('edit_item_route', item_id=item_id))  # Redirect to edit page

        # Update item in the database
        update_item(item_id, item_name, quantity, item_description)
        flash('Item updated successfully!', 'success')  # Flash success message
        return redirect(url_for('index'))  # Redirect to index page

    # If GET request, fetch the item to edit
    item = get_item(item_id)  # Ensure you have a function to fetch an item by ID
    return render_template('edit_item.html', item=item)  # Render the edit item form

@app.route('/delete-item/<int:item_id>')
def delete_item_route(item_id):
    delete_item(item_id)  # Delete the item with the given ID from the database
    flash('Item deleted successfully!', 'success')  # Flash success message
    return redirect(url_for('index'))  # Redirect back to index

@app.route('/generate-report')
def generate_report_route():
    send_email_notification()  # Trigger report generation and email notification
    flash('Report generated and email sent.', 'info')  # Inform user about the action
    return redirect(url_for('index'))  # Redirect back to index

if __name__ == '__main__':
    schedule_report()  # Schedule any periodic tasks if needed
    app.run(debug=True)  # Run the application in debug mode
