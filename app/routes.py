from flask import Flask, render_template, request, redirect, url_for, flash
from app.database import get_items, add_item, update_item, delete_item
from app.email_notification import send_email_notification
from app.scheduler import schedule_report

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    items = get_items()
    return render_template('inventory.html', items=items)

@app.route('/add-item', methods=['GET', 'POST'])
def add_item_route():
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        quantity = request.form.get('item_quantity')
        threshold = request.form.get('item_threshold')
        item_description = request.form.get('item_description')

        # Input validation to ensure all fields are filled
        if not item_name or not quantity or not threshold or not item_description:
            flash('All fields are required!', 'danger')
            return redirect(url_for('add_item_route'))

        # Convert quantity and threshold to integers
        try:
            quantity = int(quantity)
            threshold = int(threshold)
        except ValueError:
            flash('Quantity and Threshold must be numbers!', 'danger')
            return redirect(url_for('add_item_route'))

        add_item(item_name, quantity, threshold)  # Add item to the database
        flash('Item added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_item.html')

@app.route('/edit-item/<int:item_id>', methods=['GET', 'POST'])
def edit_item_route(item_id):
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        quantity = request.form.get('item_quantity')
        threshold = request.form.get('item_threshold')
        
        # Input validation to ensure all fields are filled
        if not item_name or not quantity or not threshold:
            flash('All fields are required!', 'danger')
            return redirect(url_for('edit_item_route', item_id=item_id))

        # Convert quantity and threshold to integers
        try:
            quantity = int(quantity)
            threshold = int(threshold)
        except ValueError:
            flash('Quantity and Threshold must be numbers!', 'danger')
            return redirect(url_for('edit_item_route', item_id=item_id))
        
        update_item(item_id, item_name, quantity, threshold)  # Update item in the database
        flash('Item updated successfully!', 'success')
        return redirect(url_for('index'))

    item = [item for item in get_items() if item['id'] == item_id][0]
    return render_template('edit_item.html', item=item)

@app.route('/delete-item/<int:item_id>')
def delete_item_route(item_id):
    delete_item(item_id)  # Delete item from the database
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/generate-report')
def generate_report_route():
    message = send_email_notification()  # Generate report and send email notification
    flash(message, 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    schedule_report()  # Schedule report generation
    app.run(debug=True)
